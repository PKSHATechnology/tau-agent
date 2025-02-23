import os

import httpx
from celery import Celery
from typing import Any
from tau.agent import Agent
from tau.agent.tools import configure_tool

redis_url = os.environ["REDIS_URL"]

# Create Celery application
app = Celery(
    "tau",
    broker=redis_url,
    backend=redis_url,
)

# Configure Celery
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

agents = {}


@app.task(bind=True)
def start_agent(self, tool_configs: list[dict[str, Any]], system_prompt):
    tools = list()

    for t in tool_configs:
        try:
            tools.append(configure_tool(t["name"], t["args"]))
        except Exception as e:
            print(e)

    agent = Agent(tools, system_prompt)
    agents[self.request.id] = agent
    return self.request.id


@app.task
def invoke_agent(agent_id, message: str, callback_url: str):
    agent = agents.get(agent_id)
    if agent is not None:
        reply = agent.send_message(message)
        print(reply)
        with httpx.Client() as client:
            response = client.post(
                callback_url, json={"agent_id": agent_id, "result": "ok", "content": reply}
            )
            response.raise_for_status()
        agents[agent_id] = agent
    else:
        raise AgentNotFoundError("Agent not found.")


@app.task
def close_agent(task_id):
    if task_id in agents:
        del agents[task_id]
    else:
        raise AgentNotFoundError("Agent not found.")


class AgentNotFoundError(Exception):
    pass
