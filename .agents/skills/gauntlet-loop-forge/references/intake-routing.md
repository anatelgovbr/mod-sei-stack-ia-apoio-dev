# Intake and Mission Routing

## Contents

- Layer 0: extract supplied context
- Asking order
- Where each answer comes from
- Domain routing
- Action safety
- Effort sizing
- Interview behavior


Interrogate only what is missing, in layers, so a vague idea becomes a concrete Gauntlet input without forcing the user to design the implementation. `SKILL.md` section 3 holds the fields that must be resolved.

## Layer 0: extract supplied context

Before asking anything:

- read the user's idea, prompt, plan, PRD, specification, issue, file, repo context, or linked source;
- extract explicit requirements, checklists, metrics, SLAs, constraints, forbidden actions, human gates, references, and existing quality criteria;
- read what the environment itself reveals: test suites, CI configuration, schemas, style guides, lint rules, prior prompts, conventions;
- label each datum `USER`, `SOURCE`, or later `DERIVED`;
- surface contradictions instead of silently choosing a side.

## Asking order

Ask in this order, one compact batch per layer, skipping whatever Layer 0 already settled:

1. **Mission and artifact:** outcome, audience, artifacts, starting state, source of truth, harness. Resolve these before any verification question.
2. **Scope and success:** in and out of scope, preserved behavior, acceptance criteria, quality dimensions, hard constraints versus preferences, candidate bars.
3. **Verification and domain:** hard gates, comparative judging, and the specialization the mission triggers.
4. **Action safety:** tools, access, permissions, irreversible actions, approvals.
5. **Effort:** the single maximum-rounds question.

Acceptance criteria describe observable outcomes.

## Where each answer comes from

When a field is delegated to you, or the user is unsure, derive it from this order of evidence rather than inventing one:

| Field | Look here first | Conservative fallback |
|---|---|---|
| Mission and artifacts | The user's own statement, the issue body, the spec's goal section | Ask. This one is not derivable |
| Starting state and source of truth | An existing artifact, repo, draft, or prior version, and whichever document the material treats as authoritative | The largest existing artifact, stated as an assumption |
| Scope boundaries | Explicit in and out lists, the acceptance section, adjacent components the material protects | Narrowest reading that still delivers the mission |
| Harness or runtime | Configuration and instruction files present, the runtime the user is already using | An agentic runtime with subagents, plus the degraded note for plain chat |
| Acceptance criteria | Requirements, checklists, existing tests, defect reports, SLAs | The mission restated as observable conditions, one per artifact |
| Quality bar | Named exemplar, frozen test suite, benchmark, threshold, comparable deliverable, rubric already in use | Two or three concrete candidates offered to the user, or bar discovery as the first workstream |
| Verification and gates | Commands the project already runs, CI steps, review rules, the domain profile | Deterministic gates for objective properties plus a rubric for the rest |
| Quality dimensions | Non-functional requirements in the material, the domain profile | The domain default set, trimmed to what the mission can affect |
| Hard constraints | Stated musts, platform and compatibility facts, policy and legal limits, style guides in the repo | Treat stated preferences as preferences, and invent no constraint |
| Tools, data, permissions | Explicit grants, available credentials, the runtime's own permissions | Read-only. Anything not granted is forbidden |
| Human gates | Stated approvals, irreversible or external actions the mission implies | Gate every irreversible, external, spending, or destructive action |
| Maximum effort | An explicit limit in the material | The signal table in `bounded-execution.md` |
| Observability | An existing progress or ledger convention in the project | A single ledger file such as `workbench.md` |

Architecture, file layout, decomposition, and implementation sequence belong to the lead agent, and reach the prompt only where the material makes them genuine constraints.

## Domain routing

Classify the mission, then load only what applies. A mixed mission combines profiles instead of choosing one label.

### Software and engineering

Trigger when any material deliverable involves code, runtime behavior, technical configuration, infrastructure, APIs, databases, data pipelines, ML implementation, builds, migrations, debugging, refactoring, performance, or security engineering.

Load `software-engineering.md` and `software-testing.md`.

### Research and analysis

Prioritize source quality, coverage, reproducibility, citation and grounding requirements, methodological checks, and calculation verification.

### Writing and editorial

Prioritize factuality, audience comprehension, structure, clarity, evidence, length and format constraints, and a concrete comparison piece when one adds signal.

### Design, visual, and UX

Prioritize inspectable references, matched states and viewports, interaction behavior, accessibility and usability, and reproducible captures.

### Data and ML evaluation

Prioritize frozen datasets and splits, metrics, baselines, robustness, seed and repetition control, leakage checks, resource limits, and real-world failure modes. When the work also includes implementation, activate the software profile too.

### Documents, business, operations, and everything else

Use explicit deliverable checklists, factuality and completeness, consistency, process and state evidence, compliance constraints, and a concrete exemplar or rubric when useful.

Quality-bar patterns for every profile live in `domain-bars.md`.

## Action safety

Resolve, and fail closed on each:

- tools and data access;
- write, deploy, and publish permissions;
- secrets and credential handling;
- irreversible actions;
- spending and external side effects;
- required approvals.

Ambiguous authorization is not authorization. The generated prompt forbids the action or routes it through a human gate.

## Effort sizing

Ask the single maximum-rounds question and derive the technical envelope, both as specified in `bounded-execution.md`. Every effort answer resolves to a finite number before the prompt is written, and the internal limit names stay out of the questions.

## Interview behavior

- ask compact groups of related questions;
- recompute the gap list after each answer;
- ask only about what is still open;
- avoid implementation questions the lead agent should decide;
- derive instead of blocking when ambiguity is low-risk and the user delegated judgment;
- resolve before finalizing when the ambiguity changes success, permissions, or safety.
