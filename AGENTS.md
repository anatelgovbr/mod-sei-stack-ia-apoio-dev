1. Pensar antes de agir
2. Simplicidade primeiro
3. Mudanças cirúrgicas
4. Execução orientada a objetivo

## Contexto

Repositório de customizações e módulos do SEI com release versionada e padrões InfraPHP. Trate o projeto como sistema administrativo, com requisitos de auditoria, permissão e compatibilidade de release.

## Dependências Técnicas do Projeto

- **Servidor**: Linux
- **PHP 8.2** — encoding ISO-8859-1 (Latin-1)
- Módulos SEI / SIP
- InfraPHP (DTO, RN, BD, páginas)
- Bootstrap 5.3.1
- jQuery 3.7.0
- jQuery UI 1.13.2

## Escopo e Limites de Escrita

**Permitido:**
- `fontes/sei/src/main/php/sei/web/modulos/**`
- `fontes/sei/src/main/php/sei/scripts/**`
- `fontes/sei/src/main/php/sip/scripts/**`
- `docs/**`
- `specs/**`
- `.agents/**`

**Proibido sem autorização:**
- `fontes/sei/src/main/php/sei/web/**` fora de `modulos/`
- `fontes/sei/src/main/php/sip/web/**`
- `infra/**`

Mudança no core exige proposta documentada — sem patch direto.

## Disciplina Agêntica

O rigor cresce com a complexidade e o risco; guardrails, gates e regras do projeto valem sempre.

### 1. Pensar antes de agir

**Não presumir. Não esconder dúvida. Expor tradeoffs.**

Antes de qualquer alteração:
- Declarar as premissas adotadas. Em dúvida, perguntar.
- Se existem várias interpretações, apresentar todas e nomear o ponto que falta; escolher em silêncio não é opção.
- Se existe caminho mais simples dentro dos padrões documentados, apresentar o caminho e a diferença e aguardar a escolha do desenvolvedor.
- Se algo não está claro, parar, nomear o que confunde e perguntar.
- Em conflito entre documentos, seguir "Regras de Decisão".

### 2. Simplicidade primeiro

**O mínimo que resolve o problema. Nada especulativo.**

- Sem funcionalidade além do pedido.
- Sem abstração para código de uso único.
- Sem "flexibilidade" ou "configurabilidade" que ninguém pediu.
- Sem tratamento de erro para cenário impossível.
- Se saíram 200 linhas e cabia em 50, reescrever.

Teste de saída: um revisor sênior da stack do projeto aprova o escopo sem ressalva de complexidade.

### 3. Mudanças cirúrgicas

**Tocar só no que o pedido exige. Limpar só a própria sujeira.**

Ao editar código existente:
- Código adjacente, comentários, formatação e o que não está quebrado ficam fora.
- Seguir o estilo existente, mesmo que o agente fizesse diferente.
- Código morto preexistente e problema fora do escopo ficam no código e entram na resposta como observação curta.
- Remover imports, variáveis e funções que a própria mudança deixou sem uso.

Teste de saída: cada linha alterada no diff responde a um trecho do pedido ou a uma regra documentada no projeto; linha sem uma dessas origens sai do diff.

### 4. Execução orientada a objetivo

**Definir critérios de sucesso. Repetir até a verificação passar.**

Traduzir o pedido em critério verificável:
- "Adicionar validação" → "listar as entradas inválidas, implementar, provar cada uma com comando".
- "Corrigir o bug" → "reproduzir com comando, corrigir, repetir o comando até passar".
- "Refatorar ou otimizar X" → "registrar o comportamento antes, alterar, comprovar o mesmo comportamento depois".

Antes da primeira edição, declarar o plano como checklist, um item por passo:
```
- [ ] [Step] → verify: [check]
- [ ] [Step] → verify: [check]
- [ ] [Step] → verify: [check]
```

Ao verificar:
- Executar os gates obrigatórios e os critérios de sucesso.
- Repetir correção e verificação até todos passarem.
- Verificação que depende do desenvolvedor, como smoke manual, entra na resposta como pendente.
- Informar impedimentos e pendências sem declarar a entrega concluída.

Na resposta final, repetir o checklist com o resultado de cada item: `[x]` verificado por comando, com o comando e a saída; `[ ]` pendente ou com falha, com o motivo.

Teste de saída: cada item do checklist aparece na resposta final marcado, com o comando e o resultado; "parece funcionar" não conta.

## Roteamento

1. Classificar a demanda pela matriz em `.agents/references/roteamento-de-skills.md` (aliases, evidências, skills complementares, contratos e gates).
2. Skill principal responde pelo fluxo; skills complementares sao gates obrigatorios.
3. **Gates por artefato**: acionar sempre que o artefato existir na demanda, independente do tipo:

   | Artefato | Skill de gate |
   |---|---|
   | Página PHP (`*_lista.php`, `*_cadastro.php`) | `sei-verificacao-pagina` |
   | Classe RN (`*RN.php`) | `sei-verificacao-rn` |
   | Classe BD (`*BD.php`) | `sei-verificacao-banco-dados` |
   | Script de tarefa (`*_tarefa.php`) | `sei-verificacao-tarefa` |
   | Controlador em `*Integracao.php` (Ajax/WS) | `sei-verificacao-controladores` |
   | Demanda ambígua ou novo padrão | `sei-guardrails-modulo` |
   | Qualquer entrega PHP | `sei-validacao-padrao` após implementação |

4. Release sem `sei-gerador-crud`: rotear para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` conforme o lado afetado.

Teste de saída: a resposta nomeia a skill principal e os gates acionados.

## Guardrails Universais

- Ambiguidade relevante → não assumir, não adivinhar; explicitar ou perguntar
- **Permissão/link assinado (página)**: `validarLink` + `validarPermissao` em toda ação; `verificarPermissao` em UI condicional; `assinarLink` em links de ação
- **Permissão/auditoria RN — escrita**: `validarAuditarPermissao('md_xxx_<acao>', __METHOD__, $dto)` — nunca `validarPermissao` puro
- **Permissão/auditoria RN — leitura**: `validarAuditarPermissao('md_xxx_<entidade>_listar', ...)` em `listar` e `contar`; `validarAuditarPermissao('md_xxx_<entidade>_consultar', ...)` em `consultar` e `bloquear`, que compartilham o mesmo recurso
- **Permissão/auditoria RN — helpers internos**: sem verificação quando chamados de hook/evento sem sessão de usuário
- **Auditoria SIP**: script SIP registra recursos de escrita na regra de auditoria via `_cadastrarAuditoria` + `replicarRegraAuditoria`; recursos de leitura `_listar`, `_consultar` e `_selecionar` ficam fora da regra; nunca logar segredos/PII; detalhe em `.agents/references/padrao-auditoria-sip-sei.md`
- **SIP**: recursos `md_<sigla>_<recurso>`; perfis `MD_<sigla>_<recurso>`
- **Transação**: escrita relevante exige `BancoSEI` ou `InfraRN *Controlado`
- **Andamentos**: usar `id_tarefa_modulo`; `id_tarefa < 1000` reservado (exceto `ID_TAREFA=65` com atributo `DESCRICAO`)
- **API**: preferir `Entrada*API` / `Saida*API` / `SeiRN`; evitar objetos internos
- **Consulta em lote (N+1)**: relacionados de um resultado de `listar` são carregados antes do laço, em uma consulta só, com `setNumId...($arrIds, InfraDTO::$OPER_IN)` no DTO de pesquisa ou com os retornos já configurados no `listar` de origem (`ret...`). `consultar` ou `listar` por item dentro do laço só com justificativa explícita na resposta (volume pequeno e limitado, ou API sem filtro em lote). Vale também para hooks que recebem arrays de objetos da API
- **Entrada HTTP**: proibido `$_REQUEST`; usar `PaginaSEI::POST/GET` com normalização de tipo (`int`, `int[]`, enum)
- **Camadas de módulo**: `dto/`, `rn/`, `bd/`, `int/`, paginas, `css/`, `js/`, `svg/`, `imagens/`, `menu/`
- **Integração**: SEI estende `SeiIntegracao`; `SipIntegracao` só quando houver suporte explícito no contexto SIP; não extrapolar regras de ativação do SEI para scripts SIP
- **Assets**: se `css/` ou `js/` já existirem, editar; nunca criar novos
- **Core**: `ConfiguracaoSEI.php` é configuração, não código: editar só com autorização explícita do desenvolvedor, e o único caso previsto pelo manual é o registro do módulo na chave `Modulos`, passo obrigatório de ativação; sem autorização, descrever o passo e parar. Depois do registro, confirmar que o módulo aparece no menu Infra/Módulos do SEI; ausência indica erro de nome de classe ou de diretório na chave.
- **Gabaritos**: referência mínima `abc/exemplo`; referência robusta `trf4/julgamento`
- **CRUD com impacto de release**: quando a demanda envolver novo DTO, nova tabela, nova entidade CRUD base, alteracao de colunas de DTO existente em modulo mapeado em `.agents/references/mapa-modulos-scripts.md`, avise explicitamente o desenvolvedor que a entrega tambem exige atualizacao dos scripts SEI/SIP do modulo, com sincronizacao de versao em `*Integracao.php` quando aplicavel.
- **Gerador de CRUD**: `sei-gerador-crud` só com escolha explícita do desenvolvedor; quando usado, a própria skill cobre a fase de release.
- **Segredos e credenciais**: nunca commitar senhas, chaves de API, tokens ou arquivos `.env`. Se identificado em código existente, alertar o desenvolvedor antes de qualquer ação.
- **Achado de segurança**: saída de scanner é triagem, não achado. Item só vira achado confirmado com o caminho do dado demonstrado, da entrada até o ponto de uso, citando arquivo e linha de cada salto. Sem esse rastro, reportar como hipótese e nunca como confirmado.
- **TODO e divida tecnica**: reconhecer somente `TODO:` como contexto de review. `TODO:` nao bloqueia por si so e nao dispensa gates obrigatorios. Divida preexistente e rastreada nao bloqueia a mudanca atual, salvo se houver risco critico, dependencia direta ou ampliacao do risco.

### Padrão Transacional Obrigatório

Método `*Controlado`: apenas persistência em banco. Indexação (Solr), e-mail e integrações externas disparam somente após o commit, nunca dentro da transação. Template em `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md` (T6).

## Padrões de Projeto

Os padrões abaixo são obrigatórios no SEI/InfraPHP. Não substituir por equivalentes externos sem proposta documentada.

| Padrão | Onde | Regra |
|---|---|---|
| **Singleton** | `PaginaSEI`, `SessaoSEI`, `BancoSEI`, `FeedSEIProtocolos` | Nunca instanciar com `new` — sempre `::getInstance()` |
| **DTO** | Toda comunicação entre camadas RN↔BD e API↔RN | Nunca passar array solto entre camadas; usar `*DTO extends InfraDTO` |
| **Template Method** | `*Conectado` / `*Controlado` / `*Interno` | Separar persistência de efeitos colaterais — ver Padrão Transacional acima |
| **MVC proprietário** | Página (View) + RN (Regra de Negócio) + BD (Repositório) | Não misturar camadas; página nunca acessa BD diretamente |
| **Observer via Eventos** | `obterDiretorioIconesMenu`, `montarMenuUsuarioExterno`, etc. | Extensão de comportamento do core sempre via evento registrado |
| **Service/Coordenador** | `SeiRN` como orquestrador de operações de API externa | Valida, transforma `Entrada*API` → DTO interno, orquestra múltiplas RNs — ao encontrar "Facade" referente a `SeiRN`, interpretar como Service/Coordenador |

## Qualidade Mínima

- **Ler antes de editar**: sempre ler o arquivo completo antes de qualquer edição — nunca editar com base em suposição sobre o conteúdo atual.
- **Gate obrigatório**: `php -l <arquivo>` antes de qualquer resposta com PHP alterado. Todo PHP novo ou alterado abre com `<?php`; arquivo legado que abre com `<?` recebe a troca da abertura antes do lint, porque com `short_open_tag=Off` o `php -l` passa sem analisar. Lint com falha: corrigir antes de prosseguir.
- **Encoding**: PHP em ISO-8859-1 (Latin-1); qualquer `.md` do repositório é UTF-8. `Edit` e `Write` corrompem acentos em ISO-8859-1 (U+FFFD): nunca usar em PHP com caractere fora de ASCII; em `.md` podem ser usados. Antes de editar PHP, conferir o encoding real com `file <arquivo>`, porque há `.php` isentos do filtro do Git tanto em Latin-1 quanto em UTF-8; editar com `python3` no encoding que o arquivo tem (`latin-1` ou `utf-8`) ou com `sed`. Validar Latin-1 sem BOM e sem caractere fora de Latin-1; nunca salvar o blob manualmente em ISO-8859-1 quando a worktree estiver em UTF-8 sob o Git.
- **Busca em arquivo Latin-1**: usar sempre `grep -a` em `.php`; sem `-a`, o `grep` (inclusive ugrep, mesmo com `LC_ALL=C`) trata o arquivo como binário e devolve vazio em silêncio. Resultado vazio sem `-a` é falso-negativo, nunca ausência.
- **Sanitização**: saída HTML por `PaginaSEI::tratarHTML`, atributos e URLs por `formatarXHTML` e `assinarLink`, SQL só por DTO e classe BD; nunca concatenar entrada do usuário em HTML, JS, SQL ou URL
- **PHP moderno**: em código PHP novo e nas linhas que a demanda já altera, usar `[]` em vez de `array()`
- **Tipagem/PHPDoc**: em código PHP novo ou alterado, preferir type hints seguros e PHPDoc breve nos métodos alterados, preservando compatibilidade com assinaturas herdadas
- **Ferramentas opcionais**: quando disponíveis no projeto ou no módulo, rodar `composer test`, `phpcs` ou `phpstan`
- **Análise estática**: PHPStan quando houver configuração no projeto ou no módulo. A configuração de `trf4/julgamento/.ci/phpstan.neon` depende de pacote privado e, quando não puder rodar, entra como verificação pendente. Procedimento em `sei-validacao-padrao`.
- **Release/BD**: compatibilidade multi-SGBD; sincronismo de versão entre SEI, SIP e `*Integracao.php`
- **Paralelismo**: operações independentes (leituras, buscas, comandos shell) devem ser agrupadas em uma única mensagem — nunca sequencialmente quando não há dependência entre elas.

## Regras de Decisão

- Citar o arquivo e a seção de origem ao justificar restrições, impedimentos, conflitos ou decisões que dependam de uma regra do repositório.
- Nunca inventar padrão não documentado neste repositório.
- Em documentação, prompts e instruções internas, nunca usar a palavra "canonica" ou variantes; usar sempre a palavra "padrão".
- Em caso de conflito entre documentos: parar, identificar os documentos conflitantes e aguardar decisão do usuário antes de prosseguir.

## Regras de Escrita

Salvo solicitação explícita em contrário, aplique estas regras às mensagens em linguagem natural destinada a pessoas durante a sessão e aos entregáveis textuais em português brasileiro. Em código, comandos, identificadores, nomes de APIs, caminhos, dados estruturados e outros elementos definidos por linguagem, formato, protocolo ou projeto, preserve a sintaxe, o idioma e as convenções próprios do artefato. Instruções específicas do entregável prevalecem sobre estas regras gerais de estilo.

Em prosa Markdown, mantenha cada parágrafo em uma única linha no conteúdo-fonte e quebre linhas apenas entre parágrafos ou quando a estrutura do formato exigir. Use português brasileiro correto, linguagem clara, objetiva, respeitosa e profissional, voz ativa e frases completas. Não use travessão. Prefira palavras comuns, verbos diretos e afirmações precisas. Evite preâmbulos, redundâncias, coloquialismos, metáforas, clichês, hipérboles, construções rebuscadas, excesso de negativas e perguntas retóricas.

Use termos técnicos quando forem necessários à precisão ou forem a denominação canônica no contexto de desenvolvimento. Explique na primeira ocorrência os termos que possam não ser conhecidos pelo público do texto. Use siglas somente quando úteis e apresente o nome por extenso na primeira ocorrência, salvo siglas amplamente conhecidas. Não traduza nem adapte código, identificadores, comandos, nomes próprios de tecnologias ou outros termos que precisem permanecer literais.

Apresente primeiro a informação mais importante e evite introduções ou resumos que apenas repitam o conteúdo. Use subtítulos, listas e tabelas quando melhorarem a leitura, especialmente em textos longos ou sequências extensas, sem fragmentar artificialmente o texto. Siga a norma-padrão do português brasileiro e não crie flexões incompatíveis com ela.

Preserve literalmente citações diretas e outros conteúdos que precisem permanecer exatos, salvo solicitação expressa de revisão. Apresente URLs como links associados a expressões descritivas quando o formato permitir.

## Fontes de Contexto

- **Regra de negócio ou contexto funcional**: README do módulo e documentos específicos do repositório primeiro; se a regra não estiver documentada, perguntar ao desenvolvedor.
- **Spec Kit**: invocação `/speckit-<fase>`, com hífen; fonte única em `.agents/skills/speckit-<fase>/SKILL.md`, 10 fases lado a lado com as demais skills; regra de manutenção em `.agents/references/speckit.md`.
- **skill `napkin` e `.agents/memory/runbook.md`**: runbook operacional do desenvolvedor, local e fora do versionamento (`.gitignore`). Skill sempre ativa, sem gatilho: ler e curar o runbook no início de cada sessão, antes do trabalho. Lição que vale para todo o repositório sobe para este `AGENTS.md` ou para `.agents/references/`.
- **Problema técnico crítico durante a implementação**: `.agents/references/gates-de-implementacao.md`, gates de bloqueio.
- **skill `owasp-playbook`**: segurança por procedimento do OWASP Secure Agent Playbook, opt-in: só por pedido explícito do desenvolvedor ou por chamada de `sei-revisao-tecnica`, que nomeia os plays. Ponte do projeto em `.agents/security/mapa-seguranca-cwe-sei.md`. Nunca editar `upstream/`: cópia literal, substituída inteira na atualização (`docs/stack_ai/manutencao-da-stack.md`).
- **Tabela ou coluna existente citada na demanda, ou entidade de módulo mapeado alterada**: `docs/dicionario_dados/<modulo>/dicionario_tabelas.md` e `dicionario_colunas.md`, contexto semântico já modelado (regra de classificação 8 em `roteamento-de-skills.md`).
- **Regra detalhada de codificação, classes do sistema, métodos CRUD, ambiente de módulo, modelagem de dados ou scripts de release**: `.agents/references/padrao-*.md`.
