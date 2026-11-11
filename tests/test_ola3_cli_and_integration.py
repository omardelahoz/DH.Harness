"""Tests for Ola 3 CLI subcommands and ecosystem integrations."""
import pytest
from typer.testing import CliRunner
from dh_harness.cli.main import app

runner = CliRunner()


def test_cli_memory_search():
    result = runner.invoke(app, ["memory", "search", "clean architecture"])
    assert result.exit_code == 0
    assert "clean_architecture" in result.output or "Semantic Search" in result.output


def test_cli_obs_metrics():
    result = runner.invoke(app, ["obs", "metrics"])
    assert result.exit_code == 0
    assert "LLM Token Usage Metrics" in result.output
    assert "gemini" in result.output
    assert "TOTAL" in result.output


def test_cli_obs_costs():
    result = runner.invoke(app, ["obs", "costs"])
    assert result.exit_code == 0
    assert "LLM Model Pricing Rates" in result.output
    assert "gemini-1.5-pro" in result.output


def test_cli_obs_traces():
    result = runner.invoke(app, ["obs", "traces"])
    assert result.exit_code == 0
    assert "OpenTelemetry Spans Export" in result.output
    assert "resourceSpans" in result.output


def test_cli_uiux_visual():
    result = runner.invoke(app, ["uiux", "visual", "tests/"])
    assert result.exit_code == 0
    assert "Visual Layout QA" in result.output


def test_cli_agents_benchmark():
    result = runner.invoke(app, ["agents", "benchmark"])
    assert result.exit_code == 0
    assert "Agent Benchmark Leaderboard" in result.output
    assert "First-Pass Acc" in result.output


def test_cli_tdd_guard_blocks_src_without_task():
    result = runner.invoke(app, ["tdd", "guard", "src/dh_harness/tdd/engine.py"])
    assert result.exit_code == 1
    assert "Modification Blocked by TDD Guard" in result.output


def test_cli_tdd_guard_permits_test_file():
    result = runner.invoke(app, ["tdd", "guard", "tests/test_feature.py"])
    assert result.exit_code == 0
    assert "Modification Permitted" in result.output


def test_cli_tdd_verify_chain():
    result = runner.invoke(app, ["tdd", "verify-chain"])
    assert result.exit_code == 0
    assert "Cryptographic Chain Intact" in result.output


def test_cli_tdd_evidence_not_found():
    result = runner.invoke(app, ["tdd", "evidence", "NON_EXISTENT_TASK_ID"])
    assert result.exit_code == 1
    assert "No active RED evidence found" in result.output
