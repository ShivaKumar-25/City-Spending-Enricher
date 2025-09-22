import os
from dotenv import load_dotenv

load_dotenv()

GEOCODE_URL = os.getenv("GEOCODE_URL", "https://geocoding-api.open-meteo.com/v1/search")
WEATHER_URL = os.getenv("WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
FX_URL = os.getenv("FX_URL", "https://api.exchangerate.host/convert")
TIMEOUT = int(os.getenv("TIMEOUT", 10))
INPUT_CSV = os.getenv("INPUT_CSV", "data/expenses.csv")
OUTPUT_JSON = os.getenv("OUTPUT_JSON", "enriched_expenses.json")
FX_API_KEY = os.getenv("FX_API_KEY")
