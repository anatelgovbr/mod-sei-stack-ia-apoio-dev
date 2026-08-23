# Checklist de DTO InfraPHP SEI

Checklist operacional para revisar `*DTO.php` em modulos SEI/SIP.

## Fontes de verdade

- `.agents/references/padrao-modelagem-dados.md` - secao `DTO, PK e FK`
- `.agents/skills/sei-verificacao-banco-dados/SKILL.md` - `DB01-DB15`
- `.agents/checklists/checklist-seguranca.md` - `B5`

## Quando usar

- novo `*DTO.php`
- alteracao de atributo, PK, FK ou relacionamento
- code review de DTO existente

## Checklist operacional

| # | Item | Origem | Severidade |
|---|---|---|---|
| 1 | `getStrNomeTabela()` reflete o nome real da tabela e respeita naming e tamanho | `DB01`, `DB03`, `DB15` | BLOQUEANTE |
| 2 | `configurarPK()` usa a PK correta e o tipo coerente com a estrategia de sequence | `DB04`, `DB10` | BLOQUEANTE/AVISO |
| 3 | Toda relacao local relevante tem `configurarFK()` explicito | `B5` | MEDIA |
| 4 | `adicionarAtributoTabelaRelacionada(...)` vem acompanhado da FK correspondente quando a relacao depende de join declarado pelo DTO | `B5` | MEDIA |
| 5 | `InfraDTO::$TIPO_FK_OBRIGATORIA` e `InfraDTO::$TIPO_FK_OPCIONAL` refletem a nulabilidade real | `padrao-modelagem-dados.md` secao `DTO, PK e FK` | MEDIA |
| 6 | DTO com exclusao logica declara `sin_ativo` de forma coerente | `DB06` | BLOQUEANTE |
| 7 | Docblock com `@table` e `@column` pode ser usado como evidencia auxiliar, mas nao substitui a descricao negocial em `comment` no modelo de dados | manual cap. 5 `Regras Gerais`, `DB12` | AVISO |
| 8 | DTO nao mascara problema estrutural de release; se o nome da tabela estoura limite ou exige novo objeto de banco, o script correspondente precisa refletir isso | `DB01`, `DB03`, `DB06` | BLOQUEANTE |

## Observacoes praticas

- `InfraDTO::$TIPO_PK_NATIVA` e o tipo correto para sequences `seq_<tabela>`.
- Atributo relacionado nao deve ser tratado como FK fisica local sem confirmar a
  modelagem real da tabela.
