from typing import Optional, List
from pydantic import BaseModel

class WeatherModule(BaseModel):
    temperature: float
    apparent_temperature: float
    condition_code: int
    humidity: int
    rain_probability: int
    wind_speed: float
    wind_direction: int
    is_day: bool
    provider: str = "Open-Meteo"
    freshness_sec: int

class AirQualityModule(BaseModel):
    pm2_5: float
    pm10: float
    aqi_category: str
    station_source: str
    freshness_sec: int

class CalendarEvent(BaseModel):
    id: str
    title: str
    start: str
    end: str
    is_all_day: bool
    location: Optional[str] = None

class CryptoQuote(BaseModel):
    symbol: str
    price_usd: float
    change_24h: float

class CurrencyRate(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    rate_date: str

class EarthquakeEvent(BaseModel):
    id: str
    magnitude: float
    place: str
    time: int
    url: str

class NewsHeadline(BaseModel):
    title: str
    publisher: str
    published_at: str
    category: str = "General"

class SpaceApodItem(BaseModel):
    title: str
    explanation: str
    date: str
    url: Optional[str] = None

class TaskItem(BaseModel):
    id: str
    title: str
    completed: bool = False
    priority: str = "medium"
    due_time: Optional[str] = None

class StockQuote(BaseModel):
    symbol: str
    name: str
    price: float
    change_amount: float
    change_percent: float
    currency: str = "USD"

class F1NextRace(BaseModel):
    race_name: str
    circuit_name: str
    country: str
    date: str
    time_utc: str
    round: int

class SportsMatch(BaseModel):
    sport: str
    tournament: str
    team1: str
    team2: str
    score1: Optional[str] = None
    score2: Optional[str] = None
    status: str

class SportsModule(BaseModel):
    f1_next_race: Optional[F1NextRace] = None
    matches: List[SportsMatch] = []

class DailyQuote(BaseModel):
    quote: str
    author: str

class TriviaQuestion(BaseModel):
    question: str
    correct_answer: str
    options: List[str]
    category: str
    difficulty: str

class WordOfTheDay(BaseModel):
    word: str
    definition: str
    part_of_speech: str
    example: str

class DailyContentModule(BaseModel):
    quote: Optional[DailyQuote] = None
    trivia: Optional[TriviaQuestion] = None
    word_of_the_day: Optional[WordOfTheDay] = None

class MediaPlayerModule(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    is_playing: bool = False
    progress_ms: int = 0
    duration_ms: int = 0
    album_art_url: Optional[str] = None

class DashboardSnapshot(BaseModel):
    device_id: str
    theme: str = "dark"
    brightness: int = 80
    weather: Optional[WeatherModule] = None
    air_quality: Optional[AirQualityModule] = None
    calendar: List[CalendarEvent] = []
    tasks: List[TaskItem] = []
    crypto: List[CryptoQuote] = []
    fx_rates: List[CurrencyRate] = []
    earthquakes: List[EarthquakeEvent] = []
    news: List[NewsHeadline] = []
    space_apod: Optional[SpaceApodItem] = None
    stocks: List[StockQuote] = []
    sports: Optional[SportsModule] = None
    daily_content: Optional[DailyContentModule] = None
    media_player: Optional[MediaPlayerModule] = None
