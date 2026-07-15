# Reasoning Skills — routing & pipelines

Router-owned reference. Disambiguates the research-* skills from each other and
from existing skills, and sequences them per spec §14.

## Disambiguation (which skill, when)

| User wants | Use | Not |
|---|---|---|
| Map existing work by stream | research-survey | research-gap |
| Find an important testable opportunity | research-gap | research-survey (maps, doesn't judge gaps) |
| Why papers disagree + reconciling mechanism | research-dialectic | research-causal (one outcome, not cross-paper) |
| Is ONE paper's methodology sound (claim vs evidence) | research-audit | research-review (venue score), research-adversary (your synthesis) |
| Is this citation/number real | research-verify | research-audit |
| Bias in the evidence-gathering chain of YOUR conclusion/synthesis | research-adversary | research-verify (per-claim fact), research-audit (one paper) |
| Competing causal explanations / identification | research-causal | research-dialectic (disagreement, not mechanism) |
| Code qualitative data into themes | research-qualitative | research-survey |
| Contradictions you'd act on as a gap (scout an opportunity) | research-gap | research-dialectic (reconciles disagreement, doesn't scout opportunities) |
| Neutral summary of ONE paper | research-write (concept-decomposition mode) | research-survey (multi-paper), research-audit (methodology attack) |

## Pipelines (spec §14)

**Standard literature-to-project:**
scope → retrieve/normalize (research-survey) → research-gap →
research-dialectic (major disagreements) → research-audit (load-bearing
papers) → research-causal (mechanisms) → research-adversary (emerging project
claim).

**Qualitative study:**
define RQs → ingest → research-qualitative → research-adversary (themes) →
compare with literature → research-dialectic (conflicts).

**Paper review:**
extract claims → research-audit → research-causal → research-adversary →
(valid contribution, unsupported claim, required experiment, likely reviewer concern).

**New research idea:**
research-gap (problems) → research-causal (mechanisms) → research-audit
(testability) → research-adversary (reject direction) → rank by
importance × tractability × novelty.

## Stall diagnosis (when the workflow loses value)

A run that stalls, repeats searches, re-reads context, has weak synthesis
despite many papers, or a suspiciously clean narrative is mis-routed, not slow.
Diagnose the bottleneck, then route the corrective action to a skill above —
the router does not gather evidence itself.

Bottleneck rules (bind the diagnosis):
- high retrieval / low useful → query too broad / no inclusion criteria / terminology not normalized / secondary overrepresentation.
- high extraction speed / low traceability → no evidence schema / summarization before extraction / compressed claims.
- many papers / weak synthesis → paper-by-paper summaries / unnormalized claims / no comparison dims / no contradiction detection / no research question.
- clean narrative / few contradictions → confirmation bias / over-filtered set / no adversarial search / prose before validation.
- many candidate gaps / weak direction → no ranking / no feasibility / no venue target / gap-gen separated from experiment design.
- repeated agent loops → no stopping criteria / no durable artifacts / re-reading context / no state ledger / unresolved questions untracked.

Every corrective action must name: the target skill, an **Expected Observable
Improvement** (what to check that the fix worked), and a **Stop/Escalation
Condition** (else it loops). If the state ledger is missing or stale, profile
`uncertain` and fix ledger discipline first — do not invent stage metrics.

## Separation principle

Retrieval ≠ synthesis ≠ novelty ≠ writing. Each pipeline step is a different
skill; a skill never does the next skill's job. research-write (narrative agent)
introduces no new factual claims — it returns new claims to the evidence
pipeline first.
