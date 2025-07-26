# app/logger.py

import logging

logger = logging.getLogger("creative_agent")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if reloaded
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
