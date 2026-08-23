---
name: sei-verificacao-tarefa
description: |
  Audita os identificadores de tarefa de modulo SEI/SIP: `id_tarefa` numerico
  e `id_tarefa_modulo` textual. Valida range, excecao 65, prefixo, tamanho e
  unicidade. Gate para qualquer script de tarefa
  (*_tarefa.php) ou definicao de tarefas no modulo.

  Use quando:
  - Novo script de tarefa criado ou alterado
  - Code review de tarefas de modulo
  - Gate automatico disparado por `sei-guardrails-modulo`
  - Pergunta como "valide as tarefas deste modulo" ou "check task IDs"
---

# sei-verificacao-tarefa

Skill de gate para validar IDs de tarefa de modulo SEI/SIP.

## Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| K1 | `id_tarefa` >= 1000 | **Erro** | Valor numerico >= 1000, exceto ID=65 com atributo `DESCRICAO` |
| K2 | `id_tarefa` < 1000 reservado | **Erro** | Bloqueia valor menor que 1000 que nao seja 65 |
| K3 | Prefixo de `id_tarefa_modulo` | **Erro** | Texto segue `MD_<SIGLA>_<NOME>` em maiusculas |
| K4 | Maximo 50 caracteres | **Erro** | `id_tarefa_modulo` tem ate 50 caracteres |
| K6 | Unicidade nas duas dimensoes | **Erro** | Nao repete `id_tarefa` nem `id_tarefa_modulo` no modulo |
| K7 | ID=65 usado apenas com atributo DESCRICAO | **Erro** | Tarefa 65 e free-text andamentos, nao usar para outro fim |

## Ranges de ID

| Range | Uso | Exemplo |
|-------|-----|---------|
| ID < 1000 | Reservado para SEI core | 1-999 |
| ID = 65 | Livre para modulo (com DESCRICAO) | Tarefa free-text |
| ID >= 1000 | Livre para modulo | 1000+ |

## Exit codes (`--exit-code`)

| Code | Significado |
|------|-------------|
| 0 | PASS, com ao menos uma definicao analisada |
| 1 | WARN, avisos presentes e zero erros |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

## Uso

```bash
# Arquivo unico
python3 audit.py --input md_ri_tarefa.php --format markdown

# Diretorio scripts/
python3 audit.py --input fontes/sei/src/main/php/sei/scripts --format json

# Em todo o modulo
python3 audit.py --input web/modulos/relacionamento-institucional/scripts --format markdown
```

## Output JSON

```json
{
  "skill": "sei-verificacao-tarefa",
  "version": "1.0.0",
  "file": "md_ri_tarefa.php",
  "tarefas": [
    {"id": 1001, "nome": "MD_RI_RESTAURANTE_CADASTRAR", "status": "OK"},
    {"id": 65, "nome": "MD_RI_ANDAMENTO_LIVRE", "descr": true, "status": "OK (65 + DESCRICAO)"},
    {"id": 999, "nome": "MD_RI_TESTE", "status": "ERRO (ID < 1000)"}
  ],
  "erros": [
    {"codigo": "K001", "regra": "K1", "id": 999, "mensagem": "ID 999 < 1000, reservado para SEI core"}
  ],
  "verdict": "BLOCK"
}
```

## Parser patterns

```python
# Formatos reconhecidos
'id_tarefa' => 1001
'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR'
$objTarefaDTO->setNumIdTarefa(1001)
$objTarefaDTO->setStrIdTarefaModulo('MD_RI_RESTAURANTE_CADASTRAR')
```

O parser reconhece `array()` e `[]`.
