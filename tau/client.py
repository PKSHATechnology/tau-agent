import json
import logging
import os
import sys
from contextlib import AsyncExitStack

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, *, config_path="config.json", logger=None):
        self.exit_stack = AsyncExitStack()
        self.config_path = config_path
        self._load_config()
        self.llm = Anthropic(api_key=self.config["llm"]["anthropicApiKey"])

        self.mcp_sessions: dict[str, ClientSession] = {}
        self.available_tools = list()
        self.tool_session = dict()
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

    def _load_config(self):
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

    async def connect_mcp_servers(self):
        mcp_servers = self.config.get("mcpServers", {})

        for name, config in mcp_servers.items():
            self.logger.debug(f"Connecting to MCP server: {name}")

            env = {**os.environ, **config.get("env", {})}
            server_params = StdioServerParameters(
                command=config["command"], args=config.get("args", []), env=env
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport))
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

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        response = self.llm.messages.create(
            model=self.config["llm"]["model"],
            max_tokens=1000,
            messages=messages,
            tools=self.available_tools,
        )

        final_text = []

        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                result = await self.mcp_sessions[self.tool_session[tool_name]].call_tool(
                    tool_name, tool_args
                )
                self.logger.debug(
                    f"[Calling tool {tool_name} of {self.tool_session[tool_name]} with args {tool_args}]"
                )

                if hasattr(content, "text") and content.text:
                    messages.append({"role": "assistant", "content": content.text})
                messages.append({"role": "user", "content": result.content})

                response = self.llm.messages.create(
                    model=self.config["llm"]["model"],
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        self.logger.debug("Starting chat loop")
        while True:
            try:
                self.logger.debug("Waiting for input...")
                query = sys.stdin.readline().strip()
                self.logger.debug(f"Received input: {query}")

                if query == "\\q":
                    self.logger.debug("Quit command received, exiting...")
                    break
                if not query:
                    self.logger.debug("Empty input, continuing...")
                    continue

                self.logger.debug("Processing query...")
                out = await self.process_query(query)
                sys.stdout.write(out + "\n")
                sys.stdout.flush()
            except Exception as e:
                self.logger.error(f"Error in chat loop: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()
