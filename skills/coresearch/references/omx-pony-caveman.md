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

## Team / Ultragoal

Use Team for parallel lanes with disjoint write scopes. Use Ultragoal as durable ledger/checkpoint owner. Ralph only when persistent single-owner verification is explicitly selected.
