# Ambiente do Modulo SEI

Limites de ambiente que o modulo precisa respeitar.

## Upload de arquivo

| Item | Valor de referencia | Observacao |
|---|---|---|
| `upload_max_filesize` no PHP | 200M | Limite de tamanho de um arquivo enviado |
| `post_max_size` no PHP | ligeiramente maior que `upload_max_filesize` | Se for igual ou menor, o upload no limite falha, porque o POST carrega o arquivo mais os demais campos |
| `SEI_TAM_MB_DOC_EXTERNO` no SEI | conforme a instalacao | Parametro do SEI que limita o documento externo em megabytes |

O modulo mantem **coerencia com o `SEI_TAM_MB_DOC_EXTERNO`** configurado no SEI como um todo. Nao adotar limite proprio maior que o do sistema.

Sintoma tipico da incoerencia: a tela do modulo aceita o arquivo, o servidor rejeita, e o usuario recebe erro sem mensagem util. A validacao do modulo precisa acontecer antes do envio, com o mesmo limite do sistema.

## Como consultar o parametro

```php
$objInfraParametro = new InfraParametro(BancoSEI::getInstance());
$numTamMb = $objInfraParametro->getValor('SEI_TAM_MB_DOC_EXTERNO');
```

Ver `.agents/references/padrao-classes-sistema-sei.md` para o contrato do `InfraParametro`.
