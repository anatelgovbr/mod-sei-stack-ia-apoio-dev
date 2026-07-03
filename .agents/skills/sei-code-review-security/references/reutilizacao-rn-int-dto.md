# Reaproveitamento em RN / INT / DTO

Disciplina aplicada pela skill `sei-code-review-security` quando o diff cria ou
altera funcao, metodo ou classe em RN, INT ou DTO (ou camada equivalente). O
objetivo e evitar duplicacao de regra de negocio e codigo na camada errada.

Pergunta central, sempre: **"essa funcao realmente precisa existir?"**

## Checklist U1-U10

| # | Pergunta | Severidade se violado | Referencia |
|---|---|---|---|
| U1 | Ja existe metodo equivalente na **mesma** RN/INT/DTO? | ALTA (duplicacao) | — |
| U2 | Ja existe equivalente em **outra RN relacionada**? | MEDIA | — |
| U3 | A responsabilidade esta na camada certa (RN x INT x DTO x pagina x operacao)? | ALTA | `sei-verificacao-rn` T3/T5 |
| U4 | Nome segue o padrao SEI (CRUD `Controlado`/`Conectado`; `md_<sigla>_...`)? | MEDIA | `sei-verificacao-rn` T1 |
| U5 | Ha regra de negocio duplicada (logica repetida em outro RN)? | ALTA | — |
| U6 | SQL cru evitavel (daria para usar DTO/criterio)? | ALTA | matriz V05 |
| U7 | Acoplamento indevido a pagina/sessao/request/superglobais/`$_REQUEST`? | ALTA | matriz V06 |
| U8 | Visibilidade correta (private/protected/public)? | MEDIA | — |
| U9 | Impacto em permissoes / scripts SEI-SIP / multi-SGBD / transacao? | conforme gate | gates R1/R3/R5 |
| U10 | A funcao precisa existir, ou da para reusar core/API publica? | sempre perguntar | `sei-mod-api-classes` |

## Onde procurar um equivalente antes de aprovar codigo novo

1. **Na propria classe** — outros metodos do mesmo RN/INT/DTO.
2. **Em RN relacionada** do mesmo modulo (`rn/` do modulo-alvo).
3. **No core / API publica** — catalogos `sei-mod-api-classes`, `sei-mod-api-operacoes`,
   `sei-mod-api-eventos` (`references/catalogo-*.md`). Uso de classe interna do core
   suportada pelas versoes alvo do modulo pode ser mantido; o ponto aqui e evitar
   duplicacao desnecessaria, nao proibir internals por si so.
4. **Nos padroes do projeto** — `.agents/references/padrao-codificacao-php.md`,
   `.agents/references/padrao-modelagem-dados.md`.

## Decisao

- Equivalente encontrado e adequado → recomendar **reuso**; achado U1/U5 ALTA.
- Camada errada (U3) → recomendar mover a responsabilidade; nao aprovar como esta.
- Uso de classe interna do core suportada pelas versoes alvo do modulo → nao tratar
  como achado por si so; so registrar se houver alternativa publica claramente mais
  adequada no mesmo contexto ou risco atual nao tratado.
- Sem equivalente e camada correta → seguir; registrar a justificativa em 1 linha.

A skill nao reescreve codigo: aponta o equivalente, a camada correta e a
recomendacao.
