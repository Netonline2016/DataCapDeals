import json
import csv
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
