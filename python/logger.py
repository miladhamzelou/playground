import logging
import sys

LOG_FORMAT = '%(asctime)s %(levelname) 8s: [%(filename)s:%(lineno)d] [%(processName)s:%(process)d %(threadName)s] - %(message)s'
DATE_FORMAT = '[%Y-%m-%d %H:%M:%S]'


def get_logger(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = get_logger(__name__)
logger.warning("test msg")
