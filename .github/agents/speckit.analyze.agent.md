---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
---

Use `.agents/skills/speckit/speckit-analyze/SKILL.md` as the standard workflow for this phase and follow it exactly.

Copilot adapter rules:
- Use the current agent invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- Preserve the `handoffs` and other agent-specific metadata declared in this file's frontmatter.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `copilot`.
- When the standard workflow references another phase, map it to the corresponding `speckit.*` agent in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
