# Classes de Sistema do SEI

Classes utilitarias do core que o modulo consome.

Todas seguem o mesmo cuidado: **chave global exige prefixo do modulo**, senao um modulo sobrescreve o valor de outro na mesma instalacao. O prefixo e `MD_<instituicao/modulo>` no CacheSEI e no ConfiguracaoSEI, e `MODULO_<NOME_DO_MODULO>_` no InfraParametro.

## CacheSEI

Acesso ao servidor de cache em memoria, memcache.

| Item | Regra |
|---|---|
| Nome do atributo | Usar o prefixo `MD_<instituicao/modulo>` para evitar nome duplicado |
| Tempo de expiracao | Usar `CacheSEI::getInstance()->getNumTempo()` para obter o valor configurado, em vez de fixar um numero |
| Acesso | Singleton, por `getInstance()` |

```php
CacheSEI::getInstance()->setAtributo(
    'MD_ABC_LISTA_TIPOS',
    $arrTipos,
    CacheSEI::getInstance()->getNumTempo()
);
```

## InfraParametro

Le e grava parametros na tabela `infra_parametro`, visiveis no menu Infra/Parametros.

| Item | Regra |
|---|---|
| Construcao | Quem chama cria `new InfraParametro(BancoSEI::getInstance())` e passa o objeto por parametro tipado para a funcao que le o parametro (secao "SOLID" de `padrao-codificacao-php.md`) |
| Nome do parametro | Usar o prefixo `MODULO_<NOME_DO_MODULO>_`, como `MODULO_PETICIONAMENTO_`. Diferenca consciente em relacao ao manual (cap. 3), que pede `MD_<instituicao/modulo>`. O parametro de versao do script de release fica `VERSAO_MODULO_<NOME_DO_MODULO>` |
| Gravacao | Se o parametro nao existir sera criado; se existir sera atualizado |
| `getValor($nome)` | Lanca `InfraException` com "Parametro <nome> nao encontrado." quando o parametro nao existe |
| `getValor($nome, false)` | Devolve `null` quando o parametro nao existe |
| Tipo do valor | Texto (`string`) ou `null`: a coluna `valor` e texto e o DTO usa `Str`; a tela Infra/Parametros grava o valor vazio como `null` |

### Tipo do parametro de modulo

| Tipo | Quem controla | Exemplo | Parametro ausente, vazio ou com valor nao aceito |
|---|---|---|---|
| Controle do modulo | Script de instalacao e o proprio modulo | `VERSAO_MODULO_<MODULO>`, ID de serie criado pelo script | Interromper a operacao com `InfraException` que cita o nome do parametro |
| Funcional | O orgao, em Infra/Parametros; o orgao pode deixar sem configurar | `MODULO_PETICIONAMENTO_OCULTA_GERAR_INTIMACAO_ACESSO_INTEGRAL` | Manter o comportamento padrao do modulo |

### Parametro funcional

Cada estado tem comportamento definido no plano e nos requisitos tecnicos do modulo:

| Estado | Comportamento |
|---|---|
| Parametro nao existe no banco | Comportamento padrao |
| Parametro existe com valor vazio (`null`) | Comportamento padrao |
| Valor padrao gravado pelo script (ex.: `0`) | Comportamento padrao |
| Cada valor aceito (ex.: `1`) | Comportamento definido para o valor |
| Valor nao aceito (ex.: `S`, `01`, `2`) | Comportamento padrao e aviso em Infra/Log (`InfraLog::$AVISO`) com o nome do parametro e o valor encontrado |

Implementacao:

- Ler em um metodo por parametro, com retorno tipado, que recebe `InfraParametro` e `LogSEI` por parametro; metodo booleano com nome em portugues, como `deveOcultarAcessoIntegral`.
- Ler com `getValor($nome, false)`.
- Guardar o nome e os valores aceitos em `public const` da RN.
- Comparar o texto com `===` e as constantes.
- Escrever o aviso com o nome, o valor encontrado e o comportamento mantido, sem chamar o valor de invalido.
- No script de release, criar o parametro com o valor padrao so quando ele nao existe (`isSetValor` + `setValor`), com as constantes da RN.
- Documentar os estados so nos requisitos tecnicos do modulo.

Teste:

- Cobrir cada estado no data provider: ausente (`null`), vazio, valor padrao, cada valor aceito e valores nao aceitos.
- Stub: `$this->createStub(InfraParametro::class)` com `willReturnMap([[NOME, false, null, $valor]])`; o stub devolve `null` quando o codigo pede outro nome.
- Log: `LogSEI::gravar` passa pelo `__call` da `InfraRN`; conferir o `INSERT INTO infra_log` no `BancoSEIFake`, com o `LogSEIFake` da `BaseTest`.
- Exemplo: `tests/unit/sei/web/modulos/peticionamento/rn/MdPetIntimacaoRNTest.php`.

## InfraDebug

Le e grava informacoes de debug, armazenando os registros na sessao.

Debug ligado para depurar nao chega a entrega. Conferencia na secao "Debug desligado" de `sei-validacao-padrao`.

## ConfiguracaoSEI

Le informacoes do arquivo de configuracoes do sistema `ConfiguracaoSEI.php`.

| Item | Regra |
|---|---|
| Nome do grupo | Usar o prefixo `MD_<instituicao/modulo>` para evitar nome duplicado |
| Leitura | Permitida pelo modulo |
| Escrita no arquivo | Ver o guardrail de Core no `AGENTS.md`: o agente nao edita por conta propria, e a edicao para registrar o modulo na chave `Modulos` exige autorizacao explicita do desenvolvedor |

## LogSEI

Grava registros na tabela `infra_log`, visiveis no menu Infra/Log. Singleton.

```php
LogSEI::getInstance()->gravar('texto do log', InfraLog::$INFORMACAO);
```

Assinatura: `gravar($strTexto, $strStaTipo = 'E')`. Nunca gravar segredo nem dado pessoal no log.
