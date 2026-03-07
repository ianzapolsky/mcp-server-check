"""MCP server for the Check Payroll API."""

from __future__ import annotations

import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import httpx
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

DEFAULT_BASE_URL = "https://sandbox.checkhq.com"


@dataclass
class CheckContext:
    client: httpx.AsyncClient
    base_url: str


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[CheckContext]:
    base_url = os.environ.get("CHECK_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    api_key = os.environ["CHECK_API_KEY"]
    async with httpx.AsyncClient(
        base_url=base_url,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30.0,
    ) as client:
        yield CheckContext(client=client, base_url=base_url)


mcp = FastMCP("Check Payroll API", lifespan=lifespan)

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


async def _check_api_get(ctx: Ctx, path: str, params: dict | None = None) -> dict:
    """Make a GET request to the Check API."""
    check_ctx = ctx.request_context.lifespan_context
    try:
        response = await check_ctx.client.get(path, params=params)
        response.raise_for_status()
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


# --- Company tools ---


@mcp.tool()
async def list_companies(
    ctx: Ctx,
    limit: int | None = None,
    active: bool | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        active: Filter by active status. True for active companies only,
            False for inactive only.
        ids: Filter to specific company IDs.
        cursor: Pagination cursor from a previous response's next_cursor
            or previous_cursor field.
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if active is not None:
        params["active"] = str(active).lower()
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    data = await _check_api_get(ctx, "/companies", params=params or None)
    if "error" in data:
        return data
    return _format_list_response(data)


@mcp.tool()
async def get_company(ctx: Ctx, company_id: str) -> dict:
    """Get details for a specific company.

    Args:
        company_id: The Check company ID (e.g. "com_xxxxx").
    """
    return await _check_api_get(ctx, f"/companies/{company_id}")


# --- Employee tools ---


@mcp.tool()
async def list_employees(
    ctx: Ctx,
    limit: int | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List employees across all companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        ids: Filter to specific employee IDs.
        cursor: Pagination cursor from a previous response's next_cursor
            or previous_cursor field.
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    data = await _check_api_get(ctx, "/employees", params=params or None)
    if "error" in data:
        return data
    return _format_list_response(data)


@mcp.tool()
async def get_employee(ctx: Ctx, employee_id: str) -> dict:
    """Get details for a specific employee.

    Args:
        employee_id: The Check employee ID (e.g. "emp_xxxxx").
    """
    return await _check_api_get(ctx, f"/employees/{employee_id}")


# --- Workplace tools ---


@mcp.tool()
async def list_workplaces(
    ctx: Ctx,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List workplaces across all companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        cursor: Pagination cursor from a previous response's next_cursor
            or previous_cursor field.
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    data = await _check_api_get(ctx, "/workplaces", params=params or None)
    if "error" in data:
        return data
    return _format_list_response(data)


@mcp.tool()
async def get_workplace(ctx: Ctx, workplace_id: str) -> dict:
    """Get details for a specific workplace.

    Args:
        workplace_id: The Check workplace ID (e.g. "wrk_xxxxx").
    """
    return await _check_api_get(ctx, f"/workplaces/{workplace_id}")


# --- Payroll tools ---


@mcp.tool()
async def list_payrolls(
    ctx: Ctx,
    limit: int | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List payrolls across all companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        ids: Filter to specific payroll IDs.
        cursor: Pagination cursor from a previous response's next_cursor
            or previous_cursor field.
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    data = await _check_api_get(ctx, "/payrolls", params=params or None)
    if "error" in data:
        return data
    return _format_list_response(data)


@mcp.tool()
async def get_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Get details for a specific payroll.

    Args:
        payroll_id: The Check payroll ID (e.g. "prl_xxxxx").
    """
    return await _check_api_get(ctx, f"/payrolls/{payroll_id}")


def main():
    if not os.environ.get("CHECK_API_KEY"):
        print("Error: CHECK_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
