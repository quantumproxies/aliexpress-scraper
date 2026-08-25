# AliExpress search API — examples

AliExpress listings — sale price, discount, orders, store and rating.

**Live page, full schema & pricing → [quanticdata.io/collectors/aliexpress-scraper-api/](https://quanticdata.io/collectors/aliexpress-scraper-api/)**

Searches AliExpress and delivers each item with product id, title, sale and original price, discount percent, star rating, orders sold, store name and link, selling points, image and item URL. Parsed from the page's own hydration payload (the item node is located by shape, not by a hard-coded path, so a layout reshuffle does not break it). TLS tier, no browser.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/aliexpress_search/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "running shoes", "country": "us", "currency": "USD", "max_results": 60}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `query` (string, required) — What to search, e.g. "running shoes".
- `currency` (string) — Price currency, e.g. USD or EUR.
- `country` (string) — ISO 3166-1 alpha-2 code — picks the local site AND the proxy exit (default us).
- `max_results` (integer) — How many items to deliver at most (1–250). You pay only for delivered items.

## Output — one row per item

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position across pages. |
| `page` | integer | Search page the row came from. |
| `product_id` | string | AliExpress product id. |
| `title` | string | Item title. |
| `price` | string | Sale price as shown. |
| `price_value` | number | Numeric sale price. |
| `currency` | string | Currency code. |
| `original_price` | string | Pre-discount price. |
| `discount_percent` | number | Discount as a percentage. |
| `rating` | number | Star rating (1–5). |
| `orders` | string | Orders sold as shown ("1,000+ sold"). |
| `store` | string | Store name. |
…and 5 more fields — full schema on the [live page](https://quanticdata.io/collectors/aliexpress-scraper-api/).

## Pricing

**$0.001 per delivered item** ($1 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 2,000 items — no card required.

## Links

- This collector: https://quanticdata.io/collectors/aliexpress-scraper-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
