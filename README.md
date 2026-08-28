# Stack de IA Apoiando Desenvolvimento

Repositório de apoio com a stack de IA usada no desenvolvimento de módulos SEI.

Aqui ficam concentrados os artefatos que dão suporte ao uso de agentes, prompts, skills e fluxo SDD com SpecKit. Este repositório não contém o código-fonte da aplicação SEI, módulos da aplicação nem scripts de release da aplicação; ele existe como skeleton da camada de IA.

---

## Sumário

- [Para quem é este documento](#para-quem-é-este-documento)
- [Stack de IA](#stack-de-ia)
  - [Introdução](#introdução)
  - [Filosofia e origem da stack](#filosofia-e-origem-da-stack)
  - [O que são modelos de IA](#o-que-são-modelos-de-ia)
  - [O que são agentes de IA](#o-que-são-agentes-de-ia)
    - [Skills: agentes especializados](#skills-agentes-especializados)
  - [O que é SDD](#o-que-é-sdd)
  - [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas)
  - [O que é o SpecKit](#o-que-é-o-speckit)
    - [Quando usar o SpecKit](#quando-usar-o-speckit)
    - [Fases do SpecKit](#fases-do-speckit)
    - [Como invocar as fases](#como-invocar-as-fases)
    - [Integrações por ferramenta](#integrações-por-ferramenta)
  - [Estrutura da stack](#estrutura-da-stack)
  - [Como começar com a stack de IA](#como-começar-com-a-stack-de-ia)
- [Atualizações da stack](#atualizações-da-stack)
  - [Como o SpecKit está organizado neste repositório](#como-o-speckit-está-organizado-neste-repositório)
  - [Mapa de atualização](#mapa-de-atualização)
  - [Como atualizar o SpecKit](#como-atualizar-o-speckit)
- [Referências](#referências)

---

## Para quem é este documento

Este README é para quem precisa usar, adaptar ou manter este skeleton da stack de IA. Ele explica como os agentes, prompts, skills, adapters e o fluxo SDD com SpecKit estão organizados neste repositório.

O foco é exclusivamente a camada de IA. Qualquer menção a módulos SEI aparece apenas como contexto de uso das skills, não como documentação da aplicação SEI.

---

## Stack de IA

### Introdução

Esta seção explica a camada de inteligência artificial integrada ao repositório. Mesmo que você nunca tenha trabalhado com IA antes, a leitura a seguir vai mostrar o que existe, como está organizado e como você pode começar a usar.

Exemplos práticos do que você pode pedir ao assistente:
- *"Analise o módulo `<nome-do-modulo>` e me diga quais são os pontos de risco de segurança."*
- *"Crie um plano de implementação para adicionar um novo campo no formulário X."*
- *"Revise o código que acabei de escrever e verifique se segue os padrões do projeto."*

Para ver mais exemplos prontos para usar, consulte [`docs/prompts-exemplo.md`](docs/prompts-exemplo.md).

### Filosofia e origem da stack

A stack de IA deste repositório foi construída sobre um padrão aberto adotado por comunidades de desenvolvimento ao redor do mundo: o [AGENTS.md](https://agents.md). Esse padrão, hoje mantido pela Agentic AI Foundation sob a Linux Foundation e presente em mais de 60 mil projetos de código aberto (projetos cujo código-fonte é público e pode ser inspecionado por qualquer pessoa), propõe uma separação clara entre o que é escrito para humanos e o que é escrito para agentes de IA:

- **README.md**: para humanos (visão geral, contexto, como começar)
- **AGENTS.md**: para agentes (regras de codificação, restrições, padrões do projeto)

Ao seguir esse padrão, a stack se torna **agnóstica de ferramenta**: qualquer assistente de IA que respeite o `AGENTS.md` consegue trabalhar neste repositório sem configuração adicional. Não estamos presos a uma ferramenta específica; o contexto do projeto viaja junto com o código.

Ferramentas como GitHub Copilot, OpenCode e outras da comunidade já seguem esse padrão nativamente, o que significa que o investimento feito na stack do projeto funciona independentemente de qual ferramenta o desenvolvedor escolher usar.

> **Origem da convenção:** o `AGENTS.md` deste repositório foi estruturado com base na convenção publicada em [agents.md](https://agents.md). O padrão não possui versionamento formal; a referência de atualização é o próprio site.

O arquivo [`CLAUDE.md`](CLAUDE.md) existe apenas como ponteiro de compatibilidade para `AGENTS.md`.

### O que são modelos de IA

Um **modelo de IA** é o "cérebro" por trás do assistente: o sistema que entende o que você escreve e gera respostas. Modelos conhecidos incluem Claude, GPT e outros modelos compatíveis com ferramentas de desenvolvimento.

Neste projeto, os modelos de IA são acessados por meio de ferramentas já integradas ao fluxo de trabalho. Você não precisa acessar o modelo diretamente; a ferramenta faz isso por você.

| Ferramenta | Modelo / Provedor |
|---|---|
| GitHub Copilot | GPT-5.6 ou Claude Opus, dependendo do plano da conta |
| OpenCode | Configurável, compatível com múltiplos modelos |
| Claude Code | Modelo Claude (Anthropic) |

Os modelos evoluem com frequência. O que importa para o uso do dia a dia é a **ferramenta**; o modelo é apenas o motor por baixo.

### O que são agentes de IA

Um **agente de IA** é um assistente configurado para operar com um conjunto específico de instruções, contexto e regras. Diferente de um modelo genérico de IA que você acessa pelo navegador, um agente:

- Conhece o projeto em que está trabalhando
- Segue **guardrails** (regras que definem o que ele pode e não pode fazer, como quais arquivos pode modificar e quais padrões de código deve seguir)
- Segue um fluxo estruturado em vez de responder de forma livre

Neste repositório, os agentes são configurados na pasta `.agents/` e integrados às ferramentas via `.github/` (Copilot), `.opencode/` (OpenCode) e `.claude/` (Claude Code). Eles não são programas independentes; são instruções que ensinam a ferramenta de IA a agir como um especialista no contexto do SEI.

**Na prática:** quando você abre este repositório no VS Code (editor de código da Microsoft) com o Copilot e pede *"revise este código segundo os padrões do projeto"*, o agente carrega automaticamente as regras do `AGENTS.md`, os guardrails de segurança e os padrões de codificação, e entrega uma revisão contextualizada, não genérica.

#### Skills: agentes especializados

As **skills** são agentes especializados em tarefas específicas. Cada skill tem um escopo bem definido. Para acionar uma skill, mencione o nome dela na conversa com o assistente (no painel de chat da ferramenta de IA, como o chat do Copilot no VS Code). Por exemplo: *"Use a skill `sei-gerador-crud` para criar a entidade X."* O assistente carregará as instruções da skill e executará o processo correspondente.

| Skill | O que faz |
|---|---|
| `sei-gerador-crud` | Gera o CRUD completo de uma entidade (tela de listagem, tela de cadastro, regras de negócio, acesso ao banco) |
| `sei-guardrails-modulo` | Aplica guardrails obrigatórios para trabalhos em módulos SEI |
| `sei-direcionador-integracao` | Ajuda a escolher entre API, evento ou operação oficial do SEI quando a intenção ainda está ambígua |
| `sei-verificacao-banco-dados` | Valida se a camada de acesso ao banco de dados segue os padrões do projeto |
| `sei-verificacao-pagina` | Valida páginas PHP quanto a segurança e padrões SEI |
| `sei-verificacao-rn` | Valida classes de regra de negócio quanto a transação e separação de camadas |
| `sei-verificacao-controladores` | Valida controladores de integração SEI |
| `sei-verificacao-tarefa` | Valida IDs de tarefas de módulo |
| `sei-gerador-scripts-release` | Gera os scripts de instalação e atualização do lado SEI |
| `sip-gerador-scripts-release` | Gera os scripts de instalação e atualização do lado SIP |
| `sei-mod-api-classes` | Ajuda a localizar contratos oficiais de API do SEI |
| `sei-mod-api-operacoes` | Orienta operações oficiais do SEI via API e `SeiRN` |
| `sei-mod-api-eventos` | Orienta interceptação de eventos do SEI via integração de módulo |
| `sei-menu-pagina` | Orienta criação ou ajuste de menus internos e páginas correspondentes |
| `sei-testes-validacao` | Centraliza checagens e validações após alterações PHP |
| `sei-tipagem-phpdoc` | Apoia modernização segura de tipagem PHP e PHPDoc quando solicitada explicitamente |
| `sei-report-todos` | Gera relatório de pendências `TODO:` em módulos escolhidos explicitamente |
| `dicionario-dados-db-scan-codebase-docs` | Cria, atualiza e verifica dicionários de dados e changelogs estruturais a partir de artefatos versionados da codebase |
| `napkin` | Mantém runbook operacional pessoal em `.agents/memory/runbook.md` |
| `caveman`, `ponytail`, `grilling` | Modos auxiliares para comunicação compacta, simplificação e stress-test de planos |
| `sei-revisao-tecnica` | Revisa diretamente segurança, conformidade, gates e qualidade técnica de diffs, arquivos ou módulos SEI, sem exigir spec |
| `code-review` | Revisa Standards de um delta commitado desde um ponto fixo, delegando a análise técnica para `sei-revisao-tecnica` |
| `speckit` | Conduz as fases do fluxo SDD com SpecKit |

> **Glossário rápido:** CRUD = conjunto de operações de criar, ler, atualizar e deletar registros. Script de release = arquivo executado na instalação ou atualização do módulo no servidor.

Use `sei-revisao-tecnica` diretamente para revisão técnica, security review, compliance, gates ou módulo SEI, inclusive sobre worktree ou diff fornecido. Os aliases históricos são resolvidos textualmente conforme a matriz de roteamento.

Use `code-review` para mudanças commitadas de branch ou PR, informando o commit, branch ou tag que fixa o início do delta. Nesta versão, a skill executa somente Standards e não avalia spec ou requisito. Para worktree sem commit, use revisão técnica direta ou forneça um diff.

A tabela acima é apenas uma visão inicial. O catálogo completo das skills, com origem, versão, licença e composição, está em [`.agents/skills/README.md`](.agents/skills/README.md).

### O que é SDD

**[SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)** (Specification-Driven Development, ou Desenvolvimento Orientado por Especificação) é uma abordagem de trabalho que coloca a especificação antes da implementação.

A ideia central é simples: antes de escrever código (implementar = traduzir uma necessidade em instruções que o computador executa), você produz uma descrição clara e estruturada do que precisa ser feito, e o agente de IA parte sempre dessa descrição. Isso evita o problema mais comum no uso de IA para código: pedir para implementar algo sem ter definido direito o que é esse "algo". Com SDD, o raciocínio vem antes da implementação.

Neste repositório, o SDD é implementado pelo framework **SpecKit** (veja a seção [O que é o SpecKit](#o-que-é-o-speckit)). O fluxo completo vai de `especificar → clarificar → planejar → decompor → implementar`.

### Ferramentas de IA suportadas

Este repositório é **agnóstico de ferramenta**: você pode usar qualquer assistente de IA, desde que ele consiga ler o contexto do repositório (especialmente `.agents/skills/` e `AGENTS.md`).

A ferramenta **recomendada** é a extensão do **GitHub Copilot no [VS Code](https://code.visualstudio.com)** (editor de código gratuito da Microsoft), por ser a mais simples de configurar e a mais integrada ao fluxo atual do projeto.

| Ferramenta | Como instalar | Arquivos de configuração |
|---|---|---|
| **[GitHub Copilot](https://github.com/features/copilot)** | Instale a extensão "GitHub Copilot" pelo marketplace do VS Code (a loja de extensões do editor, equivalente a uma loja de aplicativos) e faça login com sua conta GitHub | `.github/copilot-instructions.md` e `.vscode/settings.json` |
| **[OpenCode](https://opencode.ai)** | Instale via terminal (a interface de texto do computador onde você digita comandos) com `npm install -g opencode-ai` e configure o modelo desejado | `.opencode/opencode.json` |
| **[Claude Code](https://claude.com/claude-code)** | Instale via terminal com `curl -fsSL https://claude.ai/install.sh \| bash` e faça login com sua conta Claude | `.claude/skills` (symlink para `.agents/skills`) |

> **O que é npm?** É o gerenciador de pacotes do Node.js, uma ferramenta de linha de comando usada para instalar softwares de desenvolvimento. Se você nunca usou, peça ajuda a um desenvolvedor da equipe para instalar o OpenCode.

Se você optar por uma ferramenta diferente das listadas acima, confirme antes que ela consegue ler `.agents/skills/` e seguir as instruções de `AGENTS.md`.

### O que é o SpecKit

> **Não é necessário instalar o SpecKit.** Toda a estrutura do SpecKit já está presente neste repositório. O único requisito é ter uma das ferramentas de IA listadas na seção [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas) instalada e configurada. Se você estiver usando o GitHub Copilot ou o OpenCode com este repositório aberto, o SpecKit já está disponível.

**SpecKit** é o framework de especificação que estrutura o fluxo SDD neste repositório. Ele divide o trabalho em fases sequenciais e produz documentos padronizados (especificação, plano técnico e lista de tarefas) que servem de contexto para a implementação.

O SpecKit foi escolhido como ponto de partida do SDD neste projeto por algumas razões práticas: é uma ferramenta de fácil adoção para equipes que estão começando a introduzir especificação no fluxo de desenvolvimento, tem integração direta com o GitHub Copilot (a ferramenta recomendada do projeto) e conta com uma comunidade ativa que mantém o framework atualizado. Isso reduz o risco de depender de algo que ficará sem suporte.

> **Não substitua os arquivos do SpecKit no repositório.** Se houver uma nova versão disponível, a atualização deve ser coordenada pela equipe seguindo o processo descrito na seção [Atualizações da stack](#atualizações-da-stack). Substituir os arquivos sem revisão pode quebrar o fluxo para todas as ferramentas integradas.

> **Versão do template:** a estrutura do SpecKit neste repositório foi gerada a partir do **Template Version 0.12.4**. Consulte essa versão como referência ao comparar ou atualizar os arquivos em `.specify/`.

#### Quando usar o SpecKit

Use o SpecKit quando a demanda for **maior, nova ou ambígua**, quando você sente que precisa pensar antes de implementar. Para correções pontuais e pequenas alterações, o fluxo direto (conversa com o agente) é suficiente.

#### Fases do SpecKit

| Fase | Comando | O que faz |
|---|---|---|
| 1. Especificação | `/speckit-specify` | Transforma a descrição em linguagem natural em uma especificação estruturada |
| 2. Clarificação | `/speckit-clarify` | Levanta dúvidas e ambiguidades antes de planejar |
| 3. Planejamento | `/speckit-plan` | Produz o plano técnico de implementação |
| 4. Tarefas | `/speckit-tasks` | Decompõe o plano em tarefas granulares e sequenciadas |
| 5. Análise | `/speckit-analyze` | Analisa riscos, dependências e impactos |
| 6. Implementação | `/speckit-implement` | Implementa seguindo o plano e as tarefas definidos nas fases anteriores |

Além das fases principais, há três comandos auxiliares: `/speckit-checklist` (gera o checklist de implementação da funcionalidade), `/speckit-taskstoissues` (converte as tarefas em issues no GitHub) e `/speckit-constitution` (manutenção do arquivo `constitution.md`, que neste repositório permanece intencionalmente vazio — veja a seção [Como o SpecKit está organizado neste repositório](#como-o-speckit-está-organizado-neste-repositório)).

Os documentos gerados (especificação, plano, tarefas) ficam em `specs/<nome-da-funcionalidade>/` na sua máquina local. A pasta `specs/` está no `.gitignore` do repositório: os documentos ficam somente na sua máquina e nunca são enviados ao repositório compartilhado. Isso é intencional; esses arquivos são descartáveis e existem apenas para guiar aquela entrega específica.

#### Como invocar as fases

- **No Copilot (VS Code):** abra o painel de chat do Copilot (ícone de balão de conversa na barra lateral esquerda do VS Code), clique no nome do agente atual (geralmente aparece como `@GitHub Copilot` ou `@workspace` acima da caixa de texto) e selecione a skill correspondente, como `speckit-specify`.
- **No OpenCode (terminal, a interface de texto do computador):** digite o comando diretamente, como `/speckit-specify`.
- **No Claude Code (terminal ou app):** digite o comando diretamente, como `/speckit-specify`.

#### Integrações por ferramenta

O fluxo padrão do SpecKit vive em `.agents/skills/speckit-<fase>/` e **nenhuma integração guarda arquivo dele**. `.claude/commands/`, `.github/agents/`, `.github/prompts/` e `.opencode/command/` estão vazios, só como convenção de cada ferramenta.

As três leem `.agents/skills/` direto e encontram as fases lá, lado a lado com as demais skills do repositório, sem symlink e sem configuração extra:

- **Claude Code**: `.claude/skills`, symlink para `../.agents/skills`
- **Copilot**: `chat.agentSkillsLocations` em `.vscode/settings.json`
- **OpenCode**: `skills.paths` em `.opencode/opencode.json`

### Estrutura da stack

```text
.agents/
├── checklists/    # Checklists modulares de validação técnica (BD, DTO, RN, permissões, segurança)
├── decisions/     # Registros de decisões arquiteturais: o porquê de escolhas técnicas importantes
├── memory/        # Contexto operacional reutilizável entre sessões (ex: runbooks e guias rápidos)
├── references/    # Material de referência consultado pelas skills: padrões, roteamento e pontos de verificação
├── security/      # Guias e matrizes de revisão de segurança
└── skills/        # Skills do projeto: agentes especializados por domínio ou tipo de tarefa

.claude/
├── skills/        # Symlink para .agents/skills/ (convenção de skills do Claude Code)
└── commands/      # Comandos do Claude Code (adaptadores das skills para uso via slash command)

.github/
├── agents/        # Agentes do GitHub Copilot (adaptadores das skills para uso no VS Code)
├── prompts/       # Atalhos de prompts do Copilot
└── copilot-instructions.md  # Instruções curtas carregadas pelo Copilot

.opencode/
├── command/       # Comandos do OpenCode (adaptadores das skills para uso no terminal)
└── opencode.json  # Configuração do OpenCode para o repositório

.specify/
├── integrations/  # Manifestos de integração do SpecKit por ferramenta (usados no setup inicial)
├── memory/        # Contém o constitution.md do SpecKit, mantido intencionalmente vazio (as regras vivem nas skills de fase)
├── references/    # Referências internas do SpecKit
├── scripts/       # Scripts chamados pelas skills em tempo de execução (ex: criação de branch)
└── templates/     # Templates de origem do SpecKit (usados uma vez para gerar as skills; mantidos como referência)

docs/              # Exemplos de prompts e documentação de apoio consultada pela stack
specs/             # Documentos gerados pelo SpecKit por funcionalidade (somente na sua máquina)
AGENTS.md          # Regras do projeto para agentes de IA (leia antes de contribuir)
CLAUDE.md          # Ponteiro de compatibilidade para AGENTS.md
```

**Arquivos e pastas no `.gitignore`**

Alguns itens do repositório existem apenas localmente em cada máquina e estão listados no `.gitignore` para não serem versionados. Eles devem permanecer assim:

| Item | Por que não é versionado |
|---|---|
| `specs/` | Documentos gerados pelo SpecKit para cada funcionalidade; são locais e descartáveis |
| `node_modules/` | Dependências instaladas pelo npm para o OpenCode; nunca devem ser salvas no repositório |
| `.env*` | Arquivos de configuração com dados sensíveis como senhas e chaves de acesso ao sistema |
| `.agents/memory/runbook.md` | Runbook pessoal de cada desenvolvedor, mantido localmente pela skill `napkin` |
| `.specify/init-options.json`, `.specify/integration.json`, `.specify/feature.json` | Configuração local do SpecKit por desenvolvedor (ver seção [Como o SpecKit está organizado neste repositório](#como-o-speckit-está-organizado-neste-repositório)) |

Antes de remover qualquer item do `.gitignore`, avalie se a remoção é realmente necessária. Na dúvida, mantenha.

**O que cada pasta faz na prática:**

- `checklists/`: checklists modulares de validação técnica por camada (BD, DTO, RN, permissões, segurança). Consultados pela skill `sei-revisao-tecnica` e usados manualmente antes do merge.
- `decisions/`: registra o porquê de decisões técnicas importantes, como "por que escolhemos o SpecKit" ou "por que essa tabela foi modelada assim". Consulte antes de propor mudanças arquiteturais.
- `memory/`: guarda contexto operacional reutilizável entre sessões de trabalho, como guias rápidos e runbooks (documentos de procedimentos). O `runbook.md` dessa pasta é pessoal de cada desenvolvedor e não é versionado.
- `references/`: material base consultado pelas skills: padrões de codificação, roteamento de demandas e pontos de verificação obrigatórios.
- `security/`: guias e matrizes de revisão de segurança do código, consultados pela skill `sei-revisao-tecnica`.
- `skills/`: as skills do projeto. A maioria das pastas corresponde a uma skill com escopo e instruções próprias; algumas, como `speckit/`, agrupam uma suíte de sub-skills relacionadas.

### Como começar com a stack de IA

**Passo 1: Baixe o repositório.** Faça o clone do repositório (baixe uma cópia local usando Git) e abra a pasta raiz no VS Code.

**Passo 2: Instale uma ferramenta.** A recomendada é a extensão GitHub Copilot no VS Code. Abra o VS Code, clique no ícone de extensões na barra lateral (quatro quadradinhos), pesquise "GitHub Copilot" e clique em instalar. Depois faça login com sua conta GitHub. O Copilot detecta automaticamente os arquivos de configuração do projeto: ao abrir a pasta, ele lê o `AGENTS.md` e as pastas `.github/` e `.agents/`, carregando as regras e os agentes do projeto sem nenhuma ação adicional sua.

**Passo 3: Para uma demanda simples,** abra o chat do Copilot e descreva o que precisa. Exemplo:
> *"Analise o módulo `ia` sem alterar nada. Quero entender como funciona a integração com o servidor de soluções de IA."*

**Passo 4: Para uma demanda maior ou ambígua,** use o fluxo SpecKit, começando por `/speckit-specify`. Exemplo:
> *"Preciso adicionar uma nova funcionalidade de exportação de relatórios no módulo de utilidades."*

**Passo 5: Consulte os exemplos** em [`docs/prompts-exemplo.md`](docs/prompts-exemplo.md) para ver como formular bons pedidos para diferentes tipos de demanda.

Você **não** precisa instalar o SpecKit nem qualquer componente adicional da stack. Tudo já está configurado no repositório. O único passo é instalar a ferramenta de IA (Passo 1).

---

## Atualizações da stack

> Esta seção é voltada para quem já trabalha no projeto e precisa manter ou evoluir a stack de IA. Se você está chegando agora, pode pular para a seção [Referências](#referências) e retornar aqui quando precisar.

Esta seção trata de mudanças nos arquivos da stack de IA dentro do repositório (`.agents/`, `.claude/`, `.github/`, `.opencode/`, `.specify/`). Atualizações das ferramentas locais (Copilot, OpenCode, Claude Code) são responsabilidade de cada ferramenta e documentadas por elas mesmas.

Sempre crie uma branch dedicada e abra um Pull Request para revisão antes de incorporar qualquer mudança ao repositório principal.

### Como o SpecKit está organizado neste repositório

Para manter e atualizar o SpecKit com segurança, é preciso entender o papel de cada grupo de arquivos.

#### Skills: o que de fato executa

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
└── speckit-taskstoissues/SKILL.md
```

Esses arquivos são o **núcleo operacional do SpecKit neste repositório**. Cada `SKILL.md` contém o fluxo completo de uma fase: o que o agente deve fazer, em que ordem, quais verificações realizar e como tratar os resultados. Quando você invoca `/speckit-specify`, é a skill correspondente que o agente executa. As skills são autossuficientes e agnósticas de ferramenta: funcionam no Copilot, no OpenCode ou em qualquer outro assistente que consiga ler o arquivo.

As fases ficam no mesmo nível das demais skills do repositório porque a descoberta enxerga um nível abaixo do diretório configurado (`<local>/<nome>/SKILL.md`). Fase nova precisa só de um diretório próprio em `.agents/skills/`, nomeado `speckit-<fase>`.

> **Tenha cautela ao alterar skills do SpecKit.** Qualquer mudança nesses arquivos afeta diretamente o comportamento do fluxo SDD para toda a equipe. Antes de editar, entenda o impacto na fase inteira. Teste o fluxo após a mudança e documente o motivo no Pull Request.

#### Por que não existem adapters por ferramenta

```text
.github/agents/      vazio
.github/prompts/     vazio
.opencode/command/   vazio
.claude/commands/    vazio
```

Já existiram: um arquivo curto por fase em cada ferramenta, que carregava a skill correspondente e mapeava o nome do comando. Eram 36 arquivos para expor 9 fases.

Com as fases no mesmo nível das demais skills, todos ficaram desnecessários. As três ferramentas descobrem as 9 fases sozinhas lendo `.agents/skills/`, e o nome do gatilho passa a sair do diretório da skill, igual nas três: `/speckit-specify`.

As pastas continuam no repositório, vazias, porque são convenção de cada ferramenta. Não crie arquivo de comando nelas. Se algum dia uma ferramenta precisar disso para expor a fase, o arquivo aponta para o `SKILL.md` e não carrega workflow.

#### A pasta `.specify/`: papel no setup inicial

```text
.specify/
├── templates/         <- usada uma vez, na geração das skills
├── scripts/           <- scripts de suporte chamados em tempo de execução
├── integrations/      <- manifestos de integração, usados no setup
├── references/        <- referências internas do SpecKit
└── memory/
    └── constitution.md  <- intencionalmente vazio; não governa o fluxo (as regras vivem nas skills de fase)
```

A pasta `.specify/` cumpriu seu papel principal durante o setup inicial do SpecKit. Os templates em `.specify/templates/` foram usados **uma única vez** para gerar as skills que estão em `.agents/skills/speckit-*/`. Depois dessa geração, os templates não fazem parte do fluxo de execução diário.

Os templates permanecem no repositório como referência para atualizações futuras do SpecKit: ao avaliar uma nova versão, você compara os templates novos com as skills geradas anteriormente para identificar o que mudou e precisa ser incorporado.

O que ainda é ativo em `.specify/` no dia a dia são os scripts em `.specify/scripts/`, chamados pelas skills em tempo de execução (ex: criação de branch). O arquivo `.specify/memory/constitution.md` é mantido **intencionalmente vazio** e não governa o fluxo: as regras de governança vivem nas próprias skills de fase, em `.agents/skills/speckit-*/`.

Os três arquivos de configuração pessoal estão no `.gitignore` e não são versionados:

```text
.specify/init-options.json   <- configuração local do desenvolvedor
.specify/integration.json    <- configuração local do desenvolvedor
.specify/feature.json        <- configuração local do desenvolvedor
```

Cada desenvolvedor configura esses arquivos na sua máquina conforme a ferramenta que usa. A ausência deles não impede o uso do SpecKit; o fluxo trata a ausência como configuração padrão.

### Mapa de atualização

| Grupo de arquivo | Ao atualizar o SpecKit | Ao evoluir o projeto SEI |
|---|---|---|
| Skills `.agents/skills/speckit-*/` | Merge com atenção, ver 6.3 | Raramente; abrir PR com justificativa clara |
| Templates `.specify/templates/` | Atualizar como referência para comparação | Não se aplica |
| `checklist-sei-template.md` | Preserve, é da equipe | Atualizar conforme padrões SEI evoluem |
| `.specify/memory/constitution.md` | Manter vazio; não incorporar o template novo | Manter vazio; as regras vivem nas skills de fase |
| `.specify/scripts/`, `.specify/integrations/` | Substituição direta | Não se aplica |
| `.agents/` (fora de `skills/speckit-*/`) | Não se aplica | Ciclo normal do projeto |
| `AGENTS.md`, `.github/copilot-instructions.md` | Não se aplica | Ciclo normal do projeto |

### Como atualizar o SpecKit

1. Identifique a nova versão em [github.com/github/spec-kit](https://github.com/github/spec-kit) e leia o changelog para entender o que mudou em cada fase.
2. Para cada skill em `.agents/skills/speckit-*/`, compare a skill atual com o template novo da fase correspondente. Aplique merge manualmente, preservando qualquer ajuste que a equipe tenha feito.
3. Substitua diretamente os scripts em `.specify/scripts/`, nas duas versões: `bash/` e `powershell/`. Se a nova versão criar ou remover fase, crie ou remova o diretório correspondente em `.agents/skills/`.
4. Atualize os templates em `.specify/templates/` para refletir a nova versão: eles servem de base de comparação para a próxima atualização.
5. Mantenha `.specify/memory/constitution.md` vazio — as regras de governança vivem nas próprias skills de fase. Não incorpore o conteúdo do novo `constitution-template.md`.
6. Teste o fluxo ponta a ponta (`specify`, `plan`, `tasks`, `implement`) em uma feature de exemplo.
7. Atualize a versão registrada na nota da seção [O que é o SpecKit](#o-que-é-o-speckit) e no catálogo [`.agents/skills/README.md`](.agents/skills/README.md), e abra um Pull Request descrevendo o que mudou.

---

## Referências

**Documentação interna do projeto:**

| Documento | O que contém |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Regras centrais do projeto para agentes: o que pode ser feito, padrões de código e regras de decisão |
| [`docs/prompts-exemplo.md`](docs/prompts-exemplo.md) | Exemplos de como conversar com a ferramenta de IA para diferentes tipos de demanda |
| [`docs/manual_desenvolvimento_md/`](docs/manual_desenvolvimento_md/) | Manual oficial de desenvolvimento de módulos SEI |
| [`docs/dicionario_dados/`](docs/dicionario_dados/) | Dicionário de dados por módulo (uma pasta por módulo: SEI, SIP, Litigioso, ...) |
| [`.agents/references/roteamento-de-skills.md`](.agents/references/roteamento-de-skills.md) | Qual skill usar para cada tipo de demanda |
| [`.agents/references/gates-de-implementacao.md`](.agents/references/gates-de-implementacao.md) | Pontos de verificação obrigatórios que impedem a implementação de avançar com problemas não resolvidos |
| [`.agents/skills/README.md`](.agents/skills/README.md) | Catálogo de auditoria das skills: origem, versão, licença e composição |

**Ferramentas e padrões externos:**

| Ferramenta / Padrão | Link |
|---|---|
| VS Code | [code.visualstudio.com](https://code.visualstudio.com) |
| GitHub Copilot | [github.com/features/copilot](https://github.com/features/copilot) |
| OpenCode | [opencode.ai](https://opencode.ai) |
| Claude Code | [claude.com/claude-code](https://claude.com/claude-code) |
| Git | [git-scm.com](https://git-scm.com) |
| Docker | [docker.com](https://www.docker.com) |
| SpecKit | [github.com/github/spec-kit](https://github.com/github/spec-kit) |
| Padrão AGENTS.md | [agents.md](https://agents.md) |
