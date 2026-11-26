---
description: "Lista de tarefas para implementacao de feature em modulo SEI"
---

# Tarefas: [NOME DA FEATURE]

**Entrada**: Documentos de design em `/specs/[###-nome-feature]/`
**Pre-requisitos**: `plan.md` e `spec.md`; opcionais: `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Testes**: Incluir tarefas de teste apenas quando solicitado pela spec, pelo desenvolvedor ou por gate de validacao SEI aplicavel.

**Organizacao**: Tarefas agrupadas por historia de usuario testavel de forma independente sempre que possivel.

## Formato: `[ID] [P?] [US?] Descricao → verify: [conferencia]`

- **[P]**: Pode executar em paralelo porque altera arquivos diferentes e nao tem conflito de dependencia.
- **[US]**: Usar `[US1]`, `[US2]`, etc. apenas para tarefas de implementacao de historia de usuario.
- Incluir o caminho exato do arquivo em toda tarefa que cria ou altera arquivos.
- **verify**: comando ou conferencia que prova a tarefa concluida. Conferencia que depende do desenvolvedor, como smoke manual, fica `→ verify: pendente do desenvolvedor (<o que conferir>)`. Cada tarefa e um item do Checklist de Criterios Verificaveis da secao `Execução orientada a objetivo` do `AGENTS.md`.

## Convencoes de Caminho (SEI)

- Codigo do modulo: `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/`
- Camadas do modulo: `dto/`, `rn/`, `bd/`, `int/`, paginas na raiz do modulo, `css/`, `js/`, `svg/`, `imagens/`, `menu/`
- Scripts SEI: `fontes/sei/src/main/php/sei/scripts/`
- Scripts SIP: `fontes/sei/src/main/php/sip/scripts/`
- Artefatos da feature: `specs/[###-nome-feature]/`

## Gate de Contrato de Skill

- Ler `Roteamento de Skills e Contratos` do `plan.md` antes de gerar tarefas.
- Se qualquer contrato obrigatorio estiver com status `BLOCKED`, nao criar tarefas de implementacao para a area bloqueada.
- Tarefas de resolucao de contrato devem aparecer antes das tarefas de implementacao.
- Tarefas de validacao com `sei-validacao-padrao` devem aparecer na fase final de validacao para qualquer alteracao de codigo SEI.

## Gate do Gerador de CRUD (Condicional)

- Fonte de regras: `AGENTS.md`, secao "Guardrails Universais", item **Gerador de CRUD**; `.agents/skills/sei-gerador-crud/SKILL.md`, secao "Tres caminhos de execucao"; e o campo `Gate do Gerador de CRUD` preenchido no `plan.md`.
- Se `plan.md` indicar `Gerador Necessario: sim`, o `Status do Gate de Planejamento` deve ser `PASS` antes de qualquer tarefa de geracao.
- Tarefas que geram ou escrevem manualmente arquivos CRUD base NAO devem aparecer antes dos contratos JSON confirmados em `specs/[###-nome-feature]/crud-contratos/`.
- Se `Gerador Necessario: nao`, nao criar tarefas de `crud-contratos/`; tarefas de implementacao manual de CRUD ainda exigem contratos funcionais claros no `plan.md` antes de qualquer alteracao de codigo.

<!--
  As secoes abaixo sao exemplos de estrutura. O tasks.md gerado DEVE substituir
  as tarefas de exemplo por tarefas concretas derivadas de spec.md, plan.md e historias de usuario.
-->

## Fase 1: Preparacao e Descoberta

**Objetivo**: Confirmar escopo, estrutura do modulo, scripts, permissoes e assets existentes.

- [ ] T001 Identificar caminho do modulo-alvo em `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/` → verify: `ls` do caminho mostra o `<Modulo>Integracao.php`
- [ ] T002 Inspecionar scripts SEI/SIP existentes usando `.agents/references/mapa-modulos-scripts.md` → verify: scripts e versao atual do modulo registrados no `plan.md`
- [ ] T003 Inspecionar assets existentes em `css/` e `js/` antes de planejar alteracoes de assets → verify: arquivos existentes de `css/` e `js/` registrados no `plan.md`
- [ ] T004 Registrar permissoes, recursos, perfis e requisitos de link assinado do `plan.md` → verify: cada acao nova com recurso SIP no `plan.md`

## Fase 2: Trabalho Fundamental

**Objetivo**: Implementar pre-requisitos compartilhados que bloqueiam as historias de usuario.

- [ ] T005 Registrar impactos em DTO/RN/BD/API e contratos bloqueantes do `plan.md` antes de criar ou alterar arquivos do modulo → verify: nenhum contrato `BLOCKED` no `plan.md`
- [ ] T006 Criar ou atualizar tarefas de script de release SEI/SIP quando houver mudancas em BD, recurso, menu ou perfil → verify: uma tarefa de script para cada mudanca de BD, recurso, menu ou perfil do `plan.md`
- [ ] T007 Criar ou atualizar tarefas de recurso/perfil/menu SIP quando `plan.md` declarar impacto SIP → verify: uma tarefa para cada recurso, perfil e menu SIP do `plan.md`

## Fase 3: Historia de Usuario 1 - [Titulo] (Prioridade: P1)

**Objetivo**: [Breve descricao do que esta historia entrega]

**Teste Independente**: [Como verificar que esta historia funciona de forma isolada]

### Implementacao da Historia de Usuario 1

- [ ] T008 [US1] Implementar pagina/acao em `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/<arquivo>.php` → verify: `php -l <arquivo>.php` sem erro
- [ ] T009 [US1] Adicionar `validarLink` e `validarPermissao` para o recurso da acao em `<arquivo>.php` → verify: `python3 .agents/skills/sei-verificacao-pagina/audit.py --input <arquivo>.php` sem P1 nem P2
- [ ] T010 [US1] Normalizar parametros GET/POST via `PaginaSEI::GET/POST` em `<arquivo>.php` → verify: `python3 .agents/skills/sei-verificacao-pagina/audit.py --input <arquivo>.php` sem P5 nem P6
- [ ] T011 [US1] Conectar pagina/acao a camada RN/API definida no `plan.md` → verify: pendente do desenvolvedor (a acao executa o fluxo da RN/API do `plan.md`)

**Checkpoint**: Historia de Usuario 1 e executavel de forma independente e falhas de permissao sao tratadas.

## Fase 4: Historia de Usuario 2 - [Titulo] (Prioridade: P2)

**Objetivo**: [Breve descricao do que esta historia entrega]

**Teste Independente**: [Como verificar que esta historia funciona de forma isolada]

### Implementacao da Historia de Usuario 2

- [ ] T012 [US2] Implementar alteracoes especificas desta historia no modulo com caminhos exatos de arquivos → verify: `php -l` sem erro em cada arquivo alterado
- [ ] T013 [US2] Atualizar comportamento compartilhado de RN/BD/API se necessario para esta historia → verify: o Teste Independente da Historia de Usuario 1 continua passando

**Checkpoint**: Historia de Usuario 2 funciona sem quebrar a Historia de Usuario 1.

## Fase N: Release e Validacao

**Objetivo**: Validar sintaxe, encoding, compatibilidade de release e cenarios de smoke manual.

- [ ] T900 Executar `php -l` em todos os arquivos PHP alterados → verify: `No syntax errors detected` em cada arquivo
- [ ] T901 Verificar o encoding dos arquivos PHP alterados ou gerados: ISO-8859-1 (Latin-1) em arquivo novo e o encoding que o arquivo ja tinha nos isentos do filtro do Git → verify: `file <arquivo>` mostra esse encoding e nenhum BOM
- [ ] T902 Executar checks do Composer disponiveis (`composer test`, `phpcs`, `phpstan`) quando configurado → verify: comandos sem erro; ferramenta configurada que nao roda fica `pendente do desenvolvedor (<ferramenta>: <motivo>)`
- [ ] T903 Validar sincronizacao de versao SEI/SIP quando scripts de release foram alterados → verify: a mesma versao em `*Integracao.php` e nos scripts SEI e SIP
- [ ] T904 Smoke-test do caminho principal de sucesso, negacao de permissao, link invalido, parametros invalidos e sessao expirada quando aplicavel → verify: pendente do desenvolvedor (roteiro do smoke na resposta)
- [ ] T905 Atualizar `docs/requisitos-ancorados/<modulo>/` com os IDs de Requisitos Ancorados Afetados da `spec.md`, quando houver → verify: cada ID adicionado ou alterado aparece no arquivo do modulo com o texto novo, e cada ID retirado saiu dele

## Dependencias e Ordem de Execucao

- Preparacao e Descoberta devem ser concluidas antes das tarefas de implementacao.
- Trabalho Fundamental deve ser concluido antes das tarefas de historia de usuario que dependem dele.
- Tarefas de geracao de CRUD dependem de contratos confirmados quando `Gerador Necessario: sim`.
- Tarefas de Release e Validacao dependem de todos os arquivos PHP alterados estarem em locais finais.

## Oportunidades de Paralelismo

- Inspecoes independentes de arquivos podem executar em paralelo.
- Historias de usuario podem executar em paralelo apenas quando tocam arquivos diferentes e nao dependem da mesma alteracao de RN/BD/API.
- Comandos de validacao podem executar apos todos os arquivos dependentes estarem em suas localizacoes finais.

## Observacoes

- Substituir todos os caminhos e placeholders de exemplo no `tasks.md` gerado.
- Nao manter tarefas que nao se aplicam a feature ativa.
- Nao criar tarefas fora do escopo de escrita permitido por `AGENTS.md`.
