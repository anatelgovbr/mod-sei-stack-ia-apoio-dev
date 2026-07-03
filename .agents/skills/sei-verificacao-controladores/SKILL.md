---
name: sei-verificacao-controladores
description: >
  Skill padrao de validacao para controladores de integracao SEI em
  `*Integracao.php`. Audita regras de dispatch, autorizacao por acao/servico,
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

## Regras de validacao

| ID | Regra | Severidade | Base |
|---|---|---|---|
| CI1 | `tratarLinkSemAssinatura()` usa `preg_match` restritivo | **Erro** | `references/padroes-controladores.md` CI1 |
| CI2 | `processarControladorWebServices()` faz dispatch explicito por servico | **Erro** | `references/padroes-controladores.md` CI2 |
| CI3 | `processarControladorAjax*()` faz dispatch explicito por acao | **Erro** | `references/padroes-controladores.md` CI3 |
| CI4 | cada acao/servico sensivel valida permissao/autorizacao especifica antes de executar | **Erro** | `.agents/security/matriz-vulnerabilidades-sei.md` V03 |
| CI5 | evitar payload sensivel em retorno de controlador | **Aviso** | hardening do projeto |

## Referencias Autoritativas

- `references/padroes-controladores.md` (cobre CI1-CI5; curado das secoes 1363, 1442 e 1648 do cap. 9 do manual)
- `.agents/security/matriz-vulnerabilidades-sei.md`
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
