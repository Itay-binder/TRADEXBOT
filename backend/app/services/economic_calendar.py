from app.models import EconomicEvent


class EconomicCalendarClient:
    def __init__(self, api_key: str, source: str) -> None:
        self.api_key = api_key
        self.source = source

    def upcoming_events(self) -> list[EconomicEvent]:
        # TODO: replace with real Investing/ForexFactory provider integration.
        return [
            EconomicEvent(
                title="US CPI Release",
                impact="high",
                currency="USD",
                minutes_to_event=45,
            )
        ]
