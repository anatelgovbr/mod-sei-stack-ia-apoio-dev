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

Cada regra e avaliada somente no metodo correspondente. CI1 nao aceita um
`preg_match` de outro metodo, CI2 nao aceita um `switch` fora do controlador de
WebServices e CI3 valida separadamente cada `processarControladorAjax*()`.

CI4 exige autorizacao no proprio `case` ou bloco compartilhado antes da
execucao. O recurso literal deve ser plausivel para o modulo, mas nao precisa
ser igual ao label do `case`. CI5 apenas sinaliza payload potencialmente
sensivel e nao substitui a autorizacao de CI4.

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
| 0 | PASS, com ao menos um metodo controlador analisado |
| 1 | WARN |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

---

## Testes

```bash
cd .agents/skills/sei-verificacao-controladores && python3 -m unittest test_audit
```

11 testes sobre `audit.py`. O arquivo e independente de proposito: nao importa helper de
outra skill nem de pasta compartilhada. A duplicacao de andaime e o preco de a skill
poder ser levada inteira para outro lugar.

Dois deles garantem **fail closed**: entrada inexistente, incompativel, vazia, ou
elegivel da qual o parser nada extraiu, tem de devolver BLOCK. Detector falha verde, e
sem essa garantia o auditor passa por cima do que nao conseguiu ler e ninguem percebe.

O resto se divide em dois grupos. Um fixa que cada regra realmente barra, com o codigo
de saida e a linha certa. O outro impede falso positivo, e cada um desses e um caso que
ja aconteceu. Falso positivo importa porque auditor que grita a toa e desligado pela
equipe, e ai o gate para de proteger tudo, nao so o caso barulhento.
