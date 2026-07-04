---
name: research-review
description: Venue-calibrated simulated review and score forecast for research papers. Use when the user asks to review, critique, score, triage, forecast acceptance, identify acceptance risks, simulate reviewers, or assess submission readiness for SIGGRAPH, CVPR, NeurIPS, ICLR, AISTATS, CHI, UIST, Eurographics, or related venues.
---

# Research Review

Act as a strict but fair author-side reviewer. Provide explicit scores. Do not use this skill for confidential official peer review unless venue policy permits the intended use. In OMX execution, this is a verification surface: it may block completion when score-moving evidence gaps remain.

## Good for

- Simulated reviews, acceptance-risk triage, score forecasts, reviewer-modeling, and submission readiness.
- Venue-calibrated critique for AI, Robotics, Graphics, HCI, and hybrid papers.
- Finding score-moving evidence gaps and rewrite priorities.

## Must do

- State score/recommendation, confidence, variance, blockers, and movement conditions.
- Judge claim-evidence alignment, not just writing quality.
- Use official current forms only if verified; otherwise label scales `INTERNAL`.
- Flag confidentiality/policy limits before using official reviews.

## Not for

- Final grammar polish; use `research-proofread`.
- Writing the replacement prose; use `research-write`.
- Verifying citations/source faithfulness line-by-line; use `research-verify`.

## Inputs

Use manuscript text, figures, captions, supplement, code, results, or author notes. If key inputs are missing, score with lower confidence and state what could not be checked.

## Venue scales

Use official scales if the current venue form has been verified. Otherwise label scales as internal.

- **SIGGRAPH-style:** Strong Accept, Accept, Borderline Accept, Borderline Reject, Reject, Strong Reject. Add suggested track: Journal, Conference, or Reject.
- **Eurographics/CGF internal 1–6:** 6 strong accept, 5 accept, 4 weak accept/revision likely, 3 weak reject/major revision, 2 reject, 1 strong reject.
- **CVPR internal 1–5:** 5 strong accept, 4 accept, 3 borderline, 2 reject, 1 strong reject.
- **Robotics internal 1–5:** 5 strong accept, 4 accept, 3 borderline, 2 reject, 1 strong reject; emphasize embodied validation, system reliability, safety/reset details, and deployment limits.
- **NeurIPS-style 1–6:** 6 strong accept, 5 accept, 4 borderline accept, 3 borderline reject, 2 reject, 1 strong reject. Also rate quality, clarity, significance, originality 1–4 when useful.
- **ICLR internal 1–5:** 5 clear accept, 4 lean accept, 3 borderline, 2 lean reject, 1 clear reject.
- **AISTATS-style 1–7:** 7 strong accept, 6 accept, 5 borderline accept, 4 weak accept/weak reject, 3 borderline reject, 2 reject, 1 strong reject.
- **CHI-style:** A, ARR, RR, RRX, X plus originality, significance, research quality, presentation clarity, related work, and expertise.
- **UIST internal 1–5:** 5 strong accept, 4 accept, 3 borderline, 2 reject, 1 strong reject.

## Review dimensions

Always assess:

- clarity of contribution;
- venue fit;
- novelty or originality relative to supplied or verified related work;
- technical soundness or research quality;
- claim-evidence alignment;
- baselines, comparisons, or rationale for their absence;
- reproducibility and implementation detail;
- ethics, data, participant, or societal issues when relevant;
- limitations and failure cases;
- writing and figure effectiveness.

## Output schema

```markdown
# Simulated Review — [Venue]

## Recommendation
- Overall: [score / recommendation]
- Confidence: [1–5 or official]
- Reviewer stance: [strong accept / accept / borderline / reject]
- Likely variance: [low / medium / high]
- Submission-ready now: [yes / no / borderline]

## Summary
[2–4 sentences describing what the paper claims and contributes.]

## Claimed Contributions
1. [Contribution]
2. [Contribution]
3. [Contribution]

## Strengths
- [Specific strength tied to evidence]
- [Specific strength tied to evidence]

## Weaknesses
- [Specific weakness tied to claim/evidence]
- [Specific weakness tied to claim/evidence]

## Score Rationale
[Why this score, not one level higher or lower.]

## Score Movement Conditions
Would increase if:
- [Concrete evidence, rewrite, or analysis]

Would decrease if:
- [Concrete risk or missing support]

## Top Acceptance Risks
1. [Risk]
2. [Risk]
3. [Risk]
4. [Risk]
5. [Risk]

## Required Revisions Ranked by Score Impact
| Impact | Revision | Evidence affected | Feasibility |
|---|---|---|---|

## Questions for Authors
1. [Question whose answer could affect score]
2. [Question whose answer could affect score]

## Venue-Specific Score Sheet
[Use the relevant venue dimensions.]

## Meta-review Forecast
[Likely AC/SAC/1AC synthesis, disagreement pattern, correctable vs fundamental negatives, and likely decision path.]
```

## Borderline discipline

For any borderline score, explicitly state:

- what real contribution supports acceptance;
- what evidence, novelty, or clarity gap supports rejection;
- what would move the paper up;
- what would move the paper down.
