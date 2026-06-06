---
name: sei-menu-pagina
description: Cria/ajusta menus (interno via SIP; usuário externo/publicações via eventos) e implementa a ação/página correspondente dentro do módulo, com permissão e link assinado.
---

# Skill: Menu + Página/Ação do módulo


## Fonte de verdade (detalhes)
- `references/sip-recursos-menus-perfis.md` (passo-a-passo SIP e ícones)
- `AGENTS.md` (permissão, link assinado e entrada HTTP)

## Checklist de implementação (sem duplicar detalhes)
1) **Decidir origem do menu**
- Menu interno do SEI: configurado no **SIP** (recurso/menu/perfil/permissão).
- Menu de usuário externo/publicações: via eventos `montarMenuUsuarioExterno` / `montarMenuPublicacoes`.

2) **Permissão**
- Definir o recurso no SIP (ex.: `md_<instituicao/modulo>_<acao>`) e validar na ação.
- Para renderização condicional (botão/ícone/menu), usar `verificarPermissao`.

3) **Página/Ação**
- Entrar sempre por `controlador.php?acao=...` (ou padrão equivalente do módulo).
- No início: `validarLink()` e `validarPermissao()`.
- Parâmetros: normalizar tipos e aplicar whitelist/regex (negar por padrão).

4) **Ícone (menu interno)**
- Implementar `obterDiretorioIconesMenu` e usar SVG no diretório retornado.

## Saídas esperadas
- Item de menu funcionando (interno e/ou externo/publicações) + página/ação com controles mínimos.

