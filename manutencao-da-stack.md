# Manutenção da stack

> Este documento é para quem mantém ou evolui a stack de IA. Se você só quer usar a stack, leia [`README.md`](README.md) e [`speckit.md`](speckit.md).

Aqui estão as mudanças nos arquivos da stack dentro do repositório: `.agents/`, `.claude/`, `.claude-plugin/`, `.github/`, `.opencode/`, `.specify/`, `.vscode/` e `docs/stack_ai/`. Atualizações das ferramentas locais (Copilot, OpenCode, Claude Code) são responsabilidade de cada ferramenta e documentadas por elas mesmas.

Sempre crie uma branch dedicada e abra um Pull Request para revisão antes de incorporar qualquer mudança ao repositório principal.

## Sumário

- [Como o SpecKit está organizado](#como-o-speckit-está-organizado)
- [Mapa de atualização](#mapa-de-atualização)
- [Como atualizar o SpecKit](#como-atualizar-o-speckit)
- [Como atualizar o OWASP Secure Agent Playbook](#como-atualizar-o-owasp-secure-agent-playbook)
- [Como atualizar os demais arquivos da stack](#como-atualizar-os-demais-arquivos-da-stack)

---

## Como o SpecKit está organizado

Para manter e atualizar o SpecKit com segurança, é preciso entender o papel de cada grupo de arquivos.

### Skills: o que de fato executa

```text
.agents/skills/
├── speckit-specify/SKILL.md
├── speckit-clarify/SKILL.md
├── speckit-plan/SKILL.md
├── speckit-tasks/SKILL.md
├── speckit-analyze/SKILL.md
├── speckit-implement/SKILL.md
├── speckit-checklist/SKILL.md
├── speckit-constitution/SKILL.md
├── speckit-converge/SKILL.md
└── speckit-taskstoissues/SKILL.md
```

Esses arquivos são o **núcleo operacional do SpecKit**. Cada `SKILL.md` contém o fluxo completo de uma fase: o que o agente deve fazer, em que ordem, quais verificações realizar e como tratar os resultados. Quando você invoca `/speckit-specify`, é a skill correspondente que o agente executa.

As skills são autossuficientes e agnósticas de ferramenta: funcionam no Copilot, no OpenCode ou em qualquer outro assistente que consiga ler o arquivo.

As fases ficam no mesmo nível das demais skills do repositório porque a descoberta enxerga um nível abaixo do diretório configurado, no formato `<local>/<nome>/SKILL.md`. Fase nova precisa só de um diretório próprio em `.agents/skills/`, nomeado `speckit-<fase>`.

> **Tenha cautela ao alterar skills do SpecKit.** Qualquer mudança nesses arquivos afeta diretamente o comportamento do fluxo SDD para toda a equipe. Antes de editar, entenda o impacto na fase inteira. Teste o fluxo após a mudança e documente o motivo no Pull Request.

A regra que o agente segue ao editar uma fase está em `.agents/references/speckit.md`. Ela não é repetida aqui.

### Nenhuma ferramenta guarda arquivo de comando

As três ferramentas descobrem as 10 fases sozinhas lendo `.agents/skills/`, e o nome do gatilho sai do diretório da skill, igual nas três: `/speckit-specify`.

Não crie arquivo de comando em `.claude/commands/`, `.github/agents/`, `.github/prompts/` ou `.opencode/command/` para expor uma fase. Se algum dia uma ferramenta exigir isso, o arquivo aponta para o `SKILL.md` e não carrega workflow.

### A pasta `.specify/`

```text
.specify/
├── templates/         <- base de comparação para atualizar as skills
├── scripts/           <- scripts de suporte chamados em tempo de execução
├── integrations/      <- manifestos de integração
├── workflows/         <- registro de workflows
└── memory/
    └── constitution.md  <- intencionalmente vazio; não governa o fluxo
```

Os templates em `.specify/templates/` são a origem das skills em `.agents/skills/speckit-*/`. Eles não fazem parte do fluxo de execução diário e permanecem no repositório como referência para atualizações futuras: ao avaliar uma nova versão, você compara os templates novos com as skills geradas anteriormente para identificar o que mudou e precisa ser incorporado.

O que é ativo no dia a dia são os scripts em `.specify/scripts/`, chamados pelas skills em tempo de execução, por exemplo para criar a branch da funcionalidade.

O arquivo `.specify/memory/constitution.md` é mantido **intencionalmente vazio** e não governa o fluxo: as regras de governança vivem nas próprias skills de fase.

Os arquivos de configuração pessoal do SpecKit ficam no `.gitignore` e não são versionados. Cada desenvolvedor configura os seus na própria máquina conforme a ferramenta que usa, e a ausência deles não impede o uso do SpecKit: o fluxo trata a ausência como configuração padrão.

---

## Mapa de atualização

### SpecKit

| Grupo de arquivo | Ao atualizar o SpecKit | Ao evoluir o projeto |
|---|---|---|
| Skills em `.agents/skills/speckit-*/` | Merge manual com atenção, preservando os ajustes da equipe | Raramente; abrir PR com justificativa clara |
| Templates em `.specify/templates/` | Atualizar, para servirem de base na comparação seguinte | Não se aplica |
| Scripts em `.specify/scripts/` e manifestos em `.specify/integrations/` | Substituição direta pela versão nova | Não se aplica |
| Arquivo `.specify/memory/constitution.md` | Manter vazio; não incorporar o template novo | Manter vazio; as regras vivem nas skills de fase |
| Checklists e templates criados pela equipe | Preservar, porque são da equipe e não do SpecKit | Atualizar conforme os padrões do projeto evoluem |
| Pasta `.agents/`, fora de `skills/speckit-*/` | Não se aplica | Ciclo normal do projeto |
| Arquivos `AGENTS.md` e `.github/copilot-instructions.md` | Não se aplica | Ciclo normal do projeto |
| Pasta `docs/stack_ai/` | Atualizar a versão do template citada em `speckit.md` e no `README.md` da pasta | Ciclo normal do projeto |

### Skill `owasp-playbook`

| Grupo de arquivo | Ao atualizar a skill `owasp-playbook` | Ao evoluir o projeto |
|---|---|---|
| Pasta `.agents/skills/owasp-playbook/upstream/` | Substituição da pasta inteira pela versão nova do projeto de origem, pela seção [Como atualizar o OWASP Secure Agent Playbook](#como-atualizar-o-owasp-secure-agent-playbook) | Nunca editar o conteúdo; melhoria vira Pull Request no projeto de origem |
| Arquivo `.agents/skills/owasp-playbook/SKILL.md` | Conferir a tabela de plays disponíveis contra os plays da versão nova | Nunca receber ajuste do projeto; o que é do SEI vai para a ponte |
| Arquivo `.agents/security/mapa-seguranca-cwe-sei.md` | Conferir a tabela OpenCRE contra `upstream/data/opencre/` | Ciclo normal do projeto |
| Pasta `docs/stack_ai/` | Atualizar versão, commit e data na seção [Como atualizar o OWASP Secure Agent Playbook](#como-atualizar-o-owasp-secure-agent-playbook) e a versão na tabela de skills de terceiros do `README.md` | Ciclo normal do projeto |

---

## Como atualizar o SpecKit

1. Identifique a nova versão em [github.com/github/spec-kit](https://github.com/github/spec-kit) e leia o changelog para entender o que mudou em cada fase.
2. Para cada skill em `.agents/skills/speckit-*/`, compare a skill atual com o template novo da fase correspondente. Aplique o merge manualmente, preservando qualquer ajuste que a equipe tenha feito.
3. Substitua diretamente os scripts em `.specify/scripts/`, nas duas versões: `bash/` e `powershell/`. Se a nova versão criar ou remover fase, crie ou remova o diretório correspondente em `.agents/skills/`.
4. Atualize os templates em `.specify/templates/` para refletir a nova versão: eles servem de base de comparação para a próxima atualização.
5. Mantenha `.specify/memory/constitution.md` vazio. As regras de governança vivem nas próprias skills de fase, então não incorpore o conteúdo do novo `constitution-template.md`.
6. Teste o fluxo ponta a ponta (`specify`, `plan`, `tasks`, `implement`) em uma funcionalidade de exemplo.
7. Atualize a versão registrada na nota de [`speckit.md`](speckit.md) e na tabela de skills de terceiros do [`README.md`](README.md), e abra um Pull Request descrevendo o que mudou.

---

## Como atualizar o OWASP Secure Agent Playbook

A skill `owasp-playbook` tem duas partes. O `SKILL.md` é do projeto: seleciona o play e faz a ponte com os controles do SEI. A pasta `upstream/` é cópia parcial e literal do repositório [OWASP/secure-agent-playbook](https://github.com/OWASP/secure-agent-playbook). O conteúdo fica versionado aqui porque Copilot e OpenCode leem `.agents/skills/` direto e não instalam plugin do Claude Code.

| Item | Valor instalado |
|---|---|
| Versão | v0.2.7 |
| Commit de origem | `79fea6b9115b55687818f8c4073844ee9ba907a6` |
| Data do commit | 2026-06-02 |
| Licença do playbook | CC-BY-4.0, em `upstream/LICENSE.md` |
| Licença dos dados OWASP em `upstream/data/` e `upstream/plugins/*/data/` | CC-BY-SA-4.0, em `upstream/THIRD_PARTY_NOTICES.md` |

### Regras da pasta `upstream/`

- Nunca edite arquivo dentro de `upstream/`. A atualização substitui a pasta inteira, e editar o conteúdo cria obra derivada sob a cláusula ShareAlike dos dados OWASP.
- Mantenha a árvore do upstream como ela vem. Plays, skills e templates de dentro dela se referenciam por caminho relativo, e achatar a estrutura quebra esses links.
- A varredura de travessão do projeto não se aplica a `upstream/`. O conteúdo é em inglês e não é nosso.
- O `SKILL.md` da skill é agnóstico e não recebe ajuste do projeto: é o mesmo arquivo em qualquer repositório. Tudo que é do SEI fica na ponte `.agents/security/mapa-seguranca-cwe-sei.md`.
- Correção no conteúdo do playbook vira Pull Request no repositório de origem.
- Só o `SKILL.md` da skill, um nível abaixo de `.agents/skills/`, é descoberto pelas ferramentas. Os `SKILL.md` que existem dentro de `upstream/plugins/*/skills/` não aparecem na lista de skills.

### O que fica de fora da cópia

| Retirado do upstream | Motivo |
|---|---|
| `plugins/*/agents/` | Subagentes no formato do Claude Code. Copilot e OpenCode ignoram, e o `AGENTS.md` não autoriza abrir subagente por conta própria |
| `.claude-plugin/` na raiz e em cada plugin | Manifesto de marketplace do Claude Code. O repositório já tem o seu em `.claude-plugin/marketplace.json` |
| `.claude/skills/` | Duas skills com frontmatter `allowed-tools:`, específico do Claude Code. Os plays correspondentes já vêm em `plugins/ai-security-skills/plays/` |
| `scripts/` | Extratores em Python que geram `data/` a partir dos repositórios OWASP. Não são usados em tempo de execução |
| `template/` | Andaime para quem contribui com skill nova no upstream |
| Conjunto mobile: `plugins/code-security-skills/plays/mobile-code-review.md`, `plugins/code-security-skills/skills/mobile-code-review/`, `plugins/code-security-skills/data/mastg/`, `plugins/code-security-skills/data/masvs/` e `examples/mobile-*-fixture/` | Revisão de Android e iOS contra MASVS. Não há código mobile neste repositório. As fixtures são código vulnerável de propósito e geram ruído em varredura de segurança do próprio repositório |
| `.github/`, `.gitignore`, `CLAUDE.md` e `CONTRIBUTING.md` | Tooling e governança do repositório de origem |

### Procedimento

1. Identifique a versão nova nas [releases do upstream](https://github.com/OWASP/secure-agent-playbook/releases) e leia o changelog.
2. Em uma branch dedicada, rode o script abaixo a partir da raiz do repositório, trocando o valor de `VERSAO` pela tag nova.

```bash
VERSAO=v0.2.7
ORIGEM=$(mktemp -d)
DEST=.agents/skills/owasp-playbook/upstream

git clone --depth 1 --branch "$VERSAO" https://github.com/OWASP/secure-agent-playbook "$ORIGEM"
git -C "$ORIGEM" rev-parse HEAD
git -C "$ORIGEM" log -1 --format=%cs

rm -rf "$DEST"
cp -r "$ORIGEM" "$DEST"
rm -rf "$DEST/.git" "$DEST/.github" "$DEST/.claude" "$DEST/.claude-plugin" \
       "$DEST/.gitignore" "$DEST/CLAUDE.md" "$DEST/CONTRIBUTING.md" \
       "$DEST/scripts" "$DEST/template" \
       "$DEST"/plugins/*/.claude-plugin "$DEST"/plugins/*/agents \
       "$DEST"/examples/mobile-*-fixture \
       "$DEST/plugins/code-security-skills/plays/mobile-code-review.md" \
       "$DEST/plugins/code-security-skills/skills/mobile-code-review" \
       "$DEST/plugins/code-security-skills/data/mastg" \
       "$DEST/plugins/code-security-skills/data/masvs"
rm -rf "$ORIGEM"
```

O script copia tudo e depois remove a lista de exclusão. Pasta nova que o upstream criar aparece no `git status` e é avaliada no Pull Request: ou entra na lista de exclusão, ou fica.

3. Registre o commit e a data que o script imprimiu na tabela desta seção, e atualize a versão na tabela de skills de terceiros do [`README.md`](README.md).
4. Confira a tabela de plays disponíveis do `SKILL.md` da skill contra `ls upstream/plugins/*/plays/`. Play novo, removido ou renomeado exige ajuste na tabela e na contagem de plays citada em `AGENTS.md` e no `README.md`.
5. Confira a tabela OpenCRE de `.agents/security/mapa-seguranca-cwe-sei.md` contra `ls upstream/data/opencre/`. Ficha nova pode cobrir CWE que hoje está fora do mapa.
6. Abra o Pull Request descrevendo o que mudou.

---

## Como atualizar os demais arquivos da stack

Os demais arquivos da stack seguem o ciclo normal do projeto: branch dedicada, alteração e Pull Request para revisão.

Três arquivos são do projeto e nunca são substituídos por uma atualização da stack, porque o conteúdo deles é próprio do repositório: `AGENTS.md`, `CLAUDE.md` e o `README.md` da raiz.

Três arquivos recebem acréscimos da stack e mantêm o que o time já tinha, então divergência neles é esperada e não é problema: `.gitignore`, `.vscode/settings.json` e `.claude/settings.json`.
