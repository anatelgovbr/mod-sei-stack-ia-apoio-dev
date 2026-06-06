---
description: "Lista de tarefas para implementacao de feature em modulo SEI"
---

# Tarefas: [NOME DA FEATURE]

**Entrada**: Documentos de design em `/specs/[###-nome-feature]/`
**Pre-requisitos**: `plan.md` e `spec.md`; opcionais: `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Testes**: Incluir tarefas de teste apenas quando solicitado pela spec, pelo desenvolvedor ou por gate de validacao SEI aplicavel.

**Organizacao**: Tarefas agrupadas por historia de usuario testavel de forma independente sempre que possivel.

## Formato: `[ID] [P?] [US?] Descricao`

- **[P]**: Pode executar em paralelo porque altera arquivos diferentes e nao tem conflito de dependencia.
- **[US]**: Usar `[US1]`, `[US2]`, etc. apenas para tarefas de implementacao de historia de usuario.
- Incluir o caminho exato do arquivo em toda tarefa que cria ou altera arquivos.

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
- Tarefas de validacao com `sei-testes` devem aparecer na fase final de validacao para qualquer alteracao de codigo SEI.

## Gate do Gerador de CRUD (Condicional)

- Fonte de regras: `.specify/memory/constitution.md` secao `Gerador de CRUD InfraPHP` e o campo `Gate do Gerador de CRUD` preenchido no `plan.md`.
- Se `plan.md` indicar `Gerador Necessario: sim`, o `Status do Gate de Planejamento` deve ser `PASS` antes de qualquer tarefa de geracao.
- Tarefas que geram ou escrevem manualmente arquivos CRUD base NAO devem aparecer antes dos contratos JSON confirmados em `specs/[###-nome-feature]/crud-contratos/`.
- Se `Gerador Necessario: nao`, nao criar tarefas de `crud-contratos/`; tarefas de implementacao manual de CRUD ainda exigem contratos funcionais claros no `plan.md` antes de qualquer alteracao de codigo.

<!--
  As secoes abaixo sao exemplos de estrutura. O tasks.md gerado DEVE substituir
  as tarefas de exemplo por tarefas concretas derivadas de spec.md, plan.md e historias de usuario.
-->

## Fase 1: Preparacao e Descoberta

**Objetivo**: Confirmar escopo, estrutura do modulo, scripts, permissoes e assets existentes.

- [ ] T001 Identificar caminho do modulo-alvo em `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/`
- [ ] T002 Inspecionar scripts SEI/SIP existentes usando `.agents/references/mapa-modulos-scripts.md`
- [ ] T003 Inspecionar assets existentes em `css/` e `js/` antes de planejar alteracoes de assets
- [ ] T004 Registrar permissoes, recursos, perfis e requisitos de link assinado do `plan.md`

## Fase 2: Trabalho Fundamental

**Objetivo**: Implementar pre-requisitos compartilhados que bloqueiam as historias de usuario.

- [ ] T005 Registrar impactos em DTO/RN/BD/API e contratos bloqueantes do `plan.md` antes de criar ou alterar arquivos do modulo
- [ ] T006 Criar ou atualizar tarefas de script de release SEI/SIP quando houver mudancas em BD, recurso, menu ou perfil
- [ ] T007 Criar ou atualizar tarefas de recurso/perfil/menu SIP quando `plan.md` declarar impacto SIP

## Fase 3: Historia de Usuario 1 - [Titulo] (Prioridade: P1)

**Objetivo**: [Breve descricao do que esta historia entrega]

**Teste Independente**: [Como verificar que esta historia funciona de forma isolada]

### Implementacao da Historia de Usuario 1

- [ ] T008 [US1] Implementar pagina/acao em `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/<arquivo>.php`
- [ ] T009 [US1] Adicionar `validarLink` e `validarPermissao` para o recurso da acao
- [ ] T010 [US1] Normalizar parametros GET/POST via `PaginaSEI::GET/POST`
- [ ] T011 [US1] Conectar pagina/acao a camada RN/API definida no `plan.md`

**Checkpoint**: Historia de Usuario 1 e executavel de forma independente e falhas de permissao sao tratadas.

## Fase 4: Historia de Usuario 2 - [Titulo] (Prioridade: P2)

**Objetivo**: [Breve descricao do que esta historia entrega]

**Teste Independente**: [Como verificar que esta historia funciona de forma isolada]

### Implementacao da Historia de Usuario 2

- [ ] T012 [US2] Implementar alteracoes especificas desta historia no modulo com caminhos exatos de arquivos
- [ ] T013 [US2] Atualizar comportamento compartilhado de RN/BD/API se necessario para esta historia

**Checkpoint**: Historia de Usuario 2 funciona sem quebrar a Historia de Usuario 1.

## Fase N: Release e Validacao

**Objetivo**: Validar sintaxe, encoding, compatibilidade de release e cenarios de smoke manual.

- [ ] T900 Executar `php -l` em todos os arquivos PHP alterados
- [ ] T901 Verificar que arquivos PHP alterados/gerados estao em ISO-8859-1 (Latin-1)
- [ ] T902 Executar checks do Composer disponiveis (`composer test`, `phpcs`, `phpstan`) quando configurado
- [ ] T903 Validar sincronizacao de versao SEI/SIP quando scripts de release foram alterados
- [ ] T904 Smoke-test do caminho principal de sucesso, negacao de permissao, link invalido, parametros invalidos e sessao expirada quando aplicavel

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
