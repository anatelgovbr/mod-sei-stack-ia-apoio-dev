# docs/

Documentação técnica do repositório, escrita para ser lida tanto por pessoas quanto por agentes de IA, que consultam vários destes arquivos como fonte de verdade.

---

## Sumário

- [1. Dicionários de dados](#1-dicionários-de-dados)
- [2. Manuais](#2-manuais)
- [3. Prompts de exemplo](#3-prompts-de-exemplo)
- [4. Documentação da stack de IA](#4-documentação-da-stack-de-ia)

---

## 1. Dicionários de dados

A pasta [`dicionario_dados/`](dicionario_dados/) guarda a semântica de tabelas e colunas e o histórico estrutural de cada alvo. Cada módulo, ou o núcleo SEI/SIP, tem sua própria pasta em `dicionario_dados/<modulo>/`.

| Arquivo | O que contém |
|---|---|
| `dicionario_tabelas.md` | Nome e descrição semântica das tabelas na versão atual |
| `dicionario_colunas.md` | Descrição das tabelas e de suas colunas na versão atual |
| `CHANGELOG.md` | Histórico de alterações estruturais |

Proveniência, confiança, conflitos e lacunas das descrições são reportados ao desenvolvedor durante a execução da skill (relatório de varredura ou relatório final de `verificar`), sem arquivo dedicado.

**Módulos/alvos documentados hoje:** `apoio-plano-trabalho`, `centraliza-modulos`, `cgu`, `correios`, `ia`, `julgar`, `litigioso`, `pen`, `pesquisa`, `peticionamento`, `sei`, `sip`.

Formato, fluxo de criação/atualização e geração de changelog são definidos pela skill [`dicionario-dados-db-scan-codebase-docs`](../.agents/skills/dicionario-dados-db-scan-codebase-docs/SKILL.md). Os dois dicionários são mantidos juntos e descrevem o mesmo conjunto de tabelas na mesma versão. O formato fica em [`formato-dicionario-de-dados.md`](../.agents/skills/dicionario-dados-db-scan-codebase-docs/references/formato-dicionario-de-dados.md).

---

## 2. Manuais

A pasta [`manuais/`](manuais/) tem uma subpasta por módulo, com o mesmo nome usado em `requisitos-ancorados/<modulo>/`, e a subpasta `sei/` para o núcleo SEI. Cada subpasta guarda os seus manuais e a pasta `imagens/` usada por eles.

| Subpasta | O que contém |
|---|---|
| [`apoio-plano-trabalho/`](manuais/apoio-plano-trabalho/) | Manual de uso do módulo Apoio a Plano de Trabalho, mantido pela skill [`manual-creator-scan-codebase`](../.agents/skills/manual-creator-scan-codebase/SKILL.md) |
| [`sei/`](manuais/sei/) | Manual oficial de desenvolvimento de módulos SEI (`SEI-Modulos-v5.0`) |

Em [`sei/manual_md/`](manuais/sei/manual_md/), o manual de desenvolvimento está dividido por capítulo em Markdown, com índice em `sei_modulos_manual_dev_0_indice.md`. Os capítulos são a fonte usada pelos catálogos das skills de integração (`catalogo-api.md`, `catalogo-eventos.md`, `catalogo-operacoes.md`). A pasta `sei/` guarda o manual nos formatos de origem (`SEI-Modulos-v5.0` em `.docx`, `.odt`, `.pdf` e um `.md` único) e a pasta `imagens/`, usada pelos capítulos e pelo `.md` único. Os formatos de origem servem de base para regenerar os capítulos caso o manual oficial seja atualizado e não são o material consultado no dia a dia.

---

## 3. Prompts de exemplo

[`stack_ai/prompts-exemplo.md`](stack_ai/prompts-exemplo.md) reúne prompts prontos para uso real, amarrados às skills do repositório: correção de bug (com variações Playwright e Selenium), fluxo Speckit para funcionalidade nova, ajustes pontuais em menu, entidade e API/WebService, revisão técnica e segurança, e dicionário de dados.

Cada prompt já traz objetivo, fatos verificados versus hipóteses não confirmadas, critério de aceite e protocolo de execução, prontos para adaptar e enviar.

---

## 4. Documentação da stack de IA

[`stack_ai/`](stack_ai/) explica a stack de IA do repositório para quem vai usá-la: o que é, quais ferramentas funcionam aqui, como usar o SpecKit, prompts prontos e como manter a stack atualizada.

| Arquivo | O que contém |
|---|---|
| `README.md` | Documento principal da stack: conceitos, agentes e skills, ferramentas suportadas, SpecKit, estrutura, como começar e como atualizar |
| `speckit.md` | O que é o SpecKit, quando usar, as 10 fases e como invocar cada uma |
| `manutencao-da-stack.md` | Como atualizar o SpecKit e os demais arquivos da stack |
| `prompts-exemplo.md` | Prompts prontos para as demandas reais do SEI: bug, fluxo SpecKit, ajuste pontual, revisão técnica, dicionário de dados e modos auxiliares |

As skills do repositório, de terceiros e do projeto, estão descritas em [`stack_ai/README.md`](stack_ai/README.md). O `README.md` da raiz não detalha a stack: ele só aponta para essa pasta.

Regras de código, limites de escrita e padrões deste projeto não ficam nessa pasta: estão no [`AGENTS.md`](../AGENTS.md).
