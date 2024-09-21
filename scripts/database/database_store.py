import sqlite3
import os
import yaml
from datetime import datetime

# Database file location
DATABASE_DIR = os.path.join(os.path.dirname(__file__), '../../database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'lux_data.db')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config.yaml')

def load_config():
    """
    Loads the configuration from the config.yaml file.

    Returns:
        dict: The configuration dictionary.
    """
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r') as config_file:
        return yaml.safe_load(config_file)

def should_store_data():
    """
    Determines whether data should be stored in the database based on config.yaml.

    Returns:
        bool: True if database.store_data is set to true, False otherwise.
    """
    config = load_config()
    return config.get('database', {}).get('store_data', False)

def initialize_database():
    """
    Initializes the SQLite database, creates the directory if necessary,
    and creates the table for storing image evaluation data if it doesn't exist.
    """
    if not should_store_data():
        print("Database storing is disabled in config.yaml.")
        return

    # Create the directory if it doesn't exist
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    # Initialize the SQLite database and create the table
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_evaluation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lux REAL,
            evaluated_lux REAL,
            exposure_time REAL,
            evaluated_exposure_time REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_evaluation(lux=None, evaluated_lux=None, exposure_time=None, evaluated_exposure_time=None, update_latest=False):
    """
    Inserts or updates image evaluation data into the SQLite database, rounding lux values to 1 decimal place.

    Parameters:
        lux (float, optional): The Lux value.
        evaluated_lux (float, optional): The evaluated Lux value.
        exposure_time (float, optional): The exposure time.
        evaluated_exposure_time (float, optional): The evaluated exposure time.
        update_latest (bool, optional): If True, update the latest row. Otherwise, insert a new row.
    """
    if not should_store_data():
        print("Database storing is disabled in config.yaml.")
        return

    # Ensure the database is initialized before inserting or updating data
    initialize_database()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Automatically set the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Round the lux and evaluated_lux values to 1 decimal place if they are not None
    if lux is not None:
        lux = round(lux, 1)
    if evaluated_lux is not None:
        evaluated_lux = round(evaluated_lux, 1)

    if update_latest:
        # Update the latest row with provided values
        query = "UPDATE image_evaluation SET "
        updates = []
        params = []

        if lux is not None:
            updates.append("lux = ?")
            params.append(lux)
        if evaluated_lux is not None:
            updates.append("evaluated_lux = ?")
            params.append(evaluated_lux)
        if exposure_time is not None:
            updates.append("exposure_time = ?")
            params.append(exposure_time)
        if evaluated_exposure_time is not None:
            updates.append("evaluated_exposure_time = ?")
            params.append(evaluated_exposure_time)

        # Only update if there are fields to update
        if updates:
            query += ", ".join(updates) + " WHERE id = (SELECT MAX(id) FROM image_evaluation)"
            cursor.execute(query, params)
            print(f"Latest evaluation data updated in the database at {timestamp}")
    else:
        # Insert a new row with the values
        cursor.execute('''
            INSERT INTO image_evaluation (lux, evaluated_lux, exposure_time, evaluated_exposure_time, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (lux, evaluated_lux, exposure_time, evaluated_exposure_time, timestamp))
        print(f"Evaluation data stored in the database with timestamp {timestamp}")

    conn.commit()
    conn.close()
