# NCSA Delta runs

Operate the user's authorized NCSA Delta allocation with `scripts/ncsa.py`
(standard-library Python plus the user's SSH alias, rsync, and remote Slurm).
Authentication is the user's own interactive Kerberos + Duo session; the helper
never collects credentials and treats a transport timeout as an unknown outcome
to be diagnosed through `status` before any retry.

## Run discipline

One root per project. All staging and results live at
`<compute_root>/<project>/runs/<id>/{stage,results}`, with shared scratch at
`<compute_root>/<project>/tmp`. The helper refuses to stage anywhere else,
including sibling or hand-made staging directories, and refuses layout paths
that are symlinks escaping the structure.

`project` is an explicit `.ncsa/config.json` field; the only automatic fallback
is the repository's git remote basename, never the local directory name (a
checkout may be `kamino` while storage is `kamino-research`). Storage roots must
resolve under `/work/hdd` or `/projects` with allocation and user components.

A run ID is a user label or a short sha (`prepare --run-id`; default HEAD short
sha); a timestamp only disambiguates a label collision, since an existing run is
never reused or overwritten. Staging writes `meta.json` (git sha, config hash,
host) into the run directory and freezes the exact staged file set, hashes, and
modes; the job re-verifies both manifest digest and files before the entry
command runs.

## Scratch

Temp files go to node-local `/tmp` or `<compute_root>/<project>/tmp`. Never
`$HOME`, never per-session stamped directories. Staged runs exclude `.git`,
credentials, environments, and weights; never change a running snapshot.

## Fetch and close-out

Fetch a named result directory only; files land at
`<repository>/<results_dir>/<run_id>/` — `results_dir` defaults to `results/`
and is `artifacts/` when the repository already uses that convention. There is
no destination override. Each fetch writes a receipt at
`<results_dir>/fetched/<run_id>.json` (run ID, remote root, manifest hash, git
sha, verified file count) and prints the exact `git add`/`commit`/`push`
commands. Close out in the same session: an unfetched or uncommitted result is
an unfinished experiment. Path parity: pace records its receipts at
`runs/fetched/<run_id>.json`, while ncsa receipts live inside the repository's
configured `results_dir` — grep the right path per cluster.

Verified hashes establish transport consistency, not scientific validity; job
exit status, provenance, and experiment gates are checked separately.

## Audit

`ncsa.py audit --config .ncsa/config.json --emit` prints a self-contained
read-only POSIX snippet classifying `/work/hdd/<account>/<user>/*` and
`/projects/<account>/<user>/*` as REGISTERED, INTERNAL, or ORPHAN with size and
mtime. Run it inside the interactive Duo session and paste the output back to
`ncsa.py audit --parse`; no non-interactive SSH is assumed. Use it before
staging new runs and after finishing with a project.
