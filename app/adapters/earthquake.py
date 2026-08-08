import httpx
from typing import List
from pydantic import BaseModel

class EarthquakeEvent(BaseModel):
    id: str
    magnitude: float
    place: str
    time: int
    url: str

class USGSEarthquakeAdapter:
    BASE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

    @classmethod
    async def fetch_recent_earthquakes(cls, min_magnitude: float = 2.5) -> List[EarthquakeEvent]:
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(cls.BASE_URL)
                if response.status_code == 200:
                    features = response.json().get("features", [])
                    events = []
                    for f in features:
                        props = f.get("properties", {})
                        mag = props.get("mag", 0.0)
                        if mag and mag >= min_magnitude:
                            events.append(
                                EarthquakeEvent(
                                    id=f.get("id", ""),
                                    magnitude=mag,
                                    place=props.get("place", "Unknown"),
                                    time=props.get("time", 0),
                                    url=props.get("url", "")
                                )
                            )
                    return events[:3]
            except Exception:
                return []
        return []
