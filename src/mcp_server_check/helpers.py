"""Shared helpers for the Check MCP server."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import httpx
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession


@dataclass
class CheckContext:
    client: httpx.AsyncClient
    base_url: str


Ctx = Context[ServerSession, CheckContext]


def _extract_cursor(url: str | None) -> str | None:
    """Extract the cursor parameter from a Check API pagination URL."""
    if not url:
        return None
    parsed = urlparse(url)
    cursor_values = parse_qs(parsed.query).get("cursor")
    return cursor_values[0] if cursor_values else None


def _format_list_response(data: dict) -> dict:
    """Normalize a paginated Check API response."""
    return {
        "results": data.get("results", []),
        "next_cursor": _extract_cursor(data.get("next")),
        "previous_cursor": _extract_cursor(data.get("previous")),
    }


async def _check_api_request(
    ctx: Ctx,
    method: str,
    path: str,
    params: dict | None = None,
    data: dict | None = None,
) -> dict:
    """Make a request to the Check API with shared error handling."""
    check_ctx = ctx.request_context.lifespan_context
    try:
        response = await check_ctx.client.request(
            method, path, params=params, json=data
        )
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True}
        return response.json()
    except httpx.HTTPStatusError as e:
        try:
            error_body = e.response.json()
        except Exception:
            error_body = e.response.text
        return {
            "error": True,
            "status_code": e.response.status_code,
            "detail": error_body,
        }
    except httpx.RequestError as e:
        return {"error": True, "detail": str(e)}


async def check_api_get(ctx: Ctx, path: str, params: dict | None = None) -> dict:
    """Make a GET request to the Check API."""
    return await _check_api_request(ctx, "GET", path, params=params)


async def check_api_post(ctx: Ctx, path: str, data: dict | None = None) -> dict:
    """Make a POST request to the Check API."""
    return await _check_api_request(ctx, "POST", path, data=data)


async def check_api_patch(ctx: Ctx, path: str, data: dict) -> dict:
    """Make a PATCH request to the Check API."""
    return await _check_api_request(ctx, "PATCH", path, data=data)


async def check_api_put(ctx: Ctx, path: str, data: dict) -> dict:
    """Make a PUT request to the Check API."""
    return await _check_api_request(ctx, "PUT", path, data=data)


async def check_api_delete(ctx: Ctx, path: str, params: dict | None = None) -> dict:
    """Make a DELETE request to the Check API."""
    return await _check_api_request(ctx, "DELETE", path, params=params)


async def check_api_list(ctx: Ctx, path: str, params: dict | None = None) -> dict:
    """GET a list endpoint and return a normalized paginated response."""
    data = await check_api_get(ctx, path, params=params)
    if "error" in data:
        return data
    return _format_list_response(data)
