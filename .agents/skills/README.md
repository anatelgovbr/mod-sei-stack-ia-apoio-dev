# Skills — Registro de Auditoria

Este documento é o registro de auditoria de todas as skills disponíveis no repositório: origem, versão, licença e composição.

---

## Índice

- [caveman](#caveman)
- [code-review](#code-review)
- [grill-me](#grill-me)
- [grilling](#grilling)
- [napkin](#napkin)
- [ponytail](#ponytail)
- [ponytail-audit](#ponytail-audit)
- [ponytail-debt](#ponytail-debt)
- [ponytail-gain](#ponytail-gain)
- [ponytail-help](#ponytail-help)
- [ponytail-review](#ponytail-review)
- [skill-creator](#skill-creator)
- [sei-revisao-tecnica](#sei-revisao-tecnica)
- [dicionario-dados-db-scan-codebase-docs](#dicionario-dados-db-scan-codebase-docs)
- [sei-direcionador-integracao](#sei-direcionador-integracao)
- [sei-gerador-crud](#sei-gerador-crud)
- [sei-gerador-scripts-release](#sei-gerador-scripts-release)
- [sei-guardrails-modulo](#sei-guardrails-modulo)
- [sei-menu-pagina](#sei-menu-pagina)
- [sei-mod-api-classes](#sei-mod-api-classes)
- [sei-mod-api-eventos](#sei-mod-api-eventos)
- [sei-mod-api-operacoes](#sei-mod-api-operacoes)
- [sei-report-todos](#sei-report-todos)
- [sei-testes-validacao](#sei-testes-validacao)
- [sei-tipagem-phpdoc](#sei-tipagem-phpdoc)
- [sei-verificacao-banco-dados](#sei-verificacao-banco-dados)
- [sei-verificacao-controladores](#sei-verificacao-controladores)
- [sei-verificacao-pagina](#sei-verificacao-pagina)
- [sei-verificacao-rn](#sei-verificacao-rn)
- [sei-verificacao-tarefa](#sei-verificacao-tarefa)
- [sip-gerador-scripts-release](#sip-gerador-scripts-release)
- [speckit](#speckit)
- [speckit-analyze](#speckit-analyze)
- [speckit-checklist](#speckit-checklist)
- [speckit-clarify](#speckit-clarify)
- [speckit-constitution](#speckit-constitution)
- [speckit-implement](#speckit-implement)
- [speckit-plan](#speckit-plan)
- [speckit-specify](#speckit-specify)
- [speckit-tasks](#speckit-tasks)
- [speckit-taskstoissues](#speckit-taskstoissues)

---

## Tabela de Auditoria

| Skill | Tipo | Versão | Licença | Repositório |
|---|---|---|---|---|
| caveman | externa | v1.9.0 | MIT | github.com/JuliusBrussee/caveman |
| code-review | externa | commit `6a34259e99bc5fed4f8fe5da61c273dad14edf67` | MIT | github.com/mattpocock/skills |
| grill-me | externa | v1.0.1 | MIT | github.com/mattpocock/skills |
| grilling | externa | v1.0.1 | MIT | github.com/mattpocock/skills |
| napkin | externa | v6.1.0 | MIT | github.com/blader/napkin |
| ponytail | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-audit | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-debt | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-gain | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-help | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-review | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| skill-creator | externa | sem versionamento | Apache-2.0 | github.com/anthropics/skills |
| sei-revisao-tecnica | interna | N/A | N/A | N/A |
| dicionario-dados-db-scan-codebase-docs | interna | — | — | — |
| sei-direcionador-integracao | interna | — | — | — |
| sei-gerador-crud | interna | — | — | — |
| sei-gerador-scripts-release | interna | — | — | — |
| sei-guardrails-modulo | interna | — | — | — |
| sei-menu-pagina | interna | — | — | — |
| sei-mod-api-classes | interna | — | — | — |
| sei-mod-api-eventos | interna | — | — | — |
| sei-mod-api-operacoes | interna | — | — | — |
| sei-report-todos | interna | — | — | — |
| sei-testes-validacao | interna | — | — | — |
| sei-tipagem-phpdoc | interna | — | — | — |
| sei-verificacao-banco-dados | interna | — | — | — |
| sei-verificacao-controladores | interna | — | — | — |
| sei-verificacao-pagina | interna | — | — | — |
| sei-verificacao-rn | interna | — | — | — |
| sei-verificacao-tarefa | interna | — | — | — |
| sip-gerador-scripts-release | interna | — | — | — |
| speckit | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-analyze | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-checklist | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-clarify | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-constitution | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-implement | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-plan | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-specify | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-tasks | externa | v0.12.4 | MIT | github.com/github/spec-kit |
| speckit-taskstoissues | externa | v0.12.4 | MIT | github.com/github/spec-kit |

---

## caveman

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/JuliusBrussee/caveman — repositório autoritativo para rastreio de versão.
Também distribuída em https://github.com/mattpocock/skills/tree/main/skills/productivity.

**Versão instalada:** v1.9.0

**Licença:** MIT

**Alteração local:** Pequenos ajustes de idioma na descrição do frontmatter. Conteúdo das instruções preservado integralmente.

**Composição:**
- Seis níveis de intensidade: `lite`, `full` (padrão), `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`.
- Modo `full` elimina artigos, hedging e filler preservando todo conteúdo técnico.
- Modos `wenyan-*` comprimem no registro clássico chinês (文言文).
- Regra de auto-clareza: retorna à prosa normal em warnings destrutivos, sequências ambíguas ou confirmações de ação irreversível.
- Persiste na sessão até `stop caveman` ou `normal mode`.

**Como invocar:** `/caveman`, `/caveman lite`, `/caveman ultra`, `/caveman wenyan`

---

## code-review

> **Skill externa** mantida por terceiros, com adaptações locais para o fluxo SEI.

**Repositório:** https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review

**Commit instalado:** `6a34259e99bc5fed4f8fe5da61c273dad14edf67`

**Licença:** MIT

**Alterações locais:** Standards executa `sei-revisao-tecnica`. A avaliação de Spec foi desabilitada nesta versão. Toda a coordenação opera somente em leitura.

**Composição:**
- Revisa mudanças commitadas de branch ou PR desde um ponto fixo Git fornecido pelo desenvolvedor.
- Mantém somente Standards, executado por `sei-revisao-tecnica`.
- Não busca nem avalia spec, requisito ou issue nesta versão.
- Worktree sem commit usa revisão técnica direta ou um diff fornecido, fora deste fluxo.
- Preserva integralmente o parecer técnico emitido por `sei-revisao-tecnica`.

---

## grill-me

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/mattpocock/skills/tree/main/skills/productivity

**Versão instalada:** v1.0.1

**Licença:** MIT

**Composição:** Alias fino que delega para `grilling`.

**Como invocar:** `/grill-me`

---

## grilling

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/mattpocock/skills/tree/main/skills/productivity

**Versão instalada:** v1.0.1

**Licença:** MIT

**Composição:**
- Entrevista socrática sobre cada aspecto do plano ou design.
- Percorre cada galho da árvore de decisão resolvendo dependências uma a uma.
- Cada pergunta acompanha uma resposta recomendada.
- Perguntas são feitas uma por vez.
- Se uma pergunta puder ser respondida explorando o código, o agente explora o código em vez de perguntar.

**Como invocar:** `/grilling` ou `/grill-me`

---

## napkin

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/blader/napkin

**Versão instalada:** v6.1.0

**Licença:** MIT

**Alteração local:** O caminho do runbook foi movido para `.agents/memory/runbook.md` (marcado como `portable, any tool`), tornando a skill agnóstica de runtime.

**Composição:**
- Sempre ativa — sem trigger. Lê e cuida o runbook no início de cada sessão.
- Runbook vive em `.agents/memory/runbook.md`.
- Critério de inclusão: gotchas recorrentes, diretivas do usuário, táticas não óbvias que funcionam repetidamente.
- Critério de exclusão: notas cronológicas, postmortems sem ação concreta, logs de erro sem "Do instead".
- Máximo 10 itens por categoria; re-prioriza a cada leitura.

---

## ponytail

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Modo principal de codificação — ativo em toda resposta após invocação.
- Força solução mínima via ladder: YAGNI → reutilizar codebase → stdlib → feature nativa → dependência instalada → one-liner → apenas então escrever código novo.
- Três intensidades: `lite` (nomeia a alternativa mais simples), `full` (ladder completa, padrão), `ultra` (YAGNI extremista, desafia o requisito antes de construir).
- Marca simplificações deliberadas com comentário `ponytail: <teto>, <gatilho de upgrade>`.
- Nunca simplifica: validação de entrada, tratamento de erro que previne perda de dados, segurança, acessibilidade ou funcionalidade explicitamente solicitada.
- Desativar: `stop ponytail` / `normal mode`.

**Como invocar:** `/ponytail`, `/ponytail lite`, `/ponytail ultra`

---

## ponytail-audit

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Igual ao `ponytail-review`, mas varre o repositório inteiro em vez de um diff.
- Ranking por impacto: maior corte primeiro.
- One-shot — lista achados, não aplica.
- Tags: `delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`.

**Como invocar:** `/ponytail-audit`

---

## ponytail-debt

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Coleta todos os comentários `ponytail:` do repo em um ledger de dívida técnica.
- Comando: `grep -rnE '(#|//) ?ponytail:' .`
- Sinaliza entradas sem gatilho de upgrade com tag `no-trigger` (risco de rot silencioso).
- Fecha com `<N> markers, <M> with no trigger.` ou `No ponytail: debt. Clean ledger.`
- Pode persistir o ledger em `PONYTAIL-DEBT.md` se solicitado.

**Como invocar:** `/ponytail-debt`

---

## ponytail-gain

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Exibe scoreboard ASCII com medianas dos benchmarks publicados (5 tarefas × 3 modelos).
- Não calcula número por repositório — nunca inventa baseline de código que não foi escrito.
- One-shot; não altera modo nem persiste estado.

**Como invocar:** `/ponytail-gain`

---

## ponytail-help

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Cartão de referência rápida: todos os modos, skills e comandos ponytail.
- One-shot; não altera modo.

**Como invocar:** `/ponytail-help`

---

## ponytail-review

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Review focado **exclusivamente** em over-engineering — não avalia correção, segurança ou performance.
- Tags: `delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`.
- Um achado por linha: `L<n>: <tag> <o que cortar>. <substituto>.`
- Fecha com `net: -<N> lines possible.` ou `Lean already. Ship.`
- Complementa `code-review` e `sei-revisao-tecnica` sem sobreposição de escopo.

**Como invocar:** `/ponytail-review`

---

## skill-creator

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/anthropics/skills/tree/main/skills/skill-creator — estrutura de arquivos (`agents/`, `assets/`, `eval-viewer/`, `references/`, `scripts/`, `LICENSE.txt`, `SKILL.md`) confere com a instalação local.

**Versão instalada:** sem versionamento formal — o repositório de origem não publica tags nem releases.

**Origem:** Anthropic, PBC (copyright em `LICENSE.txt`).

**Licença:** Apache License 2.0

**Composição:**
- Fluxo completo para criar, testar e iterar skills: captura de intenção, entrevista, escrita do `SKILL.md`, casos de teste, avaliação qualitativa e quantitativa via `eval-viewer/generate_review.py`, e otimização de descrição via `scripts/run_loop.py`.
- Progressive disclosure: metadata (nome + descrição, sempre em contexto) → corpo do `SKILL.md` (ao disparar) → recursos em `scripts/`, `references/`, `assets/` (sob demanda).
- Subagentes dedicados em `agents/`: `grader.md` (avalia asserções), `comparator.md` (comparação cega A/B), `analyzer.md` (analisa por que uma versão venceu).
- Empacotamento final via `scripts/package_skill.py`, gerando arquivo `.skill` instalável.
- Instruções alternativas para Claude.ai e Cowork quando subagentes ou navegador não estão disponíveis.

**Fontes:**
- `LICENSE.txt` (Apache License 2.0, Copyright 2026 Anthropic, PBC)

---

## sei-revisao-tecnica

**Origem:** Skill interna orquestradora de revisão técnica, security review e conformidade SEI, distinta da comparação funcional executada por `code-review`.

**Composição:**
- Aceita diff, PR, branch, commit, tag, arquivos, dimensão técnica ou módulo SEI completo sem exigir spec.
- Aciona gates por artefato: `sei-verificacao-pagina` (P1-P10), `sei-verificacao-rn` (T1-T6/A1-A3), `sei-verificacao-banco-dados` (DB01-DB15), `sei-verificacao-controladores` (CI1-CI5), `sei-verificacao-tarefa` (K1-K4/K6-K7) e `sei-testes-validacao` quando aplicável.
- Aplica matriz de vulnerabilidades V01-V10, checklist de segurança C1-C10 e rastreabilidade OWASP quando houver relação aplicável.
- Avalia doze dimensões técnicas, classifica achados como `introduzido`, `ampliado`, `preexistente` ou `incerto` e exige cobertura positiva para `PASS`.
- Executa segunda passada para reduzir falsos positivos e produz candidatos a tarefas sem persistir relatório, tarefa ou issue.
- Emite somente parecer técnico: `apto tecnicamente`, `apto com ajustes`, `bloquear tecnicamente` ou `analise humana`.
- Não avalia requisito, especificação, regra de negócio ou produto e nunca chama `code-review`.

**Fontes:**
- `AGENTS.md`
- `.agents/references/roteamento-de-skills.md`
- `.agents/references/gates-de-implementacao.md`
- `.agents/security/matriz-vulnerabilidades-sei.md`
- `.agents/security/mapeamento-owasp-sei.md`
- `.agents/checklists/checklist-seguranca.md`
- `.agents/skills/sei-revisao-tecnica/references/reutilizacao-rn-int-dto.md`
- `.agents/security/origem-referencias-seguranca.md`

---

## dicionario-dados-db-scan-codebase-docs

**Origem:** Skill interna para criar, atualizar e verificar documentação de dados a partir de evidências versionadas de uma codebase.

**Composição:**
- Infere o alvo a partir do pedido e da codebase; opera quando há adaptador compatível em `registro-adaptadores.md`, na raiz da skill. Sem adaptador, dispara um protocolo que pede as informações necessárias em vez de presumir convenção.
- Núcleo genérico (`references/`) trata evidência, confiança, formato e fórmulas obrigatórias de descrição sem depender de linguagem, framework ou estrutura de projeto; todo conhecimento específico do SEI, SIP, Julgar e InfraPHP fica isolado em `adapters/sei/`.
- Materiais fornecidos pelo desenvolvedor são evidência complementar opcional; nunca substituem a busca e comparação obrigatórias com a codebase.
- Cria, atualiza ou verifica `dicionario_tabelas.md`, `dicionario_colunas.md`, `CHANGELOG.md` e relatório de atualização em `specs/`, conforme a intenção inferida e limitado ao alcance estrutural comprovado pelo adaptador.
- Princípios de ISO 8000-1, ISO/IEC 25012, ISO/IEC 25024, ISO/IEC 11179-3 e ISO/IEC 11179-4 convertidos em critérios de aceitação A1 a A10; não é declaração de conformidade.
- Verificador `scripts/verificar_dicionario.py` com os subcomandos `formato`, `tabelas-colunas`, `changelog` e `diff`, coberto por 61 testes `unittest`.

**Fontes:**
- `AGENTS.md`
- `.agents/skills/dicionario-dados-db-scan-codebase-docs/references/` (núcleo e contrato)
- `.agents/skills/dicionario-dados-db-scan-codebase-docs/adapters/sei/` (adaptadores InfraPHP e localização dos alvos)
- `.agents/skills/dicionario-dados-db-scan-codebase-docs/adapters/sei/modulos/` (overlays exclusivos de módulos)
- `.agents/references/mapa-modulos-scripts.md`
- `specs/pesquisa-padrao-mercado-dicionario-de-dados.md` (ressalva sobre ISO/IEC 11179-4)

---

## sei-direcionador-integracao

**Origem:** Skill mediadora interna criada para resolver a ambiguidade entre os três caminhos de integração do core SEI: contrato API, hook de evento e operação via SeiRN.

**Composição:**
- Recebe intenção textual do desenvolvedor.
- Consulta os três catálogos: `.agents/skills/sei-mod-api-classes/references/catalogo-api.md`, `.agents/skills/sei-mod-api-eventos/references/catalogo-eventos.md`, `.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md`.
- Apresenta até 3 opções com contexto e aguarda escolha do desenvolvedor.
- Encaminha para a skill correta: `sei-mod-api-classes`, `sei-mod-api-eventos` ou `sei-mod-api-operacoes`.
- Não tem catálogo próprio; não implementa; não roteia sem confirmação.

---

## sei-gerador-crud

**Origem:** Skill interna criada para automatizar a geração dos 6 artefatos CRUD InfraPHP a partir de um contrato JSON, seguindo o padrão estrutural TRF4 documentado no manual oficial de desenvolvimento SEI.

**Composição:**
- Três caminhos: documentação disponível (A), descrição em linguagem natural (B), JSON pronto (C).
- Motor: `generate_from_contrato.py` + templates `templates/*.tpl`.
- Referência estrutural: `.agents/skills/sei-gerador-crud/references/gabarito-trf4.md` (padrão TRF4 — não usado como template literal).
- Gates pós-geração: permissão/link assinado, `PaginaSEI::tratarHTML`, validação de lista N:N, helpers INT, validadores RN.
- Fase de Release integrada quando o módulo está mapeado.

**Fontes:**
- Manual SEI — cap. 3, 4 e 5
- `.agents/skills/sei-gerador-crud/references/gabarito-trf4.md`
- `.agents/skills/sei-gerador-crud/references/padroes-sei.md`
- `.agents/references/padrao-modelagem-dados.md`
- `.agents/references/padrao-codificacao-php.md`
- `.agents/skills/sei-gerador-crud/references/mapeamento-tipos-e-widgets.md`

---

## sei-gerador-scripts-release

**Origem:** Skill interna para padronizar a geração e atualização de scripts de release do lado SEI (`fontes/sei/src/main/php/sei/scripts/*`).

**Composição:**
- Padrão primário: `sei_atualizar_versao_modulo_ia.php`.
- Estrutura obrigatória: `*AtualizadorSeiRN extends InfraRN`, `atualizarVersaoConectado()`, `switch` com fallthrough, métodos `instalarv*()`, bootstrap final com `InfraScriptVersao::solicitarAutenticacao()`.
- DDL multi-SGBD via `InfraMetaBD::tipo*()`.
- Sincroniza `getVersao()` em `*Integracao.php`.
- Validação: `php -l` + `sei-verificacao-banco-dados` em modo `release_check`.

**Fontes:**
- `.agents/references/padrao-modelagem-dados.md`
- `.agents/skills/sei-gerador-scripts-release/references/sei-update-script-rules.md`
- Scripts de referência no repositório

---

## sei-guardrails-modulo

**Origem:** Skill interna para centralizar os guardrails obrigatórios do manual de desenvolvimento SEI/SIP antes e durante a implementação de qualquer módulo.

**Composição:**
- Verifica scripts de instalação existentes contra `.agents/references/mapa-modulos-scripts.md`.
- Guarda de assets: impede criação de novos CSS/JS quando já existem.
- Identifica pontos de impacto: menu/página, eventos, botões, operações, BD.
- Garante base obrigatória: link assinado, permissão, transação, auditoria.
- Aciona skills especializadas conforme artefatos presentes.

**Fontes:**
- `AGENTS.md`
- `.agents/security/matriz-vulnerabilidades-sei.md`
- `.agents/references/padrao-codificacao-php.md`

---

## sei-menu-pagina

**Origem:** Skill interna criada a partir das regras de configuração de menu interno via SIP documentadas no manual SEI.

**Composição:**
- Decide origem do menu: interno via SIP ou externo/publicações via hook (`sei-mod-api-eventos`).
- Implementa recurso SIP, validação de permissão e link assinado.
- Ícone de menu via evento `obterDiretorioIconesMenu` + SVG.
- Escopo limitado a menu interno, página e ação do módulo.

**Fontes:**
- `.agents/skills/sei-menu-pagina/references/sip-recursos-menus-perfis.md`
- `AGENTS.md`
- `.agents/references/padrao-auditoria-sip-sei.md`

---

## sei-mod-api-classes

**Origem:** Skill interna criada a partir do capítulo 8 do manual oficial SEI — classes `Entrada*API`, `Saida*API` e `*API` do core.

**Composição:**
- Localiza e confirma o contrato API oficial antes de propor acesso interno.
- Fonte primária: `.agents/skills/sei-mod-api-classes/references/catalogo-api.md`.
- Não implementa operações nem eventos; apenas orienta a localização do contrato correto.

**Fontes:**
- Manual SEI — cap. 8
- `.agents/skills/sei-mod-api-classes/references/catalogo-api.md`

---

## sei-mod-api-eventos

**Origem:** Skill interna criada a partir das seções de eventos e hooks do manual oficial SEI.

**Composição:**
- Escolhe o hook no catálogo `.agents/skills/sei-mod-api-eventos/references/catalogo-eventos.md`.
- Confirma assinatura em `SeiIntegracao.php` do core antes de implementar.
- Lógica mínima no hook; delegação para RN quando crescer.
- Segurança: negar por padrão; validar permissão para qualquer efeito colateral.
- Consistência transacional quando o evento gerar escrita relevante.

**Fontes:**
- Manual SEI — cap. 9
- `.agents/skills/sei-mod-api-eventos/references/catalogo-eventos.md`

---

## sei-mod-api-operacoes

**Origem:** Skill interna criada a partir das operações oficiais do SEI via `SeiRN`.

**Composição:**
- Identifica a operação no catálogo `.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md`.
- Monta objetos `Entrada*API`/`*API` sem usar classes internas.
- Executa via `SeiRN`; trata erro sem expor stacktrace.
- Transação coerente para múltiplas escritas.

**Fontes:**
- Manual SEI — operações via SeiRN
- `.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md`
- `.agents/skills/sei-mod-api-operacoes/references/andamentos.md`

---

## sei-report-todos

**Origem:** Skill interna para mapear pendências `TODO:` em módulos SEI, gerando um report estruturado sem alterar código.

**Composição:**
- Busca somente o marcador `TODO:` — não normaliza marcadores alternativos.
- Não executa até o usuário escolher módulos explicitamente.
- Classifica cada ocorrência: `dívida conhecida`, `risco relevante`, `bloqueante potencial`, `ignorar no report executivo`.
- Report opcional salvo em `.agents/reports/todos-<data>.md`.

**Fontes:**
- `AGENTS.md`
- `.agents/references/gates-de-implementacao.md`

---

## sei-testes-validacao

**Origem:** Skill interna que consolida as validações obrigatórias e opcionais após qualquer entrega PHP no repositório.

**Composição:**
- Mínimo obrigatório: `php -l` em todos os arquivos PHP alterados.
- Checks automatizados por artefato: `audit.py` de página, RN, BD, tarefa e controladores.
- Recomendações quando disponíveis: `composer test`, `phpcs`, `phpstan`.
- Smoke manual: happy path, sem permissão, link inválido, parâmetros inválidos, sessão expirada.

---

## sei-tipagem-phpdoc

**Origem:** Skill interna opt-in para modernizar assinaturas PHP com type hints e PHPDoc breve, respeitando contratos herdados do InfraPHP.

**Composição:**
- Só ativada com pedido explícito do desenvolvedor — não é gate obrigatório.
- Classifica métodos antes de tipar: `private`, construtor, `public`/`protected` sem override, override do core.
- PHPDoc breve com `@param`, `@return`, `@throws` apenas quando agregam contexto real.
- Não toca páginas procedurais `*_lista.php` e `*_cadastro.php` por padrão.

**Fontes:**
- `AGENTS.md`
- `.agents/references/padrao-codificacao-php.md`

---

## sei-verificacao-banco-dados

**Origem:** Gate criado a partir do capítulo 5 do manual oficial SEI/SIP (padrão de modelagem de dados) e seções do capítulo 4 (InfraPHP).

**Composição:**
- 15 regras (DB01-DB15): nomenclatura de tabela, N:N, limites Oracle (26/30 chars), PK, FK, exclusão lógica, constraint PK, tipos SQL-99, índice em FK, sequence, AK, COMMENT/docblock, verbos, singular, formato.
- Aceita PHP (DTO/BD), DDL SQL, arquivo ou diretório de módulo.
- 4 modos: `adhoc`, `pre_generate`, `audit`, `release_check`.
- Script `audit.py` com exit codes 0/1/2 (PASS/WARN/BLOCK).

**Fontes:**
- Manual SEI — cap. 5 e cap. 4
- `.agents/skills/sei-verificacao-banco-dados/references/padroes-manual-md.md`

---

## sei-verificacao-controladores

**Origem:** Gate criado a partir das seções 1363, 1442 e 1648 do capítulo 9 do manual oficial SEI.

**Composição:**
- 5 controles (CI1-CI5): CI1 a CI4 cobrem link sem assinatura, dispatch WS/Ajax e autorização específica; CI5 alerta sobre payload sensível em retorno de controlador.
- Script `audit.py` com exit codes 0/1/2 (PASS/WARN/BLOCK).

**Fontes:**
- Manual SEI — cap. 9, seções 1363, 1442 e 1648
- `.agents/skills/sei-verificacao-controladores/references/padroes-controladores.md`
- `.agents/security/matriz-vulnerabilidades-sei.md` — vetor V03

---

## sei-verificacao-pagina

**Origem:** Gate criado a partir dos capítulos 3, 4 e 9 do manual oficial SEI.

**Composição:**
- 10 controles (P1-P10): P1-P6 e P8-P10 são erros quando confirmados; P7 é aviso contextual, e P9 sem fluxo dinâmico confirmado permanece aviso.
- Os controles cobrem link, permissão, encoding Latin-1, entrada HTTP, UI condicional, saída HTML, hardening JS e mutação via GET.
- Script `audit.py` com exit codes 0/1/2 (PASS/WARN/BLOCK).

**Fontes:**
- Manual SEI — cap. 3, 4 e 9
- `.agents/skills/sei-verificacao-pagina/references/padroes-seguranca.md`

---

## sei-verificacao-rn

**Origem:** Gate criado a partir dos padrões de transação e separação de camadas do manual SEI.

**Composição:**
- 6 regras de transação (T1-T6): sufixo CRUD coerente, `inicializarObjInfraIBanco()`, isolamento de BD, controle manual de transação, `try/catch` com `InfraException` e efeitos externos somente após o commit.
- 3 regras de auditoria (A1-A3): recurso auditado em escrita, aviso para wrapper público de escrita sem verificação e recurso `_listar` em leitura pública, sem exigir sessão em helpers internos chamados por hook ou evento.
- Script `audit.py` com exit codes 0/1/2 (PASS/WARN/BLOCK).

**Fontes:**
- Manual SEI — InfraRN, BancoSEI, padrões de transação
- `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md`
- `.agents/references/padrao-auditoria-sip-sei.md`

---

## sei-verificacao-tarefa

**Origem:** Gate criado a partir das regras de `id_tarefa_modulo` do manual SEI.

**Composição:**
- 6 controles (K1-K4/K6-K7): ID numérico >= 1000 ou exceção 65, prefixo e tamanho de `id_tarefa_modulo`, unicidade nas duas dimensões e `DESCRICAO` obrigatória para o ID 65.
- Script `audit.py` com exit codes 0/1/2 (PASS/WARN/BLOCK).

**Fontes:**
- Manual SEI — regras de `id_tarefa_modulo`
- `.agents/skills/sei-verificacao-tarefa/references/padroes-tarefa.md`

---

## sip-gerador-scripts-release

**Origem:** Skill interna para padronizar a geração e atualização de scripts de release do lado SIP (`fontes/sei/src/main/php/sip/scripts/*`).

**Composição:**
- Família padrão: `*AtualizadorSipRN extends InfraRN`.
- Padrão primário: `sip_atualizar_versao_modulo_ia.php`.
- Criação idempotente de recursos, menus e vínculos (lookup antes de cadastrar).
- Auditoria ao final: `_cadastrar`, `_alterar`, `_excluir` (nunca `_listar`); `replicarRegraAuditoria` obrigatório.
- Literais obrigatórios: `SEI`, `Principal`, `Administrador`, `Basico`.

**Fontes:**
- `.agents/references/padrao-modelagem-dados.md`
- `.agents/skills/sip-gerador-scripts-release/references/sip-update-script-rules.md`
- `.agents/references/padrao-auditoria-sip-sei.md`
- Scripts de referência no repositório

---

## speckit

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/github/spec-kit

**Versão instalada:** v0.12.4

**Licença:** MIT

Framework de geração e gestão de especificações de features com workflows estruturados por fase. Integrado diretamente nas skills de fase. O `constitution.md` está intencionalmente vazio e não governa o fluxo. O framework em si não tem diretório próprio: o que existe no repositório são as 9 sub-skills abaixo, cada uma com seu `SKILL.md` em `.agents/skills/speckit-<fase>/`, fonte única e neutra em relação à ferramenta.

**Nenhuma integração guarda arquivo do SpecKit.** `.claude/commands/`, `.github/agents/`, `.github/prompts/` e `.opencode/command/` estão vazios. As três ferramentas leem `.agents/skills/` direto e encontram as fases lá, lado a lado com as demais skills do repositório, sem symlink e sem configuração extra:

| Ferramenta | Como chega em `.agents/skills/` |
|---|---|
| Claude Code | `.claude/skills`, symlink para `../.agents/skills` |
| Copilot | `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | `skills.paths` em `.opencode/opencode.json` |

Invocação: `/speckit-plan`, com hífen, igual nas três ferramentas. Regra de manutenção: [`.agents/references/speckit.md`](../references/speckit.md).

| Sub-skill | Fase | O que faz |
|---|---|---|
| `speckit-specify` | Especificar | Cria ou atualiza a spec a partir de descrição em linguagem natural. |
| `speckit-clarify` | Clarificar | Resolve ambiguidades e perguntas abertas na spec antes do planejamento. |
| `speckit-analyze` | Analisar | Analisa o código existente para informar o planejamento da feature. |
| `speckit-plan` | Planejar | Gera o plano de implementação a partir da spec aprovada. |
| `speckit-checklist` | Checklist | Gera ou atualiza o checklist de implementação da feature. |
| `speckit-implement` | Implementar | Executa a implementação seguindo o plano aprovado. |
| `speckit-tasks` | Tarefas | Cria e gerencia tarefas derivadas do plano. |
| `speckit-taskstoissues` | Issues | Converte tarefas do plano em issues no rastreador. |
| `speckit-constitution` | Constituição | Manutenção de `constitution.md` — não governa o fluxo das fases. |

---

## speckit-analyze

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Analisa o código existente para informar o planejamento da feature.

**Como invocar:** `/speckit-analyze` nas três ferramentas

---

## speckit-checklist

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Gera ou atualiza o checklist de implementação da feature.

**Como invocar:** `/speckit-checklist` nas três ferramentas

---

## speckit-clarify

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Resolve ambiguidades e perguntas abertas na spec antes do planejamento.

**Como invocar:** `/speckit-clarify` nas três ferramentas

---

## speckit-constitution

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Ferramenta de manutenção de `constitution.md`. Não governa o fluxo das fases — as regras vivem nas próprias skills de fase.

**Como invocar:** `/speckit-constitution` nas três ferramentas

---

## speckit-implement

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Executa a implementação seguindo o plano aprovado.

**Como invocar:** `/speckit-implement` nas três ferramentas

---

## speckit-plan

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Gera o plano de implementação a partir da spec aprovada.

**Como invocar:** `/speckit-plan` nas três ferramentas

---

## speckit-specify

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Cria ou atualiza a spec a partir de descrição em linguagem natural. Inicializa o workspace da feature (diretório, branch, arquivo de spec).

**Como invocar:** `/speckit-specify` nas três ferramentas

---

## speckit-tasks

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Cria e gerencia tarefas derivadas do plano.

**Como invocar:** `/speckit-tasks` nas três ferramentas

---

## speckit-taskstoissues

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** v0.12.4 | **Licença:** MIT

Converte tarefas do plano em issues no rastreador.

**Como invocar:** `/speckit-taskstoissues` nas três ferramentas
