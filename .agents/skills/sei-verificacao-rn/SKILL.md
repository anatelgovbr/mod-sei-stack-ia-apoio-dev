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

## Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| T1 | CRUD padronizado usa sufixo coerente | **Aviso** | `cadastrar/alterar/excluir` tendem a `Controlado`; `consultar/listar/contar` tendem a `Conectado` |
| T2 | inicializarObjInfraIBanco() implementado | **Erro** | RN estende InfraRN e retorna BancoSEI::getInstance() |
| T3 | RN nao chama BD de outra classe | **Erro** | Cada RN acessa apenas sua propria BD |
| T4 | Controle manual de conexao/transacao merece revisao | **Aviso** | `fecharConexao()`, `commitTransacao()` e similares exigem contexto claro |
| T5 | try/catch com `InfraException` e encadeamento de erro e recomendavel | **Aviso** | padrao recorrente nos exemplos do manual |
| T6 | `*Controlado` contem somente persistencia | **Erro** | e-mail, Solr, indexacao e integracao externa devem ocorrer em wrapper publico depois de todos os acessos de persistencia |
| A1 | Metodo de escrita usa recurso auditado compatível | **Erro** | o recurso inicia com `md_` e termina com o sufixo da operação de escrita |
| A2 | Wrapper publico de escrita sem verificacao | **Aviso** | revisar intencionalidade sem exigir sessao em helper `*Interno`, hook ou evento sem usuario |
| A3 | Leitura publica usa recurso `_listar` coerente | **Erro** | consultar/listar/contar usam recurso iniciado por `md_` e terminado em `_listar` |

## Observacao sobre sufixos

Aplicar T1 apenas a metodos CRUD padronizados. Nao inferir sufixo de qualquer
metodo legado por heuristica lexical ampla.

## Efeitos apos commit

O metodo `*Controlado` persiste e retorna. Um wrapper publico chama a operacao
transacional e somente depois de seu retorno envia e-mail, indexa no Solr ou
aciona integracao externa. Consulte `references/padroes-transacao.md` para o
exemplo completo.

O wrapper chama o nome público resolvido pela `InfraRN`. Chamar
`$this->algumaOperacaoControlado()` diretamente não comprova commit e bloqueia T6.

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
| 0 | PASS, com ao menos uma RN analisada |
| 1 | WARN, avisos presentes e zero erros |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

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
| Leitura (consultar/listar/contar) | `validarAuditarPermissao('md_xxx_listar', __METHOD__, $dto)` | recurso `listar`, nao entra na regra de auditoria |
| Helper interno (hook/evento) | nenhuma, sem sessao de usuario | nao aplicavel |

Ver `.agents/references/padrao-auditoria-sip-sei.md` para o padrao completo incluindo o script SIP.

---

## Testes

```bash
cd .agents/skills/sei-verificacao-rn && python3 -m unittest test_audit
```

12 testes sobre `audit.py`. O arquivo e independente de proposito: nao importa helper de
outra skill nem de pasta compartilhada. A duplicacao de andaime e o preco de a skill
poder ser levada inteira para outro lugar.

Dois deles garantem **fail closed**: entrada inexistente, incompativel, vazia, ou
elegivel da qual o parser nada extraiu, tem de devolver BLOCK. Detector falha verde, e
sem essa garantia o auditor passa por cima do que nao conseguiu ler e ninguem percebe.

O resto se divide em dois grupos. Um fixa que cada regra realmente barra, com o codigo
de saida e a linha certa. O outro impede falso positivo, e cada um desses e um caso que
ja aconteceu. Falso positivo importa porque auditor que grita a toa e desligado pela
equipe, e ai o gate para de proteger tudo, nao so o caso barulhento.
