# Referencias AppSec PHP

Curadoria de referencias externas aproveitadas para reforcar a revisao de seguranca
de codigo PHP do SEI. Este arquivo e complementar; nao substitui as regras locais
do repositorio.

## Como Esta Curadoria Foi Feita

- Nao importamos skill externa para execucao dentro deste repositorio.
- Nao copiamos skill inteira nem adotamos workflow externo como obrigatorio.
- Fizemos leitura manual de artefatos externos em Markdown (`SKILL.md` e
  `references/*.md`) e absorvemos apenas conceitos uteis ao contexto SEI/PHP.
- Cada fonte abaixo lista repo, path, tipo do artefato, o que foi absorvido e
  onde isso entrou na stack local.

## Fontes Externas Rastreaveis e Incorporadas

### 1. `github/awesome-copilot` — skill `security-review`

**Artefatos consultados**:
- repo: `github/awesome-copilot`
- tipo: `SKILL.md` + referencias Markdown da skill
- paths:
  - `skills/security-review/SKILL.md`
  - `skills/security-review/references/secret-patterns.md`
  - `skills/security-review/references/vuln-categories.md`
  - `skills/security-review/references/vulnerable-packages.md`
  - `skills/security-review/references/language-patterns.md`
  - `skills/security-review/references/report-format.md`

**O que foi absorvido**:
- analise por fluxo de dados, e nao so por heuristica solta
- verificacao de segredos hardcoded e exposicao acidental
- verificacao de dependencia vulneravel quando houver evidencia confiavel
- verificacao de aleatoriedade fraca
- exigencia de recomendacao objetiva e minima para cada achado relevante

**Onde isso entrou aqui**:
- `.agents/skills/sei-revisao-tecnica/SKILL.md`
  - secao `Procedimento obrigatorio`, com analise de fluxo de dados
  - secao `Formato do relatorio`, com consolidacao e ajuste objetivo
- `.agents/checklists/checklist-seguranca.md`
  - itens `C1`, `C2`, `C8`, `C9`, `C10`

**O que nao foi adotado**:
- severidade `CRITICAL/INFO` do modelo externo
- formato de patch proposto pela skill externa
- scanners e auditorias de dependencias como requisito obrigatorio

### 2. `github/awesome-copilot` — skill `audit-integrity`

**Artefatos consultados**:
- repo: `github/awesome-copilot`
- tipo: `SKILL.md` + referencias Markdown da skill
- paths:
  - `skills/audit-integrity/SKILL.md`
  - `skills/audit-integrity/references/anti-rationalization-guard.md`
  - `skills/audit-integrity/references/self-critique-loop.md`
  - `skills/audit-integrity/references/non-negotiable-behaviors.md`
  - `skills/audit-integrity/references/clarification-protocol.md`
  - `skills/audit-integrity/references/retry-protocol.md`
  - `skills/audit-integrity/references/self-reflection-quality-gate.md`

**O que foi absorvido**:
- segunda passada obrigatoria antes do veredito
- disciplina anti-racionalizacao para derrubar falso positivo
- exigencia de evidencia tecnica antes de classificar severidade alta ou bloqueante
- postura explicita de nao inventar achado nem esconder incerteza

**Onde isso entrou aqui**:
- `.agents/skills/sei-revisao-tecnica/SKILL.md`
  - segunda passada obrigatoria
  - criterio de evidencia e ambiguidade
- `.agents/skills/sei-revisao-tecnica/SKILL.md`
  - secao `Segunda passada obrigatoria`
  - orientacao para separar fato, hipotese e risco residual

**O que nao foi adotado**:
- rubricas internas de nota `>= 8`
- sistema de memoria/licoes da skill externa como regra operacional daqui

### 3. `netresearch/security-audit-skill` — referencias PHP/AppSec

**Artefatos consultados**:
- repo: `netresearch/security-audit-skill`
- tipo: `SKILL.md` + referencias Markdown por tema
- paths principais:
  - `skills/security-audit/SKILL.md`
  - `skills/security-audit/references/php-security-features.md`
  - `skills/security-audit/references/input-validation.md`
  - `skills/security-audit/references/file-upload-security.md`
  - `skills/security-audit/references/path-traversal-prevention.md`
  - `skills/security-audit/references/deserialization-prevention.md`
  - `skills/security-audit/references/xxe-prevention.md`
  - `skills/security-audit/references/error-message-sanitization.md`
  - `skills/security-audit/references/security-logging.md`
  - `skills/security-audit/references/api-security.md`

**O que foi absorvido**:
- temas AppSec genericos de PHP que nao sao especificos do SEI
- reforco de validacao de entrada e normalizacao
- cuidado com upload, traversal, desserializacao e XXE
- cuidado com logging e sanitizacao de mensagens de erro

**Onde isso entrou aqui**:
- `.agents/checklists/checklist-seguranca.md`
  - itens `C3`, `C4`, `C5`, `C6`, `C7`, `C8`
  - notas anti-falso-positivo dos itens `C1-C10`
- `.agents/skills/sei-revisao-tecnica/SKILL.md`
  - secao `Dimensoes tecnicas`

**O que nao foi adotado**:
- checkpoints de stacks fora de PHP/SEI
- scans automatizados como obrigatorios
- padroes de cloud/IaC/LLM fora do escopo desta stack local

## Fontes Avaliadas, Mas Nao Usadas Como Base Primaria

### `Florian Bruniaux` — `security-checklist.md`

- Houve avaliacao manual de um checklist externo atribuido a Florian Bruniaux.
- A ideia aproveitada foi apenas a organizacao por dominio de risco.
- A origem exata em repo/path nao ficou rastreada com precisao suficiente na
  primeira rodada.
- Por rigor documental, esta fonte nao deve ser tratada como base primaria
  rastreavel ate que o artefato exato seja relocalizado e registrado.

## Temas Complementares Abertos por Esta Curadoria

- segredos e credenciais hardcoded
- execucao de comandos
- desserializacao insegura
- leitura, escrita, include ou require por caminho controlavel
- upload de arquivos
- XML/XXE
- SSRF e redirect inseguro
- aleatoriedade fraca
- dependencia vulneravel, quando houver evidencia disponivel
