---
name: sei-gerador-scripts-release
description: Use when editing `fontes/sei/src/main/php/sei/scripts/*`, creating `instalarv*`, adding tables, columns, indices, sequences, DDL, seeds, or syncing `getVersao()` for SEI module release scripts.
---

# Skill: Script de Release SEI

## Quando ativar

Ative esta skill quando a demanda envolver o banco ou o script de release do SEI:
- novas tabelas do modulo
- novas colunas, PKs, FKs ou indices
- sequences de PK nativa
- seed tecnico ou negocial no SEI
- ajuste de `instalarv*`, `switch`, historico de versoes ou `getVersao()`

## Quando nao ativar

- recursos, perfis, menus e auditoria do SIP sem impacto no SEI
- criacao de modulo novo sem script existente, antes da fase de estrutura do modulo

## Input minimo

Receba do desenvolvedor:

```text
modulo: <nome>
versao_de: X.Y.Z
versao_para: X.Y.Z
artefatos: [tabelas | colunas | FKs | indices | sequences | seeds | ambos]
referencia_estrutural: [padrao-ia | outra referencia explicita]
```

Se houver nova tabela, exija especificacao suficiente de colunas, PK, FKs, sequence e seed inicial. Se faltar contrato minimo, pergunte antes de gerar.

## Padrao estrutural

- Padrao primario de estrutura: `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_ia.php`
- Referencia secundaria de validacao: `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_relacionamento_institucional.php`
- Se o desenvolvedor informar outra referencia explicita, essa referencia passa a ser obrigatoria para a estrutura do script.
- Nao tratar referencia estrutural como exemplo ilustrativo. Tratar como restricao de implementacao.

### Estrutura esperada do arquivo

- `require_once dirname(__FILE__) . '/../web/SEI.php';`
- classe `*AtualizadorSeiRN extends InfraRN`
- propriedades de classe para versao atual, nome do modulo, nome do parametro e historico de versoes
- `inicializarObjInfraIBanco()` retornando `BancoSEI::getInstance()`
- metodos `inicializar()`, `logar()`, `finalizar()`
- metodo principal `atualizarVersaoConectado()`
- `switch` com `fallthrough` sobre a versao instalada
- metodos incrementais `instalarv*()`
- bootstrap final do script com `SessaoSEI::getInstance(false)`, `BancoSEI::getInstance()->setBolScript(true)`, checagem de configuracao do modulo no SEI, `class_exists(*Integracao)`, autenticacao via `InfraScriptVersao::solicitarAutenticacao()` e chamada a `$objVersaoSeiRN->atualizarVersao()`

### Bloqueios estruturais

- Bloquear se o script usar `InfraScriptVersao` como classe base sem autorizacao explicita do desenvolvedor.
- Bloquear se faltar `atualizarVersaoConectado()`.
- Bloquear se faltar `switch` incremental com `fallthrough`.
- Bloquear se faltar qualquer um dos metadados de versao: versao atual, nome do modulo, nome do parametro ou historico de versoes.
- Bloquear se houver chamada a helper/metodo que nao exista no proprio arquivo, na classe pai ou no core confirmado.
- Bloquear se a estrutura final divergir da referencia estrutural escolhida sem desvio aprovado explicitamente.

## Regras de guarda

1. Se o modulo estiver mapeado em `.agents/references/mapa-modulos-scripts.md`, nao crie script novo; atualize o script SEI existente.
2. Nao gere tabela ou coluna com nome acima de 26 caracteres.
3. Nao gere sequence para tabela N:N com PK composta.
4. Nao gere chamadas com assinatura nao confirmada do core, como `tipoNumero(2)`.
5. Use SQL bruto apenas para `CREATE TABLE` ou quando nao houver helper equivalente no core.

## Execucao

### 1. Carregar referencias

Leia nesta ordem:
- `.agents/references/padrao-modelagem-dados.md`
- `references/sei-update-script-rules.md`
- `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_ia.php`
- `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_relacionamento_institucional.php`

### 2. Validar naming antes de gerar

- `len(nome_tabela) <= 26` -> permitido
- `len(nome_tabela) > 26` -> bloquear e pedir correcao
- `len('seq_' + nome_tabela) <= 30` -> permitido

### 3. Gerar ou ajustar `instalarv*`

- Use `CREATE TABLE` com tipos vindos de `InfraMetaBD::tipo*()`.
- Use `InfraMetaBD` para PK, FK, indices e alteracao de coluna.
- Prefira `criarSequencialNativa()` para sequence, preservando o estilo local do script quando necessario.
- Use RN/DTO/BD do core para seed e parametros quando a abstracao ja existir.
- Em `instalarv100()`, siga o padrao do modulo IA para inserir o parametro inicial de versao em `infra_parametro`.
- Em upgrades posteriores, so use helper local de atualizacao de versao se ele existir e seguir o padrao do script de referencia.

### 4. Atualizar metadados

- Atualize `case '<versao_anterior>'` no `switch` com `fallthrough` incremental.
- Atualize `$versaoAtualDesteModulo`.
- Atualize `$historicoVersoes` adicionando a nova versao ao final.
- Sincronize `getVersao()` na classe `*Integracao.php`.
- Preserve os nomes e a ordem estrutural dos blocos do script de referencia, salvo desvio aprovado.

### 5. Validar saida

- Rode `php -l` no script SEI alterado.
- Rode `python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <script_sei> --mode release_check` no script PHP gerado/alterado.
- Rode os gates de modelagem aplicaveis sobre o artefato gerado, nao sobre arquivos de documentacao da skill.
- Confirme que o script continua compativel com MySQL, SQL Server, Oracle e PostgreSQL.
- Confirme que o script final continua no padrao estrutural da referencia escolhida.
- Confirme que o bootstrap final contem as checagens de modulo configurado e `class_exists(*Integracao)` quando aplicavel ao lado SEI.

## Checklist

- [ ] script-alvo SEI correto localizado
- [ ] padrao estrutural do script definido e confirmado
- [ ] nomes dentro dos limites 26/30
- [ ] classe base `InfraRN` preservada
- [ ] `atualizarVersaoConectado()` presente
- [ ] `switch` incremental com `fallthrough` presente
- [ ] bootstrap final do script alinhado ao modulo IA
- [ ] `CREATE TABLE` com `InfraMetaBD::tipo*()`
- [ ] PK/FK/indice com helper do core
- [ ] sequence coerente com `TIPO_PK_NATIVA`
- [ ] seed idempotente
- [ ] `sei-verificacao-banco-dados` executado no script SEI gerado/alterado
- [ ] `switch`, historico e `getVersao()` sincronizados
- [ ] literais e checagens de bootstrap validados contra a referencia escolhida
