from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TRADEXBOT"
    app_env: str = "development"
    log_level: str = "INFO"

    default_timeframe: str = "5m"
    default_strategy: str = "breakout_v1"

    tradingview_api_key: str = ""
    tradingview_symbols: str = "BTCUSDT,ETHUSDT"

    economic_calendar_api_key: str = ""
    economic_calendar_source: str = "investing"

    whatsapp_webhook_url: str = ""
    pickmytrade_api_key: str = ""
    pickmytrade_base_url: str = "https://api.pickmytrade.trade"


settings = Settings()
