---
name: sei-verificacao-pagina
description: >
  Skill padrao de validacao para paginas PHP SEI/SIP. Audita controles de
  pagina documentados no manual do SEI e guardrails locais do projeto:
  `validarLink`, `validarPermissao`, `assinarLink`, `verificarPermissao`,
  `PaginaSEI::tratarHTML`, compatibilidade de encoding com `.gitattributes` e
  heuristicas complementares de entrada/saida HTTP. Gate obrigatorio para
  qualquer pagina `*_lista.php` ou `*_cadastro.php`.

  Use quando:
  - nova pagina PHP criada ou alterada no modulo
  - code review de paginas existentes
  - gate automatico disparado por `sei-guardrails-modulo`
---

# sei-verificacao-pagina

## Escopo Padrao

- paginas `*_lista.php`, `*_cadastro.php`, `controlador.php`, `index.php`
- link assinado e permissao em pagina
- entrada HTTP e saida HTML no contexto da pagina
- compatibilidade de encoding do arquivo PHP

## Regras SEI Explicitas (bloqueantes)

| ID | Regra | Severidade | Base |
|---|---|---|---|
| P1 | `validarLink()` presente na entrada da pagina | **Erro** | `references/padroes-seguranca.md` |
| P2 | `validarPermissao()` presente na entrada da pagina | **Erro** | `references/padroes-seguranca.md` |
| P3 | arquivo sem BOM e compativel com conversao Latin-1 | **Erro** | `AGENTS.md` + `.gitattributes` |
| P4 | links de acao em HTML/JS usam `assinarLink()` | **Erro** | `references/padroes-seguranca.md` |

## Guardrails Locais do Projeto

| ID | Regra | Severidade | Base |
|---|---|---|---|
| P5 | uso confirmado de `$_REQUEST` em pagina | **Erro** | `AGENTS.md` + G5 |
| P6 | `$_GET`/`$_POST` diretos exigem normalizacao explicita | **Erro** | `AGENTS.md` + G5 |
| P7 | UI condicional usa `verificarPermissao()` quando aplicavel | **Aviso** | `references/padroes-seguranca.md` |
| P8 | saida HTML dinamica usa `PaginaSEI::tratarHTML()` ou tratamento documentado | **Erro** | `references/padroes-seguranca.md` + G7 |
| P9 | fonte dinamica alcanca `innerHTML` / `document.write` sem tratamento | **Erro** | hardening web complementar + G7 |
| P10 | mutacao de estado confirmada via GET | **Erro** | hardening complementar + G9 |

P1 e P2 devem cobrir cada acao e ocorrer nessa ordem. Uma validacao global antes
do `switch` cobre todas as acoes; quando ela nao existe, o auditor verifica cada
`case` que puder extrair. P4 examina todos os links de acao encontrados.

P7 permanece contextual. Em P9, um sink sem fluxo dinamico confirmado gera
`WARN`; fonte dinamica ligada ao sink gera `BLOCK`.

## Referencias Autoritativas

- `references/padroes-seguranca.md` (cobre P1-P10; curado dos cap. 3, 4 e 9 do manual)
- `AGENTS.md`

## Exemplo Aderente ao Manual

```php
try {
    SessaoSEI::getInstance()->validarLink();
    $strAcao = PaginaSEI::GET('acao');
    SessaoSEI::getInstance()->validarPermissao($strAcao);

    if (SessaoSEI::getInstance()->verificarPermissao('md_abc_acao')) {
        $strLink = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_acao');
    }
} catch (Exception $e) {
    PaginaSEI::getInstance()->processarExcecao($e);
}
```

## Exit Codes (`--exit-code`)

| Code | Significado |
|---|---|
| 0 | PASS, com ao menos uma pagina analisada |
| 1 | WARN |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |
