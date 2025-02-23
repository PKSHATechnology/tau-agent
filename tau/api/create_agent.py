"""Create agent endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from tau.celery import start_agent

router = APIRouter()


class Tool(BaseModel):
    name: str
    args: None = None


class CreateAgentRequest(BaseModel):
    """Request model for creating an agent."""

    tools: list[Tool]
    system_prompt: str


@router.post("/agents")
async def create_agent(request: CreateAgentRequest) -> dict[str, str]:
    """Create a new agent.

    Args:
        request: The request containing tools and system prompt for the agent.

    Returns:
        dict[str, str]: A dictionary containing the agent ID.
        The agent_id is the Celery task ID that created the agent.
    """

    task = start_agent.delay(
        [t.model_dump() for t in request.tools], request.system_prompt
    )
    return {"agent_id": task.id}
