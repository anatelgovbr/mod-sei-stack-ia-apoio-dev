# Checklist de Modelagem de Dados SEI

Checklist transversal para revisar modelagem de dados, naming, limites Oracle,
portabilidade multi-SGBD e impacto de release.

## Fontes de verdade

- `.agents/references/padrao-modelagem-dados.md`
- `.agents/references/padrao-scripts-release.md`
- `.agents/references/gates-de-implementacao.md` - `R1`, `R3`, `R5`, `R6`
- `.agents/skills/sei-verificacao-banco-dados/SKILL.md` - `DB01-DB15`

## Quando usar

- review de modelagem antes de implementar
- review de modulo completo
- auditoria de DTO, BD, DDL ou script de release

## Checklist operacional

| # | Item | Origem | Severidade |
|---|---|---|---|
| 1 | Nome de tabela segue o padrao do modulo e permanece dentro dos limites de tamanho | `DB01`, `DB03`, `DB15` | BLOQUEANTE |
| 2 | Relacionamento N:N usa tabela `md_<sigla>_rel_<a>_<b>` quando o conceito nao exigir nome proprio do dominio | `DB02` | BLOQUEANTE |
| 3 | Tabelas e colunas ficam em ate `26` caracteres; indices, FKs e sequences em ate `30` | `DB03`, `DB05`, `B3`, `B4` | BLOQUEANTE |
| 4 | PK, FK, AK e sequence seguem naming coerente e portavel | `DB04`, `DB05`, `DB07`, `DB10`, `DB11` | BLOQUEANTE/AVISO |
| 5 | Tipos SQL sao portaveis entre MySQL, SQL Server, Oracle e PostgreSQL | `DB08`, `B1` | BLOQUEANTE |
| 6 | FKs relevantes possuem indice explicito ou helper equivalente | `DB09` | AVISO |
| 7 | Tabelas e colunas possuem descricao negocial em `comment`; docblock em DTO e evidencia auxiliar local, nao substituto do metadado do banco | manual cap. 5 `Regras Gerais`, `DB12` | AVISO |
| 8 | Mudanca estrutural em modulo mapeado atualiza script existente, nao cria duplicata | `R1`, `R6` | BLOQUEANTE |
| 9 | `getVersao()` e scripts SEI/SIP ficam sincronizados quando ha impacto de release | `R3` | BLOQUEANTE |

## Recortes complementares

- Para `*DTO.php`: `checklist-dto-infraphp-sei.md`
- Para `*BD.php`, DDL e scripts: `checklist-bd-ddl-sei.md`
