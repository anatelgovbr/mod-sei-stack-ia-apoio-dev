---
name: gauntlet-loop-forge
description: Gauntlet Loop prompt forge. Use to build a paste-ready Gauntlet Loop execution prompt from whatever material the user brings, or to diagnose and rewrite a Gauntlet Loop prompt that already exists.
---

# Gauntlet Loop Forge

Create or optimize a **paste-ready Gauntlet Loop execution prompt**. Produce the prompt and stop there. Execute the underlying mission only when separately asked.

Invariants to preserve in every prompt produced:

1. give the lead agent the destination and the hard constraints, and leave the route to it;
2. give it a bar it can read, run, render, or measure;
3. let the lead split the mission into the smallest independently judgeable workstreams;
4. approval comes from a critic that did not build the artifact;
5. critics judge the current artifact and its direct evidence;
6. deterministic evidence decides whatever it can decide, and blind comparison covers the rest;
7. evidence-backed `PASS` stops the loop early;
8. every iterative path carries a finite ceiling, and reaching it yields `CAPPED`;
9. raising a ceiling takes explicit human approval.

Read `references/method-core.md` when fidelity to the original method is uncertain.

## 1. Extract before asking

Accept an inline idea, goal, existing prompt, PRD, issue, plan, specification, requirements document, repo context, or other source material.

Extract every usable fact first, and treat a designated source of truth as authoritative unless the user overrides it. Ask only for what the material leaves open. Name contradictions and let the user settle them.

Finding facts is your job: when an item depends on a fact the environment holds, look it up, dispatching a subagent where the runtime allows it, instead of asking the user for what you can consult. The decisions are the user's: put each one to them.

If the target environment lacks separate contexts or subagents, say that independence is degraded and write a portable approximation. Same-context self-review is a builder judging itself, so call it that.

## 2. Classify the mission and load only relevant specialization

Classify after the first extraction pass. A mission may be single-domain or mixed.

Always use the general core, then load only what the mission needs:

- quality-bar patterns by domain: `references/domain-bars.md`;
- **any material software or engineering part:** `references/software-engineering.md` and `references/software-testing.md`, before finalizing acceptance criteria, delegation contracts, or verification gates;
- uncertain or subjective judging: `references/verification-protocol.md`;
- every mission: `references/bounded-execution.md` for the finite safety envelope.

Software is activated by any material software or engineering part of the mission, such as code and repositories, infrastructure and databases, or technical automation.

For mixed missions, compose compatible verification layers and let each part keep its own bar.

Read `references/intake-routing.md` for routing and interview logic.

## 3. Interview in layers until the prompt is buildable and judgeable

Emit the artifact only when all fourteen items below carry a value, where a value is the user's answer or your own derivation labeled `DERIVED`. An item the mission does not use carries a value saying so. Nothing stays silently assumed.

Work the items in rounds. The frontier is every item whose prerequisites are already settled: ask the whole frontier in one round, and leave for a later round any item whose answer depends on an item still open. Number each question and give the answer you recommend, so the user can accept it in one word; that recommendation is the conservative derivation, and it keeps the `DERIVED` label when the user accepts it or delegates the decision. A fact search still running is an unsettled prerequisite: only the items downstream of it wait, and the rest of the frontier goes out in the current round. Recompute the frontier after every round of answers.

Resolve, at minimum:

1. **Mission:** concrete outcome and intended user-visible or system-visible result.
2. **Artifacts:** the real outputs that will exist and be inspected.
3. **Starting state and source of truth:** greenfield, existing artifact, rewrite, repair, optimization, evaluation, migration.
4. **Scope boundaries:** in scope, out of scope, preserved behavior, dependencies.
5. **Target harness or runtime:** Claude Code or SDK, Codex, OpenAI Agents SDK, another agentic runtime, plain chat, or unknown.
6. **Acceptance criteria:** observable conditions for completion.
7. **Quality bar:** exemplar, benchmark, test suite, rubric, gold output, reference implementation, threshold, or hybrid bar the critic can inspect.
8. **Verification plan and hard gates:** objective checks that must pass, plus comparative judging where it adds signal.
9. **Quality dimensions:** correctness, clarity, robustness, security, latency, accessibility, maintainability, groundedness, fidelity, compliance, as relevant.
10. **Hard constraints versus preferences:** language, format, stack, compatibility, length, platform, policy and legal boundaries, style.
11. **Tools, data, access, permissions:** what the agents may read, run, edit, fetch, test, deploy, spend, or call.
12. **Human gates and irreversible actions:** what takes explicit approval.
13. **Maximum effort:** one plain-language question about the maximum number of improve-and-check rounds each important part may use. The user gives a number, picks a concise option, or delegates. Ask it as specified in `references/bounded-execution.md`, and keep turns, invocations, delegation depth, concurrency, and fan-out out of the question.
14. **Observability:** evidence ledger and the evidence types to retain.

Translate the maximum-effort answer into every finite technical limit the runtime and prompt require, using the derivation in `references/bounded-execution.md`. Mark derived values `DERIVED` and keep them distinct from user requirements. Explain the choice back to the user as a number of improve-and-check rounds.

Architecture, file layout, decomposition, and implementation sequence belong to the lead agent. Ask about them only when the user treats them as genuine constraints.

## 4. Resolve the quality bar

A bar must be sufficiently:

- **concrete:** named or operationally defined;
- **inspectable:** the verifier can read, run, render, or measure it;
- **comparable:** candidate and bar share explicit evaluation dimensions;
- **reproducible:** material comparison conditions are stable or documented;
- **challenging:** it prevents easy rubber-stamping.

Prefer a **hybrid bar** when one mechanism cannot settle every dimension: deterministic gates for objective properties plus an exemplar or rubric for subjective ones.

Convert "world-class", "production-ready", "perfect", "clean", "enterprise-grade", and their equivalents into observable criteria before accepting them.

If the user has no usable bar, propose two or three concrete candidates or a measurable equivalent. If finding the right bar takes domain investigation, make bar discovery the lead agent's first bounded workstream, with its own acceptance check.

## 5. Build roles and evidence flow

Define roles without unnecessary vendor lock-in:

- **Lead or orchestrator:** interprets the mission, chooses the decomposition, manages dependencies and the finite budget, tracks evidence, integrates the whole. Implementation it authored is graded by someone else.
- **Executor per workstream:** creates or revises one bounded piece and produces direct evidence. It self-checks, and `PASS` comes from the verifier.
- **Fresh verifier:** receives the goal, assigned criteria, the actual artifact, relevant constraints, and direct evidence, and decides against the bar. The executor's self-assessment and rationale stay out of the packet.
- **Integrator:** reconciles interfaces, consistency, regressions, and cross-workstream effects after local convergence.
- **Fresh final verifier:** evaluates the integrated whole against global acceptance criteria and gates.

Parallelize genuinely independent workstreams, up to the concurrency cap.

**Dispatch packet.** The lead hands each executor its scope, its assigned criteria and bar, the mandatory checks to run, the state vocabulary its verdicts must use, the ceiling for that invocation, and the shape of the return. The verifier packet is specified in `references/verification-protocol.md`.

**Workstream boundary.** An executor judges only what it was assigned. A genuine finding outside that scope goes to the lead with its full evidence trail, and never changes the state of the workstream that found it. The lead decides where it belongs.

For software missions, `references/software-engineering.md` and `references/software-testing.md` constrain the executor and verifier contract further.

## 6. Use evidence-first verification

A verifier inspects the **actual current artifact and version** plus direct evidence. Builder claims are not evidence. A mandatory gate that was never run counts as missing evidence.

An **absence claim**, such as no external side effect, no regression, no leak, or nothing left uncovered, carries the heaviest burden of all, because a search that never looked returns exactly what an exhaustive one returns. Such a claim states the space it examined, the depth it reached, and the leaves it left unopened. A pattern search is support, never the proof by itself. A relevant unopened leaf makes the claim `INCONCLUSIVE`, never `PASS`.

On a failed cycle the verifier returns at least:

- the verdict;
- criterion-by-criterion evidence, or the evidence that is missing;
- every blocking finding;
- the single highest-impact remaining gap;
- an objective acceptance check for the next revision;
- residual non-blocking risks when material.

For pairwise or LLM judging, mask provenance when feasible and reverse A/B order, under the protocol in `references/verification-protocol.md`.

Read `references/verification-protocol.md` for the evidence packet and evaluation order.

## 7. Make the loop bounded without confusing caps with quality

One local cycle is the sequence in `references/bounded-execution.md`, and the next cycle starts from that verdict, those blocking findings, the largest gap, and the next acceptance check. Between cycles, the verifier's full deliberation and the accumulated history stay behind, and the executor attacks the largest gap first inside its assigned scope.

Before each spawn, the lead checks the remaining budget and spawns only while the applicable ceiling holds.

Rules:

1. stop immediately when assigned criteria and gates earn evidence-backed `PASS`;
2. keep every local and global cap;
3. count hidden retries, self-fix loops, extra reviewers, replans, tool-runner loops, and nested agents against explicit budgets;
4. keep fan-out within `MAX_DELEGATION_DEPTH`;
5. on stagnation, replan, split, or escalate instead of repeating the same attempt until the cap;
6. on any hard ceiling reached before `PASS`, return `CAPPED` with unresolved findings and the recommended next action;
7. a continuation envelope comes only from explicit human approval;
8. reserve the integration and final-verification budget before distributing the rest, so the closing step is never the one that gets cut.

A maximum is a safety boundary, not a quality target, and this method sets no minimum: a single excellent, independently verified cycle may be enough.

A workstream `PASS` is provisional until final integration verification. If integration reveals a regression in a workstream that already passed, reopening it spends that workstream's remaining cycles. With none remaining, the run ends `CAPPED`.

Read `references/bounded-execution.md` for budget derivation, inheritance, accounting, and stagnation handling.

## 8. Require honest statuses

A **cycle verdict** is what one verifier returns about one candidate:

- `PASS`: assigned criteria and gates are evidenced;
- `FAIL`: the current version does not meet them;
- `INCONCLUSIVE`: evidence or judge consistency cannot support a stable verdict.

A **terminal state** ends a workstream or the run:

- `PASS`: all mandatory acceptance criteria and gates are evidenced, no blocking finding remains, and any required comparative bar is satisfied;
- `CAPPED`: a finite cycle, turn, spawn, time, token, or cost ceiling was reached before `PASS`;
- `BLOCKED`: access, permission, dependency, environment, data, or a human gate is unavailable;
- `ESCALATE`: requirements, bar, decomposition, or strategy need reframing;
- `STOPPED`: a human intentionally stopped the run.

While budget remains, `FAIL` starts another cycle and `INCONCLUSIVE` buys stronger evidence or a fresh judge within the verifier budget. When budget runs out first, the run ends `CAPPED`.

A run that ended without evidence reports the state it actually reached.

When the mission's own procedure carries a state vocabulary of its own, such as gate states, severity scales, or review verdicts, that vocabulary lives beside these statuses instead of replacing them. Carry it into the prompt, name it, and say which set governs what: these statuses govern the loop, the domain set governs the artifact.

## 9. Require a lightweight evidence ledger

The lead maintains a progress artifact appropriate to the harness, such as `workbench.md`, holding:

- workstream and owner;
- artifact or version locator;
- assigned acceptance criteria and bar;
- direct gate and evidence results;
- current cycle and remaining budget;
- verifier verdict and largest gap;
- change attempted and observed delta;
- open findings and residual risks;
- human gates;
- integration and final-verifier status.

Those fields are the whole ledger. Anything a reader would not audit stays out.

## 10. Adapt to the harness honestly

Map semantic limits onto runtime controls with `references/bounded-execution.md`.

## 11. Compose the final Gauntlet prompt

Assemble the returned artifact with `references/output-template.md`. It has two parts: the user's original prompt, reproduced unchanged, then the loop block appended after it under the headings and in the shapes that file gives. Return both parts every time, and keep the original prompt's wording as the user wrote it.

Keep it as short as enforceability allows. For software missions, carry only the software, TDD, and test clauses this task needs, selected from the software references.

## 12. Optimize an existing prompt

Diagnose the supplied prompt against these invariants and rewrite what materially improves fidelity, verification, boundedness, or domain fit.

Preserve the user constraints already in it. When the supplied prompt already carries a loop block, replace the block and leave the user's own part of the prompt unchanged. Strip duplicated methodology prose, arbitrary minimum-round requirements, unbounded retry paths, self-approval, vague bars, unsupported runtime commands, and irrelevant domain checks.

## 13. Self-gate before returning the prompt

Check the finished prompt against every rule in this file and in each reference you loaded, and against these two, which the prompt alone can answer:

- the user's original prompt is present unchanged, with the loop block appended after it;
- every acceptance criterion has a credible evidence path;
- every line is complete, every section holds one scope, and every identifier, title, path and command matches its source;
- the prompt is compact and executable as written.

Report what the last pass had to fix. Then return the paste-ready Gauntlet Loop prompt.
