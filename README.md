# Coresearch: Research Agent Skills for OMX

Coresearch is an installable research-agent bundle for Codex + oh-my-codex (OMX). It keeps the OMX global prompt intact, installs complete research skills, and can initialize individual research projects with a small bridge block or a full research `AGENTS.md` template.

## What lives where

| Path | Purpose | Installed where? |
|---|---|---|
| `AGENTS.md` | Development prompt for maintaining this Coresearch bundle | No |
| `templates/research/AGENTS.md` | Full research-project prompt template | Copied by `harness init --full` |
| `skills/*/SKILL.md` | Complete research skills | Symlinked/copied into `${CODEX_HOME:-~/.codex}/skills` or project `.codex/skills` |
| `harness`, `bin/harness`, `scripts/harness.py` | CLI for install/init/status/diff/rollback/repair/update | `harness self-install` symlinks command into `~/.local/bin` |

The root `AGENTS.md` is intentionally **not** the template installed into other projects. It is only for editing this bundle.

## Recommended install

### 1. Link skills so repo edits auto-update local Codex skills

```bash
./harness link
```

Equivalent:

```bash
./scripts/install.sh --scope user --mode symlink --force
```

This creates symlinks such as:

```text
~/.codex/skills/paper-design  -> ./skills/paper-design
~/.codex/skills/research-loop -> ./skills/research-loop
```

After this, edits in this repo's `skills/` directory are reflected in local Codex skill files. Restart Codex/OMX to refresh skill discovery metadata in an already-running session.

### 2. Install the `harness` command

```bash
./harness self-install
```

Default install path:

```text
${RESEARCH_HARNESS_BIN_DIR:-~/.local/bin}/harness
```

If `~/.local/bin` is on `PATH`, you can then run:

```bash
harness status
harness doctor
harness repair
harness update
```

Remove the installed command:

```bash
harness self-uninstall
```

### 3. Keep global OMX prompt unchanged by default

Your global prompt should remain the OMX default:

```text
~/.codex/AGENTS.md
```

Check:

```bash
harness status
harness doctor --strict
```

If links or command shims drift, repair the local install without modifying the global prompt:

```bash
harness repair
```

If you want natural global routing into these research skills, add only the small bridge block:

```bash
harness global          # dry-run diff
harness global --apply
```

Remove it later:

```bash
harness global --remove --apply
```

This does **not** replace the OMX global prompt; it only updates a marker-bounded block:

```text
<!-- RESEARCH_AGENT_SKILLS:START -->
...
<!-- RESEARCH_AGENT_SKILLS:END -->
```

## Project initialization

### Interactive wizard

For normal use, just run:

```bash
harness init
```

In an interactive terminal this opens a small built-in menu, similar to a dropdown:

1. choose the target directory;
2. choose `bridge` or `full`;
3. choose dry-run preview or apply;
4. choose whether to replace an existing `AGENTS.md` when using `full`.

Force the same wizard even when passing a target:

```bash
harness init . --interactive
harness init . -i
```

No extra Python packages are required. In non-interactive contexts, such as scripts or CI, use the explicit flags below.

### Safe default: project bridge

Use this for most research repos. It preserves any existing project `AGENTS.md` and adds a small research bridge block.

```bash
cd /path/to/research-repo
harness init              # same as: harness init . --bridge
harness init .            # explicit positional target
harness init -y
```

Equivalent explicit form:

```bash
harness init /path/to/research-repo --bridge
harness init /path/to/research-repo --bridge -y
```

### Full research prompt template

Use this for a research-only repo where you want the full project prompt.

```bash
harness init /path/to/research-repo --full
harness init /path/to/research-repo --full -y
```

This copies:

```text
templates/research/AGENTS.md -> /path/to/research-repo/AGENTS.md
```

If the target already has `AGENTS.md`, full mode refuses to replace it unless you explicitly pass `--replace`:

```bash
harness init /path/to/research-repo --full --replace -y
```

Long-form compatibility remains available:

```bash
harness init /path/to/research-repo --mode full --apply
```

### Diff before writing

All prompt writes are dry-run by default:

```bash
harness diff /path/to/research-repo --bridge
harness diff /path/to/research-repo --full
harness diff --global
```

### Rollback

Prompt writes create backups. Preview rollback:

```bash
harness rollback --scope project /path/to/research-repo
```

Apply rollback:

```bash
harness rollback --scope project /path/to/research-repo -y
```

Global rollback:

```bash
harness rollback --scope global
harness rollback --scope global -y
```

## How AGENTS.md execution works under OMX

When you run Codex/OMX in a project, instruction surfaces compose roughly like this:

1. **Global OMX prompt**: `${CODEX_HOME:-~/.codex}/AGENTS.md`
   - Should remain OMX default.
2. **Project prompt**: nearest `AGENTS.md` in the current directory tree.
   - Installed by `harness init --bridge` or `--full`.
3. **Skills**: `${CODEX_HOME:-~/.codex}/skills/*/SKILL.md` or project `.codex/skills/*/SKILL.md`.
   - Installed/linked by `harness link` or `harness install`.
4. **OMX runtime overlay**: runtime/team state appended by OMX marker contracts.

So the intended setup is:

- global `AGENTS.md`: OMX default;
- user skills: symlinked Coresearch skills;
- target research repo `AGENTS.md`: bridge or full research template;
- `.omx/`: only for explicit OMX runtime workflows.

## Harness command reference

```bash
harness status                         # show global/project/skill state
harness doctor --strict                # verify install health
harness repair                         # relink skills, reinstall command, validate, strict doctor
harness link                           # symlink user-scope skills to this repo
harness install --scope user           # copy user-scope skills
harness install --scope project --project-dir . --project-bridge
harness self-install                   # install harness command into ~/.local/bin
harness self-uninstall                 # remove installed harness command
harness global                         # dry-run global bridge diff
harness global -y                      # apply global bridge
harness global --remove -y             # remove global bridge
harness init                           # interactive wizard in a TTY; bridge dry-run in scripts
harness init .                         # dry-run bridge install for explicit target
harness init . --interactive           # force wizard for a target
harness init . -y                      # apply bridge to current dir
harness init . --full -y               # apply full research template
harness diff . --full
harness diff --global
harness rollback --scope project . -y
harness update                         # relink skills and validate
harness update --pull                  # git pull --ff-only, relink, validate
```

## Validation

Run the full local validation harness:

```bash
./scripts/validate.sh
```

It checks:

- plugin JSON parsing;
- Python and shell script syntax without leaving `__pycache__`;
- broken symlinks in this repo;
- stray carriage-return characters in markdown, Python, shell, JSON, and wrapper files;
- skill frontmatter and expected skill catalog;
- OMX marker contracts in `templates/research/AGENTS.md`;
- root `AGENTS.md` remains bundle-development guidance, not the installable research template;
- `pdf-crawl` safety flags and dry-run behavior;
- user copy install and bridge idempotency;
- user symlink install for repo-auto-update;
- `harness link/status`;
- `harness self-install/self-uninstall`;
- `harness global` dry/apply/remove;
- `harness doctor --strict`;
- `harness doctor` failure on broken skill symlinks;
- `harness repair` relink/self-install/strict-doctor path;
- `harness update` relink;
- `harness init` interactive, positional/flag target, bridge/full/rollback behavior;
- project install behavior;
- OMX availability.

## Policy

- Do not overwrite the global OMX prompt by default.
- Do not create `.agents/` chats, mailboxes, or paper-state forests.
- Use `.omx/` only for explicit OMX workflows, hooks, recovery, or checkpointing.
- Prefer bridge mode for existing projects and full mode for research-only projects.
