# Bounded Execution Protocol

## Contents

- Principle
- Required safety envelope
- Effort question and budget derivation
- Deriving the internal envelope
- Budget accounting
- Budget inheritance
- Workstream cycle
- Stagnation brake
- Integration
- Runtime mapping


## Principle

**Quality determines `PASS`; resource limits determine `CAPPED`.**

A maximum is a safety ceiling. Quality alone defines done, and a single verified cycle can reach it. Status semantics live in `SKILL.md` section 8.

## Required safety envelope

The final **execution prompt** must contain finite values for:

- `MAX_WORKSTREAMS`: independent material workstreams the lead may open;
- `MAX_WORKSTREAM_CYCLES`: executor to verifier cycles per workstream;
- `MAX_EXECUTOR_INVOCATIONS_PER_WORKSTREAM`: includes retries hidden inside a cycle;
- `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM`: includes fresh critics, second opinions, and rechecks;
- `MAX_INTEGRATION_CYCLES`: integrate to final-verifier cycles;
- per-role turn limits, or one shared `MAX_AGENT_TURNS`, whenever the runtime enforces turns;
- `MAX_DELEGATION_DEPTH`: child-agent nesting depth;
- `MAX_CONCURRENT_AGENTS`: simultaneous workers and reviewers;
- one global fan-out ceiling, `MAX_TOTAL_CYCLES` together with `MAX_TOTAL_AGENT_SPAWNS`;
- at least one further global boundary when practical: wall clock, tokens, compute, or cost;
- `RESERVED_FOR_INTEGRATION`: the share of the global ceilings that workstreams may not spend;
- `AUTO_EXTEND = false`.

Only explicit human approval may enlarge an envelope or authorize a continuation run. Absent that approval, an exhausted envelope ends the run as `CAPPED`.

Keep this list internal: obtain one maximum-effort choice in plain language, then derive the envelope below.

## Effort question and budget derivation

Once the task, risk, and verification needs are clear, and only when the material has not already fixed a limit, ask exactly one plain-language question:

> For each important part of this work, what is the maximum number of improve-and-check rounds the agents may use? They can finish earlier when the evidence proves success.

Offer a task-informed recommendation from this table, without exposing internal limit names:

| Plain-language choice | Select when the mission shows | `N` |
|---|---|---:|
| Up to 3 rounds | one deliverable, cheap and deterministic checks, reversible output, no existing behavior to protect | 3 |
| Up to 5 rounds | more than one material workstream, existing behavior or regressions to protect, or verification that takes several steps | 5 |
| Up to 8 rounds | failure that is costly or hard to reverse (production, security, data migration, money, external users), or verification that is expensive, noisy, or partly subjective | 8 |
| You decide from the task | the user delegates effort sizing | take the highest row with a matching signal |

Accept any positive whole number the user gives, and resolve whether it is practical for the runtime before finalizing. When the user delegates, apply the signal column and record the selection and its trigger as `DERIVED`.

This is a safety budget, sized by risk. When the user wants higher quality, strengthen the bar and the evidence: a stronger bar improves the decision rule, while a larger `N` only buys more attempts.

Derive `W`, the maximum number of independent material workstreams, from the mission in the same pass: `1` for focused work, `2` for a multi-part task, `3` for a complex mission. If the mission needs more than the cap permits, phase it or obtain approval, and never leave `W` unbounded.

## Deriving the internal envelope

Compute every expression from `N` and `W`, then put only the resulting integers and booleans in the execution prompt. The formulas are for the forge, not text for the generated prompt. Label every derived value:

| Internal limit | Exact derivation | Purpose |
|---|---|---|
| `MAX_WORKSTREAMS` | `W` | Bounds the decomposition before any work begins. |
| `MAX_WORKSTREAM_CYCLES` | `N` | Limits executor, evidence, and fresh-verifier rounds per workstream. |
| `MAX_EXECUTOR_INVOCATIONS_PER_WORKSTREAM` | `N` | Prevents hidden executor retries. |
| `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM` | `N + ceil(N / 3)` | Allows a bounded second opinion or recheck without granting an extra executor revision. |
| `MAX_INTEGRATION_CYCLES` | `ceil(N / 2)` | Limits integrate to final-verifier rounds. |
| `MAX_EXECUTOR_TURNS_PER_INVOCATION` | `max(6, 2 * N)` | Bounds one executor invocation when the runtime supports role-specific turn limits. |
| `MAX_VERIFIER_TURNS_PER_INVOCATION` | `max(4, N)` | Bounds one verifier invocation when supported. |
| `MAX_ORCHESTRATOR_TURNS` | `max(10, 3 * N)` | Covers decomposition, budget tracking, integration, and terminal reporting. |
| `MAX_AGENT_TURNS` | `max(10, 3 * N)` | Use only when the runtime has one shared per-agent turn control. |
| `MAX_DELEGATION_DEPTH` | `1` | Keeps delegation to the lead's direct executors and verifiers; use `2` only with explicit task-specific justification. |
| `MAX_CONCURRENT_AGENTS` | `min(W, 3)` | Parallelism follows independent workstreams, not round count. A cycle is sequential inside one workstream, so `W = 1` means one worker at a time. |
| `MAX_TOTAL_CYCLES` | `N + ceil(N / 2)` when `W = 1`, otherwise `ceil(3 * W * N / 4) + ceil(N / 2)` | A shared pool deliberately smaller than the sum of the local maxima, so the lead must spend rounds where they matter instead of exhausting every workstream. |
| `MAX_TOTAL_AGENT_SPAWNS` | `2 * MAX_TOTAL_CYCLES + W * ceil(N / 3) + 1` | Two agents per cycle, the bounded rechecks, and the lead. |
| `MAX_WALL_CLOCK_MINUTES` | `max(30, 15 * N)` when a time limit is practical | Adds a global wall-clock boundary. |
| `RESERVED_FOR_INTEGRATION` | `MAX_INTEGRATION_CYCLES` cycles of `MAX_TOTAL_CYCLES`, plus the matching share of any wall-clock, token, or cost ceiling | Integration and final verification are the closing step, so they are the first to be squeezed out. Reserving them up front is what keeps a run from ending with no integrated verdict at all. |
| `MAX_MINUTES_PER_EXECUTOR_INVOCATION` and `MAX_MINUTES_PER_VERIFIER_INVOCATION` | A share of `MAX_WALL_CLOCK_MINUTES` sized so no single invocation can exhaust it, with the executor share larger than the verifier share | Replaces the turn ceilings above whenever the runtime enforces no turns. |
| `AUTO_EXTEND` | `false` | Requires explicit human approval for any continuation. |

For example, a two-workstream task sized at `N = 5` and `W = 2` yields `MAX_WORKSTREAM_CYCLES = 5`, `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM = 7`, `MAX_INTEGRATION_CYCLES = 3`, `MAX_CONCURRENT_AGENTS = 2`, `MAX_TOTAL_CYCLES = 11`, and `MAX_TOTAL_AGENT_SPAWNS = 27`. The pool of 11 is below the 13 the two workstreams could each claim, which is the point: the global ceiling has to bind before every local ceiling does.

Use token, compute, or monetary ceilings the runtime exposes and the material authorizes, at the limits and prices the vendor publishes. When wall-clock enforcement is unavailable, keep the deadline as a semantic rule the orchestrator must honor.

## Budget accounting

Count activity consistently, or the ceilings mean nothing:

- one cycle is one executor invocation plus its verification;
- a re-verification after `INCONCLUSIVE` spends verifier budget only, leaving the cycle count untouched, and stays under `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM`;
- a replan spends one cycle of the workstream it replans;
- reopening a workstream after integration spends that workstream's remaining cycles and the shared pool. With none remaining, the run ends `CAPPED`;
- integration cycles draw on `MAX_INTEGRATION_CYCLES` and on the shared pool;
- every agent invocation decrements `MAX_TOTAL_AGENT_SPAWNS`, including rechecks and second opinions;
- the reserve is not available to workstreams: the lead refuses a workstream spawn that would eat into `RESERVED_FOR_INTEGRATION`;
- the lead checks the remaining budget before each spawn and refuses the spawn when any applicable ceiling is exhausted.

There is no unlimited internal retry channel hidden inside a nominal single cycle. Revisions, self-fix attempts, reruns, fresh critics, adversarial second opinions, tool-runner iterations, replans, test-fix retries, integration retries, and nested agent work all consume budget.

## Budget inheritance

Every child and workstream inherits the strictest applicable remaining limit among:

1. its local cap;
2. the parent or orchestrator remaining allowance;
3. the global remaining allowance.

A child may not spawn another child when the resulting depth would exceed `MAX_DELEGATION_DEPTH`.

## Workstream cycle

One cycle is:

1. the executor changes or produces the artifact;
2. the executor records direct evidence;
3. a fresh verifier inspects the current artifact, the criteria, and the evidence;
4. the verifier returns status, blocking findings, largest gap, and the next acceptance check;
5. the next cycle starts from that verdict, gap, and acceptance check.

Stop immediately on `PASS`.

## Stagnation brake

When the dominant failure repeats for two consecutive failed cycles without measurable improvement:

- stop repeating the same strategy;
- replan, split the workstream, strengthen the evidence, or reconsider the bar or requirement;
- remember that replanning consumes budget;
- when progress cannot be re-established, return `ESCALATE` or `CAPPED` rather than burning the remaining budget mechanically.

## Integration

Local `PASS` is provisional. After local convergence:

- spend the reserve first, before any remaining shared pool;
- assemble the actual artifacts;
- verify cross-workstream interfaces and consistency;
- run global gates;
- use a fresh final verifier;
- repeat while budget remains, up to `MAX_INTEGRATION_CYCLES`;
- stop early on global `PASS`.

## Runtime mapping

Use real runtime controls when they exist, and keep the semantic caps in the generated prompt regardless.

Examples:

- the OpenAI Agents SDK exposes `max_turns` or `maxTurns`, where exhaustion is a termination condition and not a quality pass;
- Claude and Anthropic runtimes may expose turn, budget, depth, concurrency, or tool-iteration controls depending on product and version;
- for runtimes without a verified native turn cap, enforce the limits in the orchestrator or wrapper and through the process, time, and budget controls the environment does offer.

Name only controls you can verify in the target environment.

Where the runtime exposes no per-agent turn control, do not drop the per-invocation ceiling: restate it in a unit the orchestrator can observe, usually wall-clock minutes, and carry that number into the prompt. An invocation with no ceiling of its own lets a single agent consume the whole global budget, which is the failure the envelope exists to prevent.
