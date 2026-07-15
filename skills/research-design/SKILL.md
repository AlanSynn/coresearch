---
name: research-design
description: Complete research planning workflow for paper ideas, drafts, projects, or repos. Use when the user says research-design, wants to design a paper, clarify contribution, choose a venue, plan evidence, build a claim ledger, outline the paper, or make a venue-aware score plan. Produces an in-chat design contract by default and only writes files when requested.
---

# research-design — Paper Design

Turn a rough idea, draft, experiment set, or codebase into a reviewer-legible research plan.

## What & When

Use when: "design a paper", "clarify contribution", "choose a venue", "plan
evidence", "build a claim ledger", "outline the paper", "make a venue-aware
score plan". Field modes: AI/ML/CV, Robotics, Graphics, HCI/UIST/CHI, or
hybrid. Not for: final prose → `research-write`; verified literature search →
`research-survey`; implementation or experiment code → `research-engineer` /
`$ralplan`.

## Procedure

1. **Select field and venue mode** — AI/ML/CV, Robotics, Graphics, HCI/UIST/CHI, hybrid.
2. **Identify the field object** — apply the field-object test: what can the field define, measure, build, compare, or reuse differently? Object is one of formulation, method, system, dataset, benchmark, toolkit, taxonomy, evaluation protocol, pipeline, failure theory, or artifact package.
3. **Identify the contribution type** — method / system-artifact / empirical / theory-framework / dataset-benchmark / design knowledge.
4. **Draft the central claim** — one sentence, scoped to evidence, using claim architecture:
   - **AI/Robotics/technical Graphics:** "We enable X under constraint Y using mechanism Z, validated by evidence W."
   - **HCI/design computing:** "We enable audience A to explore/make/understand X through practice Y, revealing implication Z."
   - **Hybrid:** two linked claims — technical mechanism claim plus design/workflow claim.
5. **Build contribution bullets** — two to four concrete, parallel, non-overlapping.
6. **Seed the claim ledger** — per claim: type, evidence needed, current evidence, section, risk, status.
7. **Plan evidence** — experiments, studies, ablations, baselines, figures, proofs, demos, hardware trials, qualitative analyses that directly support each claim.
8. **Map related work** — streams, closest competitors, enabling, adjacent work, missing citation categories, novelty risks.
9. **Outline the paper** — section-level argumentative spine.
10. **Forecast score** — current likely score, target score, blockers, score-up conditions, score-down risks, reviewer variance.
11. **Define next actions** — prioritized by expected score impact.

## Output

Paper Design Contract (in chat by default; files only when requested):

- **1. Project Objective** — artifact produced or revised.
- **2. Venue Mode and Reviewer Model** — primary venue/mode; field mode [AI/Robotics/Graphics/HCI/Hybrid]; narrative spine [Ha technical systems / Oh design-computing / Hybrid dual-claim]; secondary venue; reviewer expectations; likely objections; venue-rule status [verified / unverified / needs official check].
- **3. Field Object and Contribution Thesis** — field object (define/measure/build/compare/reuse differently); contribution type [method / system-artifact / empirical / theory-framework / dataset-benchmark / design knowledge]; one-sentence central claim; 2-4 concrete non-overlapping contribution bullets.
- **4. Claim Ledger Seed** — Claim | Type | Evidence needed | Current evidence | Section | Risk | Status.
- **5. Evidence Plan** — Claim | Evidence to add or strengthen | Priority | Feasibility | Score impact.
- **6. Related Work Plan** — direct competitors; enabling; adjacent; missing citation categories; novelty risks.
- **7. Paper Structure** — section outline with each section's argumentative job.
- **8. Figure Plan** — Figure | Claim supported | Panels/assets | Caption thesis | Risk answered.
- **9. Score Plan** — scale [official if verified, else internal]; current estimate; target; main blockers; score-up conditions; score-down risks; reviewer variance [low/medium/high].
- **10. Next Actions** — prioritized by score impact.
- **11. Human Decisions Needed** — only decisions the user must make.

## Reject when

- central claim is not one sentence;
- field object is not explicit and reusable;
- bullets are not concrete or overlap;
- any claim has no evidence path and is not marked unsupported;
- evidence plan follows venue folklore rather than the claims;
- score blockers or score movement conditions are not explicit;
- any fabricated citation, baseline, result, or participant detail introduced.

## State & Handoff

State: design contract in chat by default; write files only when requested.
Inputs: target venue(s); abstract/notes/draft/figures/results/code/system;
evidence available + planned; constraints (deadline, page limit, anonymity,
available experiments). Ask at most one clarifying question if target venue or
central artifact is impossible to infer; otherwise state assumptions and
proceed. Next: executable implementation plan → `$ralplan` (OMX) or a native
executor / chat-only plan if OMX is absent; autonomous experiment steering →
`research-loop` / `$autoresearch` (OMX) after the contract is clear.

Re-entry: return to `coresearch` to re-route the next stage.
