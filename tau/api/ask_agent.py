from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

from tau.celery import invoke_agent

router = APIRouter()


class AskAgentRequest(BaseModel):
    """Request model for ask agent endpoint."""

    message: str
    callback_url: HttpUrl


@router.post("/agents/{agent_id}/ask")
async def ask_agent(agent_id: str, request: AskAgentRequest) -> dict[str, str]:
    """Ask a question to an agent.

    Args:
        agent_id (str): The ID of the agent to ask.
        request (AskAgentRequest): The request containing message and callback URL.

    Returns:
        dict[str, str]: A dictionary containing the task ID.
    """
    invoke_agent.delay(agent_id, request.message, str(request.callback_url))

    return {"status": "ok"}
