import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    logger = logging.getLogger("llm_brain")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        f"{LOG_DIR}/brain.log",
        maxBytes=5_000_000,
        backupCount=3
    )

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
