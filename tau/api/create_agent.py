"""Create agent endpoint."""

from fastapi import APIRouter

from tau.worker import create_agent as create_agent_task

router = APIRouter()


@router.post("/v1/agents")
async def create_agent() -> dict[str, str]:
    """Create a new agent.

    Returns:
        dict[str, str]: A dictionary containing the agent ID.
        The agent_id is the Celery task ID that created the agent.
    """
    task = create_agent_task.delay()
    return {"agent_id": task.id}
