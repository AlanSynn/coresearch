#!/usr/bin/env python3
"""Inspect Delta, freeze selected files, stage one run and submit it once.

Uses stdlib Python, SSH/rsync, and remote Slurm. Never runs a GPU locally,
allocates in doctor/prepare/stage, or cancels jobs. Configuration is private.

Run discipline: one root per project. All staging and results live at
<compute_root>/<project>/runs/<id>/{stage,results} plus
<compute_root>/<project>/tmp for shared scratch; anything outside that
structure is refused. Results are fetched only into the user's repository
under its configured results_dir, and each fetch writes a receipt there.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys

SKIP_PARTS = {".git", ".ncsa", ".pace", ".aws", ".ssh", ".codex", ".venv", "node_modules", "__pycache__"}
SKIP_FILES = {".env", ".DS_Store"}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".keystore"}
PARTITIONS = {"gpuA40x4", "gpuA100x4", "gpuA100x8", "gpuH200x8"}
PARTITIONS |= {name + "-interactive" for name in tuple(PARTITIONS)}
# Run IDs are user labels or short shas; a timestamp is only a disambiguator.
# Keep this pattern in sync with the literal copy inside RUN_LAYOUT below.
RUN_ID_RE = r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}"
BASE_CONFIG_KEYS = {"host", "account", "compute_root", "data_root", "filesystem_dependencies",
                    "partition", "minutes", "cpus", "memory_gb", "environment"}
OPTIONAL_CONFIG_KEYS = {"project", "results_dir"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_new(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or any(part in {".", ".."} for part in value.split("/"))
            or not re.fullmatch(r"[A-Za-z0-9_./-]+", value)):
        raise ValueError("use an explicit relative path without spaces, dot traversal or shell syntax")
    return path.as_posix()


def validate_config(data: dict, *, project_default: str | None = None,
                    results_default: str = "results") -> dict:
    unknown = set(data) - BASE_CONFIG_KEYS - OPTIONAL_CONFIG_KEYS
    if unknown:
        raise ValueError("unknown config keys: " + ", ".join(sorted(unknown)))
    missing = BASE_CONFIG_KEYS - set(data)
    if missing:
        raise ValueError("config keys must include: " + ", ".join(sorted(missing)))
    for key in ("host", "account"):
        if not isinstance(data[key], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", data[key]):
            raise ValueError(f"fill a verified {key}; use an SSH alias, not embedded credentials")
    for key in ("compute_root", "data_root"):
        value = data[key]
        if (not isinstance(value, str) or not re.fullmatch(r"/[A-Za-z0-9_./-]+", value)
                or ".." in value.split("/") or len(PurePosixPath(value).parts) < 4
                or value.startswith(("/u/", "/home/", "/tmp/"))):
            raise ValueError(f"fill verified allocation storage for {key}; no HOME or node-local /tmp")
        data[key] = value.rstrip("/")
    # One root per project: runs live at <compute_root>/<project>/runs/<id>,
    # shared scratch at <compute_root>/<project>/tmp. The project is an
    # explicit config field; the git remote basename is the only fallback.
    # The local directory name is never used.
    if "project" not in data:
        if not project_default:
            raise ValueError("add an explicit project field to .ncsa/config.json "
                             "(the git remote basename of this repository; the local directory name is never used)")
        data["project"] = project_default
    if not isinstance(data["project"], str) or not re.fullmatch(RUN_ID_RE, data["project"]):
        raise ValueError("project must be a short safe name (the git remote basename or an explicit field)")
    if "results_dir" not in data:
        data["results_dir"] = results_default
    # Fetched results land only inside the repository's results_dir.
    if (not isinstance(data["results_dir"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", data["results_dir"])):
        raise ValueError("results_dir must be one safe directory name inside the repository (default 'results')")
    deps = data["filesystem_dependencies"]
    if (not isinstance(deps, list) or not deps or len(set(deps)) != len(deps)
            or any(not isinstance(x, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", x) for x in deps)):
        raise ValueError("filesystem_dependencies must list verified Slurm filesystem features")
    if data["partition"] not in PARTITIONS:
        raise ValueError("select a live NVIDIA Delta batch/interactive partition; preemption needs a separate resume policy")
    max_minutes = 60 if data["partition"].endswith("-interactive") else 120
    for key, low, high in (("minutes", 1, max_minutes), ("cpus", 1, 16), ("memory_gb", 1, 32)):
        if type(data[key]) is not int or not low <= data[key] <= high:
            raise ValueError(f"{key} must be {low}..{high} for this bounded one-GPU helper")
    if not isinstance(data["environment"], dict):
        raise ValueError("environment must be a string dictionary")
    for key, value in data["environment"].items():
        if (not re.fullmatch(r"(?:NCSA|BASELINE)_[A-Z0-9_]+", key) or not isinstance(value, str)
                or any(c in value for c in "\x00\r\n")):
            raise ValueError("environment accepts only NCSA_/BASELINE_ string values without control characters")
    if any(key in data["environment"] for key in
           ("NCSA_COMPUTE_ROOT", "NCSA_DATA_ROOT", "NCSA_FROZEN_MANIFEST_SHA256")):
        raise ValueError("storage roots and the frozen-manifest digest have dedicated fields")
    return data


def config(path: Path) -> dict:
    return validate_config(json.loads(path.read_text()))


def git_output(source: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(source), *args],
                                text=True, capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def git_remote_project(source: Path) -> str | None:
    # The only automatic project name is the git remote basename, never the
    # local directory name (e.g. a checkout dir may be "kamino" while the
    # storage project is "kamino-research").
    url = git_output(source, "remote", "get-url", "origin")
    if not url:
        return None
    tail = re.split(r"[/:]", url.rstrip("/"))[-1]
    name = re.sub(r"\.git$", "", tail)
    return name if name and re.fullmatch(RUN_ID_RE, name) else None


def git_head_sha(source: Path) -> str | None:
    sha_value = git_output(source, "rev-parse", "HEAD")
    return sha_value if sha_value and re.fullmatch(r"[a-f0-9]{40}", sha_value) else None


# The same verifier runs locally, after staging, before submission and at job
# start. Slurm captures the manifest digest with the copied batch script, so a
# queued-time change to either the repository or its manifest fails the gate.
SNAPSHOT_CHECK = r'''
def verify_snapshot(repo, records):
    import hashlib, os, pathlib, re, stat
    repo=pathlib.Path(repo)
    if repo.is_symlink() or not repo.is_dir(): raise ValueError('invalid frozen repository')
    expected={}
    for item in records:
        name=item['path']
        if (not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_./-]+',name)
                or name.startswith('/') or any(x in {'','.','..'} for x in name.split('/'))):
            raise ValueError('invalid frozen input path')
        if name in expected: raise ValueError('duplicate frozen input: '+name)
        expected[name]=item
    actual=set()
    for base, directories, files in os.walk(repo,followlinks=False):
        for name in directories+files:
            path=pathlib.Path(base)/name
            mode=path.lstat().st_mode
            if stat.S_ISLNK(mode): raise ValueError('frozen repository contains a symlink: '+str(path))
            if stat.S_ISREG(mode): actual.add(path.relative_to(repo).as_posix())
            elif not stat.S_ISDIR(mode): raise ValueError('frozen repository contains a special file: '+str(path))
    if actual!=set(expected):
        raise ValueError('frozen file set changed; extra='+str(sorted(actual-set(expected)))
                         +'; missing='+str(sorted(set(expected)-actual)))
    for name,item in expected.items():
        path=repo/name; data=path.read_bytes()
        if (len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']
                or (path.stat().st_mode & 0o777)!=item['mode']):
            raise ValueError('frozen input changed: '+name)
'''
exec(SNAPSHOT_CHECK)

# The run-layout rule is injected into the remote program (REMOTE) and also
# executed locally, so staging and every local caller derive paths from one
# implementation. Keep the RUN_ID_RE literal in sync with the module constant.
RUN_LAYOUT = r'''
def run_layout(cfg, run_id):
    import pathlib, re
    if not isinstance(run_id, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', run_id):
        raise ValueError('invalid run ID: use a short label or a short sha; a timestamp is only a disambiguator')
    project = cfg.get('project') if isinstance(cfg, dict) else None
    if not isinstance(project, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', project):
        raise ValueError('invalid project name in configuration')
    compute = pathlib.Path(cfg['compute_root'])
    if not compute.is_absolute():
        raise ValueError('compute_root must be absolute')
    base = compute / project
    root = base / 'runs' / run_id
    return base, root, base / 'tmp'

def ensure_run_layout(cfg, run_id):
    # Staging refuses anything outside <compute_root>/<project>/runs/<id>.
    # The allocation base may legitimately sit behind system-level symlinks
    # (e.g. /tmp), so it is resolved once; nothing inside the project
    # structure may link elsewhere, and an existing run is never reused.
    import pathlib
    _, _, _ = run_layout(cfg, run_id)
    base = pathlib.Path(pathlib.Path(cfg['compute_root']).resolve() / cfg['project'])
    runs = base / 'runs'
    tmp = base / 'tmp'
    for path in (runs, tmp):
        if path.is_symlink():
            raise ValueError('run layout path escapes the declared run structure: ' + str(path))
    base.mkdir(parents=True, exist_ok=True)
    runs.mkdir(exist_ok=True)
    tmp.mkdir(exist_ok=True)
    for path in (runs, tmp):
        if path.resolve() != path:
            raise ValueError('run layout path escapes the declared run structure: ' + str(path))
    root = runs / run_id
    root.mkdir(exist_ok=False)
    (root / 'stage').mkdir()
    (root / 'results').mkdir()
    (root / 'logs').mkdir()
    if root.resolve() != root:
        raise ValueError('run root resolved outside the declared run structure: ' + str(root))
    return base, root, tmp

def write_meta(root, meta):
    import json, pathlib
    path = pathlib.Path(root) / 'meta.json'
    with path.open('x') as stream:
        json.dump(meta, stream, indent=2)
        stream.write('\n')
    return path
'''

exec(RUN_LAYOUT)


def manifest_digest(manifest: dict) -> str:
    return sha(json.dumps(manifest, sort_keys=True, separators=(",", ":"), allow_nan=False).encode())


# JSON is passed on stdin. Request data is never interpolated into Python code.
# Only validated run IDs and explicit verified project roots can be mutated.
REMOTE = SNAPSHOT_CHECK + RUN_LAYOUT + r'''
import getpass, hashlib, json, os, pathlib, re, shutil, subprocess, sys
from datetime import datetime
p=json.load(sys.stdin)
def accounting_start_date(created_at_utc):
    # sacct parses a date in the remote process's local timezone. Slicing the
    # UTC stamp can select tomorrow while Delta is still on the preceding day.
    created=datetime.fromisoformat(created_at_utc.replace('Z','+00:00'))
    if created.utcoffset() is None:
        raise ValueError('created_at_utc must include a timezone offset')
    return created.astimezone().date().isoformat()
def call(args,env=None):
    try:
        r=subprocess.run(args,text=True,capture_output=True,timeout=25,env=env)
        return {'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    except (OSError,subprocess.TimeoutExpired) as exc:
        return {'returncode':-1,'stdout':'','stderr':str(exc)}
def need(args,env=None):
    r=call(args,env=env)
    if r['returncode']: raise RuntimeError(r['stderr'] or r['stdout'] or str(args))
    return r['stdout']
def store(path,value):
    with path.open('x') as f: json.dump(value,f,indent=2); f.write('\n')
def inspect(cfg=None):
    user=getpass.getuser()
    result={'hostname':os.uname().nodename,'machine':os.uname().machine,'user':user,
        'python':sys.version,'environment':{k:os.environ.get(k) for k in ('WORK','SCRATCH','SLURM_JOB_ID')},
        'accounts':call(['accounts']),
        'partitions':call(['sinfo','-h','-o','%P|%a|%l|%G']),
        'queue':call(['squeue','-h','-u',user,'-o','%i|%P|%j|%T|%R']),
        'modules':call(['bash','-lc','module list 2>&1']),
        'module_environment':call(['bash','-lc','module reset >/dev/null 2>&1 && printf "WORK=%s\\nSCRATCH=%s\\n" "$WORK" "$SCRATCH"'])}
    if cfg:
        roots={}
        for key in ('compute_root','data_root'):
            path=pathlib.Path(cfg[key]).resolve()
            ancestor=path
            while not ancestor.exists(): ancestor=ancestor.parent
            if (not (str(path).startswith('/projects/') and len(path.parts)>=4)
                    and not (str(path).startswith('/work/hdd/') and len(path.parts)>=5)):
                raise ValueError('storage must resolve under verified /projects/<allocation>/<user> or /work/hdd/<allocation>/<user>; unknown filesystem mappings are refused')
            stat=os.statvfs(ancestor)
            roots[key]={'canonical_path':str(path),'existing_ancestor':str(ancestor),
                'writable':os.access(ancestor,os.W_OK),'filesystem_free_bytes':stat.f_bavail*stat.f_frsize,
                'quota':call(['lfs','quota','-u',user,str(ancestor)])}
        result['storage']=roots
        result['selected_partition']=call(['scontrol','show','partition',cfg['partition']])
    return result
def preflight(cfg):
    report=inspect(cfg)
    for name in ('accounts','partitions','queue','selected_partition'):
        if report[name]['returncode']: raise RuntimeError('preflight failed: '+name+': '+report[name]['stderr'])
    if cfg['account'] not in report['accounts']['stdout'].split():
        raise ValueError('selected account is not an exact token in current accounts output')
    available=[row.split('|') for row in report['partitions']['stdout'].splitlines() if '|' in row]
    if not any(row[0].rstrip('*')==cfg['partition'] and row[1]=='up' for row in available):
        raise ValueError('selected partition is absent or not up')
    if any(not info['writable'] for info in report['storage'].values()): raise ValueError('storage is not writable')
    dependencies=set(cfg['filesystem_dependencies'])
    for info in report['storage'].values():
        canonical=info.get('canonical_path','')
        required='projects' if canonical.startswith('/projects/') else 'work' if canonical.startswith('/work/hdd/') else None
        if required is None: raise ValueError('unverified storage filesystem mapping')
        if required not in dependencies:
            raise ValueError('configured filesystem dependencies omit '+required)
    if cfg['partition'].endswith('-interactive'):
        for row in report['queue']['stdout'].splitlines():
            fields=row.split('|')
            if len(fields)>1 and cfg['partition'] in fields[1].split(','):
                raise RuntimeError('one pending-or-running job already occupies this interactive partition')
    return report
action=p['action']
if action=='doctor':
    print(json.dumps(inspect(p.get('config')))); sys.exit(0)
m=p['manifest']; cfg=m['config']; run=m['run_id']
project_base,root,tmp_root=run_layout(cfg,run)
stage_dir=root/'stage'
if action=='stage_init':
    report=preflight(cfg)
    for info in report['storage'].values():
        pathlib.Path(info['canonical_path']).mkdir(parents=True,exist_ok=True)
    project_base,root,tmp_root=ensure_run_layout(cfg,run)
    stage_dir=root/'stage'
    meta={'run_id':run,'git_sha':m.get('git_sha'),
        'config_sha256':hashlib.sha256(json.dumps(cfg,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'host':cfg['host']}
    write_meta(root,meta)
    store(root/'stage-preflight.json',report)
    print(json.dumps({'remote_root':str(root),'remote_stage':str(stage_dir),
        'remote_results':str(root/'results'),'tmp_root':str(tmp_root),'meta':meta,
        'preflight':report})); sys.exit(0)
if not root.is_dir(): raise RuntimeError('run was not staged')
if action=='verify_stage':
    verify_snapshot(stage_dir,m['files'])
    store(root/'manifest.json',m)
    print(json.dumps({'verified_files':len(m['files'])})); sys.exit(0)
saved=json.loads((root/'manifest.json').read_text())
if saved!=m: raise ValueError('remote run manifest changed')
name='ncsa-'+run
if action=='submit':
    lock=root/'submission.lock'; lock.mkdir(exist_ok=False)
    verify_snapshot(stage_dir,m['files'])
    report=preflight(cfg); store(root/'submit-preflight.json',report)
    if name in need(['squeue','-h','-u',getpass.getuser(),'-o','%j']).split():
        raise RuntimeError('this unique run already has an active job')
    command=['sbatch','--parsable','--account='+cfg['account'],'--partition='+cfg['partition'],
        '--job-name='+name,'--nodes=1','--ntasks=1','--cpus-per-task='+str(cfg['cpus']),
        '--gpus-per-node=1','--mem='+str(cfg['memory_gb'])+'G','--time='+str(cfg['minutes']),
        '--constraint='+'&'.join(cfg['filesystem_dependencies']),'--no-requeue',
        '--export=ALL,NCSA_FROZEN_MANIFEST_SHA256='+hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest(),
        '--chdir='+str(stage_dir),'--output='+str(root/'logs/%j.out'),'--error='+str(root/'logs/%j.err'),
        str(stage_dir/'ncsa-job.sh')]
    # With --export=ALL, Slurm gives an inherited value precedence over the
    # explicit CLI value. Set this private variable in the child environment too.
    submit_environment=dict(os.environ)
    submit_environment['NCSA_FROZEN_MANIFEST_SHA256']=hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    job=need(command,env=submit_environment).strip().split(';')[0]
    if not job.isdecimal(): raise RuntimeError('sbatch returned an unrecognized job ID')
    receipt={'job_id':job,'job_name':name,'command':command}
    store(root/'submission.json',receipt)
    print(json.dumps(receipt)); sys.exit(0)
if action=='status':
    receipt=root/'submission.json'
    result={'submission':json.loads(receipt.read_text()) if receipt.exists() else None,
        'remote_submission_lock':(root/'submission.lock').exists(),
        'queue':call(['squeue','-h','-u',getpass.getuser(),'--name',name,'-o','%i|%P|%j|%T|%R']),
        'accounting':call(['sacct','-n','-P','--allocations','--name',name,'--starttime',accounting_start_date(m['created_at_utc']),
            '--format=JobIDRaw,JobName%64,State,ExitCode,Elapsed,AllocTRES%128'])}
    print(json.dumps(result)); sys.exit(0)
if action=='inventory':
    relative=p['relative']
    if p.get('storage')=='data':
        base=pathlib.Path(cfg['data_root']).resolve()
        if not relative.startswith('results/'):
            raise ValueError('data storage retrieval is restricted to named results directories')
    else:
        base=root/'results'
    if (pathlib.PurePosixPath(relative).is_absolute()
    if (pathlib.PurePosixPath(relative).is_absolute()
            or any(part in {'','.','..'} for part in relative.split('/'))):
        raise ValueError('retrieve an explicit relative result path')
    requested=base
    for part in relative.split('/'):
        requested=requested/part
        if requested.is_symlink(): raise ValueError('result symlinks are not fetched')
    requested=requested.resolve()
    if requested==base or not requested.is_relative_to(base): raise ValueError('retrieve a named result path only')
    if not requested.exists(): raise FileNotFoundError(relative)
    files=sorted(requested.rglob('*')) if requested.is_dir() else [requested]
    records=[]
    for path in files:
        if path.is_symlink(): raise ValueError('result symlinks are not fetched')
        if path.is_file():
            data=path.read_bytes(); records.append({'path':str(path.relative_to(base)),
                'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'mode':path.stat().st_mode & 0o777})
    print(json.dumps({'files':records,'remote_base':str(base)})); sys.exit(0)
raise ValueError('unknown operation')
'''


def rpc(host: str, action: str, *, inventory_timeout_seconds: int = 120, **payload) -> dict:
    # A large read-only result inventory may exceed the ordinary SSH budget.
    # Submission/status/staging keep their original unknown-outcome deadline.
    if (type(inventory_timeout_seconds) is not int or not 1 <= inventory_timeout_seconds <= 600
            or (action != "inventory" and inventory_timeout_seconds != 120)):
        raise ValueError("only a read-only inventory may select a bounded 1..600-second timeout")
    try:
        result = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host,
                                 "python3 -c " + shlex.quote(REMOTE)],
                                input=json.dumps({"action": action, **payload}, allow_nan=False),
                                text=True, capture_output=True, timeout=inventory_timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("SSH outcome is unknown; inspect this run before retrying") from exc
    if result.returncode:
        raise RuntimeError("Delta operation failed: " + result.stderr[-3000:])
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Delta returned non-JSON output; do not infer operation success") from exc


def prepare(args) -> dict:
    source = args.source.resolve()
    cfg = validate_config(
        json.loads(args.config.read_text()),
        project_default=git_remote_project(source),
        results_default="artifacts" if (source / "artifacts").is_dir() else "results")
    if args.run_id is not None and (not isinstance(args.run_id, str) or not re.fullmatch(RUN_ID_RE, args.run_id)):
        raise ValueError("invalid --run-id: use a short label or a short sha; a timestamp is only a disambiguator")
    head_sha = git_head_sha(source)
    run_id = args.run_id or (head_sha[:12] if head_sha else None)
    if args.out.exists():
        raise FileExistsError("choose a new private output directory; frozen runs are never overwritten")
    if not args.entry or any(any(c in word for c in "\x00\r\n") for word in args.entry):
        raise ValueError("provide --entry followed by the executable and its arguments")
    selected = set()
    for name in args.include:
        relative = relative_path(name)
        location = source / relative
        if not location.exists():
            raise FileNotFoundError(relative)
        if location.is_symlink() or not location.resolve().is_relative_to(source):
            raise ValueError("included path escaped the source or is a symlink: " + relative)
        for path in ([location] if location.is_file() else location.rglob("*")):
            rel = path.relative_to(source)
            if (any(part in SKIP_PARTS or part == '.env' or part.startswith('.env.') for part in rel.parts)
                    or path.name in SKIP_FILES
                    or path.name.startswith('.env.') or path.suffix.lower() in PRIVATE_SUFFIXES):
                continue
            if path.is_symlink():
                raise ValueError("source symlinks are not staged: " + str(rel))
            if not path.is_file():
                continue
            if not path.resolve().is_relative_to(source):
                raise ValueError("source file escaped the project: " + str(rel))
            if path.suffix in {".pt", ".pth", ".ckpt", ".pyc"}:
                continue
            relative_path(rel.as_posix())
            selected.add(path)
    if not selected:
        raise ValueError("no selected source files")
    if source / "ncsa-job.sh" in selected:
        raise ValueError("ncsa-job.sh is reserved for the generated batch entry")
    if not run_id:
        run_id = sha(json.dumps(sorted(record["path"] + record["sha256"] for record in records),
                                sort_keys=True).encode())[:12]
    _, remote_run_root, tmp_root = run_layout(cfg, run_id)
    args.out.mkdir(parents=True)
    # The local run mirrors the remote layout: the frozen copy lives in stage/.
    destination = args.out / "stage"
    records = []
    for path in sorted(selected):
        relative = path.relative_to(source)
        data = path.read_bytes()
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        mode = path.stat().st_mode & 0o777
        target.chmod(mode)
        records.append({"path": relative.as_posix(), "sha256": sha(data), "bytes": len(data), "mode": mode})
    body = ["#!/usr/bin/env bash", "set -euo pipefail",
            ': "${SLURM_JOB_ID:?Run through the staged Slurm allocation}"',
            ': "${NCSA_FROZEN_MANIFEST_SHA256:?Submit with the frozen manifest digest}"',
            "python3 -I -B - <<'NCSA_VERIFY_INPUTS'",
            "import hashlib, json, os, pathlib",
            SNAPSHOT_CHECK,
            "manifest=json.loads((pathlib.Path.cwd().parent/'manifest.json').read_text())",
            "digest=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()",
            "if digest!=os.environ['NCSA_FROZEN_MANIFEST_SHA256']: raise ValueError('frozen manifest changed after submission')",
            "verify_snapshot(pathlib.Path.cwd(),manifest['files'])",
            "NCSA_VERIFY_INPUTS",
            "export NCSA_COMPUTE_ROOT=" + shlex.quote(cfg["compute_root"]),
            "export NCSA_DATA_ROOT=" + shlex.quote(cfg["data_root"]),
            "export NCSA_RUN_ROOT=" + shlex.quote(str(remote_run_root)),
            "export NCSA_RESULTS=" + shlex.quote(str(remote_run_root / "results")),
            "export NCSA_TMP_ROOT=" + shlex.quote(str(tmp_root)),
            "# Scratch is node-local /tmp or the shared NCSA_TMP_ROOT directory;",
            "# never $HOME and never a per-session stamped directory.",
            'mkdir -p "$NCSA_TMP_ROOT"',
            'export TMPDIR="${TMPDIR:-/tmp}"']
    body.extend("export " + key + "=" + shlex.quote(value) for key, value in sorted(cfg["environment"].items()))
    body.append("exec srun --ntasks=1 " + shlex.join(args.entry))
    script = ("\n".join(body) + "\n").encode()
    (destination / "ncsa-job.sh").write_bytes(script)
    records.append({"path": "ncsa-job.sh", "sha256": sha(script), "bytes": len(script),
                    "mode": (destination / "ncsa-job.sh").stat().st_mode & 0o777})
    manifest = {"schema_version": 3, "created_at_utc": stamp(), "run_id": run_id,
                "git_sha": head_sha, "status": "prepared; not staged or submitted", "config": cfg,
                "entry": args.entry, "gpu_count": 1, "files": records,
                "helper_sha256": sha(Path(__file__).read_bytes()), "remote_execution_verified": False}
    write_new(args.out / "manifest.json", manifest)
    return {"run": str(args.out), "run_id": manifest["run_id"], "files": len(records),
            "one_gpu_wall_minutes": cfg["minutes"], "partition": cfg["partition"],
            "note": "Prepared only. Inspect current allocation balance, quotas and charges before staging/submission."}


def load_run(path: Path) -> dict:
    manifest = json.loads((path / "manifest.json").read_text())
    if not isinstance(manifest.get("run_id"), str) or not re.fullmatch(RUN_ID_RE, manifest["run_id"]):
        raise ValueError("invalid run ID")
    if manifest.get("schema_version") != 3:
        raise ValueError("prepare a new run with the current run layout and job-start integrity gate")
    validate_config(manifest["config"])
    verify_snapshot(path / "stage", manifest["files"])
    return manifest


def stage(args, manifest: dict) -> dict:
    if (args.run / "stage-attempt.json").exists():
        raise RuntimeError("stage was already attempted; inspect it rather than overwrite the remote snapshot")
    write_new(args.run / "stage-attempt.json", {"started_at_utc": stamp()})
    host = manifest["config"]["host"]
    initialized = rpc(host, "stage_init", manifest=manifest)
    root = initialized["remote_stage"]
    # Paths are restricted to shell-safe characters; no rsync --delete or
    # whole-project down-sync is used. The remote destination is a fresh run.
    subprocess.run(["rsync", "-az", "-e", "ssh -o BatchMode=yes -o ConnectTimeout=10",
                    str((args.run / "stage").resolve()) + "/", host + ":" + root + "/"], check=True)
    verified = rpc(host, "verify_stage", manifest=manifest)
    result = {"remote_root": root, **verified, "staged_at_utc": stamp()}
    write_new(args.run / "stage.json", result)
    return result


def submit(args, manifest: dict) -> dict:
    if not (args.run / "stage.json").exists():
        raise RuntimeError("verify staging first")
    write_new(args.run / "submission-attempt.json", {"started_at_utc": stamp(), "outcome": "unknown until receipt/status"})
    result = rpc(manifest["config"]["host"], "submit", manifest=manifest)
    write_new(args.run / "submission.json", result)
    return result


def git_repo_root(run_dir: Path) -> Path:
    top = git_output(run_dir, "rev-parse", "--show-toplevel")
    if not top:
        raise ValueError("fetch requires the run directory to live inside the user's git repository; "
                         "results go to that repository's locked results_dir, never to a chosen destination")
    return Path(top).resolve()


def fetch(args, manifest: dict) -> dict:
    relative = relative_path(args.relative)
    if args.storage == "data" and not relative.startswith("results/"):
        raise ValueError("data-root retrieval requires a named results/<run> path")
    if relative.split("/")[0] in SKIP_PARTS or relative in {"src", "scripts", "third_party"}:
        raise ValueError("retrieve a specific result directory, not code or an environment")
    repo_root = git_repo_root(args.run)
    results_dir = manifest["config"]["results_dir"]
    destination = repo_root / results_dir / manifest["run_id"]
    receipt_path = repo_root / results_dir / "fetched" / (manifest["run_id"] + ".json")
    if destination.exists() or receipt_path.exists():
        raise FileExistsError("results for this run were already fetched; fetching never overwrites")
    host = manifest["config"]["host"]
    inventory = rpc(host, "inventory", manifest=manifest, relative=relative, storage=args.storage,
                    inventory_timeout_seconds=getattr(args, "inventory_timeout_seconds", 120))
    if not inventory["files"]:
        raise RuntimeError("the named result path has no files")
    destination.mkdir(parents=True)
    subprocess.run(["rsync", "-azR", "-e", "ssh -o BatchMode=yes -o ConnectTimeout=10",
                    host + ":" + inventory["remote_base"] + "/./" + relative,
                    str(destination.resolve()) + "/"], check=True)
    verify_snapshot(destination, inventory["files"])
    _, remote_run_root, _ = run_layout(manifest["config"], manifest["run_id"])
    write_new(receipt_path, {"run_id": manifest["run_id"], "fetched_at_utc": stamp(),
                             "remote_run_root": str(remote_run_root),
                             "remote_base": inventory["remote_base"],
                             "manifest_sha256": manifest_digest(manifest),
                             "git_sha": manifest.get("git_sha"), "storage": args.storage,
                             "relative": relative, "files": len(inventory["files"]),
                             "all_file_hashes_verified": True,
                             "experiment_success": "not inferred from file transfer"})
    destination_rel = destination.relative_to(repo_root).as_posix()
    receipt_rel = receipt_path.relative_to(repo_root).as_posix()
    close_out = ["git -C " + shlex.quote(str(repo_root)) + " add "
                 + shlex.quote(destination_rel) + " " + shlex.quote(receipt_rel),
                 "git -C " + shlex.quote(str(repo_root)) + " commit -m "
                 + shlex.quote("results(ncsa): fetch run " + manifest["run_id"]),
                 "git -C " + shlex.quote(str(repo_root)) + " push"]
    return {"results": str(destination), "receipt": str(receipt_path),
            "verified_files": len(inventory["files"]), "close_out": close_out,
            "close_out_rule": "commit and push the fetched results and receipt in the same session"}


AUDIT_MARKER_BEGIN = "## ncsa audit v1 begin"
AUDIT_MARKER_END = "## ncsa audit v1 end"
AUDIT_CLASSES = ("REGISTERED", "INTERNAL", "ORPHAN")

# Emitted for the user's interactive Kerberos+Duo session; the helper never
# opens a non-interactive audit channel. Read-only: hostname/id/date/du/stat.
AUDIT_SNIPPET = r"""# NCSA Delta storage audit - read-only (hostname, id, date, du, stat only).
# Run this inside your interactive Kerberos+Duo Delta session, then paste the
# complete output back to: ncsa.py audit --parse
classify() {
  p=$1
  for reg in \
@REGISTERED@
  do
    case "$p" in
      "$reg") printf 'REGISTERED'; return;;
      "$reg"/*) printf 'INTERNAL'; return;;
    esac
    case "$reg" in
      "$p"/*) printf 'REGISTERED'; return;;
    esac
  done
  printf 'ORPHAN'
}
printf '%s\n' '@BEGIN@'
printf '## host=%s user=%s utc=%s\n' "$(hostname)" "$(id -un)" "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
for scan in \
@SCAN@
do
  if [ ! -d "$scan" ]; then
    printf '## missing-root\t%s\n' "$scan"
    continue
  fi
  for entry in "$scan"/* "$scan"/.[!.]*; do
    if [ ! -e "$entry" ]; then continue; fi
    size=$(du -sk "$entry" 2>/dev/null | cut -f1)
    mtime=$(stat -c '%Y' "$entry" 2>/dev/null | cut -f1)
    printf '%s\t%s\t%s\t%s\n' "$(classify "$entry")" "${size:-?}" "${mtime:-?}" "$entry"
  done
done
printf '%s\n' '@END@'
"""


def sh_list(values: list) -> str:
    # Config validation already restricts every value to shell-safe characters.
    return "    " + " \\\n    ".join("'" + value + "'" for value in values)


def audit_emit(configs: list) -> str:
    scan_roots, registered = set(), set()
    for cfg in configs:
        for key in ("compute_root", "data_root"):
            root = cfg[key]
            if not root.startswith(("/work/hdd/", "/projects/")):
                raise ValueError("audit needs storage roots under /work/hdd or /projects: " + root)
            # Scan the whole <allocation>/<user> directory, not only project roots.
            depth = 5 if root.startswith("/work/hdd/") else 4
            parts = PurePosixPath(root).parts
            if len(parts) < depth:
                raise ValueError("storage root is missing allocation/user components: " + root)
            scan_roots.add(PurePosixPath(*parts[:depth]).as_posix())
            registered.add(root)
            registered.add((PurePosixPath(root) / cfg["project"]).as_posix())
    return (AUDIT_SNIPPET
            .replace("@REGISTERED@", sh_list(sorted(registered)))
            .replace("@SCAN@", sh_list(sorted(scan_roots)))
            .replace("@BEGIN@", AUDIT_MARKER_BEGIN)
            .replace("@END@", AUDIT_MARKER_END))


def summarize_audit_report(text: str) -> dict:
    lines = text.splitlines()
    if AUDIT_MARKER_BEGIN not in lines or AUDIT_MARKER_END not in lines:
        raise ValueError("report is missing the ncsa audit begin/end markers; paste the complete snippet output")
    begin, end = lines.index(AUDIT_MARKER_BEGIN), lines.index(AUDIT_MARKER_END)
    if end <= begin:
        raise ValueError("audit report markers are out of order")
    entries, missing_roots, header = [], [], {}
    for line in lines[begin + 1:end]:
        if line.startswith("## host="):
            for part in line[len("## "):].split():
                key, _, value = part.partition("=")
                if key in ("host", "user", "utc"):
                    header[key] = value
            continue
        if line.startswith("## missing-root\t"):
            missing_roots.append(line.split("\t", 1)[1])
            continue
        if line.startswith("##"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError("malformed audit row (expected 4 tab-separated fields): " + line[:80])
        klass, size, mtime, path = fields
        if klass not in AUDIT_CLASSES:
            raise ValueError("unknown audit class: " + klass)
        if not path.startswith("/"):
            raise ValueError("audit row path must be absolute: " + line[:80])
        try:
            size_kb, mtime_epoch = int(size), int(mtime)
        except ValueError:
            raise ValueError("audit row has an unreadable size/mtime (du/stat failed remotely): " + line[:80])
        entries.append({"class": klass, "kb": size_kb,
                        "mtime_utc": datetime.fromtimestamp(mtime_epoch, timezone.utc).isoformat(),
                        "path": path})
    if not entries:
        raise ValueError("audit report contains no entries")
    by_class = {klass: {"count": 0, "kb": 0} for klass in AUDIT_CLASSES}
    for entry in entries:
        by_class[entry["class"]]["count"] += 1
        by_class[entry["class"]]["kb"] += entry["kb"]
    orphans = [entry["path"] for entry in entries if entry["class"] == "ORPHAN"]
    stamps = [entry["mtime_utc"] for entry in entries]
    return {"entries": len(entries), "by_class": by_class,
            "orphans": orphans[:20], "orphan_count": len(orphans),
            "oldest_mtime_utc": min(stamps), "newest_mtime_utc": max(stamps),
            "missing_roots": missing_roots,
            "remote_host": header.get("host"), "remote_user": header.get("user"),
            "remote_utc": header.get("utc")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="read-only connection/account/partition/storage report")
    doctor.add_argument("--host", default="delta")
    doctor.add_argument("--config", type=Path)
    doctor.add_argument("--out", type=Path)
    freeze = commands.add_parser("prepare", help="freeze selected files locally; no connection/allocation")
    freeze.add_argument("--config", type=Path, required=True)
    freeze.add_argument("--source", type=Path, required=True)
    freeze.add_argument("--include", action="append", required=True)
    freeze.add_argument("--out", type=Path, required=True)
    freeze.add_argument("--run-id", default=None,
                        help="run label (or short sha); default is the repository HEAD short sha; "
                             "a timestamp is only a disambiguator")
    freeze.add_argument("--entry", nargs=argparse.REMAINDER, required=True)
    for command in ("stage", "submit", "status", "fetch"):
        part = commands.add_parser(command)
        part.add_argument("--run", type=Path, required=True)
        if command == "fetch":
            part.add_argument("--storage", choices=("run", "data"), default="run")
            part.add_argument("--relative", required=True)
            part.add_argument("--inventory-timeout-seconds", type=int, default=120,
                              help="read-only inventory deadline, 1..600 seconds; default 120")
    audit = commands.add_parser("audit",
                                help="emit the read-only Delta storage audit snippet, or parse a pasted report")
    audit.add_argument("--config", type=Path, action="append",
                       help="a project .ncsa/config.json; repeat to register several projects in one audit")
    audit_mode = audit.add_mutually_exclusive_group(required=True)
    audit_mode.add_argument("--emit", action="store_true",
                            help="print the POSIX shell snippet to run inside the interactive Delta session")
    audit_mode.add_argument("--parse", nargs="?", const="-", default=None, metavar="REPORT",
                            help="parse a pasted report file ('-' reads stdin) and print a summary")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            cfg = config(args.config) if args.config else None
            host = cfg["host"] if cfg else args.host
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", host):
                raise ValueError("invalid SSH alias")
            result = rpc(host, "doctor", config=cfg)
            if args.out:
                write_new(args.out, result)
        elif args.command == "prepare":
            result = prepare(args)
        elif args.command == "audit":
            if args.emit:
                if not args.config:
                    raise ValueError("audit --emit needs at least one --config")
                print(audit_emit([config(path) for path in args.config]))
                return
            text = sys.stdin.read() if args.parse == "-" else Path(args.parse).read_text()
            result = summarize_audit_report(text)
        else:
            manifest = load_run(args.run)
            if args.command == "stage":
                result = stage(args, manifest)
            elif args.command == "submit":
                result = submit(args, manifest)
            elif args.command == "status":
                result = rpc(manifest["config"]["host"], "status", manifest=manifest)
            else:
                result = fetch(args, manifest)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
