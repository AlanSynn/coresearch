# Claim review

A generic "double-check" or a reviewer on every step adds cost without adding evidence. An independent review is
different: a reviewer that never saw the author's reasoning, and preferably runs on the other model family, fails in
different ways. Use it at claim milestones: when a result is about to support a claim in a paper, a decision or a
report to the user, and for subjective deliverables as described below. Run the reviewer at `xhigh` effort or above;
a Claude Code subagent gets a higher effort only when you ask for it.

Give the reviewer the brief (question, success criterion, evidence standard), the artifacts (code revision, commands,
configurations, raw result paths) and the list of claims. Do not give it the narrative of how the result was reached.
Keep it read-only.

| Author | Reviewer |
|---|---|
| Claude Code (Fable, Opus) | Codex: `codex exec --sandbox read-only -c model_reasoning_effort=xhigh -o review.md "$(cat brief.md)" < /dev/null` |
| Codex (Astra, Sol) | Claude Code: `claude -p --effort xhigh --permission-mode plan "$(cat brief.md)" > review.md` |

A review brief that works across both families:

```text
You are reviewing a research result you did not produce. The brief and the artifacts are listed below; the author's
reasoning is not. Check whether the artifacts support each listed claim under the stated success criterion and
evidence standard. Report every discrepancy you find, with file:line or command evidence, including weak or missing
controls, leakage between optimization and evaluation, selection effects, and claims the evidence does not cover.
Skip style. Do not fix anything.
```

Ask for every discrepancy and filter afterwards: a reviewer told to report only severe issues reports less. The lead
decides which findings matter, records the decision and the evidence in the brief, and reruns the review only after a
material change. Two models that read the same wrong input are still not independent evidence; where possible, the
reviewer reruns a check from the raw artifacts.

## Subjective deliverables

Some results have no oracle: visual and motion quality, figures, demo comparisons, manuscript sections. Grading your
own work of this kind skews positive, so before such a result is shown as an improvement or adopted as the new
incumbent, run a capped evaluator loop:

- Write the criteria before the work starts, and calibrate them on one or two of the user's earlier judgments where
  they exist.
- The evaluator is a fresh, read-only agent, from the other model family where possible, at `xhigh` effort or above.
  It sees the rendered frames, video, figure or text and the criteria, not the author's reasoning, and it crops, zooms
  and measures images (for example with PIL or OpenCV) instead of judging them at a glance. The author inspects its
  own renders the same way before handing them over.
- Revise and evaluate again for at most three rounds; stop early when no criterion fails or a round brings no
  improvement. Keep every round's artifact and choose the best one, not the last.
