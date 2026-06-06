# Checklist de [TIPO] — [NOME DA FEATURE]

**Objetivo**: [Breve descricao do foco de qualidade de requisitos]
**Criado em**: [DATA]
**Feature**: [Link para spec.md ou documentacao relevante]

**Nota**: Este checklist e gerado por `/speckit.checklist` ou por `/speckit.specify` como gate de qualidade de requisitos.

<!--
  Os itens deste checklist testam a qualidade dos requisitos escritos.
  Nao sao testes de implementacao. Substituir todos os itens de exemplo
  nos arquivos gerados por itens derivados da feature ativa.
-->

## Completude dos Requisitos

- [ ] CHK001 Todos os perfis de usuario afetados e contextos SEI relevantes estao especificados? [Completude]
- [ ] CHK002 Todos os cenarios principais, alternativos e de erro estao documentados? [Cobertura]

## Clareza dos Requisitos

- [ ] CHK003 Termos vagos estao quantificados ou substituidos por criterios objetivos? [Clareza]
- [ ] CHK004 Permissoes, menus, recursos e impactos em perfis estao sem ambiguidade quando aplicavel? [Clareza]

## Consistencia e Rastreabilidade

- [ ] CHK005 Os requisitos funcionais sao consistentes com as historias de usuario e criterios de sucesso? [Consistencia]
- [ ] CHK006 Cada requisito pode ser rastreado a pelo menos uma historia de usuario ou item explicito de escopo? [Rastreabilidade]

## Casos de Borda e Premissas

- [ ] CHK007 Condicoes de contorno e modos de falha estao especificados? [Cobertura]
- [ ] CHK008 As premissas sao explicitas e seguras para o planejamento? [Premissa]

## Observacoes

- Usar `[x]` apenas apos o item de qualidade de requisito estar satisfeito.
- Usar os marcadores `[Gap]`, `[Ambiguidade]`, `[Conflito]` ou `[Premissa]` quando util.
- Checklists gerados devem substituir os itens de exemplo por itens derivados da feature ativa.
