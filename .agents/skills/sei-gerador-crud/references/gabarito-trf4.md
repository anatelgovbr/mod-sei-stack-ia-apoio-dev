# Referencia: Gabarito TRF4

## Objetivo

Esta referencia resume os casos padrao usados para validar o gerador: uma
entidade standalone com exclusao logica ativa, uma entidade com FK sem
`sin_ativo` e o padrao de nomenclatura/modelagem observado no manual.

Este arquivo e apenas referencia estrutural. A geracao padrao do CRUD vem de
`generate_from_contrato.py`; o unico template lido pelo motor e
`templates/lista.php.tpl`, usado na lista de entidade simples. Nao tratar este
gabarito como template literal de saida.

## Arquivos do gabarito

Os arquivos completos ficam em `references/gabarito-trf4/`. Sao a saida do
Gerador de Codigo oficial do TRF4, versao 1.46.4, para o dominio `md_abc`
descrito em `references/dominio-md-abc.md` (5 entidades: `md_abc_projeto`,
`md_abc_aquisicao`, `md_abc_contrato`, `md_abc_responsavel` e
`md_abc_rel_contrato_proj`), com estes ajustes sobre a saida bruta:
- sistema `abc` trocado por `SEI` (`BancoSEI`, `SessaoSEI`, `PaginaSEI`, `SEI.php`)
- chamadas `montarSelect???????`, que o gerador oficial deixa para o desenvolvedor,
  resolvidas para `montarSelectIdentificacao` e `montarSelectDescricao`
- sufixo de genero das mensagens de validacao corrigido (`informado`, `informada`)
- tabela N:N renomeada de `md_abc_rel_contrato_projeto` (27 caracteres) para
  `md_abc_rel_contrato_proj`, dentro do limite de 26 do padrao de modelagem
- cabecalho institucional mantido, sem a linha `criado por`

Estrutura da pasta:
- `dto/`, `bd/`, `rn/`, `int/`: uma classe por entidade
- raiz: `md_abc_<entidade>_lista.php` e `md_abc_<entidade>_cadastro.php`

Uso:
- comparar a estrutura do CRUD gerado com o arquivo equivalente da mesma
  entidade (metodos, recursos de permissao, blocos comentados, helpers INT,
  cases da lista e campos do cadastro)
- os arquivos sao PHP em Latin-1 na worktree; buscar sempre com `grep -a`
- os 30 arquivos abrem com `<?php` e passam em `php -l`; o `require_once` de
  um nivel (`/../SEI.php`) e artefato do gerador oficial, nao serve de modelo

## Desvios conscientes do gabarito

O projeto prevalece sobre o gabarito. A saida do gerador difere do gabarito nos
pontos abaixo, cada um com a regra que o justifica.

| Ponto | Gabarito TRF4 1.46.4 | Saida da skill | Regra |
|---|---|---|---|
| Chave primaria | `TIPO_PK_SEQUENCIAL` | `TIPO_PK_NATIVA` com `seq_<tabela>` | `padrao-modelagem-dados.md`, secao de chaves; manual cap. 4 |
| Chave estrangeira no DTO | sem `configurarFK` | `configurarFK` por FK, com `TIPO_FK_OPCIONAL` e `FILTRO_FK_WHERE` conforme o contrato | manual cap. 4; `padrao-modelagem-dados.md` |
| Duas FKs para a mesma tabela | nao coberto | alias SQL na segunda (`unidade u2`, `u2.sigla`), atributo relacionado com o sufixo da coluna (`SiglaUnidadeDestino`) | idioma do core (`ColegiadoDTO.php`) |
| Sintaxe de array | `array()` | `[]` | `AGENTS.md`, "PHP moderno"; `padrao-codificacao-php.md` |
| Caminho do `require_once` | `dirname(__FILE__)` com um nivel | `__DIR__` com profundidade derivada do diretorio de saida | modulos reais em `modulos/<inst>/<modulo>/` |
| Recurso de `consultar` e `bloquear` | `_consultar` | `_consultar` (igual) | `AGENTS.md`, leitura em RN |
| Sufixo de `bloquear` | `bloquearConectado` (Gerador TRF4 a partir de 1.44) | `bloquearControlado` | manual cap. 4, "Bloquear (Controlado)": o lock so vale dentro da transacao |
| Docblock do DTO | sem | `@table` e `@column` com os comentarios do contrato | `sei-verificacao-banco-dados`, regra DB12 |
| Acao da pagina | `PaginaSEI::GET('acao')` repetido | `$strAcao` reutilizado em links, formulario e JavaScript | `sei-verificacao-pagina` |
| Presenca de POST e GET | `isset($_POST['sbm...'])`, `isset($_GET['id_...'])` | `PaginaSEI::POST('sbm...') !== null`, `PaginaSEI::GET('id_...') !== null` | `AGENTS.md`, entrada HTTP; gate P006 |
| Identificadores de GET, POST e selecao | sem normalizacao | `ctype_digit` mais `(int)` | `AGENTS.md`, entrada HTTP |
| Mensagem de sucesso | texto cru em `adicionarMensagem` | texto cru (igual); `InfraPagina::montarMensagens` ja escapa | evita escape duplo |
| Fluxo de `sin_ativo` na lista | tela propria de reativacao (`acao=_reativar` lista inativos com `acao_confirmada`) | lista unica com inativos em `trVermelha`, icone e botao de reativar na propria lista, sem `acao_confirmada` | modelo de `trf4/julgamento/motivo_ausencia_lista.php` |
| Classe da linha inativa | `infraTrVermelha` | `trVermelha` | idioma do core do SEI |
| Blocos de `sin_ativo` sem exclusao logica | comentados | comentados, com o mesmo conteudo do modo ativo | igual ao gabarito |
| Validador monetario | so obrigatoriedade | `InfraUtil::validarDin` sem alterar o valor | idioma do core (`DocumentoRN`); `prepararDin` converte na gravacao |
| Validador de data e hora | `validarData` | `validarDataHora` para `dth_` | idioma dos modulos (`ColegiadoVersaoRN`) |
| Inteiro e FK opcionais | sempre obrigatorios | vazio vira `null` quando `obrigatorio: false` | coerencia entre DTO, RN e formulario |
| Largura dos campos | 25% | por tipo e tamanho | `mapeamento-tipos-e-widgets.md` |
| Helper INT com `sin_ativo` | sem ramo `else` | sem ramo `else` (igual) | `configurarExclusaoLogica` ja filtra ativos |
| Andaimes comentados | colunas nao principais, paginacao, `@var` | colunas nao principais e `@var` mantidos; paginacao ativa por padrao (`regrasGeracao.paginacao`) | 70 das 113 listas reais paginam |
| Escopo por unidade, unicidade e dependentes | ausentes | opcionais por contrato (`escopoUnidade`, `unico`, `dependentes`) | idioma de `trf4/julgamento` (`destaque_cadastro.php`, `MotivoAusenciaRN.php`) |
| Lista N:N | sem colunas de dados | colunas relacionadas com `getThOrdenacao` | usabilidade; o gabarito nao mostra dado algum |
| Indices do ID composto na lista N:N | `[1]` e `[2]` | `[0]` e `[1]` com `count(...)==2` e `ctype_digit` | consistente com o ID gravado como `pk1-pk2` |

## Contrato 1: `md_abc_projeto`

- tabela: `md_abc_projeto`
- arquivos gerados:
  - `MdAbcProjetoDTO.php`
  - `MdAbcProjetoBD.php`
  - `MdAbcProjetoRN.php`
  - `MdAbcProjetoINT.php`
  - `md_abc_projeto_lista.php`
  - `md_abc_projeto_cadastro.php`
- colunas reais do gabarito:
  - `id_md_abc_projeto` (`int`, PK)
  - `identificacao` (`varchar`)
  - `descricao` (`varchar`)
  - `dta_cadastramento` (`date`)
  - `sin_ativo` (`char(1)`)
- caracteristicas obrigatorias:
  - exclusao logica ativa
  - helper INT `montarSelectIdentificacao(...)`
  - lista com botoes/cases de desativar e reativar
  - cadastro com `txtIdentificacao`, `txtDescricao`, `txtCadastramento`

## Contrato 2: `md_abc_aquisicao`

- tabela: `md_abc_aquisicao`
- arquivos gerados:
  - `MdAbcAquisicaoDTO.php`
  - `MdAbcAquisicaoBD.php`
  - `MdAbcAquisicaoRN.php`
  - `MdAbcAquisicaoINT.php`
  - `md_abc_aquisicao_lista.php`
  - `md_abc_aquisicao_cadastro.php`
- colunas reais do gabarito:
  - `id_md_abc_aquisicao` (`int`, PK)
  - `id_md_abc_projeto` (`int`, FK)
  - `descricao` (`varchar`)
  - `din_custo` (`numeric`)
- caracteristicas obrigatorias:
  - sem `sin_ativo`
  - blocos de desativar/reativar/bloquear comentados
  - DTO com `adicionarAtributoTabelaRelacionada(...)`
  - cadastro com `<select>` de projeto
  - lista com filtro persistido `selMdAbcProjeto`
  - helper INT `montarSelectDescricao(..., $numIdMdAbcProjeto='')`

## Convencoes observadas

- nao sintetizar comentario de cabecalho institucional apenas para "parecer oficial"
- quando o arquivo de referencia tiver bloco de identificacao, tratar isso como detalhe historico do artefato, nao como requisito estrutural do gerador
- nomes fisicos de PK/FK seguem o nome completo da tabela de origem
  (ex.: `id_md_abc_contrato`, `id_md_abc_projeto`); FK com outro nome e aceita
  quando houver duas FKs para a mesma tabela (papeis distintos)
- relacoes N:N seguem o padrao `md_<sigla>_rel_<a>_<b>` com PK composta pelas FKs
- na estrutura final do modulo, classes ficam em `dto/`, `bd/`, `rn/`, `int/`
- na estrutura final do modulo em `modulos/<inst>/<modulo>/`, classes usam `require_once __DIR__ . '/../../../../SEI.php';` e paginas `require_once __DIR__ . '/../../../SEI.php';` (um nivel a menos em `modulos/<modulo>/`)
- paginas sao procedurais e usam `PaginaSEI::getInstance()` extensivamente
- comparacao com o gabarito e estrutural, nao byte a byte

## Nota importante sobre os contratos

Os nomes de coluna usados para validar o gerador devem seguir o dominio de referencia
em `references/dominio-md-abc.md`. Ele prevalece sobre exemplos resumidos quando
houver divergencia de nomenclatura.
