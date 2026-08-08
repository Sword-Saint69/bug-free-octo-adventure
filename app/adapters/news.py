import httpx
import xml.etree.ElementTree as ET
from typing import List
from app.schemas.dashboard import NewsHeadline

class RSSNewsAdapter:
    BBC_RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"

    @classmethod
    async def fetch_curated_news(cls) -> List[NewsHeadline]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        headlines: List[NewsHeadline] = []
        async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
            try:
                res = await client.get(cls.BBC_RSS_URL)
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    items = root.findall(".//channel/item")
                    for item in items[:5]:
                        title = item.findtext("title", "").strip()
                        pub_date = item.findtext("pubDate", "").strip()
                        if title:
                            headlines.append(
                                NewsHeadline(
                                    title=title,
                                    publisher="BBC World News Live",
                                    published_at=pub_date,
                                    category="World News"
                                )
                            )
            except Exception:
                pass

        return headlines
