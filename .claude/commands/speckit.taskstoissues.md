---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.
disable-model-invocation: true
---

Use `.agents/skills/speckit/speckit-taskstoissues/SKILL.md` as the standard workflow for this phase and follow it exactly.

Claude Code adapter rules:
- Use the current command invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- This phase writes GitHub issues; confirm a GitHub-capable tool (e.g. `gh` CLI via Bash, or a configured GitHub MCP tool) is available before proceeding.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `claude`.
- When the standard workflow references another phase, map it to the corresponding `/speckit.*` command in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
