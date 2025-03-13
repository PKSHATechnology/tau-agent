"""Create agent endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from tau.agent import AgentConfig
from tau.worker.celery import start_agent

router = APIRouter()


class CreateAgentRequest(BaseModel):
    agent: AgentConfig


@router.post("/agents")
async def create_agent(request: CreateAgentRequest) -> dict[str, str]:
    """Create a new agent.

    Args:
        request: The request containing tools and system prompt for the agent.

    Returns:
        dict[str, str]: A dictionary containing the agent ID.
        The agent_id is the Celery task ID that created the agent.
    """

    task = start_agent.delay(request.agent.model_dump())
    return {"agent_id": task.id}
