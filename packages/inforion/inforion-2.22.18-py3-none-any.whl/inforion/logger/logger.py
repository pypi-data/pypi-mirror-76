import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "inforion.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, add_log_file=False):
    logger = logging.getLogger(logger_name)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    # logger.addHandler(get_console_handler())
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    if add_log_file:
        logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
