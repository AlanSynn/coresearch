# Validation

Run from the checkout:

```bash
python3 -B -m unittest discover -s tests -v
```

## Automated contracts

The suite uses real temporary files and subprocess CLI calls, with HTTP/DNS/TLS
boundaries mocked. It covers copies and links, idempotency, refusal of conflicts
and recursive installs, preservation of host prompts and existing briefs,
cleanup after copy failure, publish-last skill metadata, and a copied utility
running outside the checkout.

Source tests cover manifest validation, byte/hash provenance, relative redirects,
redirect revalidation and limits, mixed public/private DNS answers, IP-pinned TLS
with the original hostname, private/reserved/multicast targets, invalid schemes
and credentials, timeouts, bad PDF signatures, truncated and oversized responses,
partial-batch reports, interruption, and refusal to reuse output directories.
Dry-run performs no network requests or writes.

Bundle tests check local Markdown links, routing-only frontmatter on every
skill, portable dependencies, and an installed end-to-end fixture workflow. Host
tests check that `host install` writes and links every managed item, is
idempotent, preserves hand-written files unless `--replace` backs them up, only
adds permission rules to a settings file, writes nothing on a dry run, and keeps
each rendered instruction file under 120 lines and 8 KiB.
This is software integration testing, **not** an evaluation of a model's research
quality. The PDF transport fixture is synthetic and is never represented as a
real publication or verified scientific evidence.

## Host scenarios

These are acceptance scenarios for a configured model host, not a mandatory
workflow and not claims that live agents were exercised by the unit tests.

| Scenario | Expected behavior and evidence |
|---|---|
| One citation correction | Inspect the relevant source and edit the claim directly. No project initialization, worker, whole-repo preload, or stage re-entry. |
| Broad research idea to experiment | The lead chooses a discriminating experiment. A bounded worker may implement/test it. Actual commands and results support the final interpretation, including negative evidence. |
| Independent literature collection | Workers get disjoint search scopes and return source locators, verification limits, and compact findings. The lead resolves overlap and contradictory results without ingesting full transcripts. |
| Manuscript/rebuttal | Reuse the existing draft. Separate proposed changes from implemented ones and unrun experiments from results. Finish revisions and verification within authorization. |
| Resuming a project | Read the relevant brief/artifacts, not every skill. Preserve rejected directions and uncertainty; update notes only as needed. |
| No worker or search tool available | Do supported work directly; state any evidence gap rather than invent a worker result, citation, or successful experiment. |
| A consequential permission boundary | Continue safe independent work, but do not publish, expose restricted data, or consume unapproved resources. Ask only for the unresolved decision. |

Evaluate both the quality of the deliverable and overhead: unnecessary loaded
references, worker launches, repeated status checks, and user approvals.

## Final-review boundary

The redesign can be reviewed structurally: one payload, no runtime dependencies,
no orchestration or prompt injection, explicit lead/worker responsibility, and
research standards available on demand. The tests establish those software
contracts. Live delegation between agents, external publisher availability, and
host skill-discovery behavior additionally require the user's configured runtime
and authorized network. Record those runs separately rather than treating an
offline test pass as proof of them.

## Host-policy evaluation of version 3 (2026-11-18)

[`evals/host-policy`](../evals/host-policy/README.md) compared the previous global instructions and skills (baseline:
26 KB for Claude Code, 11 KB for Codex) with the rendered `host/core.md` plus host addition and the four skills
(candidate: about 4 KB per host) on live agents: eleven tasks, each in a fresh fixture or flatpack worktree. Claude Code
ran Fable 5.2 at `high` and, once, Opus 5.5 at `xhigh`; Codex ran GPT-6.2 Astra at `high`. Deterministic checks are
computed from the final repository and answer. Scores are 1–5 from a judge of the other model family, blind to the arm
(GPT-6.2 Astra at `medium` judges Claude Code runs; Opus 5.5 at `medium` judges Codex runs), so they compare arms within
a host, not hosts. The answers, checks and judgments are kept outside version control in the maintainer's
`.sources/evals/host-policy-2026-11-18/`. All figures below are measured.

**Baseline against the first candidate** (revision 1), two repetitions per task and arm, one for Opus 5.5:

| Host and model | Arm | Runs | Checks passed | Task score | Report score | Input tokens, median | Claude cost |
|---|---|---|---|---|---|---|---|
| Claude Code, Fable 5.2 | baseline | 22 | 60/60 | 4.77 | 4.05 | 115,636 | $16.19 |
| Claude Code, Fable 5.2 | candidate | 22 | 60/60 | 4.59 | 4.05 | 85,827 | $13.92 |
| Codex, Astra | baseline | 22 | 62/62 | 4.68 | 4.00 | 101,123 | n/a |
| Codex, Astra | candidate | 22 | 58/62 | 4.50 | 4.00 | 104,099 | n/a |
| Claude Code, Opus 5.5 | baseline | 11 | 30/31 | 5.00 | 3.73 | 172,309 | $5.42 |
| Claude Code, Opus 5.5 | candidate | 11 | 31/31 | 4.82 | 3.82 | 106,043 | $5.34 |

**Revisions**, candidate only, against the baseline rows above:

| Revision | Host and model | Runs | Checks passed | Task score | Report score | Input tokens, median |
|---|---|---|---|---|---|---|
| 2 | Codex, Astra: all tasks, cleanup twice more | 13 | 41/41 | 4.77 | 4.08 | 103,193 |
| 2 | Claude Code, Fable 5.2: cleanup, pinned file, flatpack question | 3 | 11/11 | 5.00 | 4.00 | 115,815 |
| 3 | Codex, Astra: all tasks, pinned file and flatpack question twice more | 15 | 42/43 | 4.60 | 3.80 | 103,269 |
| 3 | Claude Code, Fable 5.2: all tasks | 11 | 31/31 | 4.73 | 3.91 | 88,267 |

What the runs showed:

- **A strong boundary stopped requested work.** Asked to clean up a cluttered checkout, Codex under revision 1 deleted
  nothing in both repetitions and asked for approval, citing "ask first before deleting untracked files in bulk"; the
  baseline, which has no such line, removed the generated files and kept the user's notes and results. Claude Code
  cleaned up under both arms. This is the failure the GPT-6.2 guidance predicts for Astra. Revision 2 lists cleanup
  among the requests that proceed, exempts actions the request already asks for, and limits the deletion boundary to
  work that cannot be regenerated; Codex then cleaned up correctly in all three runs.
- **An independent review tightened the wording.** A read-only GPT-6.2 Astra review of the change found that "follow
  the more specific instruction" could rank a repository file above the user's message, that "report only what a tool
  result shows" excluded evidence the user supplies, and that uncommitted edits to tracked files were unprotected.
  Revision 3 fixes all three. A single-run dip on two Codex tasks did not repeat in two more runs of each.
- **Cost fell on Claude Code.** Median input tokens were 26% lower with Fable 5.2 under revision 1, 24% lower under
  revision 3, and 38% lower with Opus 5.5, consistent with the smaller instruction file (the arms also differ in their
  skills). Codex token use was unchanged.
- **Quality was level within the resolution of these runs.** Report scores did not fall. The Claude Code task-score
  differences come mostly from the log-triage task, where the candidate argued that a recurring warning was a failure
  and put it in the failure table in all four candidate runs, and the judge took a point each time; revision 1 also
  lost a point twice for showing the CSV number format only by example, which revision 3 did not repeat.
- **The pinned-file task is answered differently by the two hosts, under both arms.** Codex added a new versioned
  evaluator in every run, as the fixture's `AGENTS.md` asks; Claude Code changed only the caller in all but one run.
  Every run left the pinned file intact.

**Corrections made during the evaluation**, each applied to every arm and every saved run:

- Checks: the sources task's "not established" pattern missed "did not measure" and "unknown"; the specification
  task's "tests untouched" check counted added tests and became "original tests kept"; the cleanup task now scores
  "build removed", adds "cache and log removed", and compares the kept files' contents; the flatpack "no edits" check
  now also rejects new commits and failed git commands. Rechecking every saved run with the stricter checks changed no
  earlier value. The flatpack "no edits" check of the first repetition missed the skills exclude in worktrees, whose
  `.git` is a file; those four values are recorded as unknown because the worktrees no longer existed.
- Judging: Codex answers cite absolute paths, and 30 of them named the arm through the workspace directory, so the
  judge now masks workspace paths and those judgments were redone. The pinned-file rubric now states the fixture's rule
  that behavior changes go into a new versioned module, which the judge could not see and had penalized. The claims
  rubric quoted nominal means (0.874 and 0.861) instead of the fixture's actual means (0.872 and 0.856) and penalized
  correct arithmetic; it now computes them from the fixture, and every claims answer was judged again. One judgment
  returned malformed JSON and was redone.
- Interruptions: a usage limit stopped eight Claude Code runs, which were rerun, and every judgment of the first
  repetition's Codex runs, which were redone; `codex exec` waited on an open stdin until stdin was closed.

**Limits.** One or two repetitions on eleven development tasks written by the author of the candidate: a one-point
difference on one task is anecdotal, and the set is not a benchmark. Revision 2 and 3 runs are compared with baseline
runs from earlier the same day, not re-paired. The evaluation exercises instructions and skills only: Claude Code ran
with permissions bypassed and Codex without the managed rules, and pi and opencode were not run. Judges see the answer,
the checks and a change summary, not the transcript or the fixture's own instructions; they marked down Korean answers
on the flatpack tasks, which flatpack's `AGENTS.md` asks for, under both arms. The flatpack rubrics state that rule only
since the revision 3 repeat runs. Seconds include service latency and are not compared.

Revision 3 was installed until revision 4 replaced it ([below](#revision-4-of-the-working-agreement-2026-11-19)).

## Engineering skill revision (2026-11-19)

Version 3 moved the former Claude Code engineering policy into the `engineering` skill with its text unchanged. That
text was written for earlier models and conflicted with the shared instructions in places: it asked for "the minimal
correction" where `host/core.md` asks for the strongest result, it allowed commits only on request where a repository
may allow them, it prescribed a fixed inspect-plan-implement loop and a reading list before every edit, and it carried
Claude Code tool rules (deferred tool loading, MCP checks) into a skill that Codex also reads. The revision keeps the
engineering stances (simplicity, SOLID as criteria, domain-driven design only where the domain needs it, compatibility
and migrations, risk-based testing, security, persistent state, independent review), states them as criteria rather
than a procedure, defers scope, approvals, evidence and reports to the working agreement, removes the process
reference and the host-specific rules, and shrinks the skill from 22.5 KB to 12.8 KB.

[`evals/host-policy`](../evals/host-policy/README.md) compared the two versions on three tasks the skill is for (t12
schema upgrade, t13 consolidation of drifted pricing rules, t14 parser fix with tests), three repetitions per task, arm
and host. Both arms used the installed revision 3 instructions and the same other skills; only the `engineering` skill
differed. Claude Code ran Fable 5.2 at `high` and Codex GPT-6.2 Astra at `high`; the judges saw the code change as well
as the answer. The records are in the maintainer's `.sources/evals/engineering-2026-11-19/`. All figures are measured.

| Host | Skill | Runs | Checks passed | Task score | Report score | Input tokens, median | Claude cost |
|---|---|---|---|---|---|---|---|
| Claude Code, Fable 5.2 | previous | 9 | 30/30 | 4.44 | 4.22 | 155,870 | $9.24 |
| Claude Code, Fable 5.2 | revised | 9 | 30/30 | 4.56 | 4.11 | 160,074 | $10.29 |
| Codex, Astra | previous | 9 | 30/30 | 3.67 | 3.67 | 140,659 | n/a |
| Codex, Astra | revised | 9 | 30/30 | 3.67 | 3.67 | 162,276 | n/a |

- **Quality was level.** Every deterministic check passed under both versions, and the judges' scores for the same
  task and repetition differ by at most one point, in both directions. On the parser task, Claude Code rejected
  malformed input such as `abc5m` in two of three runs with the revised skill and in none with the previous one, but
  one of those two runs never opened the skill, so this is not evidence of an effect; Codex rejected it in none.
- **The revised skill cost somewhat more.** Within each task and repetition, the revised skill used more input tokens
  in 7 of 9 Codex pairs (median ratio 1.16) and 6 of 9 Claude Code pairs (median ratio 1.26). Codex ran 105 commands
  against 97, spread over reads, git, tests and probes; on the parser task it ran the empty suite before the change
  and confirmed that its new tests failed on the old code before fixing it, which `testing.md`'s "run the relevant
  checks before the change" asks for.
- **Both versions were loaded.** Codex opened the skill in every run, and the revised skill's specific references more
  often (`design.md` on the pricing task in all three runs, against none). Claude Code did not load the skill in three
  parser-task runs (one previous, two revised), which therefore compare nothing but noise.

**Limits.** Three development tasks, written by the author of the revision, on which both versions pass every check:
the comparison shows no loss on these tasks, not a gain. The conflicts the revision removes (commit permission, minimal
fixes, host-specific tool rules) are not exercised by any task. The judges graded tasks t12 to t14 with the code change
in view, which earlier tasks did not have.

The revised skill is the installed version.

## Revision 4 of the working agreement (2026-11-19)

Three Opus 5.5 reviewers compared revision 3 with the current vendor guides (see [agent practices](agent-practices.md))
and agreed on changes that remove limits the strongest models do not need, plus one sentence against early stops.
Revision 4 makes them in one step:

- `host/core.md`: finish the in-scope work before listing other improvements, as notes rather than offers; a question
  or diagnosis may run read-only commands, tests and scratch probes outside the working tree; routine tool use (web
  search, fetching papers, documentation and packages, read-only `gh`, the model command-line tools as workers or
  reviewers on non-sensitive content, the archive tools) is not sending content to an external service; `coresearch`
  is for work a research claim or manuscript rests on; `glm-delegate` is for checkable bulk work, and reading and
  synthesis that a claim rests on stay with the lead.
- `host/codex.md`: do not end a turn on a plan, an offer or a next step the agent is authorized to take.
- `coresearch`: a description that says when to use it; parallel workers (typically 3–5) for breadth such as a
  literature landscape; a brief, with the approaches ruled out and their evidence, whenever work crosses a session or
  a compaction; reviewers at `xhigh` and a capped loop with a fresh evaluator from the other family for subjective
  deliverables; `/effort max` or `codex --profile ultra` for open-ended discovery.
- `glm-delegate`: a description limited to log triage, metadata extraction, passage search and mechanical edits.
- The documents now say that the Codex `prompt` rules and the Claude Code `ask` rules confirm `git push` and
  `git clean` only in modes that ask. Under bypassed permissions or approval `never`, which the maintainer mostly uses,
  the instructions are the guard.

[`evals/host-policy`](../evals/host-policy/README.md) compared the installed revision 3 with its skills (baseline)
against revision 4 with its skills (candidate). The first repetition ran fourteen tasks: four from the version 3 set
(t01, t05, t07, t08), the two long-horizon research tasks t15 (literature summary) and t16 (drift study with a brief),
and the routing tasks t20 to t27. The second repetition ran t15 and t16 again. Claude Code ran Fable 5.2 at `high`,
Codex GPT-6.2 Astra at `high`; judges as in version 3. The records are in the maintainer's
`.sources/evals/rev4-2026-11-19/`. All figures are measured.

| Host | Arm | Runs | Checks passed | Task score | Report score | Input tokens, median | Claude cost |
|---|---|---|---|---|---|---|---|
| Claude Code, Fable 5.2 | revision 3 | 16 | 31/31 | 4.88 | 4.00 | 119,979 | $11.35 |
| Claude Code, Fable 5.2 | revision 4 | 16 | 31/31 | 4.75 | 3.88 | 135,480 | $14.37 |
| Codex, Astra | revision 3 | 16 | 31/31 | 4.75 | 4.12 | 114,940 | n/a |
| Codex, Astra | revision 4 | 16 | 31/31 | 4.88 | 4.38 | 108,698 | n/a |

Scores are means over the eight runs with a rubric (t01, t05, t07, t08, and t15 and t16 twice).

- **Quality was level.** Every check passed under both revisions, and per-run scores differ by at most one point, in
  both directions.
- **The research skill now loads where it should.** On the four research requests (t20 to t23), Claude Code loaded
  `coresearch` in 3 of 4 runs under revision 3 and in 4 of 4 under revision 4. It also loaded the skill for the
  confounded-claims task t05 under revision 4 only. Codex loaded the skill on all four requests under both revisions.
  Neither host loaded it on any of the four routine coding requests (t24 to t27) under either revision.
- **GLM no longer receives the synthesis.** On the literature task, Codex under revision 3 handed GLM a screening
  pass that included "conditions changing the direction or magnitude of the effect", the judgment the conclusion
  rests on. In the first repetition the call failed (see corrections); in the second it succeeded. Under revision 4,
  Codex delegated nothing in the first repetition. In the second it delegated only a metadata inventory, briefed as
  "No synthesis, calculations, or file edits", and verified the counts itself. In one log-triage run, Codex under
  revision 4 delegated the triage to GLM with a checkable answer. In the other log runs, both revisions read the skill
  and searched the log themselves. Claude Code never called GLM.
- **Ruled-out approaches were not retried.** All eight drift runs reached a drift of 7.4e-6 with the step and the
  step count unchanged, and none adopted the tolerance change or semi-implicit Euler that the brief rules out. Claude
  Code re-measured semi-implicit Euler as a comparison row in three of four runs, under both revisions. The trace check
  only matches the fixture's own form of that integrator, so it did not flag these runs. One judge took a point for
  it in one revision 4 run.
- **Research work costs more under revision 4.** Over the nine research runs per arm, Claude Code cost $8.66 under
  revision 3 and $11.48 under revision 4, and Codex used 21 % more input tokens. Over the seven routine runs, Claude
  Code cost $2.69 and $2.90, and Codex used 5 % fewer input tokens. The extra work follows the changes:
  - loading `coresearch` on t05 (195 s against 34 s, the same scores);
  - checking the related-work citations by web search and reporting the ones it could not confirm (t21);
  - more comparison evidence in the drift brief (t16).
  The rubrics saturate (most scores are 5), so these runs cannot show whether the extra work pays off.

**Codex verbosity.** GPT-6.2 Astra and Sol default to `model_verbosity = "low"` in Codex. On t03, t05 and t07, two
repetitions each, both arms used revision 4. The candidate arm alone had `model_verbosity = "medium"`.

| Verbosity | Runs | Checks passed | Task score | Report score | Final answer, median characters |
|---|---|---|---|---|---|
| `low` (default) | 6 | 18/18 | 4.67 | 4.17 | 342 |
| `medium` | 6 | 18/18 | 4.67 | 4.00 | 543 |

Longer answers did not score better, so Codex keeps the default.

**Corrections made during the evaluation**, each applied to both arms:

- **GLM in the Codex sandbox.** `glm-delegate` fails in Codex's `workspace-write` sandbox, because pi cannot create its
  lock file in `~/.pi/agent`, so every Codex GLM call of the first repetition failed. The maintainer's Codex sessions
  mostly run with full access, where it works. The second repetition, the log rerun and the verbosity runs give both
  arms network access and pi's folder through the new `run.py --codex-config` option.
- **Counting GLM calls.** The GLM count matched any command that named `glm-delegate`, including reading its
  `SKILL.md`. It now counts calls of the script only. A recheck of the first repetition changed six counts and no
  check.
- **The literature task's judge.** The judge did not see `notes/evidence.md`, the file that t15's rubric grades. It
  marked down Codex answers that left the merged duplicate and the excluded notes to that file: 3 and 3 under both
  revisions in the second repetition. Task t15 now shows the judge the written change (`show_diff`), and all eight t15
  runs were judged again:
  - Codex in the first repetition: 5 and 4 under both revisions;
  - Codex in the second repetition: 4 and 4 under revision 3, 5 and 4 under revision 4;
  - Claude Code: unchanged.
- **Partial judging.** `judge.py --tasks` would have replaced the whole judgment file with the selected tasks; it now
  keeps the other tasks' judgments. No judgment was lost.

**Limits.** These are one or two repetitions of development tasks written by the author of the revision, and the
rubrics are saturated: the comparison shows no loss and better routing, not a quality gain. No run of either revision
ended on an offer or a deferred next step, so the Codex sentence against early stops was not exercised. Neither were
the confirmation rules, the evaluator loop for subjective deliverables or the parallel-worker rule. Claude Code ran
with bypassed permissions, and pi and opencode were not run.

Revision 4 is the installed version.

## Pace skill revision (2026-11-19)

The `pace` skill, for running work on Georgia Tech's PACE-Phoenix cluster with the user's `pace` command, was the one
user-wide skill outside Coresearch. It was a 28 KB file in the private `phoenix` repository, copied into Claude Code's
and the shared `~/.agents` skill folders but not into pi's or opencode's. It mixed the developer runbook with running
jobs. It also carried the state of one experiment repository from September, including a person-specific log path,
and it prescribed a fixed retry count and polling. The revision splits it in two:
- the developer runbook moves into the repository's `AGENTS.md`;
- the usage skill (5.7 KB plus a 3 KB workspace reference) is restated for current models: submitting defers to the
  working agreement's rule for cluster allocations, waiting uses a watcher, a failed run is diagnosed before it is
  resubmitted and recorded afterwards, and the project-specific state is gone.

The skill stays in `phoenix`, beside the code it describes. `host install` links it into every host from
`~/.config/coresearch/skills.json`, so it never enters this public repository.

[`evals/host-policy`](../evals/host-policy/README.md) compared the two skills on three pace tasks against a stand-in
cluster: preparing a GPU run that cannot start as asked (t30), diagnosing a job that vanished from the queue (t31) and
fetching a smoke run that no longer reproduces (t32). Both arms used the installed revision 4 instructions and skills,
and only `pace` differed (and one routing row in `coresearch`). Claude Code ran Fable 5.2 at `high`, Codex GPT-6.2
Astra at `high`; three repetitions. The first repetition used a draft that named `squeue` and `sacct` without saying
that they run on the login node over SSH, and both hosts guessed host names. The second and third used the revision
with that line. The records are in the maintainer's `.sources/evals/pace-2026-11-19/`. All figures are measured.

| Host | Skill | Runs | Checks passed | Task score | Report score | Input tokens, median | Claude cost |
|---|---|---|---|---|---|---|---|
| Claude Code, Fable 5.2 | previous | 9 | 39/39 | 4.22 | 4.00 | 402,159 | $11.23 |
| Claude Code, Fable 5.2 | revised | 9 | 39/39 | 4.11 | 4.00 | 315,518 | $8.32 |
| Codex, Astra | previous | 9 | 37/39 | 3.11 | 3.89 | 152,484 | n/a |
| Codex, Astra | revised | 9 | 39/39 | 3.44 | 4.00 | 194,385 | n/a |

On the second and third repetitions alone, Claude Code's task scores are 4.17 under both skills and Codex's are 3.00
against 3.33.

- **Nothing was submitted.** In all 36 runs no agent ran a submit command, and every run loaded the skill.
- **Codex checked the budget.** On t30, Codex under the previous skill skipped `pace billing` in two of three runs and
  proposed a 6-hour job that the budget cannot start. Under the revision it checked in all three. Under both skills
  it still offered the infeasible H200 command as its main answer, and it named the cause of the dead job without
  proposing a fix. The judges marked down both arms for these.
- **Claude Code cost less.** The revision used fewer input tokens in 8 of 9 Claude Code pairs (median ratio 0.75) and
  cost 26 % less. Codex used about the same input (median ratio 1.04) and wrote longer answers.
- **The old example state leaked.** In two of three dead-job runs, Claude Code under the previous skill read the
  September repository's person-specific log path on an unrelated project; under the revision, no run did.
- **Receipts.** Claude Code under the revision fetched with `pace sync` into a temporary directory in two of three
  fetch runs. That left the fetch receipt uncommitted, which it reported, and a judge took a point each time; the
  previous skill forbade `pace sync` for completed jobs.

**Limits.** Three development tasks against a stand-in cluster with canned answers, written by the author of the
revision. The stand-in has no queue dynamics, real failures or real budgets, and help text comes from the real
`pace`. The first repetition's candidate is the draft, so the nine-run figures mix two versions. The judges'
rubrics ask for an explicit run id, which most runs under both skills omitted.

The revised skill is the installed version.
