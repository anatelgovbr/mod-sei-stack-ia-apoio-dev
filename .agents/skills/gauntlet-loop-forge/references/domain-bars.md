# Domain Quality-Bar Patterns

## Contents

- Universal bar construction
- Software / engineering
- Research / analysis
- Writing / editorial
- Visual / UX / product design
- Data / ML evaluation
- Documents / reports / decks
- Business / operations / workflows
- Prompt / agent behavior


Use these as patterns, not mandatory checklists. Select only dimensions that matter to the mission.

## Universal bar construction

Prefer a hybrid of:

1. source-of-truth acceptance criteria;
2. deterministic or directly observable gates;
3. representative real-world behavior;
4. non-functional quality thresholds;
5. an external exemplar/reference only where it adds information.

## Software / engineering

Activate the dedicated software references.

Typical bars include frozen tests, acceptance examples, runtime behavior, contract compatibility, performance/reliability/security thresholds, and reference implementations when genuinely comparable.

## Research / analysis

Strong evidence may include:

- explicit research question and coverage checklist;
- source authority/recency requirements;
- primary-source preference where possible;
- claim-to-source traceability;
- reproducible calculations;
- uncertainty and contradictory-evidence handling;
- a named high-quality report/paper methodology when useful.

## Writing / editorial

Strong evidence may include:

- audience and communication objective;
- factual/source checks;
- structure and coverage requirements;
- comprehension/clarity test;
- length/format constraints;
- one or more concrete published references for measurable qualities such as clarity, density, or organization.

The bar measures qualities like clarity, density, and organization. A living author's distinctive style stays out of it.

## Visual / UX / product design

Strong evidence may include:

- named real products/pages/design references;
- matched viewports/states/content density;
- reproducible screenshots/captures;
- interaction correctness;
- accessibility/usability checks;
- responsiveness/performance gates.

## Data / ML evaluation

Strong evidence may include:

- frozen dataset and split;
- task metric and target;
- simple baseline(s);
- leakage checks;
- robustness/slice analysis;
- repeated runs/seed controls where stochasticity matters;
- latency/cost/resource ceilings;
- deployment/monitoring constraints.

If implementation is part of the task, also activate software specialization.

## Documents / reports / decks

Strong evidence may include:

- completeness against a checklist/source of truth;
- factual/source validation;
- page/section-level legibility and consistency;
- format/brand/compliance requirements;
- whole-document integration review;
- a comparable real deliverable when subjective polish matters.

## Business / operations / workflows

Strong evidence may include:

- defined target state and process constraints;
- measurable KPI/SLAs;
- state-transition or reconciliation checks;
- exception/failure handling;
- compliance and human approvals;
- auditability and reversibility where relevant.

## Prompt / agent behavior

Strong evidence may include:

- frozen eval set;
- expected behaviors/gold outputs;
- automated graders and calibrated rubric;
- baseline prompt/model comparison;
- failure-mode coverage;
- cost/latency ceilings;
- reproducible run conditions.
