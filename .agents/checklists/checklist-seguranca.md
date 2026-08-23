# Checklist de Seguranca para Modulos SEI

**Fontes de verdade deste checklist**:
- `.agents/references/gates-de-implementacao.md`: gates de bloqueio transversais
- `.agents/security/matriz-vulnerabilidades-sei.md`: vetores V01-V10
- skills de gate por artefato (`sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores`)

Use este checklist em revisoes de seguranca de PR, hardening de modulos e auditorias pontuais.
Para revisao tecnica ou de seguranca de PR, usar a skill `sei-revisao-tecnica`.
Este checklist tambem cobre os itens AppSec PHP `C1-C10`.
Para referencias de apoio desses itens, ver `.agents/security/origem-referencias-seguranca.md`.

## Estado do gate e severidade do risco

Severidade e estado sao dimensoes independentes. `BLOQUEANTE`, `ALTA`, `MEDIA` e
`BAIXA` qualificam o impacto do risco. `PASS`, `WARN` e `BLOCK` registram o
resultado do gate. Toda violacao confirmada de gate bloqueante retorna `BLOCK`,
mesmo quando a severidade do risco for `ALTA`. Heuristica inconclusiva permanece
`WARN`, e `PASS` exige cobertura positiva do artefato.

## 0. Checklists Modulares

Este arquivo permanece como checklist umbrella. Para revisao por tema, usar tambem:

| Tema | Checklist modular | Fontes principais |
|---|---|---|
| Permissoes | `.agents/checklists/checklist-permissoes-sei.md` | `G3`, `G4`, `G8`, `G9`, `V01-V03` |
| RN e transacoes | `.agents/checklists/checklist-rn-transacoes-sei.md` | `T1-T6`, `V07` |
| Modelagem de dados | `.agents/checklists/checklist-modelagem-dados-sei.md` | `DB01-DB15`, `padrao-modelagem-dados.md` |
| DTO InfraPHP | `.agents/checklists/checklist-dto-infraphp-sei.md` | `B5`, `DB01-DB15` |
| BD, DDL e release | `.agents/checklists/checklist-bd-ddl-sei.md` | `B1-B6`, `DB01-DB15`, `R1/R3-R6`, `V05` |

---

## 1. Checklist por Tipo de Demanda

### 1.1 Pagina / Formulario PHP (`*_lista.php`, `*_cadastro.php`)

| # | Item | Gate | Estado quando confirmado | Severidade do risco |
|---|------|------|--------------------------|---------------------|
| P1 | `validarLink()` chamado no inicio da acao | G3 | `BLOCK` | BLOQUEANTE |
| P2 | `validarPermissao()` chamado apos `validarLink()` | G3 | `BLOCK` | BLOQUEANTE |
| P3 | Arquivos PHP compativeis com conversao Latin-1 e sem BOM | G1 | `BLOCK` | BLOQUEANTE |
| P4 | Links de acao gerados com `assinarLink()` | G4 | `BLOCK` | BLOQUEANTE |
| P5 | Uso confirmado de `$_REQUEST` em pagina | G5 | `BLOCK` | ALTA |
| P6 | Uso direto de `$_GET`/`$_POST` sem normalizacao explicita | G5 | `BLOCK` | ALTA |
| P7 | Renderizacao condicional de UI usa `verificarPermissao()` quando aplicavel | Contextual | `WARN` | ALTA |
| P8 | Saida HTML dinamica sem `PaginaSEI::tratarHTML()` ou tratamento documentado | G7 | `BLOCK` | ALTA |
| P9 | Fonte dinamica alcanca `innerHTML`/`document.write` ou sink equivalente sem tratamento | G7 | `BLOCK` | ALTA |
| P10 | Mutacao de estado confirmada via GET | G9 | `BLOCK` | ALTA |

P7 permanece contextual e retorna `WARN` quando isolado. Se a mesma evidencia
confirmar execucao nao autorizada, aplica-se o gate de autorizacao correspondente
e o resultado passa a `BLOCK`.

> **Nota P2, qual variante de permissao usar**: acoes que alteram dados sensiveis, consultam
> CPF/CNPJ ou impactam processo/documento devem usar `validarAuditarPermissao($recurso, __METHOD__, $valores)`
> para gerar trilha em `infra_auditoria`. Leitura simples: `validarPermissao` e suficiente.
> Para verificar sem lancar excecao: `verificarPermissao` (retorna bool).

> **Lint PHP**: `php -l` em todo PHP alterado continua obrigatorio via `sei-testes-validacao`
> e gate G2. Ele nao entra na numeracao P1-P10.

### 1.2 Acao AJAX / WebService em `*Integracao.php`

| # | Item | Severidade do risco |
|---|------|-----------------------|
| A1 | `processarControladorAjax*()` com dispatch explicito por acao | BLOQUEANTE |
| A2 | Cada acao AJAX valida permissao/autorizacao especifica antes de executar | BLOQUEANTE |
| A3 | `tratarLinkSemAssinatura()` com `preg_match` restritivo | BLOQUEANTE |
| A4 | `processarControladorWebServices()` com dispatch explicito por servico | BLOQUEANTE |
| A5 | Cada servico WS valida permissao/autorizacao especifica antes de executar | BLOQUEANTE |
| A6 | Payload de retorno sem dados sensiveis quando aplicavel | ALTA |
| A7 | URL arbitraria do usuario (redirect, fetch, iframe, link sem assinatura) validada por whitelist (scheme/host/path) e regex estrita; negar por padrao (SSRF/Open Redirect) | BLOQUEANTE |

### 1.3 Evento / Hook (`*Integracao extends SeiIntegracao`)

| # | Item | Severidade do risco |
|---|------|-----------------------|
| E1 | Sem efeito colateral irreversivel sem log de auditoria | ALTA |
| E2 | Efeitos colaterais (email, Solr, sistemas externos) no wrapper publico somente apos o retorno de `*Controlado`; `*Controlado` contem apenas persistencia | ALTA |
| E3 | Se houver acoplamento a internals do core, confirmar compatibilidade com as versoes suportadas do modulo; so reportar quando houver risco atual nao tratado ou alternativa publica claramente mais adequada no mesmo contexto | MEDIA |
| E4 | Excecoes do evento tratadas sem derrubar o fluxo principal do SEI | ALTA |
| E5 | Condicao de disparo documentada, sem efeito silencioso em toda acao do sistema | MEDIA |

### 1.4 API / WebService (`Entrada*API`, `Saida*API`, `SeiRN`)

| # | Item | Severidade do risco |
|---|------|-----------------------|
| W1 | Usar `Entrada*API` / `Saida*API`; evitar objetos internos sem justificativa | MEDIA |
| W2 | Autenticacao e autorizacao do chamador verificadas antes de qualquer operacao | BLOQUEANTE |
| W3 | Payload de entrada validado antes de chamar `SeiRN` | ALTA |
| W4 | Erros de negocio retornados com codigo semantico, sem exposicao de excecao interna | ALTA |
| W5 | Dados pessoais ou sensiveis nao incluidos na resposta alem do estritamente necessario | ALTA |

### 1.5 Banco de Dados (DDL, DTO, BD)

| # | Item | Severidade do risco |
|---|------|-----------------------|
| B1 | DDL usa tipos portaveis; evitar `AUTO_INCREMENT`, `IDENTITY` e `SERIAL` direto em tabela funcional, preservando a estrategia multi-SGBD de sequence prevista pelo manual quando aplicavel | BLOQUEANTE |
| B2 | Sequences criadas com `criarSequencialNativa` | ALTA |
| B3 | Nomes de tabelas e colunas com ate 26 caracteres (limite Oracle) | BLOQUEANTE |
| B4 | Nomes de indices, FKs e sequences com ate 30 caracteres | BLOQUEANTE |
| B5 | `configurarFK()` explicito para toda `adicionarAtributoTabelaRelacionada()` | MEDIA |
| B6 | SQL dinamico sem concatenacao de entrada do usuario | BLOQUEANTE |

### 1.6 Logs e Auditoria

| # | Item | Severidade do risco |
|---|------|-----------------------|
| L1 | Logs sem PII (dados pessoais, CPF, email, telefone) | ALTA |
| L2 | Logs sem segredos (tokens, senhas, chaves) | BLOQUEANTE |
| L3 | Operacoes criticas registradas com trilha de auditoria via `validarAuditarPermissao` | ALTA |
| L4 | `InfraDebug` desligado em producao | ALTA |

### 1.7 PHP / AppSec Transversal

| # | Item | Severidade do risco |
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

> **Notas C1-C10, anti-falso-positivo**:
> - So reportar C1/C2 quando houver evidencia concreta de segredo real ou exposicao sensivel. Placeholder, fixture ou exemplo obviamente invalido nao conta.
> - C3 exige caminho de execucao plausivel e entrada realmente controlavel ou sem restricao suficiente.
> - C4 exige avaliar a origem do dado serializado. Serializacao interna e controlada, sem entrada externa, nao e achado por si so.
> - C5 e C8 exigem influencia real de dado externo ou configuracao nao confiavel.
> - C10 depende de evidencia existente no repositorio ou em relatorio disponivel ao revisor. A ausencia de ferramenta externa nao e achado.

---

## 2. Criterios de Severidade

| Nivel | Definicao | Acao requerida |
|-------|-----------|----------------|
| **BLOQUEANTE** | Viola autenticacao, autorizacao, expoe dados sensiveis ou quebra integridade. | Corrigir antes do merge. |
| **ALTA** | Risco real de exploracao ou violacao de padrao critico. | Corrigir antes da entrega ou registrar issue com prazo definido. |
| **MEDIA** | Viola padrao do projeto mas sem risco direto de exploracao no contexto atual. | Registrar issue e corrigir na proxima sprint. |
| **BAIXA** | Melhoria de qualidade ou boa pratica nao aplicada. Sem risco imediato. | Registrar como debito tecnico. Corrigir quando conveniente. |

---

Severidade nao substitui o estado do gate. Uma violacao confirmada de G5, G7 ou
G9, por exemplo, retorna `BLOCK` mesmo com severidade `ALTA`.

## 3. Gatilhos para usar este checklist

| Situacao | Secoes aplicaveis |
|----------|-------------------|
| PR com nova pagina PHP ou acao | 1.1, 1.6, 1.7 + skill `sei-verificacao-pagina` |
| PR com nova acao AJAX no modulo | 1.2, 1.6, 1.7 + skill `sei-verificacao-controladores` |
| PR com novo evento em `*Integracao` | 1.3, 1.6, 1.7 + skill `sei-mod-api-eventos` |
| PR com nova operacao API/WS | 1.4, 1.6, 1.7 + skill `sei-mod-api-operacoes` |
| PR com mudanca em BD (DDL, DTO, BD) | 1.5, 1.7 + skill `sei-verificacao-banco-dados` |
| Hardening geral de modulo | Todas as secoes + skill `sei-guardrails-modulo` |
| Revisao de modulo completo | Todas as secoes + skill `sei-revisao-tecnica` (escopo de modulo) |

---

## 4. Instrucoes de Uso para IA

Execute `sei-revisao-tecnica`. Este checklist e a referencia de criterios,
severidades e itens `C1-C10` utilizados pela skill. Nao e um protocolo de execucao
independente.
