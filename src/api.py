import math
import time
from typing import List, Any

import requests

from src.models import Deal


class FilfoxClient:
    def __init__(self, base_url: str = "https://filfox.info/api/v1", max_retries: int = 3):
        self.base_url = base_url
        self.max_retries = max_retries
        self.session = requests.Session()

    def _get(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                last_exception = e
                if hasattr(response, 'status_code') and 400 <= response.status_code < 500:
                    raise
                wait = 2 ** attempt
                time.sleep(wait)
        raise last_exception

    def get_deals(self, address: str, page_size: int = 100, delay_ms: int = 200) -> List[Deal]:
        url = f"{self.base_url}/deal/list"
        params = {"address": address, "pageSize": page_size, "page": 0}

        data = self._get(url, params)
        total_count = data["totalCount"]
        deals = [Deal.from_dict(d) for d in data.get("deals", [])]

        total_pages = math.ceil(total_count / page_size)
        for page in range(1, total_pages):
            params["page"] = page
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)
            data = self._get(url, params)
            deals.extend(Deal.from_dict(d) for d in data.get("deals", []))

        return deals
