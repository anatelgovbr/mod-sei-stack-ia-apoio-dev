# SpecKit Ownership

Os fluxos padrao do SpecKit neste repositorio vivem em um lugar so:

- `.agents/skills/speckit-<fase>/SKILL.md`

Sao as 10 fases: `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `checklist`, `taskstoissues`, `constitution` e `converge`.

## Como as fases ficam visiveis

Ferramenta descobre skill em diretorios configurados no formato `<local>/<nome>/SKILL.md`, um nivel abaixo do diretorio configurado. As fases ficam nesse nivel, lado a lado com as demais skills do repositorio, entao as tres ferramentas as encontram sem symlink e sem copia, cada uma pelo seu proprio caminho de configuracao.

| Ferramenta | Como chega em `.agents/skills/` |
|---|---|
| Claude Code | plugin local `stack-ai`, do marketplace `stack-ai-<repositorio>`, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json` |
| Copilot | `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | `skills.paths` em `.opencode/opencode.json` |

Invocacao: `/speckit-plan`, `/speckit-specify`, com hifen. O nome sai do diretorio da skill, entao e o mesmo nas tres.

## Nenhuma integracao guarda arquivo do SpecKit

Nenhuma das tres ferramentas tem pasta de comando neste repositorio. As tres leem as skills direto em `.agents/skills/`.

## Scripts das fases

Os scripts que as fases executam ficam em `.specify/scripts/`, na raiz do repositorio, em duas versoes equivalentes:

| Ambiente | Pasta | Extensao |
|---|---|---|
| Linux, macOS ou WSL | `.specify/scripts/bash/` | `.sh` |
| Windows PowerShell | `.specify/scripts/powershell/` | `.ps1` |

As duas pastas tem os mesmos 6 scripts: `common`, `check-prerequisites`, `setup-plan`, `setup-tasks`, `create-new-feature` e `resolve-template`. Cada par imprime o mesmo JSON, entao a fase funciona igual nos dois ambientes.

O `SKILL.md` declara os dois caminhos no frontmatter, em `scripts`. A secao `Script Selection` do corpo diz ao agente qual entrada usar conforme o shell. Ao editar um script bash, edite tambem o `.ps1` correspondente.

Nenhuma fase escreve no arquivo de contexto do projeto. O `update-agent-context` do SpecKit, que reescreve `AGENTS.md`, `CLAUDE.md` ou `copilot-instructions.md` a partir do plano, nao entra na carga: esses arquivos sao do time.

## Templates dos artefatos

Os esqueletos de `spec.md`, `plan.md`, `tasks.md` e das checklists ficam em `.specify/templates/<artefato>-template.md`. O script da fase resolve o template e o copia para `specs/<feature>/` quando o arquivo ainda nao existe (`create-new-feature` para spec, `setup-plan` para plan, `setup-tasks` para tasks, `check-prerequisites --template` para checklist); a skill preenche o arquivo seguindo a estrutura do template. Esses templates carregam as secoes do SEI e sao da equipe.

Os templates de comando do SpecKit (`templates/commands/<fase>.md` no projeto de origem) nao ficam no repositorio: o conteudo deles ja esta em cada `SKILL.md`.

## Regra de manutencao

1. Altere sempre `.agents/skills/speckit-<fase>/SKILL.md`. Nao existe segunda copia para sincronizar.
2. Mantenha o `SKILL.md` neutro em relacao ao runtime: nada de `/speckit-plan` nem `/speckit.plan` no corpo. Cite a fase de forma generica e deixe a ferramenta resolver o gatilho.
3. Fase nova precisa de um diretorio proprio em `.agents/skills/`, nomeado `speckit-<fase>`, com `name: speckit-<fase>` no frontmatter. O nome do diretorio e o que vira o gatilho de invocacao.
4. Nao crie pasta de comando de ferramenta para expor a fase. Se algum dia uma ferramenta exigir isso, o arquivo aponta para o `SKILL.md` e nao carrega workflow.
5. Estrutura de artefato gerado (secao, campo, ordem) muda em `.specify/templates/<artefato>-template.md`. A skill da fase nao repete essa estrutura.
