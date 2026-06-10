---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: 
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
---

Use `.agents/skills/speckit/speckit-tasks/SKILL.md` as the standard workflow for this phase and follow it exactly.

Copilot adapter rules:
- Use the current agent invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- Preserve the `handoffs` and other agent-specific metadata declared in this file's frontmatter.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `copilot`.
- When the standard workflow references another phase, map it to the corresponding `speckit.*` agent in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
