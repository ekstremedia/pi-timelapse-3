# scripts/image/configure_camera.py

import libcamera
from scripts.image.set_hdr_status import set_hdr_state  # Importing HDR functions

def configure_camera(picam2, config, daylight, iso=None, shutter_speed=None, logger=None):
    focus_mode = libcamera.controls.AfModeEnum.Manual if config['camera_settings']['focus_mode'] == 'manual' else libcamera.controls.AfModeEnum.Auto # type: ignore
    lens_position = config['camera_settings']['lens_position'] if config['camera_settings']['focus_mode'] == 'manual' else None

    # Set common controls
    controls = {
        "AwbEnable": config['camera_settings']['awb_enable'],
        "AwbMode": getattr(libcamera.controls.AwbModeEnum, config['camera_settings']['awb_mode']), # type: ignore
        "AfMode": focus_mode,
        "LensPosition": lens_position,
        "ColourGains": tuple(config['camera_settings']['colour_gains_day']) if daylight else tuple(config['camera_settings']['colour_gains_night']),
    }

    # Add night-specific controls
    if not daylight:
        if (shutter_speed is not None) and (iso is not None):
            controls["ExposureTime"] = int(shutter_speed)  # Only set at night
            controls["AnalogueGain"] = round(iso)  # Only set at night


    # Apply exposure compensation for daylight to brighten images if exposure_value is set in config
    exposure_value = config['camera_settings'].get('exposure_value')  # Safely fetch the exposure_value or None if not set
    if daylight and exposure_value is not None:
        controls["ExposureValue"] = exposure_value  # Apply exposure compensation
        
    set_hdr_state(daylight and config['camera_settings']['hdr'], logger)  # Set HDR based on daylight and config

    return picam2.create_still_configuration(
        main={"size": tuple(config['camera_settings']['main_size'])},
        lores={"size": tuple(config['camera_settings']['lores_size'])},
        display=config['camera_settings']['display'],
        controls=controls
    )
