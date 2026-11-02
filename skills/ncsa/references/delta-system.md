# NCSA Delta — condensed system facts

Extracted from https://docs.ncsa.illinois.edu/systems/delta/en/latest/ on 2026-10-06
(current RedHat 9 documentation, not the archived `/en/rh9/` pages). Site notices
take precedence over this file.

## Access and authentication

- Login: `ssh <user>@login.delta.ncsa.illinois.edu` (round-robin; specific nodes
  `dt-login01`–`dt-login04.delta.ncsa.illinois.edu` — use a specific hostname when
  re-attaching tmux). Typical usage: `ssh delta` via the user's own SSH alias.
  Slurm login banner ≠ GPU allocation.
- Auth: NCSA (Kerberos) password, then Duo MFA — reply `1` for Duo Push or type a
  six-digit passcode. SSH key pairs are **disabled for general use** (PI exception
  via support ticket), so `ssh -o BatchMode=yes` cannot establish a session;
  authentication is a user-side manual step — the helper never collects
  credentials or MFA codes. If prompts misbehave:
  `ssh -o PreferredAuthentications=keyboard-interactive,password`.
- Login-node limits (Linux cgroups): 16 cores per user; memory caps 37G/62G by
  tier; no swap. Anything heavier belongs in a Slurm job.
- Eligibility: a Delta/ACCESS allocation (NCSA username listed in the ACCESS
  profile; `accounts` on the cluster).
- rsync/scp through the login node works but must stay small; GUI clients must
  handle the Duo prompt.

## Partitions, QoS, charging (SU per GPU-hour)

| Partition | GPUs/node | Max duration | Notes |
|---|---|---|---|
| `gpuA40x4` | 4× A40 | 48 h | 0.5 SU; `-preempt` 0.25 |
| `gpuA100x4` | 4× A100 (62.5 GB) | 48 h | default queue; 1.0 SU; `-preempt` 0.5 |
| `gpuA100x8` | 8× A100 (250 GB) | 48 h | 1.5 SU |
| `gpuH200x8` | 8× H200 (250 GB) | 48 h, max 1 node | 3.0 SU |
| `gpuMI100x8` | 8× AMD MI100 | 48 h | 0.25 SU (AMD ROCm stack) |
| `cpu` | — | 48 h | 1 core-hour ≤2 GB = 1 SU |

- Every partition also has `-interactive` (1 h walltime; **one job total, running
  or queued, per user per interactive partition**; A40/A100x4 max 4 nodes,
  A100x8 2, H200x8 1). `gpuA100x4-preempt` / `gpuA40x4-preempt`: 48 h, 10 min
  PreemptExemptTime + 5 min GraceTime on SIGTERM; use only with a verified
  checkpoint policy.
- Defaults: 1000 MB/core, 30 min walltime. No auto-requeue since 2022-12-19 (opt
  in with `--requeue`). Node sharing is default; exclusive = `--exclusive --mem=0`.
  No MIG slicing on A100.
- Billing: reserved resources, `max(cores, memory fraction)` — never observed use.
  `accounts` = balances, `jobcharge` = charge estimate, `quota` = storage.
  `QOSGrpBillingMinutes` pending reason = exhausted balance (PI files XRAS
  supplement). No per-job refunds.
- Full node ≈ 128 SU/h (CPU), 4-way GPU node ≈ 4 SU/h ... per-GPU factors above
  govern mixed jobs.

## Example submissions (verbatim from docs)

```sh
# interactive GPU (short debugging only)
srun --partition=gpuA40x4-interactive --nodes=1 --gpus-per-node=1 --tasks=1 \
  --tasks-per-node=16 --cpus-per-task=1 --mem=20g --pty bash
salloc --mem=16g --nodes=1 --ntasks-per-node=1 --cpus-per-task=2 \
  --partition=gpuA40x4-interactive,gpuA100x4-interactive \
  --account=account_name --time=00:30:00 --gpus-per-node=1

# batch, 1 GPU
sbatch --partition=gpuA40x4 --mem=50G --ntasks-per-node=1 --gpus-per-node=1 \
  --gpu-bind=closest --exclusive -t 04:00:00 job.sh

# batch, 4 GPUs
sbatch --partition=gpuA100x4 --mem=208G --nodes=1 --ntasks-per-node=4 \
  --cpus-per-task=16 --gpus-per-node=4 --gpu-bind=closest --exclusive \
  --no-requeue -t 04:00:00 job.sh
```

Set `--account`, `--time`, and memory explicitly; staggering chained jobs:
`--dependency=after:JOBID+5`.

## Filesystem dependencies (required for non-HOME I/O)

`#SBATCH --constraint="projects&work"` (submit time) or
`scontrol update job=JOBID Features="projects&work"` (while pending; verify with
`scontrol show job | grep Feature`). Labels: `projects` → /projects, `work` →
/work/hdd, `ime` (depends on /work/hdd), `taiga` (same FS as /projects). HOME (/u)
is always assumed. The "scratch" label seen in older examples is absent from the
current feature table.

## Storage

| FS | Path | Quota | Notes |
|---|---|---|---|
| HOME | `/u/<user>` | 100 GB, 750k files | daily snapshots, 30 days (`~/.snapshot/`); not for job I/O |
| PROJECTS | `/projects/<account>/<user>` | 500 GB (1–25 TB by request) | shared project data/results |
| WORK HDD | `/work/hdd/<account>/<user>` | 1 TB (1–100 TB by request) | **the current scratch volume**; job I/O target |
| WORK NVME | `/work/nvme/...` | by support ticket | many-small-file I/O |
| /tmp | node-local | 0.74 TB (CPU) / 1.5 TB (GPU) SSD | wiped after each job; copy results out before exit |

`module reset` in job scripts sets `SCRATCH`/`WORK` env vars. No archive storage
exists; expired-project data gets a 30-day grace period.

## Data transfer

- scp/rsync: small transfers only (protect the login node; Duo prompt applies).
- Globus (bulk): endpoint collections **"NCSA Delta"** and **"ACCESS Delta"**;
  shared with DeltaAI — `/work/hdd` and `/work/nvme` are visible from both, home
  dirs are not. Sharing is done from `/projects` only.

## Software stack (RH9 transition, 2025)

RedHat 9; NVIDIA driver 570.148.08; base CUDA 12.8 (`cudatoolkit/25.3_12.8`);
default PE `PrgEnv-gnu` (gcc 13.2, cray-mpich/8.1.32); `PrgEnv-nvidia`/`PrgEnv-cray`
available; MPI = cray-mpich only (OpenMPI <½ perf); `MPICH_GPU_SUPPORT_ENABLED=1`
for GPU RDMA; NCCL via `aws-ofi-nccl`; Python via miniforge; `pytorch-conda/2.8`,
`tensorflow-conda/2.18`.
