---
name: ncsa
description: Operate NCSA Delta allocations and storage for GPU experiments, including account and queue inspection, frozen staging under one root per project, bounded Slurm submission, tracking, audited storage, and result retrieval into the repository's locked results directory. Use when the user selects NCSA Delta; do not apply PACE/Phoenix defaults or DeltaAI node recipes.
---

# NCSA Delta

Use Delta only for the user's authorized experiment. Keep torch/GPU execution on an
allocated compute node; the login banner describes a login node, not a GPU
allocation. This skill never changes SSH authentication, collects passwords or MFA
codes, grants new network permissions, or authorizes unrelated jobs.

Read [references/operations.md](references/operations.md) before staging or
submitting; [references/delta-system.md](references/delta-system.md) holds condensed
system facts with exact Slurm/storage examples. Use this skill's absolute
`scripts/ncsa.py` path for the companion helper (standard-library Python + the
user's SSH alias + rsync + remote Slurm). Read any project-specific Delta guide
before choosing an entry command (in the motion-editing repository:
`skills/ncsa/references/motion-preserve.md`, separate from this skill).

## Run discipline

- One root per project. All staging and results live at
  `<compute_root>/<project>/runs/<id>/{stage,results}` plus
  `<compute_root>/<project>/tmp` for shared scratch. The helper refuses to
  stage anywhere else, including sibling or hand-made staging directories.
- `project` is an explicit `.ncsa/config.json` field; the only automatic
  fallback is the repository's git remote basename. The local directory name
  is never used (a checkout may be `kamino` while storage is `kamino-research`).
- Run IDs are a user label or a short sha (`prepare --run-id`, default HEAD
  short sha); a timestamp is only a disambiguator for label collisions. Staging
  writes `meta.json` (git sha, config hash, host) into the run directory.
- Scratch goes to node-local `/tmp` or `<compute_root>/<project>/tmp`. Never
  `$HOME`, never per-session stamped directories.
- Results are fetched only into the repository's locked `results_dir`
  (`results/` by default, `artifacts/` when the repository already uses that
  convention), never to a per-fetch destination, and each fetch writes a
  receipt under `<results_dir>/fetched/<run_id>.json`.
- Close out in the same session: after a fetch, commit the fetched results
  plus receipt and push. The helper prints the exact git commands.

## Connect

- Start with `python3 <skill>/scripts/ncsa.py doctor --host delta` (read-only).
- Auth is the user's own SSH alias with NCSA Kerberos password + Duo MFA; the
  server offers no publickey auth. If `BatchMode` fails, report the
  transport/authentication failure and ask the user to authenticate in their own
  terminal. Never collect passwords/MFA codes, alter SSH controls, or use another
  process to evade a permission restriction.
- No session, no guessed hosts/accounts/allocations. Use the exact GPU allocation
  returned by `accounts`; check `quota`/`jobcharge`. Delta has no assumed free tier.

## System facts (live docs, RH9 era)

- Slurm partitions (SU per GPU-hour): `gpuA40x4` 0.5, `gpuA100x4` 1.0,
  `gpuA100x8` 1.5, `gpuH200x8` 3.0 (max 1 node), `gpuMI100x8` 0.25, plus `cpu`.
  `-interactive` variants: 1 hr max and only ONE job (running or queued) per user
  per interactive partition. Non-interactive max 48 hr. Defaults 1000 MB/core,
  30 min; no auto-requeue.
- Filesystem dependencies (`--constraint=`): `projects` (/projects), `work`
  (/work/hdd), `ime`, `taiga`; HOME (/u) always assumed. Docs contain stale
  `/scratch` examples — the feature table has no `scratch` label; do not invent an
  alias or assume `$HOME/scratch`.
- Storage: `/projects/<account>/<user>` (500 GB base), `/work/hdd/<account>/<user>`
  (1 TB base — this is the current scratch volume), node-local `/tmp` (wiped after
  each job). None is a backup: keep hashes and an independent recovery copy.
- Billing is on reserved resources (cores vs memory, whichever is larger), not
  observed use. `QOSGrpBillingMinutes` in squeue means exhausted balance.
- Prefer a normal batch partition over interactive for unattended batches; follow
  the newest live site notice.

## Execute and verify

1. Freeze code, sources, requests, seed, limits, and environment recipe per run.
   Stage only selected files: no credentials, `.env`, SSH/AWS config, key files,
   environments, weights, or `.git`. Never change a running snapshot.
2. Start with a small single-GPU job; explicitly request CPU, memory, wall time,
   account, and filesystem dependencies. Avoid whole-node exclusivity unless needed.
   Capture actual modules, packages, GPU, and job identity.
3. Treat an SSH/submission timeout as an unknown outcome: query both `squeue` and
   `sacct` with the unique job name/ID before retrying. The helper preserves the
   attempt record and remote lock; it does not auto-resubmit. Never cancel the
   user's other jobs to make room.
4. Fetch named result directories only, into the repository's locked
   `results_dir`. Check hashes, job exit status, model provenance, and
   experiment gates separately — a successful upload or CPU test is not a
   successful GPU experiment. Preserve failures and rejected candidates, then
   commit and push the fetched results and receipt in the same session.
5. Diagnose before retrying; stop after three repetitions of the same failure.
   Resume a preempted batch only with a verified resume boundary or an explicitly
   accounted new run.

## Audit storage

`ncsa.py audit --config .ncsa/config.json --emit` prints a self-contained POSIX
shell snippet. The user runs it inside their own interactive Kerberos+Duo Delta
session and pastes the full output back to `ncsa.py audit --parse`; the helper
then summarizes each top-level entry of `/work/hdd/<account>/<user>` and
`/projects/<account>/<user>` as REGISTERED (matches a configured project root),
INTERNAL (inside one), or ORPHAN, with size and mtime. The helper never assumes
non-interactive SSH for this, and the snippet is read-only.

The helper's hashes establish consistency of captured files, not remote
attestation, model quality, or cross-machine determinism. Keep prepared,
submitted, executed, and independently verified evidence distinct.
