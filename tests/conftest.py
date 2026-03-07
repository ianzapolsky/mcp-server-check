"""Shared test fixtures for the Check MCP server."""

from __future__ import annotations

from dataclasses import dataclass

import httpx
import pytest
import respx
from mcp_server_check.helpers import CheckContext

BASE_URL = "https://sandbox.checkhq.com"


@dataclass
class FakeRequestContext:
    lifespan_context: CheckContext


class FakeCtx:
    """Minimal stand-in for mcp Context that provides lifespan_context."""

    def __init__(self, check_ctx: CheckContext):
        self.request_context = FakeRequestContext(lifespan_context=check_ctx)


@pytest.fixture
def mock_api():
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def ctx(mock_api):
    """Create a fake context with an httpx client routed through respx."""
    client = httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": "Bearer test-key"},
        timeout=30.0,
    )
    check_ctx = CheckContext(client=client, base_url=BASE_URL)
    return FakeCtx(check_ctx)
