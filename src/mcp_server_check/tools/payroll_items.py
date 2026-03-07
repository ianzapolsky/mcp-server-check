"""Payroll item tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_delete,
    check_api_get,
    check_api_list,
    check_api_patch,
    check_api_post,
)


async def list_payroll_items(
    ctx: Ctx,
    limit: int | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List payroll items across all payrolls.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        ids: Filter to specific payroll item IDs.
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/payroll_items", params=params or None)


async def get_payroll_item(ctx: Ctx, payroll_item_id: str) -> dict:
    """Get details for a specific payroll item.

    Args:
        payroll_item_id: The Check payroll item ID.
    """
    return await check_api_get(ctx, f"/payroll_items/{payroll_item_id}")


async def create_payroll_item(
    ctx: Ctx, payroll: str, employee: str, data: dict | None = None
) -> dict:
    """Create a new payroll item.

    Args:
        payroll: The Check payroll ID.
        employee: The Check employee ID.
        data: Additional payroll item fields (earnings, reimbursements, etc.).
    """
    body: dict = {"payroll": payroll, "employee": employee}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/payroll_items", data=body)


async def update_payroll_item(ctx: Ctx, payroll_item_id: str, data: dict) -> dict:
    """Update an existing payroll item.

    Args:
        payroll_item_id: The Check payroll item ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/payroll_items/{payroll_item_id}", data=data)


async def bulk_update_payroll_items(ctx: Ctx, data: dict) -> dict:
    """Bulk update payroll items.

    Args:
        data: Bulk update payload with items array.
    """
    return await check_api_patch(ctx, "/payroll_items", data=data)


async def delete_payroll_item(ctx: Ctx, payroll_item_id: str) -> dict:
    """Delete a payroll item.

    Args:
        payroll_item_id: The Check payroll item ID.
    """
    return await check_api_delete(ctx, f"/payroll_items/{payroll_item_id}")


async def bulk_delete_payroll_items(
    ctx: Ctx, ids: list[str]
) -> dict:
    """Bulk delete payroll items.

    Args:
        ids: List of payroll item IDs to delete.
    """
    params = {"ids": ",".join(ids)}
    return await check_api_delete(ctx, "/payroll_items", params=params)


async def get_payroll_item_paper_check(ctx: Ctx, payroll_item_id: str) -> dict:
    """Get paper check details for a payroll item.

    Args:
        payroll_item_id: The Check payroll item ID.
    """
    return await check_api_get(ctx, f"/payroll_items/{payroll_item_id}/paper_check")


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_payroll_items)
    mcp.add_tool(get_payroll_item)
    mcp.add_tool(create_payroll_item)
    mcp.add_tool(update_payroll_item)
    mcp.add_tool(bulk_update_payroll_items)
    mcp.add_tool(delete_payroll_item)
    mcp.add_tool(bulk_delete_payroll_items)
    mcp.add_tool(get_payroll_item_paper_check)
