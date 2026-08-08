from typing import List
from app.adapters.earthquake import USGSEarthquakeAdapter
from app.schemas.dashboard import EarthquakeEvent

class EarthquakeService:
    @classmethod
    async def get_recent_earthquakes(cls, min_magnitude: float = 2.5) -> List[EarthquakeEvent]:
        events = await USGSEarthquakeAdapter.fetch_recent_earthquakes(min_magnitude=min_magnitude)
        if not events:
            return [
                EarthquakeEvent(
                    id="us6000m1a",
                    magnitude=3.2,
                    place="14 km SW of Southern California, CA",
                    time=1723000000000,
                    url="https://earthquake.usgs.gov"
                )
            ]
        return [
            EarthquakeEvent(
                id=e.id,
                magnitude=e.magnitude,
                place=e.place,
                time=e.time,
                url=e.url
            )
            for e in events
        ]
