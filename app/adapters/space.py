import httpx
from typing import Optional
from pydantic import BaseModel

class SpaceApodItem(BaseModel):
    title: str
    explanation: str
    date: str
    url: Optional[str] = None

class NASAAdapter:
    BASE_URL = "https://api.nasa.gov/planetary/apod"

    @classmethod
    async def fetch_apod(cls, api_key: str = "DEMO_KEY") -> Optional[SpaceApodItem]:
        params = {"api_key": api_key}
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(cls.BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return SpaceApodItem(
                        title=data.get("title", "Astronomy Picture of the Day"),
                        explanation=data.get("explanation", "")[:200] + "...",
                        date=data.get("date", ""),
                        url=data.get("url")
                    )
            except Exception:
                return None
        return None
