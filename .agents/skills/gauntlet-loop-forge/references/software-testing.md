# Software Test Strategy for Gauntlet Work

## Contents

- Test-layer selection
- Test doubles and fidelity
- Contract testing
- Property/invariant and parameterized tests
- Mutation testing
- Security verification
- Reliability and fault tolerance
- Performance and scalability
- Database and migration testing
- Static and build gates
- Test quality and flakiness
- Evidence hierarchy
- Sources


Use this reference to choose **the smallest test portfolio that gives strong evidence for the specific risk**, not to maximize test count.

The TDD micro-loop and the test contract for each change type live in `software-engineering.md`. This file is about which tests to build and what makes their evidence strong.

## 1. Test-layer selection

Use a portfolio rather than relying on a single test type.

### Small/unit/component tests

Use for fast, specific feedback on logic and edge cases. Prefer many fast tests where they provide real confidence.

### Integration tests

Use to prove components/dependencies collaborate correctly, especially where isolated tests could pass while wiring/contracts fail.

### End-to-end / critical user journey tests

Use a smaller number for high-value workflows and system fidelity, and isolate the same failure with cheaper focused tests wherever they can.

Balance the suite by tradeoffs in speed, maintainability, utilization and cost, reliability and flakiness, and fidelity to production conditions, rather than by a fixed numeric unit, integration, and E2E ratio.

## 2. Test doubles and fidelity

Prefer the highest-fidelity dependency that remains practical and deterministic:

1. real implementation when safe/practical;
2. a maintained fake when real use is impractical;
3. mocks/stubs when needed for isolation or hard-to-trigger cases.

Keep the behavior under test real, and reach for a double only for the dependencies around it.

## 3. Contract testing

For service/API/event integrations, use contract tests when they provide faster, more focused evidence than broad E2E tests. Verify both consumer expectations and provider conformance as appropriate to the architecture.

A contract test earns its name from behavioral consumer and provider evidence. Static schema validation is a separate, weaker check.

## 4. Property/invariant and parameterized tests

Use when behavior can be expressed as invariants across broad input spaces, boundary values, or combinatorial cases. They are especially useful for parsers, serialization, algorithms, financial/math rules, transformations, state machines, and data processing.

Record seeds/examples needed to reproduce a discovered failure.

## 5. Mutation testing

For high-risk changed logic where tooling exists, mutation testing can test the **tests**: intentionally modified production behavior should be caught by the suite.

Use mutation score as supporting evidence, not a universal threshold. Investigate important surviving mutants rather than gaming the number.

## 6. Security verification

For security-relevant systems, derive tests from actual threats and requirements. Where applicable use recognized verification requirements such as OWASP ASVS as a source for technical security controls.

Potential evidence includes:

- authn/authz boundary tests;
- injection/untrusted-input cases;
- secret/PII handling;
- dependency/SAST findings;
- session/crypto/configuration controls;
- least privilege;
- abuse/rate-limit/error-path behavior.

A clean generic unit suite is not a substitute for security verification.

## 7. Reliability and fault tolerance

Test relevant failure modes:

- timeout;
- retry and duplicate delivery;
- idempotency;
- partial dependency failure;
- stale state/concurrency/races;
- restart/recovery;
- rollback;
- queue/event reprocessing;
- degraded mode;
- data consistency after failure.

Use fault injection or controlled dependency failures when appropriate.

## 8. Performance and scalability

When performance matters, define a baseline/threshold before optimization and measure under reproducible conditions.

Possible gates:

- latency percentiles;
- throughput;
- memory/CPU/resource use;
- load/scalability behavior;
- soak stability;
- regression tolerance against a frozen baseline.

Accept a benchmark that reproduces the conditions of the requirement it claims to prove.

## 9. Database and migration testing

As applicable verify:

- forward migration;
- backward/compatibility window;
- idempotency/retry behavior;
- data invariants;
- rollback/restore plan;
- large-data/runtime characteristics;
- deployment ordering with mixed application versions.

Destructive production actions remain human-gated.

## 10. Static and build gates

Use project-appropriate build, compiler/type, lint, formatting-policy, static-analysis, generated-schema, and dependency checks as objective evidence. A user-defined functional requirement outranks style-only tooling, unless that tooling is a mandatory project gate.

## 11. Test quality and flakiness

A verifier should reject tests that are:

- non-deterministic without controlled/reproducible conditions;
- assertion-free or trivially true;
- coupled to irrelevant implementation details;
- so heavily mocked that they cannot catch the target defect;
- weakened, skipped, or deleted merely to make the suite green;
- duplicative without adding risk coverage.

Record and isolate known flaky tests rather than silently rerunning until green. Retry budgets remain finite and visible.

## 12. Evidence hierarchy for software

Prefer, roughly:

1. failing pre-change acceptance/regression evidence when feasible;
2. focused passing post-change test;
3. relevant broader regression/integration suite;
4. runtime/contract evidence;
5. non-functional/security/reliability evidence;
6. code review/static inspection;
7. subjective comparison only for dimensions not objectively decidable.

## 13. Sources informing this profile

- Martin Fowler, Test-Driven Development (Red–Green–Refactor and maintaining a test list): https://martinfowler.com/bliki/TestDrivenDevelopment.html
- Google Testing Blog, testing pyramid and SMURF tradeoffs: https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html and https://testing.googleblog.com/2024/10/
- Google Testing Blog, test fidelity and test doubles: https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html
- Pact documentation, consumer/provider contract testing: https://docs.pact.io/
- Hypothesis documentation, property-based testing: https://hypothesis.readthedocs.io/
- PIT/Stryker documentation, mutation testing: https://pitest.org/ and https://stryker-mutator.io/docs/
- OWASP ASVS, technical security verification requirements: https://owasp.org/www-project-application-security-verification-standard/
