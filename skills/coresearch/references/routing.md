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

## Field and artifact companions

- Field/tone uncertainty → read `field-modes.md`, then route to `research-design` or `research-write`.
- Research importance / contribution object uncertainty → read `research-rules.md`, then route to `research-design`.
- `.pptx` mechanics → route to the Claude `pptx` companion after `research-slides` defines claims/narrative.
- `.docx`, generic `.pdf`, `.xlsx`, frontend, or web artifact mechanics → read `artifact-companions.md`; Coresearch owns claims, companion owns format mechanics.

## OMX lanes

- `$best-practice-research`: upstream docs/practice lookup before architecture choices.
- `$ralplan`: executable code/system plan with tradeoffs.
- `$team + $ultragoal`: parallel implementation with durable checkpoints.
- `$autoresearch`: validator-gated research execution only after mission + validator exist.
- `$ultraqa`: hostile QA after implementation when e2e risk matters.

Do not use `$autoresearch` for ordinary planning lookup. Feed its approved artifact back into `$ralplan` when architecture follows.
