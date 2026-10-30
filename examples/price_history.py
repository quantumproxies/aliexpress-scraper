"""Daily price and orders history for the top AliExpress results of a keyword.

Appends one row per item to aliexpress_history.csv with a UTC timestamp, so you
can see which items gain orders or change price. Run it from cron:

    0 8 * * *  cd /path/to/here && python price_history.py "running shoes" --top 50

Needs a login (`aliexpress-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_aliexpress_scraper import AliExpressScraper

FIELDS = ["checked_at", "keyword", "rank", "product_id", "price_value", "original_price_value", "currency",
          "discount_percent", "orders_count", "rating", "choice", "title"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--top", type=int, default=50, help="results per keyword (max 250)")
    parser.add_argument("--out", default="aliexpress_history.csv")
    args = parser.parse_args()

    aliexpress = AliExpressScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for keyword in args.keywords:
            for item in aliexpress.search(keyword, country=args.country, currency=args.currency, max_results=args.top):
                writer.writerow({"checked_at": checked_at, "keyword": keyword, **item})
                written += 1
    print(f"{written} rows appended to {args.out}")


if __name__ == "__main__":
    main()
