from app.models import MarketSnapshot


class TradingViewClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_market_data(self, symbols: list[str], timeframe: str) -> list[MarketSnapshot]:
        # TODO: replace with real TradingView/broker data bridge.
        snapshots: list[MarketSnapshot] = []
        for symbol in symbols:
            snapshots.append(
                MarketSnapshot(
                    symbol=symbol,
                    timeframe=timeframe,
                    close=100.0,
                    volume=2000.0,
                    indicators={"rsi": 52.1, "ema_fast": 99.8, "ema_slow": 98.9},
                )
            )
        return snapshots
