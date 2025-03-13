import os
import pickle

import httpx
import redis
from celery import Celery

from tau.agent import Agent, AgentConfig

redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]
redis_url = f"redis://{redis_host}:{redis_port}"

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

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)


@app.task(bind=True)
def start_agent(self, config: dict):
    agent = Agent(AgentConfig(**config))
    _set_agent(self.request.id, agent)
    return self.request.id


@app.task
def invoke_agent(agent_id, message: str, callback_url: str):
    agent = _get_agent(agent_id)
    if agent is not None:
        reply = agent.send_message(message)
        print(reply)
        with httpx.Client() as client:
            response = client.post(
                callback_url,
                json={"agent_id": agent_id, "result": "ok", "content": reply}
            )
            response.raise_for_status()
        _set_agent(agent_id, agent)
    else:
        raise AgentNotFoundError("Agent not found.")


@app.task
def close_agent(task_id):
    _del_agent(task_id)


def _redis_keys(agent_id):
    return agent_id + "_config", agent_id + "_messages"


def _del_agent(agent_id):
    config_key, messages_key = _redis_keys(agent_id)
    redis_client.delete(config_key)
    redis_client.delete(messages_key)


def _get_agent(agent_id):
    config_key, messages_key = _redis_keys(agent_id)
    config_obj = redis_client.get(config_key)
    messages_obj = redis_client.get(messages_key)
    if config_obj is not None and messages_obj is not None:
        config = pickle.loads(config_obj)
        messages = pickle.loads(messages_obj)
        agent = Agent(config)
        agent.messages = messages
        return agent
    else:
        return None


def _set_agent(agent_id, agent):
    config_key, messages_key = _redis_keys(agent_id)
    config_obj = pickle.dumps(agent.config)
    messages_obj = pickle.dumps(agent.messages)
    redis_client.set(config_key, config_obj)
    redis_client.set(messages_key, messages_obj)


class AgentNotFoundError(Exception):
    pass
