import uuid
from typing import Optional
from fastapi import APIRouter, Header
from app.schemas.response import StandardResponse
from app.schemas.dashboard import DashboardSnapshot, AirQualityModule
from app.services.weather_service import WeatherService
from app.services.calendar_service import CalendarService
from app.services.crypto_service import CryptoService
from app.services.fx_service import FXService
from app.services.earthquake_service import EarthquakeService
from app.services.news_service import NewsService
from app.services.tasks_service import TasksService
from app.services.stocks_service import StocksService
from app.services.sports_service import SportsService
from app.services.daily_content_service import DailyContentService
from app.services.media_service import MediaService
from app.services.air_quality_service import AirQualityService

router = APIRouter()

@router.get("/device/dashboard", response_model=StandardResponse[DashboardSnapshot], summary="ESP32 Dashboard Single Snapshot API")
async def get_device_dashboard(
    authorization: str = Header(...),
    x_device_id: str = Header(...),
    x_firmware_version: str = Header("1.0.0"),
    x_hardware_revision: str = Header("esp32s3_v1"),
    latitude: float = 20.2961,
    longitude: float = 85.8245,
    country_code: str = "IN",
    ics_url: Optional[str] = None
):
    """
    ESP32-S3 TFT Display-kk vendiyulla single aggregated snapshot endpoint.
    Ee function 100% keyless live APIs vazhi Weather, AQI, Crypto, Stocks, Sports/F1, Daily Quotes/Trivia, Spotify Media Player, FX rates, Earthquakes, News, NASA Space APOD, matrum Dynamic Tasks fetch cheythu array/JSON summary aayi nalkunnu.
    """
    weather_data = await WeatherService.get_weather(latitude, longitude)
    air_quality_data = await AirQualityService.get_air_quality(latitude, longitude)
    calendar_events = await CalendarService.get_calendar_events(ics_url=ics_url, country_code=country_code)
    crypto_quotes = await CryptoService.get_crypto_prices()
    fx_rates = await FXService.get_fx_rates()
    earthquakes = await EarthquakeService.get_recent_earthquakes()
    news_headlines = await NewsService.get_curated_news()
    space_apod = await NewsService.get_space_apod()
    user_tasks = await TasksService.get_user_tasks()
    stock_quotes = await StocksService.get_stocks()
    sports_module = await SportsService.get_sports()
    daily_content = await DailyContentService.get_daily_content()
    media_player = await MediaService.get_media_player()
    
    snapshot = DashboardSnapshot(
        device_id=x_device_id,
        theme="dark",
        brightness=85,
        weather=weather_data,
        air_quality=air_quality_data,
        calendar=calendar_events,
        tasks=user_tasks,
        crypto=crypto_quotes,
        fx_rates=fx_rates,
        earthquakes=earthquakes,
        news=news_headlines,
        space_apod=space_apod,
        stocks=stock_quotes,
        sports=sports_module,
        daily_content=daily_content,
        media_player=media_player
    )
    
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=snapshot
    )
