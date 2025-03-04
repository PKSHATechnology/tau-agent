from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from tau.agent import SupportedModels


def get_llm(name: SupportedModels):
    if name in ["gpt-4o", "gpt-4o-mini", "o3-mini", "o1-mini", "o1", ]:
        return ChatOpenAI(model=name, temperature=0)
    if name == "claude-3-7-sonnet":
        return ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0)
    if name == "claude-3-5-sonnet":
        return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    if name == "claude-3-5-haiku":
        return ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    else:
        raise ValueError(f"Unsupported model: {name}")
