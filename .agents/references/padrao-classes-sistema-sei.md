# Classes de Sistema do SEI

Classes utilitarias do core que o modulo consome.

Todas seguem o mesmo cuidado: **chave global exige prefixo `MD_<instituicao/modulo>`**, senao um modulo sobrescreve o valor de outro na mesma instalacao.

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
| Construcao | Ao criar o objeto, passar a instancia do banco: `new InfraParametro(BancoSEI::getInstance())` |
| Nome do parametro | Usar o prefixo `MD_<instituicao/modulo>` |
| Gravacao | Se o parametro nao existir sera criado; se existir sera atualizado |

## InfraDebug

Le e grava informacoes de debug, armazenando os registros na sessao.

Nao deixar debug ligado em producao. Ver a regra de `InfraErroPHP` em `sei-testes-validacao`.

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
