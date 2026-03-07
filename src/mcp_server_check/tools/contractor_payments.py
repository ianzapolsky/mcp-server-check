"""Contractor payment tools for the Check API."""

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


async def list_contractor_payments(
    ctx: Ctx,
    limit: int | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List contractor payments across all companies.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        ids: Filter to specific contractor payment IDs.
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/contractor_payments", params=params or None)


async def get_contractor_payment(ctx: Ctx, contractor_payment_id: str) -> dict:
    """Get details for a specific contractor payment.

    Args:
        contractor_payment_id: The Check contractor payment ID.
    """
    return await check_api_get(ctx, f"/contractor_payments/{contractor_payment_id}")


async def create_contractor_payment(
    ctx: Ctx, contractor: str, payroll: str, data: dict | None = None
) -> dict:
    """Create a new contractor payment.

    Args:
        contractor: The Check contractor ID.
        payroll: The Check payroll ID.
        data: Additional payment fields (amount, reimbursements, etc.).
    """
    body: dict = {"contractor": contractor, "payroll": payroll}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/contractor_payments", data=body)


async def update_contractor_payment(
    ctx: Ctx, contractor_payment_id: str, data: dict
) -> dict:
    """Update an existing contractor payment.

    Args:
        contractor_payment_id: The Check contractor payment ID.
        data: Fields to update.
    """
    return await check_api_patch(
        ctx, f"/contractor_payments/{contractor_payment_id}", data=data
    )


async def delete_contractor_payment(ctx: Ctx, contractor_payment_id: str) -> dict:
    """Delete a contractor payment.

    Args:
        contractor_payment_id: The Check contractor payment ID.
    """
    return await check_api_delete(ctx, f"/contractor_payments/{contractor_payment_id}")


async def get_contractor_payment_paper_check(
    ctx: Ctx, contractor_payment_id: str
) -> dict:
    """Get paper check details for a contractor payment.

    Args:
        contractor_payment_id: The Check contractor payment ID.
    """
    return await check_api_get(
        ctx, f"/contractor_payments/{contractor_payment_id}/paper_check"
    )


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_contractor_payments)
    mcp.add_tool(get_contractor_payment)
    mcp.add_tool(create_contractor_payment)
    mcp.add_tool(update_contractor_payment)
    mcp.add_tool(delete_contractor_payment)
    mcp.add_tool(get_contractor_payment_paper_check)
