---
name: rebuttal-plan
description: Rebuttal and response-planning workflow for research paper reviews. Use when the user provides reviewer comments, scores, meta-reviews, or discussion-phase feedback and wants a response strategy, score movement forecast, experiments or clarifications to add, or concise rebuttal text for venues such as NeurIPS, ICLR, CVPR, SIGGRAPH, CHI, UIST, or AISTATS.
---

# Rebuttal Plan

Turn reviews into a score-moving response strategy. Prioritize factual corrections, misunderstandings, and feasible evidence additions. Do not promise new experiments or claims unless the user confirms they can be done.

## Inputs

Use reviewer text, scores, confidence, paper context, constraints, response length, and allowed updates. If scores are missing, infer likely stance with low-to-moderate confidence.

## Workflow

1. **Parse each review.** Extract likely score, confidence, positive anchors, and score-blocking concerns.
2. **Classify concerns.** Factual misunderstanding, missing explanation, missing experiment, novelty overlap, weak evidence, writing issue, fundamental flaw.
3. **Estimate leverage.** High, medium, low, or very low score movement potential.
4. **Build global strategy.** Lead with consensus corrections and score-moving clarifications. Do not fight every point.
5. **Plan additions.** Feasible experiments, tables, figures, citations, or text changes if allowed.
6. **Draft response bullets.** Concise, respectful, evidence-based.
7. **Forecast movement.** Post-rebuttal scores and decision path.

## Leverage guide

| Concern type | Typical leverage |
|---|---|
| Factual misunderstanding | High |
| Explanation already present but missed | Medium to high |
| Missing quick experiment or analysis | Medium |
| Missing weeks-long experiment | Low |
| Novelty concern with strong prior overlap | Low unless distinction is crisp |
| Weak venue fit | Low to medium |
| Writing clarity | Medium to high |
| Fundamental technical flaw | Very low |

## Output schema

```markdown
# Rebuttal Plan — [Venue]

## Global Strategy
[3–5 bullets in priority order.]

## Review-by-Review Diagnosis
### Reviewer [ID]
- Likely score / stance:
- Confidence:
- Positive anchors:
- Score-moving concerns:
- Legitimate weaknesses:
- Possible misunderstandings:
- Rebuttal leverage: [high / medium / low / very low]
- Best response strategy:

## Cross-Reviewer Themes
| Theme | Reviewers | Severity | Response priority | Evidence needed |
|---|---|---|---|---|

## Prioritized Response Bullets
1. [Response point with evidence]
2. [Response point with evidence]
3. [Response point with evidence]

## Additions if Allowed
| Addition | Addresses | Feasibility | Expected score impact |
|---|---|---|---|

## Risks and What Not to Say
- [Risk]
- [Overclaim or defensive phrasing to avoid]

## Predicted Score Movement
| Reviewer | Before | After forecast | Reason |
|---|---|---|---|

## Draft Rebuttal Skeleton
[Concise paragraph/bullet structure, not padded prose.]
```

## Guardrails

- Do not attack reviewers.
- Do not overpromise experiments.
- Do not introduce unsupported claims.
- If a weakness is legitimate, acknowledge it and scope the claim.
