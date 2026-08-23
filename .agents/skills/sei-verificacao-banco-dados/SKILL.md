---
name: sei-verificacao-banco-dados
description: >
  Audita modelagem de dados de módulos SEI/SIP contra os padrões dos manuais
  TRF4. Aceita código PHP existente (DTOs, BDs), DDLs SQL ou diretórios de módulo
  inteiros como entrada. Não depende de contratos JSON; analiza artefatos brutos.
  Pode ser chamada por qualquer skill, prompt ou agente.

  Use quando:
  - Code review de módulo SEI existente (DTO/BD)
  - Auditoria de scripts DDL antes de release
  - Verificação de modelagem antes de implementar feature
  - Pergunta direta como "audite a modelagem do módulo restaurante"
  - Quando mencionar auditar/verificar/revisar modelagem de dados
---

# sei-verificacao-banco-dados

Skill autônoma de code review para modelagem de dados SEI/SIP.

## Como funciona

1. **Parse**: extrai estrutura de dados de PHP (DTO/BD) ou SQL (DDL)
2. **Valida**: verifica cada entidade contra as 15 regras dos manuais TRF4
3. **Reporta**: retorna erros (bloqueantes) e avisos (informativos)

## Regras de auditoria

| ID | Regra | Sev | Base |
|----|-------|-----|------|
| DB01 | Nome tabela `md_<sigla>_<entidade>` | Erro | §Tabela |
| DB02 | N:N: `md_<sigla>_rel_<a>_<b>` | Erro | §Tabela |
| DB03 | Tamanho: tabela/coluna ≤ 26 chars; índice/FK/constraint/sequence ≤ 30 chars | Erro | §Regras Gerais |
| DB04 | PK simples com geração automática usa exatamente `id_<tabela>` | Erro | §Colunas |
| DB05 | Constraint FK em snake_case identifica proprietária e referência | Erro | §Chave Estrangeira |
| DB06 | `sin_ativo` em exclusão lógica | Erro | §Colunas |
| DB07 | PK constraint `pk_<nome>` | Erro | §Chave Primária |
| DB08 | Tipos SQL-99 e nomes SQL relacionados em snake_case | Erro | §Tipos de Dados |
| DB09 | Índice em FK | Aviso | §Índices |
| DB10 | Sequence `seq_<nome>` | Aviso | §Sequências |
| DB11 | AK constraint `ak_<nome>_<campos>` | Aviso | §Chave Alternativa |
| DB12 | COMMENT ON / docblock | Aviso | §Regras Gerais |
| DB13 | Sem verbos | Aviso | §Tabela |
| DB14 | Singular | Aviso | §Regras Gerais |
| DB15 | Formato minúsculas + sublinhado | Aviso | §Regras Gerais |

**Erro** = bloqueante (impede conformidade)
**Aviso** = informativo (não bloqueia mas indica desvio)

## Input

Aceita os seguintes formatos:
- **Arquivo PHP único** (DTO ou BD): `--input dto/MdRiRestauranteDTO.php`
- **Múltiplos arquivos**: `--input dto/A.php,bd/A.php`
- **Diretório de módulo** (escaneia dto/ e bd/): `--input web/modulos/relacionamento-institucional`
- **DDL raw**: `--input "CREATE TABLE md_ri_restaurante..."`
- **Arquivo SQL**: `--input tabela.sql`

Para forçar tipo: `--type php` ou `--type sql`

Scripts incrementais sem `CREATE TABLE` são elegíveis quando contêm
`ALTER TABLE`, `adicionarColuna`, chaves, índices ou sequences. Helpers com
`array()` e `[]` são equivalentes. Tabelas temporárias declaradas no próprio
script são ignoradas. Um arquivo `*BD.php` isolado também é aceito.
Quando DTO e BD descrevem a mesma tabela, as evidências são mescladas antes da validação.

## Output

### Markdown (human-readable)

```
 sei-verificacao-banco-dados v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 md_ri_restaurante
   ✗ E006 - DB06
     Exclusao logica sem coluna sin_ativo.
     Remedio: adicionar sin_ativo char(1) default 'S'

   ⚠ W004 - DB12
     DTO sem docblock com @table/@column descritivos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESUMO
  Entidades auditadas: 4
  Erros (bloqueantes): 1  |  Avisos: 3
  Nota de conformidade: 82/100
  Veredito: BLOCK, corrija erros antes de prosseguir.
```

### JSON (máquina)

```json
{
  "skill": "sei-verificacao-banco-dados",
  "version": "1.0.0",
  "timestamp": "2026-04-29T...",
  "input": { "type": "directory", "path": "...", "mode": "adhoc" },
  "results": [
    {
      "entidade": "md_ri_restaurante",
      "arquivos": ["MdRiRestauranteDTO.php"],
      "erros": [{"codigo": "E006", "regra": "DB06", "mensagem": "...", "remedio": "...", "arquivo": "MdRiRestauranteDTO.php", "linha": 20}],
      "avisos": [],
      "status": "BLOCK"
    }
  ],
  "stats": { "entidades": 4, "erros": 1, "avisos": 3, "nota": 82 },
  "verdict": "BLOCK"
}
```

## Exit codes (`--exit-code`)

| Code | Significado |
|------|-------------|
| 0 | PASS, com ao menos uma entidade analisada |
| 1 | WARN, avisos presentes e zero erros |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

## Uso

```bash
# diretório de DTOs (módulo completo)
python3 audit.py --input fontes/sei/src/main/php/sei/web/modulos/relacionamento-institucional/dto --format markdown

# arquivo único
python3 audit.py --input dto/MdRiRestauranteDTO.php --format json

# com exit code
python3 audit.py --input dto/ --format json --exit-code

# forçar tipo SQL
python3 audit.py --input "CREATE TABLE md_ri_teste..." --type sql --format markdown
```

## Parsing PHP (InfraPHP)

O parser extrai de DTOs:
- `getStrNomeTabela()` → nome da tabela
- `adicionarAtributoTabela($pref, $nome, $campoSql)` → colunas
- `configurarPK($attr, $tipo)` → tipo SEQUENCIAL/NATIVA/INFORMADO
- `configurarFK($attr, $tabela, $campo)` → FK
- `configurarExclusaoLogica($attr, $valor)` → presença de sin_ativo
- `adicionarAtributoTabelaRelacionada(...)` → colunas de join

Todo erro ou aviso estrutural inclui `arquivo` e `linha` da evidência analisada.

O parser extrai de BDs:
- `fk_md_...` → constraints de FK
- `pk_md_...` → constraint de PK
- `ak_md_...` → constraints AK/unique
- `InfraSequencia` → uso de sequences

## Integration

Skill agnóstica, pode ser chamada por:
- `sei-revisao-tecnica` (gate de modelagem em revisoes tecnicas)
- `sei-gerador-crud` (gate pré-geração opcional)
- `sei-gerador-scripts-release` (verificacao pre-release SEI)
- `sip-gerador-scripts-release` (verificacao pre-release SIP, quando houver DDL)
- `sei-mod-api-eventos` (validação de modelo)
- Qualquer prompt ou agente que precise auditar modelagem

## Modos de auditoria

| Modo | Uso |
|------|-----|
| `adhoc` | Default, qualquer verificação pontual |
| `pre_generate` | Antes de gerar CRUD (validar контракт) |
| `audit` | Auditoria de módulo existente |
| `release_check` | Verificação somente da modelagem presente nos scripts de release |

Use `--mode <modo>` para selecionar.

`release_check` não valida versão, sincronismo SEI/SIP ou `*Integracao.php`.
Essas dimensões pertencem à coordenação de release.
