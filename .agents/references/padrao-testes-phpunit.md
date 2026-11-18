# Padrão de Testes Unitários com PHPUnit

Práticas para teste novo ou alterado em `tests/unit`. Como rodar: seção "Testes" do `README.md` da raiz.

## Ambiente do teste

- No contêiner `qa`, `/testes` é a pasta `tests/` do repositório, e `/opt` é `fontes/sei/src/main/php`, com a `ConfiguracaoSEI.php` de `tests/unit/sei/config` no lugar da configuração da máquina. Essa configuração só carrega os módulos listados nela.
- O teste usa o código do módulo como ele é; o módulo não muda para o teste passar.

## Nome e escopo

- Um comportamento por método de teste. O nome começa com `test` e vem em português: `testRecusaModeloDeOutraUnidade`, `testCadastrarGravaODocumentoValidado`.
- A chave de cada caso do data provider descreve o cenário e completa o nome do teste na saída do PHPUnit: `yield 'modelo de outra unidade' => [...];`.

## Data provider

- Os dados de cada caso são escalares, arrays ou objetos de valor. Test doubles e objetos com dependências são criados no método de teste, a partir dos dados do caso.
- Cada variação de entrada vira um caso do data provider, e o corpo do teste segue reto, sem `if`, laço ou cálculo do valor esperado.
- O valor esperado vem no caso como literal.

## Assertions

- Verifique o efeito do código testado: valor devolvido, SQL registrado pelo test double do banco, permissão validada ou exceção lançada.
- `assertSame` para escalares e arrays; `assertEquals` para objetos comparados por valor.
- Exceção esperada: `expectException` e `expectExceptionMessage` logo antes da ação. Mensagem de validação da InfraPHP: `self::listarValidacoes(self::capturarInfraException(fn() => ...))`, do `ValidacaoHelper`.

## Test doubles

- Banco, sessão e log: `BancoSEIFake`, `SessaoSEIFake` e `LogSEIFake`, que a `BaseTest` coloca no lugar dos reais antes de cada teste.
- Outra dependência que só fornece dados ao código testado: `createStub`.
- `createMock` com `expects` fica para o teste que verifica uma chamada que o código faz para fora, como um envio. Nos demais casos, verifique o resultado.

## Fakes e helpers

- `$this->objBanco` (`BancoSEIFake`): `responder('/ FROM nome_da_tabela /', [[...]])` devolve as linhas para a consulta cujo SQL casa com a expressão regular, com a chave de cada coluna igual ao nome do atributo do DTO em minúsculas, como `iditemetapa`. `afetarLinhas(...)` define quantas linhas cada comando seguinte afeta, e `falharCom($objExcecao)` faz toda consulta e todo comando seguinte lançarem a exceção. O fake registra `arrConsultas`, `arrComandos`, `arrSequencias` e `arrTransacoes`.
- `$this->objSessao` (`SessaoSEIFake`): usuário logado com todas as permissões, menos as negadas com `negarPermissao('md_xxx_recurso')`. Registra cada recurso validado em `arrRecursosValidados` e, em `arrAuditorias`, o recurso, a operação e uma cópia do parâmetro de cada `validarAuditarPermissao`, como estavam nesse momento.
- `BancoHelper`: `lerComando($this->objBanco->arrComandos[0])` devolve a tabela, as colunas gravadas e o filtro de um INSERT, UPDATE ou DELETE; `listarComandos()` e `listarConsultas()` devolvem o SQL na ordem; `listarValoresLigados($arrRegistro)` devolve os valores ligados; `listarApelidosNoSelect($strSql)` e `listarApelidosNoFrom($strSql)` devolvem os apelidos de tabela citados nas colunas do SELECT e os ligados no FROM, para conferir que a consulta não cita tabela fora do FROM.
- `ValidacaoHelper`: `capturarInfraException(fn() => ...)` devolve a `InfraException` lançada e falha o teste se nada for lançado; `listarValidacoes($e)` devolve as mensagens de validação, na ordem.
- `$this->objLog` (`LogSEIFake`): guarda em `arrRastro` as linhas do rastro do Peticionamento, sem passar pelo banco, e deixa as demais linhas seguirem o caminho real do log. `falharCom` faz a gravação do rastro lançar a exceção informada.
- `RastroHelper`: `listarRastro` devolve as linhas do rastro sem o UUID, a hora e a linha do arquivo, que mudam a cada execução; `responderParametrosDeEmail` programa os parâmetros de e-mail do SEI, que o aviso de rollback lê. O envio de e-mail fica desligado na configuração dos testes.
- `PropriedadeEstaticaHelper`: `definirEstatico` e `lerEstatico` alteram e leem uma propriedade estática, mesmo privada.

## Requisito e defeito conhecido

- O comentário do teste cita o ID do requisito do módulo que ele verifica, como `RF-APT-008`, quando houver.
- Teste que mostra um defeito real ainda sem correção recebe `#[Group('defeito-conhecido')]`: fica fora da execução padrão e roda com `--group defeito-conhecido`. Com o defeito corrigido, o atributo sai.

## Fora do teste unitário

- Páginas (`*_lista.php`, `*_cadastro.php`), JavaScript do módulo e caminhos que dependem de dados reais do núcleo, como documento com acesso da unidade e versões do editor, ficam para o teste e2e ou para o teste manual.

## Integração

Comportamento que depende de transação real, do core ou do envio de e-mail, como o desfazimento depois de uma falha, tem teste em `tests/integracao`, com banco e servidor de e-mail reais. Fake de banco não cancela gravação, e por isso não pega recibo ou documento que voltou com a transação cancelada. O teste de falha confere a causa com `lerCausas` e termina com a nova tentativa sem falha.

## Independência e determinismo

- Cada teste monta o próprio cenário e passa sozinho, com `--filter`, ou em qualquer ordem.
- Estado estático alterado no teste volta ao valor inicial no `tearDown`, como em `MdAptIntegracaoTest`.
- O teste dá o mesmo resultado em qualquer dia, hora e máquina, sem depender de dado aleatório ou de rede.

## Configuração por atributo

- Configure o teste com os atributos do PHPUnit 11: `#[DataProvider]`, `#[Group]`, `#[CoversClass]`.
- Código que pode causar erro fatal ao ser carregado, como o integrador de um módulo, roda com `#[RunInSeparateProcess]` e `#[PreserveGlobalState(false)]`, como em `SmokeTest`.
