# db_utils.py 🧱 DB Connection + Insert + Cleanup

import mysql.connector
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

# ✅ Load env
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

# ✅ MySQL connection
def create_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
    except mysql.connector.Error as err:
        logging.error(f"❌ DB connection failed: {err}")
        return None

# ✅ Table create if not exists
def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        state VARCHAR(50),
        temperature FLOAT,
        humidity INT,
        weather_description VARCHAR(255),
        icon VARCHAR(10),
        timestamp DATETIME
    )
    """)

# ✅ Insert 1 row
def insert_weather(cursor, city, state, temp, humidity, desc, icon, timestamp):
    cursor.execute("""
        INSERT INTO weather_data (city, state, temperature, humidity, weather_description, icon, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (city, state, temp, humidity, desc, icon, timestamp))

# ✅ Cleanup old data > X days
def delete_old_data(days=30):
    conn = create_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cutoff = datetime.now() - timedelta(days=days)
    cursor.execute("DELETE FROM weather_data WHERE timestamp < %s", (cutoff,))
    conn.commit()
    logging.info(f"🧹 Deleted data older than {days} days")
    cursor.close()
    conn.close()

