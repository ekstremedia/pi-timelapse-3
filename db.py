import sqlite3
import os

# Path to your SQLite database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database/lux_data.db')

def echo_database():
    """
    Prints the content of the database in a formatted table.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Fetch all rows from the database
    cursor.execute("SELECT * FROM image_evaluation")
    rows = cursor.fetchall()

    # Print table headers
    print(f"{'ID':<5}{'Lux':<10}{'Evaluated Lux':<15}{'Exposure Time':<15}{'Evaluated Exposure Time':<25}{'Timestamp':<20}")
    print("-" * 85)

    # Print each row, replacing None with a placeholder
    for row in rows:
        lux = row[1] if row[1] is not None else "N/A"
        evaluated_lux = row[2] if row[2] is not None else "N/A"
        exposure_time = row[3] if row[3] is not None else "N/A"
        evaluated_exposure_time = row[4] if row[4] is not None else "N/A"
        timestamp = row[5] if row[5] is not None else "N/A"

        print(f"{row[0]:<5}{lux:<10}{evaluated_lux:<15}{exposure_time:<15}{evaluated_exposure_time:<25}{timestamp:<20}")

    conn.close()


if __name__ == "__main__":
    echo_database()

