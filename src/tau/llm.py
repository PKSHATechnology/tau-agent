import abc

from anthropic import Anthropic, AnthropicBedrock
from anthropic.types import Message

from tau.config import AnthropicLLMConfig, LLMConfig, AnthropicBedrockLLMConfig


class LLM(abc.ABC):
    def invoke(self, messages: list[dict], tools: list) -> Message:
        raise NotImplementedError


class AnthropicLLM(LLM):
    def __init__(self, config: AnthropicLLMConfig):
        self.model = config.model
        self.llm = Anthropic(api_key=config.anthropic_api_key)

    def invoke(self, messages: list[dict], tools: list) -> Message:
        return self.llm.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages,
            tools=tools,
        )


class AnthropicBedrockLLM(LLM):
    def __init__(self, config: AnthropicBedrockLLMConfig):
        self.model = config.model
        self.llm = AnthropicBedrock(
            aws_secret_key=config.aws_secret_key,
            aws_access_key=config.aws_access_key,
            aws_region=config.aws_region,
            aws_profile=config.aws_profile,
            aws_session_token=config.aws_session_token,
        )

    def invoke(self, messages: list[dict], tools: list) -> Message:
        return self.llm.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages,
            tools=tools,
        )


def create_llm(config: LLMConfig) -> LLM:
    if config.provider == "anthropic":
        return AnthropicLLM(config)
    elif config.provider == "anthropic_bedrock":
        return AnthropicBedrockLLM(config)
    else:
        raise ValueError(f"Unknown LLM provider: {config.provider}")
