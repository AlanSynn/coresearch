---
name: research-engineer
description: Research engineering workflow for reproducible experiments, analysis code, datasets, benchmarks, ML or graphics pipelines, HCI study analysis, and artifact release. Use when implementing, refactoring, testing, debugging, or documenting code that supports paper claims or research results.
---

# Research Engineer

Build and modify research code so paper claims remain reproducible and inspectable. Keep changes minimal and verifiable.

## Principles

- **Claim-driven:** know which paper claim the code supports.
- **Explicit configuration:** no hidden defaults, magic strings, or silent side effects.
- **Boundary isolation:** keep IO, datasets, models, devices, APIs, and external formats at adapters.
- **Determinism:** pass seeds or generators explicitly where feasible.
- **Logging:** record config, seed, model/data versions, hardware, command, and commit when available.
- **Metrics:** define units, aggregation, confidence intervals or seed variation when relevant.
- **Minimal architecture:** do not over-engineer exploratory scripts; do not under-engineer result-producing pipelines.

## Workflow

Use `omx explore` first for simple read-only repo lookups when OMX exposes it. Use `$team` only for approved parallel work with disjoint write scopes; otherwise keep implementation in the current session and verify locally.

1. Identify the claim, metric, dataset, and expected artifact.
2. Inspect existing code and tests before editing.
3. Propose the smallest design that satisfies the research need.
4. Implement surgically.
5. Add or update tests, smoke checks, or reproducibility scripts.
6. Run validation commands.
7. Report changed files, commands, results, and remaining limitations.

## Architecture defaults

- Use Strategy plus Registry only when multiple methods are real requirements.
- Use adapters for third-party APIs and external formats.
- Use immutable data objects for domain concepts where practical.
- Prefer typed interfaces and fail-fast config parsing.
- Avoid `Any` or untyped blobs unless external data requires it, and contain them at boundaries.
- Vectorize tensor operations unless a loop is clearer and performance is irrelevant.

## Output schema

```markdown
## Decision
[Pattern and rationale in 1–2 lines.]

## Claim Supported
[Paper claim, experiment, figure, or artifact this code supports.]

## Interface
[Types, commands, or file contracts.]

## Implementation
[Summary of changes or code if not editing files.]

## Checks
| Command | Result | Notes |
|---|---|---|

## Reproducibility Notes
- Config:
- Seed:
- Data/model versions:
- Hardware/compute if relevant:
- Output artifacts:

## Limitations
[What the code or experiment still does not establish.]
```

## Stop conditions

Stop when the requested artifact is implemented, validation has run or a blocker is explicit, and the user can reproduce the result from the reported command. Ask before destructive actions, public releases, data deletion, or repository history changes.
