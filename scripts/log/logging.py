import logging
import os
from datetime import datetime
from colored import fg, attr

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

def log_colored_capture(file_name, iso, shutter_speed, quality, compression, daylight, hdr_state, camera_config, metadataForPrint):
    """
    Logs the image capture details with a table-like formatted output and colored sections.
    """
    # Define colors
    green = fg('green')
    firstColor = fg('white')
    yellow = fg('yellow')
    red = fg('red')
    reset = attr('reset')

    print("-" * 50)

    # Set column width for consistency
    column_width = 26

    # Log the capture details
    print(f"{green}Capture Summary:{reset}")
    print(f"{firstColor}{'File Name:':<{column_width}}{yellow}{file_name}{reset}")
    print(f"{firstColor}{'ISO:':<{column_width}}{yellow}{iso}{reset}")
    print(f"{firstColor}{'Shutter Speed:':<{column_width}}{yellow}{shutter_speed}{reset}")
    print(f"{firstColor}{'Quality:':<{column_width}}{yellow}{quality}{reset}")
    print(f"{firstColor}{'Compression:':<{column_width}}{yellow}{compression}{reset}")
    print(f"{firstColor}{'Daylight:':<{column_width}}{yellow}{daylight}{reset}")
    print(f"{firstColor}{'HDR:':<{column_width}}{yellow}{hdr_state}{reset}")

    print("\n" + "-" * 50)

    # Log camera configuration
    print(f"{green}Camera Configuration:{reset}")
    for key, value in camera_config['controls'].items():
        print(f"{firstColor}{key:<{column_width}}{yellow}{value}{reset}")

    print("\n" + "-" * 50)

    # Log metadata
    print(f"{green}Metadata Information:{reset}")
    for key, value in metadataForPrint.items():
        print(f"{firstColor}{key:<{column_width}}{yellow}{value}{reset}")

    print("-" * 50)
