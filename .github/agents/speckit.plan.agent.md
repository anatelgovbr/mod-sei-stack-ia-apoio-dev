---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

Use `.agents/skills/speckit/speckit-plan/SKILL.md` as the standard workflow for this phase and follow it exactly.

Copilot adapter rules:
- Use the current agent invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- Preserve the `handoffs` and other agent-specific metadata declared in this file's frontmatter.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `copilot`.
- When the standard workflow references another phase, map it to the corresponding `speckit.*` agent in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
