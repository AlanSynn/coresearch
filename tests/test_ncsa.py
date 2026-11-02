"""Offline NCSA Delta helper contracts, plus CLI coverage with stub ssh/rsync.

No real SSH: Delta needs an interactive Duo session, so remote transport is a
stub fixture and every check runs locally in disposable directories.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ncsa_under_test", ROOT / "skills/coresearch/scripts/ncsa.py")
ncsa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ncsa)

CONFIG = {"host": "delta", "account": "verified-delta-gpu",
          "compute_root": "/work/hdd/verified/user", "data_root": "/projects/verified/user",
          "project": "verified-user-repo", "results_dir": "results",
          "filesystem_dependencies": ["projects", "work"], "partition": "gpuA100x4",
          "minutes": 120, "cpus": 16, "memory_gb": 32, "environment": {}}


def cli(*args, path=None, cwd=None):
    environment = dict(os.environ)
    if path is not None:
        environment["PATH"] = str(path) + os.pathsep + environment["PATH"]
    return subprocess.run([sys.executable, "-B", str(ROOT / "skills/coresearch/scripts/ncsa.py"), *map(str, args)],
                          cwd=cwd, env=environment, input="", capture_output=True, text=True, timeout=30)


def stub_transport(bin_dir: Path, remote_base: str) -> None:
    sha = hashlib.sha256(b"{}\n").hexdigest()
    inventory = ('{"files": [{"path": "results/synthetic-result/result.json", '
                 '"sha256": "' + sha + '", "bytes": 3, "mode": 420}], "remote_base": "' + remote_base + '"}')
    (bin_dir / "ssh").write_text("#!/usr/bin/env sh\ncat <<'JSON'\n" + inventory + "\nJSON\n")
    (bin_dir / "rsync").write_text(
        "#!/usr/bin/env sh\n"
        "for last; do :; done\n"
        'mkdir -p "$last/results/synthetic-result"\n'
        "printf '{}\\n' > \"$last/results/synthetic-result/result.json\"\n"
        'chmod 644 "$last/results/synthetic-result/result.json"\n')
    for script in (bin_dir / "ssh", bin_dir / "rsync"):
        script.chmod(0o755)


def synthetic_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "scripts").mkdir()
    (repo / "artifacts").mkdir()  # the convention prepare detects as results_dir
    (repo / "scripts/entry.py").write_text("# Synthetic frozen input; not executed.\n")
    config = {key: value for key, value in CONFIG.items() if key != "results_dir"}
    (repo / ".ncsa").mkdir()
    (repo / ".ncsa/config.json").write_text(json.dumps(config))
    return repo


class Limits(unittest.TestCase):
    def test_normal_and_interactive_partition_bounds(self):
        for partition in sorted(ncsa.PARTITIONS):
            limit = 60 if partition.endswith("-interactive") else 120
            for minutes in (1, limit):
                with self.subTest(partition=partition, minutes=minutes):
                    config = dict(CONFIG, partition=partition, minutes=minutes)
                    self.assertEqual(ncsa.validate_config(dict(config))["minutes"], minutes)
            for minutes in (limit + 1, 0, True, float(limit)):
                with self.subTest(partition=partition, invalid_minutes=minutes):
                    with self.assertRaises(ValueError):
                        ncsa.validate_config(dict(CONFIG, partition=partition, minutes=minutes))

    def test_cpu_memory_and_partition_limits_remain(self):
        for key, value in (("cpus", 17), ("cpus", True), ("memory_gb", 33),
                           ("memory_gb", True), ("partition", "gpuA100x4-preempt")):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                ncsa.validate_config(dict(CONFIG, **{key: value}))

    def test_project_comes_from_field_remote_basename_never_dirname(self):
        without = {key: value for key, value in CONFIG.items() if key != "project"}
        with self.assertRaises(ValueError):
            ncsa.validate_config(dict(without))
        self.assertEqual(ncsa.validate_config(dict(without), project_default="remote-name")["project"],
                         "remote-name")
        for bad in ("", "../evil", "a/b", ".hidden", True, None):
            with self.subTest(project=bad), self.assertRaises(ValueError):
                ncsa.validate_config(dict(CONFIG, project=bad))
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                            "git@example.com:group/kamino-research.git"], check=True)
            self.assertEqual(ncsa.git_remote_project(repo), "kamino-research")
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(ncsa.git_remote_project(Path(folder)))

    def test_results_dir_defaults_and_detection(self):
        without = {key: value for key, value in CONFIG.items() if key != "results_dir"}
        self.assertEqual(ncsa.validate_config(dict(without))["results_dir"], "results")
        self.assertEqual(ncsa.validate_config(dict(without), results_default="artifacts")["results_dir"],
                         "artifacts")
        for bad in ("", "../evil", "a/b", ".hidden", "/abs", True):
            with self.subTest(results_dir=bad), self.assertRaises(ValueError):
                ncsa.validate_config(dict(CONFIG, results_dir=bad))

    def test_run_id_pattern_literal_stays_in_sync_with_run_layout(self):
        # RUN_LAYOUT runs remotely and cannot reference module constants, so
        # the run-ID pattern is duplicated there; this fails on drift locally
        # instead of relying on the remote fullmatch backstop.
        self.assertIn("re.fullmatch(r'" + ncsa.RUN_ID_RE + "', run_id)", ncsa.RUN_LAYOUT)

    def test_run_layout_is_one_root_per_project_and_refuses_escapes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = {"compute_root": str(root / "compute"), "project": "proj"}
            base, run_root, scratch = ncsa.run_layout(config, "mylabel")
            self.assertEqual(run_root, root / "compute" / "proj" / "runs" / "mylabel")
            self.assertEqual(scratch, root / "compute" / "proj" / "tmp")
            ncsa.ensure_run_layout(config, "mylabel")
            for name in ("stage", "results", "logs"):
                self.assertTrue((run_root / name).is_dir(), name)
            self.assertTrue(scratch.is_dir())
            meta = ncsa.write_meta(run_root, {"run_id": "mylabel", "git_sha": None,
                                              "config_sha256": "ab" * 32, "host": "delta"})
            self.assertEqual(sorted(json.loads(meta.read_text())),
                             ["config_sha256", "git_sha", "host", "run_id"])
            with self.assertRaises(FileExistsError):
                ncsa.write_meta(run_root, {"run_id": "mylabel"})
            for bad in ("", "..", "../escape", "a/b", None, 5, "x" * 65):
                with self.subTest(run_id=bad), self.assertRaises(ValueError):
                    ncsa.run_layout(config, bad)
            with self.assertRaises(FileExistsError):
                ncsa.ensure_run_layout(config, "mylabel")
            outside = root / "outside"
            outside.mkdir()
            linked = root / "compute" / "other"
            linked.mkdir()
            (linked / "proj").symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(config, compute_root=str(linked)), "new-run")
            (root / "compute" / "proj2").mkdir()
            (root / "compute" / "proj2" / "runs").symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(config, project="proj2"), "new-run")
            (root / "compute" / "proj3").mkdir()
            (root / "compute" / "proj3" / "tmp").symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(config, project="proj3"), "new-run")

    def test_prepare_records_layout_meta_and_scratch_rule_without_transport(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ncsa, "rpc", side_effect=AssertionError("no transport")):
            root = Path(folder)
            source = root / "source"
            source.mkdir()
            (source / "entry.py").write_text("# Synthetic frozen input; not executed.\n")
            config = root / "config.json"
            config.write_text(json.dumps(CONFIG))
            output = root / "run"
            arguments = SimpleNamespace(config=config, source=source, out=output,
                                        include=["entry.py"], entry=["python3", "-B", "entry.py"],
                                        run_id="synthetic-label")
            ncsa.prepare(arguments)
            manifest = ncsa.load_run(output)
            self.assertEqual(manifest["run_id"], "synthetic-label")
            self.assertEqual(manifest["gpu_count"], 1)
            self.assertEqual(manifest["config"]["minutes"], 120)
            self.assertEqual(manifest["config"]["cpus"], 16)
            self.assertIsNone(manifest["git_sha"])
            self.assertFalse((output / "submission-attempt.json").exists())
            script = (output / "stage/ncsa-job.sh").read_text()
            self.assertIn('export TMPDIR="${TMPDIR:-/tmp}"', script)
            self.assertIn("NCSA_TMP_ROOT=/work/hdd/verified/user/verified-user-repo/tmp", script)
            self.assertIn("NCSA_RESULTS=/work/hdd/verified/user/verified-user-repo/runs/synthetic-label/results", script)
            self.assertNotIn('"$HOME"', script)
            self.assertNotIn("mktemp", script)

    def test_prepare_run_id_falls_back_to_head_sha_then_content_digest(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ncsa, "rpc", side_effect=AssertionError("no transport")):
            root = Path(folder)
            source = root / "source"
            source.mkdir()
            (source / "entry.py").write_text("# Synthetic frozen input; not executed.\n")
            config = root / "config.json"
            config.write_text(json.dumps(CONFIG))
            stripped = {key: value for key, value in CONFIG.items() if key != "project"}
            stripped_config = root / "config-no-project.json"
            stripped_config.write_text(json.dumps(stripped))
            # No project in the config and no git remote: prepare must refuse
            # instead of falling back to the local directory name.
            arguments = SimpleNamespace(config=stripped_config, source=source, out=root / "run-a",
                                        include=["entry.py"], entry=["python3", "-B", "entry.py"],
                                        run_id=None)
            with self.assertRaises(ValueError):
                ncsa.prepare(arguments)
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "add", "entry.py"], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.email=t@example.com",
                            "-c", "user.name=T", "commit", "-qm", "synthetic"], check=True)
            arguments = SimpleNamespace(config=config, source=source, out=root / "run-b",
                                        include=["entry.py"], entry=["python3", "-B", "entry.py"],
                                        run_id=None)
            result = ncsa.prepare(arguments)
            head = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                                  text=True, capture_output=True, check=True).stdout.strip()
            self.assertEqual(result["run_id"], head[:12])
            for bad in ("../escape", "a/b", ""):
                with self.subTest(run_id=bad), self.assertRaises(ValueError):
                    ncsa.prepare(SimpleNamespace(config=config, source=source, out=root / ("run-" + bad),
                                                 include=["entry.py"], entry=["python3", "-B", "entry.py"],
                                                 run_id=bad))

    def test_ordinary_rpc_keeps_120_seconds_and_auth_controls(self):
        for action in ("doctor", "status", "stage_init", "verify_stage", "submit"):
            with self.subTest(action=action), patch.object(ncsa.subprocess, "run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, "{}", "")
                self.assertEqual(ncsa.rpc("delta", action), {})
                self.assertEqual(run.call_args.kwargs["timeout"], 120)
                self.assertEqual(run.call_args.args[0][:6],
                                 ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "delta"])
                self.assertEqual(json.loads(run.call_args.kwargs["input"]), {"action": action})

    def test_only_inventory_rpc_accepts_larger_deadline(self):
        with patch.object(ncsa.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, '{"files": []}', "")
            ncsa.rpc("delta", "inventory", inventory_timeout_seconds=600, relative="results/named")
            self.assertEqual(run.call_args.kwargs["timeout"], 600)
            self.assertNotIn("inventory_timeout_seconds", json.loads(run.call_args.kwargs["input"]))
        for action, value in (("inventory", 601), ("inventory", 0), ("inventory", True),
                              ("inventory", 600.0), ("submit", 600), ("status", 600), ("doctor", 600)):
            with self.subTest(action=action, deadline=value), patch.object(ncsa.subprocess, "run") as run:
                with self.assertRaises(ValueError):
                    ncsa.rpc("delta", action, inventory_timeout_seconds=value)
                run.assert_not_called()

    def test_inventory_timeout_preserves_unknown_outcome_exception(self):
        with patch.object(ncsa.subprocess, "run", side_effect=subprocess.TimeoutExpired("synthetic ssh", 600)):
            with self.assertRaisesRegex(RuntimeError, "SSH outcome is unknown"):
                ncsa.rpc("delta", "inventory", inventory_timeout_seconds=600)

    def prepare_synthetic_run(self, repo: Path, results_dir: str) -> dict:
        arguments = SimpleNamespace(config=repo / ".ncsa/config.json", source=repo,
                                    out=repo / ".ncsa/runs/synthetic01",
                                    include=["scripts"], entry=["python3", "-B", "scripts/entry.py"],
                                    run_id="synthetic01")
        ncsa.prepare(arguments)
        manifest = ncsa.load_run(arguments.out)
        manifest["config"]["results_dir"] = results_dir
        return manifest

    def test_fetch_lands_in_repo_locked_results_dir_with_receipt(self):
        for results_dir, storage, relative in (("artifacts", "data", "results/synthetic-result"),
                                               ("results", "run", "synthetic-metrics")):
            with self.subTest(results_dir=results_dir, storage=storage):
                with tempfile.TemporaryDirectory() as folder:
                    repo = Path(folder) / "repo"
                    repo.mkdir()
                    subprocess.run(["git", "init", "-q", str(repo)], check=True)
                    (repo / "scripts").mkdir()
                    (repo / "scripts/entry.py").write_text("# Synthetic frozen input; not executed.\n")
                    config = {key: value for key, value in CONFIG.items() if key != "results_dir"}
                    (repo / ".ncsa").mkdir()
                    (repo / ".ncsa/config.json").write_text(json.dumps(config))
                    manifest = self.prepare_synthetic_run(repo, results_dir)
                    record_path = relative + "/result.json"
                    record = {"path": record_path, "bytes": 3, "sha256": ncsa.sha(b"{}\n"), "mode": 0o644}
                    inventory = {"files": [record],
                                 "remote_base": "/work/hdd/verified/user/verified-user-repo/runs/synthetic01/results"}
                    arguments = SimpleNamespace(run=repo / ".ncsa/runs/synthetic01", storage=storage,
                                                relative=relative, inventory_timeout_seconds=600)
                    destination = repo / results_dir / "synthetic01"

                    def fake_rsync(command, **options):
                        self.assertEqual(command[0], "rsync")
                        target = destination / record_path
                        target.parent.mkdir(parents=True)
                        target.write_bytes(b"{}\n")
                        target.chmod(0o644)
                        return subprocess.CompletedProcess(command, 0)

                    with patch.object(ncsa, "rpc", return_value=inventory), \
                            patch.object(ncsa, "git_output", return_value=str(repo)), \
                            patch.object(ncsa.subprocess, "run", side_effect=fake_rsync):
                        result = ncsa.fetch(arguments, manifest)
                    self.assertTrue((destination / record_path).is_file())
                    receipt = json.loads((repo / results_dir / "fetched/synthetic01.json").read_text())
                    self.assertEqual(receipt["run_id"], "synthetic01")
                    self.assertEqual(receipt["manifest_sha256"], ncsa.manifest_digest(manifest))
                    self.assertEqual(receipt["remote_run_root"],
                                     "/work/hdd/verified/user/verified-user-repo/runs/synthetic01")
                    self.assertTrue(receipt["all_file_hashes_verified"])
                    self.assertTrue(result["close_out"][0].startswith("git -C "))
                    self.assertIn(f" add {results_dir}/synthetic01 {results_dir}/fetched/synthetic01.json",
                                  result["close_out"][0])
                    self.assertIn(" commit -m ", result["close_out"][1])
                    self.assertEqual(result["close_out"][2].rsplit(" ", 1)[-1], "push")
                    # A second fetch of the same run never overwrites anything.
                    with patch.object(ncsa, "rpc", side_effect=AssertionError("no second inventory")):
                        with self.assertRaises(FileExistsError):
                            ncsa.fetch(arguments, manifest)

    def test_fetch_refuses_run_directory_outside_a_git_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            plain = Path(folder) / "plain"
            (plain / ".ncsa/runs/synthetic01").mkdir(parents=True)
            manifest = {"run_id": "synthetic01", "schema_version": 3, "config": dict(CONFIG), "files": []}
            (plain / ".ncsa/runs/synthetic01/manifest.json").write_text(json.dumps(manifest))
            arguments = SimpleNamespace(run=plain / ".ncsa/runs/synthetic01", storage="run",
                                        relative="named", inventory_timeout_seconds=120)
            with patch.object(ncsa, "rpc", side_effect=AssertionError("no transport")):
                with self.assertRaisesRegex(ValueError, "git repository"):
                    ncsa.fetch(arguments, manifest)


class CommandLine(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        stub_transport(self.bin, "/work/hdd/verified/user/verified-repo/runs/label-one/results")
        self.repo = synthetic_repo(self.root)
        # Project-level roots, like the real per-project configurations: the
        # allocation user dir is then unregistered, so the audit snippet can
        # classify REGISTERED/INTERNAL/ORPHAN distinctly.
        config = json.loads((self.repo / ".ncsa/config.json").read_text())
        config["compute_root"] = "/work/hdd/verified/user/verified-repo"
        config["data_root"] = "/projects/verified/user/verified-repo"
        config["project"] = "verified-repo"
        (self.repo / ".ncsa/config.json").write_text(json.dumps(config))

    def prepare(self, *extra, config=".ncsa/config.json"):
        return cli("prepare", "--config", self.repo / config, "--source", self.repo,
                   "--include", "scripts", "--out", self.repo / ".ncsa/runs/label-one",
                   "--run-id", "label-one", "--entry", "python3", "scripts/entry.py",
                   *extra, cwd=self.repo)

    def test_prepare_refuses_missing_project_and_traversal_run_id(self):
        (self.repo / ".ncsa/config-no-project.json").write_text(
            json.dumps({key: value for key, value in CONFIG.items() if key != "project"}))
        # The fixture repo has no git remote, so project must be explicit;
        # the local directory name is never a fallback.
        result = self.prepare(config=".ncsa/config-no-project.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit project field", result.stderr)
        self.assertFalse((self.repo / ".ncsa/runs/rejected").exists())
        prepared = self.prepare()
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        self.assertIn('"run_id": "label-one"', prepared.stdout)
        self.assertTrue((self.repo / ".ncsa/runs/label-one/stage/scripts/entry.py").is_file())
        script = (self.repo / ".ncsa/runs/label-one/stage/ncsa-job.sh").read_text()
        self.assertIn('export TMPDIR="${TMPDIR:-/tmp}"', script)
        self.assertIn("NCSA_TMP_ROOT=/work/hdd/verified/user/verified-repo/verified-repo/tmp", script)
        bad = cli("prepare", "--config", self.repo / ".ncsa/config.json", "--source", self.repo,
                  "--include", "scripts", "--out", self.repo / ".ncsa/runs/escape",
                  "--run-id", "../escape", "--entry", "python3", "scripts/entry.py", cwd=self.repo)
        self.assertNotEqual(bad.returncode, 0)
        self.assertFalse((self.repo / ".ncsa/runs/escape").exists())

    def test_fetch_cli_uses_detected_results_dir_and_prints_close_out(self):
        self.assertEqual(self.prepare().returncode, 0, self.prepare().stderr)
        fetched = cli("fetch", "--run", ".ncsa/runs/label-one",
                      "--relative", "results/synthetic-result", "--storage", "data",
                      path=self.bin, cwd=self.repo)
        self.assertEqual(fetched.returncode, 0, fetched.stderr)
        self.assertTrue((self.repo / "artifacts/label-one/results/synthetic-result/result.json").is_file())
        receipt = json.loads((self.repo / "artifacts/fetched/label-one.json").read_text())
        self.assertEqual(receipt["run_id"], "label-one")
        self.assertIn("manifest_sha256", receipt)
        self.assertIn("git -C", fetched.stdout)
        self.assertIn(" add artifacts/label-one artifacts/fetched/label-one.json", fetched.stdout)
        self.assertIn("git -C", fetched.stdout)
        self.assertRegex(fetched.stdout, r"git -C \S+ push")
        overridden = cli("fetch", "--run", ".ncsa/runs/label-one", "--relative", "results/synthetic-result",
                         "--storage", "data", "--dest", "somewhere", path=self.bin, cwd=self.repo)
        self.assertNotEqual(overridden.returncode, 0)
        self.assertIn("unrecognized arguments", overridden.stderr)
        again = cli("fetch", "--run", ".ncsa/runs/label-one", "--relative", "results/synthetic-result",
                    "--storage", "data", path=self.bin, cwd=self.repo)
        self.assertNotEqual(again.returncode, 0)
        self.assertIn("already fetched", again.stderr)

    def test_audit_cli_emits_posix_snippet_classifies_and_parses(self):
        emitted = cli("audit", "--config", self.repo / ".ncsa/config.json", "--emit", cwd=self.repo)
        self.assertEqual(emitted.returncode, 0, emitted.stderr)
        snippet = self.root / "audit.sh"
        snippet.write_text(emitted.stdout)
        self.assertEqual(subprocess.run(["sh", "-n", str(snippet)], capture_output=True).returncode, 0)
        text = snippet.read_text()
        self.assertIn("du -sk", text)
        self.assertIn("stat -c '%Y'", text)
        self.assertIn("/work/hdd/verified/user", text)
        self.assertIn("/projects/verified/user", text)
        local = subprocess.run(["sh", str(snippet)], capture_output=True, text=True, timeout=30)
        self.assertEqual(local.returncode, 0, local.stderr)
        self.assertIn("## ncsa audit v1 begin", local.stdout)
        self.assertIn("## ncsa audit v1 end", local.stdout)
        self.assertIn("missing-root", local.stdout)  # fixture roots exist only on Delta
        lines = text.splitlines()
        classify = lines[lines.index("classify() {"):lines.index("}", lines.index("classify() {")) + 1]
        driver = snippet.with_name("classify.sh")
        driver.write_text("\n".join(classify) + """
check() {
  result=$(classify "$1")
  if [ "$result" != "$2" ]; then
    echo "classify $1 -> $result (expected $2)" >&2
    exit 1
  fi
}
check '/work/hdd/verified/user/verified-repo' REGISTERED
check '/projects/verified/user/verified-repo' REGISTERED
check '/work/hdd/verified/user/verified-repo/runs/label-one' INTERNAL
check '/work/hdd/verified/user/stray' ORPHAN
""")
        self.assertEqual(subprocess.run(["sh", str(driver)], capture_output=True, timeout=30).returncode, 0)
        report = self.root / "report.txt"
        report.write_text("\n".join([
            "## ncsa audit v1 begin",
            "## host=delta-login-1 user=verified utc=2026-11-01T00:00:00Z",
            "REGISTERED\t1024\t1761916800\t/work/hdd/verified/user/verified-repo",
            "INTERNAL\t512\t1761916801\t/work/hdd/verified/user/verified-repo/old",
            "ORPHAN\t64\t1761000000\t/work/hdd/verified/user/stray",
            "## ncsa audit v1 end",
        ]))
        parsed = cli("audit", "--parse", report, cwd=self.repo)
        self.assertEqual(parsed.returncode, 0, parsed.stderr)
        self.assertIn('"orphan_count": 1', parsed.stdout)
        self.assertIn('"REGISTERED"', parsed.stdout)
        self.assertIn("delta-login-1", parsed.stdout)
        malformed = self.root / "malformed.txt"
        malformed.write_text("not an audit report\n")
        bad = cli("audit", "--parse", malformed, cwd=self.repo)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("markers", bad.stderr)


if __name__ == "__main__":
    unittest.main()
