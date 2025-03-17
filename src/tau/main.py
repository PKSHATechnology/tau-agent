import argparse
import asyncio
import json
import logging
import sys

from tau.client import MCPClient
from tau.message_store import create_message_store
from tau.chat import start_chat

logger = logging.getLogger("tau")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


async def async_main():
    parser = argparse.ArgumentParser(description="Tau MCP Client")
    parser.add_argument(
        "-c",
        "--config",
        default="config.json",
        help="Path to the configuration file (default: config.json)",
    )
    args = parser.parse_args()

    # Load configuration from file
    with open(args.config, "r") as f:
        config = json.load(f)

    message_store = create_message_store(config["message_store"])
    client = MCPClient(llm_config=config["llm"], message_store=message_store, logger=logger)
    try:
        await client.connect_mcp_servers(config["mcp_servers"])
        await start_chat(client)
    finally:
        await client.cleanup()


def main():
    """Entry point for the application."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
