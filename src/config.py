from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "SiloFlow"
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)
    APP_PORT: int = Field(default=8001)
    APP_SECRET_KEY: str = Field(default="change-me")
    DATABASE_URL: str = Field(default="postgresql+asyncpg://siloflow:password@localhost:5432/siloflow")
    DATABASE_POOL_SIZE: int = Field(default=15)
    REDIS_URL: str = Field(default="redis://localhost:6379/1")
    MODEL_DIR: str = Field(default="./models")
    ROCM_ENABLED: bool = Field(default=False)
    ROCM_DEVICE_ID: int = Field(default=0)
    WEATHER_API_KEY: str = Field(default="")
    SATELLITE_API_KEY: str = Field(default="")
    LOG_LEVEL: str = Field(default="INFO")
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
