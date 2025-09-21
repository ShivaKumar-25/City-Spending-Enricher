import csv
import json
import requests
import logging
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, filename="logs/enrichment.log", filemode="a")

GEOCODE_URL = os.getenv("GEOCODE_URL", "https://geocoding-api.open-meteo.com/v1/search")
WEATHER_URL = os.getenv("WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
FX_URL = os.getenv("FX_URL", "https://api.exchangerate.host/convert")
TIMEOUT = int(os.getenv("TIMEOUT", 10))
INPUT_CSV = os.getenv("INPUT_CSV", "expenses.csv")
OUTPUT_JSON = os.getenv("OUTPUT_JSON", "enriched_expenses.json")


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


def convert_usd(amount, cur):
    try:
        params = {"from": cur, "to": "USD", "amount": amount}
        r = requests.get(FX_URL, params=params, timeout=TIMEOUT)
        d = r.json()
        logging.info(f"FX data: {d}")
        rate = d.get("info", {}).get("rate")
        result = d.get("result")
        return rate, result
    except Exception as e:
        logging.warning(f"Currency conversion failed for {amount} {cur}: {e}")
        return None, None


def enrich(input_csv, output_json):
    logging.info(f"Starting enrichment for {input_csv}")
    results = []
    with open(input_csv, "r") as f:
        rows = f.read().strip().splitlines()
        _, data = rows[0].split(","), rows[1:]
        for line in data:
            city, country, cur, amount = line.split(",")
            amount = float(amount)

            lat, lon = get_geocode(city, country)
            temp, wind = get_weather(lat, lon) if lat else (None, None)
            rate, usd = convert_usd(amount, cur)

            results.append(
                {
                    "city": city,
                    "country_code": country,
                    "local_currency": cur,
                    "amount_local": amount,
                    "fx_rate_to_usd": rate,
                    "amount_usd": usd,
                    "latitude": lat,
                    "longitude": lon,
                    "temperature_c": temp,
                    "wind_speed_mps": wind,
                    "retrieved_at": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                }
            )
            logging.info(f"Processed {city}, {country}")

    with open(output_json, "w") as f:
        json.dump(results, f, indent=4)
    logging.info(f"Enriched json : {output_json}")


if __name__ == "__main__":
    enrich(INPUT_CSV, OUTPUT_JSON)
