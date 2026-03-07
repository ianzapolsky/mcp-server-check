"""Employee tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_get,
    check_api_list,
    check_api_patch,
    check_api_post,
)


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
        cursor: Pagination cursor from a previous response.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if ids:
        params["ids"] = ",".join(ids)
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/employees", params=params or None)


async def get_employee(ctx: Ctx, employee_id: str) -> dict:
    """Get details for a specific employee.

    Args:
        employee_id: The Check employee ID (e.g. "emp_xxxxx").
    """
    return await check_api_get(ctx, f"/employees/{employee_id}")


async def create_employee(
    ctx: Ctx, company: str, first_name: str, last_name: str, data: dict | None = None
) -> dict:
    """Create a new employee.

    Args:
        company: The Check company ID the employee belongs to.
        first_name: Employee's first name.
        last_name: Employee's last name.
        data: Additional employee fields (dob, start_date, residence, etc.).
    """
    body: dict = {"company": company, "first_name": first_name, "last_name": last_name}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/employees", data=body)


async def update_employee(ctx: Ctx, employee_id: str, data: dict) -> dict:
    """Update an existing employee.

    Args:
        employee_id: The Check employee ID.
        data: Fields to update.
    """
    return await check_api_patch(ctx, f"/employees/{employee_id}", data=data)


async def onboard_employee(ctx: Ctx, employee_id: str) -> dict:
    """Onboard an employee, transitioning them to active status.

    Args:
        employee_id: The Check employee ID.
    """
    return await check_api_post(ctx, f"/employees/{employee_id}/onboard")


# --- Paystubs ---


async def list_employee_paystubs(
    ctx: Ctx,
    employee_id: str,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List paystubs for an employee.

    Args:
        employee_id: The Check employee ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/employees/{employee_id}/paystubs", params=params or None
    )


async def get_employee_paystub(ctx: Ctx, employee_id: str, payroll_id: str) -> dict:
    """Get a specific paystub for an employee.

    Args:
        employee_id: The Check employee ID.
        payroll_id: The Check payroll ID.
    """
    return await check_api_get(ctx, f"/employees/{employee_id}/paystubs/{payroll_id}")


# --- Forms ---


async def list_employee_forms(
    ctx: Ctx,
    employee_id: str,
    limit: int | None = None,
    cursor: str | None = None,
) -> dict:
    """List forms for an employee.

    Args:
        employee_id: The Check employee ID.
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(
        ctx, f"/employees/{employee_id}/forms", params=params or None
    )


async def get_employee_form(ctx: Ctx, employee_id: str, form_id: str) -> dict:
    """Get a specific form for an employee.

    Args:
        employee_id: The Check employee ID.
        form_id: The form ID.
    """
    return await check_api_get(ctx, f"/employees/{employee_id}/forms/{form_id}")


async def submit_employee_form(
    ctx: Ctx, employee_id: str, form_id: str, data: dict | None = None
) -> dict:
    """Submit an employee form.

    Args:
        employee_id: The Check employee ID.
        form_id: The form ID.
        data: Form submission data.
    """
    return await check_api_post(
        ctx, f"/employees/{employee_id}/forms/{form_id}/submit", data=data
    )


async def sign_and_submit_employee_form(
    ctx: Ctx, employee_id: str, form_id: str, data: dict | None = None
) -> dict:
    """Sign and submit an employee form.

    Args:
        employee_id: The Check employee ID.
        form_id: The form ID.
        data: Form submission data including signature.
    """
    return await check_api_post(
        ctx, f"/employees/{employee_id}/forms/{form_id}/sign_and_submit", data=data
    )


# --- Company Defined Attributes ---


async def get_employee_company_defined_attributes(ctx: Ctx, employee_id: str) -> dict:
    """Get company-defined attributes for an employee.

    Args:
        employee_id: The Check employee ID.
    """
    return await check_api_get(
        ctx, f"/employees/{employee_id}/company_defined_attributes"
    )


async def update_employee_company_defined_attributes(
    ctx: Ctx, employee_id: str, data: dict
) -> dict:
    """Update company-defined attributes for an employee.

    Args:
        employee_id: The Check employee ID.
        data: Attributes to update.
    """
    return await check_api_patch(
        ctx, f"/employees/{employee_id}/company_defined_attributes", data=data
    )


# --- Reciprocity Elections ---


async def get_employee_reciprocity_elections(ctx: Ctx, employee_id: str) -> dict:
    """Get reciprocity elections for an employee.

    Args:
        employee_id: The Check employee ID.
    """
    return await check_api_get(ctx, f"/employees/{employee_id}/reciprocity_elections")


async def update_employee_reciprocity_elections(
    ctx: Ctx, employee_id: str, data: dict
) -> dict:
    """Update reciprocity elections for an employee.

    Args:
        employee_id: The Check employee ID.
        data: Reciprocity election data.
    """
    return await check_api_patch(
        ctx, f"/employees/{employee_id}/reciprocity_elections", data=data
    )


# --- Other ---


async def reveal_employee_ssn(ctx: Ctx, employee_id: str) -> dict:
    """Reveal the SSN for an employee.

    Args:
        employee_id: The Check employee ID.
    """
    return await check_api_get(ctx, f"/employees/{employee_id}/reveal")


async def authorize_employee_partner(
    ctx: Ctx, employee_id: str, data: dict | None = None
) -> dict:
    """Authorize a partner for an employee.

    Args:
        employee_id: The Check employee ID.
        data: Partner authorization details.
    """
    return await check_api_post(
        ctx, f"/employees/{employee_id}/authorize_partner", data=data
    )


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_employees)
    mcp.add_tool(get_employee)
    mcp.add_tool(create_employee)
    mcp.add_tool(update_employee)
    mcp.add_tool(onboard_employee)
    mcp.add_tool(list_employee_paystubs)
    mcp.add_tool(get_employee_paystub)
    mcp.add_tool(list_employee_forms)
    mcp.add_tool(get_employee_form)
    mcp.add_tool(submit_employee_form)
    mcp.add_tool(sign_and_submit_employee_form)
    mcp.add_tool(get_employee_company_defined_attributes)
    mcp.add_tool(update_employee_company_defined_attributes)
    mcp.add_tool(get_employee_reciprocity_elections)
    mcp.add_tool(update_employee_reciprocity_elections)
    mcp.add_tool(reveal_employee_ssn)
    mcp.add_tool(authorize_employee_partner)
