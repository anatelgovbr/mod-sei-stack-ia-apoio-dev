# Padrões de Modelagem de Dados — Manual TRF4

Este documento consolida as 15 regras de modelagem de dados extraídas dos manuais
oficiais de desenvolvimento SEI/SIP — especificamente `sei_modulos_manual_dev_5_padrao_modelagem_de_dados.md`
e seções relevantes de `sei_modulos_manual_dev_4_infraphp.md`.

Todas as regras são quoting direto ou interpretação fiel do manual.
Cada regra inclui: identificador, severidade, base oficial, descrição e exemplo.

---

## Regras de Nomenclatura (Gerais)

### DB01: Nome de Tabela: `md_<sigla>_<entidade>`
**Severidade:** Erro
**Base:** Manual SEI MD §Tabelas (linha 25-33)

Nomes de tabelas devem:
- Usar prefixo `md_<instituicao/modulo>`
- Usar apenas substantivos (sem verbos)
- Estar no singular
- Usar minúsculas e sublinhado para separar palavras
- Suprimir preposições
- Limite de 26 caracteres

**Conforme:**
- `md_abc_pedido`
- `md_ri_restaurante`
- `md_ri_tp_ctrl_demanda`

**Não conforme:**
- `md_abc_pedidos` (plural)
- `md_abc_criar_pedido` (verbo)
- `md_abc_tipo_controle_de_demanda` (excede 26)

---

### DB02: Relacionamento N:N: `_rel_`
**Severidade:** Erro
**Base:** Manual SEI MD §Tabelas (linha 35-41)

Tabelas de relacionamento muitos-para-muitos devem usar prefixo `_rel_`
seguido dos nomes das entidades envolvidas, **sem** o prefixo `md_<sigla>`.

**Conforme:**
- `md_abc_rel_pedido_item`
- `md_ri_rel_cardapio_prato`
- `md_abc_rel_usuario_sistema`

**Exceção conceitual:** Se o relacionamento expressar um conceito forte do sistema,
pode usar esse conceito como nome:
- `md_abc_administrador_sistema` (em vez de `md_abc_rel_usuario_sistema`)

**Não conforme:**
- `md_abc_pedido_item` (falta `_rel_`)
- `md_abc_rel_pedido_item_produto` (excede limite de 26)

---

### DB03: Limite de 26 caracteres
**Severidade:** Erro
**Base:** Manual SEI MD §Regras Gerais (linha 8-13)

Nomes de tabelas e colunas limitados a **máximo 26 caracteres**.
Reservar 4 caracteres para prefixos (`seq_`, `fk_`, `i01_`, etc.)
isso evita atingir o limite de 30 do Oracle para nomes de elementos.

**Conforme:**
- `md_ri_tp_ctrl_demanda` (22 chars)

**Não conforme:**
- `md_abc_tipo_controle_de_demanda` (34 chars)
- `md_ri_restaurante_cardapio` (28 chars)

---

### DB15: Formato do nome: minúsculas + sublinhado + sem preposições
**Severidade:** Aviso
**Base:** Manual SEI MD §Regras Gerais (linha 14-17)

- Usar apenas letras minúsculas
- Separar palavras com `_` (sublinhado)
- Suprimir preposições (de, da, do, em, etc.)

**Conforme:** `md_abc_data_vencimento`
**Não conforme:** `md_abc_data_de_vencimento`

---

## Regras de Colunas

### DB04: PK Sequencial: `id_md_<sigla>_<entidade>`
**Severidade:** Erro
**Base:** Manual SEI MD §Colunas (linha 49-52)

Chaves primárias sequenciais devem usar prefixo `id` seguido do nome
da tabela **completo** (com prefixo `md_`).

**Conforme:**
- `id_md_abc_pedido`
- `id_md_ri_restaurante`
- `id_md_ri_rel_cardapio_prato`

**Não conforme:**
- `id_pedido` (falta prefixo md_)
- `id_md_abc` (nome da tabela incompleto)

Para **PKs que usam FK** (chave composta), manter a nomenclatura
igual à chave primária de origem:
- `id_md_abc_tabela_a`
- `id_md_abc_tabela_b`

No DTO, todas as colunas da PK composta usam `TIPO_PK_INFORMADO`. A tabela
de relacionamento com PK composta não possui sequence.

---

### DB06: `sin_ativo` em entidades com exclusão lógica
**Severidade:** Erro
**Base:** Manual SEI MD §Colunas (linha 69)

Para **exclusão lógica**, utilizar o campo `sin_ativo` do tipo `char(1)`
com valor default `'S'` (ativo).

No InfraPHP, isso é configurado via `configurarExclusaoLogica('SinAtivo', 'N')`.

**Conforme:**
```php
$this->configurarExclusaoLogica('SinAtivo', 'N');
// E a coluna correspondente:
$this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'SinAtivo', 'sin_ativo');
```

**Não conforme:**
- Entidade com `configurarExclusaoLogica()` mas sem coluna `sin_ativo`
- Coluna `sin_ativo` com tipo diferente de `char(1)`

---

## Regras de Constraints

### DB07: PK constraint: `pk_<nome>`
**Severidade:** Erro
**Base:** Manual SEI MD §Chave Primária (linha 94-99)

Constraint de chave primária deve usar prefixo `pk_` seguido do nome da entidade.

**Conforme:**
- `pk_md_abc_pedido`
- `pk_md_ri_restaurante`

**Não conforme:**
- `pk_md_abc` (nome incompleto)
- `PK_md_abc_pedido` (maiúscula)

---

### DB05: FK constraint: `fk_md_<sigla>_<ent>_<ref>`
**Severidade:** Erro
**Base:** Manual SEI MD §Chave Estrangeira (linha 110-114)

FK constraint deve usar prefixo `fk_md_<sigla>` seguido do nome da entidade
que possui a FK e do nome da entidade referenciada, **sem** o prefixo `md_<sigla>`
na referência.
O nome completo da constraint usa apenas letras minúsculas, números e sublinhado.

**Conforme:**
- `fk_md_abc_item_pedido` (item referencia pedido)
- `fk_md_ri_rel_cardapio_prato_restaurante`
- `fk_md_ri_rel_cardapio_prato_cardapio`

**Não conforme:**
- `fk_item_pedido` (falta prefixo md_)
- `fk_md_abc_item_md_abc_pedido` (referência tem prefixo redundante)
- `fk_md_abc_item_md_pedido` (referência tem prefixo partial)

---

### DB11: AK constraint: `ak_<nome>_<campos>`
**Severidade:** Aviso
**Base:** Manual SEI MD §Chave Alternativa (linha 102-107)

Constraints unique (chaves candidatas) devem usar prefixo `ak_` seguido do
nome da entidade e dos campos que a compõem.

**Conforme:**
- `ak_md_abc_pedido_codigo`
- `ak_md_ri_restaurante_cnpj`

**Não conforme:**
- `ak_md_abc` (sem campos)
- `unique_md_abc_pedido_codigo` (prefixo errado)

---

## Regras de Índices e Sequences

### DB09: Índice em colunas FK
**Severidade:** Aviso
**Base:** Manual SEI MD §Índices (linha 117-131)

Índices que **não** representam FKs devem usar prefixo `i(01-99)_` seguido
do nome da entidade. Para FKs, usar o mesmo nome da constraint de FK.

**Conforme:**
- `fk_md_abc_item_pedido` (índice para FK — mesmo nome)
- `i01_md_abc_pedido`
- `i02_md_abc_pedido`

**Não conforme:**
- FK sem índice correspondente
- Índice com nome diferente da constraint FK

---

### DB10: Sequence naming: `seq_<nome>`
**Severidade:** Aviso
**Base:** Manual SEI MD §Sequências (linha 135-171)

Sequences devem usar prefixo `seq_` seguido do nome do objeto ao qual atendem,
**sem** prefixo `md_<sigla>`.

**Conforme:**
- `seq_md_abc_pedido`
- `seq_md_ri_restaurante`

**Não conforme:**
- `seq_md-abc-pedido` (hífens)
- `sequence_md_abc_pedido` (nome diferente)

**Importante:** O prefixo `seq_` é usado, diferente do prefixo `md_` das tabelas.

---

## Regras de Tipos e Comentários

### DB08: Tipos SQL-99 (sem money/text)
**Severidade:** Erro
**Base:** Manual SEI MD §Tipos de Dados (linha 71-91)

Apenas tipos definidos pelo padrão SQL-99 (SQL3). Evitar tipos proprietários.

**Tipos recomendados:**
- `integer` — inteiros com sinal
- `smallint` — inteiros pequenos
- `numeric(p,s)` — decimais com precisão fixa
- `decimal(p,s)` — precisão maior que numeric
- `varchar(n)` — tamanho variável
- `char(n)` — tamanho fixo
- `date`, `time(p)`, `timestamp(p)`
- `boolean`, `blob`, `clob`

**Proibidos:**
- `money` — tipo proprietário
- `text` — tipo variável sem limite (não padrão)
- `serial` — shortcut PostgreSQL, não portátil
- `identity` — shortcut SQL Server, não portátil

**Conforme:**
- `numeric(10,2)` para valores monetários
- `varchar(100)` para nomes

**Não conforme:**
- `money(10,2)` (não é SQL-99)
- `text` sem limite definido

Em `adicionarAtributoTabelaRelacionada(...)`, o terceiro argumento identifica
a coluna SQL. Ele deve ser um literal em snake_case, com alias também em
snake_case quando qualificado, por exemplo `item.nome`.

---

### DB12: Comentários / Docblock
**Severidade:** Aviso
**Base:** Manual SEI MD §Regras Gerais (linha 18-19)

Todas as tabelas e colunas devem possuir descrição negocial no campo de
metadado `comment`, informando sua finalidade funcional.
Se a coluna for de status multivalorado, informar também opções e finalidades.

**Exemplo de COMMENT:**
```sql
COMMENT ON TABLE md_ri_restaurante IS 'Restaurantes participantes do programa de alimentação';
COMMENT ON COLUMN md_ri_restaurante.sin_ativo IS 'Indica se o restaurante está ativo no programa. Valores: S=Ativo, N=Inativo';
```

**No DTO (InfraPHP), usar docblock:**
```php
/**
 * @table Restaurantes participantes do programa de alimentação
 * @column sin_ativo S=Ativo, N=Inativo
 */
class MdRiRestauranteDTO extends InfraDTO {
```

**Conforme:**
- COMMENT ON em todas as tabelas e colunas
- Docblock no DTO com @table e @column

**Não conforme:**
- Tabela sem nenhum comentário
- Coluna de status sem indicar opções

---

## Regras de Semântica

### DB13: Sem verbos no nome da tabela
**Severidade:** Aviso
**Base:** Manual SEI MD §Tabela (linha 25)

Não utilizar verbos para designar nomes de tabelas. Priorizar substantivos.

**Conforme:**
- `md_abc_pedido` (substantivo)
- `md_abc_item` (substantivo)

**Não conforme:**
- `md_abc_criar_pedido` (verbo)
- `md_abc_gerar_documento` (verbo)
- `md_abc_realizar_pagamento` (verbo)

---

### DB14: Singular nos nomes
**Severidade:** Aviso
**Base:** Manual SEI MD §Regras Gerais (linha 17)

Todas as tabelas e colunas devem estar no singular.

**Conforme:**
- `md_abc_pedido`
- `md_abc_item`

**Não conforme:**
- `md_abc_pedidos`
- `md_abc_itens`

---

## Matriz de Severidade Resumida

| ID | Regra | Sev | Base |
|----|-------|-----|------|
| DB01 | Nome tabela `md_<sigla>_<entidade>` | **Erro** | §Tabela |
| DB02 | N:N: `_rel_` | **Erro** | §Tabela |
| DB03 | Tamanho ≤ 26 chars | **Erro** | §Regras Gerais |
| DB04 | PK gerada `id_md_<sigla>_<entidade>` | **Erro** | §Colunas |
| DB05 | FK `fk_md_<sigla>_<ent>_<ref>` | **Erro** | §Chave Estrangeira |
| DB06 | `sin_ativo` em exclusão lógica | **Erro** | §Colunas |
| DB07 | PK constraint `pk_<nome>` | **Erro** | §Chave Primária |
| DB08 | Tipos SQL-99 (sem money/text) | **Erro** | §Tipos de Dados |
| DB09 | Índice em FK | **Aviso** | §Índices |
| DB10 | Sequence `seq_<nome>` | **Aviso** | §Sequências |
| DB11 | AK constraint `ak_<nome>_<campos>` | **Aviso** | §Chave Alternativa |
| DB12 | COMMENT ON / docblock | **Aviso** | §Regras Gerais |
| DB13 | Sem verbos | **Aviso** | §Tabela |
| DB14 | Singular | **Aviso** | §Regras Gerais |
| DB15 | Formato minúsculas + sublinhado | **Aviso** | §Regras Gerais |

**Erro** = bloqueante (impede conformidade)
**Aviso** = informativo (não bloqueia mas indica desvio)

---

## Prefixos de Colunas (informativos)

| Prefixo | Significado | Exemplo |
|---------|-------------|---------|
| `sin_` | Sinalizador S/N | `sin_ativo` |
| `sta_` | Status multivalorado | `sta_documento` |
| `dta_` | Data | `dta_criacao` |
| `dth_` | Data/hora | `dth_alteracao` |
| `din_` | Dinheiro | `din_valor` |

Estes são conveções de nomenclatura de colunas, não regras de auditoria.

---

## Referencias cruzadas

- **Templates DDL e InfraMetaBD**: consultar `.agents/references/padrao-modelagem-dados.md`
  - Contém boilerplate de criação de tabelas, sequences multi-SGBD, tipos `InfraMetaBD`
- **Regras DB01-DB15 (este arquivo)**: validação de modelagem contra padrões TRF4
