# export_csv.py 📁 Export Old Weather Data to CSV

import csv
from db_utils import create_connection
from datetime import datetime, timedelta
import logging

def export_old_data_to_csv(days=30):
    conn = create_connection()
    if not conn:
        logging.error("❌ Failed to connect to DB for export")
        return

    cursor = conn.cursor()
    cutoff = datetime.now() - timedelta(days=days)
    
    try:
        cursor.execute("SELECT * FROM weather_data WHERE timestamp < %s", (cutoff,))
        rows = cursor.fetchall()

        if rows:
            filename = f"weather_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([i[0] for i in cursor.description])  # column headers
                writer.writerows(rows)

            logging.info(f"✅ Exported {len(rows)} rows to {filename}")
        else:
            logging.info("📂 No old data to export")

    except Exception as e:
        logging.error(f"❌ Export failed: {e}")

    cursor.close()
    conn.close()
