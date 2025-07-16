# icon_mapper.py
# Map OpenWeatherMap icon codes to your custom high-quality icons

ICON_MAP = {
    "01d": "weather_icons/clear_day.png",        # ☀️ Clear Day
    "01n": "weather_icons/clear_night.png",      # 🌙 Clear Night

    "02d": "weather_icons/few_clouds_day.png",   # 🌤️ Few Clouds Day
    "02n": "weather_icons/few_clouds_night.png", # ☁️ Few Clouds Night

    "03d": "weather_icons/scattered_clouds.png", # ☁️ Scattered Clouds
    "03n": "weather_icons/scattered_clouds.png",

    "04d": "weather_icons/broken_clouds_day.png", # 🌥️ Broken Clouds
    "04n": "weather_icons/broken_clouds_night.png",

    "09d": "weather_icons/shower_rain_day.png",   # 🌧️ Shower Rain
    "09n": "weather_icons/shower_rain_night.png",

    "10d": "weather_icons/rain_day.png",          # 🌦️ Rain Day
    "10n": "weather_icons/rain_night.png",

    "11d": "weather_icons/thunderstorm_day.png",  # ⛈️ Thunderstorm
    "11n": "weather_icons/thunderstorm_night.png",

    "13d": "weather_icons/snow.png",              # ❄️ Snow
    "13n": "weather_icons/snow.png",

    "50d": "weather_icons/mist.png",              # 🌫️ Mist / Fog / Haze
    "50n": "weather_icons/mist.png",
}

def get_icon_path(icon_code):
    """
    Returns the file path of the high-quality weather icon for the given icon code.
    Defaults to a placeholder icon if code not found.
    """
    return ICON_MAP.get(icon_code, "weather_icons/default.png")

