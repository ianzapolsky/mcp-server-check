"""Contractor tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_get,
    check_api_list,
    check_api_patch,
    check_api_post,
)


async def list_contractors(
    ctx: Ctx,
    limit: int | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
) -> dict:
    """List contractors across all companies in your Check account.

    Args:
        limit: Maximum number of results to return (default 10, max 100).
        ids: Filter to specific contractor IDs.
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/contractors", params=params or None)


async def get_contractor(ctx: Ctx, contractor_id: str) -> dict:
    """Get details for a specific contractor.

    Args:
        contractor_id: The Check contractor ID (e.g. "ctr_xxxxx").
    """
    return await check_api_get(ctx, f"/contractors/{contractor_id}")


async def create_contractor(
    ctx: Ctx, company: str, data: dict | None = None
) -> dict:
    """Create a new contractor.

    Args:
        company: The Check company ID.
        data: Additional contractor fields (first_name, last_name, type, etc.).
    """
    body: dict = {"company": company}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/contractors", data=body)


async def update_contractor(ctx: Ctx, contractor_id: str, data: dict) -> dict:
    """Update an existing contractor.

    Args:
        contractor_id: The Check contractor ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/contractors/{contractor_id}", data=data)


async def onboard_contractor(ctx: Ctx, contractor_id: str) -> dict:
    """Onboard a contractor, transitioning them to active status.

    Args:
        contractor_id: The Check contractor ID.
    """
    return await check_api_post(ctx, f"/contractors/{contractor_id}/onboard")


async def list_contractor_payments_for_contractor(
    ctx: Ctx,
    contractor_id: str,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List payments for a specific contractor.

    Args:
        contractor_id: The Check contractor ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/contractors/{contractor_id}/payments", params=params or None
    )


async def get_contractor_payment_for_payroll(
    ctx: Ctx, contractor_id: str, payroll_id: str
) -> dict:
    """Get a contractor payment for a specific payroll.

    Args:
        contractor_id: The Check contractor ID.
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(
        ctx, f"/contractors/{contractor_id}/payments/{payroll_id}"
    )


async def list_contractor_forms(
    ctx: Ctx,
    contractor_id: str,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List forms for a contractor.

    Args:
        contractor_id: The Check contractor ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/contractors/{contractor_id}/forms", params=params or None
    )


async def submit_contractor_form(
    ctx: Ctx, contractor_id: str, form_id: str, data: dict | None = None
) -> dict:
    """Submit a contractor form.

    Args:
        contractor_id: The Check contractor ID.
        form_id: The form ID.
        data: Form submission data.
    """
    return await check_api_post(
        ctx, f"/contractors/{contractor_id}/forms/{form_id}/submit", data=data
    )


async def reveal_contractor_ssn(ctx: Ctx, contractor_id: str) -> dict:
    """Reveal the SSN/EIN for a contractor.

    Args:
        contractor_id: The Check contractor ID.
    """
    return await check_api_get(ctx, f"/contractors/{contractor_id}/reveal")


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_contractors)
    mcp.add_tool(get_contractor)
    mcp.add_tool(create_contractor)
    mcp.add_tool(update_contractor)
    mcp.add_tool(onboard_contractor)
    mcp.add_tool(list_contractor_payments_for_contractor)
    mcp.add_tool(get_contractor_payment_for_payroll)
    mcp.add_tool(list_contractor_forms)
    mcp.add_tool(submit_contractor_form)
    mcp.add_tool(reveal_contractor_ssn)
