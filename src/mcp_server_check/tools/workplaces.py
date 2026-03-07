"""Workplace tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_get,
    check_api_list,
    check_api_patch,
    check_api_post,
)


async def list_workplaces(
    ctx: Ctx,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List workplaces across all companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/workplaces", params=params or None)


async def get_workplace(ctx: Ctx, workplace_id: str) -> dict:
    """Get details for a specific workplace.

    Args:
        workplace_id: The Check workplace ID (e.g. "wrk_xxxxx").
    """
    return await check_api_get(ctx, f"/workplaces/{workplace_id}")


async def create_workplace(
    ctx: Ctx, company: str, address: dict, data: dict | None = None
) -> dict:
    """Create a new workplace.

    Args:
        company: The Check company ID.
        address: Workplace address object with line1, city, state, zip, country.
        data: Additional workplace fields (name, etc.).
    """
    body: dict = {"company": company, "address": address}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/workplaces", data=body)


async def update_workplace(ctx: Ctx, workplace_id: str, data: dict) -> dict:
    """Update an existing workplace.

    Args:
        workplace_id: The Check workplace ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/workplaces/{workplace_id}", data=data)


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_workplaces)
    mcp.add_tool(get_workplace)
    mcp.add_tool(create_workplace)
    mcp.add_tool(update_workplace)
