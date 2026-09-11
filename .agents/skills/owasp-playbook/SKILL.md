---
name: owasp-playbook
description: >
  Revisao de seguranca por procedimento do OWASP Secure Agent Playbook. Uso
  direto em uma frase, sem conhecer seguranca: "revise a seguranca das minhas
  alteracoes", "tem senha exposta", "auditoria completa", "vou implementar X,
  o que preciso cuidar". Tambem e chamada por outra skill com os plays
  nomeados. Escolhe os plays pelos sinais presentes no escopo, infere o
  escopo, roda os auditores que o projeto registrou na ponte, traduz cada
  achado pela ponte do projeto e entrega resumo em linguagem simples antes da
  tabela tecnica. Cobre codigo, API, dependencia, segredo, infraestrutura como
  codigo, mobile, configuracao de agente de IA, servidor MCP, aplicacao LLM e
  requisito ASVS para codigo novo. Agnostica de linguagem e de projeto. Nao
  usar por roteamento automatico.
disable-model-invocation: false
license: CC-BY-4.0 no playbook e CC-BY-SA-4.0 nos dados OWASP. Ver upstream/LICENSE.md e upstream/THIRD_PARTY_NOTICES.md
---

# owasp-playbook

Ponte entre o OWASP Secure Agent Playbook, copiado sem modificacao em `upstream/`, e o repositorio onde a skill esta instalada. Esta skill nao contem procedimento de seguranca proprio e nao contem nada do projeto: ela escolhe os plays, executa o que esta escrito neles e traduz o resultado pela ponte que o projeto registrar. O mesmo `SKILL.md` serve a qualquer repositorio.

## Dois modos de entrada

| Modo | Quando | O que vale |
|---|---|---|
| Direto | O desenvolvedor chama a skill com uma frase, sem nomear play | Tabela de intencao escolhe o modo ou o play, o escopo e inferido, os sinais do escopo escolhem os plays, e a saida abre com o resumo em linguagem simples |
| Chamada por skill | Outra skill nomeia os plays e o escopo | Pule intencao, escopo e sinais. Execute os plays nomeados, traduza pela ponte e devolva no formato que a skill chamadora pede |

## Regras fixas, nos dois modos

1. Nunca edite arquivo dentro de `upstream/`. E copia literal do projeto de origem, substituida inteira na atualizacao. O procedimento esta na documentacao de manutencao da stack do repositorio.
2. Somente leitura. Nao altere codigo, nao abra tarefa, issue ou PR. Correcao e outra tarefa; ver "Depois do relatorio".
3. Sem rede. Os templates do upstream sugerem chamar a API do OpenCRE; nao chame. A ficha local esta em `upstream/data/opencre/`.
4. Uma escala de severidade: `BLOQUEANTE`, `ALTA`, `MEDIA`, `BAIXA`. Se a ponte do projeto tiver a linha do achado, a severidade dela vale. Sem linha, converta a do play: `CRITICAL` vira `BLOQUEANTE`, `HIGH` vira `ALTA`, `MEDIUM` vira `MEDIA`, `LOW` e `INFORMATIONAL` viram `BAIXA`.
5. Triagem nao e achado. Item so vira confirmado com o caminho do dado demonstrado, da entrada ate o ponto de uso, citando arquivo e linha de cada salto. Sem esse rastro, e "precisa de conferencia".
6. Segredo real nunca aparece em texto claro na evidencia. Mascare.
7. Ignore diretorio de dependencia instalada, como `vendor/` e `node_modules/`, e a pasta `upstream/` em todo play, exceto `sca-audit`.
8. Play sem alvo nao roda. Responda em uma frase por que nao se aplica.
9. Teste dinamico, que envia entrada a uma aplicacao em execucao, so roda com tres coisas na frase do desenvolvedor: o alvo em execucao, a garantia de que nao e producao e a autorizacao explicita. Sem as tres, o play roda so a parte estatica, sobre o codigo, e o relatorio diz que o teste dinamico nao rodou e o que falta para rodar.

## Ponte do projeto

A ponte e o unico lugar onde o projeto entra. E um arquivo Markdown do repositorio, fora desta skill. Encontre-a nesta ordem:

1. O item do `AGENTS.md` que cita `owasp-playbook` e aponta um arquivo em `.agents/security/`. Esse arquivo e a ponte.
2. Sem esse item, `.agents/security/guia-seguranca.md`, se existir: a ponte e o proprio guia, e a traducao usa a tabela de rastreio CWE dele.
3. Sem nenhum dos dois, nao ha ponte. Reporte com o CWE, a referencia OWASP e a severidade convertida do play. Diga no relatorio que o projeto nao tem ponte registrada.

A ponte e lida por secao. Cada secao e opcional e tem um comportamento fixo quando falta:

| Secao da ponte | O que a skill le | Sem a secao |
|---|---|---|
| `## Traducao` | tabela de CWE para controle local, severidade, gate, estado e secao ASVS | usa CWE, referencia OWASP e severidade convertida do play |
| `## Sinais do projeto` | tabela de sinal do projeto para play, alem dos sinais genericos abaixo | so os sinais genericos |
| `## Auditores do projeto` | comandos a rodar na etapa Framework-Specific Checks do play | a etapa roda so com o conteudo generico do play, e o relatorio diz isso em uma frase |
| `## Excecoes` | o que nao e achado neste repositorio | nenhuma excecao |
| `## Saidas opcionais` | gerador de PDF, de issues ou outro formato do projeto | so o JSON de findings e o texto das issues |
| `## Correcao` | para onde rotear o pedido de correcao | "peca a correcao citando o achado" |

Acento no titulo da secao nao importa: a secao e reconhecida com ou sem acento.

## Modo direto

### Tabela de intencao

Decida em duas etapas. Primeiro o tipo de pedido, que define o modo. Depois o objeto citado, que acrescenta plays e define o escopo padrao. Classifique pelo sentido da frase: as palavras nas tabelas sao exemplos, nao lista fechada, e valem em qualquer lingua. Nao pergunte qual play usar.

**Etapa 1, tipo de pedido.** Um so. Percorra na ordem e pare no primeiro que casar.

| Tipo de pedido | Como reconhecer | Modo |
|---|---|---|
| Vai construir algo | verbo no futuro ou pedido de orientacao antes do codigo: "vou implementar", "vou criar", "como faco", "o que preciso cuidar", "que requisito vale" | `security-guidance`, ver "Requisito ASVS". Nenhum play roda |
| Quer saber o que existe | "o que da para verificar", "quais verificacoes", "o que voce consegue checar" | inventario: tabela de sinais aplicada ao repositorio, sem executar play |
| Quer tudo | "auditoria completa", "revise tudo", "repositorio inteiro", "de ponta a ponta" | modo completo |
| Quer procurar uma coisa especifica | pergunta sobre um objeto da etapa 2, sem pedir revisao geral: "tem senha exposta?", "as dependencias tem CVE?", "a API e segura?" | so os plays do objeto, no escopo padrao do objeto |
| Quer revisar codigo | "revise a seguranca", "esta seguro", "antes de entregar", "antes do merge", ou nenhuma das anteriores | modo padrao, mais os plays do objeto citado, se houver |

**Etapa 2, objeto citado.** Zero, um ou varios. Cada objeto acrescenta seus plays, e objetos se somam.

| Objeto | Como aparece na frase | Plays | Escopo padrao, quando a frase nao cita caminho |
|---|---|---|---|
| Credencial | senha, chave, token, segredo, credencial, `.env`, "vazou" | `secrets-scan` | repositorio inteiro |
| Dependencia | dependencia, biblioteca, pacote, vendor, CVE, "versao vulneravel" | `sca-audit` | manifestos, lockfiles e diretorios vendorizados do repositorio |
| API | API, endpoint, webservice, SOAP, REST, GraphQL, "integracao que expoe" | `api-security-review` | arquivos que definem rota, endpoint ou servico |
| Aplicacao web contra o Top 10 | "OWASP Top 10", "top 10" | `owasp-top10-web-review` | aplicacao ou modulo citado; sem citacao, repositorio inteiro com aviso |
| Infraestrutura | infraestrutura, Terraform, Kubernetes, Helm, CloudFormation, container, Docker, nuvem | `iac-security-review` | arquivos de infraestrutura como codigo |
| Aplicativo movel | aplicativo, app, Android, iOS, mobile, Flutter | `mobile-code-review` | projeto movel |
| Servidor MCP | MCP, "servidor MCP", "ferramenta do agente" | `mcp-server-review` | configuracao e codigo de MCP |
| Aplicacao com LLM | chat, assistente, prompt, modelo de linguagem, LLM, RAG, "o modulo de IA" | `llm-risk-assess` e a parte estatica de `prompt-injection-testing`, sempre juntos. Com "injecao de prompt", "testar o chat" ou "red team" mais alvo em execucao e autorizacao, tambem a parte dinamica | codigo que chama modelo de linguagem |
| Configuracao dos agentes de IA | "agentes de IA", Copilot, Claude, OpenCode, Cursor, "stack de IA", `AGENTS.md`, "instrucoes do agente" | `agent-security-audit` | `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.github/`, `.opencode/`, `.cursor/` |
| Agente autonomo | "agente autonomo", agentico, "laco de ferramentas" | `agentic-ai-risk-assess`; com "varios agentes", multiagente ou MAESTRO, tambem `multi-agentic-threat-model` | codigo do agente |
| Verificacao AISVS | AISVS | `ai-security-verification` | aplicacao de IA citada |

**Desempate.**

- "IA" sozinho e ambiguo entre aplicacao com LLM e configuracao dos agentes. Resolva pelos sinais do repositorio: codigo que chama modelo de linguagem leva a `llm-risk-assess`; so configuracao de agente leva a `agent-security-audit`; os dois presentes, os dois plays.
- Palavra de objeto dentro de pedido de construcao nao vira play: "vou implementar a troca de senha" e `security-guidance`, nao `secrets-scan`.
- Palavra de objeto no sentido tecnico do dominio nao vira play: "chave primaria", "token de sessao do framework" e "pacote de instalacao" so contam quando a pergunta e sobre exposicao, vulnerabilidade ou seguranca daquele objeto.
- Frase com caminho, modulo ou branch citado: o caminho vale como escopo, e os plays vem dos sinais do escopo mais o objeto citado.
- Objeto citado sem alvo no repositorio: nao rode o play; responda em uma frase que nao se aplica e por que.
- Nada reconhecido: modo padrao, e o relatorio diz qual foi a suposicao.

### Escopo

Se o tipo de pedido for procurar uma coisa especifica e a frase nao citar caminho, o escopo e o escopo padrao do objeto, na tabela da etapa 2. Nos demais casos, ordem fixa. Pare na primeira que existir e abra o relatorio dizendo qual foi.

1. Caminho, modulo, arquivo ou branch citado na frase.
2. Mudancas nao commitadas, por `git status` e `git diff`.
3. Branch atual contra a branch principal do repositorio.
4. Repositorio inteiro. Avise que e grande e proponha recorte antes de seguir.

Nao faca outra pergunta ao desenvolvedor. Assuma o padrao, registre a suposicao e siga.

### Sinais genericos

Cada play tem um sinal. Se o sinal aparece no escopo, o play roda. A ponte pode acrescentar sinais do projeto na secao `## Sinais do projeto`.

| Play | Sinal no escopo | Quando roda |
|---|---|---|
| `code-review-security` | qualquer arquivo de codigo-fonte | sempre que o escopo tiver codigo |
| `secrets-scan` | qualquer arquivo, inclusive configuracao e script | sempre |
| `sca-audit` | manifesto ou lockfile de dependencia (`package.json`, `package-lock.json`, `composer.json`, `composer.lock`, `requirements.txt`, `pyproject.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `Cargo.toml`) ou diretorio de dependencia vendorizada | por sinal |
| `api-security-review` | especificacao OpenAPI, Swagger ou WSDL; arquivo que define rota, endpoint, controlador de API ou servico SOAP, REST ou GraphQL | por sinal |
| `owasp-top10-web-review` | aplicacao web | so por intencao |
| `iac-security-review` | `*.tf`, `*.tfvars`, manifesto Kubernetes com `apiVersion:` e `kind:`, Helm chart, CloudFormation com `AWSTemplateFormatVersion`, `Dockerfile`, `docker-compose` | por sinal |
| `mobile-code-review` | `AndroidManifest.xml`, `build.gradle` de aplicativo, `*.xcodeproj`, `Info.plist`, `pubspec.yaml` com Flutter | por sinal |
| `mcp-server-review` | `.mcp.json`, chave `mcpServers` em configuracao, codigo que usa SDK de MCP | por sinal |
| `llm-risk-assess` | codigo que chama provedor de LLM por SDK ou HTTP, template de prompt, pipeline de RAG, endpoint de chat | por sinal |
| `prompt-injection-testing` | mesmo sinal de LLM: entrada de chat, template de prompt, ingestao de documento, ferramenta chamada pelo modelo | por sinal, parte estatica: etapa 1 do play, mapa das superficies de entrada, e revisao das defesas do codigo contra cada tecnica e evasao. Parte dinamica so pela regra fixa 9 |
| `agent-security-audit` | `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.github/copilot-instructions.md`, `.opencode/`, `.cursor/`, configuracao de MCP, codigo de orquestracao de agente | por sinal |
| `agentic-ai-risk-assess` | agente autonomo no codigo: laco de chamada de ferramenta, framework de agente | por sinal |
| `multi-agentic-threat-model` | dois ou mais agentes se comunicando no codigo ou na configuracao | por sinal |
| `ai-security-verification` | aplicacao de IA | so por intencao |
| `securability-engineering-review`, `prd-fiasse-asvs-enhancement`, `securable-generation` | nenhum | so por nome |

### Modo padrao

Para diff, branch, arquivos ou modulo.

1. Inventarie o escopo por tipo de arquivo e aplique a tabela de sinais genericos e a secao `## Sinais do projeto` da ponte.
2. Rode os comandos da secao `## Auditores do projeto` da ponte sobre o escopo. Esta e a etapa Framework-Specific Checks do play. Sem a secao, siga e registre.
3. Rode `code-review-security` sobre o escopo, classe a classe. O que os auditores do projeto ja cobriram nao precisa ser repetido; concentre o play no que nenhum auditor cobre.
4. Rode `secrets-scan` sobre o mesmo escopo.
5. Rode cada play cujo sinal apareceu no escopo no passo 1 e cada play acrescentado pelo objeto citado na tabela de intencao.
6. Traduza tudo pela ponte e escreva o relatorio no formato abaixo.

### Modo completo

Para o repositorio inteiro, por intencao.

1. Aplique a tabela de sinais ao repositorio inteiro e liste, play por play, se ha alvo e qual e a evidencia.
2. Rode o modo padrao com o repositorio como escopo, incluindo cada play com alvo.
3. Entregue um relatorio consolidado, com a lista explicita do que nao rodou e por que.

## Plays disponiveis

Caminhos relativos a esta pasta. Em chamada por skill, o play e nomeado por esta tabela.

| Play | Arquivo |
|---|---|
| `code-review-security` | `upstream/plugins/code-security-skills/plays/code-review-security.md` |
| `secrets-scan` | `upstream/plugins/code-security-skills/plays/secrets-scan.md` |
| `sca-audit` | `upstream/plugins/code-security-skills/plays/sca-audit.md` |
| `api-security-review` | `upstream/plugins/code-security-skills/plays/api-security-review.md` |
| `owasp-top10-web-review` | `upstream/plugins/code-security-skills/plays/owasp-top10-web-review.md` |
| `iac-security-review` | `upstream/plugins/code-security-skills/plays/iac-security-review.md` |
| `mobile-code-review` | `upstream/plugins/code-security-skills/plays/mobile-code-review.md` |
| `securability-engineering-review` | `upstream/plugins/code-security-skills/plays/securability-engineering-review.md`; o procedimento real esta em `upstream/plugins/code-security-skills/skills/securability-engineering-review/SKILL.md` |
| `prd-fiasse-asvs-enhancement` | `upstream/plugins/code-security-skills/plays/prd-fiasse-asvs-enhancement.md`; stub, conteudo em `upstream/plugins/code-security-skills/skills/prd-securability-enhancement/SKILL.md` |
| `securable-generation` | `upstream/plugins/code-security-skills/plays/securable-generation.md`; stub, conteudo em `upstream/plugins/code-security-skills/skills/securability-engineering/SKILL.md` |
| `agent-security-audit` | `upstream/plugins/ai-security-skills/plays/agent-security-audit.md` |
| `mcp-server-review` | `upstream/plugins/ai-security-skills/plays/mcp-server-review.md` |
| `llm-risk-assess` | `upstream/plugins/ai-security-skills/plays/llm-risk-assess.md` |
| `agentic-ai-risk-assess` | `upstream/plugins/ai-security-skills/plays/agentic-ai-risk-assess.md` |
| `ai-security-verification` | `upstream/plugins/ai-security-skills/plays/ai-security-verification.md` |
| `multi-agentic-threat-model` | `upstream/plugins/ai-security-skills/plays/multi-agentic-threat-model.md` |
| `prompt-injection-testing` | `upstream/plugins/ai-security-skills/plays/prompt-injection-testing.md` |

Play que nao existir em `upstream/plugins/*/plays/` na versao instalada nao roda. A copia pode ser parcial; confira o diretorio antes de citar.

## Requisito ASVS para plano ou codigo novo

Nao e play. E a skill `security-guidance` do upstream: indice do ASVS 5.0 por gatilho de tarefa, com a ficha de cada secao em `upstream/plugins/code-security-skills/data/asvs/`. Arquivo: `upstream/plugins/code-security-skills/skills/security-guidance/SKILL.md`.

1. Leia so a secao do indice que casar com a tarefa e a ficha `data/asvs/` que ela aponta.
2. O ID ASVS entra no plano ou no achado como justificativa. Severidade e estado continuam vindo da ponte.
3. O padrao de implementacao continua vindo da ponte e das referencias do projeto. A `security-guidance` diz o requisito, nao a implementacao.
4. Em uso direto, responda em linguagem simples: o que cuidar, por que, e onde no projeto isso se resolve. O ID ASVS vai entre parenteses.

## Formato de saida no modo direto

Primeiro o resumo, depois a tabela. Nunca o contrario.

### Resumo em linguagem simples

Cinco blocos curtos, sem sigla, sem CWE, sem nome de gate:

1. **O que foi olhado.** Escopo assumido, plays que rodaram e o que ficou de fora.
2. **O que foi encontrado.** Uma frase por achado, dizendo onde e qual o efeito para quem usa o sistema. Sem achado, escreva "Nada encontrado no escopo olhado" e repita o escopo.
3. **Quao grave.** Um rotulo por achado: "corrigir antes de entregar" para `BLOQUEANTE`, "corrigir em seguida" para `ALTA`, "melhoria" para `MEDIA` e `BAIXA`. Achado sem caminho do dado demonstrado leva "precisa de conferencia" no lugar do rotulo.
4. **O que fazer agora.** Uma frase por achado, no imperativo, sem codigo.
5. **O que parece problema e nao e.** Falso positivo derrubado e excecao da ponte, para o desenvolvedor nao reabrir.

### Tabela tecnica

Para quem vai corrigir. Uma linha por achado:

| # | Local | Achado | CWE | Ref OWASP | ASVS | Severidade | Estado | Controle local |
|---|---|---|---|---|---|---|---|---|

`Local` e `arquivo:linha`. `Estado` e `confirmado` ou `precisa de conferencia`. `Controle local` vem da secao `## Traducao` da ponte e fica vazio sem ponte. Abaixo da tabela, um bloco por achado confirmado com a evidencia e o caminho do dado, `arquivo:linha` em cada salto.

Os templates do upstream, `templates/finding.md` e `templates/report.md`, sao referencia de campos, nao formato obrigatorio. Nao use ID `NDC-`, nao use CVSS, nao chame API.

### Saidas opcionais

Quando o desenvolvedor pedir "gere tambem o PDF" ou "gere as issues":

1. Consolide os achados em um JSON de findings, fonte unica dos numeros. Campos de cada achado: `id`, `categoria`, `severidade` em `critica`, `alta`, `media` ou `baixa`, `arquivo`, `linha_inicio`, `linha_fim`, `descricao`, `evidencia`, `impacto`, `sugestao_correcao`, `criterios_aceite`, `acionavel`, `grupo_issue`. `BLOQUEANTE` vira `critica`; as demais mantem o nome em minusculo.
2. Issues: uma por achado com `acionavel` verdadeiro, agrupando pelo `grupo_issue`. So o texto; nao crie issue em ferramenta nenhuma.
3. PDF e caminho de gravacao: o que a secao `## Saidas opcionais` da ponte definir. Sem a secao, entregue o JSON e o texto das issues na resposta.

## Depois do relatorio

Termine sempre com uma frase de proximo passo. Com achado: "Para corrigir, peca: corrija o achado N do relatorio de seguranca". Sem achado: "Nada a corrigir neste escopo".

Se o desenvolvedor pedir a correcao, encerre esta skill e siga o que a secao `## Correcao` da ponte indicar. Sem a secao, diga que a correcao e outra tarefa e peca que ela seja pedida citando o achado. Esta skill nao corrige.

## O que esta skill nao faz

- Nao roda scanner. O playbook e procedimento em Markdown, sem script de varredura. Os unicos scripts sao os auditores que a ponte do projeto listar.
- Nao contem nada do projeto. Linguagem, framework, modulos, auditores e excecoes entram pela ponte.
- Nao abre issue nem tarefa.
- Nao altera codigo.
- Nao faz pergunta de seguranca ao desenvolvedor. Assume o padrao e registra.
