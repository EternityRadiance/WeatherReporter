import requests
import os
from collections import Counter
from dotenv import load_dotenv
from geo_locator import get_location

load_dotenv()

def get_params(city, lat, lon):
    params = {
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric",
        "lang": "ru",
    }
    if lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    else:
        params["q"] = city
    return params

def fetch_forecast(city, lat, lon):
    url = os.getenv("WEATHER_API_BASE_URL")
    params = get_params(city, lat, lon)

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.Timeout:
        print("OpenWeatherMap Request Timeout")
        return None
    except requests.ConnectionError:
        print("OpenWeatherMap Connection Error")
        return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    if response.status_code == 401:
        print("Wrong API Key")
        return None
    if response.status_code == 404:
        print("City not found")
        return None
    if response.status_code == 429:
        print("Request limit")
        return None
    if response.status_code != 200:
        print(f"Request error: {response.status_code}")
        return None
    
    data = response.json()
    return data["list"]

#Extracting date
def extract_date(point):
    dt_txt = point.get("dt_txt")
    if dt_txt is None:
        return None
    return dt_txt.split(" ")[0]

#Extracting time
def extract_time(point):
    dt_txt = point.get("dt_txt")
    if dt_txt is None:
        return None
    return dt_txt.split(" ")[1]

#Pick description
def get_desc(day_points):
    for point in day_points:
        time = extract_time(point)
        if time is not None and time.startswith("12:00"):
            weather_list = point.get("weather", [])
            if len(weather_list) > 0:
                desc = weather_list[0].get("description")
                if desc:
                    return desc

    counter = Counter()
    for point in day_points:
        weather_list = point.get("weather", [])
        if len(weather_list) > 0:
            desc = weather_list[0].get("description")
            if desc:
                counter[desc] += 1
    if len(counter) > 0:
        return counter.most_common(1)[0][0]

    return "No data"

def aggregate_forecast(points, city):

    days = {}

    for point in points:
        date = extract_date(point)
        if date is None:
            continue
        if date not in days:
            days[date] = []

        days[date].append(point)

    if len(days) == 0:
        print("Points error")
        return []

    dates = sorted(days.keys())
    log_dates = dates[0:4]

    result = []
    for date in log_dates:
        day_points = days[date]

        temp_min_vals = []
        temp_max_vals = []
        humidity_vals = []
        wind_vals = []

        for point in day_points:
            main = point.get("main", {})
            wind = point.get("wind", {})

            if "temp_min" in main:
                temp_min_vals.append(main["temp_min"])
            if "temp_max" in main:
                temp_max_vals.append(main["temp_max"])
            if "humidity" in main:
                humidity_vals.append(main["humidity"])
            if "speed" in wind:
                wind_vals.append(wind["speed"])

        temp_min = min(temp_min_vals)
        temp_max = max(temp_max_vals)

        if len(humidity_vals) > 0:
            humidity = round(sum(humidity_vals) / len(humidity_vals))
        else:
            humidity = 0

        if len(wind_vals) > 0:
            wind_speed = max(wind_vals)
        else:
            wind_speed = 0.0

        description = get_desc(day_points)

        result.append({
            "city": city,
            "date": date,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "description": description,
        })

    return result

def get_daily(city, lat, lon):
    points = fetch_forecast(city, lat, lon)

    if points is None:
        print("OpenWeatherMap forecast error")
        return None

    daily = aggregate_forecast(points, city)
    if len(daily) == 0:
        print("Aggregation error: no days")
        return None

    return daily