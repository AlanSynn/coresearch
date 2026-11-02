## Configuration and preflight

Use the current [Delta RH9 guide](https://docs.ncsa.illinois.edu/systems/delta/en/latest/),
not the archived `/en/rh9/` pages. Site examples can be stale; runtime evidence and
the user's newer notice take precedence.

Run from the target project root. The examples show a repository-local skill
copy; for an installed skill, use its absolute helper and example-config paths
from the skill catalog instead. `prepare --source .` always refers to the target
project, not to the skill's directory.

First run the skill's helper without a configuration:

```sh
python3 skills/ncsa/scripts/ncsa.py doctor --host delta
```

It reads the account, queue, partitions, module environment and system identity.
It neither allocates nor writes remotely. It cannot authenticate a new MFA session;
the user manages authentication in their own terminal.

Create a private configuration from `config.example.json`. Fill account and
resolved storage roots from live evidence; the empty example intentionally fails
before any allocation. `compute_root` and `data_root` are dedicated directories
within the user's allocation storage. They must resolve under `/work/hdd` or
`/projects`, with allocation and user subdirectories. Inspect aliases before using
them. The helper refuses other filesystem mappings pending live verification.
Roots are not the filesystem's
top-level shared directory. Configure a verified bootstrap Python separately in
the project worker's environment settings.

```sh
mkdir -p .ncsa
cp skills/ncsa/references/config.example.json .ncsa/config.json
python3 skills/ncsa/scripts/ncsa.py doctor --config .ncsa/config.json \
  --out .ncsa/preflight.json
```

The example uses one GPU, four CPU cores, 16 GB and 30 minutes. Those are bounded
initial requests, not statements about the user's allocation. Check `accounts`,
`quota` and `jobcharge` as applicable. [Accounting](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/job_accounting.html)
can charge CPU/memory reservations as well as GPUs. Do not infer a free queue or
use a CPU allocation for a GPU job.

The current filesystem feature table maps `/projects` to `projects` and
`/work/hdd` to `work`; use both if the job uses both. Other storage requires a
live-verified feature mapping. [Job dependencies](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/running_jobs.html#file-system-dependency-specification-for-jobs)
are part of submission. [Storage documentation](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/data_mgmt.html)
has conflicting WORK/SCRATCH examples. Shared free space is not remaining quota.
Neither project/work storage nor node-local `/tmp` is a backup; retain source
hashes and a recovery copy outside the running job.

The helper permits at most 120 minutes for a normal NVIDIA batch partition and
60 minutes for an interactive partition, with the existing one-GPU, sixteen-CPU
and 32-GB bounds. A longer supported batch still needs a verified live partition,
explicit configuration, frozen inputs and one recorded submission.

## Frozen execution

`prepare` copies only explicitly included relative files/directories into a new
local run and writes byte hashes and permissions. It rejects symlinks and traversal,
excludes `.env`/`.env.*`, SSH/AWS configuration, key files, environments, weights
and Git metadata, and quotes
the executable arguments and permitted environment values. Place `--entry` last.
Use `bash` explicitly for a shell entry when appropriate. Include every imported
project dependency, not the entire workspace.

```sh
python3 skills/ncsa/scripts/ncsa.py prepare \
  --config .ncsa/config.json --source . \
  --include scripts --include src \
  --out .ncsa/runs/first-check \
  --entry bash scripts/my_gpu_job.sh
python3 skills/ncsa/scripts/ncsa.py stage --run .ncsa/runs/first-check
python3 skills/ncsa/scripts/ncsa.py submit --run .ncsa/runs/first-check
python3 skills/ncsa/scripts/ncsa.py status --run .ncsa/runs/first-check
```

`my_gpu_job.sh` is the user's actual prepared entry; the generic skill supplies no
such job. Read the project's worker guide for its concrete command. `stage` creates
a new remote run, performs read-only preflight, uploads without deletion, and checks
the exact staged file set, hashes and modes. `submit` repeats both integrity
verification and preflight before one bounded `sbatch` call. Slurm captures the
manifest digest with the batch script; the job checks that digest and all files
again before starting the entry command. Queued-time changes are refused. The
submission child also receives that digest explicitly, because inherited values
take precedence with [Slurm's `--export=ALL`](https://slurm.schedmd.com/sbatch.html#OPT_export).
The helper supports NVIDIA batch and interactive partitions; it intentionally
excludes preemptible submission until a project has a verified checkpoint policy.
There is no automatic allocation in staging or the model client.

## Unknown outcomes, recovery and retrieval

The local `submission-attempt.json` is created before transport, and the remote
submission lock before `sbatch`. A failure can therefore leave an unknown outcome.
`status` looks for this unique run in both `squeue` and `sacct`, and reads any remote
job receipt. A missing queue row alone is insufficient: the job may have finished.
An accounting-query error is also not evidence of absence. Never clear a lock or
prepare a duplicate submission simply because the SSH client timed out.

For an authoritative non-submission or terminal failure, diagnose first and
prepare a new run with the correction and prior attempt recorded. For a partially
completed batch, use the project's explicit hash-checked resume mechanism; do not
overwrite accepted raw results. The helper provides no cancellation command.

Fetch a named output path into a fresh local directory:

```sh
python3 skills/ncsa/scripts/ncsa.py fetch --run .ncsa/runs/first-check \
  --relative artifacts/results/first-check --out artifacts/received/first-check
```

This path must name actual results in the staged repository. For a worker writing
to configured project data storage, pass `--storage data --relative results/<run>`;
data-root retrieval is restricted to named `results/` directories. The helper compares
the exact fetched file set, hashes and modes with a remote inventory. Symlinks,
including a named result directory pointing elsewhere, and changed files fail
verification.
It does not judge scientific validity. Avoid syncing environments, weights or the
whole work tree.

Large result directories can take more than the default 120 seconds to enumerate
and hash remotely. Only `fetch` accepts `--inventory-timeout-seconds`, bounded to
1..600 seconds. This changes the read-only inventory deadline; it does not change
SSH authentication, submission/status/staging deadlines, inventories, hashes,
modes or unknown-outcome handling. Preserve timed-out attempts and diagnose them
before retrying the same named directory with a suitable bounded deadline.
