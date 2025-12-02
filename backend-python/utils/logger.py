import logging
import json
from datetime import datetime

# Create logs directory if it doesn't exist
import os
os.makedirs('logs', exist_ok=True)

# Configure file logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_data(title, data):
    """Log data to file with nice formatting"""
    logger.info(f"\n{'='*60}\n{title}\n{'='*60}")
    if isinstance(data, (dict, list)):
        logger.info(json.dumps(data, indent=2, default=str))
    else:
        logger.info(str(data))
    logger.info('='*60)
