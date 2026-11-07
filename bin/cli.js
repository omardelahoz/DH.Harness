#!/usr/bin/env node
/**
 * DH Engineering Harness for Google Antigravity
 * Node.js CLI distribution launcher & bootstrap orchestrator.
 */

const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const VERSION = '1.0.0';

function findPython() {
  const isWin = process.platform === 'win32';
  const venvPython = isWin
    ? path.join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe')
    : path.join(PROJECT_ROOT, '.venv', 'bin', 'python');

  if (fs.existsSync(venvPython)) {
    return venvPython;
  }

  const candidates = isWin ? ['python', 'py', 'python3'] : ['python3', 'python'];
  for (const cmd of candidates) {
    try {
      const res = spawnSync(cmd, ['--version'], { stdio: 'ignore' });
      if (res.status === 0) {
        return cmd;
      }
    } catch (_) {}
  }

  console.error('\x1b[31m[ERROR]\x1b[0m Python 3.10+ is required but not found in PATH or .venv.');
  process.exit(1);
}

function printHelp() {
  console.log(`
\x1b[1m\x1b[36mDH Engineering Harness for Google Antigravity\x1b[0m (v${VERSION})
Agentic Software Engineering, Deterministic TDD & Workflow Governance

\x1b[1mUSAGE:\x1b[0m
  npx dh-harness <command> [options]
  dh-harness <command> [options]

\x1b[1mCORE COMMANDS:\x1b[0m
  \x1b[32mhealth\x1b[0m                  Holistic 6-pillar project health diagnostic (100% GA score)
  \x1b[32mstatus\x1b[0m                  Show project status, active tasks, and memory dashboard
  \x1b[32mcontinue, next\x1b[0m          Diagnose continuity and recommend next task (¿Con qué continuamos?)
  \x1b[32minit\x1b[0m                    Bootstrap project workspace (.project/, .agents/, and verification db)
  \x1b[32mclassify <prompt>\x1b[0m       Classify interaction mode (Conversational, BugFix, Dev, etc.)
  \x1b[32mcheck\x1b[0m                   Run quality gates, verification tests, and audits

\x1b[1mENGINEERING SUITES:\x1b[0m
  \x1b[32mskills <list|show|match>\x1b[0m   Built-in engineering skills catalog and dynamic matching
  \x1b[32magents <list|show>\x1b[0m         Specialized agents catalog, contracts, and role boundaries
  \x1b[32mtdd <audit-tests>\x1b[0m          Deterministic TDD engine and AST false test detector
  \x1b[32mtask <start|step|run|status>\x1b[0m Step-by-step task execution and verification engine
  \x1b[32mgit <check-dod|validate-commit>\x1b[0m Git governance, conventional commits, and DoD audit
  \x1b[32msec <scan|licenses>\x1b[0m        AST secret scanner and SPDX permissive license whitelist
  \x1b[32mquality <audit>\x1b[0m            Quality engine, gates, and independent review enforcement
  \x1b[32mdocs <adr list|adr new>\x1b[0m    Architecture Decision Records (ADRs) automation
  \x1b[32march <audit>\x1b[0m               Clean Architecture layer boundaries static auditor
  \x1b[32mrelease <manifest>\x1b[0m         Build and inspect formal release manifest

\x1b[1mOPTIONS:\x1b[0m
  --help, -h             Show this help message
  --version, -v          Show version information
`);
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    printHelp();
    process.exit(0);
  }

  if (args.includes('--version') || args.includes('-v')) {
    console.log(`dh-harness v${VERSION}`);
    process.exit(0);
  }

  const pythonBin = findPython();
  const firstArg = args[0];

  let pyArgs = [];
  if (firstArg === 'engine' || firstArg === 'task') {
    const harnessPy = path.join(PROJECT_ROOT, '.engine', 'harness.py');
    pyArgs = [harnessPy, ...args.slice(1)];
  } else {
    // Forward to Python CLI package module
    pyArgs = ['-m', 'dh_harness.cli.main', ...args];
  }

  const proc = spawn(pythonBin, pyArgs, {
    cwd: PROJECT_ROOT,
    stdio: 'inherit',
    env: {
      ...process.env,
      PYTHONPATH: path.join(PROJECT_ROOT, 'src') + (process.env.PYTHONPATH ? path.delimiter + process.env.PYTHONPATH : '')
    }
  });

  proc.on('close', (code) => {
    process.exit(code || 0);
  });
}

main();
