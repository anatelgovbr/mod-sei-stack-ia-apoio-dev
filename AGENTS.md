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
- `specs/**`
- `.agents/**`

**Proibido sem autorização:**
- `fontes/sei/src/main/php/sei/web/**` fora de `modulos/`
- `fontes/sei/src/main/php/sip/web/**`
- `infra/**`

Mudança no core exige proposta documentada — sem patch direto.

## Hierarquia de Autoridade

- Em Fluxo Direto, siga este arquivo.
- Se houver conflito entre documentos, pare e solicite decisão.

## Guardrails Universais

- **Permissão/link assinado (página)**: `validarLink` + `validarPermissao` em toda ação; `verificarPermissao` em UI condicional; `assinarLink` em links de ação
- **Permissão/auditoria RN — escrita**: `validarAuditarPermissao('md_xxx_<acao>', __METHOD__, $dto)` — nunca `validarPermissao` puro
- **Permissão/auditoria RN — leitura**: `validarAuditarPermissao('md_xxx_listar', __METHOD__, $dto)`
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
- **Core**: `ConfiguracaoSEI.php` é somente referência; não editar
- **Gabaritos**: referência mínima `abc/exemplo`; referência robusta `trf4/julgamento`
- **CRUD com impacto de release**: quando a demanda envolver novo DTO, nova tabela, nova entidade CRUD base, alteracao de colunas de DTO existente em modulo mapeado em `.agents/references/mapa-modulos-scripts.md`, avise explicitamente o desenvolvedor que a entrega tambem exige atualizacao dos scripts SEI/SIP do modulo, com sincronizacao de versao em `*Integracao.php` quando aplicavel.
- **Gerador de CRUD**: use `sei-gerador-crud` apenas com escolha explícita do desenvolvedor. Se usado, a skill propria cobre a fase de release. Se nao usado, roteie release para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release`.
- **Segredos e credenciais**: nunca commitar senhas, chaves de API, tokens ou arquivos `.env`. Se identificado em código existente, alertar o desenvolvedor antes de qualquer ação.
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
- **Encoding**: ISO-8859-1 (Latin-1). O blob final é normalizado por `.gitattributes`; validar compatibilidade com Latin-1, ausência de BOM e ausência de caracteres fora de Latin-1. Não salvar manualmente o blob em ISO-8859-1 quando a worktree estiver em UTF-8 sob controle do Git. **Ferramentas AI**: `Edit` e `Write` corrompem acentos em arquivos ISO-8859-1 (U+FFFD). Para editar PHP com acentos, usar `python3` com `encoding='latin-1'` ou `sed`. Nunca usar `Edit`/`Write` diretamente em arquivos com caracteres fora de ASCII.
- **Sanitização**: sem concatenação insegura em HTML, JS, SQL e URLs
- **PHP moderno**: em código PHP novo ou alterado, usar `[]` em vez de `array()`
- **Tipagem/PHPDoc**: em código PHP novo ou alterado, preferir type hints seguros e PHPDoc breve nos métodos alterados, preservando compatibilidade com assinaturas herdadas
- **Auditoria**: métodos de escrita na RN exigem `validarAuditarPermissao` (não `validarPermissao`); script SIP registra recursos de escrita na regra de auditoria via `_cadastrarAuditoria` + `replicarRegraAuditoria` — recurso `_listar` nunca entra na regra; nunca logar segredos/PII; ver `.agents/references/padrao-auditoria-sip-sei.md`
- **Ferramentas opcionais**: quando aplicável, rodar `composer test`, `phpcs` ou `phpstan`
- **Release/BD**: compatibilidade multi-SGBD; sincronismo de versão entre SEI, SIP e `*Integracao.php`
- **Paralelismo**: operações independentes (leituras, buscas, comandos shell) devem ser agrupadas em uma única mensagem — nunca sequencialmente quando não há dependência entre elas.

## Regras de Decisão

- Executar exatamente o que foi solicitado — nada mais, nada menos. Não refatorar, não adicionar funcionalidade extra e não "aproveitar a passagem" para limpar código adjacente sem autorização explícita.
- Ao aplicar qualquer regra, citar o arquivo e a seção de origem
- Nunca inventar padrão não documentado neste repositório
- Em documentação, prompts e instruções internas, nunca usar a palavra "canonica" ou variantes; usar sempre a palavra "padrao"
- Em caso de conflito entre documentos: parar, identificar os dois documentos conflitantes e aguardar decisão do desenvolvedor antes de prosseguir
- Em caso de ambiguidade de contrato ou requisito: perguntar, nunca inferir

## Fontes de Contexto

- **Documentacao do modulo e contexto do desenvolvedor**: para contexto funcional e regras de negocio, consultar primeiro o README do modulo e demais documentos especificos do repositorio. Se a regra de negocio nao estiver documentada, perguntar ao desenvolvedor.
- **Spec Kit**: o fluxo padrao do Spec Kit no repositorio fica em `.agents/skills/speckit/`; integracoes de ferramenta apenas expõem esse conteudo com adapters leves.
- **roteamento-de-skills.md**: matriz de demanda, skill principal, skills complementares, contratos obrigatórios e gate de bloqueio.
- **gates-de-implementacao.md**: gates de bloqueio para problemas técnicos críticos.
- **mapa-modulos-scripts.md**: mapeamento de módulo para scripts SEI/SIP — consultar quando houver impacto de release.
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
