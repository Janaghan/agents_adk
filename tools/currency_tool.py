import requests

def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Returns the real-time exchange rate between two currencies using a free API."""
    try:
        # Using a free, no-key-required API for real-time rates
        url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("result") == "success":
            rate = data["rates"].get(target_currency.upper())
            if rate:
                return {
                    "base": base_currency.upper(),
                    "target": target_currency.upper(),
                    "rate": rate,
                    "date": data.get("time_last_update_utc")
                }
        return {"error": "Could not fetch real-time exchange rate."}
    except Exception as e:
        return {"error": str(e)}
