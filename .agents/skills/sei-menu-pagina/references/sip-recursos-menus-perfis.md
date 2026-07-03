# SIP — Recursos, Menus e Perfis (para módulos)

Resumo do passo-a-passo do manual SEI-Módulos (v5.0) para menus internos.
Consultar esta referência ao criar ou ajustar menus, recursos ou perfis no SIP.

---

## Quando consultar

- Criar novo item de menu interno do SEI.
- Criar recurso para controle de permissão de uma ação.
- Criar ou ajustar perfil de módulo.
- Implementar ícone de menu.
- Preparar a pagina/acao do modulo consumida por menu de usuario externo ou publicacoes.

Para menu de usuario externo ou publicacoes como ponto de extensao no core, a
skill principal e `sei-mod-api-eventos`. Esta referencia continua util apenas para
os recursos SIP, pagina/acao do modulo e impactos de release relacionados.

---

## Verificar antes de criar

Antes de criar qualquer recurso, menu ou perfil, verificar se já existe estrutura
no módulo. Inspecionar:

```
fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/menu/
```

E os scripts de instalação já existentes em:
`.agents/references/mapa-modulos-scripts.md`

Nunca duplicar recursos, menus ou perfis já cadastrados nos scripts de release.

---

## 1) Recurso (SIP)

- Criar recurso em **Recursos > Novo**.
- Convenção obrigatória: `md_<instituicao/modulo>_<acao>` (tudo minúsculo, sem acento).
  - Exemplo: `md_anatel_sdd_listar`, `md_anatel_sdd_cadastrar`
- O recurso deve ser registrado no script de instalação/upgrade do SIP.

---

## 2) Item de menu (SIP)

- Montar menu em **Menus > Montar** associando o recurso criado acima.
- Um item de menu exige um recurso vinculado — sem recurso, sem menu.

### Ícone do menu

- O módulo deve implementar o evento `obterDiretorioIconesMenu`.
- Colocar o SVG no diretório retornado pelo evento.
- No campo "Ícone" do SIP: informar apenas o **nome do arquivo** (sem caminho).
- SVG deve estar em `svg/` ou em subdiretório retornado pelo evento — verificar
  o padrão do módulo antes de criar.

---

## 3) Perfil (SIP)

- Criar perfil em **Perfis > Novo**.
- Convenção obrigatória: `MD_<INSTITUICAO/MODULO>` (maiúsculo).
  - Exemplo: `MD_ANATEL_SDD`
- Perfil deve ser registrado no script de instalação/upgrade do SIP.

---

## 4) Montagem e permissão

1. Adicionar o recurso e item de menu no perfil em **Perfis > Montar**.
2. Atribuir o perfil a usuários/unidades conforme política da instalação.
3. Re-login no SEI para o menu aparecer.

---

## Menus fora do SIP

Usuario externo e pesquisa de publicacoes nao recebem menus do SIP.
Para esses casos, usar eventos na `*Integracao.php` com `sei-mod-api-eventos` como
skill principal:

- `montarMenuUsuarioExterno` — menu do portal do usuário externo.
- `montarMenuPublicacoes` — menu da pesquisa de publicações.

---

## Checklist antes de concluir

- [ ] Recurso criado com convenção `md_<inst/mod>_<acao>`
- [ ] Recurso registrado no script SIP de release
- [ ] Perfil criado com convenção `MD_<INST/MOD>`
- [ ] Perfil registrado no script SIP de release
- [ ] Item de menu vinculado ao recurso
- [ ] Ícone SVG adicionado (se menu interno)
- [ ] Ação PHP tem `validarPermissao` com o recurso correspondente
- [ ] Re-login testado: menu aparece para perfil correto

---

## Referências

- Gabarito mínimo: `fontes/sei/src/main/php/sei/web/modulos/abc/exemplo/`
- Gabarito robusto: `fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/`
- Fundamentos de permissão: `AGENTS.md`
- Eventos no core para menu externo/publicacoes: `.agents/skills/sei-mod-api-eventos/`
- Scripts de release SIP: `.agents/skills/sip-gerador-scripts-release/`
