# Roteamento de Skills e Contratos

Referencia cross-context: aplica-se ao Fluxo Direto e e carregada como extensao normativa pelo Spec Kit. Regras de governança dos comandos Spec Kit estao em `.specify/memory/constitution.md`.

## Regras Gerais — Fluxo Direto

- Identificar o tipo de demanda na matriz abaixo antes de escrever codigo.
- Acionar a skill principal listada; a orientacao dela prevalece em seu escopo.
- Verificar gates complementares aplicaveis ao artefato-alvo (DTO, RN, paginas, tarefas) usando as skills de gate listadas na coluna "Skills complementares".
- Se a demanda envolver release nos dois lados, acionar as duas skills de release: `sei-gerador-scripts-release` e `sip-gerador-scripts-release`.
- Para validacoes de seguranca, usar as skills canonicas por artefato (`sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-tarefa`, `sei-verificacao-controladores`).
- `sei-testes-validacao` e complementar em qualquer demanda com implementacao PHP ou risco operacional.
- `sei-tipagem-phpdoc` e opcional: so acionar quando o desenvolvedor pedir explicitamente tipagem, type hints, propriedades tipadas ou PHPDoc breve. Nao e gate obrigatorio nem skill de roteamento automatico.

## Matriz de Demanda

| Tipo de demanda | Evidencias | Skill principal | Skills complementares | Contrato obrigatorio | Gate |
| --- | --- | --- | --- | --- | --- |
| Novo CRUD InfraPHP via gerador | desenvolvedor optou por `sei-gerador-crud` para nova tabela/entidade; `DTO`, `RN`, `BD`, `INT`; paginas `*_lista.php` ou `*_cadastro.php` | `sei-gerador-crud` | `sei-verificacao-banco-dados`, `sei-verificacao-rn`, `sei-verificacao-pagina`, `sei-verificacao-tarefa` (conforme artefatos gerados) | JSON em `specs/<feature>/crud-contratos/<tabela>.json` | Bloquear se contrato pendente |
| Novo CRUD InfraPHP manual | desenvolvedor optou por nao usar o gerador; nova tabela/entidade; `DTO`, `RN`, `BD`, `INT`; paginas `*_lista.php` ou `*_cadastro.php` | `sei-guardrails-modulo` | `sei-verificacao-banco-dados`, `sei-verificacao-rn`, `sei-verificacao-pagina`, `sei-menu-pagina`, `sei-gerador-scripts-release`, `sip-gerador-scripts-release` (conforme impacto) | contrato funcional no `plan.md`: entidade, campos, permissoes, transacoes, release e criterios de aceite | Bloquear se entidade/campos/permissoes/release estiverem ambiguos; nao exigir `crud-contratos/` |
| Menu ou pagina | nova acao, pagina, item de menu, botao, icone, link de acao | `sei-menu-pagina` | `sei-verificacao-pagina` | contrato de acao: recurso SIP, perfil, menu, acao, parametros, permissao, link assinado | Bloquear se recurso/permissao/acao estiver indefinido |
| Evento | hook em `*Integracao`, menu externo, publicacoes, assinatura, envio, cancelamento | `sei-eventos` | `sei-api` (pre-condicao), `sei-verificacao-rn`, `sei-verificacao-controladores` (quando houver `processarControladorAjax*`, `tratarLinkSemAssinatura` ou controlador WS) | contrato de evento: nome do hook, assinatura, entrada, efeito colateral, transacao, auditoria | Bloquear se hook, efeito ou transacao estiver ambiguo |
| API ou WebService | operacao `SeiRN`, `Entrada*API`, `Saida*API`, WS, integracao externa | `sei-operacoes` | `sei-api` (pre-condicao), `sei-verificacao-controladores` (quando houver `processarControladorWebServices`) | contrato de operacao: classe de entrada/saida, metodo `SeiRN`, payload minimo, erros, autorizacao | Bloquear se usar classe interna sem justificativa ou payload ambiguo |
| Release SEI / BD | tabelas, colunas, indices, sequences, seeds, versao do script SEI | `sei-gerador-scripts-release` | `sei-verificacao-banco-dados` | contrato de release: versao alvo, script SEI, DDL multi-SGBD, seed, rollback | Bloquear se houver impacto BD/SEI sem plano de script |
| Release SIP | recursos, perfis, menus, auditoria, parametros, versao do script SIP | `sip-gerador-scripts-release` | `sei-verificacao-banco-dados` (quando houver DDL SIP) | contrato de release: versao alvo, script SIP, recursos/perfis/menus, auditoria, rollback | Bloquear se houver impacto SIP sem plano de script |
| Indexacao, pesquisa ou feed | Solr, pesquisa, feed de protocolos, publicacao, reindexacao, metadados pesquisaveis | `sei-guardrails-modulo` | — | contrato de indexacao: origem dos dados, momento de publicacao, transacao, reprocessamento, impacto em pesquisa | Bloquear se indexacao ocorrer dentro de transacao critica sem justificativa ou sem plano de reprocessamento |
| Novo modulo | nova pasta em `modulos/<inst>/<modulo>`, nova `*Integracao.php` | — | — | contrato de modulo: instituicao, nome, versao inicial, integracao, pastas, ativacao documentada | Bloquear se exigir patch automatico no core |
| Validacao geral | auditoria de seguranca, revisao de permissoes, compliance, analise de risco operacional | `sei-guardrails-modulo` | `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores` (conforme escopo) | checklist de escopo, seguranca, entrada, saida, auditoria e transacao; ver `.agents/security/matriz-vulnerabilidades-sei.md` | Bloquear se violar `AGENTS.md` ou escopo permitido |
| Hardening ou bugfix | seguranca, sanitizacao, refatoracao pontual, correcao de defeito | `sei-guardrails-modulo` | `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-controladores` (conforme artefato alterado) | checklist de escopo, seguranca, entrada, saida, auditoria e transacao; ver `.agents/security/matriz-vulnerabilidades-sei.md` | Bloquear se violar `AGENTS.md` ou escopo permitido |
| Validacao e testes | lint, smoke, regressao, build, falha de teste | `sei-testes-validacao` | — | lista de arquivos PHP alterados e checks disponiveis | Bloquear entrega sem `php -l` nos PHP alterados |

| Descoberta ambigua | demanda onde o desenvolvedor nao sabe se precisa de API, evento ou operacao; intencao ambigua entre os 3 contratos do core | `sei-direcionador-integracao` | `sei-api`, `sei-eventos`, `sei-operacoes` (conforme escolha do desenvolvedor apos triagem) | Intencao textual do desenvolvedor e correspondencia nos catalogos | Bloquear se o desenvolvedor nao confirmar o caminho |

## Alias Aceitos

- Se o desenvolvedor escrever `sei-crud-generator`, interpretar como `sei-gerador-crud`.
