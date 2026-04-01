import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(city_name, latitude, longitude):
    # Define parameters for the API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,precipitation_probability_max",
        "timezone": "auto"
    }

    try:
        # Make the API request with a timeout
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Extract relevant data and return it in a structured format
        return {
            "city": city_name,
            "dates": data.get("daily", {}).get("time", []),
            "temp_max": data.get("daily", {}).get("temperature_2m_max", []),
            "temp_min": data.get("daily", {}).get("temperature_2m_min", []),
            "precipitation": data.get("daily", {}).get("precipitation_sum", []),
            "wind_speed_max": data.get("daily", {}).get("wind_speed_10m_max", []),
            "precip_prob_max": data.get("daily", {}).get("precipitation_probability_max", [])
        }
    # Handle potential exceptions during the API request
    except requests.exceptions.Timeout:
        print(f"Request timed out for {city_name}")
        return None
    # Handle other types of request exceptions (e.g., connection errors, HTTP errors)
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {city_name}: {e}")
        return None