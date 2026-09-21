# Exemplos de contrato JSON

Estes arquivos mostram o formato aceito pelo `generate_from_contrato.py`.

O contrato JSON e um artefato interno da IA. Os exemplos existem apenas para o desenvolvedor montar um JSON compativel e informar o arquivo no prompt quando quiser pular parte da fase de perguntas.

## Como usar

1. Copie um dos exemplos em `examples/`.
2. Ajuste nomes fisicos, comentarios, rotulos, teclas de atalho, artigos e relacionamentos para a entidade real.
3. Informe o caminho do JSON no prompt ou cole o conteudo para a IA validar e usar internamente.
4. Quando houver feature ativa em fluxo Spec Kit, o contrato final fica em `specs/<feature>/crud-contratos/<tabela>.json`; fora do Spec Kit, em `tmp/crud-contratos/<tabela>.json`. Os dois caminhos estao fora do versionamento.

## Arquivos disponiveis

| Arquivo | Use quando | Cobertura |
| ------- | ---------- | --------- |
| `contrato-entidade-minimo.json` | A entidade nao tem FK e nao usa exclusao logica | PK nativa + campos simples |
| `contrato-entidade-com-fk.json` | A entidade depende de outra tabela e usa `sin_ativo` | PK nativa + FK + `relacionamentos` + `ui` |
| `contrato-relacao-nn.json` | A entidade e uma tabela de relacao entre duas tabelas | PK composta + `relacionamentos` + `relacionamentosNn` |

## Esquema do contrato

Chaves obrigatorias em todo contrato:

| Chave | Conteudo |
| ----- | -------- |
| `entidade.tabela` | nome fisico `md_<sigla>_<entidade>`, minusculas, ate 26 caracteres |
| `entidade.singular`, `entidade.plural` | textos exibidos ao usuario, acentuados |
| `entidade.artigo` | `o` ou `a`; define concordancia das mensagens da entidade |
| `entidade.campoPrincipal` | coluna exibida na lista e usada no helper `montarSelect*` do INT; em N:N so passa pela validacao |
| `entidade.comentario` | descricao negocial da tabela; vai para o docblock `@table` do DTO e para a release |
| `colunas[].nome`, `colunas[].tipoBanco`, `colunas[].obrigatorio`, `colunas[].comentario` | tipos aceitos: `int`, `integer`, `varchar` (com `tamanho`), `char` (com `tamanho`), `date` (`dta_*`), `timestamp` (`dth_*`), `datetime`, `numeric` (`din_*` para dinheiro; `precisao` e `escala` opcionais, usados na release) |
| `colunas[].chavePrimaria` | `true` na PK; uma PK `id_<tabela>` no CRUD simples, duas PKs informadas na N:N |
| `regrasGeracao.campoSinAtivo` | `"sin_ativo"` quando a entidade tem exclusao logica (exige a coluna `sin_ativo char(1)`), `null` quando nao tem; obrigatoria no CRUD simples |

Chaves opcionais:

| Chave | Conteudo |
| ----- | -------- |
| `colunas[].chaveEstrangeira` | `true` em coluna FK (documental; o que gera a FK e `relacionamentos`) |
| `relacionamentos[]` | uma entrada por FK: `coluna`, `tabelaReferencia`, `campoExibicao` (coluna do pai mostrada no select e na lista), `tipoFk` (`obrigatoria` ou `opcional`, coerente com `obrigatorio` da coluna), `filtroFk` (`on` ou `where`), `tipoExibicao` (tipo SQL de `campoExibicao` quando nao for texto) |
| `relacionamentosNn[]` | exatamente duas entradas na N:N: `tabelaOrigem`, `classeInt`, `metodoInt`, `rotulo`, `artigo`, `teclaAtalho` |
| `ui.ordemFormulario` | ordem dos campos no cadastro; quando presente, precisa conter toda coluna que nao seja PK nem `sin_ativo` |
| `ui.campos.<coluna>` | `rotulo` (acentuado), `teclaAtalho` (letra do rotulo), `artigo` (`o` ou `a`, concordancia das mensagens da coluna) |
| `regrasGeracao.paginacao` | `true` (padrao) ativa `prepararPaginacao` e `processarPaginacao` na lista; `false` deixa as linhas comentadas |
| `regrasGeracao.escopoUnidade` | nome de coluna `int` obrigatoria que guarda a unidade: preenchida com a unidade atual da sessao, filtra lista e INT, fora do formulario e de `relacionamentos` |
| `regrasGeracao.dependentes[]` | `tabela`, `coluna` (FK na filha), `rotulo` e `artigo` de cada entidade filha; excluir e desativar bloqueiam quando `contar` na RN filha e maior que zero |
| `colunas[].unico` | `true` gera validacao de chave candidata unica (por unidade quando ha `escopoUnidade`); nao vale para PK nem N:N |

## Regras que o gerador aplica

- Toda tabela e toda coluna precisam de `comentario`.
- Textos exibidos (`singular`, `plural`, `comentario`, `rotulo`) aceitam apostrofo (o motor escapa nos literais PHP e JavaScript) e rejeitam `"`, `\`, `<`, `>`, `&`, caractere de controle e `*/`.
- CRUD simples: a PK deve se chamar `id_<tabela>`.
- N:N: `regrasGeracao.campoSinAtivo` deve ser `null`; o nome `md_<sigla>_rel_<a>_<b>` e preferido e gera alerta quando ausente.
- FK que nao repete o nome da PK de origem e aceita (papeis distintos como origem e destino) e gera alerta; duas FKs para a mesma tabela recebem alias SQL no DTO.
- O helper `<Classe>INT::montarSelect<CampoExibicao>` de cada FK precisa existir em `web/int/` (tabela do core) ou no `int/` do modulo; classe encontrada sem o metodo falha com mensagem, classe ausente gera alerta.
- `teclaAtalho` nao pode ser `S`, `C` ou `F` (botoes do cadastro) e, em coluna FK, tambem nao pode ser `N`, `E`, `T` ou `R` (botoes da lista).
- `sta_*` (status multivalorado) e rejeitado.
- `timestamp` exige prefixo `dth_`; `date` nao pode usar `dth_`.
- Entidades com `sin_ativo` geram INT filtrando ativos por padrao e incluindo o item selecionado mesmo inativo.

## Exemplo de prompt

```text
Use o contrato em .agents/skills/sei-gerador-crud/examples/contrato-entidade-minimo.json
como base, ajuste para a tabela md_ri_classificacao e gere o CRUD no modulo alvo.
```
