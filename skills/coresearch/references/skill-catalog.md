# Coresearch Skill Catalog

## Owned by Coresearch harness

`coresearch`, `research-design`, `research-survey`, `research-loop`, `research-engineer`, `research-figures`, `research-pdfs`, `research-write`, `research-review`, `research-proofread`, `research-rebuttal`, `research-slides`, `pptx`, `research-verify`.

## No shim aliases

Coresearch uses canonical `coresearch`, `research-*`, and `pptx` names only. Old `paper-*`, `claim-check`, `pdf-crawl`, `rebuttal-plan`, and `research-guidelines` shims are intentionally not managed by this harness.

## Native agent roles

Skill names are not native `agent_type` names. When delegating, use installed OMX roles (`explore`, `researcher`, `executor`, `test-engineer`, `verifier`, `critic`, `code-reviewer`, `writer`, etc.) and pass the Coresearch stage/skill/field/evidence context in the handoff. `worker` is team-runtime-only, not a generic route.

## Companion routes, not owned by default

- `academic-ppt`: source-faithful academic `.pptx` generation from LaTeX/PDF/equations; optional route from `research-slides` when source fidelity matters more than general PowerPoint mechanics.
- `docx`, `pdf`, `xlsx`: Claude document skills; use only when those file formats are explicit input/output.
- Claude `pptx`: preferred external mechanics engine when exact Claude PowerPoint behavior is desired; Coresearch `pptx` prepares the academic brief and validates claims/QA.
- `web-artifacts-builder`, `frontend-design`, `frontend-skill`: web demo/artifact polish; route only when research output needs interactive/demo UI.
- `autoresearch`, `autoresearch-goal`: OMX validator-gated loops.
- `best-practice-research`: upstream docs/practice evidence.
- `caveman`: terse communication mode.
- `ponytail:*`: minimal-code plugin.
- `design`, `analyze`, `code-review`, `security-review`, `ultraqa`: external OMX review/diagnostic surfaces.

Do not bulk-copy proprietary companion text into this repo. Prefer external routing/delegation plus Coresearch-owned concise contracts.
