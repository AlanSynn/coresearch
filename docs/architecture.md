# Architecture and migration

## Version 3: one source for the agents' standing instructions (2026-11-18)

**Context.** The same user works through Claude Code, Codex, pi and opencode. Their global instruction files had
drifted apart: a 26 KB, 180-line engineering policy for Claude Code, an 11 KB research stance for Codex, and a GLM
delegation block copied into four files. Codex reads at most 32 KiB of global plus project instructions, and the
Codex global and flatpack's project file together had reached 32,703 bytes. The current vendor guides for the
strongest models (GPT-6.2 Astra and Sol, Claude Fable 5.2 and Opus 5.5; see [agent practices](agent-practices.md))
recommend short, consistent standing instructions, decision boundaries stated once, and procedures loaded on demand,
and warn that guidance written for weaker models can hold the strongest ones back.

**Decision.** Coresearch is the single source for those instructions. `host/core.md` holds the shared working
agreement and `host/<host>.md` the few lines specific to one host. `scripts/coresearch.py host install` renders one
generated instruction file per host, links every skill in `skills/` into each host's skills directory, links
`glm-delegate` onto the PATH, and installs confirmation rules for push and clean (Codex rules, Claude Code ask
rules; they act only in permission modes that ask, so in the user's usual bypass and approval-`never` modes the prose
boundary in `core.md` is the guard) and Claude Code's default effort for Fable 5.2, `high`, which its guide recommends for research and
long agentic work and which Claude Code would otherwise leave at `medium`. Procedures moved out of the always-loaded files into skills: `engineering` (the former
Claude Code policy, split by topic and then restated as criteria for current models; see
[validation](validation.md#engineering-skill-revision-2026-11-19)), `glm-delegate` and `disk-archive`.

This replaces version 2's boundary that Coresearch never edits host configuration or global prompts, **for the `host`
command only**. `install` and `init` keep that boundary.

**Safeguards.** Generated files start with an HTML comment naming their sources and a digest of their text; Claude Code
strips such comments from its context. The `host` command refuses to overwrite a file it did not generate, or a
generated file edited by hand, unless `--replace` is given, and then moves the original to
`~/.local/state/coresearch/backups/<UTC time>/`, outside every directory a host scans for skills or rules. New files
and links are staged beside their destination and swapped in, so a failure leaves the original in place; a generated
file reached through a link, such as a dotfiles checkout, is rewritten at the link's target. In a host's settings file
the command only adds the settings it manages, after a backup, keeping the file's link and permission bits: a list
gains the entries it lacks, any other value is set only where its key is absent, so a level the user saved stays, and a
file with an unexpected structure is left alone. `host check` reports any managed file, link or rule that differs
from the checkout.

**Alternatives considered.** A single file symlinked into every host was rejected because Codex has no import mechanism
and each host needs a different addition. Hand-maintained files per host were the previous state and drifted within
weeks. One long global file was rejected because of the Codex size cap and the vendors' guidance against long standing
prompts.

**Consequences.** A change to `host/core.md` reaches every host at once, so it is evaluated with
[`evals/host-policy`](../evals/host-policy/README.md) before installation; the first evaluation and the revision it
led to are in [validation](validation.md). Project instructions still take precedence over the core. Revisit this when a vendor guide changes materially (re-run `scripts/fetch_guides.py`) or an evaluation
shows a regression.

## Version 2: starting point and decision

The inspected baseline is `d62ad4e0609b5ec912a2f7c0d3b0d378326e3f0f`.
It bundled 15 skills, an explicit stage/re-entry router, cross-skill YAML state,
OMX-specific runtime references, full/bridge project prompts, and a large
installer/repair/rollback surface. Those mechanisms mostly managed agent behavior
and prompt placement rather than producing research evidence.

The redesign starts with Astra's judgment and the host's existing tools. Coresearch
is a portable research skill, not an agent server. There is deliberately no
`run` command: invoking a model, granting permissions, starting workers, and
tracking jobs are host responsibilities. This avoids embedding provider APIs,
credentials, model identifiers, and another orchestration lifecycle.

[OpenAI's design guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
informs the separation of short routing metadata, task-local resources, and
repository-specific instructions. It is not copied into a persistent prompt.

## What survived, and what did not

| Earlier assumption | Replacement and reason |
|---|---|
| Every task needs a stage, field, primary role, and router re-entry | One skill exposes resources. Astra chooses the relevant work directly. |
| Analytical lenses need separate agents/skills and serialized outputs | One analysis reference; use only the lens that resolves a real uncertainty. |
| Persistent orchestration needs an active-skill/blocked/gap/claim YAML ledger | Existing artifacts plus an optional short Markdown brief; no schema engine or mirrors. |
| Research requires an OMX prompt bridge or full project instructions | No installed project/global instructions. Native skill discovery is sufficient. |
| Install lifecycle requires self-install, aliases, repair, update, rollback, inventory, wizards | Two explicit commands: install one payload; optionally create one brief. Git and ordinary files handle the rest. |
| Autonomous research requires framework lane selection and fixed retry counts | Scientific validators and budgets in task context; host job lifecycle; lead decides when to change direction. |
| Source collection should infer paper identity through multiple fuzzy APIs | The agent resolves identity. A small downloader fetches exact open URLs and records transport provenance. |
| Every role needs repeated evidence and safety instructions | One short evidence floor, then only task-specific standards in relevant resources. |

The research capability mapping is intentional, not a silent feature drop:
`research-survey` and citation checking become Literature; `research-design`,
`research-loop`, and `research-engineer` become Experiments; `research-gap`,
`research-dialectic`, `research-causal`, `research-qualitative`, `research-audit`,
and `research-adversary` become Analysis. `research-write`, `research-review`,
`research-rebuttal`, and manuscript verification become Manuscripts. Source
verification remains shared with Literature. AI/ML/CV, Robotics, Graphics, HCI,
and hybrid evidence standards remain in the experiments resource. Office-format
mechanics stay with appropriate external tools.

A retrieved PDF is intentionally weaker evidence than an inspected paper, and an
inspected paper is weaker than support for a particular claim. Transport reports
never collapse those distinctions. Fuzzy lookup and the old roadmap table parser
are removed, not retained as compatibility adapters.

## Boundaries

The root `AGENTS.md` is only for maintaining this repository. Installation copies
or links `skills/coresearch` including its relative references, template, and
source utility; it never copies this root file. Skill names are discovered from
the actual payload, not a second role manifest. `.codex-plugin/plugin.json`
contains distribution metadata only.

Astra decides research strategy and validates the final synthesis. A worker gets
a bounded objective, scope, needed context, artifact, and completion criteria.
Native workers and configured Claude Code processes are alternatives, not
additional mandatory infrastructure. A task without available workers proceeds
directly. Completion notifications or a blocking native call replace polling.

The optional brief is project state, not persistent behavioral instruction. No
reference is mandatory for every task; no initialization, output directory,
agent, or approval ceremony is required merely to answer a small question.
Real authorization boundaries still apply to confidential data, participant
studies, external publication, compute, and destructive operations.

The two Python utilities own only deterministic mechanics. Installation refuses
conflicts instead of acquiring overwrite/backup/rollback responsibilities.
The downloader assumes an authorized, curated URL manifest, pins TLS to validated
public DNS answers, and retains partial results in a fresh directory. DNS and
socket timeouts are not a wall-clock job scheduler. Host limits remain necessary
for hard deadlines. It does not parse or execute downloaded documents.
The Delta helper (`skills/coresearch/scripts/ncsa.py`, documented as the NCSA
Delta resource) likewise owns only deterministic mechanics: run layout,
inventory hashing, retrieval receipts, and audit snippets. The allocation,
account, and interactive Kerberos+Duo session remain the user's.

## Migration from version 1

This is a breaking replacement, not a compatibility release. The repository
contains no old role skills, `_coresearch` markers, `skills/manifest.json`, OMX
reference layer, `harness`/`bin` wrappers, shell installer, prompt template, or
old validation script.

On an existing machine, inspect the previous install before removal. Remove only
Coresearch-owned `research-*` skill directories or links and the old `coresearch`
copy/link from the previous installation; preserve unrelated skills and local
edits. Old defaults included `~/.codex/skills`, `~/.claude/skills`, and project
`.codex/skills` / `.claude/skills`. Install version 2 in the current host directory
shown in the README. A conflicting old destination is deliberately not erased.

Remove the old `~/.local/bin/harness` link only after confirming it belongs to
this checkout. Existing prompt blocks bounded by
`<!-- RESEARCH_AGENT_SKILLS:START -->` and `<!-- RESEARCH_AGENT_SKILLS:END -->`
are obsolete. Review and remove just that block, retaining all surrounding
instructions. A former full-project prompt needs a human-readable review to
retain genuine project constraints; do not replace it wholesale with the new
bundle's root `AGENTS.md`. The new installer never edits these files for you.

Keep old research artifacts, PDFs, notes, and ledgers as evidence. They need no
conversion to continue using them, and can be summarized into the optional brief
only when useful. New source batches use explicit URL JSON manifests. This is
one-time migration guidance, not a legacy runtime kept inside version 2.
