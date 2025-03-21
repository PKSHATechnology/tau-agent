import logging
import os
from contextlib import AsyncExitStack
from datetime import timedelta
from typing import Optional

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tau.config import LLMConfig, MCPServerConfig
from tau.message_store import MessageStore
from tau.types import SessionID


class MCPClient:
    def __init__(
        self,
        *,
        llm_config: LLMConfig,
        message_store: MessageStore,
        logger: Optional[logging.Logger] = None,
    ):
        self.exit_stack = AsyncExitStack()
        self.llm = Anthropic(api_key=llm_config["anthropic_api_key"])
        self.model = llm_config["model"]
        self.message_store = message_store

        self.mcp_sessions: dict[str, ClientSession] = {}
        self.available_tools = list()
        self.tool_session = dict()
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

    async def connect_mcp_servers(self, mcp_servers: list[MCPServerConfig]):
        for config in mcp_servers:
            name = config["name"]
            self.logger.debug(f"Connecting to MCP server: {name}")

            env = {**os.environ, **config.get("env", {})}
            server_params = StdioServerParameters(
                command=config["command"], args=config.get("args", []), env=env
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            session = await self.exit_stack.enter_async_context(
                ClientSession(*stdio_transport, read_timeout_seconds=timedelta(seconds=10))
            )
            await session.initialize()

            self.mcp_sessions[name] = session

        for session_name, session in self.mcp_sessions.items():
            res = await session.list_tools()
            for tool in res.tools:
                self.available_tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    }
                )
                self.tool_session[tool.name] = session_name

    async def invoke_message(self, session_id: SessionID, message: str) -> str:
        messages = self.message_store.load(session_id)

        messages.append({"role": "user", "content": message})
        result_text = []

        # Initial response
        response = self.llm.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages,
            tools=self.available_tools,
        )
        self.logger.debug(f"Initial response: {response.content}")

        # Process the response, which may contain multiple tool calls
        while True:
            has_tool_use = False

            messages.append({"role": "assistant", "content": response.content})

            for content in response.content:
                if content.type == "text":
                    result_text.append(content.text)
                elif content.type == "tool_use":
                    has_tool_use = True
                    tool_id = content.id
                    tool_name = content.name
                    tool_args = content.input

                    # Call the tool
                    self.logger.debug(
                        f"Calling tool {tool_name} of {self.tool_session[tool_name]} with args {tool_args}"
                    )

                    try:
                        tool_call_result = await self.mcp_sessions[
                            self.tool_session[tool_name]
                        ].call_tool(tool_name, tool_args)

                        # Add the tool result to the conversation
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": c.text,
                                    }
                                    for c in tool_call_result.content
                                ],
                            }
                        )
                    except Exception as e:
                        self.logger.error(f"Error calling tool {tool_name}: {e}")
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": f"Error calling tool: {e}",
                                    }
                                ],
                            }
                        )

                    # Get a new response from the LLM with the updated conversation
                    response = self.llm.messages.create(
                        model=self.model,
                        max_tokens=1000,
                        messages=messages,
                        tools=self.available_tools,
                    )

            # If no tool use was found, we're done
            if not has_tool_use:
                break

        self.message_store.save(session_id, messages)

        return "\n".join(result_text)

    async def cleanup(self):
        await self.exit_stack.aclose()
