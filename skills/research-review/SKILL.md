---
name: research-review
description: Venue-calibrated simulated review and score forecast for research papers. Use when the user asks to review, critique, score, triage, forecast acceptance, identify acceptance risks, simulate reviewers, or assess submission readiness for SIGGRAPH, CVPR, NeurIPS, ICLR, AISTATS, CHI, UIST, Eurographics, or related venues.
---

# research-review — Venue Review & Score Forecast

Act as a strict but fair author-side reviewer; provide explicit scores. Not for
confidential official peer review unless venue policy permits. In OMX this is a
verification surface: may block completion when score-moving evidence gaps remain.

## What & When

Venue-calibrated simulated review, acceptance-risk triage, score forecast,
reviewer-modeling, submission readiness — for AI, Robotics, Graphics, HCI, hybrid
papers. Use when: "review", "critique", "score", "triage", "forecast acceptance",
"identify acceptance risks", "simulate reviewers", "assess submission readiness";
finding score-moving evidence gaps and rewrite priorities.

Not for: grammar polish → research-proofread; replacement prose → research-write;
citation/source faithfulness → research-verify.

Inputs: manuscript text, figures, captions, supplement, code, results, author
notes. If key inputs are missing, score lower-confidence and state what could not
be checked.

## Procedure

Use official scales if the current venue form is verified; otherwise label scales
`INTERNAL` — memorized mappings go stale each cycle. One anchor; apply the
analogous official scale for the target venue:

- **NeurIPS-style 1–6:** 6 strong accept, 5 accept, 4 borderline accept, 3
  borderline reject, 2 reject, 1 strong reject; rate quality/clarity/significance/
  originality 1–4 when useful.

State score/recommendation, confidence, variance, blockers, and movement
conditions. Judge claim-evidence alignment, not just writing quality. Flag
confidentiality/policy limits before using official reviews.

Review dimensions — always assess:

- clarity of contribution; venue fit;
- novelty/originality relative to supplied or verified related work; claim-evidence alignment;
- technical soundness or research quality; baselines/comparisons or rationale for absence;
- reproducibility and implementation detail; writing and figure effectiveness;
- ethics/data/participant/societal issues when relevant; limitations and failure cases.

Borderline discipline — for any borderline score, explicitly state: what real
contribution supports acceptance; what evidence/novelty/clarity gap supports
rejection; what would move the paper up; what would move the paper down.

## Output

Mandatory fields:

- **Recommendation:** Overall score/recommendation; Confidence (1–5 or official);
  Reviewer stance (strong accept / accept / borderline / reject); Likely variance (low / medium / high); Submission-ready now (yes / no / borderline).
- **Summary:** 2–4 sentences describing what the paper claims and contributes.
- **Claimed Contributions:** numbered list.
- **Strengths:** each tied to specific evidence.
- **Weaknesses:** each tied to claim/evidence.
- **Score Rationale:** why this score, not one level higher or lower.
- **Score Movement Conditions:** "Would increase if" (concrete evidence, rewrite, or analysis); "Would decrease if" (concrete risk or missing support).
- **Top Acceptance Risks:** ranked, ~5.
- **Required Revisions Ranked by Score Impact:** table — Impact | Revision | Evidence affected | Feasibility.
- **Questions for Authors:** answers that could move the score.
- **Venue-Specific Score Sheet:** the relevant venue dimensions.
- **Meta-review Forecast:** likely AC/SAC/1AC synthesis, disagreement pattern, correctable vs fundamental negatives, likely decision path.

## Reject when

- score/recommendation missing confidence, variance, blockers, or movement conditions;
- borderline score missing any of the four required statements (accept support / reject support / up-mover / down-mover);
- official scale cited without current-form verification, or without flagging confidentiality/policy limits.

## State & Handoff

State: review produced; score-moving evidence gaps block OMX completion until
closed. Next: research-write (revision prose) / research-verify (citation
faithfulness) / research-audit (methodology attack) / research-proofread (final
polish). Carry forward variance and unanswered author-questions as warnings. In
a multi-skill run, also seed `quality_state` (unsupported_claims /
missing_counterevidence / unresolved_methodology_issues) from the score-moving
gaps (state-ledger.md); standalone, the review above is enough.
