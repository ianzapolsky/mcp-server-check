"""Tests for the ``check setup`` command."""

from __future__ import annotations

import json
import os
from unittest.mock import patch

from click.testing import CliRunner

from mcp_server_check.cli import cli
from mcp_server_check.cli.setup import CHECK_SENTINEL, _render_content


def test_setup_creates_claude_md():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["setup"])
        assert result.exit_code == 0
        assert os.path.exists("CLAUDE.md")
        with open("CLAUDE.md") as f:
            content = f.read()
        assert CHECK_SENTINEL in content
        assert "# Check Payroll API" in content


def test_setup_custom_filename():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["setup", "--file", "AGENTS.md"])
        assert result.exit_code == 0
        assert os.path.exists("AGENTS.md")
        assert not os.path.exists("CLAUDE.md")
        with open("AGENTS.md") as f:
            assert CHECK_SENTINEL in f.read()


def test_setup_prompts_before_overwrite():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("CLAUDE.md", "w") as f:
            f.write("existing content")

        # Decline overwrite
        result = runner.invoke(cli, ["setup"], input="n\n")
        assert result.exit_code != 0
        with open("CLAUDE.md") as f:
            assert f.read() == "existing content"

        # Accept overwrite
        result = runner.invoke(cli, ["setup"], input="y\n")
        assert result.exit_code == 0
        with open("CLAUDE.md") as f:
            assert CHECK_SENTINEL in f.read()


def test_setup_force_overwrites():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("CLAUDE.md", "w") as f:
            f.write("existing content")

        result = runner.invoke(cli, ["setup", "--force"])
        assert result.exit_code == 0
        with open("CLAUDE.md") as f:
            assert CHECK_SENTINEL in f.read()


def test_setup_does_not_require_api_key():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["setup"], env={})
        assert result.exit_code == 0
        assert os.path.exists("CLAUDE.md")


def test_setup_visible_in_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "setup" in result.output


def test_setup_visible_with_toolset_filter():
    """setup should appear even when CHECK_TOOLSETS restricts visible groups."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"], env={"CHECK_TOOLSETS": "companies"})
    assert result.exit_code == 0
    assert "setup" in result.output


def test_setup_custom_directory(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["setup", "--directory", str(tmp_path)])
    assert result.exit_code == 0
    target = tmp_path / "CLAUDE.md"
    assert target.exists()
    assert CHECK_SENTINEL in target.read_text()


# ---------------------------------------------------------------------------
# uv run prefix when check is not on PATH
# ---------------------------------------------------------------------------


def test_uses_uv_run_prefix_when_not_on_path():
    with patch("mcp_server_check.cli.setup._check_is_on_path", return_value=False):
        content = _render_content()
    assert "uv run check companies list" in content
    assert "\ncheck companies list" not in content


def test_no_prefix_when_on_path():
    with patch("mcp_server_check.cli.setup._check_is_on_path", return_value=True):
        content = _render_content()
    assert "\ncheck companies list" in content
    assert "uv run check" not in content


# ---------------------------------------------------------------------------
# Early exit when file already has Check instructions
# ---------------------------------------------------------------------------


def test_skips_if_file_already_has_check_instructions():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("CLAUDE.md", "w") as f:
            f.write(f"# My project\n\n{CHECK_SENTINEL}\n\nSome Check content.\n")

        result = runner.invoke(cli, ["setup"])
        assert result.exit_code == 0
        assert "already has Check CLI instructions" in result.output
        # File should be unchanged
        with open("CLAUDE.md") as f:
            assert f.read().startswith("# My project")


def test_force_does_not_bypass_sentinel_check():
    """Even --force should skip if the sentinel is already present."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("CLAUDE.md", "w") as f:
            f.write(f"# Existing\n{CHECK_SENTINEL}\n")

        result = runner.invoke(cli, ["setup", "--force"])
        assert result.exit_code == 0
        assert "already has Check CLI instructions" in result.output


# ---------------------------------------------------------------------------
# Claude settings.json permission validation
# ---------------------------------------------------------------------------


def _write_settings(directory: str, filename: str, data: dict) -> None:
    claude_dir = os.path.join(directory, ".claude")
    os.makedirs(claude_dir, exist_ok=True)
    with open(os.path.join(claude_dir, filename), "w") as f:
        json.dump(data, f)


def test_warns_when_no_bash_check_permission():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["setup"])
        assert result.exit_code == 0
        assert "No Bash(check *) permission found" in result.output


def test_no_warning_when_permission_in_settings():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _write_settings(
            ".",
            "settings.json",
            {"permissions": {"allow": ["Bash(check *)"]}},
        )
        result = runner.invoke(cli, ["setup"])
        assert result.exit_code == 0
        assert "No Bash(check *)" not in result.output


def test_no_warning_when_permission_in_local_settings():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _write_settings(
            ".",
            "settings.local.json",
            {"permissions": {"allow": ["Bash(uv run check:*)"]}},
        )
        result = runner.invoke(cli, ["setup"])
        assert result.exit_code == 0
        assert "No Bash(check *)" not in result.output
