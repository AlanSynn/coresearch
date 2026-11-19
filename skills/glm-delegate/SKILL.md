---
name: glm-delegate
description: Hand bulk reading, log triage or mechanical edits to GLM through pi when the raw material is large and the answer is small.
---

# Delegating bounded work to GLM

The user's pi subscription gives unlimited use of the latest GLM. The aim is to save the lead model's tokens on bulk,
low-judgment work without lowering the quality of the result. The saving is net of your own cost: the brief, the
answer and your verification all count. Sending non-sensitive repository content through this route is approved.

Call it only through [`scripts/glm-delegate`](scripts/glm-delegate), which is also linked as `glm-delegate` on the PATH:
the brief goes on stdin and GLM's final answer comes back on stdout. It is read-only by default; `--write` allows edits
and refuses to start unless `--cwd` is a clean git tree, so the diff afterwards is exactly GLM's change. GLM gets no
context files, skills or MCP servers, but its read tools are not confined to `--cwd`. Other options: `--cwd`,
`--timeout`, `--thinking`, `--max-chars`. Run long jobs in the background. Each call appends one line to
`~/.local/state/glm-delegate/calls.jsonl` (time, model, brief and answer sizes, duration, exit code) so the thresholds
below can be checked against real use.

## Order of preference

1. No model. Cut raw output before it reaches your context (`head`, `tail`, `grep`, `--stat`, `wc`, a script). To wait
   for something, use a watcher that prints a line only when a condition changes, with a timeout.
2. GLM, when bulk text must be read or judged: a cited digest, a classification or a bounded edit. When a watch
   condition needs reading (is this error real?), filter with `grep` first, send only the matching lines, and act only
   on a positive verdict with its evidence line.
3. Yourself, for everything else.

## When to delegate

All of these should hold:

- The work is token-heavy but low-judgment: reading or searching large logs, files or documents and returning a cited
  digest; triaging long test or build output; mechanical, fully specified edits across many files; boilerplate,
  format conversion, or a first draft of tests from a given spec; a broad first-pass search.
- The raw material you would otherwise read is large (a rule of thumb, not yet measured: more than about 10k tokens)
  and the answer you need is small. Lookups where you know the location, repeated small calls in a loop, and code you
  are about to edit yourself stay with you.
- You can check the result cheaply: tests, lint or type checks, a pattern or count check, or file:line citations.

Keep these with you: design, architecture or trade-off decisions; security, authorization, persistence or migrations;
ambiguous work; final judgments, research claims or review verdicts; exact counts and measurements (run the command
yourself); protected, frozen or pinned files; secrets, credentials and personal or private data, because the content
goes to an external provider.

## Protocol

1. Write a complete brief: the goal and why it matters, the exact scope and files, constraints, the repository state it
   needs (branch, changed files, the commands and results so far), the form of the answer (facts with file:line
   evidence; UNABLE instead of guessing), a size cap for the answer, and the done criteria. State no conclusion you
   want confirmed.
2. Stay read-only unless edits are the task. Use `--write` only with a named file set, in a worktree when your own tree
   has uncommitted changes, and split a large change into separate delegations.
3. Treat the output as an untrusted draft and verify in proportion to its size. Rerun the checks yourself and
   spot-check citations. After `--write`, read the `--stat` summary the wrapper prints first; read a diff in full only
   when it is small (about 200 changed lines or fewer). For a larger mechanical change, check by property: grep the
   changed lines for anything outside the expected pattern, confirm the changed-file set matches the brief, and read
   hunks only where tests do not reach. A truncated answer names the file that holds the full text.
4. If a check fails or the output looks wrong, allow one corrective retry that names the failure, then do the work
   yourself. If pi or GLM is unavailable or slow, do it yourself and say so briefly.
5. Do not delegate from a session that already runs on GLM or from inside `glm-delegate`; the wrapper refuses when
   `GLM_DELEGATE` is set.
6. In the final report, say what was delegated and what you verified yourself.
