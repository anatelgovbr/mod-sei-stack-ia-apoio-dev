# SEI — Modulos SEI Constitution

## Uso no Spec Kit

Use este arquivo apenas em `/speckit.*`.
Use a documentação funcional existente no repositório como fonte para spec, plan e tasks. Se faltar regra de negócio, peça contexto ao desenvolvedor.
Em conflito com `AGENTS.md` dentro do fluxo Spec Kit, siga este arquivo para regras de fase e bloqueio.

## Contexto

Repositório de customizações e módulos do SEI com release versionada e padrões InfraPHP. Trate o projeto como sistema administrativo, com requisitos de auditoria, permissão e compatibilidade de release.

## Dependências Técnicas do Projeto

- Sistema Operacional Linux;
- **PHP 8.2** — encoding ISO-8859-1 (Latin-1)
- Extensões PHP previstas no manual de instalação do SEI
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

## Hierarquia de Verdade e Politica de Conflito

No fluxo Spec Kit, use a seguinte precedência:

1. `.specify/memory/constitution.md` (este arquivo)
2. `.agents/references/skill-routing-and-contracts.md` (extensão normativa)
3. `.specify/templates/` (estrutura de artefatos)
4. `AGENTS.md` (guardrails universais + ponto de entrada)
5. Skills individuais (especialização por tipo de demanda)

Fonte de verdade para roteamento: `.agents/references/skill-routing-and-contracts.md`. Não redefinir a matriz aqui.

## Módulo-Alvo Obrigatório no /speckit.specify

Determine o módulo-alvo antes de continuar. Use-o para definir caminho de arquivos, nomes físicos e verificação do `mapa-modulos-scripts.md`.

**Regra de estrutura**: subpastas de módulo são sempre camadas técnicas (`dto/`, `rn/`, `bd/`, `int/`, páginas na raiz do módulo). Entidades de negócio **nunca geram subpastas próprias**. Um mesmo módulo acolhe múltiplas entidades compartilhando as mesmas pastas de camada.

**Dois padrões válidos de caminho de modulo** (verificar sempre o filesystem):
- Módulo plano: `fontes/.../modulos/<modulo>/` — ex.: `modulos/relacionamento-institucional/`, `modulos/ia/`
- Módulo com namespace: `fontes/.../modulos/<namespace>/<modulo>/` — ex.: `modulos/trf4/julgamento/`, `modulos/abc/exemplo/`

Se o módulo-alvo não estiver inequívoco, pare e pergunte.

## Skill Routing Gate

`/speckit.plan` deve classificar a demanda e registrar skill, contratos e bloqueios aplicáveis usando `.agents/references/skill-routing-and-contracts.md`.

- Quando uma skill exigir contrato, o contrato deve existir antes de qualquer tarefa de implementação que dependa dele.
- Se o contrato estiver ausente, incompleto ou ambíguo, o gate deve ser `BLOCKED`.
- `/speckit.tasks` não pode gerar tarefas de implementação para área com contrato `BLOCKED`.
- `/speckit.implement` deve parar se houver contrato obrigatório com status diferente de `PASS`.

## Gerador de CRUD InfraPHP

Opt-in explicito do desenvolvedor. Contrato JSON confirmado antes de gerar. Sem contrato confirmado e salvo em `specs/<feature>/crud-contratos/<tabela>.json`, o plan não pode ser dado como concluido. Regras detalhadas na skill `sei-gerador-crud`.

Se não usar o gerador, CRUD manual segue roteamento padrão com release via skill.
