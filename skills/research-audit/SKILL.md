---
name: research-audit
description: Methodology Auditor. Audit whether a paper's evidence supports its claims, at single-paper and cross-paper level, across claim definition, experimental unit, sampling, baselines, metrics, statistics, ablations, user studies, generalization, reproducibility. Severity-rated issues plus a revised defensible claim.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/audits/<paper>-audit.md
---

# research-audit — Methodology Auditor

Check whether evidence supports claims. Attack the logic, not the author. Always
end with what the evidence DOES support.

## What & When

Single-paper audit; cross-paper methodological comparison. Use when: "is this
paper's methodology sound", "would reviewers attack this", auditing a
load-bearing source. Not for: venue score → research-review; one-citation fact
check → research-verify; challenging your own synthesis chain → research-adversary.

## Procedure

Audit each dimension; tie every finding to the claim it affects.

- **Claim definition** — capability/causal/comparative/generalization/usability/deployment; broader than evidence?
- **Experimental unit** — users/motions/objects/scenes/seeds/tasks/artifacts.
- **Sampling** — representative? hard cases excluded? train/test separate?
- **Baselines** — strongest included? comparable supervision/compute? faithful impl? strawman?
- **Metrics** — measures the claim? sensitive to failure? gameable? consistent with prior work? perceptual quality inferred from geometric error?
- **Statistical reasoning** — independence? right test? repeated measures? multiple comparisons? effect sizes? CIs? significance vs relevance?
- **Ablations** — isolates the mechanism? independent removal? changes budget/capacity? interactions?
- **User study design** — formative/summative/comparative/exploratory? real task? trained? novelty bias? behavior vs preference? qualitative traceable?
- **Generalization** — unseen subjects/objects/geometries/categories/viewpoints/motions/real-world. Never call category-holdout "universal generalization".
- **Reproducibility** — code/data/hyperparams/preprocessing/seeds/hardware/cost/scripts/failed runs.

## Output

- Paper + Claim
- Claim-to-Evidence Alignment — mandatory `claim_type:` (empirical_result/methodological/.../reviewer_interpretation) and whether the paper's stated claim type is broader than evidence supports
- Experimental Design / Dataset-Population Boundaries / Baseline Fairness / Metric Validity / Statistical Validity / Ablation Validity / Generalization Claims / Reproducibility
- Critical Issues table: Severity | Issue | Evidence | Effect on Claim | Required Fix (severity: critical/major/moderate/minor/uncertain)
- Valid Contributions
- Revised Defensible Claim — what the evidence actually supports; carries three-dim confidence
- Recommended Additional Experiment

## Reject when (gates 2,4,5,6,7)

- audit incomplete without a Revised Defensible Claim (attacking without stating what survives is not an audit);
- abstract-only paper + central claim → mark statistical/repro dims `uncertain`, say so, do not guess.

## State & Handoff

State: ledger `source_state=audited`; unsupported claims to
`quality_state.unresolved_methodology_issues`. Next: research-causal (causal claim
survived) / research-adversary (chain bias) / research-review (venue-fit) /
research-gap (if load-bearing paper fails, the gap changes). Artifacts: audit md
+ revised-claim block.

Re-entry: return to `coresearch` to re-route the next stage.
