# Executable workspaces, agent context and parallel work

## 15. Executable workspaces and evidence
- Use available tests, scripts, or a REPL for complex calculations and transformations. Compose tools through small, inspectable steps, not a large speculative program whose intermediate results are never observed.
- Reuse expensive intermediate artifacts within the task when valid. Keep their inputs, producing code or version, assumptions, and relevant metadata; invalidate dependent artifacts when those change.
- Treat persistent state as a working hypothesis, not a trustworthy snapshot. Matching names, shapes, types, or sizes do not establish equal contents or freshness; validate relevant values and invariants.
- After failure, inspect surviving variables, mutated objects, files, transactions, and remote jobs. Namespace cleanup is not transactional rollback, and a reused process is not a clean environment.
- Before claiming reproducibility, rerun the relevant path from a clean, reproducible starting state without undocumented interactive history. Preserve user work and isolate scratch artifacts; never clean destructively to achieve this.
- Inspect intermediate visual outputs when they affect correctness. Check coordinate frames, units, axes, transforms, mask alignment, depth scale, occlusion, and uncertainty as applicable. Distinguish sample indices from original frame IDs and timestamps.
- Cross-check important conclusions using a different failure mode, such as an independent calculation, implementation, or observation. Two tools sharing the same incorrect input are not independent evidence.
- Keep observations compact and attributable to the action that produced them: status, relevant output or error, artifact references, and next check. Mark truncation; retrieve missing details when they affect a decision.
- Measure actual tool executions and costs at runtime when they matter; source-code pattern counts are estimates. Include failed attempts and retries in consumption accounting even when state is discarded.
- Use existing environments first. Do not install Python kernels, GPU stacks, MCP servers, or extra services merely to follow this workflow. AST filters, prompts, and worktrees are not substitutes for an enforced sandbox.

## 16. Claude Code context and tools
- Read only the files, ranges, and search results needed. Use relevant installed Skills on demand; do not load every procedure or tool description into every task.
- Load deferred tool schemas through ToolSearch on demand, one tool at a time, with exact `select:<tool_name>` queries; never use loose keyword patterns, which can load several large schemas at once.
- Verify MCP server connectivity with lightweight zero-argument tools, not heavyweight ones that require external setup (browsers, devices).
- Keep global guidance general and repository guidance specific to verified commands, boundaries, and unusual constraints. Load detailed documents and path-scoped rules only when relevant.
- Before a long-task handoff or context reset, preserve a concise state summary in the existing tracking mechanism: goal, current changes, evidence, decisions, unresolved risks, and next action. Recheck actual files when resuming.
- Persist only confirmed, reusable knowledge. Do not promote temporary hypotheses, failure logs, or secrets into global memory; keep shared project knowledge in team-managed documentation.
- Enforce repeatable checks through appropriate scripts, CI, and hooks rather than prose alone. Bound automation, propagate failures, prevent recursive invocation, and respect authorization for configuration or permission changes.

## 17. Parallel work and independent review
- Parallelize only independent work with clear boundaries. Avoid splitting trivial tasks or tightly coupled edits just to use multiple agents.
- Specify each delegate's goal, inputs, owned files, write permissions, and acceptance checks. Separate concurrent edits by ownership or worktrees and verify the actual base revision.
- For consequential changes, seek an independent review when available. Ask for counterexamples against requirements, diffs, and evidence, not agreement with the implementation narrative.
- Ground reviews and checklist completion in concrete artifacts and checks. Agreement between agents, repeated use of the same model, or an unchecked "verified" label is not independent validation.
- The integrating agent must inspect delegated results and revalidate the combined state. Never claim a review or tool execution that did not occur.
