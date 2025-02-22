import os
from celery import Celery
from dotenv import load_dotenv
from tau.agent import Agent
from typing import Callable

# Load environment variables from .env file
load_dotenv()

# Get Redis connection settings from environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_db = os.getenv("REDIS_DB", "0")

# Configure Redis URLs for broker and backend
redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"

# Create Celery application
celery_app = Celery(
    "tau",
    broker=redis_url,
    backend=redis_url,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
)

agents = {}


@celery_app.task(bind=True)
def create_agent(self):
    agent = Agent()
    agents[self.request.id] = agent
    return self.request.id


@celery_app.task
def invoke_agent(task_id, f: Callable[[Agent], None]):
    agent = agents.get(task_id)
    if agent:
        f(agent)
    else:
        raise AgentNotFoundError("Agent not found.")


@celery_app.task
def close_agent(task_id):
    if task_id in agents:
        del agents[task_id]
        return "Agent ended."
    else:
        raise AgentNotFoundError("Agent not found.")


class AgentNotFoundError(Exception):
    pass
