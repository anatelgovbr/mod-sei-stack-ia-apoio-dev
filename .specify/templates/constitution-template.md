# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->

---

<!-- EXEMPLO PARA PROJETOS SEI/PHP — remover esta secao antes de usar o template -->
<!--
## Hierarquia de Verdade e Politica de Conflito (SEI)

Em caso de conflito entre documentos, a ordem de precedencia e:
1. .specify/memory/constitution.md (este arquivo)
2. .agents/references/skill-routing-and-contracts.md (extensao normativa para roteamento)
3. .specify/templates/ (estrutura de artefatos)
4. AGENTS.md (guardrails universais)
5. Skills individuais
6. Playbooks

## Spec Kit como Ferramenta Opcional (SEI)

O uso do Spec Kit e decisao exclusiva do desenvolvedor.
A IA nao deve iniciar o fluxo Spec Kit por conta propria.

## Skill Routing Gate (SEI)

- Classificar demanda usando .agents/references/skill-routing-and-contracts.md
- Skill obrigatoria deve ser acionada antes de planejar implementacao
- Contrato obrigatorio ausente, incompleto ou ambiguo → registrar BLOCKED no plan.md
- /speckit.tasks nao pode gerar tasks de implementacao para area bloqueada
- /speckit.implement para se contrato com status diferente de PASS

## Portoes de Qualidade (SEI)

- php -l em todos os arquivos PHP alterados
- Encoding ISO-8859-1 obrigatorio
- validarLink + validarPermissao em toda acao
- assinarLink em links de acao
- Sem $_REQUEST; usar PaginaSEI::POST/GET
- Transacao para escrita relevante em BD
- Scripts SEI e SIP sincronizados com getVersao()

## Portabilidade de Release (SEI)

- DDL multi-SGBD: MySQL, PostgreSQL, Oracle, SQL Server
- Versoes SEI e SIP sincronizadas
- Seguir sei-modulo-release-scripts e playbook `release`
-->

