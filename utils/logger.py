import logging
import sys


def setup_logger():
    logger = logging.getLogger("failure_agent")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "\n[%(levelname)s] %(asctime)s | %(message)s",
        "%H:%M:%S"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = setup_logger()
