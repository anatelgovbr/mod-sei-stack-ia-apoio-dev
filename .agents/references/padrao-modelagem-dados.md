# Padrão de Modelagem de Dados SEI

Referência consolidada para nomenclatura, tipos, chaves, sequências e regras
comuns de scripts de atualização/instalação em módulos SEI/SIP.
Combina o manual SEI-Módulos v5.0 com orientações adicionais do projeto.

---

## Naming e limites

- **Limite para tabelas e colunas**: **26 caracteres** (limite absoluto — os 4 chars restantes
  até o cap Oracle de 30 são reservados para prefixos de objetos derivados: `seq_`, `fk_`, `iNN_`).
- **Limite para índices, FKs e sequences**: **30 caracteres** (cap Oracle).
- Usar apenas letras minúsculas, números e sublinhado.
- Usar singular; suprimir preposições; separar termos por sublinhado.
- Toda tabela e toda coluna têm descrição negocial no docblock do DTO: `@table` para a tabela e `@column` para cada coluna.
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
- **Busca textual**: para modelar ou alterar uma coluna `idx_<entidade>`, aplique a seção [Coluna derivada para busca textual](padrao-metodos-crud-infraphp.md#coluna-derivada-para-busca-textual).

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
| Índice que não representa FK | `iNN_<tabela>`, com `NN` de `01` a `99` | `i01_md_ri_filme` |
| Índice que representa FK | o nome da FK | `fk_md_ri_rel_fa_filme` |

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

No script SEI, a sequence é criada com `BancoSEI::getInstance()->criarSequencialNativa('seq_md_xx_entidade', 1)`, que funciona nos quatro bancos. Criar, remover e ajustar o próximo valor: `.agents/references/padrao-scripts-release.md`, seções "Sequence / auto-incremento", "Remover sequence" e "Ajustar o próximo valor de uma sequence".

---

## Tipos InfraMetaBD (para DDL em scripts)

Os métodos `tipo*()` da `InfraMetaBD`, o tipo que cada um gera em cada banco e o limite de tamanho de cada um estão em `.agents/references/padrao-scripts-release.md`, seções "Objeto obrigatório" e "Criar tabela".

---

## Scripts de atualização/instalação SEI/SIP

### Princípios gerais

- Gere scripts incrementais por versão. Não pule versões sem rota explícita de migração.
- Atualize apenas scripts já mapeados para módulos existentes em `.agents/references/mapa-modulos-scripts.md`.
- Mantenha idempotência sempre que possível: consulte antes de criar relações, recursos, menus, seeds e parâmetros.
- `atualizarNumeroVersao()` deve ser a última ação funcional de cada `instalarv*`.

### Naming aplicado a scripts

- As seções `Naming e limites` e `Chaves e índices (naming)` acima são a fonte única para nomes e limites de tabela, coluna, índice, FK e sequence.

### Regras multibanco e helpers do core

- Prefira os tipos de `InfraMetaBD::tipo*()` para manter portabilidade entre MySQL, SQL Server, Oracle e PostgreSQL.
- Use `InfraMetaBD` para alterar colunas, criar/remover PK, FK e índices.
- Use SQL bruto apenas quando o core não oferecer abstração equivalente. O caso principal é `CREATE TABLE`.
- Crie sequence com `criarSequencialNativa()`, inclusive em script que já ramifica por banco para sequence.
- Siga os padrões multibanco de `.agents/references/padrao-scripts-release.md` para tipo da coluna de FK, FK nas colunas da PK, coluna `NOT NULL` em tabela com dados, alteração ou exclusão de coluna com FK ou índice, troca de tipo de coluna com dados, remoção e ajuste de sequence, checagem de existência, índice único, opção de nulidade em minúsculas, `setBolValidarIdentificador(true)` e leitura e gravação de dados no script.

### Preferência por funções do core

- Prefira `adicionarColuna`, `alterarColuna`, `adicionarChavePrimaria`, `adicionarChaveEstrangeira`, `criarIndice` e `processarIndicesChavesEstrangeiras`.
- Prefira RN/DTO/BD do core para seed inicial e atualização de parâmetros quando a abstração já existir.
- Prefira `consultar` ou `contar` antes de cadastrar qualquer dado que precise ser idempotente.

### Guardrails de geração

- Não use SQL bruto para `ALTER TABLE`, PK, FK ou índice quando houver helper do core.
- Não gere sequence para tabela N:N com PK composta.
- Não duplique índice de FK quando `adicionarChaveEstrangeira()` já o cria por padrão.
- Gere `tipoNumero()` e `tipoNumeroGrande()` sem argumento: os dois métodos não recebem parâmetro.
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
- Conferir o DDL gerado contra cada padrão multibanco de `.agents/references/padrao-scripts-release.md` que se aplica a ele.

### Pontos a confirmar antes de automatizar mais

- Existência de helper superior ao SQL direto para vinculação de auditoria no SIP.

> Para padrões completos de código dos métodos `instalarv*` (DDL, FKs, boilerplate SIP),
> consultar: `.agents/references/padrao-scripts-release.md`

> Para regras de auditoria de modelagem (DB01-DB15) com verificação automatizada,
> consultar: `.agents/skills/sei-verificacao-banco-dados/references/padroes-manual-md.md`


## Portabilidade entre bancos

Regras do manual que valem para todo script de instalação e atualização. Erro aqui passa no banco de desenvolvimento e quebra o release no banco do cliente.

- **Comprimento de coluna**: `tipoTextoVariavel(n)` vai até **4000** e `tipoTextoFixo(n)` até **255**; texto maior usa `tipoTextoGrande()`. Acima desses valores, pelo menos um dos quatro bancos recusa a coluna; o limite de cada banco está em `.agents/references/padrao-scripts-release.md`, seção "Criar tabela".
- **Sequences**: são usadas quando o DTO declara o tipo de chave primária nativa. Dependendo do banco, a sequence é implementada como tabela ou como sequence real, então o script não pode assumir uma das duas formas.
- **Funções de banco**: em script de instalação e atualização, usar os métodos da `InfraMetaBD` e o `criarSequencialNativa` do `BancoSEI` em vez de DDL escrita à mão, conforme a seção "Regras multibanco e helpers do core". O manual (cap. 5) cita `/infra/InfraBD.php`, mas os métodos de DDL ficam na `InfraMetaBD`; a `InfraBD` é a classe base das BDs, com o acesso por DTO.

### Bind de campos CLOB em `executarSql`

A assinatura é `executarSql($strSql, $arrCamposBind = null)` nos quatro bancos, e devolve o número de registros afetados. O formato do segundo parâmetro e a marcação do campo no SQL mudam de um banco para outro: no Oracle, o array é indexado pelo nome do marcador, como `[':txt' => $strTexto]` para `values (:txt)`.

No Oracle, texto com mais de 4000 bytes escrito direto no SQL falha (ORA-01704), e a gravação em coluna `tipoTextoGrande()` exige bind. MySQL, SQL Server e PostgreSQL aceitam esse texto direto no SQL.

Para gravar texto longo no script, use DTO e BD: a `InfraBD` monta o bind de cada banco. Em SQL escrito à mão, ramifique por banco, com bind no ramo Oracle.

## Nomenclatura de tabela, regras do manual

- **Sem verbos.** Nao usar verbo para designar nome de tabela. Priorizar substantivo, com o prefixo do modulo.
- **Clareza dentro de 26 caracteres.** O nome representa a entidade de forma clara dentro do limite. Abreviar so quando o nome completo nao couber, e de forma consistente entre tabelas do mesmo modulo.
- **Conjunto de valores.** Tabela que representa conjunto de valores relacionados a uma entidade recebe prefixo proprio, para distingui-la da tabela da entidade.
