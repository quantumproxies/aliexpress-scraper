"""Minimal AliExpress search API call — one typed row per item.

Docs & schema: https://quanticdata.io/collectors/aliexpress-scraper-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/aliexpress_search/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "query": "running shoes",
        "country": "us",
        "currency": "USD",
        "max_results": 60
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("page"), row.get("product_id"), row.get("title"))
print(f"{len(data['results'])} items, cost ${data['cost']}")
