import requests

def get_weather(location: str) -> dict:
    """Returns current weather and temperature for a given location using Open-Meteo."""
    try:
        # 1. Geocoding API to get coordinates from city name
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = requests.get(geo_url).json()

        if 'results' not in geo_response:
            return {"status": "error", "message": f"Location '{location}' not found."}

        # Extract coordinates
        geo_data = geo_response['results'][0]
        lat = geo_data['latitude']
        lon = geo_data['longitude']

        # 2. Weather Forecast API
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weather_code"
        }
        weather_response = requests.get(weather_url, params=params).json()

        current = weather_response['current']
        temp = current['temperature_2m']
        
        return {
            "status": "success",
            "location": geo_data['name'],
            "country": geo_data.get('country', 'Unknown'),
            "temperature": f"{temp}°C",
            "weather_code": current['weather_code']
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
