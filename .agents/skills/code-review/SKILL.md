---
name: code-review
description: Review committed changes since a fixed point (commit, branch, tag, or merge-base) against this repository's documented standards. Delegates the Standards review to sei-revisao-tecnica. Use when the user wants to review a committed branch, a PR, or asks to "review since X". The upstream Spec axis is disabled in the current version.
---

Standards review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?

The Standards axis runs in an independent sub-agent so it does not pollute the
coordinator's context. In this repository, it delegates the complete review to
`sei-revisao-tecnica`.

The upstream **Spec** axis is intentionally disabled in the current version. Do
not search for a spec, issue or requirement, and do not evaluate functional
adherence. If the request includes that intent, run Standards only and state
that Spec was not evaluated.

If a file named `spec.md` or another requirements document is itself part of the
Git diff, Standards may inspect its changed lines only as a changed repository
artifact. Do not load it as the functional source of truth, derive requirements
from it, or compare the implementation against it.

Do not remove such files from the Standards diff. Standards reviews every
changed file for applicable repository standards, including documentation
quality, secrets and unsafe instructions, while remaining neutral about whether
the implementation satisfies the document.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point: a commit SHA, branch name, tag,
`main`, `HEAD~5`, etc. If they did not specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so
the comparison is against the merge-base). Also note the list of commits via
`git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves
(`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty
diff should fail here, not inside the Standards sub-agent.

Never replace an invalid fixed point with the empty tree, its parent, `HEAD`, a
default branch, or any other fallback. Report the invalid reference and stop.

Operate read-only. Do not checkout, fetch, commit, push or mutate refs.

### 2. Identify the standards sources

Anything in the repo that documents how code should be written, such as
`AGENTS.md`, `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

For SEI, `sei-revisao-tecnica` owns the repository-specific standards, artifact
gates, security controls, coverage rules, second pass and technical verdict. Do
not reproduce those rules in this skill.

On top of whatever the repo documents, the Standards axis always carries the
**smell baseline** below, a fixed set of Fowler code smells (_Refactoring_,
ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it
  endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible
  Feature Envy"), never a hard violation, and, like any standard here, skip
  anything tooling already enforces.

Each smell reads *what it is* followed by *how to fix*; match it against the
diff:

- **Mysterious Name**: a function, variable, or type whose name does not reveal
  what it does or holds. Rename it; if no honest name comes, the design is murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or
  file in the change. Extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than
  its own. Move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together, a
  type wanting to be born. Bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain
  concept that deserves its own type. Give the concept its own small type.
- **Repeated Switches**: the same `switch` or `if` cascade on the same type
  recurs across the change. Replace with polymorphism, or one map both sites
  share.
- **Shotgun Surgery**: one logical change forces scattered edits across many
  files in the diff. Gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated
  reasons. Split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs
  that are not current. Delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller should not
  depend on. Hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. Cut it,
  call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most
  of what it inherits. Drop the inheritance, use composition.

### 3. Spawn the Standards sub-agent

The Standards sub-agent prompt includes:

- The full diff command and commit list.
- The list of standards-source files found in step 2, plus the smell baseline
  from step 2 pasted in full. The sub-agent has no other access to it.
- The instruction to load and execute `sei-revisao-tecnica` over the supplied
  diff, preserving its technical coverage, second pass and verdict.
- The brief: "Report, per file or hunk where relevant, every place the diff
  violates a documented standard with the source file and rule, plus any
  baseline smell with its name and quoted hunk. Distinguish hard violations from
  judgement calls. Repository standards override the baseline. Skip anything
  tooling enforces."

The sub-agent must actually load and follow `sei-revisao-tecnica`; naming it is
not enough. Do not substitute a generic quality review, omit SEI gates, or use a
legacy reviewer. The Standards result is invalid unless it contains the coverage,
dimensions, second pass and technical verdict required by
`sei-revisao-tecnica`.

### 4. Report

Present the Standards report verbatim or lightly cleaned under this heading:

```text
## Standards
<complete sei-revisao-tecnica report>
```

End with one line containing the total findings and the worst Standards issue,
if any. Preserve the technical verdict emitted by `sei-revisao-tecnica`.

Do not add a `Spec` section. If the user requested functional comparison, add
only this plain note after the Standards summary, with no heading:

`Spec was not evaluated because that axis is disabled in the current version.`

## Origin and Local Adaptation

Based on `mattpocock/skills`, `skills/engineering/code-review/SKILL.md`, commit
`6a34259e99bc5fed4f8fe5da61c273dad14edf67`, under the MIT license.

Local adaptation is limited to delegating Standards to `sei-revisao-tecnica`,
disabling the upstream Spec axis, and requiring read-only operation.
