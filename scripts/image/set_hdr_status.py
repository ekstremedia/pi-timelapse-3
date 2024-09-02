# scripts/image/set_hdr_status.py

import json
import os
import subprocess
import time
from datetime import datetime, timedelta

from scripts.log.logging import log_message

# Path to store the last HDR change time
LAST_HDR_CHANGE_PATH = 'temp/last_hdr_change.json'
HDR_COOLDOWN_PERIOD = timedelta(hours=1)  # 1 hour cooldown period

def load_last_hdr_change_time():
    if os.path.exists(LAST_HDR_CHANGE_PATH):
        try:
            with open(LAST_HDR_CHANGE_PATH, 'r') as file:
                data = json.load(file)
                return datetime.fromisoformat(data["last_change"])
        except Exception as e:
            log_message(None, f"Error loading last HDR change time: {e}")
    return datetime.min  # Return a very old time if no record exists

def save_last_hdr_change_time():
    try:
        with open(LAST_HDR_CHANGE_PATH, 'w') as file:
            json.dump({"last_change": datetime.now().isoformat()}, file)
    except Exception as e:
        log_message(None, f"Error saving last HDR change time: {e}")

def get_current_hdr_state():
    result = subprocess.run(
        ["v4l2-ctl", "--get-ctrl=wide_dynamic_range", "-d", "/dev/v4l-subdev0"],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    return "wide_dynamic_range: 1" in output

def set_hdr_state(enable, logger=None):
    """
    Sets the HDR (Wide Dynamic Range) state of the camera.

    Parameters:
        enable (bool): True to enable HDR, False to disable.
    """
    current_state = get_current_hdr_state()
    last_change_time = load_last_hdr_change_time()

    if datetime.now() - last_change_time < HDR_COOLDOWN_PERIOD:
        if logger:
            log_message(logger, f"HDR change is in cooldown. Skipping change. Current state: {current_state}, Desired state: {enable}")
        return

    if enable and not current_state:
        if logger:
            log_message(logger, "Enabling HDR")
        os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
        save_last_hdr_change_time()
        time.sleep(5)  # Adding a delay after enabling HDR

    elif not enable and current_state:
        if logger:
            log_message(logger, "Disabling HDR")
        os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")
        save_last_hdr_change_time()
        time.sleep(5)  # Adding a delay after disabling HDR
