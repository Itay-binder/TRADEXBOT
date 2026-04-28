from app.config import settings
from app.models import BotConfig
from app.services.economic_calendar import EconomicCalendarClient
from app.services.notifier import WhatsAppNotifier
from app.services.pickmytrade import PickMyTradeClient
from app.services.signal_engine import SignalEngine
from app.services.tradingview_client import TradingViewClient


def execute_scan(config: BotConfig) -> dict:
    market_client = TradingViewClient(api_key=settings.tradingview_api_key)
    calendar_client = EconomicCalendarClient(
        api_key=settings.economic_calendar_api_key,
        source=settings.economic_calendar_source,
    )
    signal_engine = SignalEngine()
    notifier = WhatsAppNotifier(settings.whatsapp_webhook_url)
    execution_client = PickMyTradeClient(settings.pickmytrade_base_url, settings.pickmytrade_api_key)

    snapshots = market_client.fetch_market_data(config.symbols, config.timeframe)
    events = calendar_client.upcoming_events() if config.news_filter_enabled else []
    signals = signal_engine.build_signals(config, snapshots, events)

    for signal in signals:
        notifier.send(signal)
        if config.live_trading_enabled:
            execution_client.submit_signal(signal)

    return {
        "config": config.model_dump(),
        "economic_events": [event.model_dump() for event in events],
        "signals": [signal.model_dump() for signal in signals],
    }
