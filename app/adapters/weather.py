import httpx
from typing import Optional
from app.schemas.dashboard import WeatherModule

class OpenMeteoAdapter:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float) -> Optional[WeatherModule]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
            "timezone": "auto"
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(cls.BASE_URL, params=params)
                if response.status_code == 200:
                    current = response.json().get("current", {})
                    return WeatherModule(
                        temperature=float(current.get("temperature_2m", 0.0)),
                        apparent_temperature=float(current.get("apparent_temperature", 0.0)),
                        condition_code=int(current.get("weather_code", 0)),
                        humidity=int(current.get("relative_humidity_2m", 0)),
                        rain_probability=int(current.get("precipitation", 0)),
                        wind_speed=float(current.get("wind_speed_10m", 0.0)),
                        wind_direction=int(current.get("wind_direction_10m", 0)),
                        is_day=bool(current.get("is_day", 1)),
                        provider="Open-Meteo Live",
                        freshness_sec=0
                    )
            except Exception:
                return None
        return None
