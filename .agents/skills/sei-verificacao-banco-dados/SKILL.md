---
name: sei-verificacao-banco-dados
description: >
  Audita modelagem de dados de módulos SEI/SIP contra os padrões dos manuais
  TRF4. Aceita código PHP existente (DTOs, BDs), DDLs SQL ou diretórios de módulo
  inteiros como entrada. Não depende de contratos JSON — analiza artefatos brutos.
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
| R1 | Nome tabela `md_<sigla>_<entidade>` | Erro | §Tabela |
| R2 | N:N: `md_<sigla>_rel_<a>_<b>` | Erro | §Tabela |
| R3 | Tamanho ≤ 26 chars | Erro | §Regras Gerais |
| R4 | PK gerada `id_md_<sigla>_<entidade>` | Erro | §Colunas |
| R5 | FK `fk_md_<sigla>_<ent>_<ref>` | Erro | §Chave Estrangeira |
| R6 | `sin_ativo` em exclusão lógica | Erro | §Colunas |
| R7 | PK constraint `pk_<nome>` | Erro | §Chave Primária |
| R8 | Tipos SQL-99 (sem money/text) | Erro | §Tipos de Dados |
| R9 | Índice em FK | Aviso | §Índices |
| R10 | Sequence `seq_<nome>` | Aviso | §Sequências |
| R11 | AK constraint `ak_<nome>_<campos>` | Aviso | §Chave Alternativa |
| R12 | COMMENT ON / docblock | Aviso | §Regras Gerais |
| R13 | Sem verbos | Aviso | §Tabela |
| R14 | Singular | Aviso | §Regras Gerais |
| R15 | Formato minúsculas + sublinhado | Aviso | §Regras Gerais |

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

## Output

### Markdown (human-readable)

```
 sei-verificacao-banco-dados v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 md_ri_restaurante
   ✗ E006 — R6
     Exclusao logica sem coluna sin_ativo.
     Remedio: adicionar sin_ativo char(1) default 'S'

   ⚠ W004 — R12
     DTO sem docblock com @table/@column descritivos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESUMO
  Entidades auditadas: 4
  Erros (bloqueantes): 1  |  Avisos: 3
  Nota de conformidade: 82/100
  Veredito: BLOCK — Corrija erros antes de prosseguir.
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
      "erros": [{"codigo": "E006", "regra": 6, "mensagem": "...", "remedio": "..."}],
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
| 0 | PASS — sem erros e sem avisos |
| 1 | WARN — avisos presentes, zero erros |
| 2 | BLOCK — erros presentes |

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

O parser extrai de BDs:
- `fk_md_...` → constraints de FK
- `pk_md_...` → constraint de PK
- `ak_md_...` → constraints AK/unique
- `InfraSequencia` → uso de sequences

## Integration

Skill agnóstica — pode ser chamada por:
- `code-review` (auditoria de código existente)
- `sei-gerador-crud` (gate pré-geração opcional)
- `sei-gerador-scripts-release` (verificacao pre-release SEI)
- `sip-gerador-scripts-release` (verificacao pre-release SIP, quando houver DDL)
- `sei-eventos` (validação de modelo)
- Qualquer prompt ou agente que precise auditar modelagem

## Modos de auditoria

| Modo | Uso |
|------|-----|
| `adhoc` | Default — qualquer verificação pontual |
| `pre_generate` | Antes de gerar CRUD (validar контракт) |
| `audit` | Auditoria de módulo existente |
| `release_check` | Verificação pre-release de scripts |

Use `--mode <modo>` para selecionar.
