import argparse
import asyncio
import json
import sys
import uuid

from tau.client import MCPClient
from tau.config import load_config
from tau.llm import create_llm
from tau.logger import logger
from tau.message_store import create_message_store


async def _chat(client: MCPClient):
    session_id = uuid.uuid4().hex
    client.logger.debug(f"New Session: {session_id}")
    while True:
        client.logger.debug("Waiting for input...")
        query = sys.stdin.readline().strip()

        if not query:
            continue

        if query == "\\q":
            client.logger.debug("Quit command received, exiting...")
            break

        if query == "\\n":
            session_id = uuid.uuid4().hex
            client.logger.debug(f"New Session command received, {session_id}")
            continue

        out = await client.invoke_message(session_id, query)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()


async def _json_server(client: MCPClient):
    while True:
        client.logger.debug("Waiting for input...")
        query = sys.stdin.readline().strip()

        if not query:
            continue

        try:
            d = json.loads(query)

            q_type = d["type"]

            if q_type == "message":
                out = await client.invoke_message(d["session_id"], d["content"])
                sys.stdout.write(json.dumps({"result": "success", "message": out}))
                sys.stdout.flush()
            elif q_type == "quit":
                client.logger.debug("Quit command received, exiting...")
                break

        except Exception as e:
            client.logger.error(f"Error: {e}")

            sys.stdout.write(json.dumps({"result": "error", "message": str(e)}))
            sys.stdout.flush()
            continue


async def _main(handler):
    parser = argparse.ArgumentParser(description="Tau MCP Client")
    parser.add_argument(
        "-c",
        "--config",
        default="config.json",
        help="Path to the configuration file (default: config.json)",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    llm = create_llm(config.llm)
    message_store = create_message_store(config.message_store)
    client = MCPClient(llm=llm, message_store=message_store, logger=logger)
    try:
        await client.connect_mcp_servers(config.mcp_servers)
        await handler(client)
    finally:
        await client.cleanup()


def chat():
    asyncio.run(_main(_chat))


def json_server():
    asyncio.run(_main(_json_server))


if __name__ == "__main__":
    chat()
