from fastapi import APIRouter

from app.config import settings
from app.models import BotConfig
from app.services.orchestrator import execute_scan

router = APIRouter()
runtime_config = BotConfig(
    timeframe=settings.default_timeframe,
    strategy=settings.default_strategy,
    symbols=[item.strip() for item in settings.tradingview_symbols.split(",") if item.strip()],
)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/config", response_model=BotConfig)
def get_config() -> BotConfig:
    return runtime_config


@router.post("/config", response_model=BotConfig)
def set_config(new_config: BotConfig) -> BotConfig:
    global runtime_config
    runtime_config = new_config
    return runtime_config


@router.post("/scan")
def run_scan() -> dict:
    return execute_scan(runtime_config)
