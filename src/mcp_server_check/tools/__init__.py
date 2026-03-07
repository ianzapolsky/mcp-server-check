"""Tool modules for the Check MCP server."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import (
    bank_accounts,
    companies,
    compensation,
    components,
    contractor_payments,
    contractors,
    documents,
    employees,
    external_payrolls,
    forms,
    payments,
    payroll_items,
    payrolls,
    platform,
    tax,
    webhooks,
    workplaces,
)

_MODULES = [
    bank_accounts,
    companies,
    compensation,
    components,
    contractor_payments,
    contractors,
    documents,
    employees,
    external_payrolls,
    forms,
    payroll_items,
    payrolls,
    payments,
    platform,
    tax,
    webhooks,
    workplaces,
]


def register_all(mcp: FastMCP) -> None:
    """Register tools from every module."""
    for mod in _MODULES:
        mod.register(mcp)
