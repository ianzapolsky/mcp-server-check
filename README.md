# mcp-server-check

An [MCP](https://modelcontextprotocol.io/) server that wraps the [Check Payroll API](https://docs.checkhq.com/), enabling Claude and other MCP clients to read companies, employees, workplaces, and payrolls.

## Quickstart

```bash
# Install and run with uvx (no clone needed)
CHECK_API_KEY=your-key uvx mcp-server-check
```

Or install from source:

```bash
git clone https://github.com/ianzapolsky/mcp-server-check.git
cd mcp-server-check
uv sync
CHECK_API_KEY=your-key uv run mcp-server-check
```

## Configuration

| Environment Variable | Required | Default | Description |
|---|---|---|---|
| `CHECK_API_KEY` | Yes | — | Your Check API key (Bearer token) |
| `CHECK_API_BASE_URL` | No | `https://sandbox.checkhq.com` | API base URL. Use `https://api.checkhq.com` for production. |

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "check": {
      "command": "uvx",
      "args": ["mcp-server-check"],
      "env": {
        "CHECK_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Usage with Claude Code

```bash
claude mcp add check -- uvx mcp-server-check
```

Then set the `CHECK_API_KEY` environment variable in your shell before running Claude Code.

## Available Tools

| Tool | Description |
|---|---|
| `list_companies` | List companies with optional filters (active status, IDs) |
| `get_company` | Get details for a specific company |
| `list_employees` | List employees with optional filters (IDs) |
| `get_employee` | Get details for a specific employee |
| `list_workplaces` | List workplaces |
| `get_workplace` | Get details for a specific workplace |
| `list_payrolls` | List payrolls with optional filters (IDs) |
| `get_payroll` | Get details for a specific payroll |

All list tools support `limit` and `cursor` parameters for pagination.

## Development

```bash
git clone https://github.com/ianzapolsky/mcp-server-check.git
cd mcp-server-check
uv sync --group dev
uv run pytest
```
