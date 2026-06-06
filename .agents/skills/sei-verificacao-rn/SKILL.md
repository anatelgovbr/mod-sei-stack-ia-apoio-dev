---
name: sei-verificacao-rn
description: >
  Audita classes RN (Regras de Negocio) SEI/SIP quanto a padroes de
  transacao e separacao de camadas com foco no que tem base mais forte no
  manual: implementacao de inicializarObjInfraIBanco(), isolamento de BD por RN
  e avisos contextuais sobre nomenclatura CRUD e controle manual. Gate
  obrigatorio para qualquer
  arquivo *RN.php.

  Use quando:
  - Novo RN criado ou alterado no modulo
  - Code review de RN existente
  - Gate automatico disparado por `sei-guardrails-modulo`
  - Pergunta como "valide as transacoes desta RN" ou "check RN transaction"
---

# sei-verificacao-rn

Skill de gate para validar padroes de transacao em classes RN do SEI.

## 5 Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| T1 | CRUD padronizado usa sufixo coerente | **Aviso** | `cadastrar/alterar/excluir` tendem a `Controlado`; `consultar/listar/contar` tendem a `Conectado` |
| T2 | inicializarObjInfraIBanco() implementado | **Erro** | RN estende InfraRN e retorna BancoSEI::getInstance() |
| T3 | RN nao chama BD de outra classe | **Erro** | Cada RN acessa apenas sua propria BD |
| T4 | Controle manual de conexao/transacao merece revisao | **Aviso** | `fecharConexao()`, `commitTransacao()` e similares exigem contexto claro |
| T5 | RN nao chama BD de outra classe | **Erro** | Cada RN acessa apenas sua propria BD |
| T5 | try/catch com `InfraException` e encadeamento de erro e recomendavel | **Aviso** | padrao recorrente nos exemplos do manual |

## Observacao sobre sufixos

Aplicar T1 apenas a metodos CRUD padronizados. Nao inferir sufixo de qualquer
metodo legado por heuristica lexical ampla.

## Inicializacao correta

```php
class MdRiRestauranteRN extends InfraRN {

    protected function inicializarObjInfraIBanco() {
        return BancoSEI::getInstance();
    }
}
```

## Exit codes (`--exit-code`)

| Code | Significado |
|------|-------------|
| 0 | PASS — todas as regras conformes |
| 1 | WARN — avisos presentes, zero erros |
| 2 | BLOCK — erros presentes |

## Uso

```bash
# Arquivo unico
python3 audit.py --input MdRiRestauranteRN.php --format markdown

# Diretorio rn/
python3 audit.py --input web/modulos/relacionamento-institucional/rn --format json
```

## Output JSON

```json
{
  "skill": "sei-verificacao-rn",
  "version": "1.0.0",
  "file": "MdRiRestauranteRN.php",
  "metodos": [
    {"nome": "cadastrarControlado", "esperado": "Controlado", "encontrado": "Controlado", "status": "OK"},
    {"nome": "consultarConectado", "esperado": "Conectado", "encontrado": "Controlado", "status": "ERRO"}
  ],
  "erros": [
    {"codigo": "T001", "regra": "T1", "mensagem": "consultar() usa sufixo Controlado mas deveria usar Conectado (operacao read)"}
  ],
  "verdict": "BLOCK"
}
```

## Heuristica de clasificacao

```python
WRITE_KEYWORDS = ['cadastrar', 'alterar', 'excluir', 'desativar', 'reativar',
                  'bloquear', 'incluir', 'remover', 'atualizar', 'gerar']
READ_KEYWORDS = ['consultar', 'listar', 'contar', 'buscar', 'verificar', 'recuperar']

# Analisa nome do metodo e corpo para inferir tipo de operacao
# write operation →espera sufixo Controlado
# read operation →espera sufixo Conectado
```
