"""Shared types for the Check MCP server."""

from __future__ import annotations

from typing_extensions import TypedDict


class Address(TypedDict, total=False):
    """A US mailing address. All keys are optional at the type level; the API
    will enforce which ones are required for each endpoint."""

    line1: str
    """Street address or PO Box."""

    line2: str
    """Apartment, suite, unit, or building."""

    city: str
    """City, district, suburb, town, or village."""

    state: str
    """2-letter state code (e.g. "CA")."""

    postal_code: str
    """5-digit ZIP / postal code (e.g. "94105"). Do NOT use 'zip'."""

    country: str
    """2-letter country code. Defaults to "US" if omitted."""
