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
  - Refatoracao de RN, inclusive a revisao dela
  - Gate automatico disparado por `sei-guardrails-modulo`
  - Pergunta como "valide as transacoes desta RN" ou "check RN transaction"
---

# sei-verificacao-rn

Skill de gate para validar padroes de transacao em classes RN do SEI.

## Regras de auditoria

| ID | Regra | Severidade | O que verifica |
|----|-------|------------|----------------|
| T1 | CRUD padronizado usa sufixo coerente | **Aviso** | `cadastrar/alterar/excluir` tendem a `Controlado`; `consultar/listar/contar` tendem a `Conectado` |
| T2 | inicializarObjInfraIBanco() implementado | **Erro** | RN estende InfraRN e retorna BancoSEI::getInstance(); com herança indireta, o método vem da classe-mãe, e o `audit.py` bloqueia a classe cuja cadeia não chega à InfraRN |
| T3 | RN nao chama BD de outra classe | **Erro** | Cada RN acessa apenas sua propria BD |
| T4 | Controle manual de conexao/transacao merece revisao | **Aviso** | `fecharConexao()`, `commitTransacao()` e similares exigem contexto claro |
| T5 | try/catch com `InfraException` e encadeamento de erro e recomendavel | **Aviso** | padrao recorrente nos exemplos do manual |
| T6 | `*Controlado` contém somente persistência | **Erro** | E-mail, indexação no Solr e demais integrações externas são disparados após o commit. |
| A1 | Metodo de escrita usa recurso auditado compatível | **Erro** | o recurso inicia com `md_` e termina com o sufixo da operação de escrita; `bloquear` compartilha o recurso `_consultar`, porque o SIP não gera recurso `bloquear` |
| A2 | Wrapper publico de escrita sem verificacao | **Aviso** | revisar intencionalidade sem exigir sessao em helper `*Interno`, hook ou evento sem usuario |
| A3 | Leitura publica usa o recurso da operacao | **Erro** | `consultar` e `bloquear` usam recurso terminado em `_consultar`; `listar` e `contar` usam recurso terminado em `_listar`; todos iniciados por `md_` |
| T7 | `getIdConexao()` so testa conexao aberta | **Erro** | O retorno nunca vai para `mysqli_*`, `oci_*`, `pg_*` ou similar |
| T8 | Contrato do metodo com sufixo | **Erro** | Metodo `protected`, com um unico parametro (DTO ou array), chamado pelo nome publico sem sufixo |
| T9 | Uma transacao para o laco | **Erro** | Laco que chama operacao `Controlado` por item roda dentro de `Controlado`; lote que continua apos falha isolada justifica `Conectado` em comentario |
| T10 | Controle manual com estado auxiliar | **Aviso** | Abertura e fechamento manual pelo `BancoSEI` sabem se a conexao ou a transacao ja esta aberta |
| T11 | RN repete as validacoes da interface | **Erro** | Tamanho, obrigatoriedade e demais regras ja validadas na tela sao validadas tambem na RN |

O `audit.py` avalia T1 a T6 e A1 a A3. T7 a T12 sao revisao manual, com exemplos em `references/padroes-transacao.md`.

Na revisão manual de `bloquear`, `excluir`, `desativar` ou `reativar`, confira os chamadores, os DTOs e o limite da transação conforme os [contratos de bloqueio e lote](../../references/padrao-metodos-crud-infraphp.md#regras-por-metodo).

## Observacao sobre sufixos

Aplicar T1 apenas a metodos CRUD padronizados. Nao inferir sufixo de qualquer
metodo legado por heuristica lexical ampla.

## Efeitos apos commit

O wrapper chama a operação pelo nome público resolvido pela `InfraRN`. O fluxo que confirma o commit dispara o efeito externo, conforme a [regra T6](references/padroes-transacao.md#t6---efeitos-externos-somente-apos-o-retorno-transacional). Chamar `$this->algumaOperacaoControlado()` diretamente não comprova commit e bloqueia T6.

## Coluna derivada para busca textual (revisão complementar)

Quando a mudança afetar a coluna `idx_`, seus campos de origem ou sua consulta, aplique a [referência de busca textual](../../references/padrao-metodos-crud-infraphp.md#coluna-derivada-para-busca-textual). Confira se a escrita da coluna usa o estado completo e participa da mesma transação dos dados de origem. Atualizá-la após o commit é não conforme. Na consulta, verifique a montagem dos critérios e a preservação dos filtros do fluxo. Registre a evidência dos caminhos verificados além do resultado de `audit.py`.

## Refatoração

Escrita ou revisão de refatoração que extrai, move, divide ou renomeia método de RN aplica a T12 de `references/padroes-transacao.md`, com os limites de `*Controlado` e `*Conectado`. A verificação é manual: o `audit.py` não avalia a T12.

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
| Leitura (listar/contar) | `validarAuditarPermissao('md_xxx_listar', __METHOD__, $dto)` | recurso `listar`, nao entra na regra de auditoria |
| Leitura (consultar/bloquear) | `validarAuditarPermissao('md_xxx_consultar', __METHOD__, $dto)` | recurso `consultar`, nao entra na regra de auditoria; `bloquear` e `*Controlado` e compartilha o mesmo recurso |
| Helper interno (hook/evento) | nenhuma, sem sessao de usuario | nao aplicavel |

Ver `.agents/references/padrao-auditoria-sip-sei.md` para o padrao completo incluindo o script SIP.

---

## Testes

```bash
cd .agents/skills/sei-verificacao-rn && python3 -m unittest test_audit
```

Testes sobre `audit.py`. O arquivo e independente de proposito: nao importa helper de
outra skill nem de pasta compartilhada. A duplicacao de andaime e o preco de a skill
poder ser levada inteira para outro lugar.

Dois deles garantem **fail closed**: entrada inexistente, incompativel, vazia, ou
elegivel da qual o parser nada extraiu, tem de devolver BLOCK. Detector falha verde, e
sem essa garantia o auditor passa por cima do que nao conseguiu ler e ninguem percebe.

O resto se divide em dois grupos. Um fixa que cada regra realmente barra, com o codigo
de saida e a linha certa. O outro impede falso positivo, e cada um desses e um caso que
ja aconteceu. Falso positivo importa porque auditor que grita a toa e desligado pela
equipe, e ai o gate para de proteger tudo, nao so o caso barulhento.

## Dependências de registros do core

Confira dependências afetadas pela regra da RN, inclusive sem DDL, e os caminhos inversos de ativação. Aplicar, com `sei-guardrails-modulo`, a [matriz de proteção](../sei-mod-api-eventos/references/protecao-dependencias-core.md) também a protocolos e dependências funcionais sem FK.
