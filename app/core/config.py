import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Project Configuration Settings:
    Ee class .env file-il ninnu environment variables auto-load cheyyunnu.
    """
    PROJECT_NAME: str = "Microcontroller Dashboard API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    
    # Cloud API Coordinates (Default: Bhubaneswar / India)
    DEFAULT_LATITUDE: float = 20.2961
    DEFAULT_LONGITUDE: float = 85.8245
    DEFAULT_COUNTRY_CODE: str = "IN"

    # Optional API Keys (100% keyless fallback undenkilum custom keys nalkam)
    OPENAQ_API_KEY: str = ""
    COINGECKO_API_KEY: str = ""
    NASA_API_KEY: str = "DEMO_KEY"
    RUNTIME_CONFIG_PATH: str = ""
    CORS_ORIGINS: str = "*"

    class Config:
        case_sensitive = True
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = "utf-8"

settings = Settings()
