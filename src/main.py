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
