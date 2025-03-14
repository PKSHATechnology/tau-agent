from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from tau.agent.core.llms import SupportedModels, get_llm
from tau.agent.core.tools import configure_tool


class AgentToolConfig(BaseModel):
    tool: str
    args: dict = {}


class AgentConfig(BaseModel):
    model: SupportedModels
    prompt: str
    tools: list[AgentToolConfig]


class Agent:
    def __init__(self, config: AgentConfig, agent_id: str):
        self.config = config
        self._react_agent = create_react_agent(
            model=get_llm(config.model),
            tools=[configure_tool(t.tool, t.args, agent_id) for t in config.tools],
        )
        self.messages: list[SystemMessage | HumanMessage] = [SystemMessage(content=config.prompt)]

    def send_message(self, message: str) -> str:
        self.messages.append(HumanMessage(content=message))
        result = self._react_agent.invoke({"messages": self.messages})
        self.messages = result["messages"]
        return self.messages[-1].content
