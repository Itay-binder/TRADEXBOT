import requests

from app.models import Signal


class WhatsAppNotifier:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, signal: Signal) -> None:
        if not self.webhook_url:
            return

        payload = {
            "text": (
                f"TRADEXBOT Signal | {signal.symbol} {signal.timeframe}\n"
                f"Side: {signal.side}\n"
                f"Confidence: {signal.confidence:.2f}\n"
                f"Reason: {signal.reason}\n"
                f"Risk: {signal.risk_note}"
            )
        }
        requests.post(self.webhook_url, json=payload, timeout=10)
