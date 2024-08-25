import os
import subprocess
import time
import yaml
from scripts.log.logging import setup_logger, log_message, setup_logging_directory

def load_config(config_path):
    """
    Loads the configuration from a YAML file.

    Parameters:
        config_path (str): Path to the config.yaml file.

    Returns:
        dict: The configuration dictionary.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    # Load the configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)

    # Setup logging if enabled
    logger = None
    if config.get('logging', {}).get('capture_image', False):
        logs_dir = setup_logging_directory()
        log_file = os.path.join(logs_dir, 'timelapse.log')
        logger = setup_logger('timelapse', log_file)

    interval = config['camera_settings']['interval']
    
    while True:
        # Start capturing images at specified intervals
        log_message(logger, f"Starting a new capture cycle.")
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'capture_image.py')
            subprocess.run(['python3', script_path], check=True)
        except subprocess.CalledProcessError as e:
            log_message(logger, f"Error during image capture: {e}")
        
        log_message(logger, f"Sleeping for {interval} seconds before next capture.")
        time.sleep(interval)
