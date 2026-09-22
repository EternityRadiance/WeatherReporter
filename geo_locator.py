import requests
import os
from dotenv import load_dotenv


load_dotenv()

def fallback():
    city = os.getenv("GEO_API_FALLBACK_CITY")
    return city, None, None

def get_location():
    try:
        response = requests.get(os.getenv("GEO_API_URL"), timeout=5)

        if response.status_code != 200:
            print(f"Error! Status code: {response.status_code}")
            return fallback()

        data = response.json()

        city = data.get("city")
        if "loc" in data:
#            lat, lon = map(float, data.get("loc").split(","))
            lat, lon = data.get("loc").split(",")
        if not city:
            raise ValueError
        return city, lat, lon
    
    except requests.exceptions.Timeout:
        print("Request timeout")
        return fallback()
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return fallback()
    except requests.exceptions.RequestException as exc:
        print(f"Request Exception: {exc}")
        return fallback()