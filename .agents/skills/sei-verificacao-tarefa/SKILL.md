---
name: sei-verificacao-tarefa
description: |
  Audita IDs de tarefa de modulo SEI/SIP (id_tarefa_modulo) quanto a
  padroes do manual: range maior ou igual a 1000 (exceto 65), prefixo MD_sigla_modulo,
  max 50 caracteres, e unicidade. Gate para qualquer script de tarefa
  (*_tarefa.php) ou definicao de tarefas no modulo.

  Use quando:
  - Novo script de tarefa criado ou alterado
  - Code review de tarefas de modulo
  - Gate automatico disparado por `sei-guardrails-modulo`
  - Pergunta como "valide as tarefas deste modulo" ou "check task IDs"
---

# sei-verificacao-tarefa

Skill de gate para validar IDs de tarefa de modulo SEI/SIP.

## 7 Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| K1 | ID >= 1000 | **Erro** | Valor numerico >= 1000, exceto ID=65 com atributo DESCRICAO |
| K2 | ID < 1000 reservado | **Erro** | Alerta se encontrar ID < 1000 que nao seja 65 |
| K3 | Prefixo MD_sigla_modulo em maiusculas | **Erro** | Nome segue padrao: MD_RI_RESTAURANTE_CADASTRAR |
| K4 | Maximo 50 caracteres no nome | **Erro** | strlen(nome) <= 50 |
| K5 | Tabela de tarefas existe com definicao | **Aviso** | Tarefa registrada na tabela md_<sigla>_tarefa |
| K6 | ID nao conflita com mesma tarefa no modulo | **Aviso** | Duplicidade de ID no modulo |
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
| 0 | PASS — todas as regras conformes |
| 1 | WARN — avisos presentes, zero erros |
| 2 | BLOCK — erros presentes |

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
    {"id": 65, "nome": "MD_RI_ANDAMENTO_LIVRE", "descr": "Andamentos livres", "status": "OK (65 + DESCRICAO)"},
    {"id": 999, "nome": "MD_RI_TESTE", "status": "ERRO (ID < 1000)"}
  ],
  "erros": [
    {"codigo": "K001", "regra": "K1", "id": 999, "mensagem": "ID 999 < 1000 — reservado para SEI core"}
  ],
  "verdict": "BLOCK"
}
```

## Parser patterns

```python
# Extrai definicoes de tarefa do arquivo PHP
re.findall(r"['\"]?(\d+)['\"]?\s*=>\s*['\"](MD_\w+)['\"]", content)
re.findall(r"['\"]?(\d+)['\"]?\s*,\s*['\"]([^'\"]+)['\"]", content)
re.findall(r"(\d+)\s*=>\s*array\s*\(\s*['\"]id_tarefa['\"]\s*=>\s*(\d+)", content)
```
