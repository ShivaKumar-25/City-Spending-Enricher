import requests
import logging
from .config import GEOCODE_URL, TIMEOUT

def get_geocode(city, country):
    try:
        params = {"name": city, "country": country, "count": 1}
        r = requests.get(GEOCODE_URL, params=params, timeout=TIMEOUT)
        results = r.json().get("results", [])
        if results:
            d = results[0]
            logging.info(f"Geocode data: {d}")
            return d.get("latitude"), d.get("longitude")
        return None, None
    except Exception as e:
        logging.warning(f"Geocode failed for {city}, {country}: {e}")
        return None, None
