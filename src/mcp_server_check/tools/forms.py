"""Form tools for the Check API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_check.helpers import (
    Ctx,
    check_api_get,
    check_api_list,
    check_api_post,
)


async def list_forms(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List forms across all companies.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/forms", params=params or None)


async def get_form(ctx: Ctx, form_id: str) -> dict:
    """Get details for a specific form.

    Args:
        form_id: The Check form ID.
    """
    return await check_api_get(ctx, f"/forms/{form_id}")


async def render_form(ctx: Ctx, form_id: str) -> dict:
    """Render a form for display.

    Args:
        form_id: The Check form ID.
    """
    return await check_api_get(ctx, f"/forms/{form_id}/render")


async def validate_form(ctx: Ctx, form_id: str, data: dict) -> dict:
    """Validate form data before submission.

    Args:
        form_id: The Check form ID.
        data: Form data to validate.
    """
    return await check_api_post(ctx, f"/forms/{form_id}/validate", data=data)


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_forms)
    mcp.add_tool(get_form)
    mcp.add_tool(render_form)
    mcp.add_tool(validate_form)
