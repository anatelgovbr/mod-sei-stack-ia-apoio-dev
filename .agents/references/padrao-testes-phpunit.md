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

- Banco e sessão: `BancoSEIFake` e `SessaoSEIFake`, que a `BaseTest` coloca no lugar dos reais antes de cada teste.
- Outra dependência que só fornece dados ao código testado: `createStub`.
- `createMock` com `expects` fica para o teste que verifica uma chamada que o código faz para fora, como um envio. Nos demais casos, verifique o resultado.

## Fakes e helpers

- `$this->objBanco` (`BancoSEIFake`): `responder('/ FROM nome_da_tabela /', [[...]])` devolve as linhas para a consulta cujo SQL casa com a expressão regular, com a chave de cada coluna igual ao nome do atributo do DTO em minúsculas, como `iditemetapa`. `afetarLinhas(...)` define quantas linhas cada comando seguinte afeta, e `falharCom($objExcecao)` faz toda consulta e todo comando seguinte lançarem a exceção. O fake registra `arrConsultas`, `arrComandos`, `arrSequencias` e `arrTransacoes`.
- `$this->objSessao` (`SessaoSEIFake`): usuário logado com todas as permissões, menos as negadas com `negarPermissao('md_xxx_recurso')`. Registra cada recurso validado em `arrRecursosValidados`.
- `BancoHelper`: `lerComando($this->objBanco->arrComandos[0])` devolve a tabela, as colunas gravadas e o filtro de um INSERT, UPDATE ou DELETE; `listarComandos()` e `listarConsultas()` devolvem o SQL na ordem; `listarValoresLigados($arrRegistro)` devolve os valores ligados.
- `ValidacaoHelper`: `capturarInfraException(fn() => ...)` devolve a `InfraException` lançada e falha o teste se nada for lançado; `listarValidacoes($e)` devolve as mensagens de validação, na ordem.
- `PropriedadeEstaticaHelper`: `definirEstatico` e `lerEstatico` alteram e leem uma propriedade estática, mesmo privada.

## Requisito e defeito conhecido

- O comentário do teste cita o ID do requisito do módulo que ele verifica, como `RF-APT-008`, quando houver.
- Teste que mostra um defeito real ainda sem correção recebe `#[Group('defeito-conhecido')]`: fica fora da execução padrão e roda com `--group defeito-conhecido`. Com o defeito corrigido, o atributo sai.

## Fora do teste unitário

- Páginas (`*_lista.php`, `*_cadastro.php`), JavaScript do módulo e caminhos que dependem de dados reais do núcleo, como documento com acesso da unidade e versões do editor, ficam para o teste e2e ou para o teste manual.

## Independência e determinismo

- Cada teste monta o próprio cenário e passa sozinho, com `--filter`, ou em qualquer ordem.
- Estado estático alterado no teste volta ao valor inicial no `tearDown`, como em `MdAptIntegracaoTest`.
- O teste dá o mesmo resultado em qualquer dia, hora e máquina, sem depender de dado aleatório ou de rede.

## Configuração por atributo

- Configure o teste com os atributos do PHPUnit 11: `#[DataProvider]`, `#[Group]`, `#[CoversClass]`.
- Código que pode causar erro fatal ao ser carregado, como o integrador de um módulo, roda com `#[RunInSeparateProcess]` e `#[PreserveGlobalState(false)]`, como em `SmokeTest`.
