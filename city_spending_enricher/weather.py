import requests
import logging
from .config import WEATHER_URL, TIMEOUT

def get_weather(lat, lon):
    try:
        params = {"latitude": lat, "longitude": lon, "current_weather": True}
        r = requests.get(WEATHER_URL, params=params, timeout=TIMEOUT)
        w = r.json().get("current_weather")
        if w:
            logging.info(f"Weather data: {w}")
            return w.get("temperature"), w.get("windspeed")
        return None, None
    except Exception as e:
        logging.warning(f"Weather lookup failed for {lat}, {lon}: {e}")
        return None, None
