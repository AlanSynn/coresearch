# Research Contract

The one rule everything hangs on: **every research output traceable from
source evidence → extracted claim → interpreted implication → final conclusion.**
No major claim without supporting evidence. No novelty without closest-work
comparison. No causal language without identification. No absence-from-search.

## Orchestrator input contract (what a run needs)

```yaml
topic: string
research_question: string
intended_contribution: method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge
target_venues: [string]
scope: { years: [start,end], domains: [string], populations: [string], excluded_topics: [string] }
evidence_requirements: { minimum_primary_sources: int, minimum_independent_groups: int, require_counterevidence: bool }
output_path: string
# optional: known_papers, existing_project_claims, candidate_hypotheses,
# available_datasets, time_budget, compute_budget, implementation_constraints
```

## Claim ↔ evidence binding

The evidence + claim object structure, confidence dimensions, and rating rules
live in [evidence-grounding.md](evidence-grounding.md) — skills load that ONE
file per invocation. Binding rules that live here: no major claim without ≥1
`supporting_evidence`; contradicting evidence narrows scope, never hidden;
unresolved evidence id = blocker.

## Contribution ↔ evidence matching

`intended_contribution` decides what evidence the claim must carry:

| Contribution | Evidence must establish |
|---|---|
| method | what is new vs closest work; a test that would fail without it |
| system | components, data flow, failure modes, cost |
| representation | what it captures, what it loses, where it helps |
| theory | scope conditions, predictions, disconfirming cases |
| dataset | coverage, bias, annotation procedure, license |
| benchmark | difficulty calibration, leakage check, baselines, evaluation protocol |
| empirical_finding | direction, magnitude, identification strategy, limitations |
| design_knowledge | grounded excerpts, negative cases, transfer conditions |

## Harness rules (spec §19 / §21)

1. Separate retrieval from synthesis. No single agent search + read + novelty + write.
2. Preserve rejected directions — log with reason; don't regenerate unless new evidence.
3. Load only relevant context: current RQ, schema, relevant artifacts, unresolved. Not every doc.
4. No novelty claim without closest-work comparison.
5. No causal claim without an identification strategy.
6. Match evidence to contribution type (table above).
7. Maintain explicit stopping criteria.
8. Report uncertainty as output, not as absence.

## Integrity floor (overrides everything)

Shared with evidence-grounding.md §Integrity floor — if the no-fabrication list changes, update both.

Separate, never blend: fact / inference / recommendation / unknown.
Distinguish author's empirical result from agent's interpretation.
Do not invent citations, venues, results, participants, metrics, or code behavior.
If evidence too weak for a position — say so, fail the synthesis rather than fabricate one.
