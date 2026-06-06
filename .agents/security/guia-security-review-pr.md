# Guia de Revisao de Seguranca em Pull Requests — Modulos SEI

Este guia define quando acionar revisao de seguranca, quais skills executar,
o que registrar no PR e quando um item de seguranca bloqueia o merge.

**Fontes de referencia**:
- Gates: `.agents/references/implementation-gates.md`
- Vetores: `.agents/security/matriz-vulnerabilidades-sei.md`

---

## 1. Quando Acionar Revisao de Seguranca no PR

A tabela abaixo define os gatilhos. Uma demanda pode ter multiplos gatilhos ativos.

| Artefato alterado no PR | Skills de gate a executar | Revisao manual necessaria |
|------------------------|--------------------------|---------------------------|
| Nova pagina PHP (`*_lista.php`, `*_cadastro.php`) | `sei-verificacao-pagina` | Sim — verificar P1-P12 do checklist |
| Pagina PHP existente alterada | `sei-verificacao-pagina` | Sim — verificar P1, P2, P5, P8, P9 |
| Nova acao AJAX em `*Integracao.php` | `sei-verificacao-pagina` | Sim — verificar A1-A7 do checklist |
| Nova RN de escrita (`*RN.php`) | `sei-verificacao-rn` | Sim — verificar V07 (efeito colateral em transacao) |
| Novo BD ou DDL (`*BD.php`, script `.sql`) | `sei-verificacao-banco-dados` | Sim — verificar B1-B6 do checklist |
| Nova operacao API/WS | `sei-operacoes` | Sim — verificar W1-W5 do checklist |
| Mudanca em encoding de qualquer arquivo PHP | `sei-testes-validacao` (php -l) | Verificar G1 — encoding ISO-8859-1 |
| Hardening geral / revisao de modulo | `sei-guardrails-modulo` | Todos os vetores aplicaveis |

---

## 2. Como Registrar Resultado no PR

### 2.1 Resultado das skills de gate

Para cada skill executada, incluir no corpo do PR ou em comentario dedicado:

```
## Revisao de Seguranca

### sei-verificacao-pagina
Status: PASS / BLOCK
Evidencias: [link para output ou descricao inline]

### sei-verificacao-rn
Status: PASS / N/A
Motivo N/A: [ex.: "nenhuma escrita em BD neste PR"]

### sei-verificacao-banco-dados
Status: PASS / BLOCK
Evidencias: [link para output]
```

### 2.2 Achados encontrados

Para cada achado de seguranca encontrado na revisao manual, incluir:

```
### Achado [N] — [Titulo]
Severidade: BLOQUEANTE / ALTA / MEDIA / BAIXA
Arquivo: [arquivo:linha]
Descricao: [o que foi encontrado]
Status: [Corrigido neste PR / Issue #NNN registrada / Aceito como risco]
```

---

## 3. Criterios de Bloqueio de Merge

### Bloqueia o merge (obrigatorio antes de aprovar)

- Qualquer achado de severidade **BLOQUEANTE** nao resolvido.
- `php -l` com erro de sintaxe em qualquer arquivo PHP alterado (gate G2).
- Arquivo PHP em encoding UTF-8 (gate G1).
- Acao PHP sem `validarLink()` (gate G3, vetor V01).
- Acao PHP sem `validarPermissao()` (gate G3, vetor V02).
- Acao AJAX sem autorizacao por acao especifica (vetor V03).
- SQL concatenado com entrada do usuario (gate G6, vetor V05).
- Log com PII ou segredos (gate G8, vetor V10).

### Nao bloqueia merge — mas exige issue registrada

- Achado de severidade **ALTA** nao resolvido no PR.
- Deve haver issue vinculada com prazo definido antes da aprovacao.

### Nao bloqueia merge — registrar como debito tecnico

- Achados de severidade **MEDIA** ou **BAIXA**.
- Registrar em issue ou comentario de debito tecnico no PR.

---

## 4. Protocolo para IA

Quando a IA participar da revisao de seguranca de um PR:

1. Identificar todos os artefatos alterados no PR.
2. Para cada artefato, consultar a tabela da secao 1 e determinar quais gates aplicam.
3. Executar as skills de gate correspondentes.
4. Verificar os vetores de `matriz-vulnerabilidades-sei.md` para os tipos de artefato alterados.
5. Para cada violacao encontrada: registrar usando o formato da secao 2.2.
6. Classificar cada achado pela tabela de severidade de `matriz-vulnerabilidades-sei.md`.
7. Reportar resultado final:
   - Lista de gates executados e status (PASS / BLOCK / N/A).
   - Lista de achados com severidade e status.
   - Veredicto: "Liberado para merge" ou "Bloqueado — ver achados BLOQUEANTES".
8. Nunca classificar um achado como severidade menor para facilitar aprovacao.
9. Se houver duvida sobre severidade: classificar para cima, nao para baixo.

---

## 5. Revisao de Modulo Completo (fora de PR)

Para revisoes completas de modulo (nao vinculadas a um PR especifico):

1. Usar `template-security-review-modulo.md` para estruturar o documento.
2. Salvar resultado em `.agents/security/<modulo>-security-review.md`.
3. Registrar issues para cada achado BLOQUEANTE ou ALTA ainda nao resolvido.
4. Agendar revalidacao quando houver mudancas significativas no modulo.

**Modulos em producao sem revisao de seguranca registrada** (referencia: `PRD.md`):

| Modulo | Status |
|--------|--------|
| `peticionamento` | Revisao registrada em `peticionamento-security-review.md` |
| `relacionamento-institucional` | Sem revisao registrada |
| `litigioso` | Sem revisao registrada |
| `pesquisa` | Sem revisao registrada |
| `ia` | Sem revisao registrada |
| `correios` | Sem revisao registrada |
| `centraliza-modulos` | Sem revisao registrada |
| `utilidades` | Sem revisao registrada |

Usar `template-security-review-modulo.md` para criar as revisoes pendentes.
