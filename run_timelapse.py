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
        # Start the timer to measure the time taken for capturing the image
        start_time = time.time()
        log_message(logger, f"Starting a new capture cycle.")
        
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'capture_image.py')
            subprocess.run(['python3', script_path], check=True)
        except subprocess.CalledProcessError as e:
            log_message(logger, f"Error during image capture: {e}")
        
        # Calculate the time taken to capture the image
        capture_duration = time.time() - start_time
        remaining_sleep = max(0, interval - capture_duration)  # Ensure no negative sleep times

        log_message(logger, f"Capture took {capture_duration:.2f} seconds. Sleeping for {remaining_sleep:.2f} seconds before next capture.")
        time.sleep(remaining_sleep)
