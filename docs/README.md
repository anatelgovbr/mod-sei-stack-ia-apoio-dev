# docs/

Documentação técnica do repositório, escrita para ser lida tanto por pessoas quanto por agentes de IA, que consultam vários destes arquivos como fonte de verdade.

---

## Sumário

- [1. Dicionários de dados](#1-dicionários-de-dados)
- [2. Manual de desenvolvimento](#2-manual-de-desenvolvimento)
- [3. Gabarito do gerador de CRUD](#3-gabarito-do-gerador-de-crud)
- [4. Prompts de exemplo](#4-prompts-de-exemplo)

---

## 1. Dicionários de dados

A pasta [`dicionario_dados/`](dicionario_dados/) guarda o dicionário de dados (schema e semântica de tabelas e colunas) e o histórico de versões de cada módulo, do SEI ou do SIP. Cada módulo, ou o núcleo SEI/SIP, tem sua própria pasta em `dicionario_dados/<modulo>/`, com dois arquivos:

| Arquivo | O que contém |
|---|---|
| `dicionario.md` | Schema e semântica das tabelas e colunas na versão atual |
| `CHANGELOG.md` | Histórico de versões do dicionário, entrada por entrada |

**Módulos/alvos documentados hoje:** `apoio-plano-trabalho`, `centraliza-modulos`, `controle-de-demandas`, `correios`, `ia`, `julgar`, `litigioso`, `pen`, `peticionamento`, `sei`, `sip`.

Formato, fluxo de criação/atualização e geração de changelog são definidos pela referência compartilhada [`formato-dicionario-de-dados.md`](../.agents/references/dicionario-dados/formato-dicionario-de-dados.md), consumida por duas skills conforme o alvo: [`sei-dicionario-dados-core`](../.agents/skills/sei-dicionario-dados-core/SKILL.md) para SEI, SIP e Julgar; [`sei-dicionario-dados-modulo`](../.agents/skills/sei-dicionario-dados-modulo/SKILL.md) para módulo customizado. Siga esse formato ao editar os arquivos manualmente; a referência garante consistência de estilo entre dicionários.

---

## 2. Manual de desenvolvimento

[`manual_desenvolvimento_md/`](manual_desenvolvimento_md/) é o manual oficial de desenvolvimento de módulos SEI (`SEI-Modulos-v5.0`) dividido por capítulo em Markdown, com índice em `sei_modulos_manual_dev_0_indice.md`. É a fonte usada pelos catálogos das skills de integração (`catalogo-api.md`, `catalogo-eventos.md`, `catalogo-operacoes.md`).

[`manual_desenvolvimento/`](manual_desenvolvimento/) guarda o mesmo manual nos formatos de origem (`.docx`, `.odt`, `.pdf` e um `.md` único), mais as imagens referenciadas no texto. Serve de base para regenerar `manual_desenvolvimento_md/` caso o manual oficial seja atualizado; não é o material consultado no dia a dia.

---

## 3. Gabarito do gerador de CRUD

A pasta [`gabarito_gerador_codigo_crud/`](gabarito_gerador_codigo_crud/) traz um exemplo completo de saída do gerador de CRUD (`sei-gerador-crud`) para o domínio fictício `md_abc`: DTO, BD, RN, INT e páginas de lista/cadastro, mais o contrato de domínio (`dominio-md-abc.md`). Funciona como referência estrutural adicional aos gabaritos de módulo citados no `AGENTS.md`: `abc/exemplo` como referência mínima e `trf4/julgamento` como referência robusta.

---

## 4. Prompts de exemplo

[`prompts-exemplo.md`](prompts-exemplo.md) reúne exemplos prontos de prompts para desenvolvedores conversarem com a ferramenta de IA, organizados por tipo de demanda (análise, bug, menu/página, CRUD, release, API/WebService, revisão, pedido de plano).
