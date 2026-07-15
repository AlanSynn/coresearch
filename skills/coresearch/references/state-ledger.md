# Orchestrator State Ledger

Durable state so a multi-skill run does not repeat searches, forget rejected
ideas, loop, or silently overwrite. Each skill reads before starting, updates on
finish. Runtime = the user project (NOT inside skills/, NOT a `.agents/` forest).

## Schema (spec §15)

```yaml
project:
  title: string
  research_question: string
  intended_contribution: method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge
  target_venues: [string]
current_stage: string
completed_skills: [string]
active_skill: string
blocked_by: [{ skill, reason }]
source_state:        # per source_id
  - { id, state: retrieved|screened|fully_read|audited|missing, notes }
claim_state:         # per claim_id
  - { id, state: supported|contradicted|unresolved|rejected, confidence }
gap_state:
  candidates: [string]
  falsified: [{ gap, reason }]
  surviving: [string]
hypothesis_state:
  candidates: [string]
  distinguishable: [string]
  unidentifiable: [string]
quality_state:
  unsupported_claims: [string]
  missing_counterevidence: [string]
  unresolved_methodology_issues: [string]
next_actions: [string]
stop_conditions: [string]
```

## Read/update protocol

- Read the ledger first. If `claim_state` already has a rejected direction for
  the same claim with the same evidence, do not regenerate — surface it.
- Update only the keys your skill touched. Never blanket-overwrite.
- On finish: set `active_skill` null; add the skill to `completed_skills` only if
  absent; replace (do not duplicate) any `next_actions` entry your skill already
  wrote, else append; merge `stop_conditions` without duplicating. Re-entry and
  pipeline loops may call finish more than once — keep these writes idempotent.
- A skill that cannot proceed writes itself to `blocked_by` with a reason
  (replacing any prior entry for the same skill) rather than emitting a
  fabricated partial result.

## Mapping from skill vocabularies

`research-survey` emits `verification_status`, not `source_state.state`. Map
before writing the ledger:

- `PDF VERIFIED` / `FULL TEXT VERIFIED` → `fully_read`
- `METADATA VERIFIED` → `screened`
- `PARTIALLY VERIFIED` → `retrieved` (flag the uncertainty in notes)
- `NOT FOUND` → `missing`

Producer/consumer pairs that share a ledger key: research-survey seeds
`source_state`; research-audit writes `source_state.state = audited` after a
load-bearing read. research-gap writes `gap_state`; research-loop seeds
`hypothesis_state.candidates`; research-causal extends it. research-review and
research-audit/adversary/dialectic/qualitative all touch `quality_state` —
update only the subkeys your skill reasoned about.

## Where it lives

Canonical: `docs/research/decisions/ledger.yaml` under the user's `output_path`
project (spec §4, §15). skills never write state inside their own directory.
OMX missions may mirror checkpoints under `.omx/specs/<mission>/`, and
`$ultragoal` may wrap the same ledger — when an OMX run is active those are
convenience copies; `ledger.yaml` stays the canonical Coresearch state. A
non-OMX consumer reads and writes `ledger.yaml` only.
