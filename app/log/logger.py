# app/core/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create a rotating file handler (max 5 MB per file, keep 5 backups)
handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "llm_requests.log"), maxBytes=5*1024*1024, backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[handler]
)

llm_logger = logging.getLogger("llm_logger")
