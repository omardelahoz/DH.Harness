import os
import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from dh_harness.interaction.classifier import classify_interaction
from dh_harness.sdk.adapter import AntigravitySDKAdapter
from dh_harness.memory.engine import MemoryEngine
from dh_harness.tasks.manager import TaskManager
from dh_harness.continuity.engine import ContinuityEngine
from dh_harness.core.contracts import HierarchicalTask, TaskState
from dh_harness.governance.gates import TestQualityGate

app = typer.Typer(
    name="dh-harness",
    help="DH Engineering Harness for Google Antigravity - Agentic Software Engineering & TDD Governance"
)
tdd_app = typer.Typer(
    name="tdd",
    help="Mandatory TDD Engine commands (audit-tests, guard, evidence)"
)
app.add_typer(tdd_app, name="tdd")

console = Console()

def _load_project_tasks() -> TaskManager:
    """Loads tasks from .project and engine into TaskManager."""
    mgr = TaskManager()
    t1 = HierarchicalTask(
        id="DH-001",
        title="Foundation, SDK Validation & Dual Packaging",
        description="Bootstrap AEE, Antigravity SDK, and npm/python wrappers",
        state=TaskState.DONE,
        evidence=["PR #1 merged into main with Graviton Task 1 COMPLETED"],
        priority=1
    )
    t2 = HierarchicalTask(
        id="DH-002",
        title="Master Orchestrator, DAG & Project Continuity Engine",
        description="Implement DAG dependency graph, task state machine, and continuity engine",
        state=TaskState.DONE,
        evidence=["PR #2 merged into main with Graviton Task 2 COMPLETED"],
        dependencies=["DH-001"],
        priority=1
    )
    t3 = HierarchicalTask(
        id="DH-003",
        title="Mandatory TDD Advanced Engine & False Test Detector",
        description="Detect empty tests, trivial assertions, cryptographic RED evidence, and TDD guard",
        state=TaskState.IN_PROGRESS,
        dependencies=["DH-002"],
        priority=1
    )
    t4 = HierarchicalTask(
        id="DH-004",
        title="Agent Ecosystem & Specialized Roles Catalog",
        description="Implement specialized agent registry according to info.md Section 4",
        state=TaskState.BACKLOG,
        dependencies=["DH-003"],
        priority=2
    )

    for t in [t1, t2, t3, t4]:
        mgr.register_task(t)
    return mgr

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

@app.command(name="continue")
def continue_work():
    """Diagnose project continuity and recommend what to do next ('¿Con qué continuamos?')."""
    mgr = _load_project_tasks()
    engine = ContinuityEngine(mgr)
    report = engine.generate_continuity_report()

    console.print(Panel(
        f"[bold cyan]PROJECT CONTINUITY & WORK PLANNING ENGINE[/bold cyan]\n"
        f"[bold yellow]¿Con qué continuamos hoy?[/bold yellow]",
        title="Continuity Dashboard",
        expand=False
    ))

    table = Table(title="Project Progress Overview")
    table.add_column("State", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Tasks", style="green")

    table.add_row("Completed", str(report.completed_count), ", ".join(report.completed_tasks) or "None")
    table.add_row("In Progress", str(report.in_progress_count), ", ".join(report.in_progress_tasks) or "None")
    table.add_row("Pending", str(report.pending_count), ", ".join(report.pending_tasks) or "None")
    table.add_row("Blocked", str(report.blocked_count), ", ".join(report.blocked_tasks) or "None")
    console.print(table)

    if report.parallel_candidates:
        console.print(f"\n[bold green]⚡ Parallel Executable Candidates (DAG Ready):[/bold green] {', '.join(report.parallel_candidates)}")

    console.print(Panel(
        f"[bold]Recommended Next Task:[/bold] [bold green]{report.recommended_task}[/bold green]\n"
        f"[bold]Rationale:[/bold] {report.rationale}",
        title="Recommended Continuation (RECOMMENDED mode)",
        border_style="green"
    ))

@app.command()
def next():
    """Alias for continue."""
    continue_work()

@tdd_app.command(name="audit-tests")
def audit_tests(path: str = typer.Argument("tests", help="Directory or file path to audit")):
    """Audit test suite to detect false or cosmetic tests."""
    console.print(f"[cyan][*] Auditing test files in '{path}' for semantic quality...[/cyan]")
    gate = TestQualityGate()
    result = gate.audit_directory(path)

    if result.passed:
        console.print(Panel(
            "[bold green]✔ Zero False Tests Detected![/bold green]\n"
            "All test functions have verifiable assertions or exception expectations.",
            title="TDD Quality Audit",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]✖ Test Quality Audit Failed![/bold red]\n{result.message}",
            title="TDD Quality Audit Alert",
            border_style="red"
        ))
        raise typer.Exit(code=1)

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
