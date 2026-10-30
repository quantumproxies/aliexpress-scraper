"""Shortlist AliExpress products for a store: well rated and already selling.

    python product_shortlist.py "running shoes" "yoga mat" --min-rating 4.5 --top 20

Searches each keyword, drops sponsored cards, keeps the items rated at or
above --min-rating, sorts them by units sold and writes the best --top per
keyword to shortlist.csv with price, discount, orders and delivery window.
"""

import argparse

from quanticdata_aliexpress_scraper import AliExpressScraper, write

FIELDS = ["rank", "product_id", "title", "price_value", "currency", "original_price_value", "discount_percent",
          "rating", "orders_count", "choice", "free_shipping", "delivery_date_min", "delivery_date_max", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us", help="local AliExpress site, e.g. us, it, de")
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--scan", type=int, default=120, help="results to scan per keyword (max 250)")
    parser.add_argument("--min-rating", type=float, default=4.5)
    parser.add_argument("--top", type=int, default=20, help="items to keep per keyword")
    parser.add_argument("--out", default="shortlist.csv")
    args = parser.parse_args()

    aliexpress = AliExpressScraper()
    rows = []
    for keyword in args.keywords:
        run = aliexpress.search(keyword, country=args.country, currency=args.currency, max_results=args.scan)
        rated = [r for r in run if not r.get("sponsored") and (r.get("rating") or 0) >= args.min_rating]
        rated.sort(key=lambda r: r.get("orders_count") or 0, reverse=True)
        picked = rated[:args.top]
        print(f"{keyword!r}: {len(run)} scanned, {len(rated)} rated {args.min_rating}+, {len(picked)} kept")
        rows.extend({"keyword": keyword, **{k: r.get(k) for k in FIELDS}} for r in picked)

    write(rows, args.out)
    print(f"{len(rows)} items written to {args.out}")


if __name__ == "__main__":
    main()
