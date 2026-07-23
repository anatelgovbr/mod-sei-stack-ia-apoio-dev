# SpecKit Ownership

Os fluxos padrao do SpecKit neste repositorio vivem em:

- `.agents/skills/speckit/speckit-*/SKILL.md`

Os adapters por ferramenta existem apenas para expor UX e metadados especificos:

- `.opencode/command/speckit.*.md` — wrappers do OpenCode
- `.github/agents/speckit.*.agent.md` — wrappers do Copilot
- `.github/prompts/speckit.*.prompt.md` — aliases finos para os agents do Copilot
- `.claude/commands/speckit.*.md` — wrappers do Claude Code

## Regra de manutencao

1. Altere primeiro a skill padrao da fase correspondente.
2. Ajuste depois apenas os detalhes especificos de adapter:
   - `handoffs` (OpenCode e Copilot; nao aplicavel ao Claude Code, que nao tem esse conceito)
   - nomes de entrada da ferramenta
   - target de `update-agent-context.sh`
3. Nao duplique o workflow completo em commands ou agents.

## Responsabilidades dos adapters

- OpenCode: preservar `handoffs` e mapear a fase para `/speckit.*`.
- Copilot: preservar `handoffs` e mapear a fase para `speckit.*`.
- Claude Code: mapear a fase para `/speckit.*`; sem `handoffs` (a ferramenta nao suporta esse conceito).
- Skills: manter o workflow do SpecKit neutro em relacao ao runtime.
