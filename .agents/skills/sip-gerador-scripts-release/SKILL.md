---
name: sip-gerador-scripts-release
description: Use when editing `fontes/sei/src/main/php/sip/scripts/*`, creating `instalarv*`, adding SIP resources, profiles, menus, audit bindings, parameters, or syncing SIP module versioning.
---

# Skill: Script de Release SIP

## Quando ativar

Ative esta skill quando a demanda envolver o script de release do SIP:
- novos recursos SIP
- vinculos com perfis
- itens de menu
- regra ou replicacao de auditoria
- parametros do SIP
- ajuste de `instalarv*`, `switch`, historico de versoes ou parametro de versao

## Quando nao ativar

- DDL estrutural do modulo no banco do SEI como foco principal
- validacoes de ativacao de modulo em `ConfiguracaoSEI` ou `class_exists(*Integracao)`

## Input minimo

Receba do desenvolvedor:

```text
modulo: <nome>
versao_de: X.Y.Z
versao_para: X.Y.Z
artefatos: [recursos | perfis | menus | auditoria | parametros | ambos]
referencia_estrutural: [padrao-ia | outra referencia explicita]
```

Se faltar informacao sobre perfis, menus, recursos ou escopo de auditoria, pergunte antes de gerar.

## Padrao estrutural

- Padrao primario de estrutura: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_ia.php`
- Referencia secundaria de validacao: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_relacionamento_institucional.php`
- Se o desenvolvedor informar outra referencia explicita, essa referencia passa a ser obrigatoria para a estrutura do script.
- Nao tratar referencia estrutural como exemplo ilustrativo. Tratar como restricao de implementacao.

### Estrutura esperada do arquivo

- `require_once dirname(__FILE__) . '/../web/Sip.php';`
- classe `*AtualizadorSipRN extends InfraRN`
- propriedades de classe para versao atual, nome do modulo, nome do parametro e historico de versoes
- `inicializarObjInfraIBanco()` retornando `BancoSip::getInstance()`
- metodos `inicializar()`, `logar()`, `finalizar()`
- metodo principal `atualizarVersaoConectado()`
- `switch` com `fallthrough` sobre a versao instalada
- metodos incrementais `instalarv*()`
- helper local no proprio script para `adicionarRecursoPerfil()`, `adicionarItemMenu()` e auditoria, salvo quando houver referencia estrutural diferente aprovada
- bootstrap final do script com `SessaoSip::getInstance(false)`, `BancoSip::getInstance()->setBolScript(true)`, autenticacao via `InfraScriptVersao::solicitarAutenticacao()` e chamada a `$objVersaoSipRN->atualizarVersao()`

### Literais obrigatorios do lado SIP

- sistema: `SEI`
- menu principal: `Principal`
- item de menu pai: usar exatamente o rotulo presente na referencia estrutural escolhida, inclusive acentuacao quando houver
- perfis base quando aplicavel: `Administrador` e `Basico`

### Bloqueios estruturais

- Bloquear se o script usar `InfraScriptVersao` como classe base sem autorizacao explicita do desenvolvedor.
- Bloquear se faltar `atualizarVersaoConectado()`.
- Bloquear se faltar `switch` incremental com `fallthrough`.
- Bloquear se faltar qualquer um dos metadados de versao: versao atual, nome do modulo, nome do parametro ou historico de versoes.
- Bloquear se recursos, perfis, menu e item de menu forem criados sem lookup previo.
- Bloquear se houver chamada a helper/metodo que nao exista no proprio arquivo, na classe pai ou no core confirmado.
- Bloquear se a estrutura final divergir da referencia estrutural escolhida sem desvio aprovado explicitamente.

## Regras de guarda

1. Se o modulo estiver mapeado em `.agents/references/mapa-modulos-scripts.md`, nao crie script novo; atualize o script SIP existente.
2. Nao use SQL bruto para criar recurso, perfil, menu ou vinculo quando existir RN/DTO equivalente.
3. So use SQL direto em auditoria como fallback controlado, apos tentar RN/DTO/helper.
4. Nao aplique regras de bootstrap ou ativacao do SEI em `sip/scripts/*`.

## Execucao

### 1. Carregar referencias

Leia nesta ordem:
- `.agents/references/padrao-modelagem-dados.md`
- `references/sip-update-script-rules.md`
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_ia.php`
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_relacionamento_institucional.php`

### 2. Resolver contexto SIP

- obtenha `SistemaRN`, `PerfilRN`, `MenuRN` e `ItemMenuRN` quando o fluxo exigir
- localize `SEI`, perfis-base e menus antes de criar vinculos
- valide os literais `Principal`, rotulo exato do item de menu pai, `Administrador` e `Basico` contra a referencia estrutural escolhida antes de escrever o script

### 3. Gerar ou ajustar `instalarv*`

- crie recursos de forma idempotente: consultar antes de cadastrar
- crie itens de menu de forma idempotente: consultar antes de cadastrar
- vincule perfil-recurso e perfil-item-menu apenas quando a relacao nao existir
- trate auditoria ao final; se nao houver helper claro, use fallback controlado
- em `instalarv100()`, siga o padrao do modulo IA para inserir o parametro inicial de versao em `infra_parametro`
- em upgrades posteriores, so use helper local de atualizacao de versao se ele existir e seguir o padrao do script de referencia

### 4. Atualizar metadados

- atualize `case '<versao_anterior>'` no `switch` com `fallthrough` incremental
- atualize `$versaoAtualDesteModulo`
- atualize `$historicoVersoes` ao final do array
- preserve os nomes e a ordem estrutural dos blocos do script de referencia, salvo desvio aprovado

### 5. Validar saida

- rode `php -l` no script SIP alterado
- se o script SIP gerado/alterado contiver DDL, rode `python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <script_sip> --mode release_check`
- confirme que nao houve duplicidade de recurso, menu, relacao ou auditoria
- confirme que a skill nao puxou responsabilidades do SEI para o SIP
- confirme que o script final continua no padrao estrutural da referencia escolhida
- confirme que os lookups de `SEI`, `Principal`, rotulo exato do item de menu pai, `Administrador` e `Basico` aparecem antes das criacoes dependentes

## Checklist

- [ ] script-alvo SIP correto localizado
- [ ] padrao estrutural do script definido e confirmado
- [ ] `BancoSip` e `SessaoSip` corretos
- [ ] classe base `InfraRN` preservada
- [ ] `atualizarVersaoConectado()` presente
- [ ] `switch` incremental com `fallthrough` presente
- [ ] helper local de recurso/menu/auditoria alinhado a referencia escolhida
- [ ] recursos criados com idempotencia
- [ ] menus criados com idempotencia
- [ ] vinculos de perfil sem duplicidade
- [ ] auditoria tratada por helper ou fallback controlado
- [ ] `sei-verificacao-banco-dados` executado no script SIP quando houver DDL gerado/alterado
- [ ] `switch`, historico e parametro de versao atualizados
- [ ] literais SIP e lookups validados contra a referencia escolhida, inclusive acentuacao quando aplicavel
