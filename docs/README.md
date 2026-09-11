# docs/

Documentação técnica do repositório, escrita para ser lida tanto por pessoas quanto por agentes de IA, que consultam vários destes arquivos como fonte de verdade.

---

## Sumário

- [1. Dicionários de dados](#1-dicionários-de-dados)
- [2. Manual de desenvolvimento](#2-manual-de-desenvolvimento)
- [3. Gabarito do gerador de CRUD](#3-gabarito-do-gerador-de-crud)
- [4. Prompts de exemplo](#4-prompts-de-exemplo)
- [5. Documentação da stack de IA](#5-documentação-da-stack-de-ia)

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

## 2. Manual de desenvolvimento

[`manual_desenvolvimento_md/`](manual_desenvolvimento_md/) é o manual oficial de desenvolvimento de módulos SEI (`SEI-Modulos-v5.0`) dividido por capítulo em Markdown, com índice em `sei_modulos_manual_dev_0_indice.md`. É a fonte usada pelos catálogos das skills de integração (`catalogo-api.md`, `catalogo-eventos.md`, `catalogo-operacoes.md`).

[`manual_desenvolvimento/`](manual_desenvolvimento/) guarda o mesmo manual nos formatos de origem (`.docx`, `.odt`, `.pdf` e um `.md` único), mais as imagens referenciadas no texto. Serve de base para regenerar `manual_desenvolvimento_md/` caso o manual oficial seja atualizado; não é o material consultado no dia a dia.

---

## 3. Gabarito do gerador de CRUD

A pasta [`gabarito_gerador_codigo_crud/`](gabarito_gerador_codigo_crud/) traz um exemplo completo de saída do gerador de CRUD (`sei-gerador-crud`) para o domínio fictício `md_abc`: DTO, BD, RN, INT e páginas de lista/cadastro, mais o contrato de domínio (`dominio-md-abc.md`). Funciona como referência estrutural adicional aos gabaritos de módulo citados no `AGENTS.md`: `abc/exemplo` como referência mínima e `trf4/julgamento` como referência robusta.

---

## 4. Prompts de exemplo

[`prompts-exemplo.md`](../prompts-exemplo.md) reúne prompts prontos para uso real, amarrados às skills do repositório: correção de bug (com variações Playwright e Selenium), fluxo Speckit para funcionalidade nova, ajustes pontuais em menu, entidade e API/WebService, revisão técnica e segurança, e dicionário de dados.

Cada prompt já traz objetivo, fatos verificados versus hipóteses não confirmadas, critério de aceite e protocolo de execução, prontos para adaptar e enviar.

---

## 5. Documentação da stack de IA

a raiz do repositório (`README.md`, `speckit.md`, `manutencao-da-stack.md` e `prompts-exemplo.md`) explica a stack de IA do repositório para quem vai usá-la: o que é, quais ferramentas funcionam aqui, como usar o SpecKit, prompts prontos e como manter a stack atualizada.

| Arquivo | O que contém |
|---|---|
| `README.md` | Documento principal da stack: conceitos, agentes e skills, ferramentas suportadas, SpecKit, estrutura, como começar e como atualizar |
| `speckit.md` | O que é o SpecKit, quando usar, as 10 fases e como invocar cada uma |
| `manutencao-da-stack.md` | Como atualizar o SpecKit e os demais arquivos da stack |
| `prompts-exemplo.md` | Prompts prontos para as demandas reais do SEI: bug, fluxo SpecKit, ajuste pontual, revisão técnica, dicionário de dados e modos auxiliares |

As skills do repositório, de terceiros e do projeto, estão descritas em [`README.md`](../README.md). O `README.md` da raiz não detalha a stack: ele só aponta para essa pasta.

Regras de código, limites de escrita e padrões deste projeto não ficam nessa pasta: estão no [`AGENTS.md`](../AGENTS.md).
