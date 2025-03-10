from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from tau.agent.core.llms import SupportedModels, get_llm
from tau.agent.core.tools import configure_tool


class AgentToolConfig(BaseModel):
    tool: str
    args: dict = None


class AgentConfig(BaseModel):
    model: SupportedModels
    prompt: str
    tools: list[AgentToolConfig]


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
