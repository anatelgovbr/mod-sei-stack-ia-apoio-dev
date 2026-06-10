---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
---

Use `.agents/skills/speckit/speckit-implement/SKILL.md` as the standard workflow for this phase and follow it exactly.

OpenCode adapter rules:
- Use the current command invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- Preserve the `handoffs` and other command-specific metadata declared in this file's frontmatter.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `opencode`.
- When the standard workflow references another phase, map it to the corresponding `/speckit.*` command in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
