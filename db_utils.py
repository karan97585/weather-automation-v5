import mysql.connector
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

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
def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        state VARCHAR(50),
        temperature FLOAT,
        temperature_fahrenheit FLOAT,
        feels_like FLOAT,
        humidity INT,
        weather_description VARCHAR(255),
        icon VARCHAR(10),
        wind_speed FLOAT,
        cloudiness INT,
        timestamp DATETIME,
        day_of_week VARCHAR(20),
        hour INT,
        temp_category VARCHAR(20),
        is_raining VARCHAR(10),
        alert_level VARCHAR(10)
    )
    """)


def insert_weather(cursor, city, state, temp, temp_f, feels_like, humidity, desc, icon,
                   wind_speed, cloudiness, timestamp, day_of_week, hour, temp_category,
                   is_raining, alert_level):
    cursor.execute("""
        INSERT INTO weather_data 
        (city, state, temperature, temperature_fahrenheit, feels_like, humidity,
         weather_description, icon, wind_speed, cloudiness, timestamp,
         day_of_week, hour, temp_category, is_raining, alert_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (city, state, temp, temp_f, feels_like, humidity, desc, icon,
          wind_speed, cloudiness, timestamp, day_of_week, hour, temp_category,
          is_raining, alert_level))

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
