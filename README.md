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
