"""Pull from source DB / CSV / API into raw structures."""

from typing import Any


def extract_from_csv(path: str, **kwargs: Any) -> list[dict]:
    """Extract rows from a CSV file. Stub."""
    raise NotImplementedError("Implement CSV extraction (e.g. with pandas or csv).")


def extract_from_db(uri: str, query: str, **kwargs: Any) -> list[dict]:
    """Extract rows from a database. Stub."""
    raise NotImplementedError("Implement DB extraction.")


def extract_from_api(base_url: str, endpoint: str, **kwargs: Any) -> list[dict]:
    """Extract from an API. Stub."""
    raise NotImplementedError("Implement API extraction.")
