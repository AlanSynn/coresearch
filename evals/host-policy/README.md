# Host-policy evaluation

Compares two instruction arms on live agents before a change to `host/` is installed:

- **baseline**: the hosts' previous global instructions and skills, from a snapshot directory given with `--baseline`
  (`claude_global.md`, `codex_global.md`, and every skill in `skills/`). The snapshot holds personal files and stays
  out of the repository. To evaluate a change to one skill, the snapshot holds the current rendered instructions and
  the current skills with the old version of that skill.
- **candidate**: `host/core.md` plus the host addition, rendered by `scripts/coresearch.py`, with every skill in
  `skills/`.

The arms differ only in global instructions and skills. Each run gets its own workspace with a fresh fixture
repository from [`tasks.py`](tasks.py). Claude Code runs with `--setting-sources project,local`, so the user's own
`CLAUDE.md`, settings and skills stay out; the arm's instructions sit in a `CLAUDE.md` above the repository and its
skills in the repository's `.claude/skills`. Codex runs with a temporary `CODEX_HOME` holding the arm's `AGENTS.md`, a
minimal `config.toml` and the arm's skills; a copy of the user's `auth.json` is placed there with mode 600 for the run
and deleted right after it. The flatpack tasks run in a detached worktree of the flatpack checkout, removed afterwards.

```bash
python3 -B evals/host-policy/run.py --baseline <snapshot dir> --out /tmp/host-policy-eval/<name> \
  --claude-model <model> --codex-model <model> [--claude-effort high --codex-effort high]
python3 -B evals/host-policy/judge.py /tmp/host-policy-eval/<name> --codex-judge <model> --claude-judge <model>
python3 -B evals/host-policy/summarize.py /tmp/host-policy-eval/<name> [more run dirs]
```

Nothing has a default model: `run.py` refuses without a model for every host it runs and `judge.py` without a judge
model for every host it judges, and both refuse a name such as `default` or `best` that could resolve to a top-tier
model. Fable and Astra, any model whose name contains `fable` or `astra`, are expensive and their usage limits are
tight, so they run only within a grant the user made. The user grants in their own terminal:

```bash
python3 evals/host-policy/grants.py grant fable --runs 40 [--hours 12]   # asks the user to type the family
python3 evals/host-policy/grants.py list
python3 evals/host-policy/grants.py revoke fable
```

The grant is kept in `~/.config/coresearch/eval-grants.json`, outside the repository. `run.py` and `judge.py` take
the runs and judgments they need from it before anything starts and refuse otherwise, naming the command for the
user. The grant command reads its confirmation from the controlling terminal, which an agent's shell does not have.
An agent asks the user for a grant and never creates, edits or works around one. Inside a run, a hook in Claude Code
and in Codex (whose hooks run without a trust review, since the run's temporary home holds only this hook) denies a
subagent that asks for a top-tier family the run has no grant for; the run records every subagent model request in
`subagent_models`. The harness also drops `ANTHROPIC_*MODEL*` and `CLAUDE_CODE_*MODEL*` variables from the agents'
environment and refuses Codex config lines that would choose the model or effort.

`run.py` records deterministic checks, tokens, turns and time per run, and from the agent's tool calls (Claude Code's
transcript, Codex's command events) the skill files it opened, its `glm-delegate` calls and any task-specific trace
signals. Codex runs in the `workspace-write` sandbox, where pi cannot write its lock file and `glm-delegate` fails; to
let it work as it does under full access, pass both arms
`--codex-config $'sandbox_workspace_write.network_access = true\nsandbox_workspace_write.writable_roots = ["<home>/.pi/agent"]'`.
`--candidate-codex-config` adds lines to the candidate's Codex config only, to compare one setting, and
`--candidate-skill NAME=DIR` adds or replaces one skill in the candidate arm, such as a skill kept in another
repository.

The pace tasks (t30 to t32) run against a stand-in for the PACE-Phoenix cluster, [`fakecluster.py`](fakecluster.py),
installed in the run's workspace as `pace`, `ssh`, `scp`, `rsync` and the Slurm commands. It answers from the
task's canned cluster state and logs every call, so a check can tell whether the agent submitted anything, and
nothing reaches the real cluster: Claude Code gets the stand-in first on its PATH through `CLAUDE_ENV_FILE`, which
runs after its shell profile, and may not call the real tools by absolute path; Codex runs non-login shells, so
the profile cannot put the real `pace` first, inside a sandbox without network. Help, version and cost commands run
the real `pace`, whose own SSH calls reach the stand-in.

`judge.py` scores each run's task-specific rubric and its report with a judge from the other model family (Codex
judges Claude Code runs, Claude Code judges Codex runs), blind to the arm: workspace paths, which name the arm, are
masked in the answer it sees. It does not see the fixture's own instructions, so a rubric must state any project rule
the answer is graded against. For tasks whose rubric grades a written file or the design (`show_diff`), it also sees
the change against the fixture commit, cut at 20,000 characters. Runs use live accounts and count against their
usage. A run or judgment that hits a usage limit is marked and left out of the summary; `judge.py --missing` judges
only the runs that still lack a score, `judge.py --tasks` only the named tasks (routing tasks have no rubric), and
`run.py --recheck <run dir>` recomputes the deterministic checks and trace fields after a check is corrected.

The tasks target behaviors that standing instructions can change: answering a question without editing, finishing a
fix, stating assumptions on an ambiguous feature, preserving user work during cleanup, claim discipline on confounded
results, grounding in sources, triaging a 2.3 MB log, finishing a multi-part implementation, leaving a pinned file
alone, and two questions on the real flatpack repository. Three engineering tasks (t12 to t14) are the changes the
`engineering` skill is for: upgrading a stored SQLite schema that users already have, consolidating pricing rules that
drifted apart against a written policy, and fixing a parser bug with tests that must fail on the old code. Two
research tasks need a long horizon: a related-work summary over 48 paper notes (t15) that must cite the three
contrary results and invent no identifier, and a simulation whose energy drift must fall below a target (t16) under a
brief that records approaches already ruled out, which the trace checks for retries. Tasks t20 to t27 are routing
tests without a rubric: four research requests that should load `coresearch` and four routine coding requests that
should not. Three pace tasks prepare a GPU run that cannot start as asked (t30), diagnose a job that vanished from
the queue (t31) and fetch a smoke run whose result no longer reproduces (t32). They are a small development set,
not a benchmark: a difference on one task in one run is anecdotal.
