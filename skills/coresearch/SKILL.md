---
name: coresearch
description: "Use when a research claim or paper rests on the work: experiment design, literature, analysis, claim review, manuscripts, long studies. Not routine coding."
---

# Coresearch

The lead model (the session's own model) owns framing, strategy, consequential decisions, synthesis, and final
verification. Delegate bounded gathering, implementation, testing, or review when useful; do trivial work directly. A
worker completes its assigned scope and returns findings rather than taking over the research agenda.

Aim at the strongest contribution the evidence could support. Build a working end-to-end slice early, run it, and let
real outputs choose the next step. Explore alternatives quickly, then double down on what works. Validate lightly while
exploring and rigorously before a claim: a promising preliminary result is a reason to investigate further, not
evidence for a general conclusion.

Breadth-first work (a literature landscape, several candidate methods or datasets, several independent hypotheses)
goes further with parallel workers, typically three to five, one per independent thread with its own sub-question and
output file. Keep coupled work, such as one pipeline, with one agent.

Finish the requested deliverable, including relevant validation and correction.

Use existing project artifacts. When work will cross a session or a compaction, keep a [brief](templates/brief.md)
(a project state file with the same fields counts), including the approaches ruled out and why: they stay while the
reason holds. On resuming, read it and the recent git log and rerun the smallest end-to-end check before new work. A
task that fits in one session needs no brief.

## On demand

Read a reference only when the current task needs it; they are resources, not stages.

| Need | Resource |
|---|---|
| Literature, citations, source collection | [Literature](references/literature.md) |
| Contribution design, experiments, research engineering, unattended runs | [Experiments](references/experiments.md) |
| Gaps, contradictions, causal or qualitative analysis | [Analysis](references/analysis.md) |
| Writing, figures, review, rebuttal, release | [Manuscripts](references/manuscripts.md) |
| A bounded worker assignment, including GLM for bulk work | [Delegation](references/delegation.md) |
| An independent review before a result supports a claim | [Claim review](references/review.md) |
| NCSA Delta GPU runs, staging, result retrieval, storage audit | [NCSA Delta](references/ncsa.md) |
| PACE-Phoenix GPU runs | the `pace` skill |

Keep empirical claims traceable to inspected sources or actual runs. A retrieved
file is not a verified claim. Preserve contrary evidence and unresolved limits
in the deliverable, not just in a worker transcript.
