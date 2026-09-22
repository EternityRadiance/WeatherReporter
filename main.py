#from geo_locator import get_location
#from weather_client import get_daily

# Смотри типы в geo_locator
#city, lat, lon = get_location()
#print(city, lat, lon)

#daily = get_daily(city, lat, lon)
#if daily is None:
#    print("Forecast error")

#print()
#print(f"Forecast for {city}:")
#print("-" * 70)


#for day in daily:
#    print(f"{day["date"]}")
#    print(f"min {day["temp_min"]}")
#    print(f"max {day["temp_max"]}")
#    print(f"{day["description"]}")
#    print(f"humidity  {day["humidity"]}")
#    print(f"wind speed {day["wind_speed"]}")
#    print("-" * 70)


from geo_locator import get_location
from weather_client import get_daily
from db_models import init_db, save_forecast
from exporter import to_markdown

def main():
    # ===DB Init===
    try:
        init_db()
    except Exception as e:
        print(f"Error DB Init: {e}")
        return 1

    # ===Getting Location===
    try:
        city, lat, lon = get_location()
    except Exception as e:
        print(f"Error getting location: {e}")
        return 2

    print(f"City: {city}")
    if lat is not None and lon is not None:
        print(f"Coords: {lat}, {lon}")
    else:
        print(f"Coords is not determined. Fallback.")
    print()
    print()
    print()

    # ===Forecast===
    daily = get_daily(city, lat, lon)
    if daily is None:
        print("Weather Forecast error.")
        return 3
    print(f"Days: {len(daily)}")
    print(f"Period: {daily[0]["date"]} - {daily[-1]["date"]}")
    print()
    print()
    print()

    # ===Saving===
    result = save_forecast(daily)
    if result is None:
        print("Db saving error.")
        return 4

    saved, skipped = result
    print(f"Saved: {saved}.")
    print(f"Skipped: {skipped}.")
    print()
    print()
    print()

    # ===ExportToMarkdown===
    path = to_markdown(city)
    if path is None:
        print("Error exporting to markdown.")
        return 5
    print(f"File: {path}")

if __name__ == "__main__":
    code = main()
    exit(code)