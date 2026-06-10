---
name: sei-mod-eventos
description: >
  Intercepta eventos do SEI via metodos na classe *Integracao (SeiIntegracao),
  usando objetos da API, com foco em permissao/link assinado, consistencia
  transacional e auditoria quando aplicavel.

  Use quando:
  - O desenvolvedor precisa interceptar um evento do SEI (assinatura, envio,
    cancelamento, publicacao, mudanca de estado)
  - Ha necessidade de adicionar botoes, icones ou itens de menu customizados
  - O agente precisa implementar um hook de extensao no modulo
  - Promptlike: "implementar o evento X", "interceptar assinatura de documento",
    "adicionar botao no controle de processos"

  Esta skill foca em interceptAR eventos — para verificar se um evento existe
  antes de implementar, usar sei-mod-api.
---

# sei-mod-eventos

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

## Procedimento

1. **Escolher o hook** no catalogo `references/catalogo-eventos.md` pelo nome do evento.
2. **Confirmar a assinatura** do metodo em `SeiIntegracao.php` (core) ou em modulos de referencia.
3. **Implementar no `*Integracao.php`**: manter logica minima no hook; delegar para RN/servicos quando a logica crescer.
4. **Seguranca**: negar por padrao em entradas nao confiaveis; validar permissao para qualquer efeito colateral; assinar links na geracao e validar na entrada.
5. **Consistencia transacional**: se o evento gerar escrita relevante (BD/processo/documento), usar transacao manual ou metodo `*Controlado`.
6. **Evidencias**: testes manuais guiados e negativos (sem permissao, link invalido, parametros invalidos); logs faceis sem PII/segredos.

## Critérios de validação

- [ ] O hook implementado corresponde a um evento documentado no catalogo.
- [ ] Logica minima mantida no hook, com delegacao para RN/servicos quando necessario.
- [ ] Permissao validada antes de qualquer efeito colateral.
- [ ] Link assinado na geracao e validado na entrada quando aplicavel.
- [ ] Transacao coerente quando ha escrita relevante.
- [ ] Testes cobrindo caminho positivo e negativos (sem permissao, parametros invalidos).

## Referências

- Catalogo de eventos: `references/catalogo-eventos.md`
- Classes API (entrada): `sei-mod-api` / `references/catalogo-api.md`
- Operacoes relacionadas: `sei-mod-operacoes`
- Manual SEI cap 9: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_9_eventos.md`
- Para verificar se existe evento oficial antes de implementar: `sei-mod-api`
