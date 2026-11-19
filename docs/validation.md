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

Revision 3 is the installed version.

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
