import os
from datetime import datetime, timezone
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

Base = declarative_base()

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    forecast_date = Column(Date, nullable=False)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

def get_engine():
    db_url = os.getenv("DB_URL")

    _ = os.getenv("DB_USER")
    _ = os.getenv("DB_PASSWORD")
    return create_engine(db_url)

engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError:
        print("Error create table")
        raise SQLAlchemyError

def save_forecast(daily):
    if daily is None or len(daily) == 0:
        print("Nothing to save")
        return(0, 0)

    session = SessionLocal()
    saved = 0
    skipped = 0

    try:
        for day in daily:
            city = day["city"]
            date_str = day["date"]

            try:
                forecast_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(f"Passed incorrect date {date_str}")
                skipped += 1
                continue

            existing_record = session.query(WeatherForecast).filter_by(
                city=city,
                forecast_date=forecast_date
            ).first()

            if existing_record is not None:
                print(f"Skipped duplicate for {city} on {forecast_date}")
                skipped += 1
                continue

            record = WeatherForecast(
                city=city,
                forecast_date=forecast_date,
                temp_min=day.get("temp_min"),
                temp_max=day.get("temp_max"),
                humidity=day.get("humidity"),
                wind_speed=day.get("wind_speed"),
                description=day.get("description")
            )
            session.add(record)
            saved += 1

        session.commit()
        print(f"Saved: {saved} records. Skipped: {skipped} records")
        return(saved, skipped)

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Db error: {e}")
        return None

    finally:
        session.close()

def load_forecast(city=None):

    session = SessionLocal()
    try:
        request = session.query(WeatherForecast)
        if city is not None:
            request = request.filter_by(city=city)
        request = request.order_by(WeatherForecast.forecast_date)

        records = request.all()
        result = []
        for r in records:
            result.append({
                "city": r.city,
                "date": r.forecast_date,
                "temp_min": r.temp_min,
                "temp_max": r.temp_max,
                "humidity": r.humidity,
                "wind_speed": r.wind_speed,
                "description": r.description
            })
        return result
    except SQLAlchemyError as e:
        print(f"Db error: {e}")
        return None

    finally:
        session.close()