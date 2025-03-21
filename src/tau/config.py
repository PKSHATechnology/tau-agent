import json
from typing import TypedDict, Literal


class AnthropicLLMConfig(TypedDict):
    provider: Literal["anthropic"]
    model: str
    anthropic_api_key: str


class AnthropicBedrockLLMConfig(TypedDict):
    provider: Literal["anthropic_bedrock"]
    model: str
    aws_secret_key: str | None
    aws_access_key: str | None
    aws_region: str | None
    aws_profile: str | None
    aws_session_token: str | None


type LLMConfig = AnthropicLLMConfig | AnthropicBedrockLLMConfig


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
