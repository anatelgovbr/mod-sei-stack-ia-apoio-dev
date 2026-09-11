# Software Engineering Specialization

## Contents

- Goal
- Executable acceptance contracts
- TDD default for behavior changes
- TDD adaptations by change type
- Executor evidence contract
- Independent software verifier
- Engineering gates by task risk
- Whole-system completion


Load this reference whenever any material part of the mission is software/engineering.

## Goal

Make each software workstream concrete, executable, testable, independently reviewable, and bounded while preserving the lead agent's freedom to choose architecture and implementation details that the user did not constrain.

## Build acceptance criteria as executable contracts

Translate requirements into observable behaviors before implementation. Prefer examples with explicit inputs, outputs, state transitions, failure behavior, and non-functional thresholds.

Each software workstream should have:

- a bounded responsibility;
- relevant source-of-truth acceptance criteria;
- an explicit verification plan;
- a TDD/test contract appropriate to its change type;
- direct evidence required from the executor;
- independent verifier criteria;
- local safety budget inherited from the global envelope.

Create workstreams a verifier can decide. A responsibility like “improve backend” or “make code production-ready” has no verdict, so give each one a bounded scope and an observable outcome.

## TDD is the default for behavior-changing implementation

For new behavior and bug fixes, require the executor to use a Red–Green–Refactor style loop at the smallest useful increment:

1. **Test list or next behavior:** identify the next observable behavior or defect case before changing production code.
2. **Red:** add or select a focused automated test that fails for the expected reason against the pre-change behavior, when technically feasible.
3. **Green:** make the smallest coherent production change needed to pass that test without breaking existing gates.
4. **Refactor:** improve structure while keeping relevant tests green.
5. **Broaden evidence:** run the appropriate higher-level regression/integration gates before handing to the verifier.

The Gauntlet executor→verifier cycle is not the same as the executor's internal Red–Green–Refactor micro-cycle. Both remain bounded: internal test/fix retries consume executor/turn budget.

## TDD adaptations by change type

### Bug fix

- First reproduce the defect with a regression test whenever feasible.
- Verify the new test fails for the defect, not because of unrelated setup.
- Implement the fix.
- Run the focused regression test plus relevant surrounding suite.

### New feature

- Start from acceptance behavior/examples.
- Add the smallest failing test that advances behavior.
- Avoid writing all tests after implementation merely to inflate coverage.

### Refactor with intended behavior preservation

- Establish sufficient characterization/regression tests first.
- Keep behavior green throughout the refactor.
- A forced failing test is not required when no behavior is supposed to change; the verifier should confirm preservation and structural objective instead.

### Legacy/hard-to-test code

- Establish characterization tests and/or create safe seams for observability/testability before risky changes.
- Prefer controlled dependency seams over broad mocking that bypasses the code most likely to fail.

### Configuration/infrastructure/migrations

- Use executable validation, plan/dry-run, policy tests, migration/recovery/idempotency tests, or environment checks as the “test first” contract where ordinary unit TDD is not meaningful.

### Performance/security/reliability work

- Define the failing benchmark, exploit/test case, fault scenario, or threshold first.
- Demonstrate the pre-change deficiency when safe and feasible.
- Implement and prove the target threshold/control afterward.

Every test earns its place by being able to fail for the behavior it names. When strict red-first execution is infeasible, the executor records the reason in the evidence ledger and uses the closest pre-change executable acceptance check.

## Executor evidence contract

Require, as relevant:

- changed artifact/diff/commit locator;
- test added/selected before implementation and its purpose;
- evidence of expected pre-change failure (`RED`) when feasible;
- focused passing result after implementation (`GREEN`);
- refactor result with tests still green;
- broader regression/integration results;
- build/type/static checks;
- runtime traces/logs/requests/responses;
- non-functional measurements;
- unresolved risks.

Accept a test result together with what ran and the artifact version it ran against.

## Independent software verifier

The verifier should:

1. inspect the actual diff/code and surrounding behavior;
2. confirm acceptance criteria are represented by meaningful tests/evidence;
3. detect tests that merely mirror implementation or cannot fail meaningfully;
4. confirm the regression/feature test targets the intended behavior;
5. rerun or independently inspect relevant gates where possible;
6. inspect second-order failures: boundary inputs, retries, idempotency, concurrency, partial failure, rollback, compatibility, auth boundaries, untrusted input, secrets/PII, observability, and performance regressions as applicable;
7. reject unrelated scope expansion or tests weakened/removed to obtain green;
8. return the largest material gap and next objective acceptance check.

## Engineering gates by task risk

Select gates proportional to the risk of the change.

Possible gates:

- unit/component tests;
- regression tests;
- integration tests;
- contract/API/schema tests;
- end-to-end/critical-user-journey tests;
- property/invariant tests;
- build/typecheck/lint/static analysis;
- concurrency/race/fault-injection tests;
- migration, rollback, backup/restore, or idempotency tests;
- security verification/SAST/dependency checks and threat-informed cases;
- performance/load/soak/latency/throughput/resource benchmarks;
- compatibility/version matrix;
- observability/telemetry validation;
- mutation testing on high-risk changed logic when the ecosystem supports it.

Read `software-testing.md` to choose and sequence tests.

## Whole-system completion

Local workstream success is insufficient. Integration must verify:

- interfaces/contracts between changed parts;
- representative end-to-end behavior;
- global regression gates;
- relevant security/reliability/performance properties;
- migration/deployment/rollback behavior when applicable;
- no acceptance criterion lost during integration.
