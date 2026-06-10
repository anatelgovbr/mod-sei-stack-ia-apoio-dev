---
name: napkin
description: |
  Maintain a per-repo napkin as a continuously curated runbook (not a session
  log). Activates EVERY session. Read and curate it before work, keep only
  recurring high-value guidance, organize by priority-sorted categories, and
  cap each category at top 10 items. The standard napkin lives at
  `.agents/memory/runbook.md` (portable, any tool).
author: Codex
version: 6.1.0
date: 2026-05-05
---

# Napkin

You maintain a per-repo markdown runbook, not a chronological log. The napkin
must be continuously curated for fast reuse in future sessions.

**This skill is always active. Every session. No trigger required.**

## Session Start: Read And Curate

First thing, every session — read `.agents/memory/runbook.md` (standard, portable).
Internalize what's there and apply it silently. Don't announce that you read it.
Just apply what you know.

Every time you read it, curate it immediately:

- Re-prioritize items by importance (highest first).
- Merge duplicates and remove stale/low-signal notes.
- Keep only recurring, high-frequency guidance.
- Ensure each item contains an explicit "Do instead" action.
- Enforce category caps (top 10 per category).

If no runbook exists yet, create the file:
- `.agents/memory/runbook.md` (padrao — qualquer ferramenta)

```markdown
# Runbook Operacional

## Regras de Curadoria
- Re-priorizar a cada leitura.
- Manter apenas notas recorrentes e de alto valor.
- Maximo 10 itens por categoria.
- Cada item inclui data + acao concreta ("Do instead").

## Execucao e Validacao (Prioridade Maxima)
1. **[YYYY-MM-DD] Regra curta**
   Do instead: acao concreta e repetivel.

## Guardrails de Comportamento de Dominio
1. **[YYYY-MM-DD] Regra curta**
   Do instead: acao concreta e repetivel.

## Shell e Confiabilidade de Comandos
1. **[YYYY-MM-DD] Regra curta**
   Do instead: acao concreta e repetivel.

## Diretivas do Usuario
1. **[YYYY-MM-DD] Diretiva**
   Do instead: seguir exatamente esta preferencia.
```

Adapt categories to the repo, but keep category structure and priority ordering.
Do not use raw journal-style entries.

## Continuous Runbook Updates

Update during work whenever you learn something reusable. Always write to
`.agents/memory/runbook.md`.

What qualifies for inclusion:

- Frequent gotchas or surprising behavior in this repo/toolchain.
- User directives that affect repeated behavior.
- Non-obvious tactics that repeatedly work.

What does not qualify:

- One-off timeline notes.
- Verbose postmortems without reusable action.
- Pure mistake logs without "Do instead" guidance.

Entry format requirements:

- Include date added (`[YYYY-MM-DD]`).
- Include short rule title.
- Include explicit `Do instead:` line.
- Keep wording concise and action-oriented.

## Category And Priority Policy

- Organize notes by category.
- Keep each category sorted by importance descending.
- Re-evaluate category choice and priority whenever editing.
- Maximum 10 items per category; if over 10, remove lowest-priority entries.
- Prefer fewer high-signal items over broad coverage.

## Practical Rule

Think of napkin as a live knowledge base for future execution speed and
reliability, not a history file.

## Example Entry

```markdown
1. **[2026-02-21] `rg` fails on giant expanded path lists**
   Do instead: run `rg` on directory roots or iterate files via `while IFS= read -r`.
```
