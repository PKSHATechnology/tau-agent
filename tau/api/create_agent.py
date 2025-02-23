"""Create agent endpoint."""

from fastapi import APIRouter

from tau.celery import start_agent

router = APIRouter()


@router.post("/v1/agents")
async def create_agent() -> dict[str, str]:
    """Create a new agent.

    Returns:
        dict[str, str]: A dictionary containing the agent ID.
        The agent_id is the Celery task ID that created the agent.
    """
    task = start_agent.delay()
    return {"agent_id": task.id}
