"""The same AliExpress search on several local sites, compared side by side.

    python market_compare.py "phone case" --markets us:USD it:EUR de:EUR --top 30

For each country:currency pair it runs the search and prints how many items
came back, the median and lowest price and the median discount, then writes
every row to market_compare.csv with the market it came from.
"""

import argparse
import statistics

from quanticdata_aliexpress_scraper import AliExpressScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keyword")
    parser.add_argument("--markets", nargs="+", default=["us:USD", "it:EUR"], help="country:currency pairs")
    parser.add_argument("--top", type=int, default=30, help="results per market (max 250)")
    parser.add_argument("--out", default="market_compare.csv")
    args = parser.parse_args()

    aliexpress = AliExpressScraper()
    rows = []
    for market in args.markets:
        country, _, currency = market.partition(":")
        run = aliexpress.search(args.keyword, country=country, currency=currency or None, max_results=args.top)
        prices = [r["price_value"] for r in run if r.get("price_value") is not None]
        discounts = [r["discount_percent"] for r in run if r.get("discount_percent") is not None]
        if prices:
            print(f"{country} ({currency or 'site default'}): {len(run)} items, median {statistics.median(prices):.2f}, "
                  f"lowest {min(prices):.2f}, median discount {statistics.median(discounts) if discounts else 0:.0f}%")
        else:
            print(f"{country}: {len(run)} items, no prices")
        rows.extend({"market": country, **r} for r in run)

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
