"""Public-first data connectors.

All connectors use stdlib-only HTTP (urllib) in v0.1. Production users can swap
in requests/aiohttp adapters without changing the public interface.
"""
from .sec_edgar import fetch_sec_data
from .yahoo_finance import fetch_yahoo_data
from .google_news import fetch_news
from .earnings_calendar import fetch_earnings_calendar

__all__ = [
    "fetch_sec_data",
    "fetch_yahoo_data",
    "fetch_news",
    "fetch_earnings_calendar",
]
