import logging
import logging.config

from os import environ
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    DEBUG = '\033[10m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def current_time():
    return datetime.now().strftime("%H:%M:%S")


def log(source, message, level="info"):
    logger = logging.getLogger()
    formatted_message = f"[{current_time()}] ({source}) {message}"
    if level == "info":
        logger.info(f"{bcolors.OKGREEN}{formatted_message}{bcolors.ENDC}")
    elif level == "warning":
        logger.warning(f"{bcolors.WARNING}{formatted_message}{bcolors.ENDC}")
    elif level == "error":
        logger.error(f"{bcolors.FAIL}{formatted_message}{bcolors.ENDC}")
    elif level == "critical":
        logger.critical(f"{bcolors.FAIL}{formatted_message}{bcolors.ENDC}")
    else:
        logger.debug(f"{bcolors.DEBUG}{formatted_message}{bcolors.ENDC}")


