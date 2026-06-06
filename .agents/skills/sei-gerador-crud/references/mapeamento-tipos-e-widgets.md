# Mapeamento de Tipos, Prefixos e Widgets

## Objetivo

Separar claramente:

- tipo SQL
- tipo semântico do nome do campo
- prefixo DTO
- widget HTML
- máscara/validação esperada

## Mapeamento atual do gerador

| Tipo SQL | Semântico típico | Prefixo DTO | Widget padrão | Validação |
|---|---|---|---|---|
| `int` / `integer` | PK/FK/inteiro | `Num` | `input` ou `select` | obrigatório quando FK/PK de entrada |
| `varchar` | texto | `Str` | `input` | trim + maxlength |
| `date` / `datetime` + coluna `dta_*` | data | `Dta` | `input` + calendário | `InfraData::validarData` |
| `timestamp` / `datetime` + coluna `dth_*` | data e hora | `Dth` | `input` + calendário | `InfraData::validarData` |
| `char(1)` | `sin_` | `Str` | `input` | `InfraUtil::isBolSinalizadorValido` |
| `numeric` | `din_` | `Din` | `input` | obrigatório + máscara monetária |

## Regras semânticas

- `sin_` -> sinalizador `S/N`
- `sta_` -> status multi-valorado
- `dta_` -> data (prefixo DTO `Dta`, constante `PREFIXO_DTA`)
- `dth_` -> data/hora (prefixo DTO `Dth`, constante `PREFIXO_DTH`)
- discriminador Dta/Dth: nome da coluna (nao o tipo SQL); `datetime` aceito por retrocompatibilidade
- `din_` -> dinheiro

## Widgets HTML

- FK obrigatória -> `select`
- `varchar` -> `input`
- `date` / `timestamp` / `datetime` -> `input` com calendário
- `numeric` -> `input` com máscara monetária
- `textarea`, `checkbox`, `radio`, `file` são alvos de evolução futura

## Limite atual

- o gerador já consegue produzir os campos do subconjunto atual
- a ampliação de widgets e tipos SQL deve ocorrer a partir deste mapeamento, não por
  `replace` direto em archetypes padrao
