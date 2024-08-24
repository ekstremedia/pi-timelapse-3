import logging
import os
from datetime import datetime

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger with the specified name, log file, and level.

    Parameters:
        name (str): The name of the logger.
        log_file (str): The file path where the logs will be stored.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger.
    """
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

def log_message(logger, message):
    """
    Logs a message using the provided logger.

    Parameters:
        logger (logging.Logger): The logger to use.
        message (str): The message to log.
    """
    logger.info(message)

def setup_logging_directory():
    """
    Ensures that the logs directory exists.
    """
    logs_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir
