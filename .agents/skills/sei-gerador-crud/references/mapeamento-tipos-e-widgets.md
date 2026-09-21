# Mapeamento de Tipos, Prefixos e Widgets

## Objetivo

Separar claramente tipo SQL, tipo semântico do nome do campo, prefixo DTO, widget HTML e validação. O gerador aplica exatamente esta tabela.

## Mapeamento do gerador

| Tipo SQL | Nome da coluna | Prefixo DTO | Widget | Validação na RN | JavaScript no cadastro |
|---|---|---|---|---|---|
| `int` / `integer` | PK `id_<tabela>` | `Num` | oculto (`hdnId<Classe>`) | sem validador (PK nativa) | nenhum |
| `int` / `integer` | FK `id_*` com `relacionamentos` | `Num` | `select` via helper INT do pai | obrigatório só quando `obrigatorio: true`; vazio vira `null` quando opcional | `infraSelectSelecionado` quando obrigatório |
| `int` / `integer` | demais | `Num` | `input` | obrigatório só quando `obrigatorio: true`; vazio vira `null` quando opcional | vazio quando obrigatório |
| `varchar` | texto | `Str` | `input` com `infraMascaraTexto` e `maxlength` | trim + tamanho máximo | vazio quando obrigatório |
| `date` | `dta_*` | `Dta` | `input` + calendário com `infraMascaraData` | `InfraData::validarData` | `infraValidarData` |
| `timestamp` | `dth_*` (obrigatório) | `Dth` | `input` + calendário com `infraMascaraDataHora` | `InfraData::validarDataHora` | `infraValidarDataHora` |
| `datetime` | `dta_*` ou `dth_*` (discrimina pelo nome) | `Dta` ou `Dth` | como acima | como acima | como acima |
| `char(1)` | `sin_*` | `Str` | não entra no formulário (`sin_ativo` é fixado em `S` no cadastro) | `InfraUtil::isBolSinalizadorValido` | nenhum |
| `numeric` | `din_*` | `Din` | `input` com `infraMascaraDinheiro` | `InfraUtil::validarDin` (aceita `1.234,56`, rejeita negativo); o valor não é alterado na RN, `InfraBD` converte na gravação | vazio quando obrigatório |
| `numeric` | sem `din_` | `Dbl` | `input` com `infraMascaraNumero` | `is_numeric` | vazio quando obrigatório |

## Regras semânticas

- `sin_` vira sinalizador `S/N`; só `sin_ativo` é reconhecido como exclusão lógica (`regrasGeracao.campoSinAtivo`).
- `sta_` (status multivalorado) é rejeitado pelo gerador com mensagem; o CRUD precisa de widget de opções que a v1 não produz.
- `dta_` guarda data; `dth_` guarda data e hora. `timestamp` sem `dth_` e `date` com `dth_` são rejeitados.
- `din_` é dinheiro; `numeric` sem `din_` é número (`Dbl`, idioma do SEI para identificadores grandes) e gera alerta ao desenvolvedor.
- Coluna sem prefixo semântico recebe o prefixo pelo tipo SQL.

## Largura dos campos no cadastro

| Campo | Largura |
|---|---|
| FK, data, data e hora, número, dinheiro | 25% |
| `varchar` até 30 | 20% |
| `varchar` até 100 | 50% |
| `varchar` acima de 100 | 95% |

O gabarito TRF4 usa 25% em todo campo; a regra por tamanho é desvio consciente da skill.

## Widgets fora da v1

`textarea`, `checkbox`, `radio` e `file` não são gerados. Coluna de texto longo sai como `input`.
