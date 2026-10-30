"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class AliexpressSearchRow(TypedDict, total=False):
    """One row of `aliexpress-scraper search` (aliexpress_search v1.1.2)."""

    rank: int
    """1-based position across pages."""
    page: int
    """Search page the row came from."""
    product_id: str
    """AliExpress product id."""
    title: str
    """Item title."""
    price: Optional[str]
    """Sale price as shown."""
    price_value: Optional[float]
    """Numeric sale price."""
    currency: Optional[str]
    """Currency code."""
    original_price: Optional[str]
    """Pre-discount price."""
    discount_percent: Optional[float]
    """Discount as a percentage."""
    rating: Optional[float]
    """Star rating (1–5)."""
    orders: Optional[str]
    """Orders sold as shown ("1,000+ sold")."""
    store: Optional[str]
    """Store name, when the listing's search data names it (some items do not)."""
    store_url: Optional[str]
    """Store URL. The search page does not carry it, so it is null on current search results; the store is linked from the item page."""
    ships_from: Optional[str]
    """Country the item ships from, as an ISO code (CN, US…)."""
    selling_points: List[str]
    """Promo chips on the card."""
    image: Optional[str]
    """Image URL."""
    url: str
    """Item URL."""
    original_price_value: Optional[float]
    """Numeric pre-discount price."""
    orders_count: Optional[int]
    """Exact units sold when the listing reports it."""
    delivery: Optional[str]
    """Delivery or shipping line shown on the card."""
    delivery_date_min: Optional[str]
    """Earliest estimated delivery date (YYYY-MM-DD)."""
    delivery_date_max: Optional[str]
    """Latest estimated delivery date (YYYY-MM-DD)."""
    free_shipping: bool
    """True when the card advertises free shipping."""
    choice: bool
    """True for AliExpress Choice items."""
    sponsored: bool
    """True for paid placements."""
    sku_id: Optional[str]
    """SKU the displayed price belongs to."""
    category_id: Optional[str]
    """AliExpress leaf category id."""
    listed_at: Optional[str]
    """Listing date (YYYY-MM-DD)."""
    images: List[str]
    """Gallery image URLs."""
