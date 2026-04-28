import logging
import time

from app.config import settings
from app.models import BotConfig
from app.services.orchestrator import execute_scan

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def build_worker_config() -> BotConfig:
    return BotConfig(
        timeframe=settings.default_timeframe,
        strategy=settings.default_strategy,
        live_trading_enabled=False,  # Keep worker in paper mode until explicitly enabled.
        news_filter_enabled=True,
        symbols=[item.strip() for item in settings.tradingview_symbols.split(",") if item.strip()],
    )


def main() -> None:
    config = build_worker_config()
    interval = max(settings.news_poll_interval_seconds, 60)
    logger.info("Worker started with interval=%s seconds and timeframe=%s", interval, config.timeframe)

    while True:
        try:
            result = execute_scan(config)
            logger.info("Scan complete. signals=%s", len(result["signals"]))
        except Exception:  # noqa: BLE001
            logger.exception("Worker scan cycle failed")
        time.sleep(interval)


if __name__ == "__main__":
    main()
