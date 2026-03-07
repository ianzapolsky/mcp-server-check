"""Compensation tools for the Check API (pay schedules, benefits, deductions, etc.)."""

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


# --- Pay Schedules ---


async def list_pay_schedules(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List pay schedules across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/pay_schedules", params=params or None)


async def get_pay_schedule(ctx: Ctx, pay_schedule_id: str) -> dict:
    """Get details for a specific pay schedule.

    Args:
        pay_schedule_id: The Check pay schedule ID.
    """
    return await check_api_get(ctx, f"/pay_schedules/{pay_schedule_id}")


async def create_pay_schedule(
    ctx: Ctx, company: str, frequency: str, data: dict | None = None
) -> dict:
    """Create a new pay schedule.

    Args:
        company: The Check company ID.
        frequency: Pay frequency (e.g. "weekly", "biweekly", "semimonthly", "monthly").
        data: Additional pay schedule fields.
    """
    body: dict = {"company": company, "frequency": frequency}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/pay_schedules", data=body)


async def update_pay_schedule(ctx: Ctx, pay_schedule_id: str, data: dict) -> dict:
    """Update a pay schedule.

    Args:
        pay_schedule_id: The Check pay schedule ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/pay_schedules/{pay_schedule_id}", data=data)


async def delete_pay_schedule(ctx: Ctx, pay_schedule_id: str) -> dict:
    """Delete a pay schedule.

    Args:
        pay_schedule_id: The Check pay schedule ID.
    """
    return await check_api_delete(ctx, f"/pay_schedules/{pay_schedule_id}")


async def get_pay_schedule_paydays(
    ctx: Ctx,
    pay_schedule_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """Get paydays for a pay schedule.

    Args:
        pay_schedule_id: The Check pay schedule ID.
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
    """
    params: dict = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return await check_api_get(
        ctx, f"/pay_schedules/{pay_schedule_id}/paydays", params=params or None
    )


# --- Benefits ---


async def list_benefits(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List employee benefits across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/benefits", params=params or None)


async def get_benefit(ctx: Ctx, benefit_id: str) -> dict:
    """Get details for a specific benefit.

    Args:
        benefit_id: The Check benefit ID.
    """
    return await check_api_get(ctx, f"/benefits/{benefit_id}")


async def create_benefit(
    ctx: Ctx, employee: str, company_benefit: str, data: dict | None = None
) -> dict:
    """Create a new employee benefit.

    Args:
        employee: The Check employee ID.
        company_benefit: The Check company benefit ID.
        data: Additional benefit fields (amount, percentage, etc.).
    """
    body: dict = {"employee": employee, "company_benefit": company_benefit}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/benefits", data=body)


async def update_benefit(ctx: Ctx, benefit_id: str, data: dict) -> dict:
    """Update a benefit.

    Args:
        benefit_id: The Check benefit ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/benefits/{benefit_id}", data=data)


async def delete_benefit(ctx: Ctx, benefit_id: str) -> dict:
    """Delete a benefit.

    Args:
        benefit_id: The Check benefit ID.
    """
    return await check_api_delete(ctx, f"/benefits/{benefit_id}")


# --- Post-Tax Deductions ---


async def list_post_tax_deductions(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List post-tax deductions across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/post_tax_deductions", params=params or None)


async def get_post_tax_deduction(ctx: Ctx, deduction_id: str) -> dict:
    """Get details for a specific post-tax deduction.

    Args:
        deduction_id: The Check post-tax deduction ID.
    """
    return await check_api_get(ctx, f"/post_tax_deductions/{deduction_id}")


async def create_post_tax_deduction(
    ctx: Ctx, employee: str, data: dict | None = None
) -> dict:
    """Create a new post-tax deduction.

    Args:
        employee: The Check employee ID.
        data: Additional deduction fields (type, amount, description, etc.).
    """
    body: dict = {"employee": employee}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/post_tax_deductions", data=body)


async def update_post_tax_deduction(ctx: Ctx, deduction_id: str, data: dict) -> dict:
    """Update a post-tax deduction.

    Args:
        deduction_id: The Check post-tax deduction ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/post_tax_deductions/{deduction_id}", data=data)


async def delete_post_tax_deduction(ctx: Ctx, deduction_id: str) -> dict:
    """Delete a post-tax deduction.

    Args:
        deduction_id: The Check post-tax deduction ID.
    """
    return await check_api_delete(ctx, f"/post_tax_deductions/{deduction_id}")


# --- Company Benefits ---


async def list_company_benefits(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List company-level benefits across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/company_benefits", params=params or None)


async def get_company_benefit(ctx: Ctx, company_benefit_id: str) -> dict:
    """Get details for a specific company benefit.

    Args:
        company_benefit_id: The Check company benefit ID.
    """
    return await check_api_get(ctx, f"/company_benefits/{company_benefit_id}")


async def create_company_benefit(
    ctx: Ctx, company: str, data: dict | None = None
) -> dict:
    """Create a new company benefit.

    Args:
        company: The Check company ID.
        data: Additional company benefit fields (description, benefit_type, etc.).
    """
    body: dict = {"company": company}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/company_benefits", data=body)


async def update_company_benefit(
    ctx: Ctx, company_benefit_id: str, data: dict
) -> dict:
    """Update a company benefit.

    Args:
        company_benefit_id: The Check company benefit ID.
        data: Fields to update.
    """
    return await check_api_patch(
        ctx, f"/company_benefits/{company_benefit_id}", data=data
    )


async def delete_company_benefit(ctx: Ctx, company_benefit_id: str) -> dict:
    """Delete a company benefit.

    Args:
        company_benefit_id: The Check company benefit ID.
    """
    return await check_api_delete(ctx, f"/company_benefits/{company_benefit_id}")


# --- Earning Rates ---


async def list_earning_rates(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List earning rates across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/earning_rates", params=params or None)


async def get_earning_rate(ctx: Ctx, earning_rate_id: str) -> dict:
    """Get details for a specific earning rate.

    Args:
        earning_rate_id: The Check earning rate ID.
    """
    return await check_api_get(ctx, f"/earning_rates/{earning_rate_id}")


async def create_earning_rate(
    ctx: Ctx, employee: str, data: dict | None = None
) -> dict:
    """Create a new earning rate.

    Args:
        employee: The Check employee ID.
        data: Additional earning rate fields (amount, period, earning_code, etc.).
    """
    body: dict = {"employee": employee}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/earning_rates", data=body)


async def update_earning_rate(ctx: Ctx, earning_rate_id: str, data: dict) -> dict:
    """Update an earning rate.

    Args:
        earning_rate_id: The Check earning rate ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/earning_rates/{earning_rate_id}", data=data)


# --- Earning Codes ---


async def list_earning_codes(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List earning codes across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/earning_codes", params=params or None)


async def get_earning_code(ctx: Ctx, earning_code_id: str) -> dict:
    """Get details for a specific earning code.

    Args:
        earning_code_id: The Check earning code ID.
    """
    return await check_api_get(ctx, f"/earning_codes/{earning_code_id}")


async def create_earning_code(
    ctx: Ctx, company: str, data: dict | None = None
) -> dict:
    """Create a new earning code.

    Args:
        company: The Check company ID.
        data: Additional earning code fields (name, type, etc.).
    """
    body: dict = {"company": company}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/earning_codes", data=body)


async def update_earning_code(ctx: Ctx, earning_code_id: str, data: dict) -> dict:
    """Update an earning code.

    Args:
        earning_code_id: The Check earning code ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/earning_codes/{earning_code_id}", data=data)


# --- Net Pay Splits ---


async def list_net_pay_splits(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List net pay splits across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/net_pay_splits", params=params or None)


async def get_net_pay_split(ctx: Ctx, net_pay_split_id: str) -> dict:
    """Get details for a specific net pay split.

    Args:
        net_pay_split_id: The Check net pay split ID.
    """
    return await check_api_get(ctx, f"/net_pay_splits/{net_pay_split_id}")


async def create_net_pay_split(
    ctx: Ctx, employee: str, data: dict | None = None
) -> dict:
    """Create a new net pay split.

    Args:
        employee: The Check employee ID.
        data: Additional net pay split fields (bank_account, amount, percentage, etc.).
    """
    body: dict = {"employee": employee}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/net_pay_splits", data=body)


def register(mcp: FastMCP) -> None:
    # Pay Schedules
    mcp.add_tool(list_pay_schedules)
    mcp.add_tool(get_pay_schedule)
    mcp.add_tool(create_pay_schedule)
    mcp.add_tool(update_pay_schedule)
    mcp.add_tool(delete_pay_schedule)
    mcp.add_tool(get_pay_schedule_paydays)
    # Benefits
    mcp.add_tool(list_benefits)
    mcp.add_tool(get_benefit)
    mcp.add_tool(create_benefit)
    mcp.add_tool(update_benefit)
    mcp.add_tool(delete_benefit)
    # Post-Tax Deductions
    mcp.add_tool(list_post_tax_deductions)
    mcp.add_tool(get_post_tax_deduction)
    mcp.add_tool(create_post_tax_deduction)
    mcp.add_tool(update_post_tax_deduction)
    mcp.add_tool(delete_post_tax_deduction)
    # Company Benefits
    mcp.add_tool(list_company_benefits)
    mcp.add_tool(get_company_benefit)
    mcp.add_tool(create_company_benefit)
    mcp.add_tool(update_company_benefit)
    mcp.add_tool(delete_company_benefit)
    # Earning Rates
    mcp.add_tool(list_earning_rates)
    mcp.add_tool(get_earning_rate)
    mcp.add_tool(create_earning_rate)
    mcp.add_tool(update_earning_rate)
    # Earning Codes
    mcp.add_tool(list_earning_codes)
    mcp.add_tool(get_earning_code)
    mcp.add_tool(create_earning_code)
    mcp.add_tool(update_earning_code)
    # Net Pay Splits
    mcp.add_tool(list_net_pay_splits)
    mcp.add_tool(get_net_pay_split)
    mcp.add_tool(create_net_pay_split)
