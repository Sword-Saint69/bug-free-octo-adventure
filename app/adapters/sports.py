import httpx
from typing import List, Optional
from app.schemas.dashboard import F1NextRace, SportsMatch, SportsModule

class SportsAdapter:
    # Keyless Jolpi / Ergast F1 API endpoint for current season next race
    F1_NEXT_RACE_URL = "https://api.jolpi.ca/ergast/f1/current/next.json"
    # Public keyless ESPN Scoreboard APIs
    ESPN_SOCCER_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    ESPN_CRICKET_URL = "https://site.api.espn.com/apis/site/v2/sports/cricket/general/scoreboard"

    @classmethod
    async def fetch_f1_next_race(cls) -> Optional[F1NextRace]:
        headers = {"User-Agent": "Mozilla/5.0"}
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
        headers = {"User-Agent": "Mozilla/5.0"}
        matches: List[SportsMatch] = []
        async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
            # 1. Fetch live Premier League Soccer matches
            try:
                res = await client.get(cls.ESPN_SOCCER_URL)
                if res.status_code == 200:
                    events = res.json().get("events", [])[:3]
                    for ev in events:
                        competitions = ev.get("competitions", [])[0]
                        competitors = competitions.get("competitors", [])
                        if len(competitors) >= 2:
                            t1 = competitors[0].get("team", {}).get("shortDisplayName", "Team A")
                            s1 = competitors[0].get("score", "0")
                            t2 = competitors[1].get("team", {}).get("shortDisplayName", "Team B")
                            s2 = competitors[1].get("score", "0")
                            status = ev.get("status", {}).get("type", {}).get("shortDetail", "Scheduled")
                            matches.append(
                                SportsMatch(
                                    sport="Football",
                                    tournament="Premier League",
                                    team1=t1,
                                    team2=t2,
                                    score1=s1,
                                    score2=s2,
                                    status=status
                                )
                            )
            except Exception:
                pass

        return matches

    @classmethod
    async def get_sports_module(cls) -> SportsModule:
        f1_race = await cls.fetch_f1_next_race()
        matches = await cls.fetch_sports_matches()
        return SportsModule(f1_next_race=f1_race, matches=matches)
