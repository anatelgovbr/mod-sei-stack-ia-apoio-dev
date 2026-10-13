# SpecKit

## Sumário

- [O que é o SpecKit](#o-que-é-o-speckit)
- [Quando usar o SpecKit](#quando-usar-o-speckit)
- [Fases do SpecKit](#fases-do-speckit)
- [Como invocar as fases](#como-invocar-as-fases)
- [Como cada ferramenta encontra as fases](#como-cada-ferramenta-encontra-as-fases)
- [Onde ficam os documentos gerados](#onde-ficam-os-documentos-gerados)

---

## O que é o SpecKit

> **Não é necessário instalar o SpecKit.** Toda a estrutura já está presente no repositório. O único requisito é ter uma das ferramentas de IA listadas em [`README.md`](README.md) instalada e configurada.

**SpecKit** é o framework de especificação que estrutura o fluxo SDD no repositório. Ele divide o trabalho em fases sequenciais e produz documentos padronizados (especificação, plano técnico e lista de tarefas) que servem de contexto para a implementação.

O SpecKit é o ponto de partida do SDD por algumas razões práticas: é de fácil adoção para equipes que estão começando a introduzir especificação no fluxo de desenvolvimento, tem integração direta com o GitHub Copilot e conta com uma comunidade ativa que mantém o framework atualizado. Isso reduz o risco de depender de algo que ficará sem suporte.

> **Não substitua os arquivos do SpecKit por conta própria.** Se houver uma nova versão disponível, a atualização deve ser coordenada pela equipe seguindo o processo de [`manutencao-da-stack.md`](manutencao-da-stack.md). Substituir os arquivos sem revisão pode quebrar o fluxo para todas as ferramentas integradas.

> **Versão do template:** a estrutura instalada foi gerada a partir do **Template Version 1.0.3**. Consulte essa versão como referência ao comparar ou atualizar os arquivos em `.specify/`.

---

## Quando usar o SpecKit

Use o SpecKit quando a demanda for **maior, nova ou ambígua**, quando você sente que precisa pensar antes de implementar.

Para correções pontuais e pequenas alterações, o fluxo direto (conversa com o agente) é suficiente. Linha de corte prática: se a mudança cabe em uma frase e não cria tela, permissão ou fluxo novos, não precisa de SpecKit.

---

## Fases do SpecKit

São 10 fases. Seis formam o fluxo principal, na ordem da tabela.

| Ordem | Fase | Comando | O que faz |
|---|---|---|---|
| 1 | Especificação | `/speckit-specify` | Transforma a descrição em linguagem natural em uma especificação estruturada |
| 2 | Clarificação | `/speckit-clarify` | Levanta dúvidas e ambiguidades antes de planejar |
| 3 | Planejamento | `/speckit-plan` | Produz o plano técnico de implementação |
| 4 | Tarefas | `/speckit-tasks` | Decompõe o plano em tarefas granulares e sequenciadas |
| 5 | Análise | `/speckit-analyze` | Analisa riscos, dependências e impactos |
| 6 | Implementação | `/speckit-implement` | Implementa seguindo o plano e as tarefas definidos nas fases anteriores |

As quatro restantes são auxiliares e entram só quando você precisa delas.

| Fase | Comando | O que faz |
|---|---|---|
| Checklist | `/speckit-checklist` | Gera o checklist de validação dos requisitos da funcionalidade |
| Tarefas para issues | `/speckit-taskstoissues` | Converte as tarefas geradas em issues no GitHub |
| Convergência | `/speckit-converge` | Compara a codebase com a spec, o plano e as tarefas, e acrescenta em `tasks.md` o que ainda falta construir |
| Constituição | `/speckit-constitution` | Mantém o arquivo `.specify/memory/constitution.md`, que é mantido intencionalmente vazio |

O `constitution.md` fica vazio de propósito e não governa o fluxo: as regras de governança vivem nas próprias skills de fase, em `.agents/skills/speckit-*/`.

---

## Como invocar as fases

| Ferramenta | Como invocar |
|---|---|
| GitHub Copilot (VS Code) | Abra o painel de chat do Copilot (ícone de balão de conversa na barra lateral esquerda), clique no nome do agente atual (geralmente `@GitHub Copilot` ou `@workspace`, acima da caixa de texto) e selecione a skill, como `speckit-specify` |
| OpenCode (terminal) | Digite o comando diretamente, como `/speckit-specify` |
| Claude Code (terminal ou app) | Digite o comando diretamente, como `/speckit-specify` |

O nome do comando sai do diretório da skill, então ele é o mesmo nas três ferramentas, sempre com hífen: `/speckit-specify`, `/speckit-plan`.

---

## Como cada ferramenta encontra as fases

O fluxo de cada fase existe uma vez só, em `.agents/skills/speckit-<fase>/SKILL.md`. Nenhuma ferramenta guarda uma cópia.

As três leem `.agents/skills/` direto e encontram as fases lá, lado a lado com as demais skills, sem symlink e sem cópia. Cada uma chega por um caminho de configuração próprio:

| Ferramenta | Caminho de configuração |
|---|---|
| Claude Code | Plugin local `stack-ai`, do marketplace local do repositório, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json` |
| GitHub Copilot | Chave `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | Chave `skills.paths` em `.opencode/opencode.json` |

Isso funciona porque a descoberta de skill procura um nível abaixo do diretório configurado, no formato `<local>/<nome>/SKILL.md`, e as fases ficam exatamente nesse nível.

Nenhuma das três precisa de arquivo de comando. Se o repositório tiver pastas de comando vazias, como `.claude/commands/`, `.github/prompts/` ou `.opencode/command/`, elas são convenção da ferramenta e não precisam de conteúdo. Não crie arquivo de comando para expor uma fase.

---

## Onde ficam os documentos gerados

Os documentos gerados (especificação, plano, tarefas) ficam em `specs/<nome-da-funcionalidade>/`, na sua máquina.

A pasta `specs/` está no `.gitignore`: os documentos ficam somente na sua máquina e nunca são enviados ao repositório compartilhado. Isso é intencional, porque esses arquivos são descartáveis e existem apenas para guiar aquela entrega específica.

Os scripts que as fases executam ficam em `.specify/scripts/`, em duas versões equivalentes: `bash/` para Linux, macOS e WSL, e `powershell/` para Windows. Cada fase escolhe a versão certa conforme o shell da sessão.
