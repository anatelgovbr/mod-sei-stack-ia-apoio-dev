# Decisões arquiteturais (ADR)

Uma ADR (Architecture Decision Record) registra uma decisão arquitetural: o contexto, as alternativas consideradas, a decisão e as consequências.

## Regras

1. Crie a ADR a partir de [`../ADR-TEMPLATE.md`](../ADR-TEMPLATE.md) na subpasta do módulo, com o mesmo nome da pasta do módulo em `docs/requisitos-ancorados/`, ou na subpasta `sei/`, quando a decisão vale para o SEI inteiro. Use o próximo número livre da subpasta e um título curto, de até cinco palavras: `ADR-<SIGLA>-NNN-titulo-curto.md`, em que `<SIGLA>` é a sigla SIP do módulo em maiúsculas, ou `SEI` na subpasta `sei/`. O número e o nome do arquivo não mudam depois.
2. Os estados são `proposta`, `aceita` e `descontinuada`, equivalentes a proposed, accepted e deprecated ou superseded no modelo original. `descontinuada` é o estado final: `proposta -> aceita -> descontinuada`.
3. A ADR nasce `proposta`, antes da implementação, e passa a `aceita` com a decisão do proprietário. Uma proposta recusada é ajustada ou descartada e não entra no commit. O motivo de cada alternativa recusada fica na seção de alternativas da ADR aceita. O registro de uma decisão que já está em uso nasce `aceita`, com a data original.
4. O conteúdo de uma ADR aceita ou descontinuada não muda. Só são permitidas correção editorial, sem mudança de sentido, e a atualização dos campos de estado e de relação.
5. Para mudar uma decisão aceita, crie uma ADR nova com o campo "Substitui: ADR-<SIGLA>-NNN", repetindo o que continua valendo. Quando a nova for aceita, a anterior passa a `descontinuada` e recebe o campo "Substituída por: ADR-<SIGLA>-MMM".
6. Uma decisão que deixou de valer sem ter substituta também passa a `descontinuada`, e o campo "Substituída por" continua "nenhuma". Quando a retirada também for uma decisão arquitetural, o motivo vai numa ADR nova.
7. Evidências, como testes, relatórios e pareceres, ficam nos próprios artefatos e citam a ADR pelo número.
8. Na revisão de código ou de desenho, uma mudança que contraria ADR aceita fica bloqueada até ser corrigida ou até uma ADR que a substitua ser aceita.

## O que fica fora da ADR

A ADR registra uma decisão, o motivo e as alternativas. O resto da documentação tem lugar próprio:

| Conteúdo | Onde fica |
|---|---|
| Desenho do mecanismo, como diagrama de sequência e passo a passo de execução | Documentação própria do módulo, fora da ADR |
| Valores de parâmetro, limites e contratos | Requisitos técnicos do módulo, em `docs/requisitos-ancorados/<modulo>/requisitos-tecnicos.md` |
| Decisão interna de componente autocontido, que não precisa de ADR | Documentação do próprio componente |

Fontes que sustentam essa separação:

- Microsoft, [Azure Well-Architected Framework, Architecture decision record](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record): "Avoid making decision records design guides. If more justification or design ideation is available, provide a link to a document as supplemental material, but the decision must be clear and stand alone without that material."
- Olaf Zimmermann, [ADR Mistakes](https://ozimmer.ch/practices/2026/09/12/ADRMistakes.html), 2026: "detailed design specifications deserve their own place in the documentation."
- Olaf Zimmermann, [ADR Creation](https://ozimmer.ch/practices/2023/04/03/ADRCreation.html), 2023, sobre o antipadrão "Mega-ADR": "A lot of detailed information about the architecture is stuffed into several multi-page ADRs serving as documentation master (or monster?)". O remédio indicado é "Move the detail design to a separate document."
- Michael Nygard, [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011, texto que deu origem às ADRs: "The whole document should be one or two pages long."

## Referências de prática

- [AWS Prescriptive Guidance: Architectural decision record process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Microsoft Azure Well-Architected Framework: Maintain an architecture decision record](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [Microsoft Engineering Fundamentals Playbook: Design Decision Log](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/)
- [Markdown Architectural Decision Records](https://adr.github.io/madr/)
- [Olaf Zimmermann: Architectural Significance Test](https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html)
