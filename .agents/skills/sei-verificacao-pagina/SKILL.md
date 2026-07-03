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

## Guardrails Locais do Projeto (avisos)

| ID | Regra | Severidade | Base |
|---|---|---|---|
| P5 | evitar `$_REQUEST` em pagina | **Aviso** | `AGENTS.md` |
| P6 | `$_GET`/`$_POST` diretos fora de `acao` exigem normalizacao explicita | **Aviso** | guardrail local |
| P7 | UI condicional usa `verificarPermissao()` quando aplicavel | **Aviso** | `references/padroes-seguranca.md` |
| P8 | saida HTML com variavel usa `PaginaSEI::tratarHTML()` quando aplicavel | **Aviso** | `references/padroes-seguranca.md` |
| P9 | evitar `innerHTML` / `document.write` com resposta ou variavel insegura | **Aviso** | hardening web complementar |
| P10 | evitar mutacao de estado via GET desprotegido | **Aviso** | hardening complementar alinhado a `assinarLink()` |

## Referencias Autoritativas

- `references/padroes-seguranca.md` (cobre P1-P10; curado dos cap. 3, 4 e 9 do manual)
- `AGENTS.md`

## Exemplo Aderente ao Manual

```php
try {
    SessaoSEI::getInstance()->validarLink();
    SessaoSEI::getInstance()->validarPermissao($_GET['acao']);

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
| 0 | PASS |
| 1 | WARN |
| 2 | BLOCK |
