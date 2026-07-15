# Evidence Grounding

The one shared contract every research-* skill reads: **every output traceable
source → claim → conclusion.** No major claim without supporting evidence. No
novelty without closest-work. No causal language without identification. No
absence from failed retrieval.

Load this ONCE per skill; do not chase other files from here.

## Evidence object (rates one source)

```yaml
evidence_id: E001
source_id: S001
claim_text: string                       # what THIS source says
claim_type: empirical_result|methodological_claim|theoretical_claim|design_claim|limitation|author_speculation|reviewer_interpretation
supporting_passage: string               # quoted/exact, not paraphrase
location: { section: string, page: int }
study_context: { task, dataset_or_population, sample_size, method, baseline, metric }
result: { direction: positive|negative|mixed|null|unknown, magnitude: string }
limitations: [string]
confidence:                              # per-SOURCE confidence (rates this one source)
  source_reliability: high|medium|low
  extraction_confidence: high|medium|low
  interpretation_confidence: high|medium|low
```

**claim_type hard rule:** never blur an author's `empirical_result` (measured) with
the agent's `reviewer_interpretation` (your reading). Different rows. Flagging
speculation (`author_speculation`) as fact = reject.

## Claim object (rates one synthesized claim)

```yaml
claim_id: C001
claim: string
supporting_evidence: [E001, E004]        # every id resolves to an evidence object
contradicting_evidence: [E011]
scope_conditions: [string]
confidence:                              # per-CLAIM confidence (rates the conclusion)
  evidence: high|medium|low              # = aggregate of source reliabilities
  coverage: high|medium|low              # = did we find the IMPORTANT relevant work
  interpretation: high|medium|low        # = does evidence directly support this conclusion
reasoning: string
```

Two confidence scales on purpose: evidence-object rates a single source;
claim-object rates the synthesized conclusion. Don't merge them.

## Confidence rating rules

- `high` claim only if all three claim-dims are high.
- One low dim → cap at `medium`; two+ low → `low`. Name which.
- Not a vote (5 weakly-independent mediums ≠ high). Not a probability (no `0.87`).
- Reading more of the same kind does not raise coverage.

## Source priority + evidence levels (inline — do not chase research-survey)

Priority ladder: 1 primary peer-reviewed → 2 official supplementary → 3 official
code/dataset docs → 4 dissertation/tech report → 5 systematic review → 6 author
project page → 7 secondary explanation. Never evidence: social media, AI
summaries, blog restatements.

Reading-depth evidence level (carry forward on each evidence object): `PDF_VERIFIED`
(full-text primary in hand) > `ABSTRACT_ONLY` > `INDEX_ONLY`. A claim's confidence
may not exceed the level of its weakest supporting source. research-survey emits a
**verification status** (PDF / FULL TEXT / METADATA / PARTIALLY VERIFIED / NOT
FOUND); the canonical map from verification status to `source_state.state` lives in
[state-ledger.md](state-ledger.md) §Mapping — read it there, do not re-derive a
parallel mapping here.

**Primary-source verification required** when the claim is central / surprising /
quantitative / causal / establishes novelty / criticizes prior work.

**Independence** (record in study_context): not independent when sources share
same dataset / same benchmark assumptions / same group / same unverified claim /
same model or annotation pipeline. Two papers on one benchmark = one group toward
`minimum_independent_groups`, not two.

## Quality gates (the ten; check before finalizing)

1. All major claims linked to evidence?
2. Empirical findings separated from speculation?
3. Disconfirming evidence explicitly searched?
4. Source populations/datasets represented correctly?
5. Causal claims supported by identification strategy?
6. Limitations described at the level of the claim?
7. Novelty based on comparison with closest work?
8. Absence NOT claimed from failed retrieval only?
9. Important unresolved uncertainties visible?
10. Another agent could reproduce the reasoning from saved artifacts?

Gate ↔ skill map (which skill enforces which): research-gap {3,7,8};
research-dialectic {2,3,9}; research-audit {2,4,5,6,7}; research-causal {5};
research-qualitative {2,6,9}; research-adversary {1,3,9}.

Severity scale (audit / adversary / verify reuse): critical / major / moderate /
minor / uncertain.

## Integrity floor

Separate, never blend: fact / inference / recommendation / unknown. Distinguish
author result from agent interpretation. Do not invent citations, venues,
results, participants, metrics, or code behavior. Evidence too weak for a
position → say so, fail the synthesis rather than fabricate.

Artifact paths live under the user project, not inside skills/:
`docs/research/{literature,evidence,hypotheses,audits,qualitative,synthesis,decisions}/`.
