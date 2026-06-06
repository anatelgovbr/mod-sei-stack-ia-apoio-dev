---
name: sei-verificacao-controladores
description: >
  Skill padrao de validacao para controladores de integracao SEI em
  `*Integracao.php`. Audita somente regras com base clara no manual do SEI para
  `processarControladorAjax`, `processarControladorAjaxExterno`,
  `processarControladorWebServices` e `tratarLinkSemAssinatura`, mais um aviso
  complementar sobre payload sensivel. Nao assume responsabilidades do
  controlador central do SEI.

  Use quando:
  - alterar metodos de controlador em `*Integracao.php`
  - revisar dispatch de AJAX interno/externo do modulo
  - revisar roteamento de WebServices do modulo
  - revisar `tratarLinkSemAssinatura`
---

# sei-verificacao-controladores

## Regras SEI Explicitas (bloqueantes)

| ID | Regra | Severidade | Base |
|---|---|---|---|
| CI1 | `tratarLinkSemAssinatura()` usa `preg_match` restritivo | **Erro** | Manual 9.1648 |
| CI2 | `processarControladorWebServices()` faz dispatch explicito por servico | **Erro** | Manual 9.1442 |
| CI3 | `processarControladorAjax*()` faz dispatch explicito por acao | **Erro** | Manual 9.1363 |

## Guardrail Complementar (aviso)

| ID | Regra | Severidade | Base |
|---|---|---|---|
| CI4 | evitar payload sensivel em retorno de controlador | **Aviso** | hardening do projeto |

## Referencias Autoritativas

- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_9_eventos.md`
- `fontes/sei/src/main/php/sei/web/SeiIntegracao.php`
- `fontes/sei/src/main/php/sei/web/controlador_ajax.php`
- `fontes/sei/src/main/php/sei/web/controlador_ajax_externo.php`
- `fontes/sei/src/main/php/sei/web/controlador_ws.php`

## Exit Codes (`--exit-code`)

| Code | Significado |
|---|---|
| 0 | PASS |
| 1 | WARN |
| 2 | BLOCK |
