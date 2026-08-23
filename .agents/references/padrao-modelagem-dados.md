# Padrão de Modelagem de Dados SEI

Referência consolidada para nomenclatura, tipos, chaves, sequências e regras
comuns de scripts de atualização/instalação em módulos SEI/SIP.
Combina o manual SEI-Módulos v5.0 com orientações adicionais do projeto.

---

## Naming e limites

- **Limite para tabelas e colunas**: **26 caracteres** (limite absoluto — os 4 chars restantes
  até o cap Oracle de 30 são reservados para prefixos de objetos derivados: `seq_`, `fk_`, `iXX_`).
- **Limite para índices, FKs e sequences**: **30 caracteres** (cap Oracle).
- Usar apenas letras minúsculas, números e sublinhado.
- Usar singular; suprimir preposições; separar termos por sublinhado.
- Toda tabela e toda coluna devem ter `comment` com descrição negocial.
  - Colunas de status multi-valorado: documentar as opções (ex.: `P=Processo, G=Doc. Gerado`).

---

## Tabelas

| Padrão | Uso |
|--------|-----|
| `md_<sigla>_<funcao>` | tabela funcional comum |
| `md_<sigla>_adm_<funcao>` | tabela de administração |
| `md_<sigla>_rel_<entidade_a>_<entidade_b>` | relacionamento N:N |
| `md_<sigla>_tipo_<entidade>` | conjunto de valores (lookup) |
| `seq_md_<sigla>_<funcao>` | controle de sequencial (gerada automaticamente pelo InfraPHP) |

- `<sigla>`: identifica o módulo — **máximo 3 caracteres** (ex: `ri`, `pet`, `lit`).
- Preferir substantivos, nunca verbos.
- Para N:N, o padrao e `md_<sigla>_rel_<entidade_a>_<entidade_b>`.
- Se a tabela representar um conceito forte do dominio, o nome pode refletir esse conceito em vez do formato `rel_*_*`, desde que permaneça claro e dentro do limite de tamanho.

Exemplos:
- `md_ri_cadastro`, `md_ri_tipo_resposta`, `md_ri_rel_cad_cidade`, `seq_md_ri_cadastro`

---

## Colunas

| Prefixo semântico | Significado | Valores |
|-------------------|-------------|---------|
| `sin_` | sinalizador booleano | `S` / `N` |
| `sta_` | status multi-valorado | documentar opções |
| `dta_` | data | — |
| `dth_` | data/hora | — |
| `din_` | dinheiro / decimal | — |
| `str_` | texto | — |
| `num_` | número inteiro | — |

- **PK gerada por sequence nativa**: `id_<nome_tabela_completo>` (ex.: `md_ri_restaurante` -> `id_md_ri_restaurante`)
- **FK**: repetir exatamente o nome da PK de origem (ex.: `id_md_ri_restaurante` na tabela filha)
- **N:N**: preferir tabela `md_<sigla>_rel_<entidade_a>_<entidade_b>` com PK composta pelas duas FKs de origem
- **Exclusão lógica padrão**: `sin_ativo` com valores `S`/`N`

## DTO, PK e FK

- Em DTOs InfraPHP, `adicionarAtributoTabelaRelacionada(...)` deve vir acompanhado da configuracao explicita da FK correspondente com `configurarFK(...)`.
- Use `InfraDTO::$TIPO_FK_OBRIGATORIA` quando a relacao for obrigatoria e `InfraDTO::$TIPO_FK_OPCIONAL` quando a relacao puder ser nula.
- Use `InfraDTO::$FILTRO_FK_ON` como padrao; reserve `InfraDTO::$FILTRO_FK_WHERE` para casos em que o filtro deva ser aplicado apos o join.

---

## Tipos (portabilidade multi-SGBD)

Preferir tipos SQL-99 comuns; evitar tipos proprietários sem equivalente:

| Tipo preferido | Evitar |
|----------------|--------|
| `integer` | `int4`, `tinyint` |
| `numeric(p,s)` | `money`, `float` |
| `varchar(n)` | `text` (sem limite) |
| `char(n)` | — |
| `date` | — |
| `timestamp` | `datetime` (proprietário) |

---

## Chaves e índices (naming)

| Objeto | Padrão | Exemplo |
|--------|--------|---------|
| Chave primária | `pk_<tabela>` | `pk_md_ri_filme` |
| Chave estrangeira | `fk_<tabela_filha>_<ref_curta>` | `fk_md_ri_rel_fa_filme` |
| Chave alternativa | `ak_<tabela>_<campo(s)>` | `ak_md_ri_filme_titulo` |
| Índice | `iXX_<tabela>_<campo(s)>` | `i01_md_ri_filme_titulo` |

- Nomes de FK e índice também respeitam o limite de 30 caracteres — use abreviações quando necessário.

---

## Sequências / auto-incremento

O InfraPHP usa o padrao `seq_<tabela_funcional>` para sequences nativas.
Toda tabela funcional com PK gerada deve ter uma sequence correspondente.
**Tabelas N:N com PK composta não usam sequence.**

DTOs que usam `seq_<tabela_funcional>` devem configurar a PK com
`InfraDTO::$TIPO_PK_NATIVA`. `InfraDTO::$TIPO_PK_SEQUENCIAL` consulta a tabela
`infra_sequencia` pelo nome da tabela sem o prefixo `seq_`, portanto nao e o
tipo correto para o padrao `seq_<tabela>`.

Padrão de criação multi-SGBD no script SEI:

```php
$this->logar('CRIANDO A SEQUENCE seq_md_xx_entidade');
if (BancoSEI::getInstance() instanceof InfraMySql) {
    BancoSEI::getInstance()->executarSql('create table seq_md_xx_entidade (id bigint not null primary key AUTO_INCREMENT, campo char(1) null) AUTO_INCREMENT = 1');
} else if (BancoSEI::getInstance() instanceof InfraSqlServer) {
    BancoSEI::getInstance()->executarSql('create table seq_md_xx_entidade (id bigint identity(1,1), campo char(1) null)');
} else if (BancoSEI::getInstance() instanceof InfraOracle || BancoSEI::getInstance() instanceof InfraPostgreSql) {
    BancoSEI::getInstance()->criarSequencialNativa('seq_md_xx_entidade', 1);
}
```

---

## Tipos InfraMetaBD (para DDL em scripts)

```php
$objInfraMetaBD = new InfraMetaBD(BancoSEI::getInstance());
```

| Método | Equivalente SQL |
|--------|----------------|
| `tipoNumero()` | `integer` / `number` |
| `tipoTextoVariavel(n)` | `varchar(n)` |
| `tipoTextoFixo(n)` | `char(n)` |
| `tipoNumeroDecimal(p,s)` | `numeric(p,s)` |
| `tipoDataHora()` | `datetime` / `timestamp` |

---

## Scripts de atualização/instalação SEI/SIP

### Princípios gerais

- Gere scripts incrementais por versão. Não pule versões sem rota explícita de migração.
- Atualize apenas scripts já mapeados para módulos existentes em `.agents/references/mapa-modulos-scripts.md`.
- Mantenha idempotência sempre que possível: consulte antes de criar relações, recursos, menus, seeds e parâmetros.
- `atualizarNumeroVersao()` deve ser a última ação funcional de cada `instalarv*`.

### Naming aplicado a scripts

- A seção `Naming e limites` acima é a fonte única para nomes de tabela, coluna, índice, FK e sequence.
- `26` caracteres é válido para tabela/coluna; `> 26` bloqueia.
- `30` caracteres é o limite para índice, FK e sequence.

### Regras multibanco e helpers do core

- Prefira os tipos de `InfraMetaBD::tipo*()` para manter portabilidade entre MySQL, SQL Server, Oracle e PostgreSQL.
- Use `InfraMetaBD` para alterar colunas, criar/remover PK, FK e índices.
- Use SQL bruto apenas quando o core não oferecer abstração equivalente. O caso principal é `CREATE TABLE`.
- Prefira `criarSequencialNativa()` para sequences quando o script-alvo não exigir preservar outro estilo local.
- Preserve o estilo do script existente quando o módulo já usar branching explícito por SGBD para sequence.

### Preferência por funções do core

- Prefira `adicionarColuna`, `alterarColuna`, `adicionarChavePrimaria`, `adicionarChaveEstrangeira`, `criarIndice` e `processarIndicesChavesEstrangeiras`.
- Prefira RN/DTO/BD do core para seed inicial e atualização de parâmetros quando a abstração já existir.
- Prefira `consultar` ou `contar` antes de cadastrar qualquer dado que precise ser idempotente.

### Guardrails de geração

- Não use SQL bruto para `ALTER TABLE`, PK, FK ou índice quando houver helper do core.
- Não gere sequence para tabela N:N com PK composta.
- Não duplique índice de FK quando `adicionarChaveEstrangeira()` já o cria por padrão.
- Não gere chamadas com assinatura divergente do core atual, como `tipoNumero(2)` ou `tipoNumeroGrande(20)`, sem confirmação explícita.
- Não trate `comment` de tabela/coluna como automatizado por padrão antes de confirmar a estratégia multibanco do projeto.
- Para efeitos colaterais e transação, seguir `AGENTS.md` na seção `Padrão Transacional Obrigatório`.

### Responsabilidade por lado

- Script SEI: DDL, schema, sequence, seed técnico, parâmetros e integrações internas.
- Script SIP: recursos, perfis, menus, auditoria, vínculos e parâmetros do SIP.
- Não leve validações de ativação do SEI para `sip/scripts/*`.
- Não use script SIP para DDL estrutural do módulo SEI fora de casos explicitamente previstos.

### Checklist antes de gerar scripts

- Confirmar módulo, versão atual e versão alvo.
- Confirmar se o impacto é SEI, SIP ou ambos.
- Confirmar nomes de tabela, coluna, FK, PK, índice e sequence dentro dos limites.
- Confirmar se a tabela precisa ou não de sequence.
- Confirmar seeds iniciais e sua idempotência.
- Confirmar se há parâmetros, recursos, perfis, menus ou auditoria envolvidos.
- Confirmar o helper do core mais específico disponível.

### Checklist após gerar scripts

- Rodar `php -l` no(s) script(s) alterado(s).
- Rodar `python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <script> --mode release_check` no artefato PHP gerado/alterado quando houver DDL.
- Revisar se o `switch` incremental ficou correto.
- Revisar se `atualizarNumeroVersao()` é a última ação funcional.
- Validar naming e modelagem com as ferramentas do projeto.
- Revisar se o script manteve compatibilidade multibanco.

### Pontos a confirmar antes de automatizar mais

- Estratégia oficial do projeto para `comment` de tabela/coluna em ambiente multibanco.
- Existência de helper superior ao SQL direto para vinculação de auditoria no SIP.

> Para padrões completos de código dos métodos `instalarv*` (DDL, FKs, boilerplate SIP),
> consultar: `.agents/references/padrao-scripts-release.md`

> Para regras de auditoria de modelagem (DB01-DB15) com verificação automatizada,
> consultar: `.agents/skills/sei-verificacao-banco-dados/references/padroes-manual-md.md`
