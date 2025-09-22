import requests
import logging
from .config import FX_URL, TIMEOUT

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
