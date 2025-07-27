# app/logger.py

import logging

# Create a module-level logger for the Creative Agent application
logger = logging.getLogger("creative_agent")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers in case of reload (e.g., during development)
if not logger.hasHandlers():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
    logger.addHandler(stream_handler)
