# 4. InfraPHP

## Visão Geral

A arquitetura propõe a separação em múltiplas camadas, denominadas: **Cliente**, **RN** e **BD**. Cada camada possui um conjunto definido de responsabilidades:

- **Cliente**
  - Interação com o usuário ou outros sistemas.
  - Validações simples que não necessitem acesso a dados.
- **RN**
  - Controle de transação.
  - Validação de permissões.
  - Auditoria.
  - Validação das regras de negócio.
- **BD**
  - Persistência.
  - Recuperação de dados.

Além disso, devem ser respeitadas as seguintes regras:

- Toda a comunicação ocorre somente entre RNs, garantindo que sempre serão executadas as permissões de acesso, regras de negócio e auditoria;
- Uma RN não pode chamar uma BD de outra classe;
- Não deve ocorrer comunicação direta entre BDs; e
- Uma BD não pode persistir ou atualizar dados em mais de uma tabela.

## InfraDTO

Para comunicação entre as camadas foi adotado o padrão de projeto **DTO** (`Data Transfer Object`), que consiste basicamente em passar apenas um objeto nas chamadas de métodos. Assim, por exemplo, na inserção de um documento, ao invés de passar todos os valores necessários como parâmetros individuais para o método de inserção, é criada uma classe para transporte denominada DocumentoDTO. Essa classe contém atributos para todos os valores envolvidos. Para inserir um documento deve ser instanciado um objeto dessa classe, sendo preenchidos os atributos com os valores correspondentes. Após essa etapa o objeto de transporte deve ser passado para o método de inserção.

Todo o tráfego **entre as camadas** deve ser feito utilizando DTOs. Essa abordagem reduz acoplamento, melhora a legibilidade do código e preserva compatibilidade com os bancos de dados suportados pelo sistema.

O framework estendeu o conceito original para permitir que o DTO seja uma fonte de informações do modelo de dados, que possibilite a geração automática de instruções SQL. Para isso, todos os DTOs deverão herdar da classe InfraDTO, implementando alguns métodos abstratos. Ao realizar esse procedimento a classe InfraDTO passará a fornecer automaticamente o seguinte conjunto de métodos:

| Método | Descrição |
|---|---|
| set\<atributo> | Configura o valor do atributo. A configuração do valor do atributo terá reflexos na operação que será realizada com o DTO:<br><ul><li>Inserções -- serão considerados na montagem do `INSERT`</li><li>Alterações -- serão adicionados ao bloco `SET` do `UPDATE`</li><li>Consultas -- serão adicionados a cláusula `WHERE`. Nesse caso aceitará um segundo parâmetro, informado o critério de filtro:<br>`InfraDTO::$OPER_IN`<br>`InfraDTO::$OPER_NOT_IN`<br>`InfraDTO::$OPER_IGUAL (valor padrão)`<br>`InfraDTO::$OPER_DIFERENTE`<br>`InfraDTO::$OPER_LIKE`<br>`InfraDTO::$OPER_NOT_LIKE`<br>`InfraDTO::$OPER_MAIOR`<br>`InfraDTO::$OPER_MENOR`<br>`InfraDTO::$OPER_MAIOR_IGUAL`<br>`InfraDTO::$OPER_MENOR_IGUAL`</li></ul> |
| get\<atributo> | Retorna o valor do atributo. |
| unSet\<atributo> | Passa a indicar que o atributo não possui mais valor configurado. |
| isSet\<atributo> | Verifica se o atributo possui valor configurado (utilizado na montagem do SQL). |
| ret\<atributo> | Indica que o atributo deve ser retornado em consultas. |
| unRet\<atributo> | Passa a indicar que o atributo não deve mais retornar na consulta. |
| isRet\<atributo> | Verifica se o atributo deve retornar (utilizado na montagem do SQL). |
| setOrd\<atributo> | Indica que o atributo deve ser utilizado para ordenação. Recebe um parâmetro informando o tipo de ordenação (ascendente ou descendente):<br>`InfraDTO::$TIPO_ORDENACAO_ASC`<br>`InfraDTO::$TIPO_ORDENACAO_DESC`<br>Esse método obedece a ordem de configuração dos atributos (para ordenação por múltiplos atributos). |
| getOrd\<atributo> | Retorna o tipo de ordenação configurado atualmente para o atributo (utilizado na montagem do SQL). |
| unOrd\<atributo> | Passa a indicar que o atributo não deve mais ser utilizado para ordenação. |
| isOrd\<atributo> | Verifica se o atributo deve ser utilizado para ordenação (utilizado na montagem do SQL). |
| retTodos | Indica que todos os atributos devem ser retornados em uma consulta. Recebe um parâmetro true/false para indicar se os campos das tabelas relacionadas também devem ser retornados (valor padrão false). |
| unSetTodos | Indica que nenhum atributo possui valor configurado. |
| unRetTodos | Indica que nenhum atributo deve retornar em uma consulta. |
| unOrdTodos | Indica que nenhum atributo deve ser utilizado para ordenação. |

Constantes de prefixos de tipos:

| Nome | Descrição | Formato |
|---|---|---|
| InfraDTO::$PREFIXO_NUM | Numérico sem decimais |  |
| InfraDTO::$PREFIXO_DIN | Valor monetário | 999.999,99 |
| InfraDTO::$PREFIXO_DBL | Numérico com decimais | 999999,99 |
| InfraDTO::$PREFIXO_STR | Texto |  |
| InfraDTO::$PREFIXO_DTA | Data | dd/mm/aaaa |
| InfraDTO::$PREFIXO_DTH | Data e hora | dd/mm/aaaa hh:mm:ss |
| InfraDTO::$PREFIXO_BOL | Booleano |  |
| InfraDTO::$PREFIXO_ARR | Array |  |
| InfraDTO::$PREFIXO_OBJ | Objeto |  |
| InfraDTO::$PREFIXO_BIN | Dados binários |  |

A montagem do DTO pode utilizar os métodos do InfraDTO descritos abaixo:

- **`getStrNomeTabela`**

Método abstrato, que retorna o nome da tabela correspondente no banco de dados (retorna *null* se o DTO não é persistido em uma tabela). Essa tabela será a principal na geração de SQLs com inner e left joins montados em relação a ela.

- **`montarDTO`**

Método abstrato, usado para adicionar e configurar os atributos do DTO.

- **`adicionarAtributo ($strPrefixo, $strNome)`**

Adiciona um atributo que não é persistido no DTO.

| strPrefixo | Utilizar uma das constantes de prefixo de tipo da classe. |
|---|---|
| strNome | Nome do atributo. |

- **`adicionarAtributoTabela($strPrefixo, $strNome, $strCampoSql)`**

Adiciona um atributo da tabela principal no DTO.

| strPrefixo | Utilizar uma das constantes de prefixo de tipo da classe. |
|---|---|
| strNome | Nome do atributo. |
| strCampoSql | Nome do campo correspondente na tabela do banco de dados. |

- **`adicionarAtributoTabelaRelacionada($strPrefixo, $strNome, $strCampoSqlRelacionado, $strTabelaRelacionada)`**

Adiciona um atributo de uma tabela relacionada com a tabela principal do DTO. O uso desse método requer a configuração da chave-estrangeira correspondente através do método `configurarFK`.

| strPrefixo | Utilizar uma das constantes de prefixo de tipo da classe. |
|---|---|
| strNome | Nome do atributo no formato \<campo>\<tabela relacionada>. Exemplo: NomeSerie, SiglaOrgao. |
| strCampoSqlRelacionado | Nome do campo correspondente na tabela relacionada do banco de dados. |

- **`configurarPK($strAtributo, $numTipoPK)`**

Indica que o atributo é chave-primária.

- **`configurarFK($strAtributo, $strTabelaRelacionda, $strCampoRelacionado, $numTipoFK,$numFiltroFK)`**

Indica que o campo é chave-estrangeira, onde:

| strAtributo | Nome do atributo. Deve ser igual ao nome de um atributo já adicionado ao DTO através dos métodos `adicionarAtributo` ou `adicionarAtributoTabelaRelacionada`. |
|---|---|
| strTabelaRelacionada | Nome da tabela que contém o atributo chave-primária correspondente a essa chave-estrangeira. |
| strCampoRelacionado | Nome do campo chave-primária na tabela relacionada. |
| $numTipoFK | Informa o tipo da chave-estrangeira, utilizar uma das constantes:<br><ul><li>`InfraDTO::$TIPO_FK_OBRIGATORIA` (default) - fará um INNER JOIN com a tabela principal.</li><li>`InfraDTO::$TIPO_FK_OPCIONAL` - fará um LEFT JOIN com a tabela principal.</li></ul> |
| $numFiltroFK | Indica a forma como os registros relacionados serão filtrados:<br><ul><li>`InfraDTO::$FILTRO_FK_ON` (default) - montará filtros da tabela relacionada diretamente no inner ou left join através da cláusula ON.</li><li>`InfraDTO::$FILTRO_FK_WHERE` - aplicará o filtro sobre o resultado final da consulta na cláusula WHERE.</li></ul> |

- **`configurarExclusaoLogica($strAtributo, $valorDesativado)`**

Sinaliza qual atributo deve ser atualizado no caso de uma exclusão lógica (método desativar).

| strAtributo | Nome do atributo. Deve ser igual ao nome de um atributo já adicionado ao DTO através do método adicionarAtributo. |
|---|---|
| valorDesativado | Informa qual valor representa um registro desativado. |

Exemplo de código de um DTO:

```php
class DocumentoDTO extends InfraDTO {
  public function getStrNomeTabela() {
    return "documento";
  }

  public function montarDTO() {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DBL, "IdDocumento", "id_documento");
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, "IdSerie", "id_serie");
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, "Numero", "numero");

    //... demais campos da tabela documento ...

    $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, "NomeSerie", "nome", "serie");
    $this->configurarPK("IdDocumento", InfraDTO::$TIPO_PK_NATIVA);
    $this->configurarFK("IdSerie", "Serie", "id_serie");
  }
```

| strAtributo | Nome do atributo. Deve ser igual ao nome de um atributo já adicionado ao DTO através do método adicionarAtributo. |
|---|---|
| numTipoPK | Informa o tipo da chave-primária. Utilizar uma das constantes:<br><ul><li>`InfraDTO::$TIPO_PK_INFORMADO` - ao inserir um registro o valor do ID deve ser informado através da chamada do método set<atributo\> correspondente).</li><li>`InfraDTO::$TIPO_PK_SEQUENCIAL` - na inserção a classe de banco buscará o próximo ID através da classe de infraestrutura InfraSequencia.</li><li>`InfraDTO::$TIPO_PK_NATIVA` - na inserção a classe de banco buscará o próximo ID através em um objeto de sequência. Ver seção Padrão de Modelagem de Dados.</li></ul> |

Exemplo de uma consulta utilizando o DTO anterior:

1) Retornar IdDocumento, Tipo do Documento e Número;
2) Somente para tipos de documento com ID igual a 18 e 20 (Atos e Portarias);
3) Ordenadas pelo tipo de documento ascendente e pelo número descendente

```php
$objDocumentoDTO = new DocumentoDTO();
$objDocumentoDTO->retDblIdDocumento();
$objDocumentoDTO->retStrNomeSerie();
$objDocumentoDTO->retStrNumero();
$objDocumentoDTO->setNumIdSerie(array(18,20),InfraDTO::$OPER_IN);
$objDocumentoDTO->setOrdStrNomeSerie(InfraDTO::$TIPO_ORDENACAO_ASC);
$objDocumentoDTO->setOrdStrNumero(InfraDTO::$TIPO_ORDENACAO_DESC);

$objDocumentoRN = new DocumentoRN();
$arrObjDocumentoDTO =
$objDocumentoRN->listarRN0008($objDocumentoDTO);
```

Consulta SQL gerada automaticamente:

```sql
SELECT documento.id_documento AS iddocumento,serie.nome AS
nomeserie,documento.numero

FROM documento INNER JOIN serie ON documento.id_serie=serie.id_serie

WHERE documento.id_serie IN (18,20)

ORDER BY serie.nome ASC, documento.numero DESC
```

**Boas práticas para consultas em autocompletes**

Em campos de autocomplete não se deve utilizar diretamente o operador **LIKE** sobre as principais colunas textuais da tabela (strings), como nome, e-mail, CPF, CNPJ ou equivalentes.

Sempre que houver campo de **indexação textual** específico para pesquisa, a consulta deve ser realizada sobre esse campo indexado, utilizando previamente a função de preparação de índice disponibilizada pelo SEI.

Essa abordagem melhora o desempenho das consultas, reduz varreduras desnecessárias em múltiplas colunas nas tabelas e torna a pesquisa mais adequada para volumes maiores de dados.

Exemplo de preparação do valor para pesquisa:

```php
$valorIndexado = InfraString::prepararIndexacao($valorPesquisa, true);

// Exemplo de uso para Contato
$valorIndexado = InfraString::prepararIndexacao($valorPesquisa, true);
$objContatoDTO->setStrIdxContato('%' . $valorIndexado . '%', InfraDTO::$OPER_LIKE);
```

## InfraPagina (1ª Camada)

A interface é composta por arquivos PHP que acessam as classes RN e geram páginas HTML. Para a comunicação com a 2ª camada os dados devem ser encapsulados em DTOs e repassados para os métodos adequados. A comunicação entre elementos da interface pode ser feita através GET, POST ou variáveis de sessão, considerando que:

- A URL de uma página deve conter pelo menos um parâmetro obrigatório denominado `acao`, cujo valor deve ser composto por **\<entidade>_\<acao>** (por exemplo: documento_assinar, serie_excluir e cidade_listar). **Normalmente estes valores correspondem a recursos no SIP**;

- Deve existir um módulo controlador denominado `controlador.php` que estabeleça a navegação entre páginas diferentes através da análise do parâmetro `acao`;

- Toda página deve submeter os seus dados para ela mesma ou para o módulo controlador.

Os principais arquivos de interface para cada entidade do sistema são:

- `<nome da entidade>_lista.php` - listagem ou pesquisa de registros. Nessa tela normalmente também são realizadas operações sobre vários registros simultaneamente, como exclusão e desativação;

- `<nome da entidade>_cadastro.php` - suporta as operações de cadastro, alteração e consulta;

- `<nome da entidade>INT.php` - elementos de interface compartilhados (combos, checkboxes, formatação de dados para exibição, etc...).

**Para facilitar o desenvolvimento da interface, foi implementada uma classe denominada `InfraPagina`**, que monta todo o esqueleto das páginas, adicionando barras superiores, menu, barra de comandos, etc. Essa classe pode ter outras especializações montando páginas com layouts diferentes: `InfraPaginaEsquema` e `InfraPaginaEsquema2`.

Exemplo para montagem de página com a classe `InfraPagina`:

```php
<?
try {
  require_once dirname(__FILE__).'/../../SEI.php';
  session_start();

  //////////////////////////////////////////////////////////////////////////////
  //InfraDebug::getInstance()->setBolLigado(false);
  //InfraDebug::getInstance()->setBolDebugInfra(false);
  //InfraDebug::getInstance()->limpar();
  //////////////////////////////////////////////////////////////////////////////

  SessaoSEI::getInstance()->validarLink();
  SessaoSEI::getInstance()->validarPermissao($_GET['acao']);

  $arrComandos = array();

  switch($_GET['acao']){
    case 'md_abc_exemplo1':
      $strTitulo = 'Exemplo 1 ABC';
      //processamento
      break;
    case 'md_abc_exemplo2':
      $strTitulo = 'Exemplo 2 ABC';
      //processamento
    break;
    default:
    throw new InfraException("Ação '".$_GET['acao']."' não reconhecida.");
  }
//monta tabela se for página de listagem
}catch(Exception $e){
  PaginaSEI::getInstance()->processarExcecao($e);
}

PaginaSEI::getInstance()->montarDocType();
PaginaSEI::getInstance()->abrirHtml();
PaginaSEI::getInstance()->abrirHead();
PaginaSEI::getInstance()->montarMeta();
PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema().' - '.$strTitulo);
PaginaSEI::getInstance()->montarStyle();
PaginaSEI::getInstance()->abrirStyle();
?>
/* CSS */
<?
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
/* Javascript */
<?
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo,'onload="inicializar();"');
?>
<form ....>
<?
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
<!-- HTML \-->
<?

PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->montarAreaTabela($strResultado, $numRegistros);
//PaginaSEI::getInstance()->montarAreaDebug();
PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos);
?>
</form>
<?
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
?>
```

Segue abaixo a relação de classes CSS disponíveis:

| Controle HTML | Classe CSS | Observação |
|---|---|---|
| Input type = [button, reset,submit] | infraButton |  |
| label | infraLabelOpcional | Descrição decampos opcionais. |
| label | infraLabelObrigatorio | Descrição decampos obrigatórios. |
| table | infraTable |  |
| tr | infraTrClara | Linha clara em tabelas deresultado. |
| tr | infraTrEscula | Linha escura em tabelas deresultado. |
| th | infraTh | Linha de títulopara tabelas. |
| caption | infraCaption | Linha de descrição da tabela. |
| Input type = checkbox | infraCheckbox |  |
| Input type = radio | infraRadio |  |
| fieldset | infraFieldset |  |
| legend | infraLegendOpcional | Grupo de campos opcional. |
| legend | infraLegendObrigatorio | Grupo de campos obrigatório. |
| span | infraTeclaAtalho | Visualização da tecla de atalho em um label. |
| form | infraForm |  |
| Input type = text | infraText |  |
| Input type = password | infraPassword |  |
| textarea | infraTextarea |  |
| select | infraSelect |  |


## InfraRN (2ª Camada)

A segunda camada implementa o padrão de projeto `Facade` (um tipo de *design pattern* de sistemas), funcionando como uma fachada de acesso aos conceitos do sistema. Nela todas as regras de negócio levantadas devem ser implementadas incluindo regras simples que já tenham sido validadas na interface, como o tamanho máximo de campos e a validação de datas. Dessa forma, garantimos que qualquer cliente (browser, web service, app, ...) que acesse as classes da 2ª camada realizará as validações de regras, permissões e auditorias necessárias.

A classe InfraRN implementa um mecanismo para controle automático do contexto de conexão ou transação. Para utilização dessa classe é necessário que:

1) a classe de 2ª camada herde de `InfraRN`;

2) seja implementado o método `inicializarObjInfraIBanco`;

3) para cada método que se deseja controlar deve criar um método protegido com o sufixo `Controlado` ou `Conectado`, recebendo como parâmetro apenas o DTO da entidade ou um array de parâmetros. Ao invocar métodos com o sufixo `Conectado` a classe abrirá uma conexão se já não estiver aberta e com o sufixo `Controlado` abrirá uma conexão e uma transação se já não estiverem abertas.

Exemplo de método da camada de regras de negócio:

```php
protected function processarControlado($objDocumentoDTO) {
  try{
    //Validação de Permissão e Auditoria
    //Validação de Regras de Negócio
    //Executa métodos de outras RNs e da BD de documento
  }catch(Exception $e){
    throw new InfraException("Erro processando documento.",$e);
  }
}
```

Utilizando esse mecanismo, após a primeira chamada a um método `Conectado` ou `Controlado`, a conexão ficará aberta até o final da execução do script. Transações vão respeitar o mesmo escopo do método, sendo confirmadas no final da execução do método ou canceladas caso uma exceção seja lançada.

## InfraBD (3ª camada)

A classe BD isola a forma como os dados são acessados e foi desenvolvida com o objetivo de automatizar os métodos básicos: cadastrar, alterar, consultar, listar, contar, excluir, desativar, reativar e bloquear. Para sua utilização basta que a classe de 3ª camada herde de `InfraBD` e repasse para seu construtor a instância do banco recebida da classe de 2ª camada:

```php
class DocumentoBD extends InfraBD {
  public function __construct($objInfraIBanco){
    parent::__construct($objInfraIBanco);
  }
}
```

Após esse procedimento as chamadas aos métodos automatizados serão respondidas pela classe `InfraBD`, que dinamicamente montará o comando SQL de acordo com a configuração do DTO recebido. A classe também disponibiliza o método `getObjInfraIBanco` para recuperação do objeto passado para o seu construtor.

Se for necessário implementar algo específico na BD é recomendado utilizar os métodos abaixo:

- formatarGravacao [Dta \| Dth \| Str \| Bol \| Num \| Din \| Dbl \| Bin]
  - Para converter o formato para gravação no banco.
- formatarLeitura [Dta \| Dth \| Str \| Bol \| Num \| Din \| Dbl \| Bin]
  - Para converter o formato lido do banco.
- formatarSelecao [Dta \| Dth \| Str \| Bol \| Num \| Din \| Dbl \| Bin]
  - Para informar ao banco como trazer o campo (cast).

Exemplo de método de alteração na camada de banco:

```php
public function processarXXXXX($objXxxxxDTO){
  try {

    $objBanco = $this->getObjInfraIBanco();

    $sql = "UPDATE xxxxx SET
    campo_e=".$objBanco->formatarGravacaoStr('T')." WHERE campo_d <= ".$objBanco->formatarGravacaoDta('01/01/2016');

    $objBanco->executarSql($sql);

  }catch(Exception $e){
    throw new InfraException("Erro processando XXXXX.",$e);
  }
}
```

Mais um exemplo de método de alteração na camada de banco:

```php
public function listarXXXXX() {
  try {

    $objBanco = $this->getObjInfraIBanco();

    $sql = "SELECT ".
           $objBanco->formatarSelecaoNum('xxxxx','campo_a','CampoA').",".
           $objBanco->formatarSelecaoStr('xxxxx','campo_b','CampoB').",".
           $objBanco->formatarSelecaoDta('xxxxx','campo_c','CampoC').
           " FROM xxxxx ".
           " WHERE campo_d >
           ".$objBanco->formatarGravacaoDta('01/01/2016').
           " AND campo_e = ".$objBanco->formatarGravacaoStr('A');

    $rs = $objBanco->consultarSql($sql);

    $ret = array();
    foreach($rs as $item){
      $objXxxxxDTO = new XxxxxDTO();
      $objXxxxxDTO->setNumCampoA($objBanco->formatarLeituraNum($item['CampoA']));
      $objXxxxxDTO->setStrCampoB($objBanco->formatarLeituraStr($item['CampoB']));
      $objXxxxxDTO->setDtaCampoC($objBanco->formatarLeituraDta($item['CampoC']));
      $ret[] = $objXxxxxDTO;
    }

    return $ret;
  }catch(Exception $e){
    throw new InfraException("Erro listando XXXXX.",$e);
  }
}
```

## Métodos Padronizados

### Cadastrar (Controlado)


![](../manual_desenvolvimento/imagens/image012.jpg)

- Enviar um DTO preenchido com os atributos para cadastro (**set**). Se for uma chave-primária sequencial ou nativa, então o atributo correspondente deve ser configurado com null;

- Será retornado um DTO preenchido com a chave-primária. Por questão de uniformidade no tratamento dos métodos, mesmo que a chave-primária já seja conhecida antes do cadastramento, ainda assim será retornado um DTO com o seu valor preenchido.

### Alterar (Controlado)

- Enviar um DTO preenchido (**set**) com a chave-primária e com os atributos para alteração;

- Nenhum DTO será retornado, pois não haverá acréscimo de informações.

### Consultar (Conectado)

- Enviar um DTO com os atributos de retorno (**ret**) configurados e preenchido (**set**) com atributos que identifiquem uma determinada ocorrência (chave-primária ou chave-candidata);

- Se mais de uma ocorrência for selecionada será gerado um erro;

- É retornado um DTO com os valores dos atributos solicitados de acordo com os dados atualmente persistidos. Os campos retornados estarão disponíveis para uso no objeto (**get**).

### Listar (Conectado)

- Enviar um DTO com os atributos de retorno (**ret**), pesquisa (**set**) e ordenação (**setOrd**) preenchidos;

- Será retornada uma lista de DTOs com todos os registros que atenderam aos critérios de pesquisa e preenchido com os atributos solicitados disponíveis para uso (**get**);

- Esse método não atenderá a todos os casos possíveis. Para outras pesquisas necessárias deve criar um método Conectado com estrutura semelhante, ou seja, recebendo um DTO e retornando uma lista.

### Contar (Conectado)

- Enviar um DTO com os atributos de pesquisa (**set**) preenchidos;

- Será retornado o número de ocorrências que atenderam aos critérios de pesquisa.

### Bloquear (Controlado)

- Enviar um DTO preenchido (**set**) com o atributo chave-primária;

- Será retornado um DTO com todos os atributos da ocorrência no banco;

- O registro **ficará em lock** até o fim da transação corrente.

### Excluir, Desativar e Reativar (Controlado)


![](../manual_desenvolvimento/imagens/image013.jpg)

- Enviar uma lista de DTOs com os atributos correspondentes a chave-primária preenchidos (**set**);

- A passagem de uma lista permite que o método seja utilizado para processamento em lote, visto que nas interfaces é comum selecionar mais de um item para essas operações.

- O método da RN recebe uma lista, enquanto o método da BD recebe um DTO específico.

No SIP, por meio do menu **Recursos/Gerar Padrão PHP**, é possível gerar automaticamente os recursos para utilização nos métodos padrão:


![](../manual_desenvolvimento/imagens/image014.jpg)

Observações:

- O método **contar** compartilha o mesmo recurso do método **listar**;

- O método **bloquear** compartilha o mesmo recurso do método **consultar**;

- O recurso **selecionar** é utilizado em telas de escolha de registros (**lupas**).

## InfraException

A classe `InfraException` fornece um mecanismo para transporte de validações e erros entre as camadas. Para que o tratamento ocorra de forma adequada, todo o código deve ser implementado com blocos **try ... catch**. A `InfraException` lançada deverá retornar na hierarquia de métodos até o ponto da 1ª camada que iniciou o procedimento, que então deverá informar o erro ou validação para o usuário. Todas as mensagens geradas pelo PHP (exceto Warnings) serão encapsuladas e lançadas em uma `InfraException` automaticamente.


![](../manual_desenvolvimento/imagens/image015.jpg)

Exemplos de tratamento de validações na camada de regras de negócio (**RN**):

- Lançando uma validação em um alert:

```php
$objInfraException = new InfraException();
if (...1...){
  $objInfraException->lancarValidacao('v1');
}
```

- Acumulando diversas validações e exibindo todas em um único alert:

```php
$objInfraException = new InfraException();

if (...1...) {
  $objInfraException->adicionarValidacao('v1');
}

if (...2...) {
  $objInfraException->adicionarValidacao('v2');
}

if (...3...) {
  $objInfraException->adicionarValidacao('v3');
}
$objInfraException->lancarValidacoes();
```

Atributo `__construct($strDescricao=null, $e=null)`:

\- Construtor.

| strDescricao | Opcional. Texto indicando o motivo da exceção. |
|---|---|
| e | Opcional. Exceção original capturada no bloco *catch*. |

Atributo `adicionarValidacao($strDescricao)`:

\- Armazena uma validação de Regra de Negócio.

| strDescricao | Mensagem para exibição ao usuário. |
|---|---|

Atributo `contemValidacoes()`:

\- Verifica se o objeto contém validações armazenadas retornando true/false.

Atributo `lancarValidacao($strDescricao)`:

\- Lança imediatamente uma exceção contendo a validação passada como parâmetro.

Atributo `lancarValidacoes()`:

\- Verifica se objeto contém validações armazenadas caso afirmativo então lança o objeto.

## Estrutura de Diretórios

Segue abaixo a estrutura de diretórios recomendada:

| Diretório | Conteúdo |
|---|---|
| dto | Classes de transporte <EntidadeDTO.php>. |
| int | Classes de interface <EntidadeINT.php>. |
| rn | Classes das regras de negócio <EntidadeRN.php>. |
| bd | Classes de banco <EntidadeBD.php>. |
| ws | Classes de web services <ServicoWS.php>. |
| css | Código CSS. |
| imagens | Imagens da aplicação. |
| js | Código javascript. |
