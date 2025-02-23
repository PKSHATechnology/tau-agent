import httpx
from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

from tau.agent import Agent
from tau.celery import invoke_agent

router = APIRouter()


class AskAgentRequest(BaseModel):
    """Request model for ask agent endpoint."""

    message: str
    callback_url: HttpUrl


@router.post("/v1/agents/{agent_id}/ask")
async def ask_agent(agent_id: str, request: AskAgentRequest) -> dict[str, str]:
    """Ask a question to an agent.

    Args:
        agent_id (str): The ID of the agent to ask.
        request (AskAgentRequest): The request containing message and callback URL.

    Returns:
        dict[str, str]: A dictionary containing the task ID.
    """

    def f(agent: Agent) -> Agent:
        result = agent.send_message(request.message)
        with httpx.Client() as client:
            response = client.post(
                request.callback_url, json={"agent_id": agent_id, "result": result}
            )
            response.raise_for_status()
        return agent

    invoke_agent.delay(agent_id, f)

    return {"status": "ok"}
