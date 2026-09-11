---
name: sei-mod-api-operacoes
description: >
  Implementa e testa operacoes oficiais do SEI via SeiRN usando classes da API
  (Entrada*API / Saida*API / *API), lancamento/consulta de andamentos e
  integracoes via WebServices quando aplicavel.

  Use quando:
  - O desenvolvedor precisa executar uma operacao oficial do SEI (gerar processo,
    incluir documento, lancar andamento, enviar processo, etc.)
  - Ha necessidade de integrar via WebServices usando a mesma API do core
  - Promptlike: "implementar a operacao X", "gerar procedimento via API",
    "lancar andamento no processo Y"

  Esta skill foca em executAR operacoes.
  Se a demanda ainda estiver ambigua entre API, evento e operacao, usar
  sei-direcionador-integracao.
---

# sei-mod-api-operacoes

## Objetivo

Orientar o agente a executar operacoes oficiais do core do SEI via `SeiRN`
usando classes da API como payload, evitando o uso de classes internas ou
implementacoes proprias quando ja existe operacao oficial.

## Quando usar

- O agente precisa executar uma operacao oficial do SEI (criar processo, incluir documento, lancar andamento, enviar, bloquear, etc.).
- O agente esta implementando integracao via WebServices usando a mesma API do core.
- Promptlike: "implementar a operacao X", "gerar procedimento via API", "lancar andamento no processo Y", "bloquear documento por API".
- A necessidade e executar acao, nao apenas consultar o catalogo de APIs.

Quando a duvida for apenas sobre qual classe `Entrada*API`/`Saida*API` usar
dentro de uma operacao ja escolhida, acionar `sei-mod-api-classes` como complemento,
nao como skill principal de triagem.

## Procedimento

1. **Identificar a operacao** no catalogo em `references/catalogo-operacoes.md`.
2. **Consultar a classe de entrada/saida** no catalogo da `sei-mod-api-classes` (`references/catalogo-api.md`) para saber quais campos sao necessarios.
3. **Montar objetos da API**: usar `Entrada*API` / `*API` preenchendo apenas os campos necessarios. Nao usar classes internas.
4. **Executar via `SeiRN`**: instanciar `SeiRN` e chamar o metodo correspondente.
5. **Tratar erro**: nao expor stacktrace ao usuario; retornar mensagens faceis de entender; logar sem PII/segredos.
6. **Transacao**: se a operacao envolver multiplas escritas ou efeitos colaterais, garantir transacao coerente (manual ou metodo `*Controlado`).
7. **Testes**: criar casos com payloads minimos e realistas em homolog (cURL/Postman) e negativos (permissao/parametros invalidos).

## Critérios de validação

- [ ] A operacao executada existe no catalogo de operacoes do manual.
- [ ] Os objetos de entrada/saida usado correspondem ao contrato oficial documentado na `sei-mod-api-classes`.
- [ ] Nao foi usada classe interna do core como payload.
- [ ] Erro tratado sem stacktrace exposto.
- [ ] Transacao coerente quando ha multiplas escritas.
- [ ] Testes incluem caso positivo, negativo (sem permissao) e borda (params invalidos).
- [ ] A skill nao assumiu demanda ambigua que deveria passar antes por `sei-direcionador-integracao`.

## Referências

- Catalogo de operacoes: `references/catalogo-operacoes.md`
- Regras de andamentos: `references/andamentos.md`
- Triagem ambigua entre API, evento e operacao: `sei-direcionador-integracao`
- Classes API (entrada/saida): `sei-mod-api-classes` / `references/catalogo-api.md`

## Regras gerais de uso das operacoes

**Preferir o ID interno.** Sempre que a operacao aceitar o ID interno ou o numero de protocolo, **usar o ID interno**. O protocolo e identificador de apresentacao e pode mudar de formato.

**A camada de Web Services usa a mesma API.** Toda operacao disponivel por Web Services esta disponivel diretamente ao modulo pela API. Nao chamar o proprio Web Service do SEI de dentro de um modulo do SEI.

**Alteracoes nos objetos e metodos.** Mudancas nos objetos da API e nos metodos da classe acompanham a versao do SEI. Ao subir de versao, conferir o capitulo 10 da versao nova antes de assumir que o contrato permaneceu.
