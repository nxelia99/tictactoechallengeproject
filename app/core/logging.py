import logging
from app.core.config import Config

# Logging configuration
def setup_logging():
    logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')