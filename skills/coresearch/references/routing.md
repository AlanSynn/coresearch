# Coresearch Routing

## Skill selection

Pick one primary skill.

- `research-design`: contribution, claim ledger, evidence plan, venue strategy.
- `research-survey`: verified papers, related-work map, novelty risk.
- `research-figures`: figure/table/caption architecture.
- `research-write`: rewrite supplied manuscript text without inventing claims.
- `research-review`: simulated venue review, score, blockers.
- `research-proofread`: final grammar/LaTeX/notation pass.
- `research-verify`: citation, number, source-faithfulness audit.
- `research-rebuttal`: reviewer response strategy.
- `research-slides`: talk/deck outline and slide text.
- `research-engineer`: research code, experiments, datasets, benchmarks, artifact release.
- `research-loop`: hypotheses, validators, sandbox, `$autoresearch` mission design.
- `research-survey` owns open-access PDF batch download via its in-skill crawler.
- Analytical skills (`research-gap`, `research-dialectic`, `research-causal`, `research-qualitative`, `research-audit`, `research-adversary`) → see [reasoning-skills.md](reasoning-skills.md).

## Field modes

- Field/tone uncertainty → read `field-modes.md`, then route to `research-design` or `research-write`.
- Research importance / contribution object uncertainty → read `research-rules.md`, then route to `research-design`.

File-format output (`.docx`/`.pdf`/`.pptx`/`.xlsx`/web) is owned by the user via external tools; Coresearch owns research content and claim integrity, not format mechanics.

## OMX lanes

Optional acceleration when an OMX install is present — owned skills complete standalone without them. Invoke a lane only when its lifecycle matters.

- `$best-practice-research`: upstream docs/practice lookup before architecture choices.
- `$ralplan`: executable code/system plan with tradeoffs.
- `$team + $ultragoal`: parallel implementation with durable checkpoints.
- `$autoresearch`: validator-gated research execution only after mission + validator exist.
- `$deep-interview`: clarify a vague research goal into a testable spec before design/loop work.
- `$ultraqa`: hostile QA after implementation when e2e risk matters.

Do not use `$autoresearch` for ordinary planning lookup. Feed its approved artifact back into `$ralplan` when architecture follows.

On terminal, every OMX lane re-enters `coresearch` to route the next research stage; lanes are executors, not routers (see omx-pony-caveman.md §Re-entry to coresearch).
