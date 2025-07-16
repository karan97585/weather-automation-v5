# main.py ✅ Scheduler Runner

import schedule
import time
from weather_fetcher import fetch_and_store_weather
from export_csv import export_old_data_to_csv
from db_utils import delete_old_data
import logging

# ✅ Logging setup
logging.basicConfig(
    filename='weather_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ✅ First run immediately
fetch_and_store_weather()
delete_old_data(days=30)
export_old_data_to_csv(days=30)

# ✅ Schedule jobs
schedule.every(30).minutes.do(fetch_and_store_weather)
schedule.every().day.at("01:00").do(delete_old_data, days=30)
schedule.every().day.at("01:10").do(export_old_data_to_csv, days=30)

while True:
    schedule.run_pending()
    time.sleep(10)
