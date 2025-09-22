import requests
import logging
from .config import FX_URL, FX_API_KEY, TIMEOUT

def convert_usd(local_currency, amount):
    """
    Convert a given amount from a local currency to USD using the FX API.

    Args:
        local_currency (str): The source currency code (e.g., 'EUR').
        amount (float): The amount in the source currency.

    Returns:
        tuple: (converted_amount, fx_rate) where:
            converted_amount (float or None): Amount in USD.
            fx_rate (float or None): Exchange rate used.
    """
    params = {
        "from": local_currency,
        "to": "USD",
        "amount": amount,
        "access_key": FX_API_KEY
    }

    try:
        response = requests.get(FX_URL, params=params, timeout=TIMEOUT)
        data = response.json()
        logging.info(f"FX API response: {data}")

        # Safely extract rate and converted result
        fx_rate = data.get("info", {}).get("rate")
        converted_amount = data.get("result")

        if fx_rate is None:
            logging.warning(f"FX API warning: 'rate' missing for {local_currency}. Full response: {data}")

        return converted_amount, fx_rate

    except requests.RequestException as e:
        logging.warning(f"Currency conversion failed for {amount} {local_currency}: {e}")
        return None, None
