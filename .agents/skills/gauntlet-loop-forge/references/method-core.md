# Gauntlet Loop Method Core

Read this when fidelity to the original method is uncertain. The operative rules are the invariants in `SKILL.md` and the loop in section 7. This file records what the method protects and the one deliberate adaptation.

## What breaks the method

However the prompt is worded, these return judgment to the builder and void the method:

- the builder judging its own artifact, directly or through a critic that inherited its reasoning;
- a critic reading the builder's summary instead of the artifact;
- a bar the artifact cannot lose against;
- rounds that polish everywhere instead of attacking the largest remaining gap;
- a decomposition imposed on the lead, when splitting the work is itself part of the judgment.

## The bounded adaptation

The original method rejects an arbitrary round count as a **definition of done**. That is not an argument for infinite execution.

Two questions stay separate here:

- **Did quality pass?** Decided only by evidence against the bar.
- **May the system keep spending effort?** Decided by the finite safety envelope.

So: stop early on `PASS`, stop as `CAPPED` when a limit is exhausted first, never report a cap as quality success, and never self-extend.

## Source lineage

Primary method:

- Matt Shumer, "How to Run a Gauntlet Loop", Something Big Is Happening, 2026: https://somethingbig.ai/gauntlet-loop
- Official prompt generator: https://somethingbig.ai/gauntlet-loop/generator

Community implementations studied:

- RoboNuggets / Jay E: https://github.com/robonuggets/gauntlet-loop
- Nicholas Spisak: https://github.com/NicholasSpisak/gauntlet-loop

This Skill synthesizes the method rather than copying either community implementation.
