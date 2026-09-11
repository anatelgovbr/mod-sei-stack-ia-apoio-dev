---
name: sei-revisao-tecnica
description: >
  Orquestra revisão técnica, security review e conformidade de SEI sobre diff,
  PR, branch, commit, tag, arquivos, dimensão específica ou módulo completo. Use
  para revisar gates, permissões, transações, controladores, entrada e saída,
  segurança, banco, release, integrações, qualidade, testes e passivo técnico.
  Não altera código, não abre tarefas ou issues, não avalia requisito,
  especificação, regra de negócio ou produto e nunca chama code-review. Entrega
  no formato padrão do template, e em formato alternativo como PDF, JSON ou
  texto de issue quando o desenvolvedor pedir. Pedidos pelos nomes antigos
  sei-code-review-security, sei-revisao-codigo-seguranca, sei-revisao-pr e
  sei-security-review devem ser roteados textualmente para esta skill, sem
  adapters ou implementações extras.
---

# sei-revisao-tecnica

Orquestre uma verificação técnica pós-implementação de código SEI. Consolide
evidências dos gates especializados, classifique a origem temporal dos achados e
emita um parecer sem alterar código, abrir tarefas ou abrir issues. A análise é
sempre em somente leitura; a única escrita permitida é o arquivo de formato
alternativo que o desenvolvedor pedir.

## Limite de responsabilidade

Esta skill responde somente se a implementação atende aos controles técnicos do
repositório e do ecossistema SEI.

- Nunca avalie aderência a requisito, especificação, regra de negócio, critério
  de aceite, intenção de produto ou valor para o usuário.
- Nunca compare o código com uma spec, mesmo quando ela for fornecida.
- Nunca chame ou componha a skill `code-review`.
- Não trate ausência de spec como lacuna, risco, `WARN` ou `BLOCK`.
- Se o pedido misturar revisão técnica e funcional, execute apenas a parte
  técnica e declare a parte funcional fora do escopo.

## Roteamento textual antigo

Os nomes `sei-code-review-security`, `sei-revisao-codigo-seguranca`,
`sei-revisao-pr` e `sei-security-review` identificam pedidos que devem ser
roteados para `sei-revisao-tecnica` antes da classificação. Eles não autorizam
diretório, frontmatter, copia, symlink ou adapter próprio.

## Fontes

- `AGENTS.md`, seções `Escopo e Limites de Escrita`, `Guardrails Universais`,
  `Padrao Transacional Obrigatorio`, `Qualidade Minima` e `Roteamento`
- `.agents/references/roteamento-de-skills.md`, matriz e gates por artefato
- `.agents/references/gates-de-implementacao.md`, estados e gates G/R/C/D
- `.agents/references/mapa-modulos-scripts.md`, impacto de release por módulo
- `.agents/security/matriz-vulnerabilidades-sei.md`, vetores V01-V10
- `.agents/checklists/checklist-seguranca.md`, controles por artefato e C1-C10
- skill `owasp-playbook`, vendorizada em `.agents/skills/owasp-playbook/`, procedimentos OWASP por CWE
- `.agents/security/mapa-seguranca-cwe-sei.md`, tradução de CWE para vetor, gate e estado deste repositório
- `templates/template-code-review.md`, formato padrão de saída do relatório
- `validar_relatorio.py`, validador de forma do relatório emitido

Use `references/reutilizacao-rn-int-dto.md` quando houver função, método ou
classe nova ou alterada em RN, INT ou DTO. Use
`.agents/security/mapa-seguranca-cwe-sei.md` sempre que a dimensão de segurança
estiver no escopo.

## Entradas aceitas

Aceite qualquer uma destas entradas sem exigir documento funcional:

- diff fornecido ou diff da worktree
- PR identificado por número, URL ou refs locais
- branch, intervalo de commits ou commit isolado
- tag isolada ou comparada com uma base declarada
- um ou mais arquivos
- uma dimensão técnica específica
- diretório de módulo completo
- pedido explícito de revisão somente leitura, sem abertura de tarefas ou issues

Todas as entradas são processadas em somente leitura. Nunca faça checkout,
altere refs ou abra tarefa, issue ou PR durante a revisão. A única gravação
permitida e a da seção `Formato alternativo a pedido`.

Determine a base técnica assim:

1. Para diff fornecido, use os lados informados.
2. Para PR, use as refs base e head fornecidas ou disponíveis localmente. Se não
   estiverem acessíveis em leitura, use `NOT_EXECUTED` sem buscar ou alterar refs.
3. Para commit isolado, compare com o primeiro pai.
4. Para intervalo ou branch, use a base indicada; se ausente, use o merge-base
   disponível e registre a escolha.
5. Para tag, use a base declarada; se ausente, compare o commit apontado pela tag
   com seu primeiro pai e registre a escolha.
6. Para arquivos sem base, revise o estado atual e marque a origem temporal como
   `incerto` quando o histórico não sustentar outra classificação.
7. Para dimensão específica, limite os achados a ela e a dependências técnicas
   indispensáveis. Marque as demais dimensões como `NOT_APPLICABLE`, nunca como
   `PASS` por falta de análise.

## Escopo de módulo completo

Ao receber um diretório de módulo, inclua:

- todos os `*Integracao.php` e seus controladores, eventos e contratos externos
- páginas PHP, JS e CSS que participem de entrada ou saída
- RN, INT, DTO, BD e DDL
- scripts de tarefa do módulo
- testes e validadores locais
- scripts SEI e SIP indicados em
  `.agents/references/mapa-modulos-scripts.md`, quando existirem
- versão declarada no `*Integracao.php` aplicável

## Procedimento obrigatório

1. Registre tipo de entrada, base técnica, arquivos e dimensões solicitadas.
2. Confira o escopo de escrita em `AGENTS.md`, seção `Escopo e Limites de
   Escrita`, sem presumir que todo arquivo fora de `modulos/**` viola G6.
3. Inventarie os artefatos antes de acionar gates. Em módulo completo, expanda o
   inventário conforme a seção anterior.
4. Acione todos os gates aplicáveis da tabela abaixo. Reaproveite evidência
   anterior somente quando ela identificar comando, escopo, artefatos e saída.
5. Execute validadores locais seguros, como `audit.py` e `php -l`, quando
   previstos pelo gate e disponíveis. Use `release_check` somente para controles
   DB01-DB15 sobre objetos de dados extraídos de scripts.
6. Complete automação com inspeção manual dos controles que ela não cobre.
7. Avalie as doze dimensões técnicas e rastreie entradas até SQL, HTML/JS, log,
   arquivo, desserialização, redirect, chamada externa ou execução. Na dimensão
   de segurança, acione `owasp-playbook` em chamada por skill, nomeando os
   plays e o escopo. A dimensão de segurança vale sempre, mesmo quando o pedido
   não cita segurança: revisão técnica completa inclui a passagem de segurança.
   Obtenha a lista obrigatória de plays e gates com
   `python3 .agents/skills/sei-revisao-tecnica/plays_aplicaveis.py <escopo>` e nomeie exatamente
   o que ele listar. Não decida por conta própria o que se aplica. `code-review-security`
   e `secrets-scan` rodam sempre; `owasp-top10-web-review` é obrigatório quando o
   escopo tem página de módulo ou `*Integracao.php` que despacha ação web;
   `api-security-review` quando houver controlador AJAX ou WebService;
   `agent-security-audit` quando o escopo tocar `AGENTS.md`, `CLAUDE.md`,
   `.agents/`, `.claude/`, `.claude-plugin/` ou `.github/`;
   `llm-risk-assess` e a parte estática de `prompt-injection-testing` quando
   houver arquivo de `modulos/ia/`; `sca-audit` quando a mudança adicionar ou
   alterar dependência. Play listado pelo script e não executado exige
   justificativa escrita no relatório, ao lado da linha. O relatório cita o
   caminho do arquivo de cada play seguido, para separar play executado de play
   lembrado. Traduza cada achado com
   `.agents/security/mapa-seguranca-cwe-sei.md`: CWE com controle local bloqueante
   violado vira `BLOCK`; CWE fora da tabela permanece `WARN`. Havendo PHP no
   escopo, use a seção `Auditores do projeto` do mapa na etapa
   Framework-Specific Checks do play, porque nenhum play cobre PHP. A saída do
   play é triagem, não achado: confirme o caminho do dado antes de reportar.
8. Classifique cada achado como `introduzido`, `ampliado`, `preexistente` ou
   `incerto`, sempre contra a base técnica registrada.
9. Exija cobertura positiva antes de atribuir `PASS`.
10. Execute a segunda passada obrigatória sobre achados, gates e cobertura.
11. Leia `templates/template-code-review.md` e escreva o relatório preenchendo
    as células do arquivo lido. Nunca reconstrua a estrutura de memória.
12. Grave o relatório em arquivo temporário fora do repositório, rode
    `validar_relatorio.py` sobre ele e corrija até exit 0. Esse arquivo é
    descartável e não conta como persistência do relatório.
13. Execute a conferência de forma obrigatória sobre os itens que o validador
    não cobre.
14. Emita o relatório no formato padrão, inteiro dentro de um único bloco de
    código cercado com a linguagem `markdown`. Não abra tarefa ou issue e não
    altere código. Havendo pedido de formato alternativo, cumpra também a seção
    `Formato alternativo a pedido` depois de emitir o padrão.

## Gates por artefato

| Artefato no escopo | Gate a acionar | Cobertura mínima |
|---|---|---|
| `*_lista.php`, `*_cadastro.php` ou página PHP de ação | `sei-verificacao-pagina` | controles P aplicáveis, link, permissão, entrada, saída e encoding |
| `*RN.php` | `sei-verificacao-rn` | T1-T6 e A1-A3 aplicáveis, auditoria, transação e pos-commit |
| `*BD.php`, DTO ou DDL | `sei-verificacao-banco-dados` | controles DB aplicáveis, mapeamento, SQL e multi-SGBD |
| controlador Ajax/WS ou `tratarLinkSemAssinatura` em `*Integracao.php` | `sei-verificacao-controladores` | controles CI aplicáveis e autorização por ação ou serviço |
| `*_tarefa.php` ou definição de tarefa | `sei-verificacao-tarefa` | controles K aplicáveis e unicidade |
| qualquer PHP no delta | `sei-testes-validacao` | `php -l`, encoding e checks locais disponíveis |
| DDL ou alteração de modelo em script SEI/SIP | `sei-verificacao-banco-dados` com `release_check` | somente DB01-DB15 aplicáveis aos objetos extraídos |
| script SEI/SIP mapeado ou impacto de versão/recurso | inspeção técnica de release desta skill | R1, R3, R4, R5 e R6, histórico, switch e `getVersao()` aplicáveis |
| módulo completo ou padrão técnico ambíguo | `sei-guardrails-modulo` | inventário, escopo e gates especializados acionados |
| artefato que recebe entrada externa, grava registro de alguem, expoe ponto de entrada, chama sistema externo, guarda credencial ou grava log | `owasp-playbook` mais `.agents/security/mapa-seguranca-cwe-sei.md` | CWE aplicáveis traduzidos para vetor e gate, com caminho do dado demonstrado em cada achado confirmado |

Acionar um gate significa carregar suas instruções, executar os checks
compatíveis e incorporar a evidência. Não substitua o gate por uma avaliação
informal desta skill.

## Inspeção técnica de release

A dimensão Release pertence a esta skill, não ao auditor de banco. Inspecione:

1. Scripts SEI e SIP existentes e o mapeamento do módulo.
2. Histórico do arquivo para localizar a versão anterior e evitar duplicação.
3. Blocos `switch` ou condicionais que selecionam instalação e upgrades.
4. Sincronismo entre scripts e `getVersao()` do `*Integracao.php`.
5. Gates R1, R3, R4, R5 e R6 aplicáveis.

Quando o script contiver DDL, acione separadamente
`sei-verificacao-banco-dados` em `release_check` apenas para DB01-DB15. Nunca
atribua controles R, histórico, `switch` ou `getVersao()` ao auditor de banco.

## Cobertura positiva e estados

Para cada gate aplicável, registre artefatos inspecionados, controles executados,
evidência e estado. Zero artefatos analisados nunca equivale a `PASS`.

| Estado | Uso |
|---|---|
| `PASS` | Ao menos um artefato compatível foi efetivamente inspecionado, todos os controles aplicáveis foram executados e não houve desvio |
| `WARN` | Há risco não bloqueante, passivo preexistente sem agravamento ou heurística inconclusiva que não impede o parecer |
| `BLOCK` | Gate formal ou controle local bloqueante foi violado e confirmado na segunda passada, por achado introduzido ou ampliado quando há delta, ou por achado de qualquer origem quando não há delta |
| `NOT_APPLICABLE` | Não há artefato compatível ou a dimensão está explicitamente fora do escopo solicitado |
| `NOT_EXECUTED` | O gate é aplicável, mas ferramenta, acesso ou evidência insuficiente impediu sua execução completa |

No relatório, os cinco estados entram nas três células que o template oferece:

| Estado do gate | Como aparece no template |
|---|---|
| `PASS` | linha do gate com `✅ PASS` |
| `WARN` | linha do gate com `⚠️ WARN` |
| `BLOCK` | linha do gate com `❌ BLOCK` |
| `NOT_APPLICABLE` | não vira linha; declare a ausência de artefato em uma frase antes da tabela |
| `NOT_EXECUTED` | linha do gate com `❌ BLOCK`, porque gate aplicável que não pode ser executado falha fechado |

Um `PASS` deve citar o conjunto de arquivos e os IDs de controles verificados.
Para controles de ausência, aceite como evidência uma busca concluida sobre o
conjunto nomeado de arquivos. Saída automatizada com zero artefatos, check
interrompido ou amostra não declarada resulta em `NOT_EXECUTED` ou `WARN`, nunca
em `PASS`.

Controle local com severidade `BLOQUEANTE`, mesmo sem gate G ou R formal, produz
`BLOCK` quando o achado permanecer confirmado após a segunda passada. Havendo
delta, o achado `preexistente` sem agravamento vira `WARN` e candidato a tarefa,
sem bloquear o parecer atual.

## Dimensões técnicas

Avalie e reporte estas dimensões separadamente:

| Dimensão | Foco técnico |
|---|---|
| Escopo | caminhos permitidos, core protegido e proposta documentada |
| Arquitetura | camadas SEI, DTO entre camadas, singletons e reaproveitamento técnico |
| Permissões | link assinado, autorização por ação, recurso SIP e auditoria RN |
| Transação | `*Controlado`, `*Interno`, persistência e efeitos após commit |
| Controladores | dispatch Ajax/WS, whitelist e autorização específica |
| Entrada/saída | normalização HTTP, sanitização, encoding e sinks |
| Segurança | V01-V10, C1-C10, segredos, PII e fluxo explorável |
| Banco | DTO/BD/DDL, SQL, chaves, nomes e multi-SGBD |
| Release | scripts existentes, versões, recursos, parâmetros e tarefas |
| Integrações | API oficial, eventos, operações, contratos e efeitos externos |
| Qualidade | clareza, coesão, acoplamento, complexidade, duplicação e desempenho |
| Testes | lint, checks locais e cobertura técnica do caminho alterado |

Qualidade limita-se a propriedades técnicas observáveis. Não julgue se o
comportamento implementado é o comportamento desejado.

## Classificação temporal

| Classe | Critério |
|---|---|
| `introduzido` | O desvio nasce no delta ou em arquivo novo |
| `ampliado` | O desvio já existia, mas o delta aumenta alcance, exposição, impacto ou dependência |
| `preexistente` | O desvio está comprovadamente na base e o delta não o agrava |
| `incerto` | A base, o histórico ou a relação causal não permitem classificação segura |

Havendo delta, passivo `preexistente` sem agravamento não produz `BLOCK` e não
bloqueia o parecer da mudança atual. Registre-o como `WARN` e candidato a tarefa.
Achado `ampliado` pertence à mudança atual e pode produzir `BLOCK`. Achado
`incerto` não deve ser promovido a bloqueio sem evidência; use `analise humana`
quando a incerteza impedir conclusão técnica.

Não havendo delta, como em revisão de módulo completo ou de arquivos sem base de
comparação, o estado do achado reflete o controle violado, e a coluna `Origem`
continua registrando `preexistente`. A proteção do passivo antigo existe para não
bloquear uma mudança em revisão, e sem mudança não há o que proteger.

Considere somente `TODO:` como marcador explícito de passivo. Ele não bloqueia
por si só e não dispensa os gates.

## Segunda passada obrigatória

Antes do parecer:

1. Reabra cada `BLOCK`, `WARN` e classificação `incerto` no contexto completo.
2. Confira proteções anteriores, chamadores, fluxo alcançável, base técnica e
   regra de origem.
3. Tente derrubar o achado com evidência contrária e remova falso positivo.
4. Confirme se o problema foi introduzido, ampliado ou apenas preexistia.
5. Revise o inventário para detectar gate ou dimensão aplicável omitida.
6. Verifique se todo `PASS` possui cobertura positiva demonstrada.
7. Registre a segunda passada na coluna `Evidencia` do gate afetado, ou na
   coluna `Achado` da linha reclassificada. Se não houve mudança de
   classificação, declare isso na linha do gate correspondente.

Achados de severidade `BLOQUEANTE` ou `ALTA` exigem `arquivo:linha`, regra de
origem e fluxo técnico que sustente o risco. Evidência inconclusiva permanece
`incerto`.

## Formato padrão do relatório

Este é o formato que sai quando o desenvolvedor não pede outro. Sem pedido
explícito de formato alternativo, entregue só ele.

O formato de saída é `templates/template-code-review.md`, fonte única. Leia o
arquivo a cada revisão, antes de escrever, e preencha as células dele. A leitura
continua obrigatória quando a revisão repete um escopo já revisado na sessão,
quando o pedido é para refazer um relatório e quando a evidência é reaproveitada.
Não reproduza a estrutura aqui, não acrescente seção que o template não tenha e
não troque os valores das colunas, que estão escritos nas próprias células.

O template tem cinco seções, nesta ordem: título `Revisao tecnica`, `Resultado`
logo abaixo do título, cabeçalho com `Escopo` e `Revisao gerada por`,
`Gates acionados`, `Achados` e `Passo a passo do achado`. `Resultado` é a
primeira coisa que o leitor vê.

Emita o relatório inteiro dentro de um único bloco de código cercado com a
linguagem `markdown`, sem texto antes ou depois do bloco. O terminal desenha
tabela Markdown com bordas gráficas, e a cópia dessa tela cola errado no GitLab.
Dentro do bloco, a cópia preserva as barras verticais e cola certo.

````markdown
```markdown
## Revisao tecnica

### Resultado

❌ BLOCKED

**Escopo**: ...
```
````

Coloque o conteúdo desta skill assim:

| Conteúdo produzido pela skill | Onde entra no template |
|---|---|
| gate acionado, com artefatos, controles e evidência | uma linha em `Gates acionados`, uma por gate |
| gate aplicável sem artefato no escopo | não vira linha; declare a ausência em uma frase antes da tabela só quando o leitor puder achar que o gate foi esquecido |
| achado, com estado, severidade, origem temporal e local | uma linha em `Achados` |
| menor ajuste e candidato a tarefa | coluna `Menor ajuste` da linha do achado; não abra seção de candidatos |
| resultado da segunda passada e reclassificação | coluna `Evidencia` do gate afetado, ou coluna `Achado` da linha reclassificada |
| passivo preexistente | linha em `Achados` com origem `preexistente`; não abra seção de passivo |
| rastro de achado `BLOCK` ou de severidade `ALTA` | `Passo a passo do achado`, em linha de setas ou em tópicos, com `arquivo:linha` em cada salto |
| parecer técnico | `Resultado` |

Achado sem rastro do dado demonstrado não entra como confirmado: reporte como
hipótese na coluna `Achado`, com a severidade que a evidência sustenta.

Se não houver achado, mantenha a tabela `Achados` vazia e escreva logo abaixo do
titulo `Achados` a frase:
`Nao encontrei desvios tecnicos relevantes no escopo efetivamente executado.`

### Limite de cada célula

Célula longa deixa a linha da tabela ilegível no bloco de código e no GitLab.
Os limites abaixo mantêm cada linha curta.

| Célula | Conteúdo aceito | Limite |
|---|---|---|
| `Escopo` | caminho do escopo e contagem por tipo de arquivo, como `.../abc/exemplo (8 PHP, 3 PNG, 2 SVG)`; a base técnica entra só quando há delta | uma linha |
| `Revisao gerada por` | `sei-revisao-tecnica` ou `leitura manual` | uma linha |
| frase de gate sem artefato | os gates `NOT_APPLICABLE` e o motivo da ausência de artefato | uma frase, antes da tabela de gates |
| coluna `Gate` | ID do gate com rótulo curto, como `G1 encoding`, ou nome da skill de gate | até 6 palavras |
| coluna `Artefatos` | grupo nomeado, como `8 arquivos PHP` ou `5 paginas *_lista.php`; lista de nomes só com até 3 arquivos | até 6 palavras |
| coluna `Estado` do gate | só `✅ PASS`, `⚠️ WARN` ou `❌ BLOCK` | um valor |
| coluna `Evidencia` | IDs de controle, contagem e veredito, em fragmentos separados por ponto e vírgula, sem frase narrativa | até 30 palavras |
| coluna `Estado` do achado | só `✅ PASS`, `⚠️ WARN` ou `❌ BLOCK` | um valor |
| coluna `Severidade` | só `BLOQUEANTE`, `ALTA`, `MEDIA` ou `BAIXA` | um valor |
| coluna `Origem` | só `introduzido`, `ampliado`, `preexistente` ou `incerto` | um valor |
| coluna `Local` | `arquivo:linha`, aceitando até um segmento de diretório, como `rn/MdAbcTesteRN.php:16` | um par |
| coluna `Achado` | o desvio afirmado, mais vetor, gate e CWE aplicáveis | até 2 frases e 30 palavras |
| coluna `Menor ajuste` | a ação de correção, no imperativo | uma frase, até 15 palavras |
| seção `Passo a passo do achado` | saltos do dado, aceitando o atalho `:linha` depois de o arquivo já ter sido nomeado na mesma linha | uma linha de setas por achado |
| seção `Resultado` | só `✅ PASS` ou `❌ BLOCKED`, sem o nome do parecer anexado | uma linha |

Os gates universais `G1`, `G2` e `G6` entram como linha própria na tabela quando
executados, além das linhas das skills de gate.

Quando o mesmo controle for violado em vários
arquivos, abra uma linha por arquivo, com `Local` no primeiro ponto daquele
arquivo e a contagem das demais ocorrências na coluna `Achado`.

### Lugar único de cada fato

Cada fato entra em uma célula só.

| Fato | Célula única |
|---|---|
| comando executado, saída e IDs de controle | coluna `Evidencia` do gate |
| resultado da segunda passada e falso positivo derrubado | coluna `Evidencia` do gate, ou coluna `Achado` da linha reclassificada |
| rastro do dado, da entrada até o ponto de uso | seção `Passo a passo do achado` |
| base técnica e refs comparadas | campo `Escopo` |
| ressalva sobre alcance do parecer | coluna `Achado` da linha que a sustenta |

Não repita evidência nem rastro dentro da coluna `Achado`. Não escreva nenhuma
ressalva, nota ou parágrafo fora das células acima.

O relatório padrão não é persistido. Não grave arquivo, não abra tarefa, issue
ou PR, não altere backlog e não invoque integração externa. A exceção está na
seção `Formato alternativo a pedido`.

## Formato alternativo a pedido

O desenvolvedor pode pedir a mesma revisão em outro formato, por exemplo PDF,
JSON de achados, texto de issue pronto para colar ou descrição de Merge Request.
Atenda o pedido. Sem pedido, não ofereça e não gere nada além do formato padrão.

O que muda é só a embalagem. Gates acionados, achados, severidade, origem
temporal, segunda passada e parecer são os mesmos do formato padrão.

| Regra | Como aplicar |
|---|---|
| Ordem | Escreva primeiro o relatório no formato padrão e valide com `validar_relatorio.py` até exit 0. O formato alternativo deriva dele |
| Substituição | O formato alternativo nunca substitui o padrão. Emita os dois na mesma resposta |
| Números | Achado, contagem e severidade vem do relatório padrão já validado. Não recalcule nada durante a geração |
| Gravação | Grave o arquivo do formato alternativo no caminho que o desenvolvedor indicar. Sem indicação, use `specs/`, que é local e não versionada |
| Limite | Gerar o texto de uma issue em arquivo não é abrir issue. Continua proibido abrir tarefa, issue ou PR, alterar código, refs ou backlog |
| Segredo | Mascare segredo e PII no arquivo gerado, com o mesmo critério do relatório padrão |

Um pedido de formato alternativo autoriza a gravação daquele arquivo e nada
mais. Ele não afrouxa nenhuma outra regra desta skill.

## Conferência de forma obrigatória

Confira cada item contra o texto já escrito, nunca contra a lembrança das
regras. Item reprovado exige corrigir a forma antes de emitir.

1. `templates/template-code-review.md` foi lido nesta revisão, e o relatório
   preenche as células do arquivo lido.
2. O relatório tem exatamente as cinco seções do template, nesta ordem, com
   `Resultado` logo abaixo do título, sem seção, subtítulo, nota de rodapé ou
   apêndice extra.
3. Fora das células do template e da frase de gate sem artefato, o relatório não
   tem nenhum parágrafo de texto corrido.
4. `Escopo` e `Revisao gerada por` ocupam uma linha cada.
5. A frase de gate sem artefato tem uma frase, fica antes da tabela de gates e
   não traz base técnica, achado nem evidência.
6. Cada célula respeita a tabela `Limite de cada célula`.
7. A coluna `Local` traz `arquivo:linha` sem caminho de diretório, salvo quando
   dois arquivos do escopo tiverem o mesmo nome.
8. Nenhum fato aparece em duas células, conforme `Lugar único de cada fato`.
9. A seção `Resultado` fica logo abaixo do título e tem uma linha, com o valor
   do template e nada mais. O nome do parecer não entra.
10. Nenhuma célula passa do limite de palavras.
11. `validar_relatorio.py` retornou exit 0 sobre o relatório já escrito.
12. O relatório inteiro está dentro de um único bloco de código cercado com a
    linguagem `markdown`, sem texto antes ou depois do bloco.

## Validador de forma

```bash
python3 .agents/skills/sei-revisao-tecnica/validar_relatorio.py <relatorio.md>
```

| Code | Significado |
|---|---|
| 0 | PASS, forma conforme o template |
| 1 | WARN, prosa fora de célula |
| 2 | BLOCK, inclusive arquivo inexistente, vazio ou sem as seções do template |

O validador cobre seções e ordem, cabeçalho e número de colunas, valores fechados
de estado, severidade e origem, formato de `Local`, limite de palavras por coluna,
âncora `arquivo:linha` nos saltos e prosa fora de célula. Ele aceita o relatório
com ou sem o bloco de código `markdown` externo. Os demais itens da conferência
de forma continuam manuais.

### Testes

```bash
cd .agents/skills/sei-revisao-tecnica && python3 -m unittest test_validar_relatorio
```

O teste `test_exemplo_aprovado_passa` fixa o padrão acordado. Regra nova que
reprove esse exemplo quebra o teste.

## Regra do parecer

Determine o parecer técnico pela condição, e escreva na seção `Resultado` só o
valor que o template oferece. O nome do parecer orienta a escolha e não entra no
relatório.

| Parecer técnico | Condição | Linha em `Resultado` |
|---|---|---|
| `bloquear tecnicamente` | existe `BLOCK` após a segunda passada, introduzido ou ampliado quando há delta, de qualquer origem quando não há delta | `❌ BLOCKED` |
| `analise humana` | existe `NOT_EXECUTED` aplicável ou incerteza relevante que impede conclusão técnica | `❌ BLOCKED` |
| `apto com ajustes` | não há `BLOCK`, mas existe `WARN`, inclusive passivo preexistente sem agravamento | `✅ PASS` |
| `apto tecnicamente` | todos os gates e dimensões no escopo estão em `PASS` ou `NOT_APPLICABLE`, com cobertura positiva para cada `PASS` | `✅ PASS` |

## Limites

- A análise é somente leitura. Não altere código, documentação, refs, backlog ou
  configuração durante a revisão.
- Não abra tarefa, issue ou PR. Persista arquivo somente no formato alternativo
  que o desenvolvedor pedir, conforme a seção `Formato alternativo a pedido`.
- Não invente controles; cite a fonte e a seção ou ID aplicável.
- Não dependa de serviço externo para concluir. Se evidência externa for
  indispensável e indisponível, use `NOT_EXECUTED`.
