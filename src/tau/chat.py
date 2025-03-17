import sys
import uuid

from tau.client import MCPClient


async def start_chat(client: MCPClient):
    """Run an interactive chat loop with the LLM.

    Args:
        client: The MCPClient instance to use for message processing
    """
    client.logger.debug("Starting chat loop")
    session_id = uuid.uuid4().hex
    client.logger.debug(f"New Session: {session_id}")
    while True:
        client.logger.debug("Waiting for input...")
        query = sys.stdin.readline().strip()
        client.logger.debug(f"Received input: {query}")

        if not query:
            client.logger.debug("Empty input, continuing...")
            continue

        if query == "\\q":
            client.logger.debug("Quit command received, exiting...")
            break

        if query == "\\n":
            session_id = uuid.uuid4().hex
            client.logger.debug(f"New Session command received, {session_id}")
            continue

        client.logger.debug("Processing query...")
        out = await client.invoke_message(session_id, query)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
