---
name: research-write
description: Rewrite research paper sections with venue-aware argument, structure, and claim calibration. Use for abstracts, introductions, related work, methods, systems, evaluations, findings, discussions, limitations, conclusions, captions, and contribution bullets. Outputs polished text first, then concise diagnostics and remaining evidence risks.
---

# research-write — Paper Section Rewriter

Rewrite paper text to be clearer, more rigorous, and reviewer-evaluable; preserve the actual work and evidence.

## What & When

Rewrites and calibrates paper sections for AI, Graphics, Robotics, HCI, or hybrid
venues — abstracts, introductions, related work, methods/systems,
evaluations/findings, discussions, limitations, conclusions, captions,
contribution bullets — matching each field's narrative while preserving author
intent and supplied evidence. Use when: "rewrite this section", "tighten the
argument", "make reviewer-ready", "explain a concept / decompose a mechanism".
Not for: inventing results/citations/participants/datasets/baselines/novelty;
acceptance scoring → research-review.

## Procedure

Pick a spine (Ha technical systems / Oh design-computing / hybrid dual-claim);
match field tone — AI/Robotics precise/measurable, HCI situated/material-centered,
Graphics representation/artifact-centered; infer venue if missing and state it.
Inputs: venue/mode, contribution, evidence + limitations, word limit, voice
constraints. Five passes → field rules; polished text first, diagnostics second.
- **Argument** — align title, abstract, intro, contributions, conclusion around one central claim.
- **Structure** — make each section's role explicit; cut paragraphs not serving the claim.
- **Evidence** — soften claims that exceed supplied evidence.
- **Venue** — adjust norms for AI/ML/CV, Robotics, Graphics, HCI, or hybrid.
- **Style** — strip hype, vague nouns, promotional and unsupported language.

**Field rewrite rules:**
- AI/ML/CV — make the bottleneck measurable; name formulation, baselines,
  ablations, datasets/splits, compute, error modes when supplied.
- Robotics — foreground embodied constraints: platform, sensing/action/contact,
  resets, safety, calibration, hardware or realistic-sim evidence, deployment.
- Graphics — foreground representation, geometric/physical correctness, authoring
  control, visual quality, runtime, galleries, comparisons, failure cases.
- HCI — foreground audience, practice, material/context, user agency,
  study/findings, artifacts, accessibility, design implications.
- Hybrid — connect workflow and mechanism in every paragraph; separate technical
  claim from design/workflow claim.

**Section patterns (the write modes):**
- Abstract — contribution, problem/context, method/system/study, strongest
  evidence, field-level takeaway, in that order.
- Introduction — spine: domain value → core difficulty → prior-work streams →
  opportunity/gap → proposed approach → evidence → contribution bullets.
- Related Work — turn annotated bibliography into synthesis. Per stream: what it
  enabled, the assumption that matters, how this paper builds on or differs.
- Method or System — explain mechanism, not just interface: inputs, outputs,
  representation, pipeline, constraints, eval-relevant implementation details,
  failure modes. HCI systems organize by workflow stage: what users do, what the
  system does, why the feature exists, what mechanism enables it.
- Evaluation or Findings — lead each result with an analytical claim, then
  evidence, interpretation, implication. Not chronological unless sequence is
  the finding.
- Discussion and Limitations — generalize carefully. Per limitation: what it
  affects, what it does not, what future evidence would test.

**Concept-decomposition mode** (trigger: "explain a concept", "decompose a
mechanism"). Decompose in five layers: problem → intuition → mechanism →
formalization → boundary conditions. The worked example must match the formal
definition; mark illustrative examples as illustrative; introduce no new factual
claims beyond supplied evidence. Emit as prose, then the same diagnostics.

## Output

```markdown
[Polished rewritten text first.]
## Diagnostics
- Venue mode assumed: [mode]
- Narrative spine used: [Ha / Oh / Hybrid]
- Main change: [one sentence]
- Claims softened or scoped: [bullets]
- Evidence still needed: [bullets]
- Likely score impact: [high / medium / low, with reason]
```

## Reject when (guardrails)

- would require inventing references, numbers, participants, datasets, baselines, or results;
- "novel", "first", "SOTA", "significant", "robust", or "general" asserted without evidence;
- request is to rewrite into product language;
- HCI rewrite drops human agency (users inspect, select, revise, reject, redirect, fabricate, appropriate system outputs);
- concept decomposition adds a claim not in supplied evidence, or the worked example diverges from the formal definition.

## State & Handoff

State: rewritten text carries inline diagnostics; softened/scoped claims flagged
for author confirmation; evidence-still-needed tracked. Next: research-review (venue-fit + scoring) / research-audit (softened claim needs methodology backing). Artifacts: section md + diagnostics.

Re-entry: return to `coresearch` to re-route the next stage.
