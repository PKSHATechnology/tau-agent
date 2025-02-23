import os
from typing import Callable

from celery import Celery

from tau.agent import Agent

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
def start_agent(self):
    agent = Agent()
    agents[self.request.id] = agent
    return self.request.id


@app.task
def invoke_agent(task_id, f: Callable[[Agent], Agent]):
    agent = agents.get(task_id)
    if task_id in agents:
        agents[task_id] = f(agent)
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
