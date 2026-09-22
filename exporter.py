import os
from dotenv import load_dotenv

from db_models import load_forecast

load_dotenv

def get_output_path():
    path = os.getenv("OUTPUT_FILE", "").strip()
    if path is None:
        print("OUTPUT_FILE path is not found")
        raise RuntimeError("OUTPUT_FILE is not found")
    return path

def format_val(value):
    if value is None:
        return ""
    try:
        f = float(value)
    except (ValueError, TypeError):
        return str(value)
    if f == int(f):
        return str(int(f))
    return str(f)

def header(records):
    city = records[0].get("city", "None")
    first_date = records[0].get("date", "")
    last_date = records[-1].get("date", "")

    return [
        "Weather Forecast",
        "",
        f"Location: {city}",
        f"Period: {first_date} - {last_date}",
        ""
    ]

def table(records):
    strings = [
        "| Date | Min.Temp | Max.Temp | Desc | Humidity | Wind |",
        "|------|----------|----------|------|----------|------|"
    ]
    for r in records:
        string = (
            f"| {r.get("date", "")} "
            f"|{format_val(r.get("temp_min"))} "
            f"{format_val(r.get("temp_max"))} "
            f"{r.get("description", "")} "
            f"{format_val(r.get("humidity"))} "
            f"{format_val(r.get("wind_speed"))}"
        )
        strings.append(string)

    return strings

def to_markdown(city=None):
    records = load_forecast(city)

    if records is None:
        print("Db data loading error")
        return None

    if len(records) == 0:
        print("Bd is empty")
        return None

    strings = []
    strings.extend(header(records))
    strings.extend(table(records))
    content = "\n".join(strings) + "\n"

    try:
        path = get_output_path()
    except RuntimeError as e:
        print(f"Error: {e}")
        return None

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        print(f"Writing error: {e}")
        return None

    print(f"Markdown saved: {path}")
    return path