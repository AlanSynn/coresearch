# OMX, Ponytail, Caveman

## Ponytail

Use minimal code, not toy output. For research code, shortest durable architecture wins:

- reuse repo patterns first;
- keep IO/model/data at adapters;
- keep config explicit;
- add one runnable check for non-trivial logic;
- avoid speculative abstractions.

## Caveman

Keep prose terse, but expand when safety/order/confidentiality would become ambiguous.

## Autoresearch

Before `$autoresearch`, require:

- mission;
- sandbox;
- validator mode: `mission-validator-script` or `prompt-architect-artifact`;
- completion artifact path;
- output artifact path if prompt-reviewed.

## Native subagents

Use native subagents only for bounded parallel work that improves quality, speed, or safety. Coresearch skills do not automatically transfer into a fresh subagent context, so every handoff must include:

- `agent_type`: pick the narrow OMX role (`explore`, `researcher`, `executor`, `test-engineer`, `verifier`, `code-reviewer`, `writer`, `critic`, etc.); do not use `worker` outside active `$team`/`$swarm`.
- Research context: field mode, primary skill, claim/evidence target, confidentiality limits, and expected output.
- Skill context: pass the relevant `coresearch`/`research-*` skill item or quote the minimal instructions needed; use `fork_context` only when prior thread context is actually required.
- Style/plugin context: explicitly restate active Ponytail/Caveman mode and level (for example, `Ponytail full active; prefer minimal durable code` or `Caveman lite active; keep report terse`). Do not assume fresh subagents inherit active skill/plugin modes.
- Scope: disjoint files or read-only question, validation expected, and what not to invent.

Default native `agent_type` mappings (not `$skill` routes):

| Need | `agent_type` | Required context |
|---|---|---|
| Repo/file/symbol lookup | `explore` | paths, symbols, exact question |
| Official docs, current venue policy, literature metadata | `researcher` | source priority, date/version needs, citation format |
| Research code edit | `executor` | claim supported, files owned, smallest check |
| Test/reproducibility plan | `test-engineer` | command surface, expected artifact, failure criteria |
| Claim/source/completion audit | `verifier` | claims, sources, PASS/FAIL/PARTIAL schema |
| Deck/figure/manuscript quality review | `code-reviewer`, `critic`, or `writer` | field mode, audience/venue, no-fabrication rule |

## Team / Ultragoal

Use Team for parallel lanes with disjoint write scopes. Use Ultragoal as durable ledger/checkpoint owner. Ralph only when persistent single-owner verification is explicitly selected.

## Re-entry to coresearch

OMX lanes (the full set is in [routing.md](routing.md) §OMX lanes; e.g.
`$autoresearch`, `$ralplan`, `$team`, `$ultragoal`, `$deep-interview`) and native
subagents are executors, not routers. On terminal — or when a research stage
follows their output — re-enter `coresearch` to re-classify and route the next
stage. Example: `$autoresearch` terminal → `coresearch` → `research-write`
(write-up) or `research-verify` (result claims). Do not chain a research skill
from inside the lane. Lane results land in the canonical `ledger.yaml`
(state-ledger.md); downstream skills read them there, not from a guessed OMX path.
