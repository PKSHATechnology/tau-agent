"""End agent endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.put("/v1/agents/{agent_id}/end")
async def end_agent(agent_id: str) -> dict[str, str]:
    """End an agent.

    Args:
        agent_id (str): The ID of the agent to end.

    Returns:
        dict[str, str]: A dictionary containing the status of the operation.
    """
    # TODO: Implement agent termination
    return {"status": "ok"}
