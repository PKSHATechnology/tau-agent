import json
from typing import Literal, Union
from pydantic import BaseModel


class AnthropicLLMConfig(BaseModel):
    provider: Literal["anthropic"]
    model: str
    anthropic_api_key: str


class AnthropicBedrockLLMConfig(BaseModel):
    provider: Literal["anthropic_bedrock"]
    model: str
    aws_secret_key: str | None = None
    aws_access_key: str | None = None
    aws_region: str | None = None
    aws_profile: str | None = None
    aws_session_token: str | None = None


LLMConfig = Union[AnthropicLLMConfig, AnthropicBedrockLLMConfig]


class MCPServerConfig(BaseModel):
    name: str
    command: str
    args: list[str] = []
    env: dict[str, str] = {}


class MemoryMessageStoreConfig(BaseModel):
    type: Literal["memory"]


MessageStoreConfig = MemoryMessageStoreConfig


class Config(BaseModel):
    llm: LLMConfig
    mcp_servers: list[MCPServerConfig]
    message_store: MessageStoreConfig


def load_config(path: str) -> Config:
    with open(path, "r") as f:
        config_data = json.load(f)

    return Config.model_validate(config_data)
