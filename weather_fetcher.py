import requests
from datetime import datetime
from db_utils import create_connection, create_table, insert_weather
from alerting import log_error
from dotenv import load_dotenv
import os
import time
import logging
import calendar

# ✅ Load env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ✅ Cities grouped by state
cities = {
    "Uttarakhand": [
        "Dehradun", "Haridwar", "Rishikesh", "Roorkee", "Haldwani", "Nainital", "Kashipur", "Rudrapur",
        "Almora", "Pithoragarh", "Bageshwar", "Tehri", "Pauri", "Mussoorie", "Khatima", "Sitarganj",
        "Tanakpur", "Lohaghat", "Champawat", "Doiwala", "Kotdwar", "Bhimtal"
    ],
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

# ✅ Categorization logic
def categorize_temp(temp):
    if temp < 10: return "Cold"
    elif temp < 25: return "Moderate"
    else: return "Hot"

def is_rain(description):
    return "Yes" if "rain" in description.lower() else "No"

def alert_level(temp, humidity):
    if temp > 40 or humidity > 90:
        return "High"
    elif temp > 30:
        return "Medium"
    else:
        return "Low"

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
                try:
                    temp = data["main"]["temp"]
                    temp_f = (temp * 9/5) + 32
                    feels_like = data["main"]["feels_like"]
                    humidity = data["main"]["humidity"]
                    desc = data["weather"][0]["description"]
                    icon = data["weather"][0]["icon"]
                    wind_speed = data["wind"]["speed"]
                    cloudiness = data["clouds"]["all"]
                    timestamp = datetime.now()
                    day_of_week = calendar.day_name[timestamp.weekday()]
                    hour = timestamp.hour
                    temp_cat = categorize_temp(temp)
                    rain = is_rain(desc)
                    alert = alert_level(temp, humidity)

                    # ✅ Insert to DB
                    insert_weather(
                        cursor, city, state, temp, temp_f, feels_like, humidity, desc, icon,
                        wind_speed, cloudiness, timestamp,
                        day_of_week, hour, temp_cat, rain, alert
                    )

                    # ✅ Detailed Logging
                    logging.info(
                        f"✅ {city}, {state} | {temp:.2f}°C / {temp_f:.2f}°F | Feels Like: {feels_like:.2f}°C | "
                        f"{humidity}% Humidity | Wind: {wind_speed:.1f} m/s | Clouds: {cloudiness}% | "
                        f"Desc: {desc} | Day: {day_of_week} | Hour: {hour} | "
                        f"Category: {temp_cat} | Rain: {rain} | Alert: {alert}"
                    )

                except Exception as e:
                    log_error(f"Insert error {city}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
