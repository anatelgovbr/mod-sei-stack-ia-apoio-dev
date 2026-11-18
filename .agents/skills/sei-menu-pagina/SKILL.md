---
name: sei-menu-pagina
description: Cria ou ajusta paginas e acoes de modulo e menus internos via SIP, com permissao e link assinado. Para menu externo/publicacoes ou extensoes por hook no core, use tambem `sei-mod-api-eventos`; siga a precedencia da matriz de roteamento.
---

# Skill: Menu + Página/Ação do módulo


## Fonte de verdade (detalhes)
- `references/sip-recursos-menus-perfis.md` (passo-a-passo SIP e ícones)
- `AGENTS.md` (permissão, link assinado e entrada HTTP)

## Checklist de implementação (sem duplicar detalhes)
1) **Decidir origem do menu**
- Menu interno do SEI: configurado no **SIP** (recurso/menu/perfil/permissão).
- Menu de usuario externo/publicacoes: usar `sei-mod-api-eventos`; usar esta skill para a pagina/acao do modulo consumida por esse menu.

2) **Permissão**
- Definir o recurso no SIP (ex.: `md_<instituicao/modulo>_<acao>`) e validar na ação.
- Para renderização condicional (botão/ícone/menu), usar `verificarPermissao`.
- Recursos de escrita (`_cadastrar`, `_alterar`, `_excluir`) devem ser incluídos na regra de auditoria SIP via `_cadastrarAuditoria` + `replicarRegraAuditoria`. Recurso `_listar` nunca entra na regra. Ver `.agents/references/padrao-auditoria-sip-sei.md`.

3) **Página/Ação**
- Entrar sempre por `controlador.php?acao=...` (ou padrão equivalente do módulo).
- No início: `validarLink()` e `validarPermissao()`.
- Parâmetros: normalizar tipos e aplicar whitelist/regex (negar por padrão).
- Se a apresentação visual for criada ou alterada, aplicar `.agents/references/padrao-acessibilidade-cores-sei.md` e validar os esquemas afetados.
- Em tela com filtro, formulário, barra de comandos ou grid, aplicar `.agents/references/padrao-interacao-telas-sei.md`: foco inicial, botão padrão do Enter, barra inferior, teclas de atalho e ordenação padrão do grid.
- Campo de autocompletar: pesquisar pelo campo de indexação, conforme `.agents/references/padrao-metodos-crud-infraphp.md`, seção "Pesquisa textual em autocompletar".
- Campo de arquivo (`fil*`): respeitar os limites de upload de `.agents/references/padrao-ambiente-modulo.md`.

4) **Ícone (menu interno)**
- Implementar `obterDiretorioIconesMenu` e usar SVG no diretório retornado.

## Saídas esperadas
- Item de menu funcionando (interno e/ou externo/publicações) + página/ação com controles mínimos.

## Limite de escopo

- Esta skill e principal para menu interno SIP, pagina do modulo, acao do modulo, link de acao e permissao da pagina quando nao houver escolha explicita de `sei-gerador-crud`, hook no core ou menu externo/publicacoes.
- Quando a entrega depender de hook em `*Integracao.php`, injecao de botao/icone em tela do core ou menu externo/publicacoes, `sei-mod-api-eventos` e principal, salvo se o desenvolvedor escolheu explicitamente `sei-gerador-crud`; nesse caso, o gerador e principal e a skill de eventos cobre o hook.
