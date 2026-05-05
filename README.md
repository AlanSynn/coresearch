# Research Agent Skills for OMX

Installable research prompt/skill bundle for Codex + oh-my-codex. The bundle keeps the global OMX prompt intact by installing skills and, optionally, adding a small marker-bounded bridge block to `AGENTS.md`.

## Recommended install

### 1. User-scope skills only

Safe default. Does not edit global `AGENTS.md`.

```bash
./scripts/install.sh --scope user
```

Then restart Codex/OMX and invoke skills explicitly:

```text
$paper-design
$paper-review
$research-loop
$claim-check
```

### 2. User-scope with global bridge

Adds or updates a small `RESEARCH_AGENT_SKILLS` block in `${CODEX_HOME:-~/.codex}/AGENTS.md`, with a timestamped backup. It does not replace the OMX global prompt.

```bash
./scripts/install.sh --scope user --global-bridge
```

Use this when you want research-task routing to happen naturally from the global prompt.

### 3. Project-scope install

Keeps research behavior local to one repository or paper workspace.

```bash
./scripts/install.sh --scope project --project-dir /path/to/research/repo --project-bridge
cd /path/to/research/repo
omx setup --scope project --plugin
# or: CODEX_HOME=.codex omx
```

Use this when you do not want any global prompt changes.

## Harness command

Use the local harness CLI for status, symlink installs, command installation, project initialization, diffs, rollback, and update/relink workflows:

```bash
./harness status
./harness doctor
./harness link
./harness self-install
harness status                         # after self-install, if ~/.local/bin is on PATH
./harness global                       # dry-run global bridge diff
./harness global --apply               # add/update small global bridge
./harness global --remove --apply      # remove small global bridge
./harness init --target /path/to/research/repo --mode bridge
./harness init --target /path/to/research/repo --mode bridge --apply
./harness init --target /path/to/research/repo --mode full --apply
./harness diff --target /path/to/research/repo --mode full
./harness diff --global
./harness rollback --scope project --target /path/to/research/repo
./harness rollback --scope project --target /path/to/research/repo --apply
./harness update                       # relink user skills and run validation
./harness update --pull                # git pull --ff-only, relink, validate
```

Modes:

- `bridge`: add a small `RESEARCH_AGENT_SKILLS` block to the target `AGENTS.md`; safest for existing projects.
- `full`: copy this repo's full `AGENTS.md` into the target; refuses to replace an existing file unless `--replace` is supplied.

`harness init`, `harness global`, `harness diff`, and `harness rollback` are dry-run by default and print unified diffs. Add `--apply` to write changes. Existing `AGENTS.md` files are backed up before writes.

`harness self-install` installs a symlink command at `${RESEARCH_HARNESS_BIN_DIR:-~/.local/bin}/harness`. Add that directory to `PATH` if the command is not found globally.

## Validate

Run the full local validation harness:

```bash
./scripts/validate.sh
```

It checks plugin JSON, skill frontmatter, OMX marker contracts, install script parsing, user/project install behavior, bridge idempotency, full project `AGENTS.md` install, and `pdf-crawl` dry-run safety.

## Development install / auto-update from this repo

Use symlinks so edits in this repo update the installed user-scope skills immediately:

```bash
./scripts/link-local.sh
```

If you also want the small global `AGENTS.md` bridge block:

```bash
./scripts/link-local.sh --global-bridge
```

Equivalent explicit form:

```bash
./scripts/install.sh --scope user --mode symlink --force
```

## Policy

- Ordinary research work stays cumulative in the current conversation.
- The bundle does not create `.agents/` chats or paper-state forests.
- `.omx/` state is used only for explicit OMX workflows, hooks, recovery, or checkpointing.
