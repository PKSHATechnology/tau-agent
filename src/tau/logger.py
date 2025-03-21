import logging
import sys

logger = logging.getLogger("tau")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
