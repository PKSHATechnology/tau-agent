from typing import Literal

from pydantic import BaseModel


class AgentTool(BaseModel):
    tool: str
    args: dict = None


SupportedModels = Literal[
    "gpt-4o", "gpt-4o-mini", "o3-mini", "o1-mini", "o1",
    "claude-3-7-sonnet", "claude-3-5-sonnet", "claude-3-5-haiku"
]


class AgentConfig(BaseModel):
    model: SupportedModels
    prompt: str
    tools: list[AgentTool]
