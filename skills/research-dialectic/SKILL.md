---
name: research-dialectic
description: Dialectical Evidence Synthesizer. Convert papers into dominant position + credible counterevidence + conditions causing disagreement + mechanistic synthesis. Use for intros, related work, framing, hypothesis generation. Fails rather than forces a fake thesis-antithesis.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/synthesis/dialectic.md
  - docs/research/evidence/*.yaml
---

# research-dialectic — Dialectical Evidence Synthesizer

Reconcile disagreeing literature into one defensible picture. Never manufacture
a contradiction to fit the format.

## What & When

Produces: dominant position, credible counterevidence, conditions causing
disagreement, mechanistic synthesis. Use for intros, related work, framing,
hypothesis generation. Not for: mapping the field by stream → research-survey;
judging whether a gap is worth a paper → research-gap; auditing one paper →
research-audit.

## Procedure

First decide whether a genuine disagreement exists. If not, say so and stop.

- **A. Normalize claims** — "Under conditions X, intervention Y affects outcome Z through mechanism M."
- **B. Classify disagreement** — factual / causal / measurement / scope / objective / terminology / implementation.
- **C. Dominant thesis** — by citation prevalence, later-method adoption, benchmark conventions, repeated evidence, field-standard assumptions. Citation count alone insufficient.
- **D. Counterevidence** — negative results, new-population failure, stronger baseline, confound, alternative mechanism, deployment failure, benchmark artifact.
- **E. Mechanistic bridge** — boundary-condition / multi-mechanism / measurement / temporal / population / representation synthesis.

## Output

- Research Question
- Dominant Position (evidence ids)
- Counterposition (evidence ids)
- Nature of the Disagreement — mandatory `disagreement_type:` **one of** `factual|causal|measurement|scope|objective|terminology|implementation` (from step B)
- Mechanistic Synthesis: mechanism, boundary conditions, predictions
- Unresolved Evidence (what the synthesis cannot absorb)
- Research Opportunity: testable question, required experiment, potential contribution

Confidence three-dim on Dominant Position and on the Synthesis separately.

## Reject when (gates 2,3,9 + fail-not-fabricate)

- sources address different questions (no real disagreement) → `disagreement_type=objective`, no synthesis;
- evidence too weak to name a dominant view;
- apparent contradiction is terminological → `disagreement_type=terminology`, stop;
- bridge is unsupported speculation;
- no experiment would distinguish the explanations.

In any of these, output Unresolved Evidence honestly; mark synthesis `low` or absent.

## State & Handoff

State: ledger `claim_state` for Dominant/Counter/Synthesis; rejected reconciliations
to `quality_state.unresolved_methodology_issues`. Next: research-causal (bridge →
model) / research-audit (test load-bearing papers).
Artifacts: dialectic.md + evidence updates.

Re-entry: return to `coresearch` to re-route the next stage.
