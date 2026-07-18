# Coresearch Bundle Development Guidelines

This repository builds and maintains an installable research-agent bundle for Codex + oh-my-codex (OMX). The root `AGENTS.md` is for developing this bundle only. The installable research project prompt lives at `templates/research/AGENTS.md`.

## Role & Intent

Maintain a lean, installable, OMX-compatible research workflow package:

- complete skills under `skills/*/SKILL.md`;
- installation and project-initialization tooling under `harness`, `bin/`, and `scripts/`;
- project prompt templates under `templates/`;
- validation that proves installs, symlinks, bridges, rollback, and safety behavior work.

Success means users can install the bundle without replacing the OMX global prompt, keep local skill edits automatically reflected through symlinks, and initialize individual research repos with either a bridge block or a full research `AGENTS.md` template.

## Operating Principles

1. **Do not repurpose this root file as the installable research prompt.** Edit `templates/research/AGENTS.md` for target-project behavior.
2. **Keep global OMX intact.** Installation should not overwrite `~/.codex/AGENTS.md`; only marker-bounded bridge updates are allowed when explicitly requested.
3. **Prefer symlink development installs.** Local edits should flow to `~/.codex/skills` through `harness link` / `scripts/link-local.sh`.
4. **Skills stay complete and modular.** Put workflow detail in skill files, not in the root prompt.
5. **No `.agents/` state forests.** Do not add legacy `.agents/` chat/mailbox/state behavior. Use `.omx/` only for explicit OMX runtime state.
6. **Diff before write.** Project/global prompt modifications should support dry-run diff previews and backups.
7. **Validate every tooling change.** Run `./scripts/validate.sh` after changing prompts, skills, install scripts, or harness behavior.

## Execution Protocol

Use the harness as the primary operational surface:

```bash
./harness status
./harness link
./harness init /path/to/repo --bridge
./harness init /path/to/repo --full -y
./harness global
./harness doctor --strict
./harness repair
./scripts/validate.sh
```

When changing install behavior:

1. update `scripts/harness.py` and wrappers if needed;
2. update `README.md` examples;
3. update `scripts/validate.sh` with a regression check;
4. run validation;
5. report changed files and validation evidence.

## Constraints & Safety

- Do not apply global bridge changes unless the user explicitly asks.
- Do not replace an existing project `AGENTS.md` without `--replace` semantics or an explicit user request.
- Do not commit generated caches such as `__pycache__`, `.omx/`, or `tmp/` artifacts.
- For long bundle commands such as `./scripts/validate.sh` or harness sweeps, use `skills/coresearch/references/execution-safe.md`: capture full output under ignored `.tmp/` scratch and inspect only bounded summaries.
- Treat this repo's `tmp/` crawls as reference-only; do not install them.

## Verification & Completion

Before claiming completion, provide:

- files changed;
- install surface affected: user skills, global bridge, project template, or harness only;
- validation command and exact PASS/FAIL result;
- any remaining manual step, such as restarting Codex/OMX to reload skill metadata.

## Recovery

Use `harness rollback` for project/global `AGENTS.md` backups. For bad local skill installs, rerun:

```bash
./harness link
```

For broader install drift, run:

```bash
./harness repair
./harness doctor --strict
./scripts/validate.sh
```

<!-- OMX:RUNTIME:START -->
<!-- OMX:RUNTIME:END -->
<!-- OMX:TEAM:WORKER:START -->
<!-- OMX:TEAM:WORKER:END -->
