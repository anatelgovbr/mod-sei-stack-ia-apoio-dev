---
name: sei-menu-pagina
description: Cria/ajusta menus internos via SIP e implementa a acao/pagina correspondente dentro do modulo, com permissao e link assinado. Para menu externo/publicacoes ou extensoes por hook no core, use `sei-mod-api-eventos`.
---

# Skill: Menu + Página/Ação do módulo


## Fonte de verdade (detalhes)
- `references/sip-recursos-menus-perfis.md` (passo-a-passo SIP e ícones)
- `AGENTS.md` (permissão, link assinado e entrada HTTP)

## Checklist de implementação (sem duplicar detalhes)
1) **Decidir origem do menu**
- Menu interno do SEI: configurado no **SIP** (recurso/menu/perfil/permissão).
- Menu de usuario externo/publicacoes: skill principal `sei-mod-api-eventos`; usar esta skill apenas para a pagina/acao do modulo consumida por esse menu.

2) **Permissão**
- Definir o recurso no SIP (ex.: `md_<instituicao/modulo>_<acao>`) e validar na ação.
- Para renderização condicional (botão/ícone/menu), usar `verificarPermissao`.
- Recursos de escrita (`_cadastrar`, `_alterar`, `_excluir`) devem ser incluídos na regra de auditoria SIP via `_cadastrarAuditoria` + `replicarRegraAuditoria`. Recurso `_listar` nunca entra na regra. Ver `.agents/references/padrao-auditoria-sip-sei.md`.

3) **Página/Ação**
- Entrar sempre por `controlador.php?acao=...` (ou padrão equivalente do módulo).
- No início: `validarLink()` e `validarPermissao()`.
- Parâmetros: normalizar tipos e aplicar whitelist/regex (negar por padrão).

4) **Ícone (menu interno)**
- Implementar `obterDiretorioIconesMenu` e usar SVG no diretório retornado.

## Saídas esperadas
- Item de menu funcionando (interno e/ou externo/publicações) + página/ação com controles mínimos.

## Limite de escopo

- Esta skill e principal para menu interno SIP, pagina do modulo, acao do modulo, link de acao e permissao da pagina.
- Quando a entrega depender de hook em `*Integracao.php`, injecao de botao/icone em tela do core ou menu externo/publicacoes, a skill principal passa a ser `sei-mod-api-eventos`.

