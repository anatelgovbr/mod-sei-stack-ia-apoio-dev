# SpecKit Ownership

Os fluxos padrao do SpecKit neste repositorio vivem em um lugar so:

- `.agents/skills/speckit-<fase>/SKILL.md`

Sao as 9 fases: `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `checklist`, `taskstoissues` e `constitution`.

## Como as fases ficam visiveis

Ferramenta descobre skill em diretorios configurados no formato `<local>/<nome>/SKILL.md`, um nivel abaixo do diretorio configurado. As fases ficam nesse nivel, lado a lado com as demais skills do repositorio, entao as tres ferramentas as encontram sem configuracao extra e sem symlink.

| Ferramenta | Como chega em `.agents/skills/` |
|---|---|
| Claude Code | `.claude/skills`, symlink para `../.agents/skills` |
| Copilot | `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | `skills.paths` em `.opencode/opencode.json` |

Invocacao: `/speckit-plan`, `/speckit-specify`, com hifen. O nome sai do diretorio da skill, entao e o mesmo nas tres.

## Nenhuma integracao guarda arquivo do SpecKit

`.claude/commands/`, `.github/agents/`, `.github/prompts/` e `.opencode/command/` estao vazios de proposito. 
As ferramentas leem as skills direto em `.agents/skills/`.

## Scripts das fases

Os scripts que as fases executam ficam em `.specify/scripts/`, na raiz do repositorio, em duas versoes equivalentes:

| Ambiente | Pasta | Extensao |
|---|---|---|
| Linux, macOS ou WSL | `.specify/scripts/bash/` | `.sh` |
| Windows PowerShell | `.specify/scripts/powershell/` | `.ps1` |

As duas pastas tem os mesmos 6 scripts: `common`, `check-prerequisites`, `setup-plan`, `setup-tasks`, `create-new-feature` e `update-agent-context`. Cada par imprime o mesmo JSON, entao a fase funciona igual nos dois ambientes.

O `SKILL.md` declara os dois caminhos no frontmatter, em `scripts` (e em `agent_scripts`, no `speckit-plan`). A secao `Script Selection` do corpo diz ao agente qual entrada usar conforme o shell. Ao editar um script bash, edite tambem o `.ps1` correspondente.

## Regra de manutencao

1. Altere sempre `.agents/skills/speckit-<fase>/SKILL.md`. Nao existe segunda copia para sincronizar.
2. Mantenha o `SKILL.md` neutro em relacao ao runtime: nada de `/speckit-plan` nem `/speckit.plan` no corpo. Cite a fase de forma generica e deixe a ferramenta resolver o gatilho.
3. Fase nova precisa de um diretorio proprio em `.agents/skills/`, nomeado `speckit-<fase>`, com `name: speckit-<fase>` no frontmatter. O nome do diretorio e o que vira o gatilho de invocacao.
4. Nao crie arquivo de comando em `.claude/commands/`, `.github/agents/`, `.github/prompts/` ou `.opencode/command/`. Se algum dia uma ferramenta precisar disso para expor a fase, o arquivo aponta para o `SKILL.md` e nao carrega workflow.
