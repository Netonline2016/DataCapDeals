# Filfox DataCap Deal Fetcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI tool that fetches all deals for a given Filecoin address from Filfox API and exports to JSON + CSV.

**Architecture:** Modular design with `models.py` (data structures), `output.py` (serialization), `api.py` (HTTP client with pagination), and `main.py` (CLI orchestration). Uses `requests` for HTTP, `dataclasses` for typing, `argparse` for CLI.

**Tech Stack:** Python 3.8+, `requests`, `pytest`, standard library (`dataclasses`, `argparse`, `csv`, `json`, `time`).

---

### Task 1: Deal Model

**Files:**
- Create: `src/models.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: Write the failing test**

```python
from src.models import Deal

def test_deal_from_dict():
    data = {
        "id": 123,
        "height": 100,
        "timestamp": 1600000000,
        "pieceSize": 34359738368,
        "verifiedDeal": True,
        "client": "f1abc",
        "provider": "f01313",
        "startEpoch": 200,
        "startTimestamp": 1600000100,
        "endEpoch": 300,
        "endTimestamp": 1600000200,
        "stroagePrice": "0"
    }
    deal = Deal.from_dict(data)
    assert deal.id == 123
    assert deal.provider == "f01313"
    assert deal.verified_deal is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py::test_deal_from_dict -v`
Expected: FAIL — `Deal` not defined or `from_dict` missing

- [ ] **Step 3: Implement Deal dataclass**

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Deal:
    id: int
    height: int
    timestamp: int
    piece_size: int
    verified_deal: bool
    client: str
    provider: str
    start_epoch: int
    start_timestamp: int
    end_epoch: int
    end_timestamp: int
    storage_price: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Deal":
        return cls(
            id=data["id"],
            height=data["height"],
            timestamp=data["timestamp"],
            piece_size=data["pieceSize"],
            verified_deal=data["verifiedDeal"],
            client=data["client"],
            provider=data["provider"],
            start_epoch=data["startEpoch"],
            start_timestamp=data["startTimestamp"],
            end_epoch=data["endEpoch"],
            end_timestamp=data["endTimestamp"],
            storage_price=data["stroagePrice"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "height": self.height,
            "timestamp": self.timestamp,
            "pieceSize": self.piece_size,
            "verifiedDeal": self.verified_deal,
            "client": self.client,
            "provider": self.provider,
            "startEpoch": self.start_epoch,
            "startTimestamp": self.start_timestamp,
            "endEpoch": self.end_epoch,
            "endTimestamp": self.end_timestamp,
            "stroagePrice": self.storage_price,
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py::test_deal_from_dict -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add Deal dataclass with from_dict/to_dict"
```

---

### Task 2: Output Module (JSON/CSV)

**Files:**
- Create: `src/output.py`
- Test: `tests/test_output.py`

- [ ] **Step 1: Write the failing test**

```python
import json
import csv
import os
from src.models import Deal
from src.output import write_json, write_csv

def test_write_json(tmp_path):
    deals = [Deal(
        id=1, height=100, timestamp=1600000000, piece_size=34359738368,
        verified_deal=True, client="f1abc", provider="f01313",
        start_epoch=200, start_timestamp=1600000100, end_epoch=300,
        end_timestamp=1600000200, storage_price="0"
    )]
    filepath = tmp_path / "deals.json"
    write_json(deals, str(filepath))
    with open(filepath) as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["provider"] == "f01313"

def test_write_csv(tmp_path):
    deals = [Deal(
        id=1, height=100, timestamp=1600000000, piece_size=34359738368,
        verified_deal=True, client="f1abc", provider="f01313",
        start_epoch=200, start_timestamp=1600000100, end_epoch=300,
        end_timestamp=1600000200, storage_price="0"
    )]
    filepath = tmp_path / "deals.csv"
    write_csv(deals, str(filepath))
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["provider"] == "f01313"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_output.py -v`
Expected: FAIL — `write_json` / `write_csv` not defined

- [ ] **Step 3: Implement output module**

```python
import csv
import json
from typing import List
from src.models import Deal


def write_json(deals: List[Deal], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([deal.to_dict() for deal in deals], f, indent=2, ensure_ascii=False)


def write_csv(deals: List[Deal], filepath: str) -> None:
    if not deals:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return

    fieldnames = list(deals[0].to_dict().keys())
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for deal in deals:
            writer.writerow(deal.to_dict())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_output.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/output.py tests/test_output.py
git commit -m "feat: add JSON and CSV output writers"
```

---

### Task 3: API Client with Pagination

**Files:**
- Create: `src/api.py`
- Test: `tests/test_api.py`
- Create: `requirements.txt`

- [ ] **Step 1: Add dependency**

`requirements.txt`:
```
requests>=2.25.0
```

- [ ] **Step 2: Write the failing test**

```python
import json
from unittest.mock import Mock, patch
from src.api import FilfoxClient
from src.models import Deal

def test_get_deals_single_page():
    mock_response = Mock()
    mock_response.json.return_value = {
        "totalCount": 2,
        "deals": [
            {"id": 1, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
             "endTimestamp": 1600000200, "stroagePrice": "0"},
            {"id": 2, "height": 101, "timestamp": 1600000001, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 201, "startTimestamp": 1600000101, "endEpoch": 301,
             "endTimestamp": 1600000201, "stroagePrice": "0"},
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.Session.get", return_value=mock_response) as mock_get:
        client = FilfoxClient()
        deals = client.get_deals("f01313", page_size=100, delay_ms=0)

    assert len(deals) == 2
    assert deals[0].id == 1
    assert deals[1].id == 2
    assert mock_get.call_count == 1


def test_get_deals_multiple_pages():
    def mock_get(url, params=None, **kwargs):
        resp = Mock()
        resp.raise_for_status.return_value = None
        page = params.get("page", 0)
        if page == 0:
            resp.json.return_value = {
                "totalCount": 150,
                "deals": [{"id": i, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
                           "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
                           "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
                           "endTimestamp": 1600000200, "stroagePrice": "0"} for i in range(100)]
            }
        else:
            resp.json.return_value = {
                "totalCount": 150,
                "deals": [{"id": i + 100, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
                           "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
                           "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
                           "endTimestamp": 1600000200, "stroagePrice": "0"} for i in range(50)]
            }
        return resp

    with patch("requests.Session.get", side_effect=mock_get):
        client = FilfoxClient()
        deals = client.get_deals("f01313", page_size=100, delay_ms=0)

    assert len(deals) == 150
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_api.py -v`
Expected: FAIL — `FilfoxClient` not defined

- [ ] **Step 4: Implement API client**

```python
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
                if response.status_code >= 400 and response.status_code < 500:
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
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/api.py tests/test_api.py requirements.txt
git commit -m "feat: add FilfoxClient with automatic pagination and retries"
```

---

### Task 4: CLI Entrypoint

**Files:**
- Create: `src/main.py`
- Modify: `src/__init__.py` (ensure package marker exists)
- Test: `tests/test_main.py`

- [ ] **Step 1: Create package marker**

`src/__init__.py`:
```python
# Package marker
```

- [ ] **Step 2: Write the failing test**

```python
import json
import os
from unittest.mock import Mock, patch
from src.main import main

def test_main_cli(tmp_path, monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {
        "totalCount": 1,
        "deals": [
            {"id": 1, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
             "endTimestamp": 1600000200, "stroagePrice": "0"},
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.Session.get", return_value=mock_response):
        monkeypatch.chdir(tmp_path)
        main(["--address", "f01313", "--output-dir", str(tmp_path / "out"), "--delay", "0"])

        json_path = tmp_path / "out" / "f01313_deals.json"
        csv_path = tmp_path / "out" / "f01313_deals.csv"
        assert json_path.exists()
        assert csv_path.exists()

        with open(json_path) as f:
            data = json.load(f)
        assert len(data) == 1
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_main.py::test_main_cli -v`
Expected: FAIL — `main` not defined or argument parsing missing

- [ ] **Step 4: Implement CLI**

```python
import argparse
import os
import sys
from typing import List

from src.api import FilfoxClient
from src.output import write_json, write_csv


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch deals for a Filecoin address from Filfox API"
    )
    parser.add_argument(
        "--address", "-a", required=True, help="Provider or client address"
    )
    parser.add_argument(
        "--output-dir", "-o", default="./output", help="Output directory"
    )
    parser.add_argument(
        "--page-size", type=int, default=100, help="Items per page"
    )
    parser.add_argument(
        "--delay", type=int, default=200, help="Milliseconds between page requests"
    )
    return parser.parse_args(args)


def main(args: List[str] = None) -> None:
    if args is None:
        args = sys.argv[1:]

    parsed = parse_args(args)
    os.makedirs(parsed.output_dir, exist_ok=True)

    client = FilfoxClient()
    print(f"Fetching deals for {parsed.address} ...")
    deals = client.get_deals(parsed.address, page_size=parsed.page_size, delay_ms=parsed.delay)
    print(f"Fetched {len(deals)} deals.")

    json_path = os.path.join(parsed.output_dir, f"{parsed.address}_deals.json")
    csv_path = os.path.join(parsed.output_dir, f"{parsed.address}_deals.csv")

    write_json(deals, json_path)
    write_csv(deals, csv_path)

    print(f"Output written to:")
    print(f"  {json_path}")
    print(f"  {csv_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_main.py::test_main_cli -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/main.py src/__init__.py tests/test_main.py
git commit -m "feat: add CLI entrypoint with argparse"
```

---

### Task 5: README and Final Verification

**Files:**
- Create: `README.md`
- Modify: `tests/` (ensure `__init__.py` exists for package imports)

- [ ] **Step 1: Create tests package marker**

`tests/__init__.py`:
```python
# Test package marker
```

- [ ] **Step 2: Write README**

```markdown
# Filfox DataCap Deal Fetcher

Fetch all Filecoin deals for a specific provider or client from the Filfox API.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main --address f01313
python -m src.main --address f1ogcgz4a6bmsmcdk3nnksw4yac5syis4tpqxd7by --output-dir ./deals --delay 200
```

## Options

- `--address` / `-a`: Target provider or client address (required)
- `--output-dir` / `-o`: Output directory (default: `./output`)
- `--page-size`: Items per page (default: 100)
- `--delay`: Milliseconds between page requests (default: 200)

## Output

Generates `{address}_deals.json` and `{address}_deals.csv` in the output directory.

## Tests

```bash
pytest tests/ -v
```
```

- [ ] **Step 3: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add README.md tests/__init__.py
git commit -m "docs: add README and test package marker"
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| Deal dataclass with API field mapping | Task 1 |
| JSON/CSV output | Task 2 |
| FilfoxClient with pagination, retries, delay | Task 3 |
| CLI with `--address`, `--output-dir`, `--page-size`, `--delay` | Task 4 |
| Sequential fetch with 200ms default delay | Task 3 + 4 |
| Error handling (retries, 4xx abort) | Task 3 |

## Placeholder Scan

- No TBD/TODO/fill-in-later references found.
- All steps contain complete code or exact commands.

## Type Consistency Check

- `Deal.from_dict` / `Deal.to_dict` signatures consistent across all tasks.
- `FilfoxClient.get_deals` signature matches design doc.
- `write_json` / `write_csv` signatures consistent.
