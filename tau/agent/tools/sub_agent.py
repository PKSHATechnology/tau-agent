from langchain_core.tools import BaseTool, Tool

from tau.agent.core.agent import Agent, AgentConfig


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


def configure_sub_agent(name: str, description: str, agent: dict, agent_id: str) -> BaseTool:
    agent = Agent(AgentConfig(**agent), agent_id)
    return Tool(
        name=name,
        func=lambda x: agent.send_message(x),
        description=description,
    )
