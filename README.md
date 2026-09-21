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
    - [Como cada ferramenta encontra as fases](#como-cada-ferramenta-encontra-as-fases)
    - [Onde ficam os documentos gerados](#onde-ficam-os-documentos-gerados)
  - [Estrutura da stack](#estrutura-da-stack)
  - [Como começar com a stack de IA](#como-começar-com-a-stack-de-ia)
- [Atualizações da stack](#atualizações-da-stack)
- [Referências](#referências)

---

## Para quem é este documento

Este README é para quem precisa usar, adaptar ou manter este skeleton da stack de IA. Ele explica como os agentes, prompts, skills e o fluxo SDD com SpecKit estão organizados neste repositório.

O foco é exclusivamente a camada de IA. Qualquer menção a módulos SEI aparece apenas como contexto de uso das skills, não como documentação da aplicação SEI.

---

## Stack de IA

### Introdução

Esta é a camada de inteligência artificial do repositório. Mesmo que você nunca tenha trabalhado com IA antes, a leitura a seguir mostra o que existe, como está organizado e como você pode começar a usar.

Exemplos práticos do que você pode pedir ao assistente:

- *"Analise este diretório e me diga quais são os pontos de risco de segurança."*
- *"Crie um plano de implementação para adicionar um novo campo no formulário X."*
- *"Revise o código que acabei de escrever e verifique se segue os padrões do projeto."*

Prompts prontos para adaptar e enviar estão em [`prompts-exemplo.md`](prompts-exemplo.md).

---

### Filosofia e origem da stack

A stack foi construída sobre um padrão aberto adotado por comunidades de desenvolvimento ao redor do mundo: o [AGENTS.md](https://agents.md). Esse padrão, hoje mantido pela Agentic AI Foundation sob a Linux Foundation e presente em mais de 60 mil projetos de código aberto (projetos cujo código-fonte é público e pode ser inspecionado por qualquer pessoa), propõe uma separação clara entre o que é escrito para humanos e o que é escrito para agentes de IA:

- **README.md**: para humanos (visão geral, contexto, como começar)
- **AGENTS.md**: para agentes (regras de codificação, restrições, padrões do projeto)

Ao seguir esse padrão, a stack se torna **agnóstica de ferramenta**: qualquer assistente de IA que respeite o `AGENTS.md` consegue trabalhar no repositório sem configuração adicional. O projeto não fica preso a uma ferramenta específica, e o contexto viaja junto com o código.

Ferramentas como GitHub Copilot, OpenCode e outras da comunidade já seguem esse padrão nativamente. Isso significa que o investimento feito na stack funciona independentemente de qual ferramenta cada pessoa escolher usar.

> **Origem da convenção:** o `AGENTS.md` é estruturado com base na convenção publicada em [agents.md](https://agents.md). O padrão não possui versionamento formal; a referência de atualização é o próprio site.

O arquivo `CLAUDE.md` existe apenas como ponteiro de compatibilidade para o `AGENTS.md`.

---

### O que são modelos de IA

Um **modelo de IA** é o "cérebro" por trás do assistente: o sistema que entende o que você escreve e gera respostas. Modelos conhecidos incluem Claude, GPT e outros modelos compatíveis com ferramentas de desenvolvimento.

Os modelos são acessados por meio de ferramentas já integradas ao fluxo de trabalho. Você não precisa acessar o modelo diretamente; a ferramenta faz isso por você.

| Ferramenta | Modelo / Provedor |
|---|---|
| GitHub Copilot | GPT ou Claude, dependendo do plano da conta |
| OpenCode | Configurável, compatível com múltiplos modelos |
| Claude Code | Modelo Claude (Anthropic) |

Os modelos evoluem com frequência. O que importa para o uso do dia a dia é a **ferramenta**; o modelo é apenas o motor por baixo.

---

### O que são agentes de IA

Um **agente de IA** é um assistente configurado para operar com um conjunto específico de instruções, contexto e regras. Diferente de um modelo genérico que você acessa pelo navegador, um agente:

- Conhece o projeto em que está trabalhando
- Segue **guardrails** (regras que definem o que ele pode e não pode fazer, como quais arquivos pode modificar e quais padrões de código deve seguir)
- Segue um fluxo estruturado em vez de responder de forma livre

Os agentes são configurados na pasta `.agents/` e integrados às ferramentas via `.github/` (Copilot), `.opencode/` (OpenCode) e `.claude/` (Claude Code). Eles não são programas independentes; são instruções que ensinam a ferramenta de IA a agir como especialista no contexto deste projeto.

**Na prática:** quando você abre o repositório no VS Code (editor de código da Microsoft) com o Copilot e pede *"revise este código segundo os padrões do projeto"*, o agente carrega automaticamente as regras do `AGENTS.md`, os guardrails de segurança e os padrões de codificação, e entrega uma revisão contextualizada, não genérica.

#### Skills: agentes especializados

As **skills** são agentes especializados em tarefas específicas. Cada skill tem um escopo bem definido. Para acionar uma skill, mencione o nome dela na conversa com o assistente (no painel de chat da ferramenta de IA, como o chat do Copilot no VS Code). Por exemplo: *"Use a skill `skill-creator` para criar uma skill de X."* O assistente carrega as instruções da skill e executa o processo correspondente.

As skills ficam em `.agents/skills/`, uma pasta por skill, distribuídas em três grupos:

| Grupo de skills | Onde estão descritas |
|---|---|
| Fases do SpecKit, com prefixo `speckit-` | Seção [Fases do SpecKit](#fases-do-speckit) deste documento |
| Demais skills de terceiros | Tabela de skills de terceiros, logo abaixo |
| Skills criadas pela equipe do projeto | Tabela de skills do projeto, mais abaixo |

As skills de terceiros trazem a versão que está em `.agents/skills/` hoje. Essa versão não se atualiza sozinha: a troca é coordenada pela equipe conforme [`manutencao-da-stack.md`](manutencao-da-stack.md).

| Skill | O que faz | Versão instalada | Licença | Repositório |
|---|---|---|---|---|
| `speckit-<fase>`, uma por fase | Conduzem as fases do fluxo SDD com SpecKit | v1.0.3 | MIT | [github/spec-kit](https://github.com/github/spec-kit) |
| `skill-creator` | Cria, edita e avalia skills | sem versionamento na origem | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| `docx` | Cria, lê, edita e manipula documentos Word (`.docx`, `.dotx`), inclusive controle de alterações e comentários | sem versionamento na origem | Proprietária da Anthropic, termos em `LICENSE.txt` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/docx) |
| `pdf` | Lê, extrai texto e tabelas, junta, divide, preenche formulários e aplica OCR em PDF | sem versionamento na origem | Proprietária da Anthropic, termos em `LICENSE.txt` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pdf) |
| `pptx` | Cria, lê e edita apresentações (`.pptx`, `.potx`), incluindo layouts, notas e comentários | sem versionamento na origem | Proprietária da Anthropic, termos em `LICENSE.txt` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pptx) |
| `xlsx` | Cria, lê, edita e converte planilhas (`.xlsx`, `.xlsm`, `.csv`, `.tsv`), com fórmulas, formatação e gráficos | sem versionamento na origem | Proprietária da Anthropic, termos em `LICENSE.txt` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/xlsx) |
| `frontend-design` | Orienta direção visual, tipografia e escolhas de design ao construir ou refazer interface | sem versionamento na origem | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) |
| `dicionario-dados-db-scan-codebase-docs` | Cria, atualiza e verifica dicionários de dados e changelogs estruturais de banco de dados a partir da codebase, dos scripts de banco e da documentação | sem versionamento na origem | GPL-3.0 | Repositório interno `ai-skills` |
| `gauntlet-loop-forge` | Transforma um objetivo, plano, especificação ou prompt existente em um prompt de execução pronto para colar, com critérios de aceite verificáveis, revisão por agente que não construiu o artefato e limite finito de rodadas | sem versionamento na origem | GPL-3.0 | Repositório interno `ai-skills` |
| `caveman` | Comprime a prosa da resposta preservando termo técnico, código e mensagem de erro | v1.9.0 | MIT | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
| `grill-me` e `grilling` | Entrevistam o desenvolvedor sobre um plano ou design, em rodadas de perguntas com resposta recomendada, antes de implementar | v1.2.3 | MIT | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) |
| `writing-for-agents` | Orienta a escrita de documento que agente de IA lê: skill, `AGENTS.md`, `CLAUDE.md` e arquivo alcançado por ponteiro de contexto | v1.2.3 | MIT | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) |
| `owasp-playbook` | Revisão de segurança por procedimento OWASP: 16 plays cobrindo código, Top 10, API, segredos, dependências, agente de IA, servidor MCP e aplicação LLM, com templates de achado e de relatório | v0.2.7 | CC-BY-4.0 no playbook e CC-BY-SA-4.0 nos dados OWASP | [OWASP/secure-agent-playbook](https://github.com/OWASP/secure-agent-playbook) |
| `napkin` | Mantém runbook operacional pessoal em `.agents/memory/runbook.md` | v6.1.0 | MIT | [blader/napkin](https://github.com/blader/napkin) |

A pasta `upstream/` da `owasp-playbook` é cópia literal do projeto de origem e **não deve ser editada**. A atualização é substituição da pasta inteira, e editar o conteúdo cria obra derivada, o que aciona a cláusula ShareAlike que cobre os dados OWASP. Ajuste específico do projeto fica fora de `upstream/`. O procedimento de atualização está em [`manutencao-da-stack.md`](manutencao-da-stack.md#como-atualizar-o-owasp-secure-agent-playbook).

A `owasp-playbook` é **opt-in por regra**: ela roda quando você pede ou quando outra skill precisa do procedimento, nunca por roteamento automático. Para pedir, basta uma frase em português, sem conhecer segurança: a skill escolhe os procedimentos pelo que há no escopo, roda os auditores que o SEI registrou na ponte e responde com um resumo em linguagem simples antes da tabela técnica. A skill é agnóstica; o que é do SEI está em `.agents/security/mapa-seguranca-cwe-sei.md`. O playbook não cobre PHP, então a revisão de módulo SEI usa junto o mapa `.agents/security/mapa-seguranca-cwe-sei.md`, que é do projeto.

A skill `caveman` é um **modo opcional**: o agente nunca a aciona sozinho, e ela só entra se você invocar. O uso dela está em [`prompts-exemplo.md`](prompts-exemplo.md), na seção de modos auxiliares.

As skills do projeto nascem neste repositório e são versionadas junto com ele:

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
| `sei-validacao-padrao` | Centraliza checagens e validações após alterações PHP |
| `sei-tipagem-phpdoc` | Apoia modernização segura de tipagem PHP e PHPDoc quando solicitada explicitamente |
| `sei-report-todos` | Gera relatório de pendências `TODO:` em módulos escolhidos explicitamente |
| `sei-revisao-tecnica` | Revisa diretamente segurança, conformidade, gates e qualidade técnica de diffs, arquivos ou módulos SEI, sem exigir spec |

Use `sei-revisao-tecnica` diretamente para revisão técnica, security review, compliance, gates ou módulo SEI, inclusive sobre worktree ou diff fornecido. Os aliases históricos são resolvidos textualmente conforme a matriz de roteamento em [`.agents/references/roteamento-de-skills.md`](../../.agents/references/roteamento-de-skills.md).

> **Glossário rápido:** CRUD = conjunto de operações de criar, ler, atualizar e deletar registros. Script de release = arquivo executado na instalação ou atualização do módulo no servidor.

---

### O que é SDD

**[SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)** (Specification-Driven Development, ou Desenvolvimento Orientado por Especificação) é uma abordagem de trabalho que coloca a especificação antes da implementação.

A ideia central é simples: antes de escrever código (implementar = traduzir uma necessidade em instruções que o computador executa), você produz uma descrição clara e estruturada do que precisa ser feito, e o agente de IA parte sempre dessa descrição. Isso evita o problema mais comum no uso de IA para código: pedir para implementar algo sem ter definido direito o que é esse "algo". Com SDD, o raciocínio vem antes da implementação.

Neste repositório, o SDD é implementado pelo framework **SpecKit**, descrito na seção [O que é o SpecKit](#o-que-é-o-speckit). O fluxo completo vai de `especificar → clarificar → planejar → decompor → implementar`.

---

### Ferramentas de IA suportadas

O repositório é **agnóstico de ferramenta**: você pode usar qualquer assistente de IA, desde que ele consiga ler o contexto do repositório (especialmente `.agents/skills/` e `AGENTS.md`).

A ferramenta **recomendada** é a extensão do **GitHub Copilot no [VS Code](https://code.visualstudio.com)** (editor de código gratuito da Microsoft), por ser a mais simples de configurar.

| Ferramenta | Como instalar | Arquivos de configuração |
|---|---|---|
| **[GitHub Copilot](https://github.com/features/copilot)** | Instale a extensão "GitHub Copilot" pelo marketplace do VS Code (a loja de extensões do editor, equivalente a uma loja de aplicativos) e faça login com sua conta GitHub | `.github/copilot-instructions.md` e `.vscode/settings.json` |
| **[OpenCode](https://opencode.ai)** | Instale via terminal (a interface de texto do computador onde você digita comandos) com `npm install -g opencode-ai` e configure o modelo desejado | `.opencode/opencode.json` |
| **[Claude Code](https://claude.com/claude-code)** | Instale via terminal com `curl -fsSL https://claude.ai/install.sh \| bash` e faça login com sua conta Claude | `.claude-plugin/marketplace.json` e `.claude/settings.json` |

> **Primeira vez no Claude Code?** As skills aparecem a partir da segunda sessão. A primeira abertura na pasta registra o plugin da stack, e a seguinte já carrega as skills. Se você abriu e não viu nenhuma, feche e abra de novo. Não é preciso rodar nenhum comando.

> **O que é npm?** É o gerenciador de pacotes do Node.js, uma ferramenta de linha de comando usada para instalar softwares de desenvolvimento. Se você nunca usou, peça ajuda a um desenvolvedor da equipe para instalar o OpenCode.

Se você optar por uma ferramenta diferente das listadas acima, confirme antes que ela consegue ler `.agents/skills/` e seguir as instruções do `AGENTS.md`.

---

### O que é o SpecKit

> **Não é necessário instalar o SpecKit.** Toda a estrutura já está presente no repositório. O único requisito é ter uma das ferramentas listadas em [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas) instalada e configurada.

**SpecKit** é o framework de especificação que estrutura o fluxo SDD no repositório. Ele divide o trabalho em fases sequenciais e produz documentos padronizados (especificação, plano técnico e lista de tarefas) que servem de contexto para a implementação.

O SpecKit é o ponto de partida do SDD por algumas razões práticas: é de fácil adoção para equipes que estão começando a introduzir especificação no fluxo de desenvolvimento, tem integração direta com o GitHub Copilot e conta com uma comunidade ativa que mantém o framework atualizado. Isso reduz o risco de depender de algo que ficará sem suporte.

> **Não substitua os arquivos do SpecKit por conta própria.** Se houver uma nova versão disponível, a atualização deve ser coordenada pela equipe seguindo o processo de [`manutencao-da-stack.md`](manutencao-da-stack.md). Substituir os arquivos sem revisão pode quebrar o fluxo para todas as ferramentas integradas.

> **Versão do template:** a estrutura instalada foi gerada a partir do **Template Version 1.0.3**. Consulte essa versão como referência ao comparar ou atualizar os arquivos em `.specify/`.

#### Quando usar o SpecKit

Use o SpecKit quando a demanda for **maior, nova ou ambígua**, quando você sente que precisa pensar antes de implementar.

Para correções pontuais e pequenas alterações, o fluxo direto (conversa com o agente) é suficiente. Linha de corte prática: se a mudança cabe em uma frase e não cria tela, permissão ou fluxo novos, não precisa de SpecKit.

#### Fases do SpecKit

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

#### Como invocar as fases

| Ferramenta | Como invocar |
|---|---|
| GitHub Copilot (VS Code) | Abra o painel de chat do Copilot (ícone de balão de conversa na barra lateral esquerda), clique no nome do agente atual (geralmente `@GitHub Copilot` ou `@workspace`, acima da caixa de texto) e selecione a skill, como `speckit-specify` |
| OpenCode (terminal) | Digite o comando diretamente, como `/speckit-specify` |
| Claude Code (terminal ou app) | Digite o comando diretamente, como `/speckit-specify` |

O nome do comando sai do diretório da skill, então ele é o mesmo nas três ferramentas, sempre com hífen: `/speckit-specify`, `/speckit-plan`.

#### Como cada ferramenta encontra as fases

O fluxo de cada fase existe uma vez só, em `.agents/skills/speckit-<fase>/SKILL.md`. Nenhuma ferramenta guarda uma cópia.

As três leem `.agents/skills/` direto e encontram as fases lá, lado a lado com as demais skills, sem symlink e sem cópia. Cada uma chega por um caminho de configuração próprio:

| Ferramenta | Caminho de configuração |
|---|---|
| Claude Code | Plugin local `stack-ai`, do marketplace local do repositório, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json` |
| GitHub Copilot | Chave `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | Chave `skills.paths` em `.opencode/opencode.json` |

Isso funciona porque a descoberta de skill procura um nível abaixo do diretório configurado, no formato `<local>/<nome>/SKILL.md`, e as fases ficam exatamente nesse nível.

Nenhuma das três precisa de arquivo de comando. Se o repositório tiver pastas de comando vazias, como `.claude/commands/`, `.github/prompts/` ou `.opencode/command/`, elas são convenção da ferramenta e não precisam de conteúdo. Não crie arquivo de comando para expor uma fase.

#### Onde ficam os documentos gerados

Os documentos gerados (especificação, plano, tarefas) ficam em `specs/<nome-da-funcionalidade>/`, na sua máquina.

A pasta `specs/` está no `.gitignore`: os documentos ficam somente na sua máquina e nunca são enviados ao repositório compartilhado. Isso é intencional, porque esses arquivos são descartáveis e existem apenas para guiar aquela entrega específica.

Os scripts que as fases executam ficam em `.specify/scripts/`, em duas versões equivalentes: `bash/` para Linux, macOS e WSL, e `powershell/` para Windows. Cada fase escolhe a versão certa conforme o shell da sessão.

---

### Estrutura da stack

```text
.agents/
├── checklists/    # Checklists modulares de validação técnica (BD, DTO, RN, permissões, segurança)
├── decisions/     # Registros de decisões arquiteturais: o porquê de escolhas técnicas importantes
├── memory/        # Contexto operacional reutilizável entre sessões (ex: runbooks e guias rápidos)
├── references/    # Material de referência consultado pelas skills: padrões, roteamento e pontos de verificação
├── security/      # Guias e matrizes de revisão de segurança
└── skills/        # As skills: agentes especializados por domínio ou tipo de tarefa

.claude/
└── settings.json  # Registra o marketplace do repositório e liga o plugin stack-ai

.claude-plugin/
└── marketplace.json  # Plugin local stack-ai; é assim que o Claude Code enxerga as skills

.github/
└── copilot-instructions.md  # Instruções curtas carregadas pelo Copilot

.opencode/
└── opencode.json  # Configuração do OpenCode para o repositório

.specify/
├── integrations/  # Manifestos de integração do SpecKit por ferramenta
├── memory/        # Contém o constitution.md do SpecKit, mantido intencionalmente vazio
├── scripts/       # Scripts chamados pelas skills em tempo de execução (ex: criação de branch)
├── templates/     # Templates de origem do SpecKit, base de comparação para atualizações
└── workflows/     # Registro de workflows do SpecKit

.vscode/
└── settings.json  # Aponta o Copilot para .agents/skills/

docs/stack_ai/     # Esta documentação
specs/             # Documentos gerados pelo SpecKit por funcionalidade (somente na sua máquina)
AGENTS.md          # Regras do projeto para agentes de IA (leia antes de contribuir)
CLAUDE.md          # Ponteiro de compatibilidade para AGENTS.md
```

As pastas que começam com ponto são pastas de configuração. Elas não contêm código da aplicação, e sim as instruções e ferramentas que orientam o trabalho dos agentes de IA.

**O que cada pasta de `.agents/` faz na prática:**

- `checklists/`: checklists modulares de validação técnica por camada (BD, DTO, RN, permissões, segurança). Consultados pela skill `sei-revisao-tecnica` e usados manualmente antes do merge.
- `decisions/`: registra o porquê de decisões técnicas importantes, como por que uma tabela foi modelada de determinada forma. Consulte antes de propor mudanças arquiteturais.
- `memory/`: guarda contexto operacional reutilizável entre sessões de trabalho. O `runbook.md` dessa pasta é pessoal de cada desenvolvedor e não é versionado.
- `references/`: material base consultado pelas skills: padrões de codificação, roteamento de demandas e pontos de verificação obrigatórios.
- `security/`: guias e matrizes de revisão de segurança do código, consultados pela skill `sei-revisao-tecnica`.
- `skills/`: as skills, uma pasta por skill, cada uma com escopo e instruções próprias.

A pasta `specs/` não vem na instalação: ela é criada na primeira vez que uma fase do SpecKit rodar, e guarda os documentos gerados para cada funcionalidade.

**Arquivos e pastas no `.gitignore`**

Alguns itens existem apenas localmente em cada máquina e estão listados no `.gitignore` para não serem versionados. Eles devem permanecer assim:

| Item | Por que não é versionado |
|---|---|
| `specs/` | Documentos gerados pelo SpecKit para cada funcionalidade; são locais e descartáveis |
| `.agents/memory/runbook.md` | Runbook pessoal de cada desenvolvedor, mantido localmente pela skill `napkin` |
| `.claude/settings.local.json` | Configuração local do Claude Code, diferente em cada máquina |
| `.specify/feature.json`, `.specify/init-options.json` e `.specify/integration.json` | Configuração local do SpecKit, por desenvolvedor e por ferramenta |
| `node_modules/` | Dependências instaladas pelo npm; nunca devem ser salvas no repositório |
| `.env*` | Arquivos de configuração com dados sensíveis como senhas e chaves de acesso |

Antes de remover qualquer item do `.gitignore`, avalie se a remoção é realmente necessária. Na dúvida, mantenha.

---

### Como começar com a stack de IA

**Passo 1: Baixe o repositório.** Faça o clone do repositório (baixe uma cópia local usando Git) e abra a pasta raiz no VS Code.

**Passo 2: Instale uma ferramenta.** A recomendada é a extensão GitHub Copilot no VS Code. Abra o VS Code, clique no ícone de extensões na barra lateral (quatro quadradinhos), pesquise "GitHub Copilot" e clique em instalar. Depois faça login com sua conta GitHub. O Copilot detecta automaticamente os arquivos de configuração do projeto: ao abrir a pasta, ele lê o `AGENTS.md` e as pastas `.github/` e `.agents/`, carregando as regras e os agentes do projeto sem nenhuma ação adicional sua.

**Passo 3: Para uma demanda simples,** abra o chat da ferramenta e descreva o que precisa. Exemplo:

> *"Analise o diretório X sem alterar nada. Quero entender como essa parte funciona."*

**Passo 4: Para uma demanda maior ou ambígua,** use o fluxo SpecKit, começando por `/speckit-specify`. Leia antes a seção [O que é o SpecKit](#o-que-é-o-speckit).

**Passo 5: Consulte os exemplos** em [`prompts-exemplo.md`](prompts-exemplo.md) para ver como formular bons pedidos para diferentes tipos de demanda.

Você **não** precisa instalar o SpecKit nem qualquer componente adicional da stack. Tudo já está configurado no repositório. O único passo é instalar a ferramenta de IA.

---

## Atualizações da stack

A manutenção da stack tem documento próprio: [`manutencao-da-stack.md`](manutencao-da-stack.md). Ele cobre como o SpecKit está organizado, o mapa de atualização, como atualizar o SpecKit, como atualizar a skill `owasp-playbook` e como atualizar os demais arquivos da stack.

Não substitua arquivos da stack por conta própria. A atualização é coordenada pela equipe, em branch dedicada e com Pull Request para revisão.

---

## Referências

**Documentação interna do projeto:**

| Documento | O que contém |
|---|---|
| [`AGENTS.md`](../../AGENTS.md) | Regras centrais do projeto para agentes: o que pode ser feito, padrões de código e regras de decisão |
| [`prompts-exemplo.md`](prompts-exemplo.md) | Prompts prontos para as demandas reais: bug, fluxo SpecKit, ajuste pontual, revisão técnica, dicionário de dados e modos auxiliares |
| [`manutencao-da-stack.md`](manutencao-da-stack.md) | Manutenção da stack: organização do SpecKit, mapa de atualização e procedimentos de atualização do SpecKit e da skill `owasp-playbook` |
| [`docs/manual_desenvolvimento_md/`](../manual_desenvolvimento_md/) | Manual oficial de desenvolvimento de módulos SEI |
| [`docs/dicionario_dados/`](../dicionario_dados/) | Dicionário de dados por módulo (uma pasta por módulo: SEI, SIP, Litigioso, ...) |
| [`.agents/references/roteamento-de-skills.md`](../../.agents/references/roteamento-de-skills.md) | Qual skill usar para cada tipo de demanda |
| [`.agents/references/gates-de-implementacao.md`](../../.agents/references/gates-de-implementacao.md) | Pontos de verificação obrigatórios que impedem a implementação de avançar com problemas não resolvidos |

**Ferramentas e padrões externos:**

| Ferramenta / Padrão | Link |
|---|---|
| VS Code | [code.visualstudio.com](https://code.visualstudio.com) |
| GitHub Copilot | [github.com/features/copilot](https://github.com/features/copilot) |
| OpenCode | [opencode.ai](https://opencode.ai) |
| Claude Code | [claude.com/claude-code](https://claude.com/claude-code) |
| Git | [git-scm.com](https://git-scm.com) |
| SpecKit | [github.com/github/spec-kit](https://github.com/github/spec-kit) |
| Padrão AGENTS.md | [agents.md](https://agents.md) |
