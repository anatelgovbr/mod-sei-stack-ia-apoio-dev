# Mapeamento OWASP dos Controles de Seguranca SEI

## Objetivo e Limites

Este documento relaciona os vetores locais `V01-V10` e os controles AppSec PHP
`C1-C10` aos seguintes referenciais:

- OWASP Top 10:2025
- OWASP API Security Top 10:2023
- OWASP Application Security Verification Standard, ASVS 5.0.0

O mapeamento serve para rastreabilidade tecnica e apoio a revisoes. Ele nao e
certificacao, auditoria independente nem declaracao de conformidade integral com
qualquer referencial OWASP. Uma relacao indica sobreposicao de objetivo ou risco,
nao equivalencia entre os controles. A verificacao de um item local tambem nao
comprova atendimento aos demais requisitos da categoria ou do capitulo OWASP.

Neste documento, `C1-C10` identifica a secao `1.7 PHP / AppSec Transversal` do
checklist local. Nao se confunde com os gates `C1-C4` do gerador CRUD.

### Classificacao das Relacoes

| Tipo | Criterio |
|---|---|
| Direta | O controle local trata a mesma fraqueza ou um requisito OWASP explicito. |
| Parcial | Ha sobreposicao objetiva, mas um dos lados possui escopo adicional. |
| Contextual | O tema e adjacente ou depende de condicao especifica. Nao deve ser tratado como equivalencia. |

Quando a tabela usa `Contextual, sem relacao forte`, nao foi identificada uma
correspondencia suficientemente especifica no referencial indicado. Essa
declaracao e intencional e evita forcar associacoes.

### Fontes Locais

- [Matriz]: definicoes `V01-V10` em
  `.agents/security/matriz-vulnerabilidades-sei.md`.
- [Checklist]: controles `C1-C10` e itens complementares em
  `.agents/checklists/checklist-seguranca.md`.
- [Gates]: condicoes de bloqueio em
  `.agents/references/gates-de-implementacao.md`.

## OWASP Top 10:2025

| Controle local | Referencia OWASP | Relacao | Cobertura | Limite | Fonte local |
|---|---|---|---|---|---|
| V01, acao sem `validarLink()` | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | Direta | A01 inclui CSRF e alteracao ou forja de URL entre as falhas de controle de acesso. | Cobre a protecao da requisicao no padrao SEI, nao todos os controles de acesso de A01. | [Matriz] V01; [Gates] G3 |
| V02, acao sem `validarPermissao()` | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | Direta | Impede execucao de funcao fora das permissoes do usuario e elevacao de privilegio. | Nao cobre propriedade de objeto, CORS, sessao ou todos os demais casos de A01. | [Matriz] V02; [Gates] G3 |
| V03, AJAX sem autorizacao por acao | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | Direta | Exige autorizacao no servidor para cada funcao exposta pelo controlador. | Nao avalia autorizacao por objeto ou campo nem todo o ciclo de sessao. | [Matriz] V03; [Gates] G8 |
| V04, XSS por saida sem escape | [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | Direta | A05 inclui XSS e neutralizacao incorreta de dados enviados ao navegador. | O controle local cobre sinks HTML e JavaScript observados, nao todas as formas de injecao. | [Matriz] V04; [Gates] G7 |
| V05, SQL Injection por concatenacao | [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | Direta | Evita que entrada controlavel altere a estrutura da consulta SQL. | Nao cobre outros interpretadores, ORMs ou stored procedures dinamicas sem evidencia local. | [Matriz] V05; [Checklist] B6 |
| V06, uso de `$_REQUEST` ou entrada sem normalizacao | [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | Parcial | Normalizacao de origem e tipo reduz entrada ambigua e sustenta validacao no servidor. | Usar superglobal diretamente nao comprova injecao por si so, e A05 nao prescreve `PaginaSEI::GET/POST`. | [Matriz] V06; [Gates] G5 |
| V07, efeito colateral dentro de transacao | [A10:2025 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | Parcial | A10 exige rollback e falha segura quando uma transacao encontra erro. | A separacao local de email, Solr e integracoes depois do commit e mais especifica que A10. | [Matriz] V07; [Checklist] E2 |
| V08, encoding incompativel com a conversao Latin-1 | [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | Contextual, sem relacao forte | O controle preserva integridade de texto no processo de conversao e entrega do SEI. | Nenhuma categoria de 2025 trata especificamente BOM ou compatibilidade do arquivo-fonte com conversao Latin-1. | [Matriz] V08; [Gates] G1 |
| V09, exposicao de stacktrace | [A10:2025 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | Direta | A10 inclui mensagens de erro com informacao sensivel e resposta insegura a excecoes. | Evitar stacktrace nao atende sozinho logging, recuperacao, alertas e falha segura de A10. | [Matriz] V09 |
| V10, log com PII ou segredos | [A09:2025 Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) | Direta | A09 inclui insercao de dados sensiveis em logs e exposicao de PII. | O item local nao cobre integridade, retencao, monitoramento e alertas exigidos por A09. | [Matriz] V10; [Checklist] L1/L2 |
| C1, segredo real hardcoded | [A02:2025 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) e [A04:2025 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) | Parcial | A02 recomenda nao embutir chaves estaticas; A04 cobre chaves criptograficas no repositorio. | C1 tambem abrange senhas, tokens e connection strings que nao sao necessariamente chaves criptograficas. | [Checklist] C1 |
| C2, segredo ou credencial exposto | [A09:2025 Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) e [A10:2025 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | Parcial | A09 cobre logs sensiveis; A10 cobre stacktraces e erros com segredos ou tokens. | A exposicao em URL, resposta comum ou comentario operacional nao e integralmente representada por uma unica categoria. | [Checklist] C2 |
| C3, comando com entrada controlavel | [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | Direta | A05 inclui injecao de comando e de argumentos em chamadas ao sistema operacional. | Nao cobre riscos de processo sem entrada controlavel que nao caracterizem injecao. | [Checklist] C3 |
| C4, desserializacao de dado nao confiavel | [A08:2025 Software or Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/) | Direta | A08 inclui desserializacao de dados nao confiaveis e ausencia de verificacao de integridade. | Serializacao interna com origem e integridade controladas nao e achado automatico em nenhum dos lados. | [Checklist] C4 |
| C5, caminho de arquivo controlavel | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) e [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | Parcial | A01 inclui path traversal; A05 inclui inclusao remota e controle inseguro de nomes em interpretadores. | Leitura, escrita, `include` e `require` possuem impactos diferentes e nao cabem integralmente em uma categoria. | [Checklist] C5 |
| C6, upload inseguro | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) e [A02:2025 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) | Contextual, sem relacao forte | Permissoes de armazenamento e exposicao em webroot podem participar do risco. | As categorias nao especificam conjuntamente tipo, extensao, tamanho, renomeacao e impedimento de execucao exigidos por C6. | [Checklist] C6 |
| C7, XML/XXE | [A02:2025 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) | Direta | A02 inclui configuracao insegura de parser e CWE-611 para entidades externas XML. | Nao cobre outros riscos de XML, schema ou transformacoes que nao envolvam configuracao insegura. | [Checklist] C7 |
| C8, URL controlavel sem allowlist | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | Direta | A01 inclui SSRF e redirecionamento para destino nao confiavel. | A categoria nao detalha igualmente todos os sinks locais, como iframe e download. | [Checklist] C8 |
| C9, aleatoriedade fraca | [A04:2025 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) | Direta | A04 inclui baixa entropia, PRNG fraco e identificadores previsiveis. | C9 se limita a tokens, nonces, segredos temporarios e identificadores sensiveis. | [Checklist] C9 |
| C10, dependencia vulneravel | [A03:2025 Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) | Direta | A03 cobre componentes vulneraveis, desatualizados ou sem manutencao e sua gestao. | C10 depende de evidencia disponivel e nao cobre sozinho SBOM, origem, CI/CD ou toda a cadeia de fornecimento. | [Checklist] C10 |

## OWASP API Security Top 10:2023

Este referencial e especifico para APIs. Controles locais de pagina, build ou
armazenamento podem nao possuir categoria correspondente na edicao 2023.

| Controle local | Referencia OWASP | Relacao | Cobertura | Limite | Fonte local |
|---|---|---|---|---|---|
| V01, acao sem `validarLink()` | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Contextual, sem relacao forte | A protecao anti-CSRF pode ser relevante para API acessada por navegador e autenticada por cookie. | A edicao 2023 nao possui categoria especifica de CSRF e `validarLink()` e um controle de pagina SEI. | [Matriz] V01; [Gates] G3 |
| V02, acao sem `validarPermissao()` | [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | Direta | Exige concessao explicita por funcao antes de executar operacao privilegiada. | Nao cobre autorizacao por objeto, propriedade ou fluxo de negocio. | [Matriz] V02; [Gates] G3 |
| V03, AJAX sem autorizacao por acao | [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | Direta | O dispatch por acao deve aplicar autorizacao especifica no servidor. | A verificacao local nao atende automaticamente autorizacao de dados e propriedades. | [Matriz] V03; [Gates] G8 |
| V04, XSS por saida sem escape | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Contextual, sem relacao forte | Uma resposta de API pode alimentar um sink inseguro no cliente. | A edicao 2023 nao tem categoria especifica para XSS nem para encoding contextual de HTML. | [Matriz] V04; [Gates] G7 |
| V05, SQL Injection por concatenacao | [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/) | Contextual, sem relacao forte | API10 cobre injecao quando dados recebidos de API integrada sao tratados como confiaveis. | V05 cobre qualquer entrada controlavel; a edicao 2023 nao possui categoria geral de injecao. | [Matriz] V05; [Checklist] B6 |
| V06, uso de `$_REQUEST` ou entrada sem normalizacao | [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | Parcial | API8 recomenda restringir formatos e tipos de conteudo aceitos pela API. | Nao exige o helper SEI nem cobre toda validacao de valor, origem e regra de negocio. | [Matriz] V06; [Gates] G5 |
| V07, efeito colateral dentro de transacao | [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/) | Contextual, sem relacao forte | Falhas, timeouts e respostas de integracoes externas podem acionar o risco local. | API10 trata confianca no consumo de APIs, nao o posicionamento do efeito externo em relacao ao commit. | [Matriz] V07; [Checklist] E2 |
| V08, encoding incompativel com a conversao Latin-1 | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Contextual, sem relacao forte | Encoding coerente evita interpretacao incorreta de payloads e respostas. | Nenhuma categoria trata compatibilidade de arquivo-fonte, BOM ou conversao Latin-1 do SEI. | [Matriz] V08; [Gates] G1 |
| V09, exposicao de stacktrace | [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | Direta | API8 cita stacktraces e informacao sensivel em mensagens de erro. | Ocultar stacktrace nao atende todo o hardening e a configuracao segura da pilha de API. | [Matriz] V09 |
| V10, log com PII ou segredos | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Contextual, sem relacao forte | Logs de APIs continuam sujeitos a minimizacao e protecao de dados. | A edicao 2023 nao possui categoria de logging e monitoramento nem requisito especifico contra PII em log. | [Matriz] V10; [Checklist] L1/L2 |
| C1, segredo real hardcoded | [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) | Parcial | Credenciais, chaves e tokens estaticos podem enfraquecer autenticacao entre clientes e APIs. | API2 nao proibe de forma geral todo segredo em codigo, configuracao ou script. | [Checklist] C1 |
| C2, segredo ou credencial exposto | [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) e [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | Parcial | API2 cobre tokens e senhas em URL; API8 cobre segredos e detalhes em erros. | Log, comentario operacional e toda resposta HTTP nao sao cobertos integralmente por essas categorias. | [Checklist] C2 |
| C3, comando com entrada controlavel | [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/) | Contextual, sem relacao forte | API10 e pertinente se dado de uma API integrada alcancar a execucao do comando. | Nao ha categoria geral de command injection na edicao 2023. | [Checklist] C3 |
| C4, desserializacao de dado nao confiavel | [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/) | Parcial | Exige validar e sanitizar dados recebidos de APIs integradas antes do processamento. | Desserializacao de outras fontes externas ou persistidas nao e tratada especificamente por API10. | [Checklist] C4 |
| C5, caminho de arquivo controlavel | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Contextual, sem relacao forte | Caminhos controlaveis podem integrar a superficie exposta por uma API. | A edicao 2023 nao possui categoria especifica para path traversal local, escrita, `include` ou `require` em caminho controlavel. | [Checklist] C5 |
| C6, upload inseguro | [API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) | Parcial | API4 exige limite maximo de upload e de recursos consumidos no processamento. | Nao cobre extensao, tipo real, nome seguro, renomeacao ou execucao no diretorio publico. | [Checklist] C6 |
| C7, XML/XXE | [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | Contextual, sem relacao forte | Habilitar recursos inseguros de parser pode caracterizar configuracao insegura da API. | API8:2023 nao identifica XXE ou entidades externas como controle especifico. | [Checklist] C7 |
| C8, URL controlavel sem allowlist | [API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/) | Direta | API7 cobre fetch, webhook e busca de arquivo por URL do cliente sem allowlist forte. | Redirecionamento no cliente, iframe e download sem requisicao do servidor ficam fora do nucleo de API7. | [Checklist] C8 |
| C9, aleatoriedade fraca | [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) | Parcial | API2 inclui tokens de autenticacao fracos ou previsiveis. | Nonces e identificadores sensiveis sem funcao de autenticacao nao sao cobertos por API2. | [Checklist] C9 |
| C10, dependencia vulneravel | [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | Parcial | API8 inclui sistemas sem patch ou desatualizados na pilha da API. | Nao cobre inventario transitivo, origem, integridade e governanca completa da cadeia de fornecimento. | [Checklist] C10 |

## OWASP ASVS 5.0.0

Os identificadores seguem o formato recomendado pela OWASP,
`v<versao>-<capitulo>.<secao>.<requisito>`. Os links apontam para o CSV oficial
da release estavel 5.0.0, que contem o texto e o nivel de cada requisito.

| Controle local | Referencia OWASP | Relacao | Cobertura | Limite | Fonte local |
|---|---|---|---|---|---|
| V01, acao sem `validarLink()` | [v5.0.0-3.5.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Requer token anti-forgery ou mecanismo equivalente em funcionalidade sensivel. | `validarLink()` e `assinarLink()` sao a implementacao local; o ASVS admite outros mecanismos. | [Matriz] V01; [Gates] G3/G4 |
| V02, acao sem `validarPermissao()` | [v5.0.0-8.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-8.3.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Restringe acesso por funcao a consumidores autorizados e exige enforcement em camada confiavel. | Nao cobre autorizacao por dado ou campo nem toda a documentacao do capitulo V8. | [Matriz] V02; [Gates] G3 |
| V03, AJAX sem autorizacao por acao | [v5.0.0-8.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-8.3.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige permissao explicita por funcao e decisao no servidor, nao apenas na UI. | O dispatch local nao verifica por si so objeto, campo ou contexto adaptativo. | [Matriz] V03; [Gates] G8 |
| V04, XSS por saida sem escape | [v5.0.0-1.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv), [v5.0.0-1.2.3](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-3.2.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Cobre encoding contextual de HTML, JavaScript/JSON e renderizacao de texto sem execucao. | `PaginaSEI::tratarHTML()` nao substitui encoding especifico para todos os contextos. | [Matriz] V04; [Gates] G7 |
| V05, SQL Injection por concatenacao | [v5.0.0-1.2.4](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Requer consultas parametrizadas, ORM seguro ou protecao equivalente contra injecao em banco. | O padrao local de criterio DTO cobre o caso descrito, nao toda consulta ou procedure possivel. | [Matriz] V05; [Checklist] B6 |
| V06, uso de `$_REQUEST` ou entrada sem normalizacao | [v5.0.0-2.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-2.2.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Parcial | Exige validacao positiva e aplicacao em camada confiavel do servidor. | O ASVS nao proibe superglobais nem prescreve `PaginaSEI::GET/POST`; a regra local tambem separa a origem HTTP. | [Matriz] V06; [Gates] G5 |
| V07, efeito colateral dentro de transacao | [v5.0.0-2.3.3](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-16.5.3](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Parcial | Exige atomicidade, rollback e falha segura em excecoes. | Nao determina explicitamente que email, Solr e integracoes ocorram somente depois do commit. | [Matriz] V07; [Checklist] E2 |
| V08, encoding incompativel com a conversao Latin-1 | [v5.0.0-4.1.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Contextual, sem relacao forte | O requisito exige charset correto no `Content-Type` da resposta HTTP. | Nao trata encoding do arquivo-fonte, BOM ou compatibilidade com a conversao Latin-1 do blob final. | [Matriz] V08; [Gates] G1 |
| V09, exposicao de stacktrace | [v5.0.0-16.5.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige mensagem generica ao consumidor sem stacktrace, query, chave ou token. | Nao cobre sozinho logging do erro, recuperacao segura e handler global. | [Matriz] V09 |
| V10, log com PII ou segredos | [v5.0.0-16.2.5](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Restringe logging de credenciais, dados de pagamento e outros dados conforme nivel de protecao. | O ASVS admite mascaramento em casos definidos; a regra local pode proibir PII de forma mais estrita. | [Matriz] V10; [Checklist] L1/L2 |
| C1, segredo real hardcoded | [v5.0.0-13.3.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige solucao de gestao de segredos e proibe segredos no codigo-fonte e nos artefatos de build. | O atendimento completo tambem requer ciclo de vida, acesso e, em L3, protecao por hardware. | [Checklist] C1 |
| C2, segredo ou credencial exposto | [v5.0.0-14.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv), [v5.0.0-16.2.5](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-16.5.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Cobre segredo em URL, log e mensagem de erro ou stacktrace. | Comentario operacional e toda forma possivel de resposta exigem avaliacao adicional alem desses requisitos. | [Checklist] C2 |
| C3, comando com entrada controlavel | [v5.0.0-1.2.5](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige protecao contra OS command injection e chamada parametrizada ou encoding contextual. | Nao declara que toda chamada de processo e proibida; C3 exige avaliar controle da entrada e allowlist. | [Checklist] C3 |
| C4, desserializacao de dado nao confiavel | [v5.0.0-1.5.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige tratamento seguro, allowlist de tipos e rejeicao de mecanismo inseguro para dado nao confiavel. | Desserializacao interna controlada nao e falha automatica; origem e integridade continuam determinantes. | [Checklist] C4 |
| C5, caminho de arquivo controlavel | [v5.0.0-5.3.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Requer dado interno ou confiavel para caminhos, ou validacao estrita contra traversal, LFI, RFI e SSRF. | Outros requisitos de armazenamento e download podem ser necessarios conforme a operacao. | [Checklist] C5 |
| C6, upload inseguro | [v5.0.0-5.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv), [v5.0.0-5.2.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv), [v5.0.0-5.3.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-5.3.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Cobre tamanho, extensao e conteudo, impedimento de execucao publica e nome/caminho seguro. | Antivirus, arquivos compactados, quotas e protecao de download ficam fora do conjunto local C6. | [Checklist] C6 |
| C7, XML/XXE | [v5.0.0-1.5.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Direta | Exige parser XML restritivo com entidades externas e recursos inseguros desabilitados. | Nao cobre validacao de schema nem toda transformacao XML/HTML. | [Checklist] C7 |
| C8, URL controlavel sem allowlist | [v5.0.0-1.3.6](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) e [v5.0.0-3.7.2](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Parcial | Cobre allowlist de protocolo, dominio, caminho e porta contra SSRF e allowlist de host para redirect. | Iframe, download e todos os detalhes de link sem assinatura podem exigir requisitos adicionais. | [Checklist] C8 |
| C9, aleatoriedade fraca | [v5.0.0-11.5.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Parcial | C9 detecta fontes explicitamente fracas para valores que devam ser imprevisiveis. | O controle local nao comprova uso de CSPRNG nem pelo menos 128 bits de entropia, e requisitos de sessao, MFA ou OAuth podem impor propriedades adicionais. | [Checklist] C9 |
| C10, dependencia vulneravel | [v5.0.0-15.2.1](https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv) | Parcial | C10 detecta dependencia com vulnerabilidade conhecida e relevante quando ha manifesto ou relatorio confiavel. | A evidencia local nao demonstra atendimento integral ao requisito ASVS, pois nao avalia a politica de atualizacao aplicavel ao componente. | [Checklist] C10 |

## Lacunas Explicitas

- Os controles locais analisados nao cobrem integralmente autenticacao, sessao,
  criptografia, comunicacao segura, inventario de APIs, consumo de recursos,
  automacao abusiva, monitoramento ou resposta a incidentes.
- Nenhum vetor `V01-V10` ou controle `C1-C10`, isolado ou em conjunto, representa
  todas as categorias do OWASP Top 10:2025 ou do OWASP API Security Top 10:2023.
- O conjunto local nao foi avaliado requisito a requisito contra todos os niveis
  L1, L2 e L3 do ASVS 5.0.0. As referencias ASVS acima sao somente as relacoes
  aplicaveis aos controles locais descritos.
- `V08` e uma regra especifica da cadeia de encoding e release do SEI. Nao ha
  relacao forte com os tres referenciais consultados.
- A edicao 2023 do OWASP API Security Top 10 nao possui categorias gerais para
  XSS, injecao, logging ou desserializacao. Relacoes nesses temas foram limitadas
  aos cenarios de API expressamente proximos e marcadas como parciais ou
  contextuais.

## Versoes e Fontes Oficiais

Consulta realizada em **17 de agosto de 2026**.

| Referencial | Versao ou data da edicao | Fonte oficial consultada |
|---|---|---|
| OWASP Top 10 | Edicao 2025. A pagina da release nao informa data editorial mais especifica. | <https://owasp.org/Top10/2025/> |
| OWASP API Security Top 10 | Edicao 2023, publicada pelo OWASP API Security Project em 2023. | <https://owasp.org/API-Security/editions/2023/en/0x11-t10/> |
| OWASP ASVS | Versao estavel 5.0.0, publicada em 30 de maio de 2025. | <https://owasp.org/www-project-application-security-verification-standard/> |
| OWASP ASVS | Tag oficial `v5.0.0`. | <https://github.com/OWASP/ASVS/tree/v5.0.0> |
| OWASP ASVS | CSV oficial em ingles usado para os identificadores dos requisitos. | <https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv> |

[Matriz]: ./matriz-vulnerabilidades-sei.md
[Checklist]: ../checklists/checklist-seguranca.md
[Gates]: ../references/gates-de-implementacao.md
