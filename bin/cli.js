#!/usr/bin/env node
/**
 * DH Engineering Harness for Google Antigravity
 * Node.js CLI distribution launcher & bootstrap orchestrator.
 */

const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const VERSION = '0.1.0';

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
Agentic Software Engineering, TDD & Workflow Governance

\x1b[1mUSAGE:\x1b[0m
  npx dh-harness <command> [options]
  dh-harness <command> [options]

\x1b[1mCORE COMMANDS:\x1b[0m
  \x1b[32mstatus\x1b[0m                  Show project health, AEE tasks, and memory dashboard
  \x1b[32minit\x1b[0m                    Initialize harness workspace and Graviton AEE engine
  \x1b[32mclassify <prompt>\x1b[0m       Classify interaction mode (Conversational, BugFix, Dev, etc.)
  \x1b[32mtdd <subcommand>\x1b[0m        TDD engine commands (red, green, verify, status)
  \x1b[32mtask <subcommand>\x1b[0m       Graviton AEE task management (start, step, run, status)
  \x1b[32mcheck\x1b[0m                   Run quality gates, verification tests, and audits

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
