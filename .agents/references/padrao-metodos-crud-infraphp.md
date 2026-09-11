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
