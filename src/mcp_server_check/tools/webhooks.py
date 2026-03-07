"""Webhook tools for the Check API."""

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


async def list_webhook_configs(
    ctx: Ctx, limit: int | None = None, cursor: str | None = None
) -> dict:
    """List webhook configurations.

    Args:
        limit: Maximum number of results to return.
        cursor: Pagination cursor.
    """
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if cursor:
        params["cursor"] = cursor
    return await check_api_list(ctx, "/webhook_configs", params=params or None)


async def get_webhook_config(ctx: Ctx, webhook_config_id: str) -> dict:
    """Get details for a specific webhook configuration.

    Args:
        webhook_config_id: The Check webhook config ID.
    """
    return await check_api_get(ctx, f"/webhook_configs/{webhook_config_id}")


async def create_webhook_config(ctx: Ctx, url: str, data: dict | None = None) -> dict:
    """Create a new webhook configuration.

    Args:
        url: The webhook endpoint URL.
        data: Additional fields (events, secret, etc.).
    """
    body: dict = {"url": url}
    if data:
        body.update(data)
    return await check_api_post(ctx, "/webhook_configs", data=body)


async def update_webhook_config(
    ctx: Ctx, webhook_config_id: str, data: dict
) -> dict:
    """Update a webhook configuration.

    Args:
        webhook_config_id: The Check webhook config ID.
        data: Fields to update.
    """
    return await check_api_patch(
        ctx, f"/webhook_configs/{webhook_config_id}", data=data
    )


async def delete_webhook_config(ctx: Ctx, webhook_config_id: str) -> dict:
    """Delete a webhook configuration.

    Args:
        webhook_config_id: The Check webhook config ID.
    """
    return await check_api_delete(ctx, f"/webhook_configs/{webhook_config_id}")


async def ping_webhook_config(ctx: Ctx, webhook_config_id: str) -> dict:
    """Send a test ping to a webhook configuration.

    Args:
        webhook_config_id: The Check webhook config ID.
    """
    return await check_api_post(ctx, f"/webhook_configs/{webhook_config_id}/ping")


async def retry_webhook_events(ctx: Ctx, data: dict) -> dict:
    """Retry failed webhook events.

    Args:
        data: Retry configuration (event IDs or filters).
    """
    return await check_api_post(ctx, "/webhook_events/retry", data=data)


def register(mcp: FastMCP) -> None:
    mcp.add_tool(list_webhook_configs)
    mcp.add_tool(get_webhook_config)
    mcp.add_tool(create_webhook_config)
    mcp.add_tool(update_webhook_config)
    mcp.add_tool(delete_webhook_config)
    mcp.add_tool(ping_webhook_config)
    mcp.add_tool(retry_webhook_events)
