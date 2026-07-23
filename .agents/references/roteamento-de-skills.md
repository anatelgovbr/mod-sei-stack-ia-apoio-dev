# Roteamento de Skills e Contratos

Referencia cross-context: aplica-se ao Fluxo Direto e e carregada como extensao normativa pelo Spec Kit.

## Aliases

| Input do desenvolvedor | Interpretar como |
| --- | --- |
| `sei-crud-generator` | `sei-gerador-crud` |
| `sei-revisao-codigo-seguranca`, `sei-revisao-pr`, `sei-security-review` | `sei-code-review-security` |

## Regras de Classificacao

1. Resolver alias antes de classificar.
2. Identificar o tipo de demanda pelas evidencias da matriz abaixo.
3. Acionar a skill principal; acionar todas as skills complementares aplicaveis ao artefato presente.
4. Verificar a coluna BLOQUEAR SE antes de prosseguir — condicao satisfeita = parar e resolver.
5. `sei-testes-validacao` e complementar obrigatorio em qualquer demanda com implementacao PHP.
6. `sei-tipagem-phpdoc` e opt-in: acionar somente se o request pedir explicitamente tipagem, type hints ou PHPDoc.
7. Release com impacto nos dois lados: acionar `sei-gerador-scripts-release` E `sip-gerador-scripts-release`.
8. Demanda cita nome de tabela/coluna existente (ex.: `md_xxx_entidade`, `sta_situacao`) ou altera/consulta estrutura de entidade ja modelada em `DTO`/`BD` de modulo mapeado: consultar `docs/dicionario_dados/<modulo>/dicionario.md` (SEI/SIP/Julgar: `docs/dicionario_dados/sei/dicionario.md`, `docs/dicionario_dados/sip/dicionario.md` ou `docs/dicionario_dados/julgar/dicionario.md`) como contexto antes de implementar — grep pela tabela especifica em dicionarios grandes, nao carregar o arquivo inteiro. Tabela/coluna ausente do dicionario ou divergente do codigo: acionar `sei-dicionario-dados-core` (alvo SEI, SIP ou Julgar) ou `sei-dicionario-dados-modulo` (alvo modulo customizado) para verificar/atualizar antes de prosseguir; nao inferir semantica sem essa confirmacao.

## Matriz de Demanda

| Tipo | Evidencias no request | Skill principal | Skills complementares | Contrato necessario antes de implementar | BLOQUEAR SE |
| --- | --- | --- | --- | --- | --- |
| CRUD via gerador | request menciona gerador ou `sei-gerador-crud`; nova tabela/entidade; artefatos `DTO`, `RN`, `BD`, `INT`, `*_lista.php`, `*_cadastro.php` | `sei-gerador-crud` | `sei-verificacao-banco-dados`, `sei-verificacao-rn`, `sei-verificacao-pagina`, `sei-verificacao-tarefa` (conforme artefatos gerados) | JSON de contrato confirmado pelo desenvolvedor | contrato pendente ou sem confirmacao |
| CRUD manual | nova tabela/entidade sem uso do gerador; artefatos `DTO`, `RN`, `BD`, `INT`, `*_lista.php`, `*_cadastro.php` | `sei-guardrails-modulo` | `sei-verificacao-banco-dados`, `sei-verificacao-rn`, `sei-verificacao-pagina`, `sei-menu-pagina`, `sei-gerador-scripts-release`, `sip-gerador-scripts-release` (conforme impacto) | entidade, campos, permissoes, transacoes, release e criterios de aceite definidos | entidade, campos, permissoes ou release ambiguos |
| Menu ou pagina | nova acao, pagina, item de menu interno SIP, link de acao | `sei-menu-pagina` | `sei-verificacao-pagina` | recurso SIP, perfil, menu, acao, parametros, permissao e link assinado definidos | recurso, permissao ou acao indefinidos |
| Evento / hook | hook em `*Integracao`, menu externo, publicacoes, assinatura, envio, cancelamento, botao ou icone injetado em tela do core | `sei-mod-api-eventos` | `sei-mod-api-classes` (quando houver duvida de contrato API), `sei-verificacao-rn`, `sei-verificacao-controladores` (quando houver `processarControladorAjax*`, `tratarLinkSemAssinatura` ou WS) | nome do hook, assinatura, entrada, efeito colateral, transacao e auditoria definidos | hook, efeito ou transacao ambiguos |
| API ou WebService | operacao `SeiRN`, `Entrada*API`, `Saida*API`, WS, integracao externa | `sei-mod-api-operacoes` | `sei-mod-api-classes`, `sei-verificacao-controladores` (quando houver `processarControladorWebServices`) | classe de entrada/saida, metodo `SeiRN`, payload minimo, erros e autorizacao definidos | classe interna usada sem justificativa ou payload ambiguo |
| Release SEI / BD | nova tabela, coluna, indice, sequence, seed ou ajuste de versao do script SEI | `sei-gerador-scripts-release` | `sei-verificacao-banco-dados` | versao alvo, script SEI, DDL multi-SGBD, seed e rollback definidos | impacto BD/SEI sem plano de script |
| Release SIP | novo recurso, perfil, menu, auditoria, parametro ou ajuste de versao do script SIP | `sip-gerador-scripts-release` | `sei-verificacao-banco-dados` (quando houver DDL SIP) | versao alvo, script SIP, recursos/perfis/menus, auditoria e rollback definidos | impacto SIP sem plano de script |
| Dicionario de dados — SEI/SIP/Julgar | criar, atualizar, verificar ou gerar changelog de `docs/dicionario_dados/{sei,sip,julgar}/**` | `sei-dicionario-dados-core` | — | operacao, versao alvo exata e caminho do repositorio de pacotes de release confirmados | versao alvo desconhecida, caminho do repositorio de pacotes nao localizado, ou DDL do pacote divergente do codigo |
| Dicionario de dados — modulo | criar, atualizar, verificar ou gerar changelog de `docs/dicionario_dados/<modulo>/**` | `sei-dicionario-dados-modulo` | — | nome do modulo, operacao e versao alvo exata definidos | versao alvo desconhecida ou DDL do script e DTO do modulo inconsistentes |
| Indexacao, pesquisa ou feed | Solr, pesquisa, feed de protocolos, publicacao, reindexacao, metadados pesquisaveis | `sei-guardrails-modulo` | — | origem dos dados, momento de publicacao, transacao, reprocessamento e impacto em pesquisa definidos | indexacao dentro de transacao critica sem justificativa ou sem plano de reprocessamento |
| Novo modulo | nova pasta em `modulos/<inst>/<modulo>`, nova `*Integracao.php` | `sei-guardrails-modulo` | `sei-gerador-scripts-release`, `sip-gerador-scripts-release`, `sei-testes-validacao` (conforme impacto) | instituicao, nome, versao inicial, integracao, pastas e ativacao documentados | exigir patch automatico no core |
| Validacao geral | auditoria de seguranca, revisao de permissoes, compliance, analise de risco operacional | `sei-guardrails-modulo` | `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores` (conforme escopo) | escopo, seguranca, entrada, saida, auditoria e transacao definidos; ver `.agents/security/matriz-vulnerabilidades-sei.md` | violar `AGENTS.md` ou escopo permitido |
| Hardening ou bugfix | seguranca, sanitizacao, refatoracao pontual, correcao de defeito | `sei-guardrails-modulo` | `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-controladores` (conforme artefato alterado) | escopo, seguranca, entrada, saida, auditoria e transacao definidos; ver `.agents/security/matriz-vulnerabilidades-sei.md` | violar `AGENTS.md` ou escopo permitido |
| Code review / security review | request contem diff, branch ou PR com arquivos em `modulos/**`; palavras "revise", "code review", "security review" | `sei-code-review-security` | `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores`, `sei-verificacao-tarefa`, `sei-guardrails-modulo`, `sei-testes-validacao` (conforme artefatos no diff) | diff/branch ou lista de arquivos + objetivo da mudanca | achado BLOQUEANTE aberto |
| Validacao e testes | lint, smoke, regressao, build, falha de teste | `sei-testes-validacao` | — | lista de arquivos PHP alterados e checks disponiveis | entrega PHP sem `php -l` executado |
| Descoberta ambigua | request nao deixa claro se precisa de API, evento ou operacao; intencao ambigua entre os 3 contratos do core | `sei-direcionador-integracao` | `sei-mod-api-classes`, `sei-mod-api-eventos`, `sei-mod-api-operacoes` (conforme escolha apos triagem) | desenvolvedor confirmou o caminho apos triagem | desenvolvedor nao confirmar o caminho |
