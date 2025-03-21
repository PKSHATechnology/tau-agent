import json
from typing import TypedDict, Literal


class AnthropicLLMConfig(TypedDict):
    provider: Literal["anthropic"]
    model: str
    anthropic_api_key: str


type LLMConfig = AnthropicLLMConfig


class MCPServerConfig(TypedDict):
    name: str
    command: str
    args: list[str]
    env: dict[str, str]


class MemoryMessageStoreConfig(TypedDict):
    type: Literal["memory"]


type MessageStoreConfig = MemoryMessageStoreConfig


class Config(TypedDict):
    llm: LLMConfig
    mcp_servers: list[MCPServerConfig]
    message_store: MessageStoreConfig


def load_config(path: str) -> Config:
    with open(path, "r") as f:
        config = json.load(f)

    return Config(**config)
