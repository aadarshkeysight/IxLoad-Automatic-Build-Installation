import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            TimedRotatingFileHandler(log_file, when='midnight', backupCount=7, encoding='utf-8')
        ]
    )

def get_logger(name):
    return logging.getLogger(name)
