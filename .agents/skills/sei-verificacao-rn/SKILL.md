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

## 7 Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| T1 | CRUD padronizado usa sufixo coerente | **Aviso** | `cadastrar/alterar/excluir` tendem a `Controlado`; `consultar/listar/contar` tendem a `Conectado` |
| T2 | inicializarObjInfraIBanco() implementado | **Erro** | RN estende InfraRN e retorna BancoSEI::getInstance() |
| T3 | RN nao chama BD de outra classe | **Erro** | Cada RN acessa apenas sua propria BD |
| T4 | Controle manual de conexao/transacao merece revisao | **Aviso** | `fecharConexao()`, `commitTransacao()` e similares exigem contexto claro |
| T5 | try/catch com `InfraException` e encadeamento de erro e recomendavel | **Aviso** | padrao recorrente nos exemplos do manual |
| A1 | Metodo de escrita usa `validarAuditarPermissao` | **Erro** | cadastrar/alterar/excluir com `validarPermissao` puro perde trilha de auditoria silenciosamente |
| A2 | Metodo de escrita sem verificacao de permissao | **Aviso** | ausencia total de check pode ser helper interno — revisar intencionalidade |

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
    {"nome": "consultarControlado", "esperado": "Conectado", "encontrado": "Controlado", "status": "AVISO"}
  ],
  "avisos": [
    {"codigo": "T001", "regra": "T1", "mensagem": "Metodo CRUD consultar usa sufixo Controlado; revisar expectativa Conectado"}
  ],
  "verdict": "WARN"
}
```

## Heuristica de classificacao

```python
CRUD_WRITE = ['cadastrar', 'alterar', 'excluir', 'desativar', 'reativar',
              'bloquear', 'incluir', 'remover']
CRUD_READ  = ['consultar', 'listar', 'contar']

# T1: analisa nome do metodo e corpo para inferir sufixo esperado
# A1/A2: analisa corpo do metodo em busca de validarAuditarPermissao / validarPermissao
```

## Padrao de permissao/auditoria esperado por tipo de operacao

| Tipo | Chamada obrigatoria | Recurso SIP esperado |
|------|--------------------|-----------------------|
| Escrita (cadastrar/alterar/excluir) | `validarAuditarPermissao('md_xxx_<acao>', __METHOD__, $dto)` | registrado na regra de auditoria do SIP |
| Leitura (consultar/listar/contar) | `validarAuditarPermissao('md_xxx_listar', __METHOD__, $dto)` | recurso `listar` — nao entra na regra de auditoria |
| Helper interno (hook/evento) | nenhuma — sem sessao de usuario | nao aplicavel |

Ver `.agents/references/padrao-auditoria-sip-sei.md` para o padrao completo incluindo o script SIP.
