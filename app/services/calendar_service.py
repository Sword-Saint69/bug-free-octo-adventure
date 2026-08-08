import httpx
import re
import datetime
from typing import List, Optional
from app.schemas.dashboard import CalendarEvent

class CalendarService:
    NAGER_API_URL = "https://date.nager.at/api/v3/PublicHolidays"

    @classmethod
    async def fetch_ics_events(cls, ics_url: str) -> List[CalendarEvent]:
        events: List[CalendarEvent] = []
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                res = await client.get(ics_url)
                if res.status_code == 200:
                    text = res.text
                    raw_events = text.split("BEGIN:VEVENT")
                    for idx, raw_ev in enumerate(raw_events[1:]):
                        summary_match = re.search(r"SUMMARY:(.*)", raw_ev)
                        dtstart_match = re.search(r"DTSTART.*:(.*)", raw_ev)
                        dtend_match = re.search(r"DTEND.*:(.*)", raw_ev)
                        
                        summary = summary_match.group(1).strip() if summary_match else "Calendar Event"
                        start = dtstart_match.group(1).strip() if dtstart_match else ""
                        end = dtend_match.group(1).strip() if dtend_match else start

                        events.append(
                            CalendarEvent(
                                id=f"ics_{idx}",
                                title=summary,
                                start=start,
                                end=end,
                                is_all_day="VALUE=DATE" in (dtstart_match.group(0) if dtstart_match else ""),
                                location=None
                            )
                        )
            except Exception:
                pass
        return events

    @classmethod
    async def fetch_public_holidays(cls, country_code: str = "IN") -> List[CalendarEvent]:
        events: List[CalendarEvent] = []
        year = datetime.datetime.now().year
        url = f"{cls.NAGER_API_URL}/{year}/{country_code}"
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    for item in data[:5]:
                        events.append(
                            CalendarEvent(
                                id=f"holiday_{item.get('date')}",
                                title=f"Holiday: {item.get('name', 'Public Holiday')}",
                                start=f"{item.get('date')}T00:00:00Z",
                                end=f"{item.get('date')}T23:59:59Z",
                                is_all_day=True,
                                location=item.get("countryCode")
                            )
                        )
            except Exception:
                pass
        return events

    @classmethod
    async def get_calendar_events(cls, ics_url: Optional[str] = None, country_code: str = "IN") -> List[CalendarEvent]:
        if ics_url:
            user_events = await cls.fetch_ics_events(ics_url)
            if user_events:
                return user_events

        return await cls.fetch_public_holidays(country_code)
