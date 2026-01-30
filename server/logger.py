import logging
import sys

logger = logging.getLogger("poker_bot_server")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)

ch.setFormatter(formatter)

logger.addHandler(ch)