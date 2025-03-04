from typing import Any

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool, Tool
from langgraph.prebuilt import create_react_agent

from tau.agent import AgentConfig
from tau.agent.llms import get_llm


class Agent:
    def __init__(self, config: AgentConfig):
        self._agent = create_react_agent(
            model=get_llm(config.model),
            tools=[configure_tool(t.tool, t.args) for t in config.tools],
        )
        self._messages: list[SystemMessage | HumanMessage] = [
            SystemMessage(content=config.prompt)
        ]

    def send_message(self, message: str) -> str:
        self._messages.append(HumanMessage(content=message))
        result = self._agent.invoke({"messages": self._messages})
        self._messages = result["messages"]
        return self._messages[-1].content



def _configure_tavily() -> BaseTool:
    return TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )

class SubAgent(Tool):
    def __init__(self, name: str, agent: Agent, description: str):
        self.agent = agent
        self.name = name
        self.description = description
        super().__init__(
            name=name,
            func=self._send_message,
            description=description,
        )

    def _send_message(self, message: str) -> str:
        return self.agent.send_message(message)

def _configure_sub_agent(name: str, agent: dict, description: str) -> BaseTool:
    agent = Agent(AgentConfig(**agent))
    return Tool(
        name=name,
        func=lambda x: agent.send_message(x),
        description=description,
    )


_tools = {
    "tavily": _configure_tavily,
    "agent": _configure_sub_agent
}


def configure_tool(name: str, args: dict | None) -> BaseTool:
    if args is None:
        args = {}
    return _tools[name](**args)
