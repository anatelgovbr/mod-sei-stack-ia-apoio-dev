# Evidence-First Verification Protocol

The failure contract a verifier returns lives in `SKILL.md` section 6, and the statuses it may use in section 8. This reference covers what the verifier receives, how it evaluates, and when comparative judging is legitimate.

## Evidence packet

A verifier evaluates the actual current artifact and version. Give it only what it needs to judge fairly:

- the mission and the assigned acceptance criteria;
- the applicable quality bar or reference;
- the hard constraints;
- the artifact itself, or a locator for the current version;
- direct measurements, test results, rendered output, traces, source evidence, calculations, or other task-appropriate proof;
- the comparison conditions.

The packet ends at the artifact and its evidence: the executor's self-assessment, effort narrative, and reasoning stay behind. Builder claims are not evidence.

## Evaluation order

1. confirm the evidence corresponds to the current artifact and not to an earlier revision;
2. evaluate the mandatory deterministic and hard gates;
3. inspect domain-specific failure modes and side effects;
4. evaluate the non-functional and quality dimensions;
5. use a rubric, reference, or pairwise judging only for dimensions not already settled objectively;
6. return the verdict and the next acceptance check.

One failed mandatory gate prevents `PASS`, and one that was never run yields `INCONCLUSIVE`.

The verifier may diagnose a failure but does not become the implementation owner.

## Absence claims

A claim that something is *not* present fails in a way a positive claim does not: an unperformed search and an exhaustive one return the same empty result. Require the claimant to supply:

- the space examined, enumerated rather than described;
- the depth reached;
- the leaves left unopened, named one by one;
- the method, where a pattern search counts as support and never as the proof.

A verifier rejects an absence claim resting on naming conventions, on tool output alone, or on a search whose space was never enumerated. A relevant unopened leaf yields `INCONCLUSIVE`.

## Pairwise and LLM-as-judge protocol

Use pairwise comparison only when it adds signal.

When possible:

1. mask candidate identity and provenance;
2. present candidate and reference under equivalent conditions;
3. judge A against B;
4. swap positions and judge again;
5. accept the content-level verdict only when it holds across both orders;
6. when the winner flips, return `INCONCLUSIVE` and reach for stronger evidence or another fresh judge.

A tie is acceptable only when the configured bar allows non-inferiority.

## Freshness

Use a fresh verifier context for each materially revised candidate whenever the harness supports separate contexts. A fresh context is what keeps the judgment on the artifact: a verifier carrying the executor's self-justification, or its own earlier deliberation, is judging something else.

Several verifiers are not automatically independent merely because there are several of them. Diversity of context, model, protocol, or evidence beats duplicated rubber-stamping.

## Whole-artifact verification

After local workstreams converge, evaluate the integrated whole for cross-boundary defects, inconsistencies, regressions, and the global acceptance criteria. Local passes do not imply a global pass, and a local `PASS` stays provisional until this step clears it.
