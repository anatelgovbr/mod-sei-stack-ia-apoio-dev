---
description: Create or update the feature specification from a natural language feature description.
handoffs: 
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
---

Use `.agents/skills/speckit/speckit-specify/SKILL.md` as the standard workflow for this phase and follow it exactly.

Copilot adapter rules:
- Use the current agent invocation and `$ARGUMENTS` as the phase input referenced in the standard skill.
- Preserve the `handoffs` and other agent-specific metadata declared in this file's frontmatter.
- If the standard workflow needs `.specify/scripts/bash/update-agent-context.sh`, invoke it with `copilot`.
- When the standard workflow references another phase, map it to the corresponding `speckit.*` agent in this integration.
- Do not duplicate or override the workflow here; update the standard skill first, then keep this adapter thin.
