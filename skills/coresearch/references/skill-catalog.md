# Coresearch Skill Catalog

## Owned by Coresearch harness

`coresearch`, `research-design`, `research-survey`, `research-loop`, `research-gap`, `research-dialectic`, `research-causal`, `research-engineer`, `research-figures`, `research-qualitative`, `research-write`, `research-review`, `research-proofread`, `research-rebuttal`, `research-slides`, `research-verify`, `research-audit`, `research-adversary`.

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

Coresearch uses canonical `coresearch` and `research-*` names only. Old `paper-*`, `claim-check`, `pdf-crawl`, `rebuttal-plan`, and `research-guidelines` shims are intentionally not managed by this harness. PowerPoint mechanics route to the external Claude `pptx` companion, not an owned skill.

## Native agent roles

Skill names are not native `agent_type` names. When delegating, use installed OMX roles (`explore`, `researcher`, `executor`, `test-engineer`, `verifier`, `critic`, `code-reviewer`, `writer`, etc.) and pass the Coresearch stage/skill/field/evidence context in the handoff. `worker` is team-runtime-only, not a generic route.

## Companion routes, not owned by default

- `academic-ppt`: source-faithful academic `.pptx` generation from LaTeX/PDF/equations; optional route from `research-slides` when source fidelity matters more than general PowerPoint mechanics.
- `docx`, `pdf`, `xlsx`: Claude document skills; use only when those file formats are explicit input/output.
- Claude `pptx`: external PowerPoint mechanics engine; `research-slides` prepares the claim-faithful brief and the companion owns build/render/QA.
- `web-artifacts-builder`, `frontend-design`, `frontend-skill`: web demo/artifact polish; route only when research output needs interactive/demo UI.
- `autoresearch`, `autoresearch-goal`: OMX validator-gated loops.
- `best-practice-research`: upstream docs/practice evidence.
- `caveman`: terse communication mode.
- `ponytail:*`: minimal-code plugin.
- `design`, `analyze`, `code-review`, `security-review`, `ultraqa`: external OMX review/diagnostic surfaces.

Do not bulk-copy proprietary companion text into this repo. Prefer external routing/delegation plus Coresearch-owned concise contracts.
