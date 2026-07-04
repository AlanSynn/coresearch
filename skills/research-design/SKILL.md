---
name: research-design
description: Complete research planning workflow for paper ideas, drafts, projects, or repos. Use when the user says research-design, wants to design a paper, clarify contribution, choose a venue, plan evidence, build a claim ledger, outline the paper, or make a venue-aware score plan. Produces an in-chat design contract by default and only writes files when requested.
---

# Research Design

Turn a rough idea, draft, experiment set, or codebase into a reviewer-legible research plan. This is the concrete workflow behind `/research-design`. Default output is in chat, not a file tree.

## Good for

- Choosing the contribution thesis, field object, and venue/reviewer model.
- Turning messy notes, demos, results, or repo state into a claim ledger and evidence plan.
- Deciding whether the work is AI, Robotics, Graphics, HCI, or hybrid and which narrative spine fits.
- Planning figures, related work, and score movement before prose or implementation.

## Must do

- Build a claim ledger: claim type, evidence needed, current evidence, section, risk, status.
- Apply the field-object test: what can the field define, measure, build, compare, or reuse differently?
- Match every major claim to evidence; mark unsupported claims instead of polishing them.
- State score blockers and score-up conditions.

## Not for

- Final prose polishing; use `research-write`.
- Verified literature search; use `research-survey`.
- Implementation details or experiment code; use `research-engineer` or `$ralplan`.

## Inputs

Use what the user provides:

- target venue or candidate venues;
- abstract, notes, draft, figures, results, code, or system description;
- evidence already available and evidence still planned;
- constraints such as deadline, page limit, anonymity, or available experiments.

Ask at most one clarifying question if the target venue or central artifact is impossible to infer. Otherwise state assumptions and proceed.

## Workflow

Use this skill in chat by default. If the user needs an executable implementation plan, hand off to `$ralplan`; if they need autonomous experiment steering, hand off to `research-loop` / `$autoresearch` after the design contract is clear.

1. **Select field and venue mode.** AI/ML/CV, Robotics, Graphics, HCI/UIST/CHI, or hybrid.
2. **Identify the field object.** Formulation, method, system, dataset, benchmark, toolkit, taxonomy, evaluation protocol, pipeline, failure theory, or artifact package.
3. **Identify the actual contribution.** Distinguish method, system/artifact, empirical, theory/framework, dataset/benchmark, or design knowledge.
4. **Draft the central claim.** One sentence, scoped to evidence.
5. **Build contribution bullets.** Two to four concrete, parallel, non-overlapping bullets.
6. **Seed a claim ledger.** For each claim: type, evidence, section, risk, status.
7. **Plan evidence.** Experiments, studies, ablations, baselines, figures, proofs, demos, hardware trials, or qualitative analyses that directly support claims.
8. **Map related work.** Streams, closest competitors, enabling work, adjacent work, missing citations, novelty risks.
9. **Outline the paper.** Section-level argumentative spine.
10. **Forecast score.** Current likely score, target score, blockers, score movement conditions.
11. **Define next actions.** Prioritized by expected score impact.

## Claim architecture

- **AI/Robotics/technical Graphics:** “We enable X under constraint Y using mechanism Z, validated by evidence W.”
- **HCI/design computing:** “We enable audience A to explore/make/understand X through practice Y, revealing implication Z.”
- **Hybrid:** state two linked claims: technical mechanism claim plus design/workflow claim.

## Output schema

```markdown
# Paper Design Contract

## 1. Project Objective
[What artifact is being produced or revised.]

## 2. Venue Mode and Reviewer Model
- Primary venue/mode: [venue]
- Field mode: [AI / Robotics / Graphics / HCI / Hybrid]
- Narrative spine: [Ha technical systems / Oh design-computing / Hybrid dual-claim]
- Secondary venue: [optional]
- Reviewer expectations: [bullets]
- Likely objections: [bullets]
- Current venue-rule status: [verified / unverified / needs official check]

## 3. Field Object and Contribution Thesis
- Field object: [what the field can define/measure/build/compare/reuse differently]
- Primary contribution type: [method / system-artifact / empirical / theory-framework / dataset-benchmark / design knowledge]

[One-sentence central claim.]

### Contribution Bullets
1. [Concrete contribution]
2. [Concrete contribution]
3. [Optional]

## 4. Claim Ledger Seed
| Claim | Type | Evidence needed | Current evidence | Section | Risk | Status |
|---|---|---|---|---|---|---|

## 5. Evidence Plan
| Claim | Evidence to add or strengthen | Priority | Feasibility | Score impact |
|---|---|---:|---|---|

## 6. Related Work Plan
- Direct competitors:
- Enabling work:
- Adjacent work:
- Missing citation categories:
- Novelty risks:

## 7. Paper Structure
[Section outline with each section's argumentative job.]

## 8. Figure Plan
| Figure | Claim supported | Panels/assets | Caption thesis | Risk answered |
|---|---|---|---|---|

## 9. Score Plan
- Scale used: [official if verified, otherwise internal]
- Current estimated score: [score]
- Target score: [score]
- Main blockers: [bullets]
- Score-up conditions: [bullets]
- Score-down risks: [bullets]
- Reviewer variance: [low / medium / high]

## 10. Next Actions
1. [High-impact action]
2. [High-impact action]
3. [Medium-impact action]

## 11. Human Decisions Needed
[Only decisions the user must make.]
```

## Validation checklist

Before finalizing, verify:

- central claim is one sentence;
- field object is explicit and reusable;
- bullets are concrete and non-overlapping;
- every claim has an evidence path or is marked unsupported;
- evidence plan matches claims rather than venue folklore;
- score blockers and score movement conditions are explicit;
- no fabricated citations, baselines, results, or participant details were introduced.
