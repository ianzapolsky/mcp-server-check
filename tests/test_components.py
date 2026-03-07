"""Tests for component tools."""

from __future__ import annotations

import httpx
import pytest

from mcp_server_check.tools.components import _ALL_TOOLS


@pytest.mark.anyio
async def test_company_component_tool(mock_api, ctx):
    """Test a company component tool."""
    tool = next(t for t in _ALL_TOOLS if t.__name__ == "create_company_run_payroll_component")
    mock_api.post("/companies/com_001/components/run_payroll").mock(
        return_value=httpx.Response(200, json={"url": "https://embed.checkhq.com/..."})
    )
    result = await tool(ctx, entity_id="com_001")
    assert "url" in result


@pytest.mark.anyio
async def test_employee_component_tool(mock_api, ctx):
    """Test an employee component tool."""
    tool = next(t for t in _ALL_TOOLS if t.__name__ == "create_employee_tax_setup_component")
    mock_api.post("/employees/emp_001/components/tax_setup").mock(
        return_value=httpx.Response(200, json={"url": "https://embed.checkhq.com/..."})
    )
    result = await tool(ctx, entity_id="emp_001")
    assert "url" in result


@pytest.mark.anyio
async def test_contractor_component_tool(mock_api, ctx):
    """Test a contractor component tool."""
    tool = next(t for t in _ALL_TOOLS if t.__name__ == "create_contractor_tax_documents_component")
    mock_api.post("/contractors/ctr_001/components/tax_documents").mock(
        return_value=httpx.Response(200, json={"url": "https://embed.checkhq.com/..."})
    )
    result = await tool(ctx, entity_id="ctr_001")
    assert "url" in result


def test_component_tool_count():
    """Verify we generated the expected number of component tools."""
    assert len(_ALL_TOOLS) == 35  # 25 company + 9 employee + 1 contractor
