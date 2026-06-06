# Padroes de Seguranca de Pagina — Referencia Resumida

## Regras SEI Explicitas

### P1 — `validarLink()`
Base: `sei_modulos_manual_dev_3_consideracoes_previas.md`, secao `SessaoSEI`.

```php
SessaoSEI::getInstance()->validarLink();
```

### P2 — `validarPermissao()`
Base: `sei_modulos_manual_dev_3_consideracoes_previas.md` e
`sei_modulos_manual_dev_4_infraphp.md`.

```php
SessaoSEI::getInstance()->validarLink();
SessaoSEI::getInstance()->validarPermissao($_GET['acao']);
```

### P3 — compatibilidade Latin-1 sem BOM
Base: guardrail do repositório + `.gitattributes`.

### P4 — `assinarLink()` em links de acao
Base: `sei_modulos_manual_dev_3_consideracoes_previas.md` e exemplos do manual 9.

```php
$strLink = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_acao');
```

## Guardrails Locais do Projeto

### P5 — evitar `$_REQUEST`
Base: `AGENTS.md`.

### P6 — normalizacao explicita de `$_GET`/`$_POST`
Base: guardrail local do projeto.

### P7 — `verificarPermissao()` para UI condicional
Base: manual 3, uso recomendado para botoes e icones.

### P8 — `PaginaSEI::tratarHTML()` quando aplicavel
Base: exemplo oficial no manual 9.

### P9 — evitar `innerHTML` / `document.write` inseguros
Base: hardening complementar.

### P10 — mutacao de estado via GET exige revisao
Base: hardening complementar alinhado a `assinarLink()`.
