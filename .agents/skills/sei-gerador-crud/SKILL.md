---
name: sei-gerador-crud
description: Gera 6 arquivos CRUD InfraPHP a partir de JSON padrao, usando o motor generate_from_contrato.py como fonte operacional e o gabarito TRF4 apenas como referencia estrutural, com guardrails obrigatorios de seguranca e release do projeto. Quando escolhida pelo desenvolvedor, esta skill tambem contempla a fase de release do modulo (scripts SEI/SIP, menu e sincronizacao de versao) quando aplicavel. Acionar somente com escolha explicita do desenvolvedor pelo gerador, ou por chamada de outra skill; nova tabela, nova entidade ou artefato CRUD sozinho nao aciona. Nao usar por roteamento automatico.
disable-model-invocation: false
---

# Gerador CRUD InfraPHP

## Proposito

Gera 6 arquivos CRUD InfraPHP (DTO, BD, RN, INT, lista, cadastro) com fidelidade estrutural ao padrao TRF4 e guardrails SEI.
Quando o modulo-alvo estiver mapeado e a entidade for nova, a fase de release (scripts SEI/SIP, item de menu e sincronizacao de versao) faz parte da entrega.
JSON de contrato: artefato interno. Construir internamente, resumir ao usuario, aguardar confirmacao antes de salvar ou usar. Se o usuario fornecer JSON proprio, validar antes de usar.
Nao gerar comentario de cabecalho institucional nos arquivos.

Fonte operacional do CRUD gerado:
- `generate_from_contrato.py` (monta DTO, BD, RN, INT, cadastro e lista N:N por codigo)
- `templates/lista.php.tpl` (unico template lido pelo motor; vale para a lista de entidade simples)

Fonte de referencia estrutural:
- `references/gabarito-trf4.md` (resumo, convencoes e a tabela de desvios conscientes)
- `references/gabarito-trf4/` (saida do Gerador de Codigo TRF4 1.46.4 para o dominio `md_abc`, com os ajustes descritos no resumo)

Regra: o gabarito TRF4 serve para comparacao estrutural e validacao de padrao. Nao usar o gabarito como template literal, nem copiar nomes, textos, identificadores ou detalhes de dominio do exemplo. Onde o gabarito e o projeto divergem, o projeto prevalece e o desvio esta registrado em `references/gabarito-trf4.md`, secao "Desvios conscientes do gabarito".

## Preflight obrigatorio

Ler as referencias principais antes de definir nomes fisicos ou release:
- `references/gabarito-trf4.md`
- `.agents/references/padrao-modelagem-dados.md`
- `.agents/references/padrao-auditoria-sip-sei.md`
- `references/mapeamento-tipos-e-widgets.md`

## Guard de assets existentes

Antes de criar ou sugerir arquivos CSS/JS para o modulo-alvo, verificar:

- Se `modulos/<nome>/css/` ja contiver arquivos: **nao criar novos arquivos CSS**. Orientar edicao dos existentes.
- Se `modulos/<nome>/js/` ja contiver arquivos: **nao criar novos arquivos JS**. Orientar edicao dos existentes.
- A mesma regra vale para arquivos PHP de asset na raiz do modulo (`*_css.php`, `*_js.php`): se existirem, editar, nao criar.

## Textos exibidos ao usuario

- Textos padrao universais do CRUD saem acentuados pelo gerador: `Ações`, `Operação realizada com sucesso.`, `Ação ... não reconhecida.`, `inválido`, `desativação`, `reativação`, `exclusão`, `não encontrado(a)`.
- Textos de dominio (singular, plural, rotulos, titulos, captions, `title`, `alt`): nao inferir; devem vir no contrato. Se ausentes ou sem acento, alertar o desenvolvedor antes de entregar.
- Concordancia: `entidade.artigo` rege as mensagens da entidade (`Nova`, `cadastrada`, `não encontrada`); `ui.campos.<coluna>.artigo` rege as mensagens da coluna (`não informada`, `inválida`, `Informe a ...`). Sem artigo por coluna, o gerador usa o masculino.

---

## Tres caminhos de execucao

Identificar o caminho pelo contexto. Ordem de deteccao: C > A > B.

### Caminho A: documentacao disponivel

Use quando existir qualquer artefato pre-escrito sobre a entidade (spec, plano, data-model, task ou descricao estruturada).

1. Ler o artefato disponivel e extrair: nome da tabela, colunas, relacoes FK, campo principal, labels de UI.
2. Validar os nomes fisicos antes de propor o contrato:
   - PK gerada por sequence nativa: `id_<nome_tabela_completo>`
   - FK: preferir o nome da PK da tabela de origem; nome diferente e aceito quando houver papeis distintos (origem e destino) e gera alerta
   - N:N: preferir `md_<sigla>_rel_<entidade_a>_<entidade_b>`; outro nome gera alerta, nao bloqueio
3. Se houver lacunas pontuais (ex: tamanho de coluna, artigo, tecla de atalho), perguntar apenas o que falta, em rodadas de no maximo 3 perguntas por vez, repetindo quantas rodadas forem necessarias ate nao restar nenhuma duvida obrigatoria.
4. Construir o JSON internamente (nao mostrar ao usuario a menos que ele peca).
5. Apresentar um resumo curto do contrato e aguardar confirmacao explicita do desenvolvedor.
6. Salvar o contrato em arquivo para executar o gerador (`specs/<feature>/crud-contratos/<tabela>.json` em fluxo Spec Kit; `tmp/crud-contratos/<tabela>.json` fora dele).
7. Executar o gerador (ver secao "Execucao").
8. Apos os gates verdes, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

### Caminho B: descricao em linguagem natural

Use quando nao houver artefato pre-escrito sobre a entidade e o usuario descrever a entidade livremente.

Perguntar somente o necessario, na ordem da tabela, parando ao ter o suficiente:

| # | O que perguntar | Quando pular |
|---|----------------|-------------|
| 1 | Nome da tabela fisica (`md_<inst>_<entidade>` ou `md_<inst>_rel_<a>_<b>` para N:N) e modulo-alvo | Se ja informado |
| 2 | Colunas: nome, tipo, tamanho (para varchar), obrigatorio, precisao e escala (para numeric) | Se descricao ja cobre |
| 3 | Existe FK para outra tabela? Qual e o campo de exibicao no pai e qual helper `montarSelect*` existe na INT do pai? | Se nao ha relacao |
| 4 | A entidade tem exclusao logica (`sin_ativo`)? | Se ja confirmado |
| 5 | Qual coluna identifica o registro na listagem? (campoPrincipal) | Se ja confirmado |
| 6 | Rotulo, tecla de atalho e artigo de cada campo | Se o artefato ja traz |
| 7 | Ja existem scripts de instalacao do modulo? Informar nome ou caminho | Se o modulo for novo ou scripts forem detectados automaticamente |

O contrato JSON gerado internamente DEVE incluir a chave `regrasGeracao` com `campoSinAtivo` igual a `"sin_ativo"` quando houver exclusao logica, ou `null` quando nao houver. O gerador rejeita o contrato simples sem essa chave.

Apos coletar o suficiente:
- Construir o JSON internamente.
- Apresentar um **resumo de 3 linhas** (tabela, campos, flags ativas) e perguntar se pode prosseguir; nao mostrar o JSON completo a menos que o usuario peca.
- Salvar o contrato em arquivo para executar o gerador.
- Executar o gerador (ver secao "Execucao").
- Apos os gates verdes, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

### Caminho C: JSON pronto

Use quando o usuario fornecer um arquivo JSON, caminho ou bloco JSON compativel.

1. Se o desenvolvedor pedir um modelo, apontar para `examples/README.md` (esquema completo) e para os contratos em `examples/`.
2. Validar o JSON (ver secao "Validacoes obrigatorias").
3. Executar o gerador diretamente.
4. Apos os gates verdes, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

---

## Execucao

Apos ter o JSON salvo em arquivo:

```bash
python3 .agents/skills/sei-gerador-crud/generate_from_contrato.py \
  <caminho/contrato.json> <diretorio_saida> [--niveis N]
```

Diretorio de saida: o modulo-alvo em `fontes/sei/src/main/php/sei/web/modulos/<instituicao>/<modulo>/` (ou `modulos/<modulo>/` nos modulos de um nivel).

**Estrutura de saida**: o motor grava direto na estrutura final do manual: `dto/<Classe>DTO.php`, `bd/<Classe>BD.php`, `rn/<Classe>RN.php`, `int/<Classe>INT.php` e as paginas `<tabela>_lista.php` e `<tabela>_cadastro.php` na raiz do diretorio informado. Nenhum arquivo existente e sobrescrito; se algum dos 6 ja existir, o motor para com erro.

**Profundidade do `require_once`**: o motor deriva a quantidade de `..` ate `web/SEI.php` do proprio diretorio de saida quando ele esta em `web/modulos/` (`modulos/<inst>/<modulo>/` = 3 niveis para paginas e 4 para classes; `modulos/<modulo>/` = 2 e 3). Fora dessa arvore (ex.: `tmp/`), usa 3 e emite alerta; passar `--niveis` para outro leiaute. Use `tmp/<tabela>/` apenas quando o desenvolvedor pedir explicitamente para testar antes de integrar.

O motor imprime um JSON com `generated_files`, `niveis`, `flags` (`temSinAtivo`, `temFk`, `numeroFks`, `nn`) e `developer_alerts`. Reportar ao desenvolvedor:
- 6 arquivos gerados com seus caminhos.
- Resultado dos gates (abaixo).
- Flags aplicadas e alertas do motor (FK fora do padrao de nome, `numeric` sem `din_`, helper INT nao localizado, N:N sem `_rel_`, saida fora de `web/modulos/`).
- Limitacoes observadas para esta entidade especifica.

### Gates obrigatorios apos a geracao

Rodar, nesta ordem, sobre o diretorio gerado. Qualquer erro bloqueia a entrega; corrigir o gerador ou o contrato antes de ajustar manualmente o CRUD gerado.

```bash
for f in <saida>/*.php <saida>/dto/*.php <saida>/bd/*.php <saida>/rn/*.php <saida>/int/*.php; do php -l "$f"; done
python3 .agents/skills/sei-verificacao-rn/audit.py --input <saida>/rn --format markdown --exit-code
python3 .agents/skills/sei-verificacao-pagina/audit.py --input <saida>/<tabela>_lista.php,<saida>/<tabela>_cadastro.php --pagina nova --format markdown --exit-code
python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <saida> --mode audit --type php --format markdown --exit-code
```

Avisos esperados e aceitos: `P007` no cadastro (botoes Salvar e Cancelar sem `verificarPermissao`, mesmo idioma do core; a acao ja passou por `validarPermissao`) e `W001`/`DB09` (indice por FK, criado por `adicionarChaveEstrangeira` na Fase de Release). Depois dos auditores, rodar `sei-validacao-padrao` conforme `.agents/references/roteamento-de-skills.md`.

Conferencia manual complementar:
- paginas usam `$strAcao = PaginaSEI::GET('acao')`, `validarPermissao($strAcao)` e `switch ($strAcao)`; nenhum `$_GET` ou `$_POST` direto.
- saida dinamica usa `PaginaSEI::tratarHTML(...)` em celulas, atributos `value` e campos hidden; `adicionarMensagem` recebe texto cru, porque `InfraPagina::montarMensagens` ja escapa.
- identificadores de GET, POST e selecao passam por `ctype_digit` ou `(int)`; listas N:N validam o ID composto com `count(...)==2` e `ctype_digit(...)`.
- helpers INT de entidades com `sin_ativo` filtram ativos por padrao (via `configurarExclusaoLogica`) e incluem o item selecionado mesmo inativo.
- `numeric` com `din_` valida com `InfraUtil::validarDin` sem alterar o valor; `dth_` valida com `InfraData::validarDataHora` e usa `infraMascaraDataHora` no cadastro.

---

## Fase de Release

Executar esta fase apos os gates verdes em todos os arquivos gerados.

### Verificacao obrigatoria no mapa

Consultar `.agents/references/mapa-modulos-scripts.md` para o modulo-alvo:

- **Modulo esta no mapa**: atualizacao dos scripts obrigatoria como parte desta skill. Nao perguntar se o desenvolvedor quer incluir release no escopo; informar que faz parte da entrega e perguntar apenas a versao-alvo quando nao estiver definida no contexto.
- **Modulo nao esta no mapa**: verificar fisicamente em `sei/scripts/` e `sip/scripts/` (nomes podem divergir do padrao convencional). Se encontrado, tratar como mapeado. Se confirmada ausencia: oferecer criacao via `sei-gerador-scripts-release` e `sip-gerador-scripts-release`, conforme escopo.
- **Modulo novo**: confirmar que existe a classe `Md<Sigla>Integracao.php` com `getVersao()`; sem ela o SEI nao carrega o modulo (`sei/web/SEI.php`). Sua criacao segue `sei-guardrails-modulo` (linha "Novo modulo" do roteamento).

### Quando os scripts existem: atualizacao incremental (obrigatoria)

Seguir `sei-gerador-scripts-release` e `sip-gerador-scripts-release` como procedimento, com `.agents/references/padrao-scripts-release.md` para os padroes de codigo concretos (DDL multi-SGBD, sequences, FKs, indices, boilerplate SIP) e `sei-menu-pagina` para o item de menu.

Propor a proxima versao (bump de **minor** por padrao para nova entidade) e aguardar confirmacao do desenvolvedor antes de alterar qualquer arquivo.

Apos confirmacao, gerar e inserir nos scripts existentes:

1. `case '<versaoAtual>': $this->instalarv<XYZ>();` no switch de ambos os scripts (sem `break`; fallthrough intencional; `break` migra para o novo ultimo case).
2. Metodo `instalarv<XYZ>()` no SEI com DDL multi-SGBD: tabela (comentarios de tabela e coluna a partir do contrato), sequence `seq_<tabela>` no CRUD simples (N:N nao tem sequence), FKs via `adicionarChaveEstrangeira` (inclusive a FK para `unidade` quando houver `escopoUnidade`), que ja cria o indice com o nome da FK (manual cap. 5), e chamada a `atualizarNumeroVersao()`.
3. Metodo `instalarv<XYZ>()` no SIP com lookup antes de cada cadastro (idempotencia), `adicionarRecursoPerfil()` por recurso, item de menu para a acao `<tabela>_listar` (sem ele a lista fica inacessivel) e chamada a `atualizarNumeroVersao()`.
4. Sincronizar `getVersao()` na classe `*Integracao.php` do modulo com a mesma versao aplicada nos scripts.
5. Criar ou atualizar regra de auditoria no SIP: incluir apenas os recursos de escrita (`_cadastrar`, `_alterar`, `_excluir`; adicionar `_desativar`/`_reativar` quando `temSinAtivo == true`). Recursos de leitura nunca entram na regra. Chamar `replicarRegraAuditoria` ao final. Ver `.agents/references/padrao-auditoria-sip-sei.md`.

Atualizar em ambos os scripts:
- `$versaoAtualDesteModulo = '<novaVersao>'`
- `$historicoVersoes`: adicionar `'<novaVersao>'` ao final do array

**Recursos SIP a registrar por entidade:**

| Condicao             | Recursos                                                                                   |
|----------------------|-------------------------------------------------------------------------------------------|
| Sempre               | `_cadastrar`, `_alterar`, `_consultar`, `_listar`, `_excluir`, `_selecionar`              |
| `temSinAtivo == true`| Adicionar `_desativar`, `_reativar`                                                       |

`_consultar` e auditado pela RN em `consultarConectado` e `bloquearControlado` e e a acao da pagina de consulta; `_listar` e auditado em `listarConectado` e `contarConectado`.

**Regra de auditoria SIP, recursos incluidos:**

| Condicao             | Entra na regra de auditoria                        |
|----------------------|----------------------------------------------------|
| Sempre               | `_cadastrar`, `_alterar`, `_excluir`               |
| `temSinAtivo == true`| Adicionar `_desativar`, `_reativar`                |
| Nunca                | `_listar`, `_consultar`, `_selecionar`             |

Perfil `Basico`: nao vincular por padrao. Vincular apenas quando a spec disser explicitamente que a funcionalidade e acessivel a todos os usuarios internos.

Validar apos edicao (script de release legado que abre com `<?` recebe a troca para `<?php` antes do lint; com `short_open_tag=Off` o `php -l` trata arquivo `<?` como texto e passa sem analisar):

```bash
php -l fontes/sei/src/main/php/sei/scripts/<script_sei>.php
php -l fontes/sei/src/main/php/sip/scripts/<script_sip>.php
python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input fontes/sei/src/main/php/sei/scripts/<script_sei>.php --mode release_check --exit-code
```

### Quando os scripts nao existem: delegar

Scripts novos completos estao fora do escopo desta skill. Orientar o desenvolvedor a usar `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` fornecendo:
- O contrato JSON da entidade como insumo para modelagem inicial
- Nome do modulo, instituicao e versao inicial desejada (`1.0.0` por padrao)

---

## Validacoes obrigatorias antes de gerar

O motor aplica todas com mensagem clara (sem traceback). Esquema completo em `examples/README.md`.

1. JSON sintaticamente valido, com `entidade` (`tabela`, `singular`, `plural`, `artigo` em `o` ou `a`, `campoPrincipal`, `comentario`) e `colunas` nao vazia.
2. CRUD simples: exatamente uma coluna com `chavePrimaria: true`, chamada `id_<tabela>`, e `regrasGeracao.campoSinAtivo` presente (`"sin_ativo"` ou `null`); N:N: exatamente duas PKs e `relacionamentosNn` com 2 entradas.
3. `entidade.campoPrincipal` referencia uma coluna existente em `colunas`.
4. Nomes fisicos: lowercase + digits + underscore, max 26 chars; tabela com prefixo `md_<sigla>_`.
5. Tabela e todas as colunas possuem `comentario` negocial preenchido; toda coluna tem `obrigatorio` booleano.
   Textos exibidos (`singular`, `plural`, `comentario`, `rotulo`) aceitam apostrofo, que o motor escapa nos literais PHP e JavaScript; `"`, `\`, `<`, `>`, `&`, caractere de controle e `*/` sao rejeitados com mensagem.
6. Tipos no subconjunto suportado: `int`, `integer`, `varchar`, `datetime`, `date`, `timestamp`, `char`, `numeric`. `timestamp` exige `dth_`; `date` nao aceita `dth_`; `sta_*` e rejeitado.
7. `campoSinAtivo`, quando informado, e `sin_ativo` e a coluna existe com tipo `char`.
8. Relacionamentos: `coluna` existe em `colunas`, `campoExibicao` informado, `tipoFk` coerente com `obrigatorio` da coluna; o helper `<Classe>INT::montarSelect<CampoExibicao>` existe em `web/int/` ou no `int/` do modulo (classe encontrada sem o metodo bloqueia; classe ausente gera alerta).
9. `ui.ordemFormulario`, quando presente, contem toda coluna de formulario; `ui.campos.<coluna>.teclaAtalho` nao usa tecla reservada (`S`, `C`, `F`; em FK tambem `N`, `E`, `T`, `R`).
10. Nenhum dos 6 arquivos-alvo ja existe no diretorio de saida (no-overwrite).

---

## Regras de derivacao

### Nomes de classe e arquivo

| Entrada | Regra | Exemplo |
|---------|-------|---------|
| `entidade.tabela` | PascalCase | `md_abc_projeto` vira `MdAbcProjeto` |
| classeBase + camada | sufixo da camada | `MdAbcProjetoDTO.php`, `MdAbcProjetoBD.php` |
| `{tabela}_lista.php` | nome fisico | `md_abc_projeto_lista.php` |
| `{tabela}_cadastro.php` | nome fisico | `md_abc_projeto_cadastro.php` |

### Prefixos de atributo DTO

| Tipo de banco | Prefixo | Exemplo coluna | Atributo DTO |
|--------------|---------|----------------|-------------|
| `int`, `integer` | `Num` | `id_md_abc_projeto` | `NumIdMdAbcProjeto` |
| `varchar` | `Str` | `identificacao` | `StrIdentificacao` |
| `date` / `datetime` + coluna `dta_*` | `Dta` | `dta_cadastramento` | `DtaCadastramento` |
| `timestamp` / `datetime` + coluna `dth_*` | `Dth` | `dth_entrega` | `DthEntrega` |
| `char(1)` | `Str` | `sin_ativo` | `StrSinAtivo` |
| `numeric` + coluna `din_*` | `Din` | `din_custo` | `DinCusto` |
| `numeric` sem `din_` | `Dbl` | `percentual` | `DblPercentual` |

Normalizacao: prefixos semanticos (`num_`, `str_`, `din_`, `dbl_`, `dta_`, `dth_`) sao removidos antes do PascalCase para evitar duplicacao (ex: `dta_` nao vira `DtaDta`).
O discriminador `Dta` vs `Dth` e determinado pelo nome da coluna: prefixo `dth_` vira `Dth`; qualquer outro tipo de data vira `Dta`.

Atributo relacionado (FK): `<CampoExibicao><SufixoDaFkSemId>`; `id_md_abc_projeto` + `identificacao` vira `StrIdentificacaoMdAbcProjeto` (igual ao gabarito) e `id_unidade_origem` + `sigla` vira `StrSiglaUnidadeOrigem`. A segunda FK para a mesma tabela recebe alias SQL (`unidade u2`, `u2.sigla`, `u2.id_unidade`).

### Elementos HTML

| Tipo | Prefixo HTML | Exemplo |
|------|-------------|---------|
| `varchar`, `datetime`, `date`, `timestamp`, `numeric`, `char` | `txt` | `txtIdentificacao` |
| FK | `sel` + sufixo da FK sem `Id` | `selMdAbcProjeto`, `selUnidadeOrigem` |
| campo oculto | `hdn` | `hdnIdMdAbcProjeto` |
| imagem calendario | `imgCal` | `imgCalCadastramento` |

### Acoes

Padrao: `{tabela}_{operacao}`; ex: `md_abc_projeto_cadastrar`, `md_abc_projeto_alterar`.

---

## Regras condicionais obrigatorias

### Quando existe `sin_ativo`

- DTO: `configurarExclusaoLogica('SinAtivo', 'N')`.
- RN: `desativarControlado()`, `reativarControlado()`, `bloquearControlado()` **ativos**.
- INT: `adicionarCriterio(...)` para incluir item selecionado mesmo inativo; o filtro de ativos vem de `configurarExclusaoLogica`.
- lista: modelo inline, desvio consciente do gabarito (que abre tela propria de reativacao): lista unica com `setBolExclusaoLogica(false)`, inativos em `trVermelha`, icones e botoes de desativar e reativar na propria lista, sem `acao_confirmada`; na selecao (`_selecionar`) so ativos. Referencia real: `trf4/julgamento/motivo_ausencia_lista.php`.

### Quando NAO existe `sin_ativo`

- Os blocos acima sao gerados em comentario com o mesmo conteudo do modo ativo (cases, flags, botoes, icones, JavaScript e metodos da RN), **nunca omitidos**, como o gabarito TRF4. `$bolAcaoDesativar` e `$bolAcaoReativar` ficam em `false`.
- Referencia padrao: `md_abc_aquisicao`.

### Quando existe FK (uma ou mais)

- DTO: `adicionarAtributoTabelaRelacionada(...)` e `configurarFK(...)` para cada FK.
- FK obrigatoria: `InfraDTO::$TIPO_FK_OBRIGATORIA`; FK opcional (`tipoFk: opcional` e `obrigatorio: false`): `InfraDTO::$TIPO_FK_OPCIONAL`, `infraLabelOpcional`, sem checagem no JavaScript e RN aceitando vazio como `null`.
- Filtro de FK: preferir `InfraDTO::$FILTRO_FK_ON`; usar `InfraDTO::$FILTRO_FK_WHERE` apenas quando necessario (`filtroFk: where`).
- INT: `montarSelect{CampoPrincipal}(..., $numId<SufixoDaFk>='')` com parametro por FK.
- cadastro: `<select>` populado via `<ClassePai>INT::montarSelect<CampoExibicao>`, `salvarCamposPost` com todos os selects.
- lista: filtro persistido com dropdown por FK.
- FK para tabela do core (`usuario`, `unidade`, `procedimento`): o helper precisa existir em `web/int/` com o nome derivado de `campoExibicao` (ex.: `UnidadeINT::montarSelectSigla`); o motor confere.

### Regras opcionais em `regrasGeracao` e nas colunas

| Chave | Efeito no CRUD gerado | Idioma de referencia |
|---|---|---|
| `regrasGeracao.paginacao` (padrao `true`) | lista com `prepararPaginacao` e `processarPaginacao` ativos; `false` deixa as duas linhas comentadas como no gabarito | `sei/web/serie_lista.php` |
| `regrasGeracao.escopoUnidade: "<coluna int>"` | a coluna recebe `SessaoSEI::getInstance()->getNumIdUnidadeAtual()` no cadastrar, no alterar e antes de consultar; lista e helper INT filtram pela unidade atual; DTO ganha `configurarFK` para `unidade` e atributo relacionado `Sigla<Sufixo>`; a coluna nao entra no formulario nem em `relacionamentos`; RN valida a coluna como obrigatoria com rotulo "Unidade" | `trf4/julgamento/destaque_cadastro.php` |
| `colunas[].unico: true` | validador da coluna consulta outro registro com o mesmo valor (`OPER_DIFERENTE` na PK, que vira `IS NOT NULL` no cadastro) e, com `sin_ativo`, distingue ocorrencia ativa de inativa; com `escopoUnidade`, a unicidade vale dentro da unidade | `trf4/julgamento/rn/MotivoAusenciaRN.php` |
| `regrasGeracao.dependentes: [{tabela, coluna, rotulo, artigo}]` | `excluirControlado` e `desativarControlado` chamam `contar` na RN filha e lancam validacao quando ha registro dependente | `trf4/julgamento/rn/MotivoAusenciaRN.php` |

Nenhuma das quatro vale para N:N. `unico` nao se aplica a PK nem a coluna de escopo.

### Quando ha PK composta (entidade N:N)

Detectado automaticamente quando existem 2 colunas com `chavePrimaria: true`. O contrato **deve** incluir `relacionamentosNn` (array de 2 entradas):

```json
"relacionamentosNn": [
  { "tabelaOrigem": "md_ri_filme", "classeInt": "MdRiFilmeINT", "metodoInt": "montarSelectTitulo", "rotulo": "Filme", "artigo": "o", "teclaAtalho": "I" },
  { "tabelaOrigem": "md_ri_ator",  "classeInt": "MdRiAtorINT",  "metodoInt": "montarSelectNome",   "rotulo": "Ator", "artigo": "o", "teclaAtalho": "A" }
]
```

Diferencas em relacao ao CRUD simples:

- DTO: duas `configurarPK(..., $TIPO_PK_INFORMADO)` em vez de uma PK nativa; sem `configurarExclusaoLogica`.
- RN: as duas PKs recebem validador de obrigatoriedade; desativar/reativar/bloquear sempre comentados.
- INT: helper `montarSelect<CampoExibicaoDaPrimeiraFk>` recebe as duas PKs como filtros opcionais; e esqueleto para composicao, porque o valor do select e a primeira PK.
- lista: IDs compostos com `explode('-', $strId)`; indices `[0]` e `[1]` com validacao `count(...)==2` e `ctype_digit(...)` (o gabarito TRF4 usa `[1]` e `[2]`, desvio registrado); colunas relacionadas exibidas com `tratarHTML` e `getThOrdenacao`.
- cadastro: dois `<select>` FK com `hdn<SufixoDaPk>` ocultos, rotulos e teclas de `relacionamentosNn`, campos extras com `ui.campos`.
- `regrasGeracao.campoSinAtivo` deve ser `null` (sin_ativo nao faz sentido em N:N).

---

## Guardrails SEI obrigatorios (todo arquivo de pagina)

- caminho relativo coerente com a camada final do modulo, derivado pelo motor: classes em `dto/`, `bd/`, `rn/`, `int/` usam um `..` a mais que as paginas da raiz do modulo.
- entrar por `controlador.php?acao=...` e tratar `acao` como parametro obrigatorio
- `session_start();`
- `SessaoSEI::getInstance()->validarLink();` como primeira validacao do bloco `try`
- `$strAcao = PaginaSEI::GET('acao');` seguido de `SessaoSEI::getInstance()->validarPermissao($strAcao);`
- `SessaoSEI::getInstance()->assinarLink(...)` em todos os links/redirects
- `PaginaSEI::tratarHTML(...)` em toda saida HTML
- a pagina submete para ela mesma via `controlador.php`
- RN: `SessaoSEI::getInstance()->validarAuditarPermissao(...)` em cada metodo; BD instanciada com `$this->getObjInfraIBanco()`
- Escrita: `*Controlado` (inclusive `bloquear`); Leitura: `*Conectado`
- toda comunicacao entre camadas deve trafegar via DTO
- uma RN nao pode chamar a BD de outra classe
- nao deve haver comunicacao direta entre BDs
- uma BD nao pode persistir ou atualizar mais de uma tabela
- e-mail, integracao externa, indexacao e processamento demorado devem ficar fora da transacao principal

---

## Checklist por camada

### DTO
- docblock com `@table` e `@column` a partir dos comentarios do contrato
- `extends InfraDTO`
- `getStrNomeTabela()` retorna a tabela fisica
- `adicionarAtributoTabela(...)` para cada coluna
- `adicionarAtributoTabelaRelacionada(...)` apenas quando houver FK
- `configurarFK(...)` para cada FK mapeada no DTO
- `configurarPK(...)` com `InfraDTO::$TIPO_PK_NATIVA` para tabelas funcionais com `seq_<tabela>`
- `configurarExclusaoLogica(...)` somente quando houver `sin_ativo`

### BD
- `extends InfraBD`
- construtor unico delegando a `parent::__construct($objInfraIBanco)`

### RN
- Docblock `@method` na classe e `@param`, `@return`, `@throws` por metodo
- Validadores privados por campo (`validarStr*`, `validarNum*`, `validarDta*`, `validarDth*`, `validarDin*`, `validarDbl*`), com unicidade quando `unico: true`
- `cadastrarControlado`, `alterarControlado` (com guards `isSet*()`), `excluirControlado`
- `consultarConectado` e `bloquearControlado` com `_consultar`; `listarConectado` e `contarConectado` com `_listar`
- Ancoras `//Regras de Negocio` nos metodos sem validador
- Blocos de desativar/reativar/bloquear ativos ou comentados conforme `sin_ativo`

### INT
- `extends InfraINT`
- Helper `montarSelect{CampoPrincipal}(...)` com ordenacao ascendente e `@throws InfraException`
- Parametro FK por relacionamento quando aplicavel
- Bloco `adicionarCriterio(sin_ativo OR pk)` apenas quando houver `sin_ativo`

### lista
- switch/case por acao
- `$bolCheck = false;` antes das flags de acao
- Filtro persistido em sessao para cada FK
- Tabela com acoes assinadas (consultar, alterar, desativar/reativar, excluir)
- JS de confirmacao para acoes destrutivas
- Andaimes comentados: retornos das demais colunas; paginacao ativa por padrao (`regrasGeracao.paginacao`)

### cadastro
- switch para `cadastrar`, `alterar`, `consultar`
- `<select>` para cada FK populado via INT
- `<input>` para `varchar`, `numeric`, datas com mascaras corretas (`infraMascaraTexto`, `infraMascaraDinheiro`, `infraMascaraNumero`, `infraMascaraData`, `infraMascaraDataHora`)
- Validacao JS (`validarCadastro()`) para todos os campos obrigatorios
- Redirect assinado apos persistencia com ancora

---

## Fontes de verdade e artefatos

### Contrato de entrada
- `references/dominio-md-abc.md`: dominio padrao de referencia (5 entidades)
- `examples/README.md`: esquema completo do contrato e guia para desenvolvedores que desejam fornecer JSON pronto
- `examples/contrato-entidade-minimo.json`: exemplo minimo de entidade standalone sem FK
- `examples/contrato-entidade-com-fk.json`: exemplo de entidade simples com FK e `sin_ativo`
- `examples/contrato-relacao-nn.json`: exemplo de relacao N:N com PK composta

### Referencias de qualidade (guardrails da IA)
- `references/gabarito-trf4.md`: dois contratos padrao de referencia estrutural e a tabela de desvios conscientes
- `references/gabarito-trf4/`: arquivos completos do gabarito TRF4 (DTO, BD, RN, INT, lista e cadastro das 5 entidades de `md_abc`)
- `.agents/references/padrao-modelagem-dados.md`: regras de nomenclatura fisica, tipos, chaves e sequencias (fonte primaria; cobre integralmente o cap. 5 do manual)
- `.agents/references/padrao-codificacao-php.md`: convencoes de codificacao
- `.agents/references/padrao-auditoria-sip-sei.md`: recursos SIP, permissao e auditoria por metodo
- `references/mapeamento-tipos-e-widgets.md`: tipos de banco x prefixos x widgets x validacao

### Runtime
- `generate_from_contrato.py`: motor de geracao (nesta pasta)
- `templates/lista.php.tpl`: template da lista de entidade simples
- `test_generate_from_contrato.py`: testes do motor

### Complementar
- `sei-gerador-scripts-release`: criacao/atualizacao do script SEI
- `sip-gerador-scripts-release`: criacao/atualizacao do script SIP
- `sei-menu-pagina`: item de menu SIP para a lista
- `.agents/references/padrao-scripts-release.md`: padroes de codigo concretos: DDL multi-SGBD, sequences, FKs, indices, boilerplate SIP
- `.agents/references/mapa-modulos-scripts.md`: manifesto modulo para scripts (consultar antes de qualquer trabalho)

---

## Limitacoes conhecidas (v1)

| Limitacao | Impacto |
|-----------|---------|
| `sta_` rejeitado | Entidades com status multi-valor precisam de widget de opcoes escrito a mao |
| Todos `varchar` como `<input>` | Sem suporte a `textarea` no v1 |
| Dependentes so por contrato | O gerador nao descobre as tabelas filhas; sem `regrasGeracao.dependentes` a exclusao nao checa vinculos |
| Helper INT de N:N | Esqueleto: valor da primeira PK, descricao pelo campo de exibicao da primeira FK |
| `ws/`, `css/`, `imagens/`, `js/` fora do escopo | Gerador produz apenas `dto/`, `bd/`, `rn/`, `int/` e paginas raiz |

---

## Testes

```bash
cd .agents/skills/sei-gerador-crud && python3 -m unittest test_generate_from_contrato
```

A suite gera as 3 entidades do dominio de referencia (standalone com `sin_ativo`, 1:N com dinheiro, N:N), uma entidade de sonda (`dth_`, `numeric` sem `din_`, inteiro e FK opcionais, duas FKs para a mesma tabela), uma entidade com escopo por unidade, coluna unica, dependentes e paginacao desligada, textos com apostrofo, e os 3 exemplos de `examples/`, e para cada saida exige `php -l` verde, Latin-1 sem BOM, sem `U+FFFD`, sem `array(`, sem `$_GET`/`$_POST`, e veredito diferente de BLOCK nos auditores de `sei-verificacao-rn`, `sei-verificacao-pagina` (`--pagina nova`) e `sei-verificacao-banco-dados`. Cobre ainda a profundidade do `require_once`, as mensagens de validacao do contrato, JSON invalido e no-overwrite. Um teste carrega DTO e BD gerados com o `InfraDTO` e o `InfraBD` reais do repositorio, com um driver falso que captura o SQL em vez de executar, e confere joins de FK, LEFT JOIN da FK opcional com alias, PK composta da N:N, sequence nativa, exclusao logica e conversao de dinheiro, decimal e data e hora na gravacao. O arquivo e independente de proposito: nao importa helper de outra skill; os auditores sao a unica dependencia externa.

## Gerador oficial do InfraPHP

Vale quando o desenvolvedor optar pelo gerador oficial do framework em vez desta skill.

As operacoes basicas podem ser geradas pelo gerador de codigo disponivel no endereco do InfraPHP. O fluxo tem quatro passos:

1. Processar os comandos SQL de criacao da tabela, preenchendo os campos **Usuario** e **Modulo Principal**. Na mesma tela, na secao `Permissoes na RN`, informar se o codigo gerado deve prever auditoria das permissoes por Regras de Auditoria do SIP. Este repositorio exige auditoria em metodo de escrita, entao marcar a opcao.
2. Clicar no botao de acao **Cadastrar Campos** da tabela escolhida para a geracao do codigo.
3. Configurar os campos: informar o **campo principal**, os **rotulos** de cada campo e as **teclas de atalho**.
4. Baixar o codigo pelos botoes de acao **Gerar BD**, **Gerar DTO**, **Gerar RN**, **Gerar INT** e os demais correspondentes as camadas.

**Dialeto SQL.** O gerador aceita apenas alguns dialetos. SQL escrito em dialeto nao suportado falha sem mensagem util.

**Padrao de modelagem.** Seguir o padrao de modelagem de dados, principalmente os prefixos de campo, e o que faz o gerador inferir tipo e widget corretamente. Ver `.agents/references/padrao-modelagem-dados.md`.

**Campo principal.** Configurar o campo principal da tabela antes de gerar. Com ele definido, o campo e retornado automaticamente na tela de lista junto com o ID, e e gerado um metodo de montagem de combo na classe INT buscando por esse campo.

**Saida do gerador oficial.** A partir da versao 1.44 ele emite `bloquearConectado` e `array()`, deixa `montarSelect???????` para o desenvolvedor resolver e nao gera `configurarFK`; ajustar esses pontos para o padrao do projeto antes de integrar (ver `references/gabarito-trf4.md`, "Desvios conscientes").
