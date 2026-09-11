# Mapa CWE para os controles de segurança do SEI

Ponte do projeto para a skill `owasp-playbook`, que é agnóstica e lê este arquivo por seção: Tradução, Sinais do projeto, Auditores do projeto, Exceções, Saídas opcionais e Correção. Tudo que é do SEI naquela skill mora aqui.

Tradução entre o vocabulário CWE e OWASP dos plays do `owasp-playbook` e os controles deste repositório. O play reporta por CWE e OWASP; este mapa diz o que aquilo significa aqui, qual gate se aplica, qual estado o achado assume e qual seção do ASVS o justifica.

Use sempre que a dimensão de segurança estiver no escopo da revisão.

**Padrão vulnerável e seguro em PHP**: `.agents/security/matriz-vulnerabilidades-sei.md`, vetores `V01` a `V10`, e a referência da skill de gate indicada em cada linha. Nenhum play do playbook cobre PHP; a linha de framework está na seção [Auditores do projeto](#auditores-do-projeto).

## Regra de tradução

1. Pegue o CWE do achado do play.
2. Localize a linha correspondente abaixo.
3. Confirme o caminho do dado, da entrada até o ponto de uso, antes de tratar como achado. Sem esse rastro, o item é hipótese.
4. Aplique o estado da linha. CWE fora da tabela vira `WARN` e comunicação ao desenvolvedor, nunca `BLOCK`.

## Tradução

| CWE | Controle local no SEI | Vetor | Gate | Skill de gate | Estado confirmado | ASVS |
|---|---|---|---|---|---|---|
| CWE-352 Cross-Site Request Forgery | `validarLink()` no início da ação e `assinarLink()` no link | `V01` | `G3`, `G4` | `sei-verificacao-pagina` (P1) | `BLOCK` | V3.5 |
| CWE-862 Missing Authorization | `validarPermissao()` na ação e autorização por ação ou serviço no controlador | `V02`, `V03` | `G3`, `G8` | `sei-verificacao-pagina` (P2), `sei-verificacao-controladores` (CI4) | `BLOCK` | V8.2, V8.3 |
| CWE-79 Cross-site Scripting | `PaginaSEI::tratarHTML()` ou equivalente documentado na saída | `V04` | `G7` | `sei-verificacao-pagina` (P8/P9) | `BLOCK` | V1.2 |
| CWE-89 SQL Injection | Consulta por DTO e BD, sem concatenação em `executarSql` | `V05` | checklist `B6` | `sei-verificacao-banco-dados` | `BLOCK` | V1.2 |
| CWE-20 Improper Input Validation | `PaginaSEI::POST/GET` com normalização de tipo; `$_REQUEST` proibido | `V06` | `G5` | `sei-verificacao-pagina` (P5/P6) | `BLOCK` | V2.2 |
| CWE-362 Race Condition e integridade transacional | Método `*Controlado` restrito a persistência; e-mail, Solr e integração externa após o commit | `V07` | `T6` | `sei-verificacao-rn` | `BLOCK` | V2.3 |
| CWE-209 Information Exposure Through an Error Message | Stacktrace fora da resposta ao usuário | `V09` | sem gate | `sei-revisao-tecnica` | `WARN` | V13.4, V16.5 |
| CWE-532 Insertion of Sensitive Information into Log | Log sem segredo e sem PII; escrita na RN com `validarAuditarPermissao` | `V10` | checklist `L1`, `L2`, `L3` | `sei-verificacao-rn` | `BLOCK` para segredo; `WARN` para PII isolada | V16.2, V16.3 |
| CWE-798 Use of Hard-coded Credentials | Segredo fora do código, da configuração versionada e dos scripts | sem vetor | checklist `C1` | `sei-revisao-tecnica` | `BLOCK` | V13.3 |
| CWE-200 Exposure of Sensitive Information | Credencial fora de log, stacktrace, URL e resposta HTTP | sem vetor | checklist `C2` | `sei-revisao-tecnica` | `BLOCK` | V14.2 |
| CWE-78 OS Command Injection | Sem `exec`, `shell_exec`, `system`, `passthru`, `proc_open` ou `popen` com entrada controlável | sem vetor | checklist `C3` | `sei-revisao-tecnica` | `BLOCK` | V1.2 |
| CWE-502 Deserialization of Untrusted Data | Sem `unserialize()` sobre dado externo ou persistido sem integridade | sem vetor | checklist `C4` | `sei-revisao-tecnica` | `BLOCK` | V1.5 |
| CWE-22 Path Traversal e CWE-98 File Inclusion | Caminho, `include` e `require` sem parte controlável, com allowlist | sem vetor | checklist `C5` | `sei-revisao-tecnica` | `WARN` | V5.3, V15.3 |
| CWE-434 Unrestricted File Upload | Upload com validação de tipo, tamanho e nome, com rename seguro e fora de área executável | sem vetor | checklist `C6` | `sei-revisao-tecnica` | `WARN` | V5.2 |
| CWE-611 XML External Entity | Parser XML e HTML com entidade externa desligada | sem vetor | checklist `C7` | `sei-revisao-tecnica` | `WARN` | V1.5 |
| CWE-918 SSRF | URL de fetch, webhook ou download com allowlist | sem vetor | checklist `C8` e `A7` | `sei-revisao-tecnica`, `sei-verificacao-controladores` | `WARN`; `BLOCK` quando confirmado no contexto `A7` | V1.2 |
| CWE-601 Open Redirect | URL de redirect, iframe ou navegação no cliente com allowlist | sem vetor | checklist `C8` e `A7` | `sei-revisao-tecnica`, `sei-verificacao-controladores` | `WARN`; `BLOCK` quando confirmado no contexto `A7` | V1.2 |
| CWE-338 Weak PRNG | Token, nonce e identificador sensível fora de `rand`, `mt_rand` e timestamp previsível | sem vetor | checklist `C9` | `sei-revisao-tecnica` | `WARN` | V11.5 |
| CWE-1395 Vulnerable Third-Party Component | Dependência sem vulnerabilidade conhecida relevante ao uso | sem vetor | checklist `C10` | `sei-revisao-tecnica` | `WARN` | V15.2 |
| CWE-1188 Insecure Default e CWE-489 Debug Code | `InfraDebug` desligado em produção | sem vetor | checklist `L4` | `sei-revisao-tecnica` | `WARN` | V13.4 |
| CWE-327 Broken or Risky Cryptographic Algorithm | Módulo não implementa criptografia própria; uso do mecanismo do core não é achado | sem vetor | sem gate | `sei-revisao-tecnica` | `WARN` | V11.2, V11.3 |
| CWE-319 Cleartext Transmission | Transporte é responsabilidade da infraestrutura, não do módulo | sem vetor | sem gate | `sei-revisao-tecnica` | `WARN` | V12.1 |
| CWE-937 e CWE-1104 Componente desatualizado ou sem manutenção | Mesma verificação de `CWE-1395`: dependência sem vulnerabilidade conhecida relevante ao uso | sem vetor | checklist `C10` | `sei-revisao-tecnica` | `WARN` | V15.2 |
| CWE-807 Decisão de segurança sobre entrada não confiável e CWE-345 Verificação insuficiente de autenticidade | `assinarLink()` aplicado somente a valor produzido pela aplicação; entrada de requisição passa por allowlist antes de compor link ou decisão de segurança | `V01` | `G3`, `G4` | `sei-verificacao-controladores`, `sei-verificacao-pagina` | `BLOCK` | V3.5, V1.2 |
| CWE-639 Authorization Bypass Through User-Controlled Key | Escopo do registro conferido na RN, além do recurso SIP da ação | `V02` | `G3` | `sei-verificacao-rn` | `BLOCK` | V8.2 |
| CWE-117 Improper Output Neutralization for Logs | Log sem quebra de linha nem caractere de controle vindo de entrada externa | `V10` | checklist `L1` | `sei-verificacao-rn` | `WARN` | V16.3 |
| CWE-778 Insufficient Logging | Toda escrita relevante passa por `validarAuditarPermissao`; operação que muda dado sem trilha é achado | `V10` | checklist `L3` | `sei-verificacao-rn` | `WARN` | V16.2 |
| CWE-915 Mass Assignment | DTO com atributos declarados um a um; sem povoar DTO em massa a partir da requisição | `V06` | `G5` | `sei-verificacao-pagina` | `WARN` | V2.2 |
| CWE-756 Missing Custom Error Page e CWE-614 Cookie sem atributo de segurança | Página de erro e atributo de cookie são do core, não do módulo | sem vetor | sem gate | `sei-revisao-tecnica` | `WARN` | V13.4, V3.4 |

A coluna ASVS aponta a seção do índice da skill `security-guidance` do upstream. A ficha da seção está em `.agents/skills/owasp-playbook/upstream/plugins/code-security-skills/data/asvs/<seção>.md`. Serve para justificar o achado com ID de requisito; não altera o estado.

## Classes do play `code-review-security`

O play revisa por classe, de A a G, e abre cada classe com o CWE de cabeçalho. Para chegar ao controle local, use as linhas do mapa indicadas por classe.

| Classe do play | Linhas do mapa e controles locais |
|---|---|
| A. Injection, CWE-74, OWASP A03 | CWE-89, CWE-79, CWE-78, CWE-22 e CWE-98, CWE-20 |
| B. Authentication & Session, CWE-287, OWASP A07 | Exceção "Autenticação e sessão" abaixo; aleatoriedade fraca em token ou nonce é CWE-338 |
| C. Authorization, CWE-862, OWASP A01 | CWE-352, CWE-862; controles sem CWE `P7`, `P10` e `CI1` na seção "Controle local sem CWE correspondente"; escrita na RN sem auditoria é checklist `L3`, skill `sei-verificacao-rn` (A1) |
| D. Cryptography, CWE-327, OWASP A02 | CWE-327, CWE-338 |
| E. Data Exposure, CWE-200, OWASP A01 | CWE-798, CWE-200, CWE-209, CWE-532; payload de retorno de AJAX e WebService é checklist `A6`, skill `sei-verificacao-controladores` (CI5), estado `WARN` |
| F. Security Misconfiguration, OWASP A05 | CWE-1188 e CWE-489, CWE-918 e CWE-601, CWE-1395; exceções "Configuração" e "Cabeçalho HTTP, CORS e rate limiting" abaixo |
| G. Deserialization & Data Integrity, CWE-502, OWASP A08 | CWE-502, CWE-611, CWE-434; CSRF fica na classe C, e o controle é `validarLink()` mais `assinarLink()`, não token de formulário |

## Sinais do projeto

Sinais que a tabela genérica da skill não enxerga. Se o sinal aparece no escopo, o play roda junto com o modo padrão.

| Sinal no escopo | Play | Onde está hoje |
|---|---|---|
| Página `*_lista.php` ou `*_cadastro.php`, ou `*Integracao.php` com `processarControlador()` | `owasp-top10-web-review` | todo módulo web do SEI. Neste repositório o play é obrigatório por sinal e deixa de depender da intenção da frase |
| `*Integracao.php` com `processarControladorAjax()`, `processarControladorAjaxExterno()` ou `processarControladorWebServices()` | `api-security-review` | AJAX interno em vários módulos, inclusive `apoio-plano-trabalho`; WebService em `centraliza-modulos`, `peticionamento`, `pen`, `ws_complementar` e `ia` |
| `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.claude-plugin/` ou `.github/` no escopo | `agent-security-audit` | stack de IA deste repositório: skills que executam script, permissões em `.claude/settings.local.json`, marketplace local e flags `disable-model-invocation` |
| Qualquer arquivo em `modulos/ia/` | `llm-risk-assess` e a parte estática de `prompt-injection-testing`, juntos | módulo SEI IA: chat, galeria de prompts, pesquisa de documento, configuração de assistente e de integração com o provedor. Superfícies de entrada: chat, prompts favoritos e da galeria, conteúdo de documento que chega ao modelo |
| Pedido de teste dinâmico do chat do módulo `ia`, com ambiente de homologação informado e autorização na frase | parte dinâmica de `prompt-injection-testing` | nunca contra produção |
| Escopo adiciona ou altera dependência: `composer.json`, `composer.lock`, diretório `vendor/` ou biblioteca nova em `js/` de módulo | `sca-audit` | `modulos/pen/vendor/`, Guzzle vendorizado sem manifesto. Dependência estável não é reauditada a cada revisão de módulo |
| `.mcp.json` ou `mcpServers` em configuração | `mcp-server-review` | não há hoje; o play responde que não se aplica |
| `infra/**` | `iac-security-review` | escopo proibido pelo `AGENTS.md`; o play não roda |

A seleção de plays e auditores não depende de leitura manual desta tabela. Rode `python3 .agents/skills/sei-revisao-tecnica/plays_aplicaveis.py <caminhos>` e use a saída como lista obrigatória. Play listado pelo script que não for executado exige justificativa escrita no relatório.

Fora do gatilho por sinal, `securability-engineering-review` é obrigatório em dois momentos: na primeira release de um módulo novo, para estabelecer a linha de base SSEM, e uma vez por ciclo de release sobre o repositório. Não roda a cada revisão de módulo, porque produz nota de postura e não lista de vulnerabilidade.

## Auditores do projeto

Etapa Framework-Specific Checks do play `code-review-security`, cuja tabela lista React, Express, Django, Flask, Spring, Rails e Go. Esta é a linha que falta. Nesta etapa, rode sobre o escopo todo auditor cujo artefato estiver presente; eles são a checagem mecânica desta linha. O que sobrar da tabela abaixo é leitura orientada, com o padrão na matriz e na referência da skill de gate de cada linha do mapa.

A fonte de verdade de qual gate se aplica a qual artefato é a tabela "Gates por artefato" do `AGENTS.md`, seção Roteamento. A lista abaixo é a forma de execução, não a lista de gates: gate novo no `AGENTS.md` entra aqui também. `sei-revisao-tecnica/plays_aplicaveis.py` deriva a lista do escopo e evita a conferência manual.

```bash
python3 .agents/skills/sei-verificacao-pagina/audit.py --input <pagina> --pagina existente --format markdown
python3 .agents/skills/sei-verificacao-rn/audit.py --input <rn/ ou RN.php> --format markdown
python3 .agents/skills/sei-verificacao-controladores/audit.py --input <Integracao.php> --format markdown
python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <modulo/ ou DTO.php> --format markdown
python3 .agents/skills/sei-verificacao-tarefa/audit.py --input <*_tarefa.php> --format markdown
```

`sei-verificacao-pagina/audit.py` aceita um arquivo por execução: rode uma vez por página.

| Framework | Key Checks |
|---|---|
| SEI / InfraPHP (PHP 8.2) | Ação sem `validarLink()` e `validarPermissao()`; AJAX e WebService sem autorização por ação; saída sem `PaginaSEI::tratarHTML()`; `$_REQUEST` e `$_GET` sem normalização de tipo; efeito colateral dentro de método `*Controlado`; escrita na RN sem `validarAuditarPermissao`; página acessando BD sem passar pela RN; encoding incompatível com a conversão Latin-1 |

## Exceções

- **Autenticação e sessão.** Módulo não implementa login. Uso do mecanismo do core, via `SessaoSEI` e SIP, sem sessão, token ou credencial próprios, não é achado.
- **Configuração.** `ConfiguracaoSEI.php` é arquivo de configuração do core. O agente descreve o passo e para; edição exige autorização explícita do desenvolvedor, conforme `AGENTS.md`.
- **Auditoria SIP.** Recurso de leitura `_listar`, `_consultar` e `_selecionar` fora da regra de auditoria SIP é o comportamento esperado, conforme `.agents/references/padrao-auditoria-sip-sei.md`.
- **Aleatoriedade.** `mt_rand` compondo nome de arquivo temporário, sem função de segurança, não é CWE-338.
- **Cabeçalho HTTP, CORS e rate limiting.** São do core e da infraestrutura. Ausência no módulo não é achado.
- **Token em URL.** Montagem do tipo `"?token=" . $variavel` é parâmetro de URL, não credencial no código. Não é CWE-798.

## Rastreabilidade por categoria OWASP

O play `owasp-top10-web-review` do `owasp-playbook` abre cada categoria com os CWE que ela cobre, no formato `A01: Broken Access Control > CWE-200, CWE-201, CWE-352, CWE-639`. Para ir da categoria OWASP até o controle local, use os dois saltos: pegue os CWE que o play lista na categoria, e traduza cada um pela tabela acima.

O play usa a edição **2021** do OWASP Top 10. Ao citar a categoria em um relatório, diga a edição, porque a numeração muda entre edições.

A lista de CWE por categoria dessa cópia do play é reduzida e não cobre todo o mapeamento oficial de 2021. `CWE-601`, por exemplo, não aparece em nenhuma categoria no arquivo instalado, embora o mapeamento completo do OWASP o coloque em A01. Ao citar categoria, use a lista do arquivo instalado como fonte e diga quando o CWE não tiver categoria lá.

## Rastreabilidade OpenCRE

O playbook traz ficha OpenCRE para parte dos CWE, em `.agents/skills/owasp-playbook/upstream/data/opencre/`. A ficha cruza o CWE com ASVS, WSTG, NIST 800-53 e outros padrões, e serve para justificar o achado diante de auditoria externa.

Disponível para estas linhas da tabela:

| CWE da tabela | Ficha OpenCRE |
|---|---|
| CWE-352 Cross-Site Request Forgery | `CWE-352.md` |
| CWE-79 Cross-site Scripting | `CWE-79.md` |
| CWE-89 SQL Injection | `CWE-89.md` |
| CWE-798 Use of Hard-coded Credentials | `CWE-798.md` |
| CWE-200 Exposure of Sensitive Information | `CWE-200.md` |
| CWE-78 OS Command Injection | `CWE-78.md` |
| CWE-502 Deserialization of Untrusted Data | `CWE-502.md` |
| CWE-22 Path Traversal | `CWE-22.md` |

As demais linhas da tabela não têm ficha OpenCRE nesta versão do playbook. A ausência da ficha não altera o estado do gate.

Há ainda fichas sem linha correspondente aqui: `CWE-16.md` (configuração), `CWE-287.md` (autenticação), `CWE-384.md` (session fixation) e `CWE-778.md` (log insuficiente). As três primeiras caem nas exceções acima, porque autenticação e sessão são do core.

## Controle local sem CWE correspondente

- **`V08`, encoding incompatível com a conversão Latin-1 em arquivo PHP.** Gate `G1`, skill `sei-verificacao-pagina` (P3). É requisito de integridade de artefato do repositório, não risco de aplicação. Nenhum play detecta, e o gate continua valendo por conta própria.
- **`P10`, mutação de estado por GET.** Gate `G9`, skill `sei-verificacao-pagina`, estado `BLOCK`. O controle é POST com link assinado.
- **`CI1`, `tratarLinkSemAssinatura()` sem `preg_match` restritivo.** Gate `G8`, skill `sei-verificacao-controladores`, estado `BLOCK`.
- **`P7`, UI condicional sem `verificarPermissao()`.** Skill `sei-verificacao-pagina`, estado `WARN` quando isolado. Se a mesma evidência confirmar execução não autorizada, vale a linha CWE-862.

## O que o playbook não cobre

| Lacuna | Como tratar aqui |
|---|---|
| PHP e InfraPHP | A tabela de checagem por framework do play `code-review-security` lista React, Express, Django, Flask, Spring, Rails e Go. Use a seção [Auditores do projeto](#auditores-do-projeto) deste mapa nessa etapa |
| Injeção de fórmula em planilha exportada, CWE-1236 | Verificação manual quando houver exportação para planilha: valor iniciado por `=`, `+`, `-` ou `@` precisa ser neutralizado |
| Efeito externo irreversível dentro da transação | Coberto por `V07`, `T6` e `sei-verificacao-rn`, que são gate próprio do SEI e independem do playbook |
| Varredura automática | O playbook é procedimento em Markdown, sem scanner e sem lista de checkpoints executáveis. Toda execução é leitura orientada por procedimento |

## Saídas opcionais

Quando o usuário pedir PDF, JSON ou texto de issues, o próprio pedido traz o formato e os caminhos. Modelos prontos em [prompts-exemplo.md, seção Variações de saída da revisão técnica](../../docs/stack_ai/prompts-exemplo.md#variações-de-saída-da-revisão-técnica).

Use os dados da revisão solicitada e informe explicitamente o JSON ao gerador preparado. A preparação ou alteração do gerador é uma tarefa separada. As saídas opcionais preservam o resultado da revisão e não autorizam abrir issues em ferramentas externas.

## Correção

Correção não é desta skill. Roteie pelo `.agents/references/roteamento-de-skills.md`: `sei-guardrails-modulo` como guardrail central e a skill de gate do artefato (`sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-controladores`, `sei-verificacao-banco-dados`), citando o achado pelo número do relatório.
