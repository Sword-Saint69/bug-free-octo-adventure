from typing import Optional
from app.adapters.weather import OpenMeteoAdapter
from app.schemas.dashboard import WeatherModule

class WeatherService:
    @classmethod
    async def get_weather(cls, latitude: float = 20.2961, longitude: float = 85.8245) -> Optional[WeatherModule]:
        return await OpenMeteoAdapter.fetch_current_weather(latitude, longitude)
