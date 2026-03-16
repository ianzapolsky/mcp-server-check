"""Workflow-level composite tools for common multi-step operations.

These tools compose multiple API calls server-side, saving the LLM
3-4 round-trips per operation.
"""

from __future__ import annotations

import asyncio

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import Ctx, check_api_get, check_api_list


async def get_company_overview(
    ctx: Ctx,
    company_id: str,
    include_employees: bool = True,
    include_payrolls: bool = True,
    include_bank_accounts: bool = True,
    employee_limit: int = 10,
    payroll_limit: int = 5,
) -> dict:
    """Get a comprehensive overview of a company in a single call.

    Returns the company details along with its employees, recent payrolls,
    and bank accounts. This replaces 4 separate API calls.

    Args:
        company_id: The Check company ID (e.g. "com_xxxxx").
        include_employees: Include the company's employees (default true).
        include_payrolls: Include recent payrolls (default true).
        include_bank_accounts: Include bank accounts (default true).
        employee_limit: Max employees to return (default 10).
        payroll_limit: Max payrolls to return (default 5).
    """
    # Always fetch the company
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["company"] = tg.create_task(
            check_api_get(ctx, f"/companies/{company_id}")
        )
        if include_employees:
            tasks["employees"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/employees",
                    params={"company": company_id, "limit": employee_limit},
                )
            )
        if include_payrolls:
            tasks["payrolls"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/payrolls",
                    params={"company": company_id, "limit": payroll_limit},
                )
            )
        if include_bank_accounts:
            tasks["bank_accounts"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/bank_accounts",
                    params={"company": company_id},
                )
            )

    result: dict = {"company": tasks["company"].result()}
    if "employees" in tasks:
        result["employees"] = tasks["employees"].result()
    if "payrolls" in tasks:
        result["payrolls"] = tasks["payrolls"].result()
    if "bank_accounts" in tasks:
        result["bank_accounts"] = tasks["bank_accounts"].result()
    return result


async def get_employee_snapshot(
    ctx: Ctx,
    employee_id: str,
    include_tax_params: bool = True,
    include_paystubs: bool = True,
    paystub_limit: int = 5,
) -> dict:
    """Get a comprehensive snapshot of an employee in a single call.

    Returns employee details along with their tax parameters and recent
    paystubs. This replaces 3 separate API calls.

    Args:
        employee_id: The Check employee ID (e.g. "emp_xxxxx").
        include_tax_params: Include employee tax parameters (default true).
        include_paystubs: Include recent paystubs (default true).
        paystub_limit: Max paystubs to return (default 5).
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["employee"] = tg.create_task(
            check_api_get(ctx, f"/employees/{employee_id}")
        )
        if include_tax_params:
            tasks["tax_params"] = tg.create_task(
                check_api_get(ctx, f"/employee_tax_params/{employee_id}")
            )
        if include_paystubs:
            tasks["paystubs"] = tg.create_task(
                check_api_list(
                    ctx,
                    f"/employees/{employee_id}/paystubs",
                    params={"limit": paystub_limit},
                )
            )

    result: dict = {"employee": tasks["employee"].result()}
    if "tax_params" in tasks:
        result["tax_params"] = tasks["tax_params"].result()
    if "paystubs" in tasks:
        result["paystubs"] = tasks["paystubs"].result()
    return result


async def diagnose_payment(
    ctx: Ctx,
    payment_id: str,
) -> dict:
    """Get a diagnostic view of a payment with its attempts and related payroll item.

    Useful for debugging failed or stuck payments. Returns the payment,
    its payment attempts, and (if linked) the originating payroll item.
    This replaces 3 separate API calls.

    Args:
        payment_id: The Check payment ID (e.g. "pmt_xxxxx").
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["payment"] = tg.create_task(check_api_get(ctx, f"/payments/{payment_id}"))
        tasks["attempts"] = tg.create_task(
            check_api_list(ctx, f"/payments/{payment_id}/payment_attempts")
        )

    payment = tasks["payment"].result()
    result: dict = {
        "payment": payment,
        "payment_attempts": tasks["attempts"].result(),
    }

    # If the payment has a payroll_item, fetch it too
    payroll_item_id = None
    if isinstance(payment, dict) and "error" not in payment:
        payroll_item_id = payment.get("payroll_item")
    if payroll_item_id:
        payroll_item = await check_api_get(ctx, f"/payroll_items/{payroll_item_id}")
        result["payroll_item"] = payroll_item

    return result


async def get_payroll_details(
    ctx: Ctx,
    payroll_id: str,
    include_items: bool = True,
    include_contractor_payments: bool = True,
    item_limit: int = 50,
) -> dict:
    """Get a complete view of a payroll with its items and contractor payments.

    Returns the payroll details along with all payroll items (employee pay stubs)
    and contractor payments in a single call. This replaces 3 separate API calls.

    Args:
        payroll_id: The Check payroll ID (e.g. "prl_xxxxx").
        include_items: Include payroll items / employee stubs (default true).
        include_contractor_payments: Include contractor payments (default true).
        item_limit: Max payroll items to return (default 50).
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["payroll"] = tg.create_task(
            check_api_get(ctx, f"/payrolls/{payroll_id}")
        )
        if include_items:
            tasks["items"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/payroll_items",
                    params={"payroll": payroll_id, "limit": item_limit},
                )
            )
        if include_contractor_payments:
            tasks["contractor_payments"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/contractor_payments",
                    params={"payroll": payroll_id},
                )
            )

    result: dict = {"payroll": tasks["payroll"].result()}
    if "items" in tasks:
        result["payroll_items"] = tasks["items"].result()
    if "contractor_payments" in tasks:
        result["contractor_payments"] = tasks["contractor_payments"].result()
    return result


async def get_contractor_snapshot(
    ctx: Ctx,
    contractor_id: str,
    include_payments: bool = True,
    include_forms: bool = True,
    payment_limit: int = 10,
) -> dict:
    """Get a comprehensive snapshot of a contractor in a single call.

    Returns contractor details along with their recent payments and forms.
    This replaces 3 separate API calls.

    Args:
        contractor_id: The Check contractor ID (e.g. "ctr_xxxxx").
        include_payments: Include recent contractor payments (default true).
        include_forms: Include contractor forms (default true).
        payment_limit: Max payments to return (default 10).
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["contractor"] = tg.create_task(
            check_api_get(ctx, f"/contractors/{contractor_id}")
        )
        if include_payments:
            tasks["payments"] = tg.create_task(
                check_api_list(
                    ctx,
                    f"/contractors/{contractor_id}/payments",
                    params={"limit": payment_limit},
                )
            )
        if include_forms:
            tasks["forms"] = tg.create_task(
                check_api_list(
                    ctx,
                    f"/contractors/{contractor_id}/forms",
                )
            )

    result: dict = {"contractor": tasks["contractor"].result()}
    if "payments" in tasks:
        result["payments"] = tasks["payments"].result()
    if "forms" in tasks:
        result["forms"] = tasks["forms"].result()
    return result


async def get_company_tax_overview(
    ctx: Ctx,
    company_id: str,
    include_elections: bool = True,
    include_filings: bool = True,
    filing_limit: int = 10,
) -> dict:
    """Get a comprehensive tax overview for a company in a single call.

    Returns company tax parameters, tax elections, and recent tax filings.
    This replaces 3 separate API calls.

    Args:
        company_id: The Check company ID (e.g. "com_xxxxx").
        include_elections: Include tax elections (default true).
        include_filings: Include recent tax filings (default true).
        filing_limit: Max tax filings to return (default 10).
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["tax_params"] = tg.create_task(
            check_api_get(ctx, f"/company_tax_params/{company_id}")
        )
        if include_elections:
            tasks["elections"] = tg.create_task(
                check_api_list(
                    ctx,
                    f"/companies/{company_id}/tax_elections",
                )
            )
        if include_filings:
            tasks["filings"] = tg.create_task(
                check_api_list(
                    ctx,
                    "/tax_filings",
                    params={"company": company_id, "limit": filing_limit},
                )
            )

    result: dict = {"tax_params": tasks["tax_params"].result()}
    if "elections" in tasks:
        result["tax_elections"] = tasks["elections"].result()
    if "filings" in tasks:
        result["tax_filings"] = tasks["filings"].result()
    return result


async def get_onboarding_status(
    ctx: Ctx,
    company_id: str,
) -> dict:
    """Check the onboarding readiness of a company.

    Returns the company details, its workplaces, employees, bank accounts,
    and any outstanding setup requirements. Useful for determining what
    steps remain before a company can run payroll. This replaces 5 separate
    API calls.

    Args:
        company_id: The Check company ID (e.g. "com_xxxxx").
    """
    tasks: dict[str, asyncio.Task] = {}
    async with asyncio.TaskGroup() as tg:
        tasks["company"] = tg.create_task(
            check_api_get(ctx, f"/companies/{company_id}")
        )
        tasks["workplaces"] = tg.create_task(
            check_api_list(
                ctx, "/workplaces", params={"company": company_id}
            )
        )
        tasks["employees"] = tg.create_task(
            check_api_list(
                ctx, "/employees", params={"company": company_id, "limit": 5}
            )
        )
        tasks["bank_accounts"] = tg.create_task(
            check_api_list(
                ctx, "/bank_accounts", params={"company": company_id}
            )
        )
        tasks["requirements"] = tg.create_task(
            check_api_list(
                ctx, "/requirements", params={"company": company_id}
            )
        )

    company = tasks["company"].result()
    workplaces = tasks["workplaces"].result()
    employees = tasks["employees"].result()
    bank_accounts = tasks["bank_accounts"].result()
    requirements = tasks["requirements"].result()

    # Build a readiness summary
    readiness: dict = {
        "has_workplaces": bool(workplaces.get("results")),
        "has_employees": bool(employees.get("results")),
        "has_bank_accounts": bool(bank_accounts.get("results")),
    }
    # Count outstanding requirements
    req_results = requirements.get("results", [])
    outstanding = [r for r in req_results if r.get("status") != "met"]
    readiness["outstanding_requirements"] = len(outstanding)
    readiness["total_requirements"] = len(req_results)
    readiness["ready"] = (
        readiness["has_workplaces"]
        and readiness["has_employees"]
        and readiness["has_bank_accounts"]
        and readiness["outstanding_requirements"] == 0
    )

    return {
        "company": company,
        "readiness": readiness,
        "workplaces": workplaces,
        "employees": employees,
        "bank_accounts": bank_accounts,
        "requirements": requirements,
    }


def register(mcp: FastMCP, *, read_only: bool = False) -> None:
    mcp.add_tool(get_company_overview)
    mcp.add_tool(get_employee_snapshot)
    mcp.add_tool(diagnose_payment)
    mcp.add_tool(get_payroll_details)
    mcp.add_tool(get_contractor_snapshot)
    mcp.add_tool(get_company_tax_overview)
    mcp.add_tool(get_onboarding_status)
