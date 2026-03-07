"""Bank account tools for the Check API."""

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


async def list_bank_accounts(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List bank accounts across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/bank_accounts", params=params or None)


async def get_bank_account(ctx: Ctx, bank_account_id: str) -> dict:
    """Get details for a specific bank account.

    Args:
        bank_account_id: The Check bank account ID.
    """
    return await check_api_get(ctx, f"/bank_accounts/{bank_account_id}")


async def create_bank_account(
    ctx: Ctx, raw_routing_number: str, raw_account_number: str, data: dict | None = None
) -> dict:
    """Create a new bank account.

    Args:
        raw_routing_number: The bank routing number.
        raw_account_number: The bank account number.
        data: Additional bank account fields (subtype, company, employee, etc.).
    """
    body: dict = {
        "raw_routing_number": raw_routing_number,
        "raw_account_number": raw_account_number,
    }
    if data:
        body.update(data)
    return await check_api_post(ctx, "/bank_accounts", data=body)


async def update_bank_account(ctx: Ctx, bank_account_id: str, data: dict) -> dict:
    """Update a bank account.

    Args:
        bank_account_id: The Check bank account ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/bank_accounts/{bank_account_id}", data=data)


async def delete_bank_account(ctx: Ctx, bank_account_id: str) -> dict:
    """Delete a bank account.

    Args:
        bank_account_id: The Check bank account ID.
    """
    return await check_api_delete(ctx, f"/bank_accounts/{bank_account_id}")


async def reveal_bank_account_number(ctx: Ctx, bank_account_id: str) -> dict:
    """Reveal the full account number for a bank account.

    Args:
        bank_account_id: The Check bank account ID.
    """
    return await check_api_get(ctx, f"/bank_accounts/{bank_account_id}/reveal")


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_bank_accounts)
    mcp.add_tool(get_bank_account)
    mcp.add_tool(create_bank_account)
    mcp.add_tool(update_bank_account)
    mcp.add_tool(delete_bank_account)
    mcp.add_tool(reveal_bank_account_number)
