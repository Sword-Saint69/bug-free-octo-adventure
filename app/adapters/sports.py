import httpx
from datetime import datetime, timezone
from typing import List, Optional
from app.schemas.dashboard import F1NextRace, SportsMatch, SportsModule

class SportsAdapter:
    # Keyless Jolpi / Ergast F1 API endpoint for current season next race
    F1_NEXT_RACE_URL = "https://api.jolpi.ca/ergast/f1/current/next.json"
    # OpenLigaDB is a documented, keyless community sports API.
    OPENLIGA_URL = "https://api.openligadb.de/getmatchdata/bl1/{season}"

    @classmethod
    async def fetch_f1_next_race(cls) -> Optional[F1NextRace]:
        headers = {"User-Agent": "Mosaic-Dashboard/1.0"}
        async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
            try:
                res = await client.get(cls.F1_NEXT_RACE_URL)
                if res.status_code == 200:
                    races = res.json().get("MRData", {}).get("RaceTable", {}).get("Races", [])
                    if races:
                        race = races[0]
                        circuit = race.get("Circuit", {})
                        location = circuit.get("Location", {})
                        return F1NextRace(
                            race_name=race.get("raceName", "Grand Prix"),
                            circuit_name=circuit.get("circuitName", "Autodromo"),
                            country=location.get("country", "Global"),
                            date=race.get("date", ""),
                            time_utc=race.get("time", "14:00:00Z"),
                            round=int(race.get("round", 1))
                        )
            except Exception:
                return None
        return None

    @classmethod
    async def fetch_sports_matches(cls) -> List[SportsMatch]:
        headers = {"User-Agent": "Mosaic-Dashboard/1.0"}
        matches: List[SportsMatch] = []
        now = datetime.now(timezone.utc)
        # European football seasons begin in the current calendar year after July.
        season = now.year if now.month >= 7 else now.year - 1
        async with httpx.AsyncClient(timeout=8.0, headers=headers) as client:
            try:
                response = await client.get(cls.OPENLIGA_URL.format(season=season))
                response.raise_for_status()
                events = response.json()
                upcoming = []
                completed = []
                for event in events:
                    event_time = datetime.fromisoformat(
                        event.get("matchDateTimeUTC", "").replace("Z", "+00:00")
                    )
                    (completed if event.get("matchIsFinished") else upcoming).append((event_time, event))
                selected = sorted(upcoming, key=lambda item: item[0])[:4]
                if not selected:
                    selected = sorted(completed, key=lambda item: item[0], reverse=True)[:4]

                for event_time, event in selected:
                    results = event.get("matchResults", [])
                    final_result = next((r for r in results if r.get("resultTypeID") == 2), None)
                    matches.append(
                        SportsMatch(
                            sport="Football",
                            tournament=event.get("leagueName", "Bundesliga"),
                            team1=event.get("team1", {}).get("teamName", "Home"),
                            team2=event.get("team2", {}).get("teamName", "Away"),
                            score1=str(final_result.get("pointsTeam1")) if final_result else None,
                            score2=str(final_result.get("pointsTeam2")) if final_result else None,
                            status="Finished" if event.get("matchIsFinished") else event_time.strftime("%d %b, %H:%M UTC"),
                        )
                    )
            except (httpx.HTTPError, ValueError, TypeError, KeyError):
                return []

        return matches

    @classmethod
    async def get_sports_module(cls) -> SportsModule:
        f1_race = await cls.fetch_f1_next_race()
        matches = await cls.fetch_sports_matches()
        return SportsModule(f1_next_race=f1_race, matches=matches)
