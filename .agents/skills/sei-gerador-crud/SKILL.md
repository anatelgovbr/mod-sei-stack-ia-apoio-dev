---
name: sei-gerador-crud
description: Gera 6 arquivos CRUD InfraPHP a partir de JSON padrao, usando os templates do gerador como fonte operacional e o gabarito TRF4 apenas como referencia estrutural, com guardrails obrigatorios de seguranca e release do projeto. Quando escolhida pelo desenvolvedor, esta skill tambem contempla a fase de release do modulo (scripts SEI/SIP e sincronizacao de versao) quando aplicavel.
---

# Gerador CRUD InfraPHP

## Proposito

Gera 6 arquivos CRUD InfraPHP (DTO, BD, RN, INT, lista, cadastro) com fidelidade ao padrao TRF4 e guardrails SEI.
Quando o modulo-alvo estiver mapeado e a entidade for nova, a fase de release (scripts SEI/SIP + sincronizacao de versao) faz parte da entrega.
JSON de contrato: artefato interno — construir internamente, resumir ao usuario, aguardar confirmacao antes de salvar ou usar. Se o usuario fornecer JSON proprio, validar antes de usar.
Nao gerar comentario de cabecalho institucional nos arquivos.

Fonte operacional do CRUD gerado:
- `generate_from_contrato.py`
- `templates/*.tpl`

Fonte de referencia estrutural:
- `references/gabarito-trf4.md`

Regra: o gabarito TRF4 serve para comparacao estrutural e validacao de padrao. Nao usar o gabarito como template literal, nem copiar nomes, textos, identificadores ou detalhes de dominio do exemplo.


## Preflight obrigatorio

Ler as referencias principais antes de definir nomes fisicos ou release:
- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_3_consideracoes_previas.md`
- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_4_infraphp.md`
- `references/gabarito-trf4.md`
- `.agents/references/padrao-modelagem-dados.md`

## Guard de assets existentes

Antes de criar ou sugerir arquivos CSS/JS para o modulo-alvo, verificar:

- Se `modulos/<nome>/css/` ja contiver arquivos: **nao criar novos arquivos CSS**. Orientar edicao dos existentes.
- Se `modulos/<nome>/js/` ja contiver arquivos: **nao criar novos arquivos JS**. Orientar edicao dos existentes.
- A mesma regra vale para arquivos PHP de asset na raiz do modulo (`*_css.php`, `*_js.php`): se existirem, editar, nao criar.

## Textos exibidos ao usuario

- Textos padrao universais do CRUD devem sair acentuados pelo gerador: `Ações`, `Operação realizada com sucesso.`, `Ação ... não reconhecida.`, `inválido`, `desativação`, `reativação` e `exclusão`.
- Textos de dominio (singular, plural, rotulos, titulos, captions, `title`, `alt`): nao inferir — devem vir no contrato. Se ausentes ou sem acento, alertar o desenvolvedor antes de entregar.

---

## Tres caminhos de execucao

Identificar o caminho pelo contexto. Ordem de deteccao: C > A > B.

### Caminho A — Documentacao disponivel

Use quando existir qualquer artefato pre-escrito sobre a entidade (spec, plano, data-model, task ou descricao estruturada).

1. Ler o artefato disponivel e extrair: nome da tabela, colunas, relacoes FK, campo principal, labels de UI.
2. Validar os nomes fisicos antes de propor o contrato:
   - PK gerada por sequence nativa: `id_<nome_tabela_completo>`
   - FK: repetir exatamente o nome da PK da tabela de origem
   - N:N: preferir `md_<sigla>_rel_<entidade_a>_<entidade_b>`
3. Se houver lacunas pontuais (ex: tamanho de coluna, artigo), perguntar apenas o que falta, em rodadas de no maximo 3 perguntas por vez, repetindo quantas rodadas forem necessarias ate nao restar nenhuma duvida obrigatoria.
4. Construir o JSON internamente (nao mostrar ao usuario a menos que ele peca).
5. Apresentar um resumo curto do contrato e aguardar confirmacao explicita do desenvolvedor.
6. Salvar o contrato em arquivo (localizacao a criterio da ferramenta) para executar o gerador.
7. Executar o gerador (ver secao "Execucao").
8. Apos `php -l` verde, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

### Caminho B — Descricao em linguagem natural

Use quando nao houver artefato pre-escrito sobre a entidade e o usuario descrever a entidade livremente.

Perguntar somente o necessario, na ordem da tabela, parando ao ter o suficiente:

| # | O que perguntar | Quando pular |
|---|----------------|-------------|
| 1 | Nome da tabela fisica (`md_<inst>_<entidade>` ou `md_<inst>_rel_<a>_<b>` para N:N) e modulo-alvo | Se ja informado |
| 2 | Colunas: nome, tipo, tamanho (para varchar), obrigatorio | Se descricao ja cobre |
| 3 | Existe FK para outra tabela? Qual e o campo de exibicao no pai? | Se nao ha relacao |
| 4 | A entidade tem exclusao logica (`sin_ativo`)? | Se ja confirmado |
| 5 | Qual coluna identifica o registro na listagem? (campoPrincipal) | Se ja confirmado |
| 6 | Ja existem scripts de instalacao do modulo? Informar nome ou caminho | Se o modulo for novo ou scripts forem detectados automaticamente |

O contrato JSON gerado internamente DEVE incluir a chave `regrasGeracao` com `campoSinAtivo` preenchido com o nome da coluna (`"sin_ativo"`) quando houver exclusao logica, ou com `null`/ausente quando nao houver. O gerador nao deriva esse valor automaticamente — a ausencia da chave causa erro.

Apos coletar o suficiente:
- Construir o JSON internamente.
- Apresentar um **resumo de 3 linhas** (tabela, campos, flags ativas) e perguntar se pode prosseguir — nao mostrar o JSON completo a menos que o usuario peca.
- Salvar o contrato em arquivo para executar o gerador.
- Executar o gerador (ver secao "Execucao").
- Apos `php -l` verde, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

### Caminho C — JSON pronto

Use quando o usuario fornecer um arquivo JSON, caminho ou bloco JSON compativel.

1. Se o desenvolvedor pedir um modelo, apontar para `examples/README.md` e para os contratos em `examples/`.
2. Validar o JSON (ver secao "Validacoes obrigatorias").
3. Executar o gerador diretamente.
4. Apos `php -l` verde, executar obrigatoriamente a Fase de Release (ver secao "Fase de Release").

---

## Execucao

Apos ter o JSON salvo em arquivo:

```bash
python3 .agents/skills/sei-gerador-crud/generate_from_contrato.py \
  <caminho/contrato.json> <diretorio_saida>
```

Diretorio de saida: o modulo-alvo em `fontes/sei/src/main/php/sei/web/modulos/<instituicao>/<modulo>/`.

**Estrutura final do modulo**:

- O motor atual grava os 6 arquivos no diretorio informado.
- Quando o destino for o modulo real, mover imediatamente as classes para as camadas corretas antes de validar:
  - `*DTO.php` -> `dto/`
  - `*BD.php` -> `bd/`
  - `*RN.php` -> `rn/`
  - `*INT.php` -> `int/`
- As paginas `*_lista.php` e `*_cadastro.php` permanecem na raiz do modulo.
- So considerar a geracao concluida quando o resultado final respeitar a estrutura do manual (`dto/`, `rn/`, `bd/`, `int/`, paginas na raiz).
- Use `tmp/<tabela>/` apenas quando o desenvolvedor pedir explicitamente para testar antes de integrar.

Apos reorganizar os arquivos para a estrutura final, rodar obrigatoriamente:

```bash
for f in <diretorio_saida>/*.php <diretorio_saida>/dto/*.php <diretorio_saida>/bd/*.php <diretorio_saida>/rn/*.php <diretorio_saida>/int/*.php; do php -l "$f"; done
```

Reportar:
- 6 arquivos gerados com seus caminhos.
- Resultado do `php -l` (OK ou ERRO com mensagem).
- Flags aplicadas: `temSinAtivo`, `temFk`, numero de FKs.
- Limitacoes observadas para esta entidade especifica.

### Gates pos-geracao do motor

Depois de gerar os arquivos, conferir antes de entregar:

- paginas usam `$strAcao = PaginaSEI::GET('acao')`, `validarPermissao($strAcao)` e `switch ($strAcao)`; nao aceitar `$_GET['acao']`.
- formularios e JavaScript usam `$strAcao` em vez de reler `PaginaSEI::GET('acao')`.
- saida dinamica usa `PaginaSEI::tratarHTML(...)`, inclusive mensagens com dados do usuario, celulas de tabela e campos hidden.
- listas N:N validam o identificador composto antes de `set*`: `count(...)==2` e `ctype_digit(...)`.
- listas N:N retornam e exibem os campos relacionados, com `</tbody>` fora do loop.
- helpers INT de entidades com `sin_ativo` filtram ativos por padrao e incluem o item selecionado mesmo inativo.
- validadores RN de `numeric` aceitam virgula decimal, normalizam para ponto, rejeitam negativos e setam `null` quando opcional vazio.
- reativacao logica consulta o registro completo com exclusao logica desabilitada e reexecuta validadores basicos antes de reativar.

Se qualquer item falhar, corrigir o gerador ou o template antes de ajustar manualmente o CRUD gerado.

---

## Fase de Release

Executar esta fase apos `php -l` verde em todos os arquivos gerados.

### Verificacao obrigatoria no mapa

Consultar `.agents/references/mapa-modulos-scripts.md` para o modulo-alvo:

- **Modulo esta no mapa**: atualizacao dos scripts obrigatoria como parte desta skill. Nao perguntar se o desenvolvedor quer incluir release no escopo; informar que faz parte da entrega e perguntar apenas a versao-alvo quando nao estiver definida no contexto.
- **Modulo nao esta no mapa**: verificar fisicamente em `sei/scripts/` e `sip/scripts/` (nomes podem divergir do padrao convencional). Se encontrado, tratar como mapeado. Se confirmada ausencia: oferecer criacao via `sei-gerador-scripts-release` e `sip-gerador-scripts-release`, conforme escopo.

### Quando os scripts existem — atualizacao incremental (obrigatoria)

Consultar `.agents/references/padrao-scripts-release.md` para padroes de codigo concretos (DDL multi-SGBD, sequences, FKs, boilerplate SIP).

Propor a proxima versao (bump de **minor** por padrao para nova entidade) e aguardar confirmacao do desenvolvedor antes de alterar qualquer arquivo.

Apos confirmacao, gerar e inserir nos scripts existentes:

1. `case '<versaoAtual>': $this->instalarv<XYZ>();` no switch de ambos os scripts (sem `break` — fallthrough intencional; `break` migra para o novo ultimo case)
2. Metodo `instalarv<XYZ>()` no SEI com DDL multi-SGBD: tabela, sequence, FKs e chamada a `atualizarNumeroVersao()`
3. Metodo `instalarv<XYZ>()` no SIP com `adicionarRecursoPerfil()` por acao e chamada a `atualizarNumeroVersao()`
4. Sincronizar `getVersao()` na classe `*Integracao.php` do modulo com a mesma versao aplicada nos scripts
5. Se o modulo ja possuir regra de auditoria no SIP, anexar os novos recursos a ela e replicar a regra ao final da atualizacao

Atualizar em ambos os scripts:
- `$versaoAtualDesteModulo = '<novaVersao>'`
- `$historicoVersoes`: adicionar `'<novaVersao>'` ao final do array

**Recursos SIP a registrar por entidade:**

| Condicao             | Recursos                                                                                   |
|----------------------|-------------------------------------------------------------------------------------------|
| Sempre               | `_cadastrar`, `_alterar`, `_consultar`, `_listar`, `_excluir`, `_selecionar`              |
| `temSinAtivo == true`| Adicionar `_desativar`, `_reativar`                                                       |

Perfil `Basico`: nao vincular por padrao. Vincular apenas quando a spec disser explicitamente que a funcionalidade e acessivel a todos os usuarios internos.

Validar apos edicao:

```bash
php -l fontes/sei/src/main/php/sei/scripts/<script_sei>.php
php -l fontes/sei/src/main/php/sip/scripts/<script_sip>.php
```

### Quando os scripts nao existem — delegar

Scripts novos completos estao fora do escopo desta skill. Orientar o desenvolvedor a usar `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` fornecendo:
- O contrato JSON da entidade como insumo para modelagem inicial
- Nome do modulo, instituicao e versao inicial desejada (`1.0.0` por padrao)

---

## Validacoes obrigatorias antes de gerar

1. JSON sintaticamente valido.
2. CRUD simples: exatamente uma coluna com `chavePrimaria: true`; N:N: exatamente duas.
3. `entidade.campoPrincipal` referencia uma coluna existente em `colunas`.
4. Nomes fisicos: lowercase + digits + underscore, max 26 chars.
   - PK gerada por sequence nativa deve seguir `id_<nome_tabela_completo>`.
   - FK deve repetir o nome da PK de origem.
5. Tabela e todas as colunas possuem `comentario` negocial preenchido.
6. Tipos no subconjunto suportado: `int`, `integer`, `varchar`, `datetime`, `date`, `timestamp`, `char`, `numeric`. Preferir `date` (coluna `dta_*`) e `timestamp` (coluna `dth_*`) sobre `datetime` (proprietário MySQL).
7. Nenhum dos 6 arquivos-alvo ja existe no diretorio de saida (no-overwrite).
8. Se houver FK em `relacionamentos`, a coluna declarada existe em `colunas`.

---

## Regras de derivacao

### Nomes de classe e arquivo

| Entrada | Regra | Exemplo |
|---------|-------|---------|
| `entidade.tabela` | PascalCase | `md_abc_projeto` → `MdAbcProjeto` |
| classeBase + camada | — | `MdAbcProjetoDTO.php`, `MdAbcProjetoBD.php` |
| `{tabela}_lista.php` | — | `md_abc_projeto_lista.php` |
| `{tabela}_cadastro.php` | — | `md_abc_projeto_cadastro.php` |

### Prefixos de atributo DTO

| Tipo de banco | Prefixo | Exemplo coluna | Atributo DTO |
|--------------|---------|----------------|-------------|
| `int`, `integer` | `Num` | `id_md_abc_projeto` | `NumIdMdAbcProjeto` |
| `varchar` | `Str` | `identificacao` | `StrIdentificacao` |
| `date` / `datetime` + coluna `dta_*` | `Dta` | `dta_cadastramento` | `DtaCadastramento` |
| `timestamp` / `datetime` + coluna `dth_*` | `Dth` | `dth_entrega` | `DthEntrega` |
| `char(1)` | `Str` | `sin_ativo` | `StrSinAtivo` |
| `numeric` | `Din` | `din_custo` | `DinCusto` |

Normalizacao: prefixos semanticos (`num_`, `str_`, `din_`, `dta_`, `dth_`) sao removidos antes do PascalCase para evitar duplicacao (ex: `dta_` nao vira `DtaDta`; `dth_` nao vira `DthDth`).
O discriminador `Dta` vs `Dth` e determinado pelo nome da coluna: prefixo `dth_` → `Dth`; qualquer outro tipo de data → `Dta`.

### Elementos HTML

| Tipo | Prefixo HTML | Exemplo |
|------|-------------|---------|
| `varchar`, `datetime`, `date`, `timestamp`, `numeric`, `char` | `txt` | `txtIdentificacao` |
| FK | `sel` | `selMdAbcProjeto` |
| campo oculto | `hdn` | `hdnIdMdAbcProjeto` |
| imagem calendario | `imgCal` | `imgCalCadastramento` |

### Acoes

Padrao: `{tabela}_{operacao}` — ex: `md_abc_projeto_cadastrar`, `md_abc_projeto_alterar`.

---

## Regras condicionais obrigatorias

### Quando existe `sin_ativo`

- DTO: `configurarExclusaoLogica('SinAtivo', 'N')`.
- RN: `desativarControlado()`, `reativarControlado()`, `bloquearConectado()` **ativos**.
- INT: `adicionarCriterio(...)` para incluir item selecionado mesmo inativo.
- lista: cases e botoes de desativar/reativar **ativos**.

### Quando NAO existe `sin_ativo`

- Os blocos acima sao gerados como comentarios `/* ... */` — **nunca omitidos**.
- Referencia padrao: `md_abc_aquisicao`.

### Quando existe FK (uma ou mais)

- DTO: `adicionarAtributoTabelaRelacionada(...)` e `configurarFK(...)` para cada FK.
- FK obrigatoria: `InfraDTO::$TIPO_FK_OBRIGATORIA`; FK opcional: `InfraDTO::$TIPO_FK_OPCIONAL`.
- Filtro de FK: preferir `InfraDTO::$FILTRO_FK_ON`; usar `InfraDTO::$FILTRO_FK_WHERE` apenas quando necessario.
- INT: `montarSelect{CampoPrincipalPai}(..., $fkVar='')` com parametro por FK.
- cadastro: `<select>` populado via classe INT, `salvarCamposPost` com todos os selects.
- lista: filtro persistido com dropdown por FK.

### Quando ha PK composta (entidade N:N)

Detectado automaticamente quando existem 2 colunas com `chavePrimaria: true`. O contrato **deve** incluir `relacionamentosNn` (array de 2 entradas):

```json
"relacionamentosNn": [
  { "tabelaOrigem": "md_ri_filme", "classeInt": "MdRiFilmeINT", "metodoInt": "montarSelectTitulo", "rotulo": "Filme" },
  { "tabelaOrigem": "md_ri_ator",  "classeInt": "MdRiAtorINT",  "metodoInt": "montarSelectNome",   "rotulo": "Ator"  }
]
```

Diferencas em relacao ao CRUD simples:

- DTO: duas `configurarPK(..., $TIPO_PK_INFORMADO)` em vez de uma sequencial; sem `configurarExclusaoLogica`.
- RN: desativar/reativar/bloquear sempre comentados (`/* ... */`).
- INT: metodo recebe os dois atributos PK como filtros opcionais.
- lista: IDs compostos com `explode('-', $strId)`; o gerador usa índices `[0]` e `[1]` com validação `count(...)==2` e `ctype_digit(...)`; o gabarito TRF4 v1.46.4 usa `[1]` e `[2]` — divergência conhecida, padrão do gerador adotado por ser logicamente consistente com o ID armazenado como `pk1-pk2`.
- lista: retornar e exibir os campos relacionados declarados em `relacionamentos`, escapando com `PaginaSEI::tratarHTML(...)`.
- cadastro: dois `<select>` FK com `hdnPk1`/`hdnPk2` ocultos; sem campo sequencial.
- `regrasGeracao.campoSinAtivo` deve ser `null` (sin_ativo nao faz sentido em N:N).

---

## Guardrails SEI obrigatorios (todo arquivo de pagina)

- usar caminho relativo coerente com a camada final do modulo:
  - classes em `dto/`, `bd/`, `rn/`, `int/`: `require_once dirname(__FILE__) . '/../../../SEI.php';`
  - paginas na raiz do modulo: `require_once dirname(__FILE__) . '/../../SEI.php';`
- entrar por `controlador.php?acao=...` e tratar `acao` como parametro obrigatorio
- `session_start();`
- `SessaoSEI::getInstance()->validarLink();` — primeira validacao do bloco `try`
- `$strAcao = PaginaSEI::GET('acao');` seguido de `SessaoSEI::getInstance()->validarPermissao($strAcao);`
- `SessaoSEI::getInstance()->assinarLink(...)` em todos os links/redirects
- `PaginaSEI::tratarHTML(...)` em toda saida HTML
- RN: `SessaoSEI::getInstance()->validarAuditarPermissao(...)` em cada metodo
- Escrita: `*Controlado`; Leitura: `*Conectado`
- toda comunicacao entre camadas deve trafegar via DTO
- uma RN nao pode chamar a BD de outra classe
- nao deve haver comunicacao direta entre BDs
- uma BD nao pode persistir ou atualizar mais de uma tabela
- e-mail, integracao externa, indexacao e processamento demorado devem ficar fora da transacao principal

---

## Checklist por camada

### DTO
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
- Docblock com `@method` para todos os metodos publicos
- Validadores privados por campo (`validarStr*`, `validarNum*`, `validarDta*`)
- `cadastrarControlado`, `alterarControlado` (com guards `isSet*()`), `excluirControlado`
- `consultarConectado`, `listarConectado`, `contarConectado`
- Blocos de desativar/reativar/bloquear ativos ou comentados conforme `sin_ativo`

### INT
- `extends InfraINT`
- Helper `montarSelect{CampoPrincipal}(...)` com ordenacao ascendente
- Parametro FK por relacionamento quando aplicavel
- Bloco `adicionarCriterio(sin_ativo OR pk)` apenas quando houver `sin_ativo`

### lista
- switch/case por acao
- Filtro persistido em sessao para cada FK
- Tabela com acoes assinadas (consultar, alterar, desativar/reativar, excluir)
- JS de confirmacao para acoes destrutivas

### cadastro
- switch para `cadastrar`, `alterar`, `consultar`
- `<select>` para cada FK populado via INT
- `<input>` para `varchar`, `numeric`, `datetime` com mascaras corretas
- Validacao JS (`validarCadastro()`) para todos os campos obrigatorios
- Redirect assinado apos persistencia com ancora

---

## Fontes de verdade e artefatos

### Contrato de entrada
- `references/dominio-md-abc.md` — dominio padrao de referencia (5 entidades)
- `examples/README.md` — guia rapido para desenvolvedores que desejam fornecer JSON pronto
- `examples/contrato-entidade-minimo.json` — exemplo minimo de entidade standalone sem FK
- `examples/contrato-entidade-com-fk.json` — exemplo de entidade simples com FK e `sin_ativo`
- `examples/contrato-relacao-nn.json` — exemplo de relacao N:N com PK composta

### Referencias de qualidade (guardrails da IA)
- `references/gabarito-trf4.md` — dois contratos padrao de referencia estrutural
- `references/padroes-sei.md` — guardrails SEI obrigatorios
- `.agents/references/padrao-modelagem-dados.md` — regras de nomenclatura fisica, tipos, chaves e sequencias (fonte primaria; manual 5 abaixo e a origem)
- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_3_consideracoes_previas.md` — recursos SIP, permissao e auditoria
- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_4_infraphp.md` — estrutura de paginas e camadas
- `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_5_padrao_modelagem_de_dados.md` — naming fisico padrao (consultar para duvidas nao cobertas pela reference acima)
- `.agents/references/padrao-codificacao-php.md` — convencoes de codificacao
- `references/mapeamento-tipos-e-widgets.md` — tipos de banco x widgets HTML

### Runtime
- `generate_from_contrato.py` — motor de geracao (nesta pasta)
- `templates/lista.php.tpl` — template ativo para lista

### Complementar
- `sei-gerador-scripts-release` — criacao/atualizacao do script SEI
- `sip-gerador-scripts-release` — criacao/atualizacao do script SIP
- `.agents/references/padrao-scripts-release.md` — padroes de codigo concretos: DDL multi-SGBD, sequences, FKs, boilerplate SIP
- `.agents/references/mapa-modulos-scripts.md` — manifesto modulo→scripts (consultar antes de qualquer trabalho)

---

## Limitacoes conhecidas (v1)

| Limitacao | Impacto |
|-----------|---------|
| `sta_` nao suportado | Entidades com status multi-valor sao rejeitadas |
| Todos `varchar` como `<input>` | Sem suporte a `textarea` no v1 |
| `ws/`, `css/`, `imagens/`, `js/` fora do escopo | Gerador produz apenas `dto/`, `bd/`, `rn/`, `int/` e paginas raiz |

---
