---
name: sei-revisao-tecnica
description: >
  Orquestra revisao tecnica, security review e conformidade de SEI sobre diff,
  PR, branch, commit, tag, arquivos, dimensao especifica ou modulo completo. Use
  para revisar gates, permissoes, transacoes, controladores, entrada e saida,
  seguranca, banco, release, integracoes, qualidade, testes e passivo tecnico.
  Atua somente em leitura, nao abre tarefas ou issues, nao avalia requisito,
  especificacao, regra de negocio ou produto e nunca chama code-review. Pedidos
  pelos nomes antigos sei-code-review-security, sei-revisao-codigo-seguranca,
  sei-revisao-pr e sei-security-review devem ser roteados textualmente para esta
  skill, sem adapters ou implementacoes extras.
---

# sei-revisao-tecnica

Orquestre uma verificacao tecnica pos-implementacao de codigo SEI, sempre em
somente leitura. Consolide evidencias dos gates especializados, classifique a
origem temporal dos achados e emita um parecer sem alterar arquivos, abrir
tarefas ou abrir issues.

## Limite de responsabilidade

Esta skill responde somente se a implementacao atende aos controles tecnicos do
repositorio e do ecossistema SEI.

- Nunca avalie aderencia a requisito, especificacao, regra de negocio, criterio
  de aceite, intencao de produto ou valor para o usuario.
- Nunca compare o codigo com uma spec, mesmo quando ela for fornecida.
- Nunca chame ou componha a skill `code-review`.
- Nao trate ausencia de spec como lacuna, risco, `WARN` ou `BLOCK`.
- Se o pedido misturar revisao tecnica e funcional, execute apenas a parte
  tecnica e declare a parte funcional fora do escopo.

## Roteamento textual antigo

Os nomes `sei-code-review-security`, `sei-revisao-codigo-seguranca`,
`sei-revisao-pr` e `sei-security-review` identificam pedidos que devem ser
roteados para `sei-revisao-tecnica` antes da classificacao. Eles nao autorizam
diretorio, frontmatter, copia, symlink ou adapter proprio.

## Fontes

- `AGENTS.md`, secoes `Escopo e Limites de Escrita`, `Guardrails Universais`,
  `Padrao Transacional Obrigatorio`, `Qualidade Minima` e `Roteamento`
- `.agents/references/roteamento-de-skills.md`, matriz e gates por artefato
- `.agents/references/gates-de-implementacao.md`, estados e gates G/R/C/D
- `.agents/references/mapa-modulos-scripts.md`, impacto de release por modulo
- `.agents/security/matriz-vulnerabilidades-sei.md`, vetores V01-V10
- `.agents/checklists/checklist-seguranca.md`, controles por artefato e C1-C10

Use `references/reutilizacao-rn-int-dto.md` quando houver funcao, metodo ou
classe nova ou alterada em RN, INT ou DTO. O exemplo completo de relatorio fica
em `examples/exemplo-relatorio-tecnico.md`.

## Entradas aceitas

Aceite qualquer uma destas entradas sem exigir documento funcional:

- diff fornecido ou diff da worktree
- PR identificado por numero, URL ou refs locais
- branch, intervalo de commits ou commit isolado
- tag isolada ou comparada com uma base declarada
- um ou mais arquivos
- uma dimensao tecnica especifica
- diretorio de modulo completo
- pedido explicito de revisao somente leitura, sem abertura de tarefas ou issues

Todas as entradas sao processadas em somente leitura. Nunca faca checkout,
altere refs, persista relatorio ou abra tarefa, issue ou PR durante a revisao.

Determine a base tecnica assim:

1. Para diff fornecido, use os lados informados.
2. Para PR, use as refs base e head fornecidas ou disponiveis localmente. Se nao
   estiverem acessiveis em leitura, use `NOT_EXECUTED` sem buscar ou alterar refs.
3. Para commit isolado, compare com o primeiro pai.
4. Para intervalo ou branch, use a base indicada; se ausente, use o merge-base
   disponivel e registre a escolha.
5. Para tag, use a base declarada; se ausente, compare o commit apontado pela tag
   com seu primeiro pai e registre a escolha.
6. Para arquivos sem base, revise o estado atual e marque a origem temporal como
   `incerto` quando o historico nao sustentar outra classificacao.
7. Para dimensao especifica, limite os achados a ela e a dependencias tecnicas
   indispensaveis. Marque as demais dimensoes como `NOT_APPLICABLE`, nunca como
   `PASS` por falta de analise.

## Escopo de modulo completo

Ao receber um diretorio de modulo, inclua:

- todos os `*Integracao.php` e seus controladores, eventos e contratos externos
- paginas PHP, JS e CSS que participem de entrada ou saida
- RN, INT, DTO, BD e DDL
- scripts de tarefa do modulo
- testes e validadores locais
- scripts SEI e SIP indicados em
  `.agents/references/mapa-modulos-scripts.md`, quando existirem
- versao declarada no `*Integracao.php` aplicavel

## Procedimento obrigatorio

1. Registre tipo de entrada, base tecnica, arquivos e dimensoes solicitadas.
2. Confira o escopo de escrita em `AGENTS.md`, secao `Escopo e Limites de
   Escrita`, sem presumir que todo arquivo fora de `modulos/**` viola G6.
3. Inventarie os artefatos antes de acionar gates. Em modulo completo, expanda o
   inventario conforme a secao anterior.
4. Acione todos os gates aplicaveis da tabela abaixo. Reaproveite evidencia
   anterior somente quando ela identificar comando, escopo, artefatos e saida.
5. Execute validadores locais seguros, como `audit.py` e `php -l`, quando
   previstos pelo gate e disponiveis. Use `release_check` somente para controles
   DB01-DB15 sobre objetos de dados extraidos de scripts.
6. Complete automacao com inspecao manual dos controles que ela nao cobre.
7. Avalie as doze dimensoes tecnicas e rastreie entradas ate SQL, HTML/JS, log,
   arquivo, desserializacao, redirect, chamada externa ou execucao.
8. Classifique cada achado como `introduzido`, `ampliado`, `preexistente` ou
   `incerto`, sempre contra a base tecnica registrada.
9. Exija cobertura positiva antes de atribuir `PASS`.
10. Execute a segunda passada obrigatoria sobre achados, gates e cobertura.
11. Emita o relatorio tecnico, os candidatos a tarefas e o parecer. Nao persista
    o relatorio, nao abra tarefa ou issue e nao altere codigo.

## Gates por artefato

| Artefato no escopo | Gate a acionar | Cobertura minima |
|---|---|---|
| `*_lista.php`, `*_cadastro.php` ou pagina PHP de acao | `sei-verificacao-pagina` | controles P aplicaveis, link, permissao, entrada, saida e encoding |
| `*RN.php` | `sei-verificacao-rn` | T1-T6 e A1-A3 aplicaveis, auditoria, transacao e pos-commit |
| `*BD.php`, DTO ou DDL | `sei-verificacao-banco-dados` | controles DB aplicaveis, mapeamento, SQL e multi-SGBD |
| controlador Ajax/WS ou `tratarLinkSemAssinatura` em `*Integracao.php` | `sei-verificacao-controladores` | controles CI aplicaveis e autorizacao por acao ou servico |
| `*_tarefa.php` ou definicao de tarefa | `sei-verificacao-tarefa` | controles K aplicaveis e unicidade |
| qualquer PHP no delta | `sei-testes-validacao` | `php -l`, encoding e checks locais disponiveis |
| DDL ou alteracao de modelo em script SEI/SIP | `sei-verificacao-banco-dados` com `release_check` | somente DB01-DB15 aplicaveis aos objetos extraidos |
| script SEI/SIP mapeado ou impacto de versao/recurso | inspecao tecnica de release desta skill | R1, R3, R4, R5 e R6, historico, switch e `getVersao()` aplicaveis |
| modulo completo ou padrao tecnico ambiguo | `sei-guardrails-modulo` | inventario, escopo e gates especializados acionados |

Acionar um gate significa carregar suas instrucoes, executar os checks
compativeis e incorporar a evidencia. Nao substitua o gate por uma avaliacao
informal desta skill.

## Inspecao tecnica de release

A dimensao Release pertence a esta skill, nao ao auditor de banco. Inspecione:

1. Scripts SEI e SIP existentes e o mapeamento do modulo.
2. Historico do arquivo para localizar a versao anterior e evitar duplicacao.
3. Blocos `switch` ou condicionais que selecionam instalacao e upgrades.
4. Sincronismo entre scripts e `getVersao()` do `*Integracao.php`.
5. Gates R1, R3, R4, R5 e R6 aplicaveis.

Quando o script contiver DDL, acione separadamente
`sei-verificacao-banco-dados` em `release_check` apenas para DB01-DB15. Nunca
atribua controles R, historico, `switch` ou `getVersao()` ao auditor de banco.

## Cobertura positiva e estados

Para cada gate aplicavel, registre artefatos inspecionados, controles executados,
evidencia e estado. Zero artefatos analisados nunca equivale a `PASS`.

| Estado | Uso |
|---|---|
| `PASS` | Ao menos um artefato compativel foi efetivamente inspecionado, todos os controles aplicaveis foram executados e nao houve desvio |
| `WARN` | Ha risco nao bloqueante, passivo preexistente sem agravamento ou heuristica inconclusiva que nao impede o parecer |
| `BLOCK` | Gate formal ou controle local bloqueante foi violado por achado introduzido ou ampliado e confirmado na segunda passada |
| `NOT_APPLICABLE` | Nao ha artefato compativel ou a dimensao esta explicitamente fora do escopo solicitado |
| `NOT_EXECUTED` | O gate e aplicavel, mas ferramenta, acesso ou evidencia insuficiente impediu sua execucao completa |

Um `PASS` deve citar o conjunto de arquivos e os IDs de controles verificados.
Para controles de ausencia, aceite como evidencia uma busca concluida sobre o
conjunto nomeado de arquivos. Saida automatizada com zero artefatos, check
interrompido ou amostra nao declarada resulta em `NOT_EXECUTED` ou `WARN`, nunca
em `PASS`.

Controle local com severidade `BLOQUEANTE`, mesmo sem gate G ou R formal, produz
`BLOCK` quando o achado for `introduzido` ou `ampliado` e permanecer confirmado
apos a segunda passada. Se o mesmo controle for comprovadamente `preexistente`
e nao houver agravamento, registre `WARN` e candidato a tarefa, sem bloquear o
parecer atual.

## Dimensoes tecnicas

Avalie e reporte estas dimensoes separadamente:

| Dimensao | Foco tecnico |
|---|---|
| Escopo | caminhos permitidos, core protegido e proposta documentada |
| Arquitetura | camadas SEI, DTO entre camadas, singletons e reaproveitamento tecnico |
| Permissoes | link assinado, autorizacao por acao, recurso SIP e auditoria RN |
| Transacao | `*Controlado`, `*Interno`, persistencia e efeitos apos commit |
| Controladores | dispatch Ajax/WS, whitelist e autorizacao especifica |
| Entrada/saida | normalizacao HTTP, sanitizacao, encoding e sinks |
| Seguranca | V01-V10, C1-C10, segredos, PII e fluxo exploravel |
| Banco | DTO/BD/DDL, SQL, chaves, nomes e multi-SGBD |
| Release | scripts existentes, versoes, recursos, parametros e tarefas |
| Integracoes | API oficial, eventos, operacoes, contratos e efeitos externos |
| Qualidade | clareza, coesao, acoplamento, complexidade, duplicacao e desempenho |
| Testes | lint, checks locais e cobertura tecnica do caminho alterado |

Qualidade limita-se a propriedades tecnicas observaveis. Nao julgue se o
comportamento implementado e o comportamento desejado.

## Classificacao temporal

| Classe | Criterio |
|---|---|
| `introduzido` | O desvio nasce no delta ou em arquivo novo |
| `ampliado` | O desvio ja existia, mas o delta aumenta alcance, exposicao, impacto ou dependencia |
| `preexistente` | O desvio esta comprovadamente na base e o delta nao o agrava |
| `incerto` | A base, o historico ou a relacao causal nao permitem classificacao segura |

Passivo `preexistente` sem agravamento nao produz `BLOCK` e nao bloqueia o
parecer da mudanca atual. Registre-o como `WARN` e candidato a tarefa. Achado
`ampliado` pertence a mudanca atual e pode produzir `BLOCK`. Achado `incerto`
nao deve ser promovido a bloqueio sem evidencia; use `analise humana` quando a
incerteza impedir conclusao tecnica.

Considere somente `TODO:` como marcador explicito de passivo. Ele nao bloqueia
por si so e nao dispensa os gates.

## Segunda passada obrigatoria

Antes do parecer:

1. Reabra cada `BLOCK`, `WARN` e classificacao `incerto` no contexto completo.
2. Confira protecoes anteriores, chamadores, fluxo alcancavel, base tecnica e
   regra de origem.
3. Tente derrubar o achado com evidencia contraria e remova falso positivo.
4. Confirme se o problema foi introduzido, ampliado ou apenas preexistia.
5. Revise o inventario para detectar gate ou dimensao aplicavel omitida.
6. Verifique se todo `PASS` possui cobertura positiva demonstrada.
7. Registre no relatorio que a segunda passada foi executada e quais
   classificacoes mudaram. Se nao houve mudanca, declare isso.

Achados de severidade `BLOQUEANTE` ou `ALTA` exigem `arquivo:linha`, regra de
origem e fluxo tecnico que sustente o risco. Evidencia inconclusiva permanece
`incerto`.

## Formato do relatorio

Use esta estrutura:

```text
## Escopo tecnico
Entrada: <diff|PR|branch/commit|tag|arquivos|dimensao|modulo>
Modo: somente leitura; nenhuma tarefa ou issue aberta
Base tecnica: <referencia>
Alvos exatos: <caminhos completos ou comando de diff>
Execucao autonoma: code-review nao acionada; spec nao carregada
Arquivos e dimensoes: <resumo>
Fora do escopo: requisito, especificacao, regra de negocio e produto nao avaliados

## Cobertura e gates
| Gate | Artefatos | Controles/evidencia | Estado |
| <skill> | <arquivos> | <IDs e evidencia> | PASS|WARN|BLOCK|NOT_APPLICABLE|NOT_EXECUTED |

## Dimensoes
| Dimensao | Estado | Evidencia ou risco residual |
| Escopo ... Testes | <estado> | <arquivo:linha, controle ou justificativa> |

## Achados tecnicos
- [<estado>][<severidade>][introduzido|ampliado|preexistente|incerto] <arquivo:linha> - <fato, origem e menor ajuste>

## Passivo preexistente
- [WARN][preexistente] <arquivo:linha> - <risco sem agravamento>

## Candidatos a tarefas
- [RT-01] Titulo: <titulo objetivo> | Prioridade/severidade: <prioridade e severidade> | Estado temporal: <introduzido|ampliado|preexistente> | Evidencia: <arquivo:linha e controle> | Risco: <impacto tecnico> | Acao minima: <acao> | Dependencia: <dependencia ou nenhuma> | Persistencia: nao realizada

## Segunda passada
Executada: sim. Alteracoes de classificacao: <lista ou nenhuma>.

## Parecer
**apto tecnicamente | apto com ajustes | bloquear tecnicamente | analise humana**
```

Omita secoes de achados ou passivo vazias, mas mantenha cobertura, dimensoes,
segunda passada e parecer. Se nao houver achado, declare:
`Nao encontrei desvios tecnicos relevantes no escopo efetivamente executado.`

Os candidatos a tarefas sao somente sugestoes no relatorio. Nao grave arquivo,
nao abra tarefa ou issue, nao altere backlog e nao invoque integracao externa.
Candidato a tarefa aceita somente estado temporal `introduzido`, `ampliado` ou
`preexistente`. Achado `incerto` permanece no relatorio e exige analise humana;
nao gere candidato ate resolver sua classificacao temporal.

## Regra do parecer

- `bloquear tecnicamente`: existe `BLOCK` introduzido ou ampliado apos a segunda
  passada.
- `analise humana`: existe `NOT_EXECUTED` aplicavel ou incerteza relevante que
  impede conclusao tecnica.
- `apto com ajustes`: nao ha `BLOCK`, mas existe `WARN`, inclusive passivo
  preexistente sem agravamento.
- `apto tecnicamente`: todos os gates e dimensoes no escopo estao em `PASS` ou
  `NOT_APPLICABLE`, com cobertura positiva para cada `PASS`.

## Limites

- Trabalhe somente em leitura. Nao altere codigo, documentacao, refs, backlog ou
  configuracao durante a revisao.
- Nao abra tarefa, issue ou PR nem persista relatorio ou candidato a tarefa.
- Nao invente controles; cite a fonte e a secao ou ID aplicavel.
- Nao dependa de servico externo para concluir. Se evidencia externa for
  indispensavel e indisponivel, use `NOT_EXECUTED`.
