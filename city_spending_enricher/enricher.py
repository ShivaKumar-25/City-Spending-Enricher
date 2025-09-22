import json
import logging
from datetime import datetime, timezone
from .config import INPUT_CSV, OUTPUT_JSON
from .geocode import get_geocode
from .weather import get_weather
from .fx import convert_usd

def enrich(input_csv=INPUT_CSV, output_json=OUTPUT_JSON):
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
                    "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
            )
            logging.info(f"Processed {city}, {country}")

    with open(output_json, "w") as f:
        json.dump(results, f, indent=4)

    logging.info(f"Enriched data written to {output_json}")
