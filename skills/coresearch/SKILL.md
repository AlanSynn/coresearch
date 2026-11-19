---
name: coresearch
description: Research projects, literature synthesis, experiments, manuscripts, and evidence review.
---

# Coresearch

The lead model (Astra in Codex; Fable or Opus in Claude Code) owns framing, strategy, consequential decisions,
synthesis, and final verification. Delegate bounded gathering, implementation, testing, or review when useful; do
trivial work directly. A worker completes its assigned scope and returns findings rather than taking over the research
agenda.

Aim at the strongest contribution the evidence could support. Build a working end-to-end slice early, run it, and let
real outputs choose the next step. Explore alternatives quickly, then double down on what works. Validate lightly while
exploring and rigorously before a claim: a promising preliminary result is a reason to investigate further, not
evidence for a general conclusion.

Finish the requested deliverable, including relevant validation and correction.
Resolve ordinary ambiguity from context; ask only when a consequential decision
cannot responsibly be inferred. Host permissions and the user's scope still apply.

Use existing project artifacts. For work spanning sessions, an optional
[brief](templates/brief.md) records the question, status, evidence, failed approaches,
and next useful action. A small task needs neither initialization nor a state ledger.

## On demand

Read only a reference that adds something needed for the current task; these are
resources, not stages or a required sequence.

| Need | Resource |
|---|---|
| Literature, citations, source collection | [Literature](references/literature.md) |
| Contribution design, experiments, research engineering, unattended runs | [Experiments](references/experiments.md) |
| Gaps, contradictions, causal or qualitative analysis | [Analysis](references/analysis.md) |
| Writing, figures, review, rebuttal, release | [Manuscripts](references/manuscripts.md) |
| A bounded worker assignment, including GLM for bulk work | [Delegation](references/delegation.md) |
| An independent review before a result supports a claim | [Claim review](references/review.md) |
| NCSA Delta GPU runs, staging, result retrieval, storage audit | [NCSA Delta](references/ncsa.md) |

Keep empirical claims traceable to inspected sources or actual runs. A retrieved
file is not a verified claim. Preserve contrary evidence and unresolved limits
in the deliverable, not just in a worker transcript.
