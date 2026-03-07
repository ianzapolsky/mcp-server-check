"""Payroll tools for the Check API."""

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
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/payrolls", params=params or None)


async def get_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Get details for a specific payroll.

    Args:
        payroll_id: The Check payroll ID (e.g. "prl_xxxxx").
    """
    return await check_api_get(ctx, f"/payrolls/{payroll_id}")


async def create_payroll(
    ctx: Ctx,
    company: str,
    period_start: str,
    period_end: str,
    payday: str,
    data: dict | None = None,
) -> dict:
    """Create a new payroll.

    Args:
        company: The Check company ID.
        period_start: Pay period start date (YYYY-MM-DD).
        period_end: Pay period end date (YYYY-MM-DD).
        payday: Payday date (YYYY-MM-DD).
        data: Additional payroll fields (type, pay_schedule, etc.).
    """
    body: dict = {
        "company": company,
        "period_start": period_start,
        "period_end": period_end,
        "payday": payday,
    }
    if data:
        body.update(data)
    return await check_api_post(ctx, "/payrolls", data=body)


async def update_payroll(ctx: Ctx, payroll_id: str, data: dict) -> dict:
    """Update an existing payroll.

    Args:
        payroll_id: The Check payroll ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/payrolls/{payroll_id}", data=data)


async def delete_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Delete a payroll.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_delete(ctx, f"/payrolls/{payroll_id}")


async def preview_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Preview a payroll before approval.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(ctx, f"/payrolls/{payroll_id}/preview")


async def approve_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Approve a payroll for processing.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(ctx, f"/payrolls/{payroll_id}/approve")


async def reopen_payroll(ctx: Ctx, payroll_id: str) -> dict:
    """Reopen a previously approved payroll.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(ctx, f"/payrolls/{payroll_id}/reopen")


async def get_payroll_paper_checks(ctx: Ctx, payroll_id: str) -> dict:
    """Get paper checks for a payroll.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(ctx, f"/payrolls/{payroll_id}/paper_checks")


async def get_payroll_cash_requirement_report(ctx: Ctx, payroll_id: str) -> dict:
    """Get a cash requirement report for a payroll.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(
        ctx, f"/payrolls/{payroll_id}/reports/cash_requirement"
    )


async def get_payroll_paper_checks_report(ctx: Ctx, payroll_id: str) -> dict:
    """Get a paper checks report for a payroll.

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(
        ctx, f"/payrolls/{payroll_id}/reports/paper_checks"
    )


# --- Simulation ---


async def simulate_start_processing(ctx: Ctx, payroll_id: str) -> dict:
    """Simulate starting payroll processing (sandbox only).

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(
        ctx, f"/payrolls/{payroll_id}/simulate/start_processing"
    )


async def simulate_complete_funding(ctx: Ctx, payroll_id: str) -> dict:
    """Simulate completing payroll funding (sandbox only).

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(
        ctx, f"/payrolls/{payroll_id}/simulate/complete_funding"
    )


async def simulate_fail_funding(ctx: Ctx, payroll_id: str) -> dict:
    """Simulate failing payroll funding (sandbox only).

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(
        ctx, f"/payrolls/{payroll_id}/simulate/fail_funding"
    )


async def simulate_complete_disbursements(ctx: Ctx, payroll_id: str) -> dict:
    """Simulate completing payroll disbursements (sandbox only).

    Args:
        payroll_id: The Check payroll ID.
    """
    return await check_api_post(
        ctx, f"/payrolls/{payroll_id}/simulate/complete_disbursements"
    )


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_payrolls)
    mcp.add_tool(get_payroll)
    mcp.add_tool(create_payroll)
    mcp.add_tool(update_payroll)
    mcp.add_tool(delete_payroll)
    mcp.add_tool(preview_payroll)
    mcp.add_tool(approve_payroll)
    mcp.add_tool(reopen_payroll)
    mcp.add_tool(get_payroll_paper_checks)
    mcp.add_tool(get_payroll_cash_requirement_report)
    mcp.add_tool(get_payroll_paper_checks_report)
    mcp.add_tool(simulate_start_processing)
    mcp.add_tool(simulate_complete_funding)
    mcp.add_tool(simulate_fail_funding)
    mcp.add_tool(simulate_complete_disbursements)
