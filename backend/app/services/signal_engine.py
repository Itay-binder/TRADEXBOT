from app.models import BotConfig, EconomicEvent, MarketSnapshot, Signal


class AIModelStub:
    def infer(self, snapshot: MarketSnapshot, strategy: str) -> tuple[str, float, str]:
        # Placeholder for your trained model inference.
        rsi = snapshot.indicators.get("rsi", 50)
        if rsi < 35:
            return "buy", 0.78, f"{strategy}: RSI indicates oversold"
        if rsi > 65:
            return "sell", 0.75, f"{strategy}: RSI indicates overbought"
        return "neutral", 0.52, f"{strategy}: No strong setup"


class SignalEngine:
    def __init__(self) -> None:
        self.model = AIModelStub()

    def build_signals(
        self,
        config: BotConfig,
        snapshots: list[MarketSnapshot],
        events: list[EconomicEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []
        high_impact_soon = any(event.impact == "high" and event.minutes_to_event <= 60 for event in events)

        for snapshot in snapshots:
            side, confidence, reason = self.model.infer(snapshot, config.strategy)
            risk_note = "Reduce size: high-impact economic event soon" if high_impact_soon else "Normal risk"
            signals.append(
                Signal(
                    symbol=snapshot.symbol,
                    timeframe=config.timeframe,
                    strategy=config.strategy,
                    side=side,
                    confidence=confidence,
                    reason=reason,
                    risk_note=risk_note,
                )
            )
        return signals
