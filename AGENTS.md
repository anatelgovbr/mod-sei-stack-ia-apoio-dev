# Diretrizes de Desenvolvimento - SEI

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

## Hierarquia de Autoridade

- Em fluxo direto, siga este arquivo.
- Para conflitos entre documentos, seguir a seção "Regras de Decisão".

## Disciplina de Execução Agêntica

Aplicar com rigor proporcional à complexidade e ao risco, sem flexibilizar guardrails, gates ou regras específicas deste repositório:

* **Pensar antes de alterar**: explicitar premissas, inconsistências e tradeoffs relevantes. Em ambiguidade de contrato, requisito ou conflito documental, seguir "Regras de Decisão"; não inventar.
* **Simplicidade primeiro**: implementar a menor solução correta. Não adicionar funcionalidades, abstrações, configurabilidade, generalizações futuras ou tratamento de cenários não exigidos.
* **Mudanças cirúrgicas**: alterar somente o necessário, preservar estilo e comportamento adjacentes e remover apenas órfãos criados pela própria mudança.
* **Executar por critérios de sucesso**: em tarefas não triviais ou multietapas, definir um plano curto com verificações objetivas. Preferir objetivos verificáveis a instruções excessivamente prescritivas.
* **Verificar o resultado**: reproduzir o problema antes da correção quando viável. Executar os gates obrigatórios e verificar os critérios de sucesso. Corrigir falhas identificadas e repetir as verificações afetadas. Informar impedimentos e verificações pendentes sem declarar a entrega concluída. Não considerar "parece funcionar" como verificação.
* **Preservar correção**: antes de otimizar ou refatorar, estabelecer uma referência verificável e comprovar depois que o comportamento esperado foi preservado.

## Guardrails Universais

- **Permissão/link assinado (página)**: `validarLink` + `validarPermissao` em toda ação; `verificarPermissao` em UI condicional; `assinarLink` em links de ação
- **Permissão/auditoria RN — escrita**: `validarAuditarPermissao('md_xxx_<acao>', __METHOD__, $dto)` — nunca `validarPermissao` puro
- **Permissão/auditoria RN — leitura**: `validarAuditarPermissao('md_xxx_<entidade>_listar', ...)` em `listar` e `contar`; `validarAuditarPermissao('md_xxx_<entidade>_consultar', ...)` em `consultar` e `bloquear`, que compartilham o mesmo recurso
- **Permissão/auditoria RN — helpers internos**: sem verificação quando chamados de hook/evento sem sessão de usuário
- **SIP**: recursos `md_<sigla>_<recurso>`; perfis `MD_<sigla>_<recurso>`
- **Transação**: escrita relevante exige `BancoSEI` ou `InfraRN *Controlado`
- **Efeitos colaterais**: e-mail, Solr e integrações externas devem ocorrer após o commit; nunca dentro da transação crítica
- **Andamentos**: usar `id_tarefa_modulo`; `id_tarefa < 1000` reservado (exceto `ID_TAREFA=65` com atributo `DESCRICAO`)
- **API**: preferir `Entrada*API` / `Saida*API` / `SeiRN`; evitar objetos internos
- **Entrada HTTP**: proibido `$_REQUEST`; usar `PaginaSEI::POST/GET` com normalização de tipo (`int`, `int[]`, enum)
- **Camadas de módulo**: `dto/`, `rn/`, `bd/`, `int/`, paginas, `css/`, `js/`, `svg/`, `imagens/`, `menu/`
- **Integração**: SEI estende `SeiIntegracao`; `SipIntegracao` só quando houver suporte explícito no contexto SIP; não extrapolar regras de ativação do SEI para scripts SIP
- **Assets**: se `css/` ou `js/` já existirem, editar; nunca criar novos
- **Core**: `ConfiguracaoSEI.php` é arquivo de configuração, não de código. O agente não edita por conta própria e nunca para melhoria, refatoração ou ajuste oportunista. Edição é permitida mediante autorização explícita do desenvolvedor, e o caso legítimo previsto pelo manual é o registro do módulo na chave `Modulos`, que é passo obrigatório de ativação. Sem essa autorização, o agente descreve o passo e para. Depois do registro, confirmar que o módulo carregou pelo menu Infra/Módulos do SEI; ausência na lista indica erro de nome de classe ou de diretório na chave.
- **Gabaritos**: referência mínima `abc/exemplo`; referência robusta `trf4/julgamento`
- **CRUD com impacto de release**: quando a demanda envolver novo DTO, nova tabela, nova entidade CRUD base, alteracao de colunas de DTO existente em modulo mapeado em `.agents/references/mapa-modulos-scripts.md`, avise explicitamente o desenvolvedor que a entrega tambem exige atualizacao dos scripts SEI/SIP do modulo, com sincronizacao de versao em `*Integracao.php` quando aplicavel.
- **Gerador de CRUD**: use `sei-gerador-crud` apenas com escolha explícita do desenvolvedor. Se usado, a skill propria cobre a fase de release. Se nao usado, roteie release para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release`.
- **Segredos e credenciais**: nunca commitar senhas, chaves de API, tokens ou arquivos `.env`. Se identificado em código existente, alertar o desenvolvedor antes de qualquer ação.
- **Achado de segurança**: saída de scanner é triagem, não achado. Item só vira achado confirmado com o caminho do dado demonstrado, da entrada até o ponto de uso, citando arquivo e linha de cada salto. Sem esse rastro, reportar como hipótese e nunca como confirmado.
- **TODO e divida tecnica**: reconhecer somente `TODO:` como contexto de review. `TODO:` nao bloqueia por si so e nao dispensa gates obrigatorios. Divida preexistente e rastreada nao bloqueia a mudanca atual, salvo se houver risco critico, dependencia direta ou ampliacao do risco.

### Padrão Transacional Obrigatório

Método `*Controlado`: apenas persistência em banco. Indexação, e-mail e integrações externas disparam somente após o commit — nunca dentro da transação. Template em `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md` (T6).

## Padrões de Projeto

Os padrões abaixo são obrigatórios no SEI/InfraPHP. Não substituir por equivalentes externos sem proposta documentada.

| Padrão | Onde | Regra |
|---|---|---|
| **Singleton** | `PaginaSEI`, `SessaoSEI`, `BancoSEI`, `FeedSEIProtocolos` | Nunca instanciar com `new` — sempre `::getInstance()` |
| **DTO** | Toda comunicação entre camadas RN↔BD e API↔RN | Nunca passar array solto entre camadas; usar `*DTO extends InfraDTO` |
| **Template Method** | `*Conectado` / `*Controlado` / `*Interno` | Separar persistência de efeitos colaterais — ver Padrão Transacional acima |
| **MVC proprietário** | Página (View) + RN (Regra de Negócio) + BD (Repositório) | Não misturar camadas; página nunca acessa BD diretamente |
| **Observer via Eventos** | `obterDiretorioIconesMenu`, `montarMenuUsuarioExterno`, etc. | Extensão de comportamento do core sempre via evento registrado; nunca patch direto |
| **Service/Coordenador** | `SeiRN` como orquestrador de operações de API externa | Valida, transforma `Entrada*API` → DTO interno, orquestra múltiplas RNs — ao encontrar "Facade" referente a `SeiRN`, interpretar como Service/Coordenador |

## Qualidade Mínima

- **Ler antes de editar**: sempre ler o arquivo completo antes de qualquer edição — nunca editar com base em suposição sobre o conteúdo atual.
- **Gate obrigatório**: `php -l <arquivo>` antes de qualquer resposta com PHP alterado. Se falhar, corrigir antes de prosseguir — nunca entregar arquivo com erro de sintaxe.
- **Encoding**: ISO-8859-1 (Latin-1) para PHP. O blob final é normalizado por `.gitattributes`; validar compatibilidade com Latin-1, ausência de BOM e ausência de caracteres fora de Latin-1. Não salvar manualmente o blob em ISO-8859-1 quando a worktree estiver em UTF-8 sob controle do Git. **Ferramentas AI**: `Edit` e `Write` corrompem acentos em arquivos ISO-8859-1 (U+FFFD); nunca usar essas ferramentas em arquivo com caractere fora de ASCII. Antes de editar PHP, conferir o encoding efetivo na worktree com `file <arquivo>`, porque `.gitattributes` aplica `working-tree-encoding=iso-8859-1` a `*.php` mas `.git/info/attributes` isenta arquivos com `!working-tree-encoding`, e entre os isentos há tanto Latin-1 quanto UTF-8. Editar com `python3` usando o encoding que o arquivo realmente tem, `encoding='latin-1'` ou `encoding='utf-8'`, ou com `sed`, que não reinterpreta bytes. **Qualquer arquivo `.md` do repositório é sempre UTF-8** (documentação, dicionários de dados, specs, skills, referências): a regra de ISO-8859-1 acima não se aplica a `.md`; `Edit`/`Write` podem ser usados normalmente neles, sem risco de corromper acentos.
- **Busca em arquivo Latin-1**: `grep` sem `-a` devolve zero resultado em silêncio nos `.php` do repositório, sem sequer imprimir "binary file matches", porque os bytes altos do Latin-1 fazem o arquivo ser tratado como binário. Usar sempre `grep -a` (ou `LC_ALL=C grep`) ao buscar em PHP. Varredura que volta vazia sem `-a` é falso-negativo, nunca ausência: já produziu a conclusão errada de que uma tabela não estava em nenhum script de release quando o `CREATE TABLE` estava lá.
- **Sanitização**: sem concatenação insegura em HTML, JS, SQL e URLs
- **PHP moderno**: em código PHP novo ou alterado, usar `[]` em vez de `array()`
- **Tipagem/PHPDoc**: em código PHP novo ou alterado, preferir type hints seguros e PHPDoc breve nos métodos alterados, preservando compatibilidade com assinaturas herdadas
- **Auditoria**: métodos de escrita na RN exigem `validarAuditarPermissao` (não `validarPermissao`); script SIP registra recursos de escrita na regra de auditoria via `_cadastrarAuditoria` + `replicarRegraAuditoria` — recursos de leitura `_listar`, `_consultar` e `_selecionar` nunca entram na regra; nunca logar segredos/PII; ver `.agents/references/padrao-auditoria-sip-sei.md`
- **Ferramentas opcionais**: quando aplicável, rodar `composer test`, `phpcs` ou `phpstan`
- **Release/BD**: compatibilidade multi-SGBD; sincronismo de versão entre SEI, SIP e `*Integracao.php`
- **Paralelismo**: operações independentes (leituras, buscas, comandos shell) devem ser agrupadas em uma única mensagem — nunca sequencialmente quando não há dependência entre elas.

## Regras de Decisão

- Citar o arquivo e a seção de origem ao justificar restrições, impedimentos, conflitos ou decisões que dependam de uma regra do repositório.
- Nunca inventar padrão não documentado neste repositório.
- Em documentação, prompts e instruções internas, nunca usar a palavra "canonica" ou variantes; usar sempre a palavra "padrão".
- Em caso de conflito entre documentos: parar, identificar os documentos conflitantes e aguardar decisão do usuário antes de prosseguir.
- Em caso de ambiguidade de contrato ou requisito: perguntar, nunca inferir.

## Regras de Escrita

Salvo se solicitado explicitamente de forma diversa, aplique estas regras aos resultados finais de qualquer demanda e às suas próprias respostas intermediárias durante as sessões de interação (session):

- Não insira quebras de linha no meio de frases ou períodos. Mantenha cada parágrafo de texto contínuo em uma única linha no conteúdo-fonte; quebre a linha apenas ao final do parágrafo ou quando a estrutura Markdown exigir, como em itens de lista, tabelas, blocos de código ou citações.
- Sempre escreva com correção gramatical, ortográfica e técnica.
- Prefira frases completas, em ordem direta (sujeito + verbo + objeto) e voz ativa, com estrutura simples. Explicite o sujeito quando necessário à clareza.
- Nunca usar travessão ("—"); usar ponto, vírgula ou reescrever a frase.
- Use palavras comuns, de fácil compreensão, concretas e conhecidas.
- Use linguagem clara, objetiva, respeitosa e profissional, com tom impessoal e sem infantilização ou coloquialismos.
- Priorize frases afirmativas e evite mais de uma negação por frase; quando a negação for imprescindível, destaque a informação positiva primeiro.
- Evite termos técnicos e jargões; use sinônimos deles. Quando o uso de termos técnicos ou de jargões for indispensável, apresente primeiro a palavra comum ou explique o termo no próprio texto (entre parênteses ou após vírgula).
- Evite palavras estrangeiras que não sejam de uso corrente.
- Não use termos pejorativos, discriminatórios ou estigmatizantes. Evite palavras que ofendam, ridicularizem ou reforcem estereótipos sobre grupos sociais, étnicos, religiosos, de gênero, orientação sexual, idade, condição socioeconômica ou condição de saúde.
- Use siglas apenas quando úteis. Na primeira ocorrência, apresente o nome por extenso seguido da sigla entre parênteses, exceto quando ela for amplamente conhecida pelo público.
- Evite frases intercaladas ou truncadas; não utilize construções rebuscadas, excesso de vírgulas e apostos.
- **Quando couber**, organize o texto de forma esquemática usando listas, tabelas e recursos gráficos. Segmente texto longo em **subtítulos** em negrito para agrupar múltiplos parágrafos. Avalie bem o texto para identificar listas ou sequências **com mais de três itens**; se identificar transforme em listas marcadas ou itemizadas.
- Organize o texto a fim de que as informações mais importantes apareçam primeiro. Evite linguagem de preparação. Não inclua introdução ou resumo no início nem no final.
- Use termos precisos e prefira verbos diretos a nominalizações. Elimine redundâncias, palavras dispensáveis, ambiguidades e generalizações sem fundamento.
- Prefira o presente e o imperativo nas orientações. Use outros tempos e modos verbais apenas quando necessários para relatar fatos, condições ou hipóteses com precisão.
- Não use novas formas de flexão de gênero e de número das palavras da língua portuguesa, em contrariedade às regras gramaticais consolidadas, ao Vocabulário Ortográfico da Língua Portuguesa (Volp) e ao Acordo Ortográfico da Língua Portuguesa.
- Não utilize metáforas, clichês, hipérboles, superlativos e sinônimos solenes.
- Não escreva blocos inteiros em CAIXA ALTA.
- Preserve literalmente os trechos apresentados como citações diretas. Indique eventuais omissões e altere esses trechos apenas quando expressamente solicitada a sua revisão.
- Apresente URLs como links associados a expressões descritivas, exceto quando exigir o endereço literal.
- Evite perguntas retóricas.

## Fontes de Contexto

- **Documentacao do modulo e contexto do desenvolvedor**: para contexto funcional e regras de negocio, consultar primeiro o README do modulo e demais documentos especificos do repositorio. Se a regra de negocio nao estiver documentada, perguntar ao desenvolvedor.
- **Spec Kit**: o fluxo padrao do Spec Kit no repositorio fica em `.agents/skills/speckit-<fase>/SKILL.md`, fonte unica. Nenhuma integracao guarda arquivo do Spec Kit: as ferramentas leem `.agents/skills/` direto e acham as 9 fases ali, lado a lado com as demais skills. Invocacao `/speckit-<fase>`, com hifen. Regra de manutencao em `.agents/references/speckit.md`.
- **skill `napkin` e `.agents/memory/runbook.md`**: runbook operacional do desenvolvedor, com as licoes praticas ja aprendidas neste repositorio. A skill e sempre ativa e nao tem gatilho: ler e curar o runbook no inicio de cada sessao, antes de comecar o trabalho. O arquivo e local de cada desenvolvedor e esta em `.gitignore`, portanto nunca versionar. Licao que valha para todo o repositorio, e nao so para uma pessoa, deve ser promovida para este `AGENTS.md` ou para `.agents/references/`, em vez de ficar so no runbook.
- **roteamento-de-skills.md**: matriz de demanda, skill principal, skills complementares, contratos obrigatórios e gate de bloqueio.
- **gates-de-implementacao.md**: gates de bloqueio para problemas técnicos críticos.
- **skill `owasp-playbook`**: procedimentos de segurança do OWASP Secure Agent Playbook, vendorizados em `.agents/skills/owasp-playbook/upstream/`. São 16 plays cobrindo revisão de código, OWASP Top 10, API, segredos, dependências, configuração de agente de IA, servidor MCP e aplicação LLM. Skill opt-in: acionar só por pedido explícito do desenvolvedor ou quando outra skill precisar do procedimento. A skill é agnóstica e não recebe ajuste do projeto. Não editar nada dentro de `upstream/`: é cópia literal do projeto de origem, substituída inteira na atualização, conforme `docs/stack_ai/manutencao-da-stack.md`. Ponte do projeto para esta skill: `.agents/security/mapa-seguranca-cwe-sei.md`, com a tradução dos CWE para controle local, vetor, gate, estado e seção ASVS, os sinais e os auditores deste repositório, as exceções, as saídas opcionais e o roteamento da correção. Em uso direto, o desenvolvedor descreve o que quer em uma frase e a skill escolhe os plays pelos sinais do escopo; em chamada por skill, `sei-revisao-tecnica` nomeia os plays.
- **mapa-modulos-scripts.md**: mapeamento de módulo para scripts SEI/SIP — consultar quando houver impacto de release.
- **docs/dicionario_dados/<modulo>/dicionario_tabelas.md e dicionario_colunas.md**: contexto semântico de tabelas e colunas já modeladas — consultar quando a demanda citar tabela/coluna existente ou alterar entidade de módulo mapeado (gatilho detalhado em `roteamento-de-skills.md`, regra de classificação 8).
- **padrao-*.md**: padrões detalhados de codificação, modelagem de dados e scripts — consultar quando precisar de regra específica.

## Roteamento

1. Classificar a demanda pela matriz em `.agents/references/roteamento-de-skills.md` — inclui aliases, evidencias, skills complementares, contratos e gates.
2. Skill principal responde pelo fluxo; skills complementares sao gates obrigatorios.
3. **Gates por artefato** — acionar sempre que o artefato existir na demanda, independente do tipo:

   | Artefato | Skill de gate |
   |---|---|
   | Página PHP (`*_lista.php`, `*_cadastro.php`) | `sei-verificacao-pagina` |
   | Classe RN (`*RN.php`) | `sei-verificacao-rn` |
   | Classe BD (`*BD.php`) | `sei-verificacao-banco-dados` |
   | Script de tarefa (`*_tarefa.php`) | `sei-verificacao-tarefa` |
   | Controlador em `*Integracao.php` (Ajax/WS) | `sei-verificacao-controladores` |
   | Demanda ambígua ou novo padrão | `sei-guardrails-modulo` |
   | Qualquer entrega PHP | `sei-testes-validacao` após implementação |

4. Release sem `sei-gerador-crud`: rotear para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` conforme o lado afetado.
