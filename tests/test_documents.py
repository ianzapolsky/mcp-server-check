"""Tests for document tools."""

from __future__ import annotations

import httpx
import pytest

from mcp_server_check.tools.documents import (
    create_company_provided_document,
    get_company_tax_document,
    list_company_tax_documents,
    list_employee_tax_documents,
    list_setup_documents,
)


@pytest.mark.anyio
async def test_list_company_tax_documents(mock_api, ctx):
    mock_api.get("/company_tax_documents").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "ctd_001"}]},
        )
    )
    result = await list_company_tax_documents(ctx)
    assert result["results"] == [{"id": "ctd_001"}]


@pytest.mark.anyio
async def test_get_company_tax_document(mock_api, ctx):
    mock_api.get("/company_tax_documents/ctd_001").mock(
        return_value=httpx.Response(200, json={"id": "ctd_001"})
    )
    result = await get_company_tax_document(ctx, document_id="ctd_001")
    assert result["id"] == "ctd_001"


@pytest.mark.anyio
async def test_list_employee_tax_documents(mock_api, ctx):
    mock_api.get("/employee_tax_documents").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "etd_001"}]},
        )
    )
    result = await list_employee_tax_documents(ctx)
    assert result["results"] == [{"id": "etd_001"}]


@pytest.mark.anyio
async def test_list_setup_documents(mock_api, ctx):
    mock_api.get("/setup_documents").mock(
        return_value=httpx.Response(
            200,
            json={"next": None, "previous": None, "results": [{"id": "sd_001"}]},
        )
    )
    result = await list_setup_documents(ctx)
    assert result["results"] == [{"id": "sd_001"}]


@pytest.mark.anyio
async def test_create_company_provided_document(mock_api, ctx):
    mock_api.post("/company_provided_documents").mock(
        return_value=httpx.Response(201, json={"id": "cpd_new"})
    )
    result = await create_company_provided_document(ctx, company="com_001")
    assert result["id"] == "cpd_new"
