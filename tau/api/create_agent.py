"""Create agent endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/v1/agents")
async def create_agent() -> dict[str, str]:
    """Create a new agent.

    Returns:
        dict[str, str]: A dictionary containing the agent ID.
    """
    # TODO: Implement agent creation
    return {"agent_id": "dummy"}
