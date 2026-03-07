"""Tests for tax tools."""

from __future__ import annotations

import httpx
import pytest

from mcp_server_check.tools.tax import (
    get_company_tax_params,
    get_tax_filing,
    list_company_tax_elections,
    list_employee_tax_params,
    list_tax_filings,
    update_company_tax_params,
)


@pytest.mark.anyio
async def test_get_company_tax_params(mock_api, ctx):
    mock_api.get("/companies/com_001/tax_params").mock(
        return_value=httpx.Response(200, json={"id": "com_001", "ein": "12-3456789"})
    )
    result = await get_company_tax_params(ctx, company_id="com_001")
    assert result["ein"] == "12-3456789"


@pytest.mark.anyio
async def test_update_company_tax_params(mock_api, ctx):
    mock_api.patch("/companies/com_001/tax_params").mock(
        return_value=httpx.Response(200, json={"id": "com_001"})
    )
    result = await update_company_tax_params(ctx, company_id="com_001", data={"ein": "12-3456789"})
    assert result["id"] == "com_001"


@pytest.mark.anyio
async def test_list_employee_tax_params(mock_api, ctx):
    mock_api.get("/employee_tax_params").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "etp_001"}]},
        )
    )
    result = await list_employee_tax_params(ctx)
    assert result["results"] == [{"id": "etp_001"}]


@pytest.mark.anyio
async def test_list_company_tax_elections(mock_api, ctx):
    mock_api.get("/companies/com_001/tax_elections").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "te_001"}]},
        )
    )
    result = await list_company_tax_elections(ctx, company_id="com_001")
    assert result["results"] == [{"id": "te_001"}]


@pytest.mark.anyio
async def test_list_tax_filings(mock_api, ctx):
    mock_api.get("/tax_filings").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "tf_001"}]},
        )
    )
    result = await list_tax_filings(ctx)
    assert result["results"] == [{"id": "tf_001"}]


@pytest.mark.anyio
async def test_get_tax_filing(mock_api, ctx):
    mock_api.get("/tax_filings/tf_001").mock(
        return_value=httpx.Response(200, json={"id": "tf_001"})
    )
    result = await get_tax_filing(ctx, tax_filing_id="tf_001")
    assert result["id"] == "tf_001"
