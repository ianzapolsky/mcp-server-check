"""Company tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_get,
    check_api_list,
    check_api_patch,
    check_api_post,
    check_api_put,
)


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
        active: Filter by active status.
        ids: Filter to specific company IDs.
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if active is not None:
        params["active"] = str(active).lower()
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/companies", params=params or None)


async def get_company(ctx: Ctx, company_id: str) -> dict:
    """Get details for a specific company.

    Args:
        company_id: The Check company ID (e.g. "com_xxxxx").
    """
    return await check_api_get(ctx, f"/companies/{company_id}")


async def create_company(ctx: Ctx, legal_name: str, data: dict | None = None) -> dict:
    """Create a new company.

    Args:
        legal_name: The legal name of the company.
        data: Additional company fields (address, phone, etc.).
    """
    body = {"legal_name": legal_name}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/companies", data=body)


async def update_company(ctx: Ctx, company_id: str, data: dict) -> dict:
    """Update an existing company.

    Args:
        company_id: The Check company ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/companies/{company_id}", data=data)


async def onboard_company(ctx: Ctx, company_id: str) -> dict:
    """Onboard a company, transitioning it to active status.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_post(ctx, f"/companies/{company_id}/onboard")


async def get_company_paydays(
    ctx: Ctx,
    company_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
    pay_schedule: str | None = None,
) -> dict:
    """Get upcoming paydays for a company.

    Args:
        company_id: The Check company ID.
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        pay_schedule: Filter by pay schedule ID.
    """
    params: dict = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if pay_schedule:
        params["pay_schedule"] = pay_schedule
    return await check_api_get(
        ctx, f"/companies/{company_id}/paydays", params=params or None
    )


async def list_company_tax_deposits(
    ctx: Ctx,
    company_id: str,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List tax deposits for a company.

    Args:
        company_id: The Check company ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/companies/{company_id}/tax_deposits", params=params or None
    )


async def get_company_benefit_aggregations(
    ctx: Ctx,
    company_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """Get benefit aggregations for a company.

    Args:
        company_id: The Check company ID.
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
    """
    params: dict = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return await check_api_get(
        ctx, f"/companies/{company_id}/benefit_aggregations", params=params or None
    )


# --- Reports ---


async def get_payroll_journal_report(
    ctx: Ctx, company_id: str, start_date: str, end_date: str
) -> dict:
    """Get a payroll journal report for a company.

    Args:
        company_id: The Check company ID.
        start_date: Report start date (YYYY-MM-DD).
        end_date: Report end date (YYYY-MM-DD).
    """
    params = {"start_date": start_date, "end_date": end_date}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/payroll_journal", params=params
    )


async def get_payroll_summary_report(
    ctx: Ctx, company_id: str, start_date: str, end_date: str
) -> dict:
    """Get a payroll summary report for a company.

    Args:
        company_id: The Check company ID.
        start_date: Report start date (YYYY-MM-DD).
        end_date: Report end date (YYYY-MM-DD).
    """
    params = {"start_date": start_date, "end_date": end_date}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/payroll_summary", params=params
    )


async def get_tax_liabilities_report(
    ctx: Ctx, company_id: str, start_date: str, end_date: str
) -> dict:
    """Get a tax liabilities report for a company.

    Args:
        company_id: The Check company ID.
        start_date: Report start date (YYYY-MM-DD).
        end_date: Report end date (YYYY-MM-DD).
    """
    params = {"start_date": start_date, "end_date": end_date}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/tax_liabilities", params=params
    )


async def get_contractor_payments_report(
    ctx: Ctx, company_id: str, start_date: str, end_date: str
) -> dict:
    """Get a contractor payments report for a company.

    Args:
        company_id: The Check company ID.
        start_date: Report start date (YYYY-MM-DD).
        end_date: Report end date (YYYY-MM-DD).
    """
    params = {"start_date": start_date, "end_date": end_date}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/contractor_payments", params=params
    )


async def get_child_support_payments_report(
    ctx: Ctx, company_id: str, start_date: str, end_date: str
) -> dict:
    """Get a child support payments report for a company.

    Args:
        company_id: The Check company ID.
        start_date: Report start date (YYYY-MM-DD).
        end_date: Report end date (YYYY-MM-DD).
    """
    params = {"start_date": start_date, "end_date": end_date}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/child_support_payments", params=params
    )


async def get_w4_exemption_status_report(ctx: Ctx, company_id: str) -> dict:
    """Get a W-4 exemption status report for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/w4_exemption_status"
    )


async def get_applied_for_ids_detailed_report(ctx: Ctx, company_id: str) -> dict:
    """Get a detailed applied-for IDs report for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/applied_for_ids_detailed"
    )


async def get_w2_preview_report(ctx: Ctx, company_id: str, year: str) -> dict:
    """Get a W-2 preview report for a company.

    Args:
        company_id: The Check company ID.
        year: Tax year (e.g. "2025").
    """
    params = {"year": year}
    return await check_api_get(
        ctx, f"/companies/{company_id}/reports/w2_preview", params=params
    )


# --- Federal EIN Verifications ---


async def list_federal_ein_verifications(
    ctx: Ctx, company_id: str, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List federal EIN verifications for a company.

    Args:
        company_id: The Check company ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx,
        f"/companies/{company_id}/federal_ein_verifications",
        params=params or None,
    )


async def get_federal_ein_verification(
    ctx: Ctx, company_id: str, verification_id: str
) -> dict:
    """Get a specific federal EIN verification.

    Args:
        company_id: The Check company ID.
        verification_id: The verification ID.
    """
    return await check_api_get(
        ctx, f"/companies/{company_id}/federal_ein_verifications/{verification_id}"
    )


# --- Signatories ---


async def list_signatories(
    ctx: Ctx, company_id: str, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List signatories for a company.

    Args:
        company_id: The Check company ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/companies/{company_id}/signatories", params=params or None
    )


async def create_signatory(ctx: Ctx, company_id: str, data: dict) -> dict:
    """Create a signatory for a company.

    Args:
        company_id: The Check company ID.
        data: Signatory fields (first_name, last_name, title, etc.).
    """
    return await check_api_post(ctx, f"/companies/{company_id}/signatories", data=data)


# --- Enrollment Profile ---


async def get_enrollment_profile(ctx: Ctx, company_id: str) -> dict:
    """Get the enrollment profile for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_get(ctx, f"/companies/{company_id}/enrollment_profile")


async def create_enrollment_profile(ctx: Ctx, company_id: str, data: dict) -> dict:
    """Create the enrollment profile for a company.

    Args:
        company_id: The Check company ID.
        data: Enrollment profile fields.
    """
    return await check_api_put(
        ctx, f"/companies/{company_id}/enrollment_profile", data=data
    )


async def update_enrollment_profile(ctx: Ctx, company_id: str, data: dict) -> dict:
    """Update the enrollment profile for a company.

    Args:
        company_id: The Check company ID.
        data: Fields to update.
    """
    return await check_api_patch(
        ctx, f"/companies/{company_id}/enrollment_profile", data=data
    )


# --- Implementation ---


async def start_implementation(ctx: Ctx, company_id: str) -> dict:
    """Start implementation for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_post(ctx, f"/companies/{company_id}/start_implementation")


async def cancel_implementation(ctx: Ctx, company_id: str) -> dict:
    """Cancel implementation for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_post(ctx, f"/companies/{company_id}/cancel_implementation")


async def request_embedded_setup(ctx: Ctx, company_id: str) -> dict:
    """Request embedded setup for a company.

    Args:
        company_id: The Check company ID.
    """
    return await check_api_post(ctx, f"/companies/{company_id}/request_embedded_setup")


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_companies)
    mcp.add_tool(get_company)
    mcp.add_tool(create_company)
    mcp.add_tool(update_company)
    mcp.add_tool(onboard_company)
    mcp.add_tool(get_company_paydays)
    mcp.add_tool(list_company_tax_deposits)
    mcp.add_tool(get_company_benefit_aggregations)
    mcp.add_tool(get_payroll_journal_report)
    mcp.add_tool(get_payroll_summary_report)
    mcp.add_tool(get_tax_liabilities_report)
    mcp.add_tool(get_contractor_payments_report)
    mcp.add_tool(get_child_support_payments_report)
    mcp.add_tool(get_w4_exemption_status_report)
    mcp.add_tool(get_applied_for_ids_detailed_report)
    mcp.add_tool(get_w2_preview_report)
    mcp.add_tool(list_federal_ein_verifications)
    mcp.add_tool(get_federal_ein_verification)
    mcp.add_tool(list_signatories)
    mcp.add_tool(create_signatory)
    mcp.add_tool(get_enrollment_profile)
    mcp.add_tool(create_enrollment_profile)
    mcp.add_tool(update_enrollment_profile)
    mcp.add_tool(start_implementation)
    mcp.add_tool(cancel_implementation)
    mcp.add_tool(request_embedded_setup)
