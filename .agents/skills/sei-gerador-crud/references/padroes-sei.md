# Padroes SEI Obrigatorios para Saida Gerada

## Paginas

- a pagina deve submeter para ela mesma ou para `controlador.php`

## RN

- instanciar a BD com `$this->getObjInfraIBanco()`

## Busca textual / autocomplete

Nunca usar `LIKE` diretamente sobre colunas textuais principais (nome, e-mail, CPF, CNPJ
ou equivalentes) em consultas de autocomplete.

Se a tabela tiver campo de indexacao textual dedicado (ex.: `str_idx_contato`), consultar
sobre ele usando `InfraString::prepararIndexacao()`:

```php
$valorIndexado = InfraString::prepararIndexacao($valorPesquisa, true);
$objContatoDTO->setStrIdxContato('%' . $valorIndexado . '%', InfraDTO::$OPER_LIKE);
```

- Melhora desempenho, reduz varredura de tabela e normaliza acentos/caixa.
