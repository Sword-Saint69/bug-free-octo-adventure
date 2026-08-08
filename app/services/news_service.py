from typing import List, Optional
from app.adapters.news import RSSNewsAdapter
from app.adapters.space import NASAAdapter
from app.schemas.dashboard import NewsHeadline, SpaceApodItem
from app.core.config import settings

class NewsService:
    @classmethod
    async def get_curated_news(cls) -> List[NewsHeadline]:
        raw_news = await RSSNewsAdapter.fetch_curated_news()
        return [
            NewsHeadline(
                title=n.title,
                publisher=n.publisher,
                published_at=n.published_at,
                category=n.category
            )
            for n in raw_news
        ]

    @classmethod
    async def get_space_apod(cls) -> Optional[SpaceApodItem]:
        apod = await NASAAdapter.fetch_apod(api_key=settings.NASA_API_KEY or "DEMO_KEY")
        if not apod:
            return SpaceApodItem(
                title="Deep Field View of Cosmic Nebula",
                explanation="A breathtaking view captured by space telescope sensors highlighting high energy cosmic formations.",
                date="2026-08-07",
                url="https://apod.nasa.gov/apod/astropix.html"
            )
        return SpaceApodItem(
            title=apod.title,
            explanation=apod.explanation,
            date=apod.date,
            url=apod.url
        )
