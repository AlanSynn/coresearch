---
name: ncsa
description: Operate NCSA Delta allocations and storage for GPU experiments, including account and queue inspection, frozen staging, bounded Slurm submission, tracking, and targeted result retrieval. Use when the user selects NCSA Delta; do not apply PACE/Phoenix defaults or DeltaAI node recipes.
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
4. Fetch named result directories only. Check hashes, job exit status, model
   provenance, and experiment gates separately — a successful upload or CPU test
   is not a successful GPU experiment. Preserve failures and rejected candidates.
5. Diagnose before retrying; stop after three repetitions of the same failure.
   Resume a preempted batch only with a verified resume boundary or an explicitly
   accounted new run.

The helper's hashes establish consistency of captured files, not remote
attestation, model quality, or cross-machine determinism. Keep prepared,
submitted, executed, and independently verified evidence distinct.
