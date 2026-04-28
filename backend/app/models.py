from typing import Literal

from pydantic import BaseModel, Field


class BotConfig(BaseModel):
    timeframe: str = Field(default="5m", examples=["5m", "15m", "1h"])
    strategy: str = Field(default="breakout_v1")
    live_trading_enabled: bool = False
    news_filter_enabled: bool = True
    symbols: list[str] = Field(default_factory=lambda: ["BTCUSDT", "ETHUSDT"])


class MarketSnapshot(BaseModel):
    symbol: str
    timeframe: str
    close: float
    volume: float
    indicators: dict[str, float]


class EconomicEvent(BaseModel):
    title: str
    impact: Literal["low", "medium", "high"]
    currency: str
    minutes_to_event: int


class Signal(BaseModel):
    symbol: str
    timeframe: str
    strategy: str
    side: Literal["buy", "sell", "neutral"]
    confidence: float = Field(ge=0, le=1)
    reason: str
    risk_note: str
