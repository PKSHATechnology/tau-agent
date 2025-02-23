"""Create agent endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from tau.agent.tools import configure_tool
from tau.celery import start_agent

router = APIRouter()


class Tool(BaseModel):
    name: str
    args: dict[str, str]


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

    tools = list()

    for t in request.tools:
        try:
            ct = configure_tool(t.name, t.args)
            tools.append(ct)
        except Exception:
            pass

    task = start_agent.delay(tools=tools, system_prompt=request.system_prompt)
    return {"agent_id": task.id}
