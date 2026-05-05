---
name: paper-design
description: Complete research planning workflow for paper ideas, drafts, projects, or repos. Use when the user says paper-design, wants to design a paper, clarify contribution, choose a venue, plan evidence, build a claim ledger, outline the paper, or make a venue-aware score plan. Produces an in-chat design contract by default and only writes files when requested.
---

# Paper Design

Turn a rough idea, draft, experiment set, or codebase into a reviewer-legible research plan. This is the concrete workflow behind `/paper-design`. Default output is in chat, not a file tree.

## Inputs

Use what the user provides:

- target venue or candidate venues;
- abstract, notes, draft, figures, results, code, or system description;
- evidence already available and evidence still planned;
- constraints such as deadline, page limit, anonymity, or available experiments.

Ask at most one clarifying question if the target venue or central artifact is impossible to infer. Otherwise state assumptions and proceed.

## Workflow

Use this skill in chat by default. If the user needs an executable implementation plan, hand off to `$ralplan`; if they need autonomous experiment steering, hand off to `research-loop` / `$autoresearch` after the design contract is clear.

1. **Select venue mode.** Graphics, AI/ML/CV, or HCI/UIST/CHI.
2. **Identify the actual contribution.** Distinguish artifact, method, study, dataset, benchmark, analysis, or theory.
3. **Draft the central claim.** One sentence, scoped to evidence.
4. **Build contribution bullets.** Two to four concrete, parallel, non-overlapping bullets.
5. **Seed a claim ledger.** For each claim: evidence, section, risk, status.
6. **Plan evidence.** Experiments, studies, ablations, baselines, figures, proofs, demos, or qualitative analyses that directly support claims.
7. **Map related work.** Streams, closest competitors, enabling work, adjacent work, missing citations, novelty risks.
8. **Outline the paper.** Section-level argumentative spine.
9. **Forecast score.** Current likely score, target score, blockers, score movement conditions.
10. **Define next actions.** Prioritized by expected score impact.

## Output schema

```markdown
# Paper Design Contract

## 1. Project Objective
[What artifact is being produced or revised.]

## 2. Venue Mode and Reviewer Model
- Primary venue/mode: [venue]
- Secondary venue: [optional]
- Reviewer expectations: [bullets]
- Likely objections: [bullets]
- Current venue-rule status: [verified / unverified / needs official check]

## 3. Contribution Thesis
[One-sentence central claim.]

### Contribution Bullets
1. [Concrete contribution]
2. [Concrete contribution]
3. [Optional]

## 4. Claim Ledger Seed
| Claim | Evidence needed | Current evidence | Section | Risk | Status |
|---|---|---|---|---|---|

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
- bullets are concrete and non-overlapping;
- every claim has an evidence path or is marked unsupported;
- evidence plan matches claims rather than venue folklore;
- score blockers and score movement conditions are explicit;
- no fabricated citations, baselines, results, or participant details were introduced.
