from typing import Optional
from app.adapters.air_quality import OpenMeteoAirQualityAdapter
from app.schemas.dashboard import AirQualityModule

class AirQualityService:
    @classmethod
    async def get_air_quality(cls, latitude: float, longitude: float) -> Optional[AirQualityModule]:
        return await OpenMeteoAirQualityAdapter.fetch_air_quality(latitude, longitude)
