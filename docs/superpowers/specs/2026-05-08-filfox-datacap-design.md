# Filfox DataCap Deal Fetcher — Design

## Overview
A Python CLI tool that fetches all Deal entries for a specific Filecoin Provider or Client from the Filfox API, exporting results in both JSON and CSV formats.

## API Behavior
- Endpoint: `GET https://filfox.info/api/v1/deal/list`
- Server-side filtering via `address` query parameter (works for both provider IDs and client addresses).
- Returns: `{ "totalCount": int, "deals": [...] }`
- Supports `page` (0-indexed) and `pageSize` pagination.

## Project Structure
```
filfox-datacap/
├── src/
│   ├── __init__.py
│   ├── api.py          # FilfoxClient: API calls + automatic pagination
│   ├── models.py       # Deal dataclass
│   ├── output.py       # JSON/CSV serialization
│   └── main.py         # CLI entrypoint
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```

## Module Design

### `api.py` — `FilfoxClient`
- `__init__(base_url="https://filfox.info/api/v1", max_retries=3)`
- `get_deals(address: str, page_size: int = 100, delay_ms: int = 200) -> List[Deal]`
  1. Request page 0 to obtain `totalCount`.
  2. Compute total pages: `ceil(totalCount / page_size)`.
  3. Sequentially fetch remaining pages with `delay_ms` sleep between requests.
  4. Accumulate and return all deals.
- Retries: exponential backoff on network errors and 5xx (max 3 attempts per page).

### `models.py` — `Deal`
Dataclass fields:
- `id`, `height`, `timestamp`, `pieceSize`, `verifiedDeal`, `client`, `provider`, `startEpoch`, `startTimestamp`, `endEpoch`, `endTimestamp`, `stroagePrice`

### `output.py`
- `write_json(deals: List[Deal], filepath: str)`
- `write_csv(deals: List[Deal], filepath: str)`

### `main.py` — CLI
Arguments:
- `--address` / `-a` (required): target provider or client address
- `--output-dir` / `-o` (default: `./output`): output directory
- `--page-size` (default: 100): items per page
- `--delay` (default: 200): milliseconds between page requests

Output files:
- `{address}_deals.json`
- `{address}_deals.csv`

## Data Flow
```
CLI (--address) → main.py → FilfoxClient.get_deals(address)
    → page 0 (get totalCount) → compute pages → sequential fetch with delay
    → merge all deals → output.py writes JSON + CSV
```

## Error Handling
- Network / 5xx: retry 3 times with exponential backoff.
- Single page fails permanently: abort immediately, print error + progress (pages fetched / total).
- 4xx (invalid address): abort immediately with clear message.
