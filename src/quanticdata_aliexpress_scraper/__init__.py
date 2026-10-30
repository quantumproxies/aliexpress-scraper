"""AliExpress Scraper API: AliExpress scraper API for Python and the command line: product search results by keyword with sale price, original price, discount, units sold, rating, delivery dates and the Choice flag, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_aliexpress_scraper import AliExpressScraper

    scraper = AliExpressScraper()   # saved login (`aliexpress-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # AliExpress product listings for a keyword
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["AliExpressScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class AliExpressScraper:
    """AliExpress Scraper API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="aliexpress-scraper/0.1.0 (+https://github.com/quantumproxies/aliexpress-scraper)", timeout=timeout)

    def search(
        self, query: str,
        *,
        currency: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """AliExpress search results for a keyword — sale price, discount, units sold, rating and delivery dates.

        Args:
            query: What to search, e.g. "running shoes".
            currency: Currency of the prices, e.g. USD or EUR.
            country: Local AliExpress site, as an ISO country code (default us).
            max_results: How many items to deliver at most (1–250). You pay only for delivered items.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 250 rows, one per item: see ``types.AliexpressSearchRow``.
        """
        payload = {
            "query": query,
            "currency": currency,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("aliexpress_search", payload, wait=wait, timeout=timeout)
