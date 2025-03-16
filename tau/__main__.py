import asyncio
import logging

from tau.client import MCPClient

logger = logging.getLogger("tau")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


async def main():
    c = MCPClient(logger=logger)
    try:
        await c.connect_mcp_servers()
        await c.chat_loop()
    finally:
        await c.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
