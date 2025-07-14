import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
import logging
import schedule
import time

# ---------------------------
# ✅ Load environment variables
# ---------------------------
load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

# ---------------------------
# ✅ Logging setup
# ---------------------------
logging.basicConfig(
    filename='weather_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---------------------------
# ✅ Cities to track
# ---------------------------
cities = {
    "Uttarakhand": [
        "Dehradun", "Haridwar", "Rishikesh", "Roorkee", "Haldwani",
        "Nainital", "Kashipur", "Rudrapur", "Almora", "Pithoragarh",
        "Bageshwar", "Chamoli", "Tehri", "Pauri", "Mussoorie",
        "Khatima", "Sitarganj", "Tanakpur", "Lohaghat", "Champawat",
        "Doiwala", "Kotdwar", "Bhimtal"
    ],
    "Delhi": ["Delhi"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Uttar Pradesh": ["Lucknow", "Kanpur"],
    "Tamil Nadu": ["Chennai", "Coimbatore"]
}

# ---------------------------
# ✅ Create DB connection
# ---------------------------
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
        logging.error(f"Database connection failed: {err}")
        return None

# ---------------------------
# ✅ Create table if not exists
# ---------------------------
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

# ---------------------------
# ✅ Fetch weather for 1 city
# ---------------------------
def fetch_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching weather for {city}: {e}")
        return None

# ---------------------------
# ✅ Main logic
# ---------------------------
def fetch_and_store_weather():
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    create_table(cursor)

    for state, city_list in cities.items():
        for city in city_list:
            data = fetch_weather(city)
            if data and data.get("main"):
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                desc = data["weather"][0]["description"]
                icon = data["weather"][0]["icon"]
                timestamp = datetime.now()

                insert_query = """
                    INSERT INTO weather_data (city, state, temperature, humidity, weather_description, icon, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (city, state, temp, humidity, desc, icon, timestamp)

                try:
                    cursor.execute(insert_query, values)
                    conn.commit()
                    logging.info(f"✅ Inserted: {city} | Temp: {temp}°C | Humidity: {humidity}%")
                except Exception as e:
                    logging.error(f"Insert failed for {city}: {e}")
            else:
                logging.warning(f"⚠️ No data found for {city}")

    cursor.close()
    conn.close()

# ---------------------------
# ✅ Schedule job every hour
# ---------------------------
def run_scheduler():
    fetch_and_store_weather()  # first run immediately
    schedule.every(30).minutes.do(fetch_and_store_weather)

    while True:
        schedule.run_pending()
        time.sleep(10)

# ---------------------------
# ✅ Run everything
# ---------------------------
if __name__ == "__main__":
    run_scheduler()
