"""Ask agent endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/v1/agents/{agent_id}/ask")
async def ask_agent(agent_id: str) -> dict[str, str]:
    """Ask a question to an agent.

    Args:
        agent_id (str): The ID of the agent to ask.

    Returns:
        dict[str, str]: A dictionary containing the agent's response.
    """
    # TODO: Implement agent question handling
    return {"response": "dummy response"}
