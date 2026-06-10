# SEI — Modulos SEI Constitution

## Uso no Spec Kit

Use este arquivo apenas em `/speckit.*`.
Use a documentacao funcional existente no repositorio como fonte para spec, plan e tasks. Se faltar regra de negocio, peca contexto ao desenvolvedor.
Em conflito com `AGENTS.md` dentro do fluxo Spec Kit, siga este arquivo para regras de fase e bloqueio.

## Hierarquia de Verdade e Politica de Conflito

No fluxo Spec Kit, use a seguinte precedencia:

1. `.specify/memory/constitution.md` (este arquivo)
2. `.agents/references/skill-routing-and-contracts.md` (extensao normativa)
3. `.specify/templates/` (estrutura de artefatos)
4. `AGENTS.md` (guardrails universais + ponto de entrada)
5. Skills individuais (especializacao por tipo de demanda)

Fonte de verdade para roteamento: `.agents/references/skill-routing-and-contracts.md`. Nao redefinir a matriz aqui.

## Modulo-Alvo Obrigatorio no /speckit.specify

Determine o modulo-alvo antes de continuar. Use-o para definir caminho de arquivos, nomes fisicos e verificacao do `mapa-modulos-scripts.md`.

**Regra de estrutura**: subpastas de modulo sao sempre camadas tecnicas (`dto/`, `rn/`, `bd/`, `int/`, paginas na raiz do modulo). Entidades de negocio **nunca geram subpastas proprias**. Um mesmo modulo acolhe multiplas entidades compartilhando as mesmas pastas de camada.

**Dois padroes validos de caminho de modulo** (verificar sempre o filesystem):
- Modulo plano: `fontes/.../modulos/<modulo>/` — ex.: `modulos/relacionamento-institucional/`, `modulos/ia/`
- Modulo com namespace: `fontes/.../modulos/<namespace>/<modulo>/` — ex.: `modulos/trf4/julgamento/`, `modulos/abc/exemplo/`

Se o modulo-alvo nao estiver inequivoco, pare e pergunte ao desenvolvedor.

## Skill Routing Gate

`/speckit.plan` deve classificar a demanda e registrar skill, contratos e bloqueios aplicaveis usando `.agents/references/skill-routing-and-contracts.md`.

- Quando uma skill exigir contrato, o contrato deve existir antes de qualquer tarefa de implementacao que dependa dele.
- Se o contrato estiver ausente, incompleto ou ambiguo, o gate deve ser `BLOCKED`.
- `/speckit.tasks` nao pode gerar tarefas de implementacao para area com contrato `BLOCKED`.
- `/speckit.implement` deve parar se houver contrato obrigatorio com status diferente de `PASS`.

## Gerador de CRUD InfraPHP

Opt-in explicito do desenvolvedor. Contrato JSON confirmado antes de gerar. Sem contrato confirmado e salvo em `specs/<feature>/crud-contratos/<tabela>.json`, o plan nao pode ser dado como concluido. Regras detalhadas na skill `sei-gerador-crud`.

Se nao usar o gerador, CRUD manual segue roteamento padrao com release via skill.
