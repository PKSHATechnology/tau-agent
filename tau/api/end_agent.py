"""End agent endpoint."""

from fastapi import APIRouter

from tau.celery import close_agent

router = APIRouter()


@router.put("/agents/{agent_id}/end")
async def end_agent(agent_id: str) -> dict[str, str]:
    """End an agent.

    Args:
        agent_id (str): The ID of the agent to end.

    Returns:
        dict[str, str]: A dictionary containing the status of the operation.
    """

    close_agent.delay(agent_id)
    return {"status": "ok"}
