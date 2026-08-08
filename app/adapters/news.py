import httpx
import xml.etree.ElementTree as ET
import asyncio
from typing import List
from app.schemas.dashboard import NewsHeadline

class RSSNewsAdapter:
    # BBC publishes these RSS feeds for syndication without an API key.
    FEEDS = (
        ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World", "World"),
        ("https://feeds.bbci.co.uk/news/technology/rss.xml", "BBC Technology", "Technology"),
    )

    @classmethod
    async def _fetch_feed(
        cls, client: httpx.AsyncClient, url: str, publisher: str, category: str
    ) -> List[NewsHeadline]:
        try:
            response = await client.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            headlines: List[NewsHeadline] = []
            for item in root.findall(".//channel/item")[:4]:
                title = item.findtext("title", "").strip()
                published_at = item.findtext("pubDate", "").strip()
                if title:
                    headlines.append(
                        NewsHeadline(
                            title=title,
                            publisher=publisher,
                            published_at=published_at,
                            category=category,
                        )
                    )
            return headlines
        except (httpx.HTTPError, ET.ParseError, ValueError):
            return []

    @classmethod
    async def fetch_curated_news(cls) -> List[NewsHeadline]:
        headers = {"User-Agent": "Mosaic-Dashboard/1.0", "Accept": "application/rss+xml, application/xml"}
        async with httpx.AsyncClient(timeout=8.0, headers=headers, follow_redirects=True) as client:
            batches = await asyncio.gather(
                *(cls._fetch_feed(client, *feed) for feed in cls.FEEDS)
            )
        return [headline for batch in batches for headline in batch][:8]
