# Workspaces, persistent state and parallel agents

- Use tests, scripts or a REPL for complex calculations and transformations, in steps whose intermediate results you
  look at.
- Reuse an expensive intermediate artifact while its inputs, code version and assumptions still match; invalidate what
  depends on it when they change.
- Treat persistent state, such as notebook kernels, caches, databases and reused processes, as a hypothesis: matching
  names, shapes or sizes do not show equal contents or freshness. After a failure, inspect what survived: variables,
  files, transactions and remote jobs.
- Before you claim reproducibility, rerun the relevant path from a clean, documented starting state, in an isolated
  scratch location rather than by cleaning the user's workspace.
- Inspect intermediate visual output when it affects correctness: coordinate frames, units, axes, transforms, mask
  alignment, depth scale and occlusion. Keep sample indices distinct from frame IDs and timestamps.
- Cross-check an important conclusion through a different failure mode, such as an independent calculation or
  observation; two tools fed the same wrong input are not independent.
- Measure tool executions and costs at run time when they matter, including failed attempts; counting call sites in
  the code is an estimate.
- Use the existing environment first, and install kernels, GPU stacks, MCP servers or services only when the task needs
  them. Prompts and worktrees are not a sandbox.
- Enforce repeatable checks with scripts, CI or hooks rather than prose.
- Before a handoff or a context reset on a long task, write the goal, current changes, evidence, decisions, risks and
  next action where the project tracks its work, and recheck the files when you resume. Keep temporary hypotheses and
  secrets out of persistent memory.
- When agents work in parallel, give each one its own files or worktree and confirm the base revision. For a
  consequential change, an independent reviewer looks for counterexamples against the requirements, the diff and the
  evidence; agreement between agents, or the same model run again, is not independent validation.
