---
name: research-engineer
description: Research engineering workflow for reproducible experiments, analysis code, datasets, benchmarks, ML or graphics pipelines, HCI study analysis, and artifact release. Use when implementing, refactoring, testing, debugging, or documenting code that supports paper claims or research results.
---

# research-engineer — Research Engineer

Build and modify research code so paper claims stay reproducible and
inspectable. Keep changes minimal and verifiable.

## What & When

Reproducible experiments, analysis code, datasets, benchmarks, simulations,
ML/graphics/robotics pipelines, HCI study analysis, artifact release; turning
prototypes into architecture-friendly, LLM-friendly, production-grade research
repos; writing or updating `AGENTS.md`/docs so future agents can route code,
claims, data, and figures. Use when implementing, refactoring, testing,
debugging, or documenting claim-supporting code. Not for: paper argument
design → `research-design`; prose rewriting → `research-write`; speculative
architecture for scratch code that supports no claim yet.

## Procedure

Tie every change to the claim it supports; reuse patterns before adding
abstractions. Use a native `explore` subagent (or `omx explore` fallback) for
read-only lookups; `$team` only for approved parallel work with disjoint write
scopes.

- **A. Claim → code** — identify which claim, figure, table, benchmark, or
  artifact the code supports; know the metric, dataset, and expected artifact.
- **B. Inspect first** — read existing code and tests before editing.
- **C. Smallest design** — satisfy the research need with the smallest viable
  design; over-engineer no exploratory script, under-engineer no
  result-producing pipeline.
- **D. Implement surgically** — keep domain logic separate from
  IO/model/device/API/file-format adapters when code will persist.
- **E. Architecture** — Strategy + Registry only when multiple methods are real
  requirements; adapters for third-party APIs/formats; DDD-shaped core
  (`domain/`, `application/`, `adapters/`, `infrastructure/`, `interfaces/`)
  when code is meant to last; immutable data objects for domain concepts; typed
  interfaces and fail-fast config; contain `Any`/untyped blobs at boundaries;
  vectorize tensor ops unless a loop is clearer. Route docs by temperature:
  `docs/hot/` active claim/run state, `docs/index/` stable maps, `docs/cold/`
  archive. Read references/architecture-playbook.md when DDD boundaries,
  hot/index/cold docs, or `AGENTS.md` notes matter.
- **F. Explicit configuration & determinism** — no hidden defaults, magic
  strings, or silent side effects; pass seeds or generators explicitly where
  feasible; define metric units, aggregation, CIs / seed variation when relevant.
- **G. Checks** — add the smallest runnable check that proves changed behavior
  or reproducibility: tests, smoke checks, or repro scripts.
- **H. Validate & report** — run validation commands; report changed files,
  commands, results, and remaining limitations.

## Output

- Decision — pattern and rationale in 1–2 lines.
- Claim Supported — paper claim, experiment, figure, or artifact this code supports.
- Interface — types, commands, or file contracts.
- Implementation — summary of changes, or code if not editing files.
- Checks — `| Command | Result | Notes |` table.
- Reproducibility Notes — Config; Seed; Data/model versions; Hardware/compute
  if relevant; Output artifacts; Docs / `AGENTS.md` updates.
- Limitations — what the code or experiment still does not establish.

## Reject when

- the artifact is not implemented, validation has not run, and no blocker is
  stated — do not claim complete;
- the user cannot reproduce the result from the reported command;
- a destructive action, public release, data deletion, or repository history
  change is pending — ask first.

## State & Handoff

State: changed code plus the Output report (commands, config, seed, data/model
versions, hardware, artifacts); update `AGENTS.md`/docs so future agents route
code → claim → data → figure. Artifacts: the code change and the
reproducibility report. Next: `research-design` (paper argument) /
`research-write` (prose). Stop when the artifact is implemented, validation has
run or a blocker is explicit, and the user can reproduce the result from the
reported command.
