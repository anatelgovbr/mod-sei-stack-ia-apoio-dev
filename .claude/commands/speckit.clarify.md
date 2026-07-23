---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
disable-model-invocation: true
---

Use `.agents/skills/speckit/speckit-clarify/SKILL.md` as the standard workflow for this phase and follow it exactly.

Claude Code adapter rules:
- Use the current command invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `claude`.
- When the standard workflow references another phase, map it to the corresponding `/speckit.*` command in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
