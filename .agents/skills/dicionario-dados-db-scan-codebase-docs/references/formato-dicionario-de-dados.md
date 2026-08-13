# Formato dos dicionarios de dados

Autoridade sobre: nomes, titulos, cabecalhos, ancoras, ordem e forma de `dicionario_tabelas.md`, `dicionario_colunas.md`, `CHANGELOG.md`, relatorio de atualizacao e relatorio de varredura.

Esta referencia nao decide conteudo, confianca ou localizacao; o `SKILL.md` carrega as autoridades correspondentes quando aplicaveis.

Leia apenas a secao do artefato que sera escrito ou verificado e a [secao de validacao](#validacao-da-forma).

## Artefatos e destinos

| Artefato | Persistencia | Destino |
|---|---|---|
| `dicionario_tabelas.md` | Arquivo versionado | Pasta de publicacao declarada pelo adaptador |
| `dicionario_colunas.md` | Arquivo versionado | Mesma pasta de `dicionario_tabelas.md` |
| `CHANGELOG.md` | Arquivo versionado | Mesma pasta dos dois dicionarios |
| Relatorio de atualizacao | Arquivo versionado, quando aplicavel | Pasta de relatorios declarada pelo adaptador |
| Relatorio de varredura | Somente resposta ao usuario | Nao gravar em arquivo |

Nao produza outro tipo de dicionario ou representacao paralela. Destino indeterminado bloqueia a escrita do artefato.

## Codificacao dos artefatos

Escreva os quatro arquivos persistentes em UTF-8 sem BOM, independentemente da codificacao das fontes lidas. Nao quebre uma linha de tabela Markdown no meio de uma celula.

Dentro de qualquer celula Markdown:

- escape todo pipe literal como `\|`, inclusive dentro de codigo inline;
- nunca escape `<`, `>` e `&` como entidade HTML (`&lt;`, `&gt;`, `&amp;`); escreva a marcacao HTML (`<ul>`, `<li>`, etc.) de forma literal, sem escape;
- mantenha listas HTML completas em uma unica linha fisica.

## Versoes, identificadores e ancoras

A gramatica vem do adaptador efetivo:

- Renderize a versao no titulo e no cabecalho do `CHANGELOG.md` exatamente na forma publicada que o adaptador declarar. Nao acrescente `v`, nao converta para SemVer e nao normalize zeros por conta propria.
- Ordene versoes pela regra de comparacao do adaptador, nao por comparacao textual.
- Reproduza identificadores fisicos de tabelas, colunas, chaves, indices e restricoes sem alterar caixa, citacao ou qualificacao admitida pela gramatica do alvo.
- Gere a ancora de cada tabela pela regra declarada pelo adaptador. Resolva colisoes conforme essa mesma regra; nao dependa implicitamente do comportamento de um renderizador Markdown.

Se a gramatica do alvo nao puder ser expressa pelo verificador atual, execute os checks compativeis e registre os demais como validacao manual. Isso nao autoriza adaptar o identificador para caber na ferramenta.

## Dois dicionarios, um conjunto

Os dois dicionarios sao mantidos juntos e descrevem o mesmo conjunto de tabelas na mesma versao.

- `dicionario_tabelas.md` contem uma linha por tabela.
- `dicionario_colunas.md` contem indice, uma secao por tabela e uma linha por coluna.
- Uma tabela aparece exatamente uma vez em cada arquivo.
- A descricao da tabela e textualmente igual nos dois arquivos: compare a sequencia UTF-8 depois de remover apenas espacos externos. Marcacao HTML, pontuacao e capitalizacao tambem precisam coincidir.

## Estrutura de dicionario_tabelas.md

```text
# <titulo comum declarado pelo adaptador> - <versao renderizada pelo adaptador>

| Tabela | Descrição |
|---|---|
| <identificador fisico da tabela A> | <descricao da tabela A> |
| <identificador fisico da tabela B> | <descricao da tabela B> |
```

- Use exatamente um `H1` e uma unica tabela Markdown.
- Nao crie indice nem secoes por tabela.
- Use exatamente os cabecalhos `Tabela` e `Descrição`, nessa ordem.
- Ordene as linhas pelo identificador fisico em ordem lexicografica crescente, sem alterar caixa para comparar.
- Escreva somente o identificador fisico na celula `Tabela`, sem anotacoes de navegacao ou situacao.

## Estrutura de dicionario_colunas.md

```text
# <mesmo titulo e mesma versao de dicionario_tabelas.md>

## Índice de Tabelas

- [<identificador da tabela A>](#<ancora da tabela A>)
- [<identificador da tabela B>](#<ancora da tabela B>)

## <identificador fisico da tabela A>

<descricao textualmente igual a dicionario_tabelas.md>

| Tabela | Coluna | Descrição |
|---|---|---|
| <tabela A> | <coluna> | <descricao> |

## <identificador fisico da tabela B>

<descricao textualmente igual a dicionario_tabelas.md>

| Tabela | Coluna | Descrição |
|---|---|---|
| <tabela B> | <coluna> | <descricao> |
```

- Use exatamente um `H1`, seguido imediatamente por `## Índice de Tabelas`.
- Cada item do indice usa o identificador fisico como rotulo e a ancora calculada pelo adaptador como destino.
- Indice e secoes possuem o mesmo conjunto, sem duplicidade, e aparecem na mesma ordem lexicografica das linhas de `dicionario_tabelas.md`.
- Cada secao usa esta ordem exata: `H2`, linha em branco, descricao em uma unica linha fisica, linha em branco, tabela Markdown.
- Use exatamente os cabecalhos `Tabela`, `Coluna` e `Descrição`, nessa ordem, em toda secao.
- A celula `Tabela` repete em cada linha o identificador fisico exato do `H2`.
- Nao envolva as secoes em outro cabecalho e nao acrescente origem, metodologia ou relatorio ao documento.

### Ordem das colunas

Depois da coluna Markdown `Tabela`, ordene as linhas assim:

1. Coluna identificadora da entidade, quando corresponder ao padrao efetivo declarado pelo adaptador.
2. Demais colunas em ordem lexicografica crescente pelo identificador fisico, sem normalizacao de caixa.

Quando a tabela nao tiver a coluna identificadora declarada, ordene todas as colunas lexicograficamente. Nao promova chave estrangeira nem presuma um padrao pelo nome.

### Descricao de coluna

A forma da celula e a formula obrigatoria de coluna carregada pelo `SKILL.md`. Especializacoes do adaptador apenas identificam o conteudo dos termos entre colchetes e nao podem alterar a formula.

Na formula com dominio multivalorado, a frase fixa "um dominio multivalorado de [quantidade] valores fixos, listados a seguir" nao repete a lista final: preserve a frase `Valores do domínio:` e converta os itens do template para `<ul><li><valor>: <descrição negocial></li></ul>` imediatamente depois dos dois-pontos, na mesma linha fisica da celula, uma unica vez. Inclua todos os valores comprovados, inclusive quando houver um unico valor, independentemente da quantidade mostrada no template.

- Termine a frase introdutoria em dois-pontos e coloque `<ul>` imediatamente depois.
- Use um unico `<ul>` e um `<li>` por valor, sem quebra fisica de linha.
- Preserve a ordem comprovada do dominio; na ausencia de ordem negocial, use a ordem da fonte com maior autoridade para essa dimensao.
- Registre qualquer limitacao do dominio no termo correspondente da ultima frase obrigatoria, nao depois da lista.

## Marcacao de lacuna

Nao insira rotulo, flag, texto fixo ou significado presumido no identificador, no cabecalho ou na descricao para representar uma lacuna.

Se qualquer termo da formula obrigatoria estiver indeterminado, a descricao afetada permanece incompleta: preserve o texto anterior somente quando ele continuar integralmente comprovado e ja obedecer a formula; caso contrario, nao publique uma frase substituta e registre a lacuna no relatorio. O artefato nao pode ser declarado completo enquanto o requisito de descricao permanecer sem atendimento.

## Relatorio de atualizacao

Gere o arquivo quando uma atualizacao produzir delta em tabela, coluna, descricao ou outra propriedade fisica documentada. O nome do arquivo, o titulo e a renderizacao da versao seguem os templates do adaptador.

Forma minima:

```text
# <titulo do relatorio de atualizacao>

## Escopo

| Campo | Valor |
|---|---|
| Alvo | <alvo> |
| Versão | <versao renderizada pelo adaptador> |
| Comparação | <estado anterior> → <estado novo> |

## Resumo

| Medida | Antes | Depois | Delta |
|---|---:|---:|---:|
| Tabelas | <n> | <n> | <n> |
| Colunas | <n> | <n> | <n> |

## <versao renderizada pelo adaptador>

### Adicionado

<tabelas, colunas ou propriedades adicionadas>

### Alterado

<tabelas, colunas, descricoes ou propriedades alteradas>

### Excluído

<tabelas, colunas ou propriedades excluidas>

## Evidencias e limitacoes

| Objeto ou grupo | Afirmação | Confiança | Evidências | Limitação |
|---|---|---|---|---|
| <objeto ou grupo> | <resultado relevante> | <nivel do processo> | <fontes> | <nenhuma ou lacuna> |
```

- Use somente as categorias com conteudo, na ordem mostrada.
- Ordene grupos de versao pela gramatica do adaptador, da mais recente para a mais antiga.
- Para tabela adicionada, inclua sua descricao e todas as colunas.
- Para objeto alterado, mostre antes e depois quando ambos forem comprovados.
- Cada afirmacao relevante recebe explicitamente um nivel de confianca definido pelo processo semantico.
- `verificar_dicionario.py diff --json` pode fornecer contagens e deltas entre dicionarios, mas nao substitui a leitura de propriedades fisicas que os dicionarios nao armazenam.

## Relatorio de varredura

Entregue na resposta ao usuario sempre que houver analise semantica. Nao grave esse relatorio nos artefatos persistentes.

Forma minima:

```text
## Varredura de <alvo>, <versao conforme o adaptador>

| Tipo de evidência | Escopo varrido | Resultado | Confiança |
|---|---|---|---|
| <tipo declarado pelo adaptador> | <artefatos ou grupo> | <achado, sem achado, não se aplica ou não acessado> | <nivel do processo> |

### Conflitos

| Objeto | Tipo | Leituras | Impacto | Decisão pendente | Confiança |
|---|---|---|---|---|---|
| <objeto> | estrutural ou semântico | <leituras> | <impacto> | <decisao> | Conflito estrutural ou Conflito semântico |

### Lacunas

| Objeto ou grupo | Rodadas concluídas | Resultado | Informação necessária | Confiança |
|---|---|---|---|---|
| <objeto ou grupo> | <rodadas> | <resultado> | <informacao ou nenhuma> | Não determinado |

### Critérios de aceitação

| Critério | Medida | Resultado | Método |
|---|---:|---|---|
| <A1 a A10 aplicável> | <n> | aprovado, reprovado ou não aplicável | automatizado ou manual |
```

- Use os niveis definidos pelo processo; nao crie uma escala paralela.
- Registre `nao se aplica` e `nao acessado` com motivo.
- Resultados sem achado equivalentes podem ser agregados; nao esconda excecoes no grupo.
- Nomeie individualmente conflito, lacuna e afirmacao positiva que altere uma descricao.

## CHANGELOG.md

O `CHANGELOG.md` registra fatos de estrutura por versao. Conteudo semantico ou de qualidade pertence aos dicionarios e relatorios.

### Titulo e cabecalhos

```text
# <titulo de changelog declarado pelo adaptador>

## [<identificador de versao renderizado pelo adaptador>]
```

- Use exatamente um `H1` e um `H2` por versao incluida.
- Nao escreva data, preambulo, metodologia ou links de comparacao.
- Cada identificador de versao aparece uma unica vez.
- Ordene as versoes da mais recente para a mais antiga segundo a gramatica do adaptador.

### Categorias e ordem

Dentro de cada versao, use somente as categorias com conteudo e sempre nesta ordem:

1. `### Adicionado`
2. `### Alterado`
3. `### Excluído`

Omita a versao inteira quando nao houver mudanca fisica liquida. Dados de referencia, permissao, menu, mensagem, agendamento e mudanca apenas semantica nao entram.

### Forma das entradas

```text
### Adicionado

- **Tabela `<tabela_nova>`**

### Alterado

- **Tabela `<tabela_existente>`**
  - **Colunas**
    - **Nova `<coluna_nova>`**
    - **Alterada `<coluna>`**: `<propriedade>`: `<antes>` para `<depois>`; `<outra propriedade>`: `<antes>` para `<depois>`.
  - **Chaves primárias**
    - **Alterada `<identificador ou assinatura>`**: `<definicao anterior>` para `<definicao nova>`.
  - **Chaves estrangeiras**
    - **Nova `<identificador ou assinatura>`**
  - **Índices**
    - **Novo `<identificador ou assinatura>`**
  - **Restrições**
    - **Alterada `<identificador ou assinatura>`**: `<definicao anterior>` para `<definicao nova>`.
  - **Propriedades da tabela**
    - **Alterada `<propriedade>`**: `<antes>` para `<depois>`.

### Excluído

- **Tabela `<tabela_excluida>`**
- **Tabela `<tabela_mantida>`**
  - **Colunas**
    - **Excluída `<coluna_excluida>`**
```

- Tabela criada ou excluida e bullet principal sem enumerar sua estrutura interna.
- Em tabela mantida, prefira esta ordem para nova escrita: `Colunas`, `Chaves primárias`, `Chaves estrangeiras`, `Índices`, `Restrições`, `Propriedades da tabela`. Outra ordem inequívoca permanece válida quando cada tópico aparecer uma única vez.
- Use os topicos mesmo com um unico objeto e omita topicos vazios.
- Registre qualquer propriedade fisica comprovadamente alterada, como tipo, tamanho, precisao, escala, nulidade, valor padrao, geracao, identidade, expressao, collation, armazenamento, particionamento, composicao, ordem ou regra de integridade.
- Para alteracao, prefira nomear cada propriedade e mostrar os estados anterior e novo. Uma definição física direta, uma recriação ou outra operação comprovada também pode ser registrada quando a fonte não expuser ambos os estados. Adição e exclusão podem trazer detalhe físico factual; não invente o estado ausente.
- Preserve na definicao os tokens da fonte estrutural. Traduza uma chamada de framework somente quando o adaptador declarar mapeamento inequivoco.
- Use um bullet por objeto. Identifique objeto sem nome pela assinatura fisica suficiente para distingui-lo.
- Renomeacao comprovada usa `renomeada de <antigo>` na entrada do nome novo. Sem prova de renomeacao, registre exclusao e adicao separadamente.
- Nao inclua finalidade, justificativa negocial nem significado de valor.

## Validacao da forma

Use os subcomandos de `../scripts/verificar_dicionario.py` indicados em `../SKILL.md` somente para o subconjunto que implementam.

Use `--help` e os testes do script como autoridade sobre os checks automatizados. Exigem leitura manual, entre outros: ordem não numérica sem `--ordem-versoes`, âncora divergente da implementação, identificador fora do subconjunto parseável, completude das propriedades físicas e correspondência do changelog com a fonte estrutural.

A9 combina o resultado automatizado e o manual. Codigo de saida zero da ferramenta nao aprova sozinho a forma completa.
