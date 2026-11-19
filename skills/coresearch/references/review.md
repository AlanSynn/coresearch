# Claim review

Current models check their own work; a generic "double-check" or a reviewer on every step adds cost without adding
evidence. An independent review is different: a reviewer that never saw the author's reasoning, and preferably runs on
the other model family, fails in different ways. Use it at claim milestones only: when a result is about to support a
claim in a paper, a decision or a report to the user.

Give the reviewer the brief (question, success criterion, evidence standard), the artifacts (code revision, commands,
configurations, raw result paths) and the list of claims. Do not give it the narrative of how the result was reached.
Keep it read-only.

| Author | Reviewer |
|---|---|
| Claude Code (Fable, Opus) | Codex: `codex exec --sandbox read-only -o review.md "$(cat brief.md)" < /dev/null` |
| Codex (Astra, Sol) | Claude Code: `claude -p --permission-mode plan "$(cat brief.md)" > review.md` |

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
