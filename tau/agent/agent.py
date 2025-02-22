import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import Tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    temperature=0,
)


class Agent:
    def __init__(self, tools: list[Tool], system_prompt: str):
        self._agent = create_react_agent(
            model=llm,
            tools=tools,
        )
        self._messages = [SystemMessage(content=system_prompt)]

    def send_message(self, message: str):
        self._messages.append(HumanMessage(content=message))
        result = self._agent.invoke({"messages": self._messages})
        self._messages = result["messages"]
        return self._messages[-1].content
