# Research Engineering Architecture Playbook

Use this when research code must become production-grade, reproducible, or LLM-friendly. Do not force this onto a one-off scratch script.

## Architecture target

Prefer a small DDD-shaped core:

```text
src/<project>/
  domain/        # entities, value objects, pure rules, claim-level concepts
  application/   # use cases, experiment orchestration, services
  adapters/      # datasets, files, model APIs, devices, plotting, web, external formats
  infrastructure/# logging, config loading, persistence, job runners
  interfaces/    # CLI, notebooks, web UI, scripts
configs/         # explicit experiment configs
experiments/     # runnable experiment entrypoints and manifests
tests/           # domain/application tests + smoke checks
docs/            # hot/index/cold knowledge routing
```

Keep the domain pure when feasible. Keep IO, GPU/device specifics, datasets, APIs, hardware, and external file formats at adapters.

## Hot / index / cold docs

Use docs as an LLM-friendly routing layer:

- `docs/hot/` — current decisions, active experiment commands, claim ledger, latest results, known blockers.
- `docs/index/` — maps from claims → code → data → figures → paper sections; stable enough for agents to route context.
- `docs/cold/` — archived runs, old notes, superseded designs, long logs, prior failed attempts.

Minimum useful files:

```text
docs/hot/claim-ledger.md
docs/hot/runbook.md
docs/index/architecture.md
docs/index/data-contracts.md
docs/index/experiment-map.md
docs/cold/README.md
```

Do not dump everything into `docs/hot`; hot means the next agent probably needs it.

## AGENTS.md architecture block

When a research repo is being initialized or upgraded, add a compact architecture block to project `AGENTS.md` or a linked `docs/index/architecture.md`:

```markdown
## Architecture Notes
- Domain concepts: [entities/value objects/claim concepts]
- Main use cases: [train/evaluate/analyze/render/export]
- Boundaries: datasets/models/devices/files/APIs live in adapters.
- Repro command: [single smoke command]
- Docs routing: hot = current, index = maps, cold = archive.
- Claim link: every result-producing command states which paper claim/figure it supports.
```

## Production-grade research defaults

- One command can reproduce each table/figure or explain why not.
- Config is explicit and versioned; seeds are passed, not hidden.
- Outputs include provenance: command, commit, config, seed, data/model versions, hardware if relevant.
- Tests cover domain logic and one smoke path through each result-producing pipeline.
- Logging is structured enough to compare runs.
- Failure cases are first-class outputs, not deleted evidence.
- Dependencies are justified; use stdlib/repo helpers first.

## When to stay simpler

Use a flat script/notebook only when all are true:

- exploratory throwaway;
- no paper claim depends on the output yet;
- no user/reviewer/reproducer will run it;
- no hidden state or external side effect matters.

Once a script supports a figure, table, benchmark, release artifact, or rebuttal experiment, promote it to a reproducible pipeline.
