---
name: sei-mod-api-eventos
description: >
  Intercepta eventos do SEI em *Integracao (SeiIntegracao), usando objetos da API,
  com permissao, consistencia transacional e auditoria quando aplicavel.
  Acionar tambem ao criar ou alterar FK ou uso funcional de registros do core,
  inclusive protocolos de processos e documentos, mesmo sem mudanca de DDL.

  Use quando:
  - O desenvolvedor precisa interceptar um evento do SEI (assinatura, envio,
    cancelamento, publicacao, mudanca de estado)
  - Ha necessidade de adicionar botoes, icones ou itens de menu customizados
  - O agente precisa implementar um hook de extensao no modulo
  - Promptlike: "implementar o evento X", "interceptar assinatura de documento",
    "adicionar botao no controle de processos"

  Esta skill foca em interceptAR eventos.
  Se a demanda ainda estiver ambigua entre API, evento e operacao, usar
  sei-direcionador-integracao.
---

# sei-mod-api-eventos

## Objetivo

Orientar o agente a implementar hooks de extensao do core do SEI via sobrecarga
de metodos em `*Integracao.php` (estende `SeiIntegracao`), usando objetos da API
como entrada, com foco em permissao/link assinado, consistencia transacional
e auditoria quando aplicavel.

## Quando usar

- O agente precisa interceptar um evento do SEI para executar logica adicional.
- O agente esta adicionando botoes, icones ou itens de menu em telas do core.
- O agente precisa rotear requisicoes AJAX ou WebServices dentro do modulo.
- Promptlike: "interceptar assinatura de documento", "adicionar botao no controle de processos", "mostrar icone especial no processo", "implementar menu de publicacoes".

Quando o desenvolvedor escolher explicitamente `sei-gerador-crud`, o gerador e
principal para o CRUD e esta skill cobre eventual hook. Caso contrario, usar
`sei-menu-pagina` como principal para menu interno SIP, pagina ou acao do
proprio modulo sem hook no core nem menu externo/publicacoes; para hook no core,
menu externo/publicacoes ou injecao de botoes/icones, usar `sei-mod-api-eventos`
como principal.

## Procedimento

0. **Dependências de registros do core**: quando a mudança afetar referência física ou uso funcional, aplicar [proteção das dependências](references/protecao-dependencias-core.md) e concluir sua matriz; inclui Administração e protocolos, sem presumir que todo evento permita veto.
1. **Escolher o hook** no catalogo `references/catalogo-eventos.md` pelo nome do evento.
2. **Confirmar a assinatura** do método em `SeiIntegracao.php` e o ponto de chamada no core da versão suportada. Para eventos de negócio, verifique a posição perante escrita/commit e a propagação da exceção. Para `montarBotaoControleProcessos`, `montarBotaoProcesso` ou `montarBotaoDocumento`, aplique o [contrato do filtro de botões por acesso recente](references/catalogo-eventos.md#filtro-de-botões-por-acesso-recente) e execute sua verificação. Módulos existentes são exemplos com limitações, não prova do contrato.
3. **Implementar no `*Integracao.php`**: manter logica minima no hook; delegar para RN/servicos quando a logica crescer.
4. **Seguranca**: negar por padrao em entradas nao confiaveis; validar permissao para qualquer efeito colateral; assinar links na geracao e validar na entrada.
5. **Consistencia transacional**: se o evento gerar escrita relevante (BD/processo/documento), usar transacao manual ou metodo `*Controlado`.
6. **Evidencias**: testes manuais guiados e negativos aplicaveis ao evento, conforme `sei-validacao-padrao`: sem permissao quando houver controle de acesso afetado, link invalido quando houver link e parametros invalidos quando houver parametros. Teste link invalido em sessao isolada; sem isolamento, registre pendencia. Mantenha logs sem PII/segredos. Se o hook criar ou alterar componente visual, aplicar `.agents/references/padrao-acessibilidade-cores-sei.md` no contexto onde ele aparece.

## Critérios de validação

- [ ] O hook implementado corresponde a um evento documentado no catalogo.
- [ ] Logica minima mantida no hook, com delegacao para RN/servicos quando necessario.
- [ ] Permissao validada antes de qualquer efeito colateral.
- [ ] Link assinado na geracao e validado na entrada quando aplicavel.
- [ ] Transacao coerente quando ha escrita relevante.
- [ ] Testes cobrindo caminho positivo e negativos aplicaveis ao evento, conforme o procedimento.
- [ ] A skill nao assumiu como principal um caso que era apenas menu interno SIP/pagina de modulo sem hook no core.

## Referências

- Catalogo de eventos: `references/catalogo-eventos.md`
- Classes API (entrada): `sei-mod-api-classes` / `references/catalogo-api.md`
- Triagem ambigua entre API, evento e operacao: `sei-direcionador-integracao`
- Operacoes relacionadas: `sei-mod-api-operacoes`
