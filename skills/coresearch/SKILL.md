---
name: coresearch
description: Central Coresearch router for Alan's academic research, paper, literature, figure, slide, rebuttal, claim verification, research-engineering, and autonomous research-loop work. Use when a request is broad, says Coresearch, starts or manages a research project, asks which paper/research skill to use, mentions research stages, or needs OMX/Ponytail/Caveman-aware routing across research skills.
---

# Coresearch

Use this as the first-stop router for research work. Keep it small: classify stage, load one matching role skill, then stop routing.

## Good for

- Broad research requests where the right role skill is unclear.
- Starting or re-scoping AI, Graphics, Robotics, HCI, or hybrid research projects.
- Choosing between paper design, writing, review, survey, figures, engineering, rebuttal, verification, slides, and autonomous-loop work.
- Routing file-artifact work to companion skills without making Coresearch own every document format.

## Must do

- Pick one primary research stage and one primary skill.
- Select a field mode when design, writing, review, figures, or engineering quality depends on AI / Robotics / Graphics / HCI norms.
- Keep `coresearch` as a central triage unit: route, load only needed references, then hand off.
- Preserve evidence discipline: separate fact, inference, recommendation, and unknown.

## Not for

- Low-level `.docx`, `.pdf`, `.pptx`, `.xlsx`, or web-app mechanics when a companion skill is the right owner.
- Replacing OMX runtime skills such as `$autopilot`, `$team`, `$ultragoal`, `$ultraqa`, or `$autoresearch`.
- Bulk-loading every skill or creating `.agents/` state forests.

## Quick workflow

1. Identify research stage: intake, idea, survey, design, prototype, evidence, figures, manuscript, review, rebuttal, release.
2. Pick the smallest role skill from the catalog.
3. Pick field mode: AI / Robotics / Graphics / HCI / hybrid.
4. Load only the needed reference below.
5. Use OMX workflows only when their lifecycle matters.
6. Keep facts, inference, and recommendations separate.

## References

- Read [stage-map.md](references/stage-map.md) when starting/reframing a project.
- Read [routing.md](references/routing.md) when choosing a skill or OMX lane.
- Read [field-modes.md](references/field-modes.md) when venue tone, narrative, evidence, or architecture depends on AI/Robotics/Graphics/HCI norms.
- Read [research-rules.md](references/research-rules.md) when screening importance, contribution type, field object, or claim-evidence fit.
- Read [reasoning-skills.md](references/reasoning-skills.md) when routing among the analytical skills (research-gap, research-dialectic, research-causal, research-qualitative, research-audit, research-adversary) or sequencing a multi-skill pipeline.
- Read [research-contract.md](references/research-contract.md) at run start to capture the orchestrator input contract (topic, intended contribution, independent-group floor, output path).
- Read [state-ledger.md](references/state-ledger.md) when orchestrating a multi-skill run or maintaining cross-skill state (it is the canonical state; OMX `.omx/specs` and `$ultragoal` only mirror it).
- Read [artifact-companions.md](references/artifact-companions.md) when `.docx`, `.pdf`, `.pptx`, `.xlsx`, frontend, or web artifact work appears.
- Read [research-integrity.md](references/research-integrity.md) for claims, citations, evidence, or confidential material.
- Read [omx-pony-caveman.md](references/omx-pony-caveman.md) when `$autoresearch`, `$ponytail`, `$caveman`, `$team`, `$ultragoal`, or native subagents affect execution.
- Read [skill-catalog.md](references/skill-catalog.md) when auditing overlaps or installed companion skills.

## Default routes

- Paper idea/contribution/evidence plan, or venue choice/strategy (which venue fits this work) → `research-design`.
- Figures/tables/captions → `research-figures`.
- Related work/literature map → `research-survey`.
- Source/citation/fact check → `research-verify`.
- Section rewrite → `research-write`.
- Venue review/score forecast → `research-review`.
- Rebuttal/discussion response → `research-rebuttal`.
- Final line edit → `research-proofread`.
- Talks/slides plan → `research-slides`; finished `.pptx` build/render/QA → Claude `pptx` companion; source-faithful LaTeX/PDF/equation-heavy decks → `academic-ppt`.
- Code/experiments/artifact release → `research-engineer`.
- Hypotheses/validators/autonomous loop design → `research-loop`; execute with `$autoresearch` only after validator mode exists.
- Experiment scope split (when two apply): which evidence supports each claim (plan) → `research-design`; hypotheses/validators/stop-conditions → `research-loop`; implement the experiment code → `research-engineer`.
- Literature gap / next paper / "is this novel" / where are contradictions → `research-gap`.
- Why papers disagree + a reconciling mechanism → `research-dialectic`.
- Is this paper's methodology sound (claim vs evidence) → `research-audit`.
- Bias in the evidence-gathering chain of a conclusion → `research-adversary`.
- Competing causal explanations / identification → `research-causal`.
- Explain a concept / decompose a mechanism → `research-write` (concept-decomposition mode).
- Qualitative coding → themes (interviews, open responses) → `research-qualitative`.
- Workflow stall diagnosis (stalled, repeating, weak synthesis) → read [reasoning-skills.md](references/reasoning-skills.md) §Stall diagnosis; routes back into the skills above.
- DOCX/PDF/PPTX/XLSX/frontend/web mechanics → keep research claim owner in Coresearch, then route to companion skills from [artifact-companions.md](references/artifact-companions.md) when installed.
- If two routes match: fact-check/number/citation → `research-verify` over `research-audit`; 'review' = venue score → `research-review`, methodology soundness → `research-audit`; experiment PLAN → `research-design`, hypotheses/validators → `research-loop`, implement code → `research-engineer`.

## Guardrails

- Do not create `.agents/` state forests.
- Do not bulk-load every research skill.
- Do not invent citations, venues, results, participants, metrics, or code behavior.
- Do not fork OMX runtime skills into Coresearch unless the user explicitly asks for adoption.
