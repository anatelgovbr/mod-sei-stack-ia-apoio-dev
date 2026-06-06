# Ignore File Policy

This reference is used by implementation commands when a feature introduces a
new toolchain or build output that requires ignore-file coverage.

## Rules

- Verify ignore files only when the active plan introduces or uses that tool.
- Do not create ignore files unrelated to the repository stack.
- If an ignore file exists, append only missing critical patterns.
- Respect `AGENTS.md` write scope before creating or changing any file.

## Common Patterns

- PHP: `vendor/`, `*.log`, `*.cache`, `.env*`
- Node.js: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
- Python: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
- Docker: `.git/`, `*.log*`, `.env*`, `coverage/`
- Universal: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`
