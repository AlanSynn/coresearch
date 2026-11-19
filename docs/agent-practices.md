# Agent practices for research

How the user's agents are instructed, and why. The working agreement itself is [`host/core.md`](../host/core.md); the
research procedures are the [`coresearch` skill](../skills/coresearch/SKILL.md). This document records the evidence
behind them, where each kind of instruction lives, and how a change is evaluated.

## Sources

The vendor guides are listed in [`guides.json`](guides.json) and saved as Markdown by `python3 scripts/fetch_guides.py`,
which writes `.sources/guides/<date>/` with a receipt of URLs, retrieval times and SHA-256 hashes. Pages published as
Markdown are kept as served; HTML pages are reduced to their article and converted with pandoc, which drops images. The
copies are vendor text, read locally and kept out of version control. Re-run the script when a vendor publishes guidance
for a new model and review what changed. The set read on 2026-11-18 covered GPT-6.2 Astra and Sol (API and Codex
guides), the "Rethinking skills and prompts for GPT-6 Astra" post, GPT-5.6 Sol, the Codex documentation on `AGENTS.md`,
skills, subagents, rules and configuration, the Claude prompting guides for Fable 5.2, 5.1 and 5, Opus 5.5 and 5 and
Sonnet 5.5, the Claude Code documentation, Anthropic's engineering and research posts on long-running and multi-agent
work, and Z.ai's coding-agent page. Vendor figures quoted below come from the vendors' own tests, mostly on small tasks:
they indicate direction, not what to expect here.

## What the guides agree on

1. **Describe the outcome, not the procedure.** State the goal, the reason, the success check, the constraints and the
   stop rules, then let the model choose the path. OpenAI's Codex guide: describe the work as to a colleague who knows
   the project, then say "what you'll look for when you review the work".
2. **Write standing instructions for the strongest model that will read them.** OpenAI: "Guidance that helps Sol or
   Luna may overconstrain GPT-6 Astra", and boundaries written in strong language for earlier models make Astra "stop
   work where you'd actually be happy for it to continue". Anthropic: skills written for earlier models "are often
   too prescriptive" for Fable 5 and can degrade output; cautions that pile up in notes and memory make Fable 5.2 ask
   for approvals it does not need.
3. **Keep them short, consistent and specific.** Write only what the agent cannot infer from the code and documents.
   Contradictions destabilize the model more than missing detail (Sol 5.6). Reserve absolute words for real
   invariants; emphasis makes the model over-apply a rule (Claude Code). Claude Code recommends fewer than 200 lines;
   Codex stops reading global plus project instructions at 32 KiB. OpenAI reports leaner system prompts scoring about
   10–15% higher with 41–66% fewer tokens in its coding-agent runs.
4. **State decision boundaries once, by request class.** Questions, reviews and diagnoses are answered, not
   implemented; changes, fixes and experiments proceed with local checks; a short named list of external, destructive
   or costly actions needs confirmation. Repeating "ask first" in several places causes needless approval requests
   (Sol 5.6, Fable 5.2).
5. **Define done.** A check that passes or fails lets the model close the loop itself. For unattended runs, enforce it
   in the harness (`/goal`, a Stop hook, a capped continuation loop) rather than with "keep going" prose, which Claude
   Code notes causes over-work when nothing is stalling. Astra "can feel more tentative about when to stop", so make
   running, inspecting and fixing part of the request when that is the job.
6. **Do not add generic self-verification.** Current models test and check their own work; "double-check" and "verify
   with a subagent" cause over-verification (Opus 5, Astra post). Independent review is different: a fresh reviewer
   that never saw the author's reasoning finds what the author cannot. Ask it to report everything and filter later,
   and to skip style.
7. **Use effort, not wording, for depth.** "Think hard" is ordinary text; effort is the control. Fable 5.2: most of the
   gain arrives at `high`, `xhigh` where a gain is measured, `max` for open-ended scientific problems. Codex: Medium
   for a survey, High to trace one cause across systems, Extra High when several causes interact.
8. **Put procedures in skills and keep their descriptions short.** Skills load on demand; a root `SKILL.md` should be a
   minimal router to its references. Over-broad descriptions make models load skills that do not help (Astra post).
9. **Keep long-horizon state in files.** A progress file with status, completed work, failed approaches and why,
   result tables at checkpoints and known limits, plus a commit per unit of work (Anthropic's long-running scientific
   computing post: without recorded failures, "successive sessions will re-attempt the same dead ends").
10. **Delegate for parallelism, isolation, fresh eyes or restricted tools, not for a better answer.** Brief delegates
    with the objective, the reason, the output, the tools and the boundaries; scale the number of agents to the
    problem; subagents can dominate a session's cost (Anthropic multi-agent research, Claude Code, Fable 5.2).
11. **Write the final report for a reader who saw nothing.** Outcome first, plain sentences, none of the shorthand
    coined while working (GPT-6.2, Fable 5.2).
12. **Keep the prefix stable.** Changing instructions mid-conversation costs cache and reasoning on both vendors; edit
    the instruction files between sessions.
13. **Change one thing at a time and measure on real tasks.** About 20 real tasks reveal large effects; judge end
    states, correctness first, then tokens and time.

## Where each instruction lives

| Layer | Holds | Mechanism |
|---|---|---|
| Shared core | Who the user is, precedence, what a request authorizes, evidence and report standards, pointers to skills | [`host/core.md`](../host/core.md), rendered into every host's global file by `coresearch.py host install` |
| Host addition | The few lines only one host needs (Monitor in Claude Code, subagents in Codex, no self-delegation on GLM) | `host/<host>.md` |
| Enforced rules | What must hold every time | Codex [`host/codex.rules`](../host/codex.rules); Claude Code [`host/claude.settings.json`](../host/claude.settings.json), merged into `settings.json`; project checks such as flatpack's pin check |
| Skills | Procedures loaded on demand | [`coresearch`](../skills/coresearch/SKILL.md), [`engineering`](../skills/engineering/SKILL.md), [`glm-delegate`](../skills/glm-delegate/SKILL.md), [`disk-archive`](../skills/disk-archive/SKILL.md) |
| Project | Mission, contracts, commands, protected files | The repository's `AGENTS.md` |
| Memory | Corrections and confirmed approaches, one per file | The host's memory; prune cautions whose reason no longer holds |

## Models and effort

| Work | Claude Code | Codex | Note |
|---|---|---|---|
| Interactive ideation, sketches, small edits | Opus 5.5 `medium` | Sol `medium` | The user reviews each step anyway |
| Research design, subtle debugging, result analysis | Fable 5.2 `high` or Opus 5.5 `xhigh` | Astra `high`–`xhigh` | Correctness depends on easily missed cases |
| Long unattended work, open-ended discovery | Fable 5.2 `high`–`xhigh` with `/goal` | Astra `xhigh`–`max` | `max` where the problem is open-ended |
| Claim review | The family that did not author the result, read-only | the same | Brief and artifacts, not the narrative |
| Bulk digests and mechanical edits | GLM through `glm-delegate` | the same | The lead verifies |

## Evaluation

Changes to `host/` are compared on live agents with [`evals/host-policy`](../evals/host-policy/README.md) before they
are installed. Results of the version 3 adoption are recorded in [validation](validation.md).
