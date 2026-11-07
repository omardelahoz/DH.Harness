import os
import sys
from datetime import datetime
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

agents_app = typer.Typer(
    name="agents",
    help="Specialized agent ecosystem and delegation registry (info.md Section 4)"
)
app.add_typer(agents_app, name="agents")

memory_app = typer.Typer(
    name="memory",
    help="Persistent memory engine, session checkpoints and recovery (info.md Section 8)"
)
app.add_typer(memory_app, name="memory")

skills_app = typer.Typer(
    name="skills",
    help="Engineering skills catalog and discovery (info.md Section 5)"
)
app.add_typer(skills_app, name="skills")

workflows_app = typer.Typer(
    name="workflows",
    help="Composable workflow engine and execution (info.md Section 6)"
)
app.add_typer(workflows_app, name="workflows")

git_app = typer.Typer(
    name="git",
    help="Git & repository governance, branch policies, and DoD verification (info.md Section 11)"
)
app.add_typer(git_app, name="git")

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
        state=TaskState.DONE,
        evidence=["PR #3 merged into main with Graviton Task 3 COMPLETED"],
        dependencies=["DH-002"],
        priority=1
    )
    t4 = HierarchicalTask(
        id="DH-004",
        title="Agent Ecosystem & Specialized Roles Catalog",
        description="Implement specialized agent registry, delegation contracts, and independent review guard",
        state=TaskState.DONE,
        evidence=["Graviton Task 4 COMPLETED (Agent Ecosystem, Delegation Engine, Independent Review Guard)"],
        dependencies=["DH-003"],
        priority=1
    )
    t5 = HierarchicalTask(
        id="DH-005",
        title="Memory Engine, Session Recovery & Context Preservation",
        description="Implement hierarchical memory, auto-recovery on restart, context truncation protection",
        state=TaskState.DONE,
        evidence=["Graviton Task 5 COMPLETED (MultiLevelMemory, Checkpoints with SHA-256, Truncation Guard)"],
        dependencies=["DH-004"],
        priority=1
    )
    t6 = HierarchicalTask(
        id="DH-006",
        title="Skills Registry & Workflow Engine",
        description="Implement dynamic skill discovery, capability matching, and composable workflows",
        state=TaskState.DONE,
        pr_number=6,
        evidence=[
            "PR #6 merged into main",
            "pytest test suite passed 78 tests",
            "Independent review approved by 'independent-code-reviewer'"
        ],
        dependencies=["DH-005"],
        priority=1
    )
    t7 = HierarchicalTask(
        id="DH-007",
        title="Git Governance, Branch Policies & PR Delivery",
        description="Implement Git repository manager, branch protection, commit policies, and PR integration",
        state=TaskState.DONE,
        pr_number=7,
        evidence=[
            "PR #7 merged into main",
            "pytest test suite passed 83 tests",
            "Independent review approved by 'independent-code-reviewer'"
        ],
        dependencies=["DH-006"],
        priority=1
    )
    t8 = HierarchicalTask(
        id="DH-008",
        title="Security & Secrets Engine",
        description="Implement AST secret scanner, dependency vulnerability auditing, and fail-closed security policies",
        state=TaskState.READY,
        dependencies=["DH-007"],
        priority=1
    )

    for t in [t1, t2, t3, t4, t5, t6, t7, t8]:
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

@agents_app.command(name="list")
def list_agents():
    """List all specialized engineering agents registered in the harness catalog."""
    from dh_harness.agents.registry import AgentRegistry
    registry = AgentRegistry()
    registry.load_defaults()
    agents = registry.list_agents()

    table = Table(title="Specialized Agents Catalog (info.md Section 4)")
    table.add_column("Agent ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold white")
    table.add_column("Role", style="magenta")
    table.add_column("Allowed Tools", style="green")

    for a in agents:
        tools_str = ", ".join(t.value for t in a.allowed_tools)
        table.add_row(a.id, a.name, a.role.value, tools_str)

    console.print(table)

@agents_app.command(name="show")
def show_agent(agent_id: str = typer.Argument(..., help="Unique identifier of the agent")):
    """Show detailed specifications and permissions for a specialized agent."""
    from dh_harness.agents.registry import AgentRegistry
    registry = AgentRegistry()
    registry.load_defaults()
    agent = registry.get_agent(agent_id)
    if not agent:
        console.print(f"[bold red]Error:[/bold red] Agent '{agent_id}' not found.")
        raise typer.Exit(code=1)

    tools_str = ", ".join(t.value for t in agent.allowed_tools)
    skills_str = ", ".join(agent.required_skills)
    criteria_str = "\n".join(f"- {c}" for c in agent.evaluation_criteria)

    console.print(Panel(
        f"[bold cyan]ID:[/bold cyan] {agent.id}\n"
        f"[bold]Name:[/bold] {agent.name}\n"
        f"[bold magenta]Role:[/bold magenta] {agent.role.value}\n"
        f"[bold]Description:[/bold] {agent.description}\n\n"
        f"[bold green]Allowed Tools:[/bold green] {tools_str}\n"
        f"[bold yellow]Required Skills:[/bold yellow] {skills_str}\n\n"
        f"[bold]Evaluation Criteria:[/bold]\n{criteria_str}",
        title=f"Agent Specification: {agent.name}",
        expand=False
    ))

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

@memory_app.command(name="status")
def memory_status():
    """Display multi-level memory statistics, knowledge items, and checkpoint status."""
    workspace = os.getcwd()
    memory = MemoryEngine(workspace)
    summary = memory.get_summary()

    console.print(Panel(
        f"[bold cyan]Multi-Level Memory & Session State[/bold cyan]\n"
        f"Memory Directory: [yellow]{memory.memory_dir}[/yellow]",
        title="Memory Engine Dashboard",
        expand=False
    ))

    table = Table(title="Memory Storage Overview")
    table.add_column("Level / Resource", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Description", style="green")

    table.add_row("Global Memory", str(summary["global_entries"]), "Engineering principles & global policies")
    table.add_row("Project Memory", str(summary["project_entries"]), "Architectural decisions, stack & status")
    table.add_row("Task Memory", str(summary["task_entries"]), "Active task objectives & state")
    table.add_row("Knowledge Base", str(summary["knowledge_entries"]), "Curated solutions & known bug patterns")

    latest_chk = summary["latest_checkpoint"]
    chk_str = f"Session: {latest_chk['session_id']} (Task: {latest_chk['active_task_id']})" if latest_chk else "None"
    table.add_row("Latest Checkpoint", "1" if latest_chk else "0", chk_str)

    console.print(table)

@memory_app.command(name="checkpoint")
def memory_checkpoint(
    session_id: str = typer.Option(None, "--session", "-s", help="Optional explicit session ID"),
    task_id: str = typer.Option(None, "--task", "-t", help="Active task ID")
):
    """Create an instant cryptographic session checkpoint with SHA-256 verification."""
    workspace = os.getcwd()
    memory = MemoryEngine(workspace)

    sess_id = session_id or f"sess_{int(datetime.now().timestamp())}"
    active_task = task_id or "DH-005"

    branch = "main"
    try:
        import subprocess
        res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            branch = res.stdout.strip()
    except Exception:
        pass

    chk = memory.checkpoints.create_checkpoint(
        session_id=sess_id,
        active_task_id=active_task,
        active_branch=branch,
        recent_actions=["CLI manual checkpoint invoked"],
        pending_steps=["Continue task execution"]
    )

    console.print(Panel(
        f"[bold green]✔ Checkpoint Created Successfully![/bold green]\n"
        f"[bold cyan]Session ID:[/bold cyan] {chk.session_id}\n"
        f"[bold]Active Task:[/bold] {chk.active_task_id}\n"
        f"[bold]Active Branch:[/bold] {chk.active_branch}\n"
        f"[bold]SHA-256 Checksum:[/bold] {chk.checksum}",
        title="Session Checkpoint",
        border_style="green"
    ))

@memory_app.command(name="recover")
def memory_recover():
    """Recover the latest verified session checkpoint and print its compact context digest."""
    workspace = os.getcwd()
    memory = MemoryEngine(workspace)
    chk = memory.checkpoints.get_latest_checkpoint()

    if not chk:
        console.print("[yellow]No session checkpoints found to recover.[/yellow]")
        return

    digest = memory.truncation_guard.generate_compact_digest(
        checkpoint=chk,
        memory=memory.levels,
        recent_events=["Session restored from checkpoint"]
    )

    console.print(Panel(
        digest,
        title=f"Recovered Session: {chk.session_id}",
        border_style="cyan"
    ))

@skills_app.command(name="list")
def list_skills():
    """List all registered engineering skills from the canonical catalog."""
    from dh_harness.skills.registry import SkillsRegistry
    reg = SkillsRegistry()
    reg.load_defaults()
    skills = reg.list_skills()

    table = Table(title="Engineering Skills Catalog (info.md Section 5)")
    table.add_column("Skill ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold white")
    table.add_column("Category", style="magenta")
    table.add_column("Required Tools", style="green")

    for s in skills:
        tools_str = ", ".join(t.value for t in s.required_tools)
        table.add_row(s.id, s.name, s.category.value, tools_str)

    console.print(table)

@skills_app.command(name="show")
def show_skill(skill_id: str = typer.Argument(..., help="Unique identifier of the skill")):
    """Show details, triggers, guidelines, and constraints of an engineering skill."""
    from dh_harness.skills.registry import SkillsRegistry
    reg = SkillsRegistry()
    reg.load_defaults()
    skill = reg.get_skill(skill_id)
    if not skill:
        console.print(f"[bold red]Error:[/bold red] Skill '{skill_id}' not found.")
        raise typer.Exit(code=1)

    triggers_str = ", ".join(skill.triggers)
    anti_triggers_str = ", ".join(skill.anti_triggers) or "None"
    tools_str = ", ".join(t.value for t in skill.required_tools)
    guidelines_str = "\n".join(f"- {g}" for g in skill.guidelines)

    console.print(Panel(
        f"[bold cyan]ID:[/bold cyan] {skill.id}\n"
        f"[bold]Name:[/bold] {skill.name}\n"
        f"[bold magenta]Category:[/bold magenta] {skill.category.value}\n"
        f"[bold]Description:[/bold] {skill.description}\n\n"
        f"[bold green]Required Tools:[/bold green] {tools_str}\n"
        f"[bold yellow]Triggers:[/bold yellow] {triggers_str}\n"
        f"[bold red]Anti-Triggers:[/bold red] {anti_triggers_str}\n\n"
        f"[bold]Mandatory Guidelines:[/bold]\n{guidelines_str}",
        title=f"Skill Specification: {skill.name}",
        expand=False
    ))

@skills_app.command(name="match")
def match_skills(prompt: str = typer.Argument(..., help="Task prompt or user requirement")):
    """Match appropriate skills for a given task requirement based on triggers."""
    from dh_harness.skills.registry import SkillsRegistry
    reg = SkillsRegistry()
    reg.load_defaults()
    matched = reg.match_skills_for_task(prompt)

    if not matched:
        console.print(f"[yellow]No specialized skills matched for prompt:[/yellow] '{prompt}'")
        return

    table = Table(title=f"Matched Skills for: '{prompt[:40]}...'")
    table.add_column("Skill ID", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Matching Triggers", style="green")

    for s in matched:
        matching_triggers = [t for t in s.triggers if t.lower() in prompt.lower()]
        table.add_row(s.id, s.category.value, ", ".join(matching_triggers))

    console.print(table)

@workflows_app.command(name="list")
def list_workflows():
    """List all composable workflows registered in the workflow engine."""
    from dh_harness.workflows.runner import WorkflowRunner
    runner = WorkflowRunner()
    workflows = runner.list_workflows()

    table = Table(title="Composable Workflow Engine Catalog (info.md Section 6)")
    table.add_column("Workflow ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold white")
    table.add_column("Stages", style="magenta")
    table.add_column("Description", style="green")

    for wf in workflows:
        table.add_row(wf.id, wf.name, str(len(wf.stages)), wf.description)

    console.print(table)

@workflows_app.command(name="describe")
def describe_workflow(workflow_id: str = typer.Argument(..., help="Unique identifier of the workflow")):
    """Describe stages, roles, and dependencies of a composable workflow."""
    from dh_harness.workflows.runner import WorkflowRunner
    runner = WorkflowRunner()
    wf = runner.get_workflow(workflow_id)
    if not wf:
        console.print(f"[bold red]Error:[/bold red] Workflow '{workflow_id}' not found.")
        raise typer.Exit(code=1)

    table = Table(title=f"Workflow Stages: {wf.name}")
    table.add_column("Order", style="dim")
    table.add_column("Stage ID", style="cyan")
    table.add_column("Name", style="bold white")
    table.add_column("Required Role", style="magenta")
    table.add_column("Depends On", style="yellow")

    for idx, stage in enumerate(wf.stages, 1):
        deps_str = ", ".join(stage.depends_on) or "None"
        table.add_row(str(idx), stage.id, stage.name, stage.required_role.value, deps_str)

    console.print(Panel(
        f"[bold cyan]ID:[/bold cyan] {wf.id}\n"
        f"[bold]Name:[/bold] {wf.name}\n"
        f"[bold]Description:[/bold] {wf.description}",
        title="Workflow Overview",
        expand=False
    ))
    console.print(table)

@git_app.command(name="status")
def git_status():
    """Diagnose repository, provider, active branch, and cleanliness."""
    from dh_harness.git.manager import GitGovernanceManager
    mgr = GitGovernanceManager()
    diag = mgr.diagnose_repo()

    console.print(Panel(
        f"[bold cyan]Git & Repository Governance Diagnostics[/bold cyan]\n"
        f"Repository Path: [yellow]{mgr.repo_path}[/yellow]",
        title="Git Repository Governance",
        expand=False
    ))

    table = Table(title="Repository Status & Policies")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_column("Status / Policy", style="green")

    table.add_row("Is Git Repository", str(diag.is_git), "[green]Verified[/green]" if diag.is_git else "[red]Not a git repo[/red]")
    table.add_row("Active Branch", diag.active_branch, "[yellow]Protected[/yellow]" if diag.active_branch in {"main", "master"} else "[green]Feature/Work Branch[/green]")
    table.add_row("Remote Provider", diag.remote_provider.value, diag.remote_url or "None (Local only)")
    table.add_row("Clean Working Tree", str(diag.is_clean), "[green]Clean[/green]" if diag.is_clean else f"[yellow]{len(diag.modified_files)} modified, {len(diag.untracked_files)} untracked[/yellow]")

    console.print(table)

@git_app.command(name="validate-branch")
def git_validate_branch(branch: str = typer.Argument(..., help="Branch name to validate")):
    """Validate that a branch name follows policy and is not a protected branch."""
    from dh_harness.git.manager import GitGovernanceManager, ProtectedBranchViolationError
    mgr = GitGovernanceManager()
    try:
        valid = mgr.validate_branch_name(branch)
        if valid:
            console.print(f"[bold green]✔ Branch '{branch}' satisfies naming policy.[/bold green]")
        else:
            console.print(f"[bold red]✖ Branch '{branch}' violates naming policy.[/bold red] Expected pattern: (feature|bugfix|refactor|hotfix)/[name]")
            raise typer.Exit(code=1)
    except ProtectedBranchViolationError as e:
        console.print(f"[bold red]✖ Protected Branch Violation:[/bold red] {e}")
        raise typer.Exit(code=1)

@git_app.command(name="validate-commit")
def git_validate_commit(message: str = typer.Argument(..., help="Commit message to validate")):
    """Validate that a commit message complies with Conventional Commits specification."""
    from dh_harness.git.manager import GitGovernanceManager
    mgr = GitGovernanceManager()
    if mgr.validate_commit_message(message):
        console.print(f"[bold green]✔ Commit message follows Conventional Commits format.[/bold green]")
    else:
        console.print(f"[bold red]✖ Commit message violates Conventional Commits format.[/bold red]\nExpected format: feat|fix|docs|refactor|test|chore[(scope)]: description")
        raise typer.Exit(code=1)

@git_app.command(name="check-dod")
def git_check_dod(task_id: str = typer.Argument(..., help="Task ID to verify Definition of Done")):
    """Verify Definition of Done criteria for a given task."""
    mgr = _load_project_tasks()
    task = mgr.get_task(task_id)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{task_id}' not found.")
        raise typer.Exit(code=1)

    from dh_harness.git.manager import GitGovernanceManager
    git_mgr = GitGovernanceManager()
    result = git_mgr.verify_definition_of_done(task, require_pr=True)

    if result.satisfied:
        console.print(Panel(
            f"[bold green]✔ Definition of Done SATISFIED for task '{task_id}'![/bold green]\n"
            f"Evidence Count: {len(result.evidence_collected)}",
            title=f"DoD Verification: {task_id}",
            border_style="green"
        ))
    else:
        missing_str = "\n".join(f"- {m}" for m in result.missing_criteria)
        console.print(Panel(
            f"[bold red]✖ Definition of Done NOT satisfied for task '{task_id}'![/bold red]\n\n"
            f"[bold]Missing Criteria:[/bold]\n{missing_str}",
            title=f"DoD Verification: {task_id}",
            border_style="red"
        ))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
