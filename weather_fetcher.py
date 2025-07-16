# weather_fetcher.py 🌦️ API Fetch + Retry + Insert

import requests
from datetime import datetime
from db_utils import create_connection, create_table, insert_weather
from alerting import log_error
from dotenv import load_dotenv
import os
import time

# ✅ Load env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ✅ Cities grouped by state
cities = {
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Roorkee", "Haldwani", "Nainital", "Kashipur", "Rudrapur", "Almora", "Pithoragarh", "Bageshwar", "Chamoli", "Tehri", "Pauri", "Mussoorie", "Khatima", "Sitarganj", "Tanakpur", "Lohaghat", "Champawat", "Doiwala", "Kotdwar", "Bhimtal"],
    "Delhi": ["Delhi"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Uttar Pradesh": ["Lucknow", "Kanpur"],
    "Tamil Nadu": ["Chennai", "Coimbatore"]
}

# ✅ Fetch single city's weather with retry
def fetch_weather(city, retries=3, delay=2):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                log_error(f"API failed for {city} (Status: {response.status_code})")
        except Exception as e:
            log_error(f"Exception while fetching {city}: {e}")
        time.sleep(delay)
    return None

# ✅ Fetch & insert data into DB
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
                insert_weather(cursor, city, state, temp, humidity, desc, icon, timestamp)
            else:
                log_error(f"⚠️ No data for {city}")

    conn.commit()
    cursor.close()
    conn.close()

