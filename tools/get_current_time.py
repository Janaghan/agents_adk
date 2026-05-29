import requests
from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_time(city: str) -> dict:
    """Returns the current real-time in a specified city using Open-Meteo geocoding and local timezone conversion."""
    try:
        # 1. Geocoding API to get timezone from city name
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if 'results' not in geo_response:
            return {"status": "error", "message": f"City '{city}' not found."}

        geo_data = geo_response['results'][0]
        timezone_str = geo_data.get('timezone')
        if not timezone_str:
            return {"status": "error", "message": f"Timezone for '{city}' not found."}

        # 2. Get current time in that timezone
        tz = ZoneInfo(timezone_str)
        local_time = datetime.now(tz)
        
        # Format the time nicely
        formatted_time = local_time.strftime("%I:%M %p")
        formatted_date = local_time.strftime("%Y-%m-%d")
        
        return {
            "status": "success",
            "city": geo_data['name'],
            "country": geo_data.get('country', 'Unknown'),
            "timezone": timezone_str,
            "date": formatted_date,
            "time": formatted_time
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

