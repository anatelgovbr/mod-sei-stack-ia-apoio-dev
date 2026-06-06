# Runbook Operacional — SEI SDD

Arquivo canonico de memoria operacional. Portavel — legivel por qualquer ferramenta de IA.

## Regras de Curadoria
- Re-priorizar a cada leitura.
- Manter apenas notas recorrentes e de alto valor.
- Maximo 10 itens por categoria.
- Cada item inclui data + acao concreta ("Do instead").

## Execucao e Validacao (Prioridade Maxima)
1. **[2026-04-28] Keep Spec Kit optional**
   Do instead: only start `/speckit.*` when the developer explicitly chooses that flow.
2. **[2026-05-04] Verify encoding after patching legacy PHP**
   Do instead: after editing old SEI/SIP scripts with accented literals, scan for `U+FFFD`/mojibake and compare with `git show HEAD:<file>` before final lint.
3. **[2026-04-29] Gate CRUD generator output**
   Do instead: when `sei-crud-code-generator` is selected, require confirmed JSON contracts before generating or editing CRUD base files.
4. **[2026-04-29] Validate CRUD generator changes with generated fixtures**
   Do instead: after editing `generate_from_contrato.py` or templates, generate simple/FK/N:N contracts in `/tmp` and run `php -l` on all 6 outputs per contract.
5. **[2026-04-28] Validate changed PHP**
   Do instead: run `php -l` on every changed PHP file and preserve ISO-8859-1 encoding.
6. **[2026-04-30] Use sei-banco-dados-check for code review de modelagem**
   Do instead: para auditar DTOs/BDs ou DDLs contra os padroes TRF4, rodar `python3 .agents/skills/sei-banco-dados-check/audit.py --input <path> --format markdown`; exit code 0=PASS, 1=WARN, 2=BLOCK.
7. **[2026-04-30] Pipeline de gates para modulos SEI**
   Do instead: apos implementar/modificar arquivos de modulo SEI, rodar `sei-pagina-seguranca-check` -> `sei-rn-transacao-check` -> `sei-tarefa-modulo-check` -> `sei-testes` quando os arquivos aplicarem.

## Domain Behavior Guardrails
1. **[2026-04-30] Do not apply SEI integration activation rules to SIP scripts**
   Do instead: in `sip/scripts/*`, only handle SIP resources/menus/profiles/audit/parameters; never add `ConfiguracaoSIP`, `SIP/Modulos`, or `class_exists(*Integracao)` checks unless SIP context explicitly supports it.
2. **[2026-04-30] List inactive records with explicit criteria**
   Do instead: in `*_reativar` list actions, call `setBolExclusaoLogica(false)` and add `adicionarCriterio(array('SinAtivo'), array(InfraDTO::$OPER_IGUAL), array('N'))`; do not rely only on `setStrSinAtivo('N')`.
3. **[2026-04-28] Keep human docs out of agent runtime**
   Do instead: do not reference `docs/README_KIT_IA.md` from `AGENTS.md`; treat it as human-facing documentation.
4. **[2026-04-28] Avoid core edits without approval**
   Do instead: document a proposal instead of patching SEI/SIP/Infra core paths outside the allowed module/script scope.

## Shell & Command Reliability
1. **[2026-04-28] `rg` may be unavailable**
   Do instead: prefer Glob/Grep tools, or use POSIX `grep` only when command-line filtering is necessary.

## User Directives
1. **[2026-05-07] Never add Active Technologies / Recent Changes to AGENTS.md**
   Do instead: AGENTS.md is a permanent directive file — never append session metadata, feature logs, or technology lists derived from plan.md to it. Those belong in `.agents/log.md` or `.agents/memory/runbook.md`.
2. **[2026-04-28] Keep MR scope clean**
   Do instead: warn before including unrelated local changes in MR summaries or integration plans.
2. **[2026-04-30] Do not infer Portuguese domain labels**
   Do instead: fix only universal CRUD UI text in the generator and emit developer alerts for domain labels, accents, singular/plural, titles, captions, `title`, and `alt`.
