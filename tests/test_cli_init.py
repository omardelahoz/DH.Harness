import pytest
from typer.testing import CliRunner
from dh_harness.cli.main import app

runner = CliRunner()

def test_cli_init_bootstraps_workspace(tmp_path):
    target = tmp_path / "my_project"
    target.mkdir()

    result = runner.invoke(app, ["init", "--workspace", str(target)])
    assert result.exit_code == 0
    assert "Initialized Successfully" in result.output

    # Check .project created
    assert (target / ".project" / "STATUS.md").exists()
    assert (target / ".project" / "rules").is_dir()
    assert (target / ".project" / "specs").is_dir()

    # Check .agents created
    assert (target / ".agents" / "skills").is_dir()
    assert (target / ".agents" / "agents").is_dir()

    # Check AGENTS.md & GEMINI.md created
    assert (target / "AGENTS.md").exists()
    assert (target / "GEMINI.md").exists()

    # Check SQLite verification database initialized
    assert (target / ".engine" / "agent_engine.db").exists()
