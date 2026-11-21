# Metodos Padronizados do CRUD InfraPHP

Contrato dos metodos que a `InfraRN` resolve automaticamente.

O recurso SIP de cada metodo esta em `.agents/references/padrao-auditoria-sip-sei.md`. O contrato transacional esta na regra T8 de `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md`.

## Quadro geral

| Metodo | Entrada | Retorno |
|---|---|---|
| `cadastrar` | DTO da entidade | O proprio DTO, com a chave primaria preenchida |
| `alterar` | DTO da entidade | Nenhum DTO, porque nao ha acrescimo de informacao |
| `excluir` | Lista de DTOs na RN, um DTO por vez na BD | Nada |
| `consultar` | DTO com os filtros | Um DTO ou nulo |
| `bloquear` | DTO com os filtros | Um DTO ou nulo, com o registro em lock |
| `listar` | DTO com retorno, pesquisa e ordenacao | Lista de DTOs |
| `contar` | DTO com os filtros | Numero de ocorrencias |
| `selecionar` | DTO com os filtros | Lista para tela de escolha |

## Regras por metodo

**`cadastrar`**. Se a chave primaria for sequencial ou nativa, o atributo correspondente e configurado com `null` antes de chamar. O framework preenche.

**`alterar`**. Nao devolve DTO. Esperar retorno desse metodo e erro de contrato.

**`consultar`**. Se mais de uma ocorrencia atender aos filtros, e gerado erro. Consultar e para registro unico; para varios, usar `listar`.

**`bloquear`**. Alem de devolver o registro, mantem **lock ate o fim da transacao corrente**. So faz sentido dentro de um metodo `Controlado`. Usar fora de transacao segura o lock por tempo indeterminado.

**`listar`**. Enviar um DTO com os atributos de retorno preenchidos por `ret`, os de pesquisa por `set` e os de ordenacao por `setOrd`.

**`contar`**. Devolve o numero de ocorrencias que atenderam aos criterios, sem trazer os registros.

**`excluir`**. Assimetria proposital entre camadas: o metodo da RN recebe uma lista de DTOs, e o metodo da BD recebe um DTO especifico. A RN percorre a lista.

**`selecionar`**. Usado em telas de escolha de registro, as lupas. Tem recurso SIP proprio, `_selecionar`, que nunca entra na regra de auditoria.

## Geracao dos recursos no SIP

No SIP, pelo menu **Recursos / Gerar Padrao PHP**, e possivel gerar automaticamente os recursos correspondentes a esses metodos, em vez de cadastrar um a um.

## Coluna derivada para busca textual

**Adoção.** Reutilize a busca da entidade quando já atender ao caso. Em entidade própria, adote `idx_<entidade>` quando o requisito pedir busca por trechos ou termos sobre texto normalizado de um ou mais campos. Para igualdade e identificadores exatos, filtre pelos atributos de origem.

**Modelagem.** Defina os campos de origem e a representação pesquisável de cada um, como números com e sem máscara quando o requisito pedir ambos. Modele a coluna textual com `InfraMetaBD::tipoTextoVariavel(n)` no script aplicável e mapeie-a no DTO como `Idx<Entidade>` com `InfraDTO::$PREFIXO_STR`. Defina tamanho, tratamento de estouro e nulabilidade em função dos dados normalizados e dos bancos suportados. A coluna guarda texto derivado preenchido pelo servidor. Reserve os campos de origem para entrada e exibição. O prefixo `idx_` nomeia a coluna, sem exigir índice físico. Avalie o desempenho de `LIKE '%termo%'` com o volume e os filtros esperados.

**Gravação.** A RN compõe o texto com `InfraString::prepararIndexacao` e grava o valor derivado na mesma transação do cadastro ou da alteração dos campos de origem. Em alteração parcial, recomponha o texto a partir do estado completo, como faz `montarIndexacaoControlado` ao reler a linha. Cubra também os demais caminhos de escrita que alterem esses campos. Em base existente, preencha os registros em lotes repetíveis, com a mesma regra de composição, antes de usar a coluna como critério de busca. A atualização da coluna é persistência no banco. A indexação externa segue a [regra T6](../skills/sei-verificacao-rn/references/padroes-transacao.md#t6---efeitos-externos-somente-apos-o-retorno-transacional).

**Consulta.** Em busca por termos, passe o atributo de entrada e o destino no DTO a `InfraString::prepararPesquisaDTO`, por exemplo `prepararPesquisaDTO($objDTO, 'PalavrasPesquisa', 'IdxEntidade')`. A função monta `OPER_LIKE` para cada termo e combina vários termos com `AND`. Para localizar um trecho contínuo, normalize o texto e aplique um único `OPER_LIKE` no destino, como no exemplo abaixo. Use os critérios do DTO para que a `InfraBD` delegue a formatação do SQL ao adaptador de banco. Preserve os filtros de escopo e permissão do fluxo. Defina a semântica de pontuação e curingas e trate a entrada que ficar vazia após a normalização antes de consultar, para evitar busca ampla acidental.

O core exemplifica a composição do texto em `fontes/sei/src/main/php/sei/web/rn/ContatoRN.php`, `fontes/sei/src/main/php/sei/web/rn/AssuntoRN.php`, `fontes/sei/src/main/php/sei/web/rn/BlocoRN.php` e `fontes/sei/src/main/php/sei/web/rn/SolicitacaoOuvidoriaRN.php`. O `fontes/sei/src/main/php/sei/scripts/atualizar_versao_sei.php` usa `tipoTextoVariavel` para `idx_bloco` e `idx_solicitacao`. Para preenchimento em lotes, veja `gerarIndexacaoContatos` em `fontes/sei/src/main/php/sei/web/rn/IndexacaoRN.php`. Um exemplo em módulo é `montarIndexacaoControlado` em `fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/rn/AutuacaoRN.php`.

## Pesquisa textual em autocompletar

Reutilize a pesquisa da entidade sobre o campo textual dedicado quando ele existir. Evite `OPER_LIKE` direto sobre os principais campos de origem, como nome, e-mail, CPF e CNPJ. Para localizar um trecho contínuo, use a opção `true` quando a pesquisa mantiver apenas letras, números e espaços. Valide o termo após normalizar e antes de montar o filtro.

```php
$strPalavrasPesquisa = InfraString::prepararIndexacao($strPalavrasPesquisa, true);
$objContatoDTO->setStrIdxContato('%' . $strPalavrasPesquisa . '%', InfraDTO::$OPER_LIKE);
```
