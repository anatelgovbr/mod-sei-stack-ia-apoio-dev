---
name: sei-mod-api-classes
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
  correta do contrato oficial de API.
  Para implementacao de operacao, usar sei-mod-api-operacoes.
  Para interceptacao de eventos, usar sei-mod-api-eventos.
  Se a demanda ainda estiver ambigua entre API, evento e operacao, usar
  sei-direcionador-integracao.
---

# sei-mod-api-classes

## Objetivo

Orientar o agente a localizar e usar classes API oficiais do core do SEI,
evitando uso de classes internas, acesso direto ao core ou implementacao propria
quando ja existe contrato oficial.

## Quando usar

- O agente precisa integrar com o SEI via modulo e quer confirmar se existe API oficial.
- O agente esta prestes a propor implementacao propria, acesso a `SeiRN` fora de operacoes conhecidas, ou uso de classes internas.
- Promptlike: "qual API usar para fazer X", "existe classe oficial para Y", "preciso acessar dado do processo".
- A necessidade ja foi delimitada como busca de contrato API oficial.

## Procedimento

1. **Consultar o catalogo** em `references/catalogo-api.md` — fonte curada do cap. 8; confirmar atributos, metodos e uso diretamente nele.
2. **Identificar a classe ou contrato correto** com base na necessidade do desenvolvedor.
3. **Confirmar que o contrato existe** antes de propor qualquer acesso interno ou implementacao propria.
5. **Se o contrato existir**: apontar a classe API oficial, seus atributos principais e o contexto de uso.
6. **Se o contrato nao existir**: sinalizar que nao ha API oficial documentada e que a abordagem exigira justificativa de seguranca e aprovacao.
7. **Se a duvida real nao for sobre API** e sim sobre escolher entre API, evento ou operacao: interromper a triagem e encaminhar para `sei-direcionador-integracao`.

## Critérios de validação

- [ ] O agente consultou o catalogo antes de propor implementacao propria.
- [ ] Nao foi recomendada classe interna do core como solucao quando existe API oficial.
- [ ] Nomes oficiais preservados conforme `references/catalogo-api.md`.
- [ ] Ambiguidades do manual sinalizadas quando aplicavel.
- [ ] A skill nao assumiu demandas ambiguas entre API, evento e operacao.
- [ ] Referencias cruzadas a `sei-mod-api-operacoes` e `sei-mod-api-eventos` corretas.

## Referências

- Catalogo curado: `references/catalogo-api.md` (cobre integralmente o cap. 8 do manual)
- Para triagem ambigua entre API, evento e operacao: `sei-direcionador-integracao`
- Para implementacao de operacao: `sei-mod-api-operacoes`
- Para interceptacao de eventos: `sei-mod-api-eventos`
