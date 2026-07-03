# Checklist de Seguranca — Modulos SEI

**Fontes de verdade deste checklist**:
- `.agents/references/gates-de-implementacao.md` — gates de bloqueio transversais
- `.agents/security/matriz-vulnerabilidades-sei.md` — vetores V01-V10
- skills de gate por artefato (`sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores`)

Use este checklist em revisoes de seguranca de PR, hardening de modulos e auditorias pontuais.
Para revisao de PR, usar a skill `sei-code-review-security`.
Este checklist tambem cobre os itens AppSec PHP `C1-C10`.
Para referencias de apoio desses itens, ver `.agents/security/origem-referencias-seguranca.md`.

## 0. Checklists Modulares

Este arquivo permanece como checklist umbrella. Para revisao por tema, usar tambem:

| Tema | Checklist modular | Fontes principais |
|---|---|---|
| Permissoes | `.agents/checklists/checklist-permissoes-sei.md` | `G3`, `G4`, `G8`, `G9`, `V01-V03` |
| RN e transacoes | `.agents/checklists/checklist-rn-transacoes-sei.md` | `T1-T5`, `V07` |
| Modelagem de dados | `.agents/checklists/checklist-modelagem-dados-sei.md` | `R1-R15`, `padrao-modelagem-dados.md` |
| DTO InfraPHP | `.agents/checklists/checklist-dto-infraphp-sei.md` | `B5`, `R1-R15` |
| BD, DDL e release | `.agents/checklists/checklist-bd-ddl-sei.md` | `B1-B6`, `R1-R6`, `V05` |

---

## 1. Checklist por Tipo de Demanda

### 1.1 Pagina / Formulario PHP (`*_lista.php`, `*_cadastro.php`)

| # | Item | Gate | Severidade se violado |
|---|------|------|-----------------------|
| P1 | `validarLink()` chamado no inicio da acao | G3 | BLOQUEANTE |
| P2 | `validarPermissao()` chamado apos `validarLink()` | G3 | BLOQUEANTE |
| P3 | Arquivos PHP compativeis com conversao Latin-1 e sem BOM | G1 | BLOQUEANTE |
| P4 | Links de acao gerados com `assinarLink()` | G4 | BLOQUEANTE |
| P5 | Evitar `$_REQUEST` em pagina | G5 | ALTA |
| P6 | `$_GET`/`$_POST` diretos exigem normalizacao explicita | G5 | ALTA |
| P7 | Renderizacao condicional de UI usa `verificarPermissao()` quando aplicavel | — | ALTA |
| P8 | Saida HTML via `PaginaSEI::tratarHTML()` quando aplicavel | G7 | ALTA |
| P9 | Evitar `innerHTML`/`document.write` inseguros | — | ALTA |
| P10 | Mutacao de estado via GET exige revisao | G9 | ALTA |

> **Nota P2 — qual variante de permissao usar**: acoes que alteram dados sensiveis, consultam
> CPF/CNPJ ou impactam processo/documento devem usar `validarAuditarPermissao($recurso, __METHOD__, $valores)`
> — gera trilha em `infra_auditoria`. Leitura simples: `validarPermissao` e suficiente.
> Para verificar sem lancar excecao: `verificarPermissao` (retorna bool).

> **Lint PHP**: `php -l` em todo PHP alterado continua obrigatorio via `sei-testes-validacao`
> e gate G2. Ele nao entra na numeracao P1-P10.

### 1.2 Acao AJAX / WebService em `*Integracao.php`

| # | Item | Severidade se violado |
|---|------|-----------------------|
| A1 | `processarControladorAjax*()` com dispatch explicito por acao | BLOQUEANTE |
| A2 | Cada acao AJAX valida permissao/autorizacao especifica antes de executar | BLOQUEANTE |
| A3 | `tratarLinkSemAssinatura()` com `preg_match` restritivo | BLOQUEANTE |
| A4 | `processarControladorWebServices()` com dispatch explicito por servico | BLOQUEANTE |
| A5 | Cada servico WS valida permissao/autorizacao especifica antes de executar | BLOQUEANTE |
| A6 | Payload de retorno sem dados sensiveis quando aplicavel | ALTA |
| A7 | URL arbitraria do usuario (redirect, fetch, iframe, link sem assinatura) validada por whitelist (scheme/host/path) e regex estrita; negar por padrao (SSRF/Open Redirect) | BLOQUEANTE |

### 1.3 Evento / Hook (`*Integracao extends SeiIntegracao`)

| # | Item | Severidade se violado |
|---|------|-----------------------|
| E1 | Sem efeito colateral irreversivel sem log de auditoria | ALTA |
| E2 | Efeitos colaterais (email, Solr, sistemas externos) fora da transacao | ALTA |
| E3 | Se houver acoplamento a internals do core, confirmar compatibilidade com as versoes suportadas do modulo; so reportar quando houver risco atual nao tratado ou alternativa publica claramente mais adequada no mesmo contexto | MEDIA |
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
| B1 | DDL usa tipos portaveis; evitar `AUTO_INCREMENT`, `IDENTITY` e `SERIAL` direto em tabela funcional, preservando a estrategia multi-SGBD de sequence prevista pelo manual quando aplicavel | BLOQUEANTE |
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

### 1.7 PHP / AppSec Transversal

| # | Item | Severidade se violado |
|---|------|-----------------------|
| C1 | Segredo real hardcoded em codigo, config ou script (`token`, senha, chave privada, connection string com credencial) | BLOQUEANTE |
| C2 | Segredo ou credencial sensivel exposto em log, stacktrace, URL, resposta HTTP ou comentario operacional | BLOQUEANTE |
| C3 | Execucao de comando (`exec`, `shell_exec`, `system`, `passthru`, `proc_open`, `popen`) com entrada controlavel ou sem allowlist clara | BLOQUEANTE |
| C4 | `unserialize()` ou desserializacao equivalente sobre dado externo, persistido sem integridade ou de origem nao confiavel | BLOQUEANTE |
| C5 | Leitura, escrita, `include`, `require` ou construcao de caminho com dado controlavel sem normalizacao e allowlist | ALTA |
| C6 | Upload sem validacao suficiente de tipo/extensao/tamanho/nome, sem rename seguro ou salvo em local publicamente executavel | ALTA |
| C7 | Parser XML/HTML configurado de forma a aceitar entidades externas ou recursos remotos quando houver dado nao confiavel | ALTA |
| C8 | URL controlavel usada para redirect, fetch, webhook, iframe, download ou chamada externa sem allowlist/validacao forte | ALTA |
| C9 | Token, nonce, segredo temporario ou identificador sensivel gerado com aleatoriedade fraca (`rand`, `mt_rand`, timestamp previsivel) | ALTA |
| C10 | Dependencia com vulnerabilidade conhecida e relevante ao contexto, quando houver manifesto ou relatorio confiavel disponivel | ALTA |

> **Notas C1-C10 — anti-falso-positivo**:
> - So reportar C1/C2 quando houver evidencia concreta de segredo real ou exposicao sensivel. Placeholder, fixture ou exemplo obviamente invalido nao conta.
> - C3 exige caminho de execucao plausivel e entrada realmente controlavel ou sem restricao suficiente.
> - C4 exige avaliar a origem do dado serializado. Serializacao interna e controlada, sem entrada externa, nao e achado por si so.
> - C5 e C8 exigem influencia real de dado externo ou configuracao nao confiavel.
> - C10 depende de evidencia existente no repositorio ou em relatorio disponivel ao revisor. A ausencia de ferramenta externa nao e achado.

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
| PR com nova pagina PHP ou acao | 1.1, 1.6, 1.7 + skill `sei-verificacao-pagina` |
| PR com nova acao AJAX no modulo | 1.2, 1.6, 1.7 + skill `sei-verificacao-controladores` |
| PR com novo evento em `*Integracao` | 1.3, 1.6, 1.7 + skill `sei-mod-api-eventos` |
| PR com nova operacao API/WS | 1.4, 1.6, 1.7 + skill `sei-mod-api-operacoes` |
| PR com mudanca em BD (DDL, DTO, BD) | 1.5, 1.7 + skill `sei-verificacao-banco-dados` |
| Hardening geral de modulo | Todas as secoes + skill `sei-guardrails-modulo` |
| Revisao de modulo completo | Todas as secoes + skill `sei-code-review-security` (escopo de modulo) |

---

## 4. Instrucoes de Uso para IA

Execute `sei-code-review-security`. Este checklist e a referencia de criterios,
severidades e itens `C1-C10` utilizados pela skill — nao e um protocolo de execucao
independente.
