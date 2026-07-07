# 3. Considerações Prévias

Antes de iniciar a construção de um módulo é necessário conhecer o funcionamento básico do SEI com relação ao controle de Perfis, Recursos, Menus e Auditoria geridos pelo Sistema de Permissões (SIP) e questões relacionadas com o controle de Conexões e Transações, Andamentos e Classes do Sistema.

## Restrições do Ambiente

O desenvolvimento de módulos deve considerar as restrições do ambiente definidas para a instalação do SEI, pois elas impactam diretamente a implementação de telas, processamentos e integrações.

### Dependências técnicas do projeto

Além do uso do framework PHP padrão do sistema, existem algumas dependências técnicas importantes que o desenvolvedor deve observar:

- Sistema Operacional Linux;
- PHP 8.2 e extensões adicionais previstas no manual de instalação;
- Bootstrap 5.3.1;
- jQuery 3.7.0; e
- jQuery UI 1.13.2.

### Codificação de arquivos (charset)

Os arquivos textuais do módulo devem ser salvos em `ISO-8859-1`, mantendo compatibilidade com o charset configurado no servidor PHP. Não se deve assumir `UTF-8` como padrão implícito do projeto. Em caso de acentuação incorreta nas telas, deve verificar se a codificação do arquivo ou se o default_charset do PHP estão corretos, usando `ISO-8859-1`.

### Limites de upload

O tamanho máximo de upload aceito pelo ambiente deve respeitar a configuração do servidor. Como referência da instalação padrão, temos:

- `upload_max_filesize` = 200M
- `post_max_size` = 201M

O valor de `post_max_size` deve ser ligeiramente maior que `upload_max_filesize`. Além disso, o módulo deve manter coerência com o **parâmetro `SEI_TAM_MB_DOC_EXTERNO`** configurado no SEI como um todo e com os valores específicos por extensão de arquivo configurados no menu **Administração > Extensões de Arquivos Permitidas**. Portanto, não se deve implementar funcionalidades sem observar os mencionados limites configurados no SEI para upload de arquivos.

## Perfis, Recursos e Menus

Todas as operações realizadas no SEI estão atreladas a **recursos** cadastrados no SIP. Os recursos podem ou não estar associados com itens de **menu**. Os recursos e itens de menu são **agrupados em perfis** que são então liberados para os usuários **por meio das permissões**.

Os itens de menu serão montados automaticamente no login do usuário no SEI, mas outros elementos associados com recursos (como botões e ícones) devem ser tratados via programação.

- Ver seção **Classes do Sistema**, classe **SessaoSEI**, método **verificarPermissao**.

A seguir são demonstrados os passos para adicionar um item de menu em um novo perfil.

1\) criar o recurso no SIP pelo menu Recursos/Novo, sendo recomendado que recursos de módulos tenham o prefixo ``MD_<instituição/módulo>``:

![](../manual_desenvolvimento/imagens/image004.png)

2\) adicionar item de menu associado com o recurso no SIP pelo menu Menus/Montar:


![](../manual_desenvolvimento/imagens/image005.png)


![](../manual_desenvolvimento/imagens/image006.png)

Para associar um ícone com o item de menu é necessário implementar no módulo o evento `obterDiretorioIconesMenu`, colocar o arquivo SVG do ícone no diretório correspondente aos ícones de menu do módulo e informar apenas o nome do arquivo SVG no campo `Ícone` na tela de cadastro de item de menu acima.

3\) criar um perfil específico no SIP pelo menu Perfis/Novo, sendo recomendado que perfis de módulos tenham o prefixo ``MD_<instituição/módulo>``:


![](../manual_desenvolvimento/imagens/image007.png)

4\) Adicionar o recurso e o item de menu no perfil no SIP pelo menu Perfis/Montar:


![](../manual_desenvolvimento/imagens/image008.jpg)

5\) atribuir permissão no perfil criado no SIP pelo menu Permissão/Nova:


![](../manual_desenvolvimento/imagens/image009.png)

6\) O item de menu criado deve aparecer no SEI. Alterações na montagem de perfis e na atribuição de permissões no SIP demandam novo login do usuário que já esteja logado no SEI:


![](../manual_desenvolvimento/imagens/image010.jpg)

As telas de usuário externo e pesquisa de publicações não recebem itens de menu geridos pelo SIP. Entretanto, é possível adicionar itens através dos eventos `montarMenuUsuarioExterno` e `montarMenuPublicacoes`.

- Ver seção **Eventos**.

## Auditoria

Para utilizar o mecanismo de auditoria é necessário:

a\) criar uma regra de auditoria no SIP e adicionar o recurso que pretende gravar trilhas de auditoria de operação, sendo recomendado que as regras de módulos tenham o prefixo ``MD_<instituição/módulo>``;


![](../manual_desenvolvimento/imagens/image011.jpg)

b\) No método da camada de regra de negócio que realiza a operação no módulo no SEI deve incluir uma chamada para `validarAuditarPermissao`, que recebe como parâmetros o nome do recurso, o nome do método e os valores associados que devem ser gravados na tabela de auditoria. Esse método também lançará um erro de acesso negado ao recurso se o usuário não tiver permissão. Se o recurso não fizer parte de nenhuma regra de auditoria, então apenas a validação de permissão será realizada.

```php
protected function lancarAndamentosControlado($arrParametros){
  try{

    SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_andamento_lancar', __METHOD__, $arrParametros);

    //processamento

  }catch(Exception $e){
    throw new InfraException('Erro lançando andamentos do módulo ABC.',$e);
  }
}
```

As operações auditadas poderão ser consultadas no SEI pelo menu Infra/Auditoria.

## Conexões e Transações

O controle das conexões e transações no banco de dados pode ser feito manipulando diretamente o objeto `BancoSEI::getInstance()` ou utilizando os sufixos `Conectado` e `Controlado`.

- Ver mais detalhes na seção **Classes do Sistema**, classe **BancoSEI**; e na seção **InfraPHP**, classe **InfraRN**.

Se o módulo realizar processamento de operações no sistema como, por exemplo, geração de processos e inclusão de documentos então será obrigatório utilizar um dos controles descritos abaixo.

### Controle manual de conexões e transações

Para controle manual, basta chamar os métodos diretamente do objeto de banco. Exemplo:

```php
class MdAbcTesteRN {

  public function processarXXXXX($a, $b){
    try{

      BancoSEI::getInstance()->abrirConexao();
      BancoSEI::getInstance()->abrirTransacao();

      //executa comandos

      BancoSEI::getInstance()->confirmarTransacao();
      BancoSEI::getInstance()->fecharConexao();

    }catch(Exception $e){

      try{
        BancoSEI::getInstance()->cancelarTransacao();
      }catch(Exception $e2){}

      try{
        BancoSEI::getInstance()->fecharConexao();
      }catch(Exception $e2){}

      throw new InfraException('Erro processando operação XXXXX no módulo ABC.',$e);

    }
  }
}
```

**Atenção:** Pode ser um problema quando existirem chamadas entre métodos que precisam abrir conexões/transações de forma isolada ou em conjunto. Nesse caso é necessário implementar um mecanismo de controle auxiliar para saber se a conexão ou transação já foi aberta.

### Controle automático de conexões e transações

O controle automático pode ser feito utilizando os sufixos reservados:

- **`Conectado`**: abre uma conexão se já não estiver aberta; e
- **`Controlado`**: abre uma conexão e uma transação se já não estiverem abertas.

A chamada entre métodos é transparente mantendo o escopo da conexão ou transação. Para utilizar esse mecanismo deve:

1\) criar uma classe filha de `InfraRN`;

2\) implementar o método `inicializarObjInfraIBanco` retornado a instância do banco de dados;

3\) criar um método `protected` com o sufixo Conectado ou Controlado;

4\) esse método não aceita múltiplos parâmetros, então deve ser utilizado um objeto DTO ou um array encapsulador.

Utilizando esse mecanismo após a primeira chamada a um método `Conectado` ou `Controlado` a conexão ficará aberta até o final da execução do script. Transações vão respeitar o mesmo escopo do método, sendo confirmadas no final da execução do método ou canceladas caso uma exceção seja lançada.

```php
class MdAbcTesteRN extends InfraRN {

  protected function inicializarObjInfraIBanco(){
    return BancoSEI::getInstance();
  }

  protected function processarXXXXXControlado($arrParametros){
    try{
      //executa comandos
    }catch(Exception $e){
      throw new InfraException('Erro processando operação XXXXX no módulo ABC.',$e);
    }
  }
}
```

Atenção para o uso desses sufixos em construções como a exemplificada abaixo, pois isso pode causar inconsistências em caso de erro e também problemas de desempenho:

```php
protected function processarTudoConectado(){ //abre apenas conexão

  $arr = $this->buscarItensBanco();

  foreach($arr as $itens){
    $this->processarXXXXX($itens);
    //abre e fecha uma transação PARA CADA elemento do array
  }
}
```

No exemplo acima, se houver erro durante o processamento, parte dos itens pode já ter sido gravada no banco, comprometendo a consistência da operação como um todo. Nesses casos, deve-se analisar se o método **processarTudo** deveria ser **Controlado**, de forma a garantir uma única transação para todo o processamento. Além disso, as **transações devem proteger exclusivamente a persistência principal dos dados.**

Ainda, não se deve colocar dentro da transação ações que não sejam necessárias para salvar os dados no banco. Por exemplo: envio de e-mail, chamada para outro sistema, processamento demorado ou tarefas auxiliares. Sempre que der, essas ações devem acontecer **apenas depois que a transação principal terminar** com sucesso.

### Transações de informações utilizando a operação GerarProcedimento

Quando for executar uma transação de inserção utilizando a operação **GerarProcedimento** da API, é necessário organizar o método para separar responsabilidades.

No exemplo abaixo, a função originalmente marcada como **Controlado** deve atuar apenas como orquestradora do fluxo, enquanto a lógica de persistência em banco deve constar em um método interno (gerarProcedimentoInterno no depois do exemplo abaixo). O envio de e-mails não deve ocorrer dentro da transação. Igualmente, a indexação do Solr deve ser acumulada durante a transação e executada apenas após sua finalização.

Essa abordagem evita gargalos, reduz o tempo de lock no banco e melhora a performance geral da operação.

**Código de exemplo - antes:**

```php
protected function gerarProcedimentoControlado($arrParametros)
{
  // gerarProcedimento + envio de e-mails + indexação Solr
}
```
**Código de exemplo - depois**, com separação entre persistência e efeitos colaterais:

```php
protected function gerarProcedimentoControlado($arrParametros)
{
  // Acumula indexações do Solr durante a transação
  FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(true);

  // Executa apenas a persistência em banco
  $retorno = $this->gerarProcedimentoInterno($arrParametros);

  // Executa indexação após a transação
  FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(false);
  FeedSEIProtocolos::getInstance()->indexarFeeds();

  // Executa envio de e-mails fora da transação
  try {
    $rn = new MdPetEmailNotificacaoRN();
    $rn->notificaoPeticionamentoExterno($retorno['parametrosEmail']);
  } catch (Exception $e) {}

  return $retorno['parametrosRecibo'];
}

protected function gerarProcedimentoInterno($arrParametros)
{
  // Apenas operações de banco
}
```

## Andamentos

Os andamentos representam os registros exibidos no histórico dos processos. Os andamentos podem ter variáveis que serão substituídas por atributos informados no momento do lançamento. Cada andamento está associado com um registro de tarefa que indica o tipo do andamento.

Tarefas com identificador menor que 1000 são reservadas do core do SEI.

A única tarefa reservada do core do SEI que um módulo pode lançar é a de ID_TAREFA=65, que representa uma atualização do andamento com texto livre (nesse caso, informar um atributo com NOME='DESCRICAO' e VALOR='texto do andamento').

Tarefas de módulos podem ser cadastradas com o comando abaixo:

```sql
INSERT INTO tarefa (
       id_tarefa,
       nome,
       sin_historico_resumido,
       sin_historico_completo,
       sin_lancar_andamento_fechado,
       sin_permite_processo_fechado,
       sin_fechar_andamentos_abertos,
       id_tarefa_modulo)
VALUES (
       ' . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ',
       'Audiência agendada no prédio @PREDIO@ (sala @SALA@)',
       'S',
       'S',
       'N',
       'S',
       'S',
       'MD_ABC_AUDIENCIA_REALIZADA')/
```

Onde:

- **id_tarefa**

Deve ser maior ou igual a 1000. Se a inserção for realizada sem a chamada ao método `getValorSequencia('seq_tarefa')`, então é necessário buscar o maior ID da tabela de tarefas:

```sql
select max(id_tarefa)+1 from tarefa
```

Se o valor retornado for maior ou igual a 1000, utilizar o valor retornado. Caso contrário, utilizar 1000. Depois precisa atualizar a sequência `seq_tarefa` para retornar à ordem padrão:

\- MySQL:

```sql
alter table seq_tarefa AUTO_INCREMENT = [último valor utilizado]
```

\- SQL Server:

```sql
DBCC CHECKIDENT ('seq_tarefa', RESEED, [último valor utilizado])
```

\- Oracle:

```sql
drop sequence seq_tarefa;
CREATE SEQUENCE seq_tarefa START WITH [último valor utilizado] INCREMENT BY 1
NOCACHE NOCYCLE
```

\- PostgreSQL:

```sql
CREATE SEQUENCE seq_tarefa INCREMENT BY 1 START WITH [último valor utilizado]
```

- `nome`

Representa o texto que será exibido no andamento. É possível utilizar variáveis no texto, que devem ter o valor informado por meio de **atributos** ao lançar o andamento. Para o texto `Audiência agendada no prédio @PREDIO@ (sala @SALA@)` é necessário informar o valor das variáveis `@PREDIO@` e `@SALA@`.

Exemplo:

```php
$objEntradaLancarAndamentoAPI = new EntradaLancarAndamentoAPI();
$objEntradaLancarAndamentoAPI->setIdProcedimento(10000000012057);
$objEntradaLancarAndamentoAPI->setIdTarefaModulo('MD_ABC_AUDIENCIA_REALIZADA');

$arrObjAtributoAndamentoAPI = array();

$objAtributoAndamentoAPI = new AtributoAndamentoAPI();
$objAtributoAndamentoAPI->setNome('PREDIO');
$objAtributoAndamentoAPI->setValor('101');
$objAtributoAndamentoAPI->setIdOrigem(54); //ID do prédio, pode ser null
$arrObjAtributoAndamentoAPI[] = $objAtributoAndamentoAPI;

$objAtributoAndamentoAPI = new AtributoAndamentoAPI();
$objAtributoAndamentoAPI->setNome('SALA');
$objAtributoAndamentoAPI->setValor('3A');
$objAtributoAndamentoAPI->setIdOrigem(9334); //ID da sala, pode ser null
$arrObjAtributoAndamentoAPI[] = $objAtributoAndamentoAPI;

$objEntradaLancarAndamentoAPI->setAtributos($arrObjAtributoAndamentoAPI);

$objSeiRN = new SeiRN();

$objSeiRN->lancarAndamento($objEntradaLancarAndamentoAPI);
```

Algumas variáveis de andamento são reservadas do sistema, mas podem ser utilizadas pelos módulos desde que as informações sejam devidamente preenchidas nos atributos:

| Nome | Valor | IdOrigem | Observação |
|---|---|---|---|
| DOCUMENTO | Número do documento | ID do documento | Gera link para o documento |
| DOCUMENTOS | Null | null | Será substituída pelos links de todos os documentos informados nos atributos DOCUMENTO associados ao andamento, separados por vírgula (agrupador) |
| NIVEL_ACESSO | null | 0 = Público<br>1 = Restrito<br>2 = Sigiloso |  |
| GRAU_SIGILO | null | U = Ultrassecreto<br>S = Secreto<br>R = Reservado |  |
| HIPOTESE_LEGAL | null | ID da hipótese legal |  |
| VISUALIZACAO |  | I = Integral<br>P = Parcial<br>N = Nenhum | Liberação de acesso externo |
| DATA_AUTUACAO | Data no formato dd/mm/aaaa | Null |  |
| TIPO_CONFERENCIA | null | ID do tipo de conferência |  |
| PROCESSO | Número do processo | ID do processo | Gera link para o processo |
| USUARIO | `[sigla]¥[Nome]` | ID do usuário |  |
| USUARIOS | Null | null | Será substituída por todos os atributos USUARIO associados ao andamento, separados por vírgula (agrupador) |
| UNIDADE | `[sigla]¥[Descrição]` | ID da unidade |  |
| ORGAO | `[sigla]¥[Descrição]` | ID do órgão |  |
| BLOCO | ID do bloco | ID do bloco |  |
| DATA_HORA | Data/hora no formato dd/mm/aaaa H:M:S | ID da atividade | Processos sigilosos |
| USUARIO_ANULACAO | `[sigla]¥[nome]` | ID da atividade | Processos sigilosos |
| INTERESSADO | `[sigla]¥[nome]` | ID do participante |  |
| LOCALIZADOR | Identificação do localizador | ID do localizador |  |
| ANEXO | Nome do anexo | ID do anexo |  |

- **`sin_historico_resumido`**

S/N -- Indica se o andamento será exibido no histórico resumido.

- **`sin_historico_completo`**

S/N -- Indica se o andamento será exibido no histórico completo.

- **`sin_lancar_andamento_fechado`**

S/N -- Indica se o andamento deverá ser lançado como aberto ou concluído. Andamento aberto aparece em amarelo na consulta do histórico, informando a última atividade realizada na unidade. Se o módulo tentar lançar um andamento aberto em processo concluído na unidade o sistema lançará um erro Processo X não possui andamento aberto na unidade Y. Para evitar esse erro ver configuração do sinalizador sin_permite_processo_fechado. Mas é importante verificar se não existe uma falha na lógica do módulo, pois talvez seja necessário reabrir o processo automaticamente ao invés de permitir o lançamento concluído. Se o processo estiver concluído e o andamento for lançado como concluído então ninguém na unidade perceberá que ocorreu alteração no histórico.

- **`sin_permite_processo_fechado`**

S/N -- Indica se permite lançar o andamento em processo concluído na unidade. Se o módulo tentar lançar um andamento aberto e o processo estiver concluído na unidade, então poderá lançar automaticamente como andamento concluído.

- **`sin_fechar_andamentos_abertos`**

S/N -- Indica se os registros de andamento em aberto na unidade devem ser concluídos. Se o processo estará aberto na unidade na hora do lançamento então utilizar o valor S. Dessa forma apenas o novo andamento ficará em amarelo no histórico de processo indicando a última atividade.

- **`id_tarefa_modulo`**

Identificador da tarefa para o módulo com até 50 caracteres maiúsculos. Utilizar o prefixo ``MD_<instituição/módulo>``. Possibilita lançar/consultar andamentos do módulo sem a necessidade de conhecer o ID interno da tarefa, que pode ser diferente em outra instalação. Não devem existir valores duplicados para esse campo. Exemplo: MD_ABC_AUDIENCIA_REALIZADA

## Classes do Sistema

### SessaoSEI

Fornece acesso aos dados da sessão do usuário no SEI. Os atributos configurados pelo módulo podem ser consultados por meio do menu **Infra/Atributos de Sessão** (necessária permissão no perfil Informática). Essa classe implementa o padrão de projeto `Singleton`, então na programação sempre deve acessar o objeto por meio do método estático `getInstance()`.

- Não é recomendado acessar diretamente o array `$_SESSION` do PHP.

Métodos de informações disponíveis na classe do sistema `SessaoSEI`:

| Método | Descrição |
|---|---|
| getNumIdUsuario() | ID do usuário no SIP |
| getStrIdOrigemUsuario() | ID Origem associado com o usuário no SIP |
| getStrSiglaUsuario() | Sigla do Usuário |
| getStrNomeUsuario() | Nome do Usuário |
| getNumIdOrgaoUsuario() | ID do órgão do usuário |
| getStrSiglaOrgaoUsuario() | Sigla do órgão do usuário |
| getStrDescricaoOrgaoUsuario() | Descrição do órgão do usuário |
| getNumIdUnidadeAtual() | ID da unidade atual de trabalho |
| getStrIdOrigemUnidadeAtual() | ID Origem associado com a unidade atual de trabalho no SIP |
| getStrSiglaUnidadeAtual() | Sigla da unidade atual de trabalho |
| getStrDescricaoUnidadeAtual() | Descrição da unidade atual de trabalho |
| getNumIdOrgaoUnidadeAtual() | ID do órgão da unidade atual de trabalho |
| getStrSiglaOrgaoUnidadeAtual() | Sigla do órgão da unidade atual de trabalho |
| getStrDescricaoOrgaoUnidadeAtual() | Descrição do órgão da unidade atual de trabalho |

Outros métodos disponíveis na classe do sistema SessaoSEI:

- **`assinarLink($strLink)`**

Assina um link associado com a sessão do usuário, evitando alteração nos parâmetros. Se ocorrer alteração nos parâmetros um erro de hash inválido será lançado, redirecionando o usuário para a tela de login.

```php
$strLinkAssinado = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=...');
```

- **`validarLink($strLink=null)`**

Valida assinatura do link e se não for válido automaticamente lança um erro de `Hash inválido` e redireciona o usuário para a tela de login. Se o parâmetro não for informado então irá validar o link da página atual. É utilizado normalmente na entrada de páginas, garantindo que o usuário acessou a tela por um link válido.

```php
SessaoSEI::getInstance()->validarLink();
```

- **`verificarLink($strLink=null)`**

Realiza o mesmo comportamento do método **`validarLink`** acima, retornando true/false ao invés de lançar um erro e redirecionar para o login.

- **`validarPermissao($strNomeRecurso)`**

Verifica se o usuário tem acesso ao recurso informado. Se o usuário não tiver acesso ao recurso será lançado o erro Acesso negado a este recurso nesta unidade. Utilizado normalmente na entrada de páginas para validar se o usuário tem acesso ao recurso apontando pelo parâmetro acao da URL.

```php
SessaoSEI::getInstance()->validarPermissao($_GET['acao']);
```

- **`verificarPermissao($strNomeRecurso)`**

Realiza o mesmo comportamento do método **`validarPermissao`** acima, retornando true/false ao invés de lançar um erro. Utilizado para montar componentes na interface, como botões e ícones, e para validar a permissão nos métodos das classes de Regra de Negócio.

```php
if (SessaoSEI::getInstance()->verificarPermissao('md_abc_andamento_lancar'))
{
  //monta botão correspondente
}
```

- **`setAtributo($strNome, $strValor)`**

Configura um atributo na sessão do usuário. Para evitar nomes duplicados utilizar o prefixo ``MD_<instituição/módulo>`` no nome do atributo.

```php
SessaoSEI::getInstance()->setAtributo('MD_ABC_ATRIBUTO_SESSAO',$strValor);
```

- **`getAtributo($strNome)`**

Recupera um atributo da sessão do usuário.

```php
$strValor = SessaoSEI::getInstance()->getAtributo('MD_ABC_ATRIBUTO_SESSAO');
```

- **`isSetAtributo($strNome)`**

Verifica se um atributo consta na sessão do usuário, retornando true/false.

```php
if
(SessaoSEI::getInstance()->isSetAtributo('MD_ABC_ATRIBUTO_SESSAO')){
}
```

- **`removerAtributo($strNome)`**

Remove um atributo da sessão do usuário.

```php
SessaoSEI::getInstance()->removerAtributo('MD_ABC_ATRIBUTO_SESSAO');
```

### CacheSEI

Fornece acesso ao servidor de cache em memória (**memcache**). Os atributos podem ser consultados por meio do menu **Infra/Cache em Memória**, sendo necessária permissão no perfil `Informática`. Essa classe implementa o padrão de projeto **`Singleton`**, então na programação sempre deve acessar o objeto por meio do método estático `getInstance()`.

Métodos disponíveis na classe do sistema `CacheSEI`:

- **`setAtributo($strChave, $strValor, $numTempo)`**

Adiciona um atributo no servidor memcache, onde:

| $strChave | Nome do atributo, utilizando com o prefixo `MD_<instituição/módulo>` para evitar nomes duplicados. |
|---|---|
| $strValor | Valor do atributo diferente de nulo. |
| $numTempo | Tempo que o atributo deve ficar na cache. Utilizar CacheSEI::getInstance()->getNumTempo() para obter o valor configurado na chave CacheSEI/Tempo do arquivo ConfiguracaoSEI.php (se a chave não for definida no arquivo de configuração, então será retornado o valor padrão do sistema 3600 = 1 hora). |

```php
CacheSEI::getInstance()->setAtributo('MD_ABC_ATRIBUTO_MEMCACHE', $strValor, CacheSEI::getInstance()->getNumTempo());
```

- **`getAtributo($strChave)`**

Recupera um atributo no servidor memcache, retornando nulo se não encontrar.

```php
$strValor =
CacheSEI::getInstance()->getAtributo('MD_ABC_ATRIBUTO_MEMCACHE');
```

### InfraParametro

Permite ler/gravar parâmetros na tabela `infra_parametro` (menu **Infra/Parâmetros**). Ao criar o objeto deve ser passada a instância do banco de dados:

```php
$objInfraParametro = new InfraParametro(BancoSEI::getInstance());
```

Métodos disponíveis na classe do sistema InfraParametro:

- **`setValor($strNome, $strValor)`**

Configura o valor de um parâmetro. Se o parâmetro não existir será criado e se já existir será atualizado. Para evitar nomes duplicados deve utilizar o prefixo `MD_<instituição/módulo>`.

```php
$objInfraParametro->setValor('MD_ABC_ID_SERIE_TESTE', '601');
```

- **`getValor($strNome, $bolErroNaoEncontrado=true)`**

Retorna o valor de um parâmetro ou nulo se não encontrar. O segundo parâmetro do método é opcional e indica se deve ser lançado um erro caso o parâmetro não exista na tabela.

```php
$numIdSerieAbc = $objInfraParametro->getValor('MD_ABC_ID_SERIE_TESTE');
```

- **`isSetValor($strNome)`**

Verifica se um parâmetro existe na tabela retornando true/false. O valor do parâmetro não é analisado, ou seja, ele pode existir, mas estar vazio.

```php
if ($objInfraParametro->isSetValor('MD_ABC_ID_SERIE_TESTE')){

}
```

- **`listarValores($arrNomes, $bolErroNaoEncontrado=true)`**

Retorna conjunto de parâmetros informados no array de entrada. O segundo parâmetro do método é opcional e indica se deve ser lançado um erro caso algum parâmetro não exista na tabela. O array de retorno é indexado pelo nomes dos parâmetros.

```php
$arrSeries = $objInfraParametro->listarValores(array('MD_ABC_PAR1', 'MD_ABC_PAR2'));
```

### LogSEI

Permite gravar registros na tabela `infra_log` (menu **Infra/Log**). Essa classe implementa o padrão de projeto `Singleton`, então na programação sempre deve acessar o objeto por meio do método estático `getInstance()`.

Métodos disponíveis na classe do sistema `LogSEI`:

- **`gravar($strTexto, $strStaTipo='E')`**

Grava o texto informado na tabela `infra_log` (não pode ser vazio). O segundo parâmetro é opcional e indica o tipo do registro de log. Utilizar uma das constantes abaixo:

- InfraLog::$ERRO (default)
- InfraLog::$AVISO
- InfraLog::$INFORMACAO
- InfraLog::$DEBUG

```php
LogSEI::getInstance()->gravar('abc teste log',InfraLog::$INFORMACAO);
```

### InfraDebug

Permite ler/gravar informações de debug, armazenando os registros na sessão, sendo assim mantidos entre chamadas do sistema. Essa classe implementa o padrão de projeto `Singleton`, então na programação sempre deve acessar o objeto por meio do método estático `getInstance()`.

Utilizando o `InfraPHP` para realizar debug nas telas do sistema deve configurar no início da execução as opções desejadas:

```php
InfraDebug::getInstance()->setBolLigado(true);
InfraDebug::getInstance()->setBolDebugInfra(true);
InfraDebug::getInstance()->limpar();
```

No final deve retirar o comentário do método que monta a área de debug para visualização:

```php
PaginaSEI::getInstance()->montarAreaDebug();
```

**Atenção**: não pode esquecer de desligar o debug após sua utilização, pois poderá comprometer o desempenho e a segurança do sistema.

Métodos disponíveis na classe do sistema `InfraDebug`:

- **`gravar($strTexto)`**

Grava um registro de debug na sessão.

```php
InfraDebug::getInstance()->gravar('Valor encontrado: '.$n);
```

- **`limpar()`**

Remove todos os registros que foram gravados no debug.

```php
InfraDebug::getInstance()->limpar();
```

- **`getStrDebug()`**

Recupera todos os registros que foram gravados no debug.

```php
$strDebug = InfraDebug::getInstance()->getStrDebug();
```

- **`setBolLigado($bolLigado)`**

Recebe true/false indicando se as chamadas ao método gravar devem ser processadas ou ignoradas.

```php
InfraDebug::getInstance()->setBolLigado(true);
```

- **`setBolDebugInfra($bolDebugInfra)`**

Recebe true/false indicando se deve registrar textos de debug gerados automaticamente pelo **`InfraPHP`** contendo, por exemplo, os SQLs executados.

```php
InfraDebug::getInstance()->setBolDebugInfra(true);
```

- **`setBolEcho($bolEcho)`**

Recebe true/false indicando se na chamada do método `gravar` deve ser feito um `echo` automaticamente do conteúdo.

```php
InfraDebug::getInstance()->setBolEcho(true);
```

### ConfiguracaoSEI

Permite ler informações do arquivo de configurações do sistema `ConfiguracaoSEI.php`. Essa classe implementa o padrão de projeto **`Singleton`**, então na programação sempre deve acessar o objeto por meio do método estático `getInstance()`.

- **`getValor($strGrupo, $strChave=null, $bolErroNaoEncontrado=true, $strValorPadrao=null)`**

Recupera o valor associado com a chave no arquivo de configuração, onde:

| $strGrupo | Nome do grupo com o prefixo `MD_<instituição/módulo>` para evitar nomes duplicados. |
|---|---|
| $strChave | Opcional. Nome da chave dentro do grupo. |
| bolErroNaoEncontrado | Opcional (valor padrão true). Indica se deve ser lançado um erro caso a configuração não exista. |
| strValorPadrao | Opcional. Informa o valor padrão para retorno se a configuração não existir. |

```php
$strServidor = ConfiguracaoSEI::getInstance()->getValor('MD_ABC_Banco','Servidor');
```

- **`isSetValor($strGrupo, $strChave)`**

Retorna true/false indicando se uma configuração existe no arquivo de configuração. O valor da configuração não é analisado, ou seja, ela pode existir, mas estar vazia.

```php
if
(ConfiguracaoSEI::getInstance()->isSetValor('MD_ABC_Banco','Servidor')){

}
```

### BancoSEI

Fornece acesso ao banco de dados. Essa classe implementa o padrão de projeto Singleton, então na programação sempre deve acessar o objeto por meio do método estático getInstance().

- **`abrirConexao()`**

Abre conexão com o banco de dados.

```php
BancoSEI::getInstance()->abrirConexao();
```

- **`fecharConexao()`**

Fecha conexão com o banco de dados.

```php
BancoSEI::getInstance()->fecharConexao();
```

- **`getIdConexao()`**

Retorna um identificador da conexão ou nulo. Esse identificador não representa um recurso de conexão do PHP, ou seja, não pode ser utilizado em chamadas diretas da extensão do banco de dados utilizado. Por **questões de segurança** o recurso de conexão é privado e controlado pela classe de banco de dados do framework `InfraPHP`.

```php
If (BancoSEI::getInstance()->getIdConexao()==null){
  BancoSEI::getInstance()->abrirConexao();
}
```

- **`abrirTransacao()`**

Inicia uma transação.

```php
BancoSEI::getInstance()->abrirTransacao();
```

- **`confirmarTransacao()`**

Confirma uma transação (commit).

```php
BancoSEI::getInstance()->confirmarTransacao();
```

- **`cancelarTransacao()`**

Cancela uma transação (rollback).

```php
BancoSEI::getInstance()->cancelarTransacao();
```

- **`consultarSql($strSql)`**

Executa no banco de dados a consulta SQL recebida, retornando um array com os registros retornados.

```php
$rs = BancoSEI::getInstance()->consultarSql('select nome, valor
from infra_parametro where nome like \'SEI_%\' order by nome asc');

Array
(
  [0] => Array
    (
      [nome] => SEI_HABILITAR_AUTENTICACAO_DOCUMENTO_EXTERNO
      [valor] => 2
    )
  [1] => Array
    (
      [nome] => SEI_HABILITAR_GRAU_SIGILO
      [valor] => 1
    )
  [2] => Array
    (
      [nome] => SEI_HABILITAR_HIPOTESE_LEGAL
      [valor] => 1
    )
  ...
)
```

- **`executarSql($strSql, $arrCamposBind=null)`**

Executa no banco de dados o comando SQL recebido, retornando o número de registros afetados. O parâmetro $arrCamposBind é utilizado apenas em bases de dados Oracle, sendo um array indexado pelos nomes dos campos CLOB para bind.

```php
BancoSEI::getInstance()->executarSql('update infra_parametro set
valor =\'2\' where nome=\'SEI_HABILITAR_HIPOTESE_LEGAL\'');
```

### InfraErroPHP

No PHP 8 várias situações que antes geravam apenas Notices passaram a gerar Warnings. Por exemplo, ao acessar uma posição de array que ainda não existe. Isso provocará um erro no sistema que antes não acontecia.

A classe `InfraErroPHP` trata essas situações, permitindo controlar o que o sistema deve fazer (ignorar, registrar em uma tabela ou lançar uma exceção).

Constantes de erro:

```php
InfraErroPHP::$W_UNDEFINED_ARRAY_KEY
InfraErroPHP::$W_UNDEFINED_VARIABLE
InfraErroPHP::$W_UNDEFINED_PROPERTY
InfraErroPHP::$W_ATTEMPT_TO_READ_PROPERTY
InfraErroPHP::$W_TRYING_TO_ACCESS_ARRAY_OFFSET
InfraErroPHP::$W_ARRAY_TO_STRING_CONVERSION
InfraErroPHP::$W_RESOURCE_USED_AS_OFFSET_CASTING_TO_INTEGER
InfraErroPHP::$W_STRING_OFFSET_CAST_OCCURRED
InfraErroPHP::$W_UNINITIALIZED_STRING_OFFSET
InfraErroPHP::$W_CANNOT_ACCESS_OFFSET_OF_TYPE_STRING_ON_STRING
InfraErroPHP::$W_ARGUMENT_MUST_BE_PASSED_BY_REFERENCE
InfraErroPHP::$W_A_NON_NUMERIC_VALUE_ENCOUNTERED
```

Constantes de tratamento:

```php
InfraErroPHP::$T_LANCAR_EXCECAO
InfraErroPHP::$T_IGNORAR
InfraErroPHP::$T_REGISTRAR
InfraErroPHP::$T_CONTABILIZAR
```

Por padrão, o SEI ignora os erros `$W_UNDEFINED_ARRAY_KEY`, `$W_UNDEFINED_VARIABLE`, `$W_UNDEFINED_PROPERTY` e `$W_TRYING_TO_ACCESS_ARRAY_OFFSET`. Os demais passarão a lançar erros.

É possível sobrescrever esse comportamento no ambiente de desenvolvimento, adicionando a chave `InfraErroPHP` no arquivo `ConfiguracaoSEI.php`. Exemplo:

```php
'InfraErroPHP' =>
  array(
    InfraErroPHP::$W_UNDEFINED_PROPERTY => InfraErroPHP::$T_REGISTRAR,
    InfraErroPHP::$W_STRING_OFFSET_CAST_OCCURRED => InfraErroPHP::$T_IGNORAR
  ),
```

Quando o tratamento `InfraErroPHP::$T_REGISTRAR` for utilizado, o erro será gravado na tabela `infra_erro_php` e poderá ser consultado por meio do menu **Infra/Erros do PHP**. O erro é gravado apenas uma vez, desde que não ocorra alteração nas linhas de código (gerando novo registro). O tratamento `InfraErroPHP::$T_CONTABILIZAR` possui comportamento semelhante ao de registro, mas contabilizando a quantidade de vezes que o erro ocorreu. Por enquanto, ainda é possível esse tipo de tratamento, mas as versões futuras do PHP prometem gerar erros para essas situações.
