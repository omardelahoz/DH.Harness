import os
import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from dh_harness.interaction.classifier import classify_interaction
from dh_harness.sdk.adapter import AntigravitySDKAdapter
from dh_harness.memory.engine import MemoryEngine

app = typer.Typer(
    name="dh-harness",
    help="DH Engineering Harness for Google Antigravity - Agentic Software Engineering & TDD Governance"
)
console = Console()

@app.command()
def status():
    """Show project health, AEE tasks, and memory dashboard."""
    workspace = os.getcwd()
    memory = MemoryEngine(workspace)
    summary = memory.get_summary()

    sdk = AntigravitySDKAdapter()
    sdk_info = sdk.get_runtime_info()

    console.print(Panel(
        f"[bold cyan]DH Engineering Harness for Google Antigravity[/bold cyan]\n"
        f"Workspace: [yellow]{workspace}[/yellow]",
        title="Project Status",
        expand=False
    ))

    table = Table(title="Harness Health & Graviton AEE")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="green")

    sdk_status = "[green]Available (v0.1.23)[/green]" if sdk_info.get("available") else "[red]Not Available[/red]"
    table.add_row("Antigravity SDK", sdk_status, sdk_info.get("package", ""))
    
    aee_status = f"[green]{summary['completed']} Completed[/green], [yellow]{summary['running']} Running[/yellow], [red]{summary['blocked']} Blocked[/red]"
    table.add_row("Graviton AEE Engine", aee_status, f"Total Tasks: {summary['tasks_total']}")

    mem_status = "[green]Active (.project/)[/green]" if summary["project_memory_exists"] else "[yellow]Missing[/yellow]"
    table.add_row("Persistent Memory", mem_status, "Rules, specs, and status tracking")

    console.print(table)

@app.command()
def classify(prompt: str):
    """Classify user request into canonical interaction mode."""
    result = classify_interaction(prompt)
    console.print(f"\n[bold]Input Prompt:[/bold] {prompt}")
    console.print(f"[bold cyan]Mode:[/bold cyan] {result.mode.value}")
    console.print(f"[bold]TDD Required:[/bold] {'[green]YES[/green]' if result.tdd_required else '[blue]NO[/blue]'}")
    console.print(f"[bold]Confidence:[/bold] {result.confidence:.2f}")
    console.print(f"[bold]Rationale:[/bold] {result.rationale}")
    console.print(f"[bold]Suggested Workflow:[/bold] {result.suggested_workflow}\n")

@app.command()
def check():
    """Run automated quality gates, verification tests, and audits."""
    console.print("[cyan][*] Running Harness Quality Gates...[/cyan]")
    import subprocess
    res = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=False)
    if res.returncode == 0:
        console.print("[green][✔] All tests passed successfully.[/green]")
    else:
        console.print("[red][✖] Some tests failed.[/red]")
        raise typer.Exit(code=res.returncode)

if __name__ == "__main__":
    app()
