# Bounded delegation

Use the host's native workers, a configured Claude Code or Codex process, or GLM
through the `glm-delegate` skill, not a Coresearch runtime. Sonnet, Opus or Sol can
handle substantial exploration, implementation, tests, and independent audits.
GLM suits large logs and build output, metadata extraction, locating passages and
mechanical edits whose completeness you can check cheaply; reading and synthesis
that a claim rests on stay with the lead. Choose by task and available tools, not a fixed
model ladder.
The lead retains architecture, ambiguous/high-impact decisions, synthesis, and final
verification. Delegation is optional, including for small research tasks.

A useful assignment contains the objective, only the relevant context/paths,
owned scope and interfaces, the tools and sources to use, how its scope differs
from sibling workers, constraints, expected artifact, and completion criteria. Specify read-only scope for exploration/audits and disjoint files or
worktrees for concurrent edits. A worker should flag an architecture issue rather
than silently expanding its mandate. Do not pass confidential data to a worker
or service outside the user's authorized environment.

Request a compact handoff: findings; files/components; changes made; unresolved
issues; and validation commands/results. Return artifact paths instead of raw
transcripts or large logs. Evidence gathering should include source locators and
what was actually inspected. An implementation handoff should identify the patch
or revision the tests exercised.

Launch once, then do independent lead work or wait on the host's completion
mechanism. Consume the completed result when it informs a decision. Do not build
status-polling loops, repeated progress requests, or a reviewer on every step; the
capped evaluator loop for [subjective deliverables](review.md#subjective-deliverables)
is the exception.
On a blocked result, the lead decides whether to rescope, supply missing context,
change workers, or do the task directly. Never claim a worker ran when no runtime
was available.

For an already configured Claude Code installation in a trusted worktree, the
non-interactive interface can consume a bounded brief and emit a final handoff:

```bash
claude -p --model sonnet "$(cat task.md)" > handoff.md
# Use --model opus for a task better suited to that worker.

codex exec --sandbox read-only -o handoff.md "$(cat task.md)" < /dev/null
# Use --sandbox workspace-write for an implementation worker in a worktree. Close stdin: when
# it is an open pipe, as in a background shell, codex exec waits for more input indefinitely.

glm-delegate --cwd /path/to/project < task.md > handoff.md
# Read-only by default; see the glm-delegate skill before using --write.
```

The brief is task-local, not persistent repository instruction. Use the host's
permission controls for the assigned scope; this command is not a sandbox.
Repository hooks/configuration may load in ordinary `-p` mode. For untrusted
checkouts or stronger isolation, use the host's supported sandbox/bare execution
and its required authentication, not permission-bypass flags.
