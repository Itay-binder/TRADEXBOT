import requests

from app.models import Signal


class PickMyTradeClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def submit_signal(self, signal: Signal) -> None:
        if not self.api_key:
            return

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = signal.model_dump()
        requests.post(f"{self.base_url}/signals", json=payload, headers=headers, timeout=10)
