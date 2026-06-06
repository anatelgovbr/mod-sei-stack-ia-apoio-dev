# Metadados do Domínio md_abc

Domínio de referência para geração de gabaritos CRUD InfraPHP (TRF4).
Cobre 5 entidades: standalone, 1:N, 1:N (2º nível), 1:1 e N:N.

---

## Tabelas

### md_abc_projeto
**Tipo:** standalone com exclusão lógica
**Artigo:** o | **Singular:** Projeto | **Plural:** Projetos | **Campo principal:** `identificacao`

| Campo | Tipo | Tamanho | Requerido | PK | FK | Tabela Origem |
|---|---|---|---|---|---|---|
| id_md_abc_projeto | integer | — | Sim | Sim | — | — |
| identificacao | varchar | 50 | Sim | — | — | — |
| descricao | varchar | 255 | Não | — | — | — |
| dta_cadastramento | date | — | Sim | — | — | — |
| sin_ativo | char | 1 | Sim | — | — | — |

**Labels UI:**

| Campo | Rótulo | Atalho | Artigo |
|---|---|---|---|
| identificacao | Identificação | I | a |
| descricao | Descrição | D | a |
| dta_cadastramento | Data de Cadastramento | C | a |
| sin_ativo | Ativo | — | o |

---

### md_abc_aquisicao
**Tipo:** 1:N → md_abc_projeto (sem sin_ativo)
**Artigo:** a | **Singular:** Aquisição | **Plural:** Aquisições | **Campo principal:** `descricao`

| Campo | Tipo | Tamanho | Requerido | PK | FK | Tabela Origem |
|---|---|---|---|---|---|---|
| id_md_abc_aquisicao | integer | — | Sim | Sim | — | — |
| id_md_abc_projeto | integer | — | Sim | — | Sim | md_abc_projeto |
| descricao | varchar | 50 | Sim | — | — | — |
| din_custo | numeric | 15,2 | Sim | — | — | — |

**Labels UI:**

| Campo | Rótulo | Atalho | Artigo |
|---|---|---|---|
| id_md_abc_projeto | Projeto | P | o |
| descricao | Descrição | D | a |
| din_custo | Custo | C | o |

---

### md_abc_contrato
**Tipo:** 1:N → md_abc_aquisicao (sem sin_ativo)
**Artigo:** o | **Singular:** Contrato | **Plural:** Contratos | **Campo principal:** `numero`

| Campo | Tipo | Tamanho | Requerido | PK | FK | Tabela Origem |
|---|---|---|---|---|---|---|
| id_md_abc_contrato | integer | — | Sim | Sim | — | — |
| id_md_abc_aquisicao | integer | — | Sim | — | Sim | md_abc_aquisicao |
| numero | varchar | 20 | Sim | — | — | — |
| dta_assinatura | date | — | Sim | — | — | — |
| din_valor | numeric | 15,2 | Sim | — | — | — |
| observacao | varchar | 500 | Não | — | — | — |

**Labels UI:**

| Campo | Rótulo | Atalho | Artigo |
|---|---|---|---|
| id_md_abc_aquisicao | Aquisição | A | a |
| numero | Número | N | o |
| dta_assinatura | Data de Assinatura | D | a |
| din_valor | Valor | V | o |
| observacao | Observação | O | a |

---

### md_abc_responsavel
**Tipo:** 1:1 → md_abc_contrato (sem sin_ativo)
**Artigo:** o | **Singular:** Responsável | **Plural:** Responsáveis | **Campo principal:** `nome`

| Campo | Tipo | Tamanho | Requerido | PK | FK | Tabela Origem |
|---|---|---|---|---|---|---|
| id_md_abc_responsavel | integer | — | Sim | Sim | — | — |
| id_md_abc_contrato | integer | — | Sim | — | Sim | md_abc_contrato |
| nome | varchar | 100 | Sim | — | — | — |
| cargo | varchar | 50 | Sim | — | — | — |
| email | varchar | 100 | Não | — | — | — |

**Constraint de unicidade:** `ak_md_abc_responsavel_contrato` em `id_md_abc_contrato` — garante o 1:1.

**Labels UI:**

| Campo | Rótulo | Atalho | Artigo |
|---|---|---|---|
| id_md_abc_contrato | Contrato | C | o |
| nome | Nome | N | o |
| cargo | Cargo | G | o |
| email | E-mail | E | o |

---

### md_abc_rel_contrato_projeto
**Tipo:** N:N → md_abc_contrato + md_abc_projeto (PK composta)
**Artigo:** a | **Singular:** Associação | **Plural:** Associações | **Campo principal:** `id_md_abc_contrato` (exibe `numero` via JOIN)

| Campo | Tipo | Tamanho | Requerido | PK | FK | Tabela Origem |
|---|---|---|---|---|---|---|
| id_md_abc_contrato | integer | — | Sim | Sim | Sim | md_abc_contrato |
| id_md_abc_projeto | integer | — | Sim | Sim | Sim | md_abc_projeto |
| dta_associacao | date | — | Sim | — | — | — |

**Labels UI:**

| Campo | Rótulo | Atalho | Artigo |
|---|---|---|---|
| id_md_abc_contrato | Contrato | C | o |
| id_md_abc_projeto | Projeto | P | o |
| dta_associacao | Data de Associação | D | a |

---

## Chaves Primárias

| Nome | Tabela | Campos |
|---|---|---|
| pk_md_abc_projeto | md_abc_projeto | id_md_abc_projeto |
| pk_md_abc_aquisicao | md_abc_aquisicao | id_md_abc_aquisicao |
| pk_md_abc_contrato | md_abc_contrato | id_md_abc_contrato |
| pk_md_abc_responsavel | md_abc_responsavel | id_md_abc_responsavel |
| pk_md_abc_rel_contrato_projeto | md_abc_rel_contrato_projeto | id_md_abc_contrato, id_md_abc_projeto |

---

## Chaves Estrangeiras

| Nome | Tabela | Campo | Tabela Origem | Campo Origem |
|---|---|---|---|---|
| fk_md_abc_aquisicao_projeto | md_abc_aquisicao | id_md_abc_projeto | md_abc_projeto | id_md_abc_projeto |
| fk_md_abc_contrato_aquisicao | md_abc_contrato | id_md_abc_aquisicao | md_abc_aquisicao | id_md_abc_aquisicao |
| fk_md_abc_responsavel_contrato | md_abc_responsavel | id_md_abc_contrato | md_abc_contrato | id_md_abc_contrato |
| fk_md_abc_rel_contrato_projeto_c | md_abc_rel_contrato_projeto | id_md_abc_contrato | md_abc_contrato | id_md_abc_contrato |
| fk_md_abc_rel_contrato_projeto_p | md_abc_rel_contrato_projeto | id_md_abc_projeto | md_abc_projeto | id_md_abc_projeto |

---

## Diagrama de Relacionamentos

```
md_abc_projeto (standalone, sin_ativo)
    │
    │ 1:N
    ▼
md_abc_aquisicao (FK → projeto)
    │
    │ 1:N
    ▼
md_abc_contrato (FK → aquisicao)
    │                    │
    │ 1:1                │ N:N (via rel)
    ▼                    ▼
md_abc_responsavel   md_abc_rel_contrato_projeto
(FK única →              (FK → contrato + FK → projeto)
 contrato)
```

---

## SQL para a ferramenta TRF4

```sql
create table md_abc_projeto (
  id_md_abc_projeto integer        not null,
  identificacao     varchar(50)    not null,
  descricao         varchar(255)       null,
  dta_cadastramento date           not null,
  sin_ativo         char(1)        not null
);
alter table md_abc_projeto
  add constraint pk_md_abc_projeto primary key (id_md_abc_projeto);

create table md_abc_aquisicao (
  id_md_abc_aquisicao integer        not null,
  id_md_abc_projeto   integer        not null,
  descricao           varchar(50)    not null,
  din_custo           numeric(15,2)  not null
);
alter table md_abc_aquisicao
  add constraint pk_md_abc_aquisicao primary key (id_md_abc_aquisicao);
alter table md_abc_aquisicao
  add constraint fk_md_abc_aquisicao_projeto
  foreign key (id_md_abc_projeto) references md_abc_projeto (id_md_abc_projeto);
create index fk_md_abc_aquisicao_projeto on md_abc_aquisicao (id_md_abc_projeto);

create table md_abc_contrato (
  id_md_abc_contrato  integer        not null,
  id_md_abc_aquisicao integer        not null,
  numero              varchar(20)    not null,
  dta_assinatura      date           not null,
  din_valor           numeric(15,2)  not null,
  observacao          varchar(500)       null
);
alter table md_abc_contrato
  add constraint pk_md_abc_contrato primary key (id_md_abc_contrato);
alter table md_abc_contrato
  add constraint fk_md_abc_contrato_aquisicao
  foreign key (id_md_abc_aquisicao) references md_abc_aquisicao (id_md_abc_aquisicao);
create index fk_md_abc_contrato_aquisicao on md_abc_contrato (id_md_abc_aquisicao);

create table md_abc_responsavel (
  id_md_abc_responsavel integer        not null,
  id_md_abc_contrato    integer        not null,
  nome                  varchar(100)   not null,
  cargo                 varchar(50)    not null,
  email                 varchar(100)       null
);
alter table md_abc_responsavel
  add constraint pk_md_abc_responsavel primary key (id_md_abc_responsavel);
alter table md_abc_responsavel
  add constraint ak_md_abc_responsavel_contrato unique (id_md_abc_contrato);
alter table md_abc_responsavel
  add constraint fk_md_abc_responsavel_contrato
  foreign key (id_md_abc_contrato) references md_abc_contrato (id_md_abc_contrato);
create index fk_md_abc_responsavel_contrato on md_abc_responsavel (id_md_abc_contrato);

create table md_abc_rel_contrato_projeto (
  id_md_abc_contrato integer  not null,
  id_md_abc_projeto  integer  not null,
  dta_associacao     date     not null
);
alter table md_abc_rel_contrato_projeto
  add constraint pk_md_abc_rel_contrato_projeto
  primary key (id_md_abc_contrato, id_md_abc_projeto);
alter table md_abc_rel_contrato_projeto
  add constraint fk_md_abc_rel_contrato_projeto_c
  foreign key (id_md_abc_contrato) references md_abc_contrato (id_md_abc_contrato);
alter table md_abc_rel_contrato_projeto
  add constraint fk_md_abc_rel_contrato_projeto_p
  foreign key (id_md_abc_projeto) references md_abc_projeto (id_md_abc_projeto);
create index fk_md_abc_rel_contrato_projeto_c on md_abc_rel_contrato_projeto (id_md_abc_contrato);
create index fk_md_abc_rel_contrato_projeto_p on md_abc_rel_contrato_projeto (id_md_abc_projeto);
```
