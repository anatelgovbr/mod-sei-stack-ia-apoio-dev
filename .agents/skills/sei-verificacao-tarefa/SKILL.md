---
name: sei-verificacao-tarefa
description: |
  Audita o cadastro de tarefa de andamento de modulo SEI: `id_tarefa`
  numerico, `id_tarefa_modulo` textual, origem do id em `seq_tarefa` e
  sinalizadores S/N. Gate para script de release que cadastra tarefa
  (`TarefaDTO` ou `INSERT INTO tarefa`) e para definicao `*_tarefa.php`.

  Use quando:
  - Cadastro de tarefa criado ou alterado no script de release do modulo
  - Code review de tarefas de modulo
  - Gate automatico disparado por `sei-guardrails-modulo`
  - Pergunta como "valide as tarefas deste modulo" ou "check task IDs"
---

# sei-verificacao-tarefa

Skill de gate para validar o cadastro de tarefa de andamento de modulo SEI. Regra completa, exemplos e escolha dos sinalizadores: `references/padroes-tarefa.md`.

## Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| K1 | `id_tarefa` >= 1000 | **Erro** | Valor numerico >= 1000; no cadastro, a 65 tambem e erro |
| K2 | `id_tarefa` < 1000 reservado | **Erro** | Bloqueia valor menor que 1000 que nao seja o lancamento da 65 |
| K3 | Prefixo de `id_tarefa_modulo` | **Erro** | Texto segue `MD_<SIGLA>_<NOME>` em maiusculas |
| K4 | Maximo 50 caracteres | **Erro** | `id_tarefa_modulo` tem ate 50 caracteres |
| K6 | Unicidade nas duas dimensoes | **Erro** | Nao repete `id_tarefa` nem `id_tarefa_modulo` no modulo |
| K7 | Tarefa 65 so no lancamento, com DESCRICAO | **Erro** | Na definicao `*_tarefa.php`, a entrada 65 exige `DESCRICAO` nao vazio |
| K8 | Id por `seq_tarefa` ou com realinhamento | **Erro** | Id fixo ou calculado fora de `getValorSequencia('seq_tarefa')` exige realinhar `seq_tarefa` no arquivo |
| K9 | Cinco sinalizadores explicitos | **Erro** | Cadastro define os cinco `sin_*` da tabela `tarefa`, com `S` ou `N` quando literal |

## Ranges de ID

| Range | Uso | Exemplo |
|-------|-----|---------|
| ID < 1000 | Reservado para SEI core | 1-999 |
| ID = 65 | Tarefa do core; o modulo so lanca, com DESCRICAO | Atualizacao de andamento |
| ID >= 1000 | Livre para modulo | 1000+ |

## Exit codes (`--exit-code`)

| Code | Significado |
|------|-------------|
| 0 | PASS, com ao menos uma definicao analisada |
| 1 | WARN, avisos presentes e zero erros |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

## Uso

Rode sobre o script de release do modulo. O script do core, `atualizar_versao_sei.php`, cadastra tarefas abaixo de 1000 e fica fora do alvo. Em diretorio, o auditor le o primeiro nivel e analisa os arquivos que cadastram tarefa ou tem `tarefa` no nome.

```bash
# Script de release do modulo
python3 audit.py --input fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_<modulo>.php --format markdown

# Definicao *_tarefa.php
python3 audit.py --input md_ri_tarefa.php --format json
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
# Cadastro: TarefaDTO passado a cadastrar(); setters e unSetTodos() lidos em ordem ate a chamada
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa)
$objTarefaDTO->setStrIdTarefaModulo('MD_RI_RESTAURANTE_CADASTRAR')
$objTarefaRN->cadastrar($objTarefaDTO)

# Cadastro: cada tupla de INSERT; colunas literais ou em variavel (ultima atribuicao literal mais acrescimos .=)
INSERT INTO tarefa ($strCampos) VALUES (<valores>)

# Definicao *_tarefa.php
'id_tarefa' => 1001
'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR'
$objTarefaDTO->setNumIdTarefa(1001)
$objTarefaDTO->setStrIdTarefaModulo('MD_RI_RESTAURANTE_CADASTRAR')
```

O parser reconhece `array()` e `[]`. Devolvem BLOCK: `INSERT INTO tarefa` com lista de colunas ou de valores que o parser nao interpreta, inclusive lista alterada por expressao nao literal ou tupla seguinte nao lida, e `cadastrar(new TarefaDTO...)`. `TarefaDTO` guardado fora de variavel simples, como propriedade ou item de array, nao e lido: confira esse cadastro na revisao.

---

## Testes

```bash
cd .agents/skills/sei-verificacao-tarefa && python3 -m unittest test_audit
```

14 testes sobre `audit.py`. O arquivo e independente de proposito: nao importa helper de
outra skill nem de pasta compartilhada. A duplicacao de andaime e o preco de a skill
poder ser levada inteira para outro lugar.

Dois deles garantem **fail closed**: entrada inexistente, incompativel, vazia, ou
elegivel da qual o parser nada extraiu, tem de devolver BLOCK. Detector falha verde, e
sem essa garantia o auditor passa por cima do que nao conseguiu ler e ninguem percebe.

O resto se divide em dois grupos. Um fixa que cada regra realmente barra, com o codigo
de saida e a linha certa. O outro impede falso positivo, e cada um desses e um caso que
ja aconteceu. Falso positivo importa porque auditor que grita a toa e desligado pela
equipe, e ai o gate para de proteger tudo, nao so o caso barulhento.
