---
name: sip-gerador-scripts-release
description: Usar para editar `fontes/sei/src/main/php/sip/scripts/*`, criar `instalarv*`, adicionar recursos SIP, perfis, menus, vinculos de auditoria, parametros ou sincronizar versionamento do modulo SIP.
---

# Skill: Script de Release SIP

## Quando ativar

Ative esta skill quando a demanda envolver o script de release do SIP:
- novos recursos SIP
- alteracao, desativacao ou remocao controlada de recursos SIP
- vinculos com perfis
- alteracao ou remocao controlada de vinculos perfil-recurso e perfil-item-menu
- itens de menu
- alteracao, desativacao ou remocao controlada de itens de menu
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
- Variante estrutural existente no repositorio: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_pen.php`
- Se o desenvolvedor informar outra referencia explicita, essa referencia passa a ser obrigatoria para a estrutura do script.
- Nao tratar referencia estrutural como exemplo ilustrativo. Tratar como restricao de implementacao.

### Escolha da familia estrutural

- Se o modulo-alvo ja possui script SIP proprio, preservar a mesma familia estrutural do arquivo existente.
- Para modulo novo ou script novo sem historico, preferir a familia `*AtualizadorSipRN extends InfraRN` observada em IA/Relacionamento Institucional/Correios.
- A variante com `InfraScriptVersao` so deve ser usada quando o modulo-alvo ja seguir esse padrao consolidado ou quando o desenvolvedor exigir explicitamente compatibilidade com ele.

### Estrutura esperada do arquivo

- `require_once dirname(__FILE__) . '/../web/Sip.php';`
- classe principal alinhada a familia estrutural escolhida
- propriedades de classe para versao atual, nome do modulo, nome do parametro e historico de versoes
- `inicializarObjInfraIBanco()` retornando `BancoSip::getInstance()`
- fluxo incremental de versao preservado (`atualizarVersaoConectado()` ou adaptador equivalente)
- `switch` com `fallthrough` sobre a versao instalada
- metodos incrementais `instalarv*()` ou `instalarV*()` conforme a familia escolhida
- helper local no proprio script para recurso, item de menu, vinculos de perfil e auditoria, salvo quando houver referencia estrutural diferente aprovada
- bootstrap final compativel com a familia estrutural escolhida

### Literais obrigatorios do lado SIP

- sistema: `SEI`
- menu principal: `Principal`
- item de menu pai: usar exatamente o rotulo presente na referencia estrutural escolhida, inclusive acentuacao quando houver
- perfis base quando aplicavel: `Administrador` e `Basico`

### Bloqueios estruturais

- Bloquear se a estrutura final divergir da familia estrutural ja consolidada no modulo-alvo sem desvio aprovado explicitamente.
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
5. Trate manutencao SIP como escopo legitimo do release: criar, alterar, desativar e remover recurso/menu/vinculo de forma controlada e idempotente quando o script historico do modulo ja fizer isso.

## Execucao

### 1. Carregar referencias

Leia nesta ordem:
- `.agents/references/padrao-modelagem-dados.md`
- `references/sip-update-script-rules.md`
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_ia.php`
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_relacionamento_institucional.php`
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_pen.php` quando o modulo-alvo ja seguir familia baseada em `InfraScriptVersao`

### 2. Resolver contexto SIP

- obtenha `SistemaRN`, `PerfilRN`, `MenuRN` e `ItemMenuRN` quando o fluxo exigir
- localize `SEI`, perfis-base e menus antes de criar vinculos
- valide os literais `Principal`, rotulo exato do item de menu pai, `Administrador` e `Basico` contra a referencia estrutural escolhida antes de escrever o script

### 3. Gerar ou ajustar `instalarv*`

- crie recursos de forma idempotente: consultar antes de cadastrar
- crie itens de menu de forma idempotente: consultar antes de cadastrar
- vincule perfil-recurso e perfil-item-menu apenas quando a relacao nao existir
- quando a demanda for de manutencao, remova ou desative recursos/vinculos/itens apenas com lookup previo e limpando as relacoes dependentes observadas no script historico do modulo
- trate auditoria ao final: incluir na regra apenas recursos de escrita (`_cadastrar`, `_alterar`, `_excluir`; `_desativar`/`_reativar` quando aplicavel) — `_listar` nunca entra; chamar `replicarRegraAuditoria` obrigatoriamente apos criar ou atualizar a regra; se nao houver helper claro, usar fallback SQL controlado; ver `.agents/references/padrao-auditoria-sip-sei.md`
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
- [ ] familia estrutural do script definida e confirmada
- [ ] `BancoSip` e `SessaoSip` corretos
- [ ] classe base/adapter estrutural preservado conforme o modulo-alvo
- [ ] `atualizarVersaoConectado()` presente
- [ ] `switch` incremental com `fallthrough` presente
- [ ] helper local de recurso/menu/vinculo/auditoria alinhado a referencia escolhida
- [ ] recursos criados com idempotencia
- [ ] menus criados com idempotencia
- [ ] vinculos de perfil sem duplicidade
- [ ] remocoes ou desativacoes tratadas com lookup e limpeza de dependencias quando aplicavel
- [ ] auditoria tratada por helper ou fallback controlado
- [ ] `sei-verificacao-banco-dados` executado no script SIP quando houver DDL gerado/alterado
- [ ] `switch`, historico e parametro de versao atualizados
- [ ] literais SIP e lookups validados contra a referencia escolhida, inclusive acentuacao quando aplicavel
