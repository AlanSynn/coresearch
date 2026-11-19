# Coresearch

A research harness and the single source of the user's standing agent instructions.
The lead model (Astra in Codex; Fable or Opus in Claude Code) frames the problem,
chooses the strategy, synthesizes worker results, and verifies the deliverable.
Native agents and GLM handle bounded work when that helps. Coresearch does not run
a second agent framework.

It holds the shared working agreement for every agent host in [`host/`](host/core.md),
four skills in [`skills/`](skills/), the [best practices](docs/agent-practices.md)
behind them, and an [evaluation](evals/host-policy/README.md) that compares
instruction changes on live agents before they are installed.

## Install the shared instructions

```bash
python3 scripts/coresearch.py host check            # what differs from this checkout
python3 scripts/coresearch.py host install --dry-run
python3 scripts/coresearch.py host install          # add --replace once to adopt hand-written files
```

This writes one generated instruction file per host (`~/.claude/CLAUDE.md`,
`~/.codex/AGENTS.md`, `~/.pi/agent/AGENTS.md`, `~/.config/opencode/AGENTS.md`),
links every skill into `~/.claude/skills` (which opencode also reads),
`~/.codex/skills` and `~/.pi/agent/skills`, links `glm-delegate` into
`~/.local/bin`, links the Codex rules in `host/codex.rules` into `~/.codex/rules`,
and adds the settings in `host/claude.settings.json` (the confirmation rules for
`git push` and `git clean`, and `high` effort for Fable 5.2) to
`~/.claude/settings.json` without touching its other settings; a value already
there, such as an effort level saved with `/effort`, is kept. The confirmation
rules act only in permission modes that ask; in Claude Code's bypass mode and
Codex with approval `never` the prose in `host/core.md` is the guard. Edit
`host/core.md` or `host/<host>.md`, never the generated files: each generated
file records a digest of its text, and one edited by hand is preserved like a
file the command did not create. Such files are replaced only with `--replace`,
which first moves them to `~/.local/state/coresearch/backups/<UTC time>/`,
under their path relative to the home directory. `host render` prints the
generated text.

Skills kept in another repository, such as the private `pace` skill for the PACE-Phoenix cluster, which lives with
its tool, are listed in `~/.config/coresearch/skills.json` (a JSON object of skill name and directory, `~/` meaning
the home directory) and linked into every host like the bundled skills. The file stays on this machine, so a private
skill never enters this repository. A skill's header must be strict YAML, which pi requires: a value holding `: `
must be quoted, or pi drops the skill without a word; `host install` and `host check` refuse a header that is not.

## Start

Use Python 3.10+; no packages or API keys are needed to install the skill.
Run from this checkout and choose the host's skills directory:

```bash
# Codex, user-level linked install
python3 scripts/coresearch.py install --to "$HOME/.agents/skills" --link

# Claude Code, user-level linked install
python3 scripts/coresearch.py install --to "$HOME/.claude/skills" --link
```

For one project, use `/path/to/project/.agents/skills` (Codex) or
`/path/to/project/.claude/skills` (Claude Code) instead. Omit `--link` for a
self-contained copy. The destination argument is the **skills directory**, not
its `coresearch` child. Paths follow the current
[Codex](https://developers.openai.com/codex/skills) and
[Claude Code](https://code.claude.com/docs/en/skills) discovery interfaces.

Reload the host's skill discovery as needed and request, for example:

> Use Coresearch to assess this research idea, implement the most informative
> feasible experiment, and review what the results actually support.

Installation does not select models, provision workers, or grant tool
permissions; choose the strongest available model as the lead.
The native Codex plugin manifest is also retained; choose plugin distribution or
manual installation, not duplicate installations of the same skill.

Skill installation and research work do not change project `AGENTS.md` /
`CLAUDE.md`; only the explicit `host` command manages the global files. No OMX
installation is needed.

## What the skill adds

Only its name and short description need discovery. The loaded
[skill](skills/coresearch/SKILL.md) establishes lead ownership and exposes six
independent resources, not a pipeline:

| Resource | Research capability |
|---|---|
| [Literature](skills/coresearch/references/literature.md) | Source-grounded synthesis, closest work, citation provenance, optional PDF collection |
| [Experiments](skills/coresearch/references/experiments.md) | Contribution design, falsifiers, baselines, executable evaluation, reproducible artifacts |
| [Analysis](skills/coresearch/references/analysis.md) | Gaps, contradictory findings, causal explanations, qualitative analysis, evidence-chain audits |
| [Manuscripts](skills/coresearch/references/manuscripts.md) | Writing, figures/slides, venue critique, rebuttal, verification, release |
| [Delegation](skills/coresearch/references/delegation.md) | Bounded assignments and compact handoffs for native workers, including Claude Code Sonnet/Opus |
| [Claim review](skills/coresearch/references/review.md) | Independent, cross-family review of a result before it supports a claim |

The lead owns consequential decisions and final interpretation. Workers own a clear
scope, relevant inputs, an expected artifact, and completion criteria. The host
supplies execution, permissions, and completion events. No model registry,
polling service, mandatory reviewer chain, or transcript ingestion is added.

## Optional project continuity

Small tasks run directly. Longer projects can reuse their existing notes or
create a brief:

```bash
python3 scripts/coresearch.py init /path/to/project --question "What would distinguish these explanations?"
```

This creates only `research/brief.md`, never overwrites an existing brief, and
never injects instructions into the project. Keep decisions and evidence paths
there when useful; it is ordinary Markdown, not a required state schema.
Both `install` and `init` apply explicitly requested writes without a wizard.
Add `--dry-run` to preview without writing.

## Optional source collection

The agent uses its search tools to resolve paper identities and direct open-access
HTTPS URLs. The downloader does not guess bibliographic matches or verify claims.
Prepare a JSON array with `id`, `title`, `url`, and `access: "open"`; see the
[placeholder example](examples/sources.json) and the
[input/output contract](skills/coresearch/references/literature.md).

```bash
python3 skills/coresearch/scripts/fetch_sources.py sources.json --output research/pdfs --dry-run
python3 skills/coresearch/scripts/fetch_sources.py sources.json --output research/pdfs
```

The real run requires a new output directory. It writes downloaded PDFs and a
`report.json` with source metadata, outcomes, requested/final URLs, timestamps,
byte counts, and SHA-256 hashes. Downloads are not marked as read or verified.
Exit codes: `0` success, `1` partial retrieval failure, `2` invalid configuration
or output, `130` interruption. Completed sources survive a later failure.

Only public HTTPS endpoints are allowed, with IP-pinned TLS, redirect checks,
byte limits, and socket timeouts. There is no proxy support, credential forwarding,
paywall bypass, publisher scraping, fuzzy title resolver, or automatic retry.
This checks transport and a PDF signature, not scientific identity or validity.

## Updating and removal

A linked installation follows the checkout. Review and update it through normal
Git operations. An identical copy or identical link is a no-op; a conflicting,
modified, or broken destination is preserved with an error. To replace a copy,
move the existing `coresearch` directory aside for review, then install again.
Removal is ordinary removal of that installed directory or symlink. No global
prompt or host configuration needs restoring.

Version 2 intentionally removes the old `harness` command, prompt bridges,
full-project prompt, role skills, and OMX routing. Existing installations are not
silently cleaned on other machines. See [migration and decisions](docs/architecture.md)
before upgrading an old installation.

## Development and validation

```bash
python3 -B -m unittest discover -s tests -v
```

Tests exercise installation, copied-skill portability, optional initialization,
source transport/security boundaries, partial results, and repository structure.
They need no external network, account, or model. CI runs the same command.
[Validation and host scenarios](docs/validation.md) distinguish tested software
contracts from live model behavior that requires a configured host.

The design follows OpenAI's
[Astra skill and prompt guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra):
remove inferred workflow machinery, disclose resources when needed, and define
real decision boundaries and completion rather than reasoning recipes.
