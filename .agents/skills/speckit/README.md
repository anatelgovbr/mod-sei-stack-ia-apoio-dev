# SpecKit Ownership

Os fluxos padrao do SpecKit neste repositorio vivem em:

- `.agents/skills/speckit/speckit-*/SKILL.md`

Os adapters por ferramenta existem apenas para expor UX e metadados especificos:

- `.opencode/command/speckit.*.md` — wrappers do OpenCode
- `.github/agents/speckit.*.agent.md` — wrappers do Copilot
- `.github/prompts/speckit.*.prompt.md` — aliases finos para os agents do Copilot

## Regra de manutencao

1. Altere primeiro a skill padrao da fase correspondente.
2. Ajuste depois apenas os detalhes especificos de adapter:
   - `handoffs`
   - nomes de entrada da ferramenta
   - target de `update-agent-context.sh`
3. Nao duplique o workflow completo em commands ou agents.

## Responsabilidades dos adapters

- OpenCode: preservar `handoffs` e mapear a fase para `/speckit.*`.
- Copilot: preservar `handoffs` e mapear a fase para `speckit.*`.
- Skills: manter o workflow do SpecKit neutro em relacao ao runtime.
