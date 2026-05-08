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
