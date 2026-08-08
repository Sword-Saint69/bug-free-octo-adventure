import httpx
from typing import Optional
from app.schemas.dashboard import AirQualityModule

class OpenMeteoAirQualityAdapter:
    BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    @classmethod
    def _determine_aqi_category(cls, us_aqi: int) -> str:
        if us_aqi <= 50:
            return "Good"
        elif us_aqi <= 100:
            return "Moderate"
        elif us_aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif us_aqi <= 200:
            return "Unhealthy"
        elif us_aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    @classmethod
    async def fetch_air_quality(cls, latitude: float, longitude: float) -> Optional[AirQualityModule]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "pm10,pm2_5,us_aqi",
            "timezone": "auto"
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                res = await client.get(cls.BASE_URL, params=params)
                if res.status_code == 200:
                    current = res.json().get("current", {})
                    pm2_5 = round(current.get("pm2_5", 0.0), 1)
                    pm10 = round(current.get("pm10", 0.0), 1)
                    us_aqi = int(current.get("us_aqi", 0))
                    category = cls._determine_aqi_category(us_aqi)

                    return AirQualityModule(
                        pm2_5=pm2_5,
                        pm10=pm10,
                        aqi_category=category,
                        station_source="Open-Meteo Air Quality Live API",
                        freshness_sec=0
                    )
            except Exception:
                return None
        return None
