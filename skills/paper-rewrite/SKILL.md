---
name: paper-rewrite
description: Rewrite research paper sections with venue-aware argument, structure, and claim calibration. Use for abstracts, introductions, related work, methods, systems, evaluations, findings, discussions, limitations, conclusions, captions, and contribution bullets. Outputs polished text first, then concise diagnostics and remaining evidence risks.
---

# Paper Rewrite

Rewrite paper text so it is clearer, more rigorous, and easier for reviewers to evaluate. Preserve the actual work and evidence. Do not add citations, results, participants, or novelty claims unless provided.

## Inputs

Use supplied section text and any available context:

- target venue or venue mode;
- intended contribution;
- evidence and limitations;
- desired word limit;
- author voice constraints.

If venue is missing, infer the closest mode and state the assumption.

## Rewrite order

1. **Argument pass:** align title, abstract, intro, contributions, and conclusion around one central claim.
2. **Structure pass:** make each section's role explicit; remove or move paragraphs that do not serve the claim.
3. **Evidence pass:** soften claims that exceed supplied evidence.
4. **Venue pass:** adjust norms for Graphics, AI/ML/CV, or HCI.
5. **Style pass:** remove hype, vague nouns, promotional language, and unsupported generalization.

## Section patterns

### Abstract

Answer, in order: contribution, problem/context, method/system/study, strongest evidence, field-level takeaway.

### Introduction

Use this spine:

1. domain value;
2. core difficulty;
3. prior-work streams;
4. opportunity or gap;
5. proposed approach;
6. evidence;
7. contribution bullets.

### Related Work

Convert annotated bibliography into synthesis. For each stream: what it enabled, what assumption matters here, and how this paper builds on or differs from it.

### Method or System

Explain mechanism, not just interface. Include inputs, outputs, representation, pipeline, constraints, implementation details needed for evaluation, and failure modes. For HCI systems, organize by workflow stage: what users do, what the system does, why the feature exists, and what mechanism enables it.

### Evaluation or Findings

Start each result with an analytical claim, then evidence, interpretation, and implication. Do not report chronologically unless sequence is the finding.

### Discussion and Limitations

Generalize carefully. For each limitation: what it affects, what it does not affect, and what future evidence would test.

## Output schema

```markdown
[Polished rewritten text first.]

## Diagnostics
- Venue mode assumed: [mode]
- Main change: [one sentence]
- Claims softened or scoped: [bullets]
- Evidence still needed: [bullets]
- Likely score impact: [high / medium / low, with reason]
```

## Guardrails

- Do not invent references, numbers, participants, datasets, baselines, or results.
- Do not use “novel,” “first,” “SOTA,” “significant,” “robust,” or “general” unless evidence is provided.
- Do not rewrite into product language.
- For HCI, keep human agency visible: users inspect, select, revise, reject, redirect, fabricate, or appropriate system outputs.
