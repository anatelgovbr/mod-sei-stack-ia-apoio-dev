---
name: sei-mod-api
description: >
  Verifica se existe classe API oficial do SEI antes de usar classe interna,
  acesso direto ao core ou implementacao propria. Auxilia o agente a localizar
  o contrato correto (Entrada*API / Saida*API / *API) para integracao via modulo.

  Use quando:
  - O desenvolvedor precisa verificar se ja existe uma API oficial para seu caso
  - Ha necessidade de identificar qual objeto da API usar (ex: ProcedimentoAPI,
    DocumentoAPI, AndamentoAPI, PublicacaoAPI)
  - O agente esta prestes a propor acesso ao core ou uso de classes internas
  - Promptlike: "qual API usar para fazer X", "existe classe oficial para Y"

  Esta skill NAO implementa operacoes nem eventos — apenas orienta a localizacao
  correta do contrato oficial.
  Para implementacao de operacao, usar sei-mod-operacoes.
  Para interceptacao de eventos, usar sei-mod-eventos.
---

# sei-mod-api

## Objetivo

Orientar o agente a localizar e usar classes API oficiais do core do SEI,
evitando uso de classes internas, acesso direto ao core ou implementacao propria
quando ja existe contrato oficial.

## Quando usar

- O agente precisa integrar com o SEI via modulo e quer confirmar se existe API oficial.
- O agente esta prestes a propor implementacao propria, acesso a `SeiRN` fora de operacoes conhecidas, ou uso de classes internas.
- Promptlike: "qual API usar para fazer X", "existe classe oficial para Y", "preciso acessar dado do processo".
- O desenvolvedor nao sabe se algo ja existe no SEI.

## Procedimento

1. **Consultar o catalogo** em `references/catalogo-api.md`.
2. **Identificar a classe ou contrato correto** com base na necessidade do desenvolvedor.
3. **Verificar o capitulo 8 do manual** (`docs/manual_desenvolvimento_md/sei_modulos_manual_dev_8_classes_api.md`) para confirmar atributos, metodos e uso.
4. **Confirmar que o contrato existe** antes de propor qualquer acesso interno ou implementacao propria.
5. **Se o contrato existir**: apontar a classe API oficial, seus atributos principais e o contexto de uso.
6. **Se o contrato nao existir**: sinalizar que nao ha API oficial documentada e que a abordagem exigira justificativa de seguranca e aprovacao.

## Critérios de validação

- [ ] O agente consultou o catalogo antes de propor implementacao propria.
- [ ] Nao foi recomendada classe interna do core como solucao quando existe API oficial.
- [ ] Nomes oficiais preservados conforme capitulo 8 do manual.
- [ ] Ambiguidades do manual sinalizadas quando aplicavel.
- [ ] Referencias cruzadas a `sei-mod-operacoes` e `sei-mod-eventos` corretas.

## Referências

- Catalogo: `references/catalogo-api.md`
- Manual SEI cap 8: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_8_classes_api.md`
- Para implementacao de operacao: `sei-mod-operacoes`
- Para interceptacao de eventos: `sei-mod-eventos`
