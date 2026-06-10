# Checklist de Seguranca — Modulos SEI

**Fonte de verdade para este checklist**: `.agents/references/implementation-gates.md` (G1-G9).
**Skill de gate de pagina**: `sei-pagina-seguranca-check` (P1-P10).
**Skill de gate de RN**: `sei-rn-transacao-check` (T1-T5).
**Skill de gate de BD**: `sei-banco-dados-check` (R1-R15).

Use este checklist em revisoes de seguranca de PR, hardening de modulos e auditorias pontuais.
Para o protocolo completo de integracao com PR, ver `guia-security-review-pr.md`.

---

## 1. Checklist por Tipo de Demanda

### 1.1 Pagina / Formulario PHP (`*_lista.php`, `*_cadastro.php`)

| # | Item | Gate | Severidade se violado |
|---|------|------|-----------------------|
| P1 | `validarLink()` chamado no inicio da acao | G3 | BLOQUEANTE |
| P2 | `validarPermissao()` chamado apos `validarLink()` | G3 | BLOQUEANTE |
| P3 | Links de acao gerados com `assinarLink()` | G4 | BLOQUEANTE |
| P4 | Renderizacao condicional de UI usa `verificarPermissao()` quando aplicavel | — | ALTA |
| P5 | Evitar `$_REQUEST` em pagina | G5 | ALTA |
| P6 | `$_GET`/`$_POST` diretos exigem normalizacao explicita | G5 | ALTA |
| P7 | Saida HTML via `PaginaSEI::tratarHTML()` quando aplicavel | G10 | ALTA |
| P8 | Evitar `innerHTML`/`document.write` inseguros | — | ALTA |
| P9 | Mutacao de estado via GET exige revisao | G12 | ALTA |
| P10 | Arquivos PHP compativeis com conversao Latin-1 e sem BOM | G1 | BLOQUEANTE |
| P11 | `php -l` sem erros de sintaxe | G2 | BLOQUEANTE |

### 1.2 Acao AJAX (`processarControladorAjax`)

| # | Item | Severidade se violado |
|---|------|-----------------------|
| A1 | `processarControladorAjax*()` com dispatch explicito por acao | BLOQUEANTE |
| A2 | `tratarLinkSemAssinatura()` com `preg_match` restritivo | BLOQUEANTE |
| A3 | `processarControladorWebServices()` com dispatch explicito por servico | BLOQUEANTE |
| A4 | Payload de retorno sem dados sensiveis quando aplicavel | ALTA |

### 1.3 Evento / Hook (`*Integracao extends SeiIntegracao`)

| # | Item | Severidade se violado |
|---|------|-----------------------|
| E1 | Sem efeito colateral irreversivel sem log de auditoria | ALTA |
| E2 | Efeitos colaterais (email, Solr, sistemas externos) fora da transacao | ALTA |
| E3 | Sem acoplamento a internals do core quando existe API publica adequada | MEDIA |
| E4 | Excecoes do evento tratadas sem derrubar o fluxo principal do SEI | ALTA |
| E5 | Condicao de disparo documentada — sem efeito silencioso em toda acao do sistema | MEDIA |

### 1.4 API / WebService (`Entrada*API`, `Saida*API`, `SeiRN`)

| # | Item | Severidade se violado |
|---|------|-----------------------|
| W1 | Usar `Entrada*API` / `Saida*API` — evitar objetos internos sem justificativa | MEDIA |
| W2 | Autenticacao e autorizacao do chamador verificadas antes de qualquer operacao | BLOQUEANTE |
| W3 | Payload de entrada validado antes de chamar `SeiRN` | ALTA |
| W4 | Erros de negocio retornados com codigo semantico — sem exposicao de excecao interna | ALTA |
| W5 | Dados pessoais ou sensiveis nao incluidos na resposta alem do estritamente necessario | ALTA |

### 1.5 Banco de Dados (DDL, DTO, BD)

| # | Item | Severidade se violado |
|---|------|-----------------------|
| B1 | DDL usa tipos portaveis (sem `AUTO_INCREMENT`, `IDENTITY`, `SERIAL` direto) | BLOQUEANTE |
| B2 | Sequences criadas com `criarSequencialNativa` | ALTA |
| B3 | Nomes de tabelas e colunas com ate 26 caracteres (limite Oracle) | BLOQUEANTE |
| B4 | Nomes de indices, FKs e sequences com ate 30 caracteres | BLOQUEANTE |
| B5 | `configurarFK()` explicito para toda `adicionarAtributoTabelaRelacionada()` | MEDIA |
| B6 | SQL dinamico sem concatenacao de entrada do usuario | BLOQUEANTE |

### 1.6 Logs e Auditoria

| # | Item | Severidade se violado |
|---|------|-----------------------|
| L1 | Logs sem PII (dados pessoais, CPF, email, telefone) | ALTA |
| L2 | Logs sem segredos (tokens, senhas, chaves) | BLOQUEANTE |
| L3 | Operacoes criticas registradas com trilha de auditoria via `validarAuditarPermissao` | ALTA |
| L4 | `InfraDebug` desligado em producao | ALTA |

---

## 2. Criterios de Severidade

| Nivel | Definicao | Acao requerida |
|-------|-----------|----------------|
| **BLOQUEANTE** | Viola autenticacao, autorizacao, expoe dados sensiveis ou quebra integridade. | Corrigir antes do merge. PR nao pode ser aprovado com item BLOQUEANTE aberto. |
| **ALTA** | Risco real de exploracao ou violacao de padrao critico. Nao e bloqueante imediato mas e urgente. | Corrigir antes da entrega ou registrar issue com prazo definido. |
| **MEDIA** | Viola padrao do projeto mas sem risco direto de exploracao no contexto atual. | Registrar issue e corrigir na proxima sprint. |
| **BAIXA** | Melhoria de qualidade ou boa pratica nao aplicada. Sem risco imediato. | Registrar como debito tecnico. Corrigir quando conveniente. |

---

## 3. Gatilhos — Quando Usar Este Checklist

| Situacao | Secoes aplicaveis |
|----------|-------------------|
| PR com nova pagina PHP ou acao | 1.1, 1.6 + skill `sei-pagina-seguranca-check` |
| PR com nova acao AJAX no modulo | 1.2, 1.6 + skill `sei-controladores-integracao-check` |
| PR com novo evento em `*Integracao` | 1.3, 1.6 + skill `sei-mod-eventos` |
| PR com nova operacao API/WS | 1.4, 1.6 + skill `sei-mod-operacoes` |
| PR com mudanca em BD (DDL, DTO, BD) | 1.5 + skill `sei-banco-dados-check` |
| Hardening geral de modulo | Todas as secoes + skill `sei-modulo-guardrails` |
| Revisao de modulo completo | Todas as secoes + `template-security-review-modulo.md` |

---

## 4. Instrucoes de Uso para IA

Ao receber demanda de hardening ou validacao de seguranca:

1. Identificar o tipo de artefato sendo criado ou alterado (pagina, AJAX, evento, API, BD).
2. Aplicar as secoes correspondentes do checklist acima.
3. Para cada item violado: registrar a severidade, a evidencia (arquivo:linha) e a recomendacao de correcao.
4. Acionar a skill de gate correspondente para validacao automatizada quando disponivel.
5. Relatar resultado usando o formato de achados de `template-security-review-modulo.md`.
6. Itens BLOQUEANTES devem ser corrigidos antes de qualquer entrega.
7. Nunca inventar padrao nao documentado aqui ou em `implementation-gates.md`.
