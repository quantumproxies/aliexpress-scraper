# AliExpress Scraper API

[![ci](https://github.com/quantumproxies/aliexpress-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/aliexpress-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape AliExpress product listings from Python or the command line: search results by keyword with the sale price, original price and discount, units sold, rating, estimated delivery dates and the Choice and free-shipping flags, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/aliexpress-scraper
aliexpress-scraper login
aliexpress-scraper search "running shoes" --country us --currency USD --max-results 60 -o running_shoes.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `aliexpress-scraper search` | keyword | Sale price, discount, units sold, rating and delivery dates, 29 fields per row ([fields and price](https://quanticdata.io/collectors/aliexpress-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper)) | up to 250 |

`--country` picks the local AliExpress site (default `us`) and `--currency` the currency the prices come back in, for example `--country it --currency EUR`. Every row carries the `product_id` and item URL, the sale and pre-discount price both as shown and as numbers, units sold, and the earliest and latest estimated delivery dates.

## Sample output

A real row from `aliexpress-scraper search "running shoes" --country us --currency USD --max-results 3` (2026-10-23):

```json
{
  "url": "https://www.aliexpress.com/item/3256811986552410.html",
  "page": 1,
  "rank": 1,
  "image": "https://ae-pic-a1.aliexpress-media.com/kf/S04a09eb3cb5444c698091c1d22b99cffl.jpg",
  "price": "US $18.42",
  "store": null,
  "title": "2026 Air Cushion Running Shoes Jogging Marathon Men Sports Breathable Lightweight Women's Comfortable Nonskid Leisure Sneakers",
  "choice": true,
  "images": [
    "https://ae-pic-a1.aliexpress-media.com/kf/S04a09eb3cb5444c698091c1d22b99cffl.jpg",
    "https://ae-pic-a1.aliexpress-media.com/kf/S7e4b795e59bd48dc854d4138bea01057M.jpg"
  ],
  "orders": "1,000+ sold",
  "rating": 4.9,
  "sku_id": "12000057698230123",
  "currency": "USD",
  "delivery": null,
  "listed_at": "2026-04-25",
  "sponsored": false,
  "store_url": null,
  "product_id": "3256811986552410",
  "ships_from": null,
  "category_id": "200000970",
  "price_value": 18.42,
  "orders_count": 1429,
  "free_shipping": false,
  "original_price": "US $47.85",
  "selling_points": [
    "New shoppers save $29.43",
    "Lowest price in 90 days"
  ],
  "discount_percent": 61,
  "delivery_date_max": "2026-11-03",
  "delivery_date_min": "2026-10-29",
  "original_price_value": 47.85
}
```

## Python

```python
from quanticdata_aliexpress_scraper import AliExpressScraper

aliexpress = AliExpressScraper()  # saved login, or QUANTICDATA_API_KEY

shoes = aliexpress.search("running shoes", country="us", currency="USD", max_results=60)
for item in shoes:
    print(item["product_id"], item["price_value"], item["discount_percent"], item["orders_count"], item["title"])
shoes.to_csv("running_shoes.csv")

cases = aliexpress.search("phone case", country="it", currency="EUR", max_results=30)
for item in sorted(cases, key=lambda r: r["orders_count"] or 0, reverse=True)[:5]:
    print(item["orders"], item["price"], item["delivery_date_max"], item["url"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Product research for a store**: Search a few keywords, keep the items rated 4.5 or more with the most units sold, and get a shortlist with price, discount and delivery window. See [`examples/product_shortlist.py`](examples/product_shortlist.py).
- **Prices across AliExpress sites**: Run the same keyword on several local sites, each in its own currency, and compare the median and lowest price and the median discount. See [`examples/market_compare.py`](examples/market_compare.py).
- **Price and orders history**: Record the top results of a keyword every day with price, discount and units sold, and see which items gain orders or change price. See [`examples/price_history.py`](examples/price_history.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `aliexpress-scraper run <id> -o out.csv` collects it later.

### `aliexpress-scraper search`

AliExpress search results for a keyword — sale price, discount, units sold, rating and delivery dates.

```
aliexpress-scraper search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search, e.g. "running shoes". |
| `--currency` | string |  | Currency of the prices, e.g. USD or EUR. |
| `--country` | string |  | Local AliExpress site, as an ISO country code (default us). |
| `--max-results` | integer | `30` | How many items to deliver at most (1–250). You pay only for delivered items. |

## Output fields

<details><summary><code>aliexpress-scraper search</code>: 29 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position across pages. |
| `page` | integer | Search page the row came from. |
| `product_id` | string | AliExpress product id. |
| `title` | string | Item title. |
| `price` | string or null | Sale price as shown. |
| `price_value` | number or null | Numeric sale price. |
| `currency` | string or null | Currency code. |
| `original_price` | string or null | Pre-discount price. |
| `discount_percent` | number or null | Discount as a percentage. |
| `rating` | number or null | Star rating (1–5). |
| `orders` | string or null | Orders sold as shown ("1,000+ sold"). |
| `store` | string or null | Store name, when the listing's search data names it (some items do not). |
| `store_url` | string or null | Store URL. The search page does not carry it, so it is null on current search results; the store is linked from the item page. |
| `ships_from` | string or null | Country the item ships from, as an ISO code (CN, US…). |
| `selling_points` | string[] | Promo chips on the card. |
| `image` | string or null | Image URL. |
| `url` | string | Item URL. |
| `original_price_value` | number or null | Numeric pre-discount price. |
| `orders_count` | integer or null | Exact units sold when the listing reports it. |
| `delivery` | string or null | Delivery or shipping line shown on the card. |
| `delivery_date_min` | string or null | Earliest estimated delivery date (YYYY-MM-DD). |
| `delivery_date_max` | string or null | Latest estimated delivery date (YYYY-MM-DD). |
| `free_shipping` | boolean | True when the card advertises free shipping. |
| `choice` | boolean | True for AliExpress Choice items. |
| `sponsored` | boolean | True for paid placements. |
| `sku_id` | string or null | SKU the displayed price belongs to. |
| `category_id` | string or null | AliExpress leaf category id. |
| `listed_at` | string or null | Listing date (YYYY-MM-DD). |
| `images` | string[] | Gallery image URLs. |

</details>

## Sign-in and API keys

- `aliexpress-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `aliexpress-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `aliexpress-scraper login --api-key`.
- `aliexpress-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/aliexpress_search/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "running shoes", "country": "us", "currency": "USD", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this AliExpress scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a keyword and get rows back; the requests run on QuanticData's side.

**Can I get prices in euros or another currency?**

Yes. Pass --currency together with --country for the local site, for example --country it --currency EUR. Every row carries the currency code next to the price.

**How many items can one run return?**

Up to 250 items per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as the image gallery and the promo chips are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/price_history.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Flipkart Scraper API](https://github.com/quantumproxies/flipkart-scraper): Flipkart scraper API for Python and the command line.
- [Walmart Scraper API](https://github.com/quantumproxies/walmart-scraper): Walmart scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=aliexpress-scraper).
