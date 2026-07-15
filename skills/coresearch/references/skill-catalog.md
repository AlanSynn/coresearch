# Coresearch Skill Catalog

## Owned by Coresearch harness

`coresearch`, `research-design`, `research-survey`, `research-loop`, `research-gap`, `research-dialectic`, `research-causal`, `research-engineer`, `research-figures`, `research-qualitative`, `research-write`, `research-review`, `research-proofread`, `research-rebuttal`, `research-verify`, `research-audit`, `research-adversary`.

## Shared evidence infrastructure (one file per skill)

The analytical/audit skills run over ONE shared evidence model so outputs are
traceable source → claim → conclusion. Each skill loads a single per-skill ref:

- `evidence-grounding.md` — evidence object + claim object (one definition),
  `claim_type` enum, 3-dim confidence + rating rules, source priority + evidence
  levels, the 10 quality gates + gate↔skill map. **The per-skill load.**
- `research-contract.md` — orchestrator input contract + contribution↔evidence
  table + harness rules + integrity floor. Loaded once at run start, not per skill.
- `state-ledger.md` — orchestrator state schema + read/update protocol. Loaded
  only by the router.
- `reasoning-skills.md` — disambiguation table + cross-skill pipelines. Router-only.

Per-invocation load: analytical/audit skills = skill + `evidence-grounding.md`; a multi-skill run also loads `state-ledger.md`; discovery/manuscript skills = skill only.

## No shim aliases

Coresearch uses canonical `coresearch` and `research-*` names only. Old `paper-*`, `claim-check`, `pdf-crawl`, `rebuttal-plan`, and `research-guidelines` shims are intentionally not managed by this harness. File-format output (`.pptx`/`.docx`/`.xlsx`/web) is produced by the user with external tools; no format-mechanics skill is owned.

## Native agent roles

Skill names are not native `agent_type` names. When delegating, use installed OMX roles (`explore`, `researcher`, `executor`, `test-engineer`, `verifier`, `critic`, `code-reviewer`, `writer`, etc.) and pass the Coresearch stage/skill/field/evidence context in the handoff. `worker` is team-runtime-only, not a generic route.

## Optional OMX acceleration (when installed)

Coresearch skills complete standalone. These OMX lanes are optional acceleration the user can invoke when an OMX install is present; the bundle never depends on them.

- `$autoresearch` / `$deep-interview --autoresearch`: validator-gated autonomous loop execution after `research-loop` designs the mission.
- `$ralplan`: executable code/system plan with tradeoffs.
- `$team` / `$ultragoal`: parallel implementation with durable checkpoints. (`$swarm` is deprecated upstream; prefer `$team`.)
- `$ralph`: persistent single-owner completion for an approved loop.
- `$best-practice-research`: upstream docs/practice lookup.
- `$ultraqa`: hostile QA after implementation.
- `$autopilot`: OMX runtime skill Coresearch does not fork.

Caveman/Ponytail behavior is inlined in [omx-pony-caveman.md](omx-pony-caveman.md); no external preference skill is required.

File-format output (`.docx`/`.pdf`/`.pptx`/`.xlsx`/web) is owned by the user via external tools; Coresearch owns research content and claim integrity, not format mechanics. Do not bulk-copy proprietary external-skill text into this repo.
