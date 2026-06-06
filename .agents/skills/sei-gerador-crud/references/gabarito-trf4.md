# Referencia: Gabarito TRF4

## Objetivo

Esta referencia resume os casos padrao usados para validar o gerador: uma
entidade standalone com exclusao logica ativa, uma entidade com FK sem
`sin_ativo` e o padrao de nomenclatura/modelagem observado no manual.

Este arquivo e apenas referencia estrutural. A geracao padrao do CRUD vem de:
- `generate_from_contrato.py`
- `templates/*.tpl`

Nao tratar este gabarito como template literal de saida.

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
  (ex.: `id_md_abc_contrato`, `id_md_abc_projeto`)
- relacoes N:N seguem o padrao `md_<sigla>_rel_<a>_<b>` com PK composta pelas FKs
- na estrutura final do modulo, classes ficam em `dto/`, `bd/`, `rn/`, `int/`
- na estrutura final do modulo, classes usam `require_once dirname(__FILE__) . '/../../../SEI.php';`
- na estrutura final do modulo, paginas usam `require_once dirname(__FILE__) . '/../../SEI.php';`
- paginas sao procedurais e usam `PaginaSEI::getInstance()` extensivamente
- comparacao com o gabarito e estrutural, nao byte a byte

## Nota importante sobre os contratos

Os nomes de coluna usados para validar o gerador devem seguir o dominio de referencia
em `references/dominio-md-abc.md`. Ele prevalece sobre exemplos resumidos quando
houver divergencia de nomenclatura.
