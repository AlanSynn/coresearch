"""Offline resource, run-layout and read-only transport bounds; no SSH or Slurm execution."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('ncsa_limits_under_test', Path(__file__).parents[1] / 'scripts/ncsa.py')
ncsa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ncsa)

CONFIG = {'host': 'delta', 'account': 'verified-delta-gpu',
          'compute_root': '/work/hdd/verified/user', 'data_root': '/projects/verified/user',
          'project': 'verified-user-repo', 'results_dir': 'results',
          'filesystem_dependencies': ['projects', 'work'], 'partition': 'gpuA100x4',
          'minutes': 120, 'cpus': 16, 'memory_gb': 32, 'environment': {}}


class Limits(unittest.TestCase):
    def test_run_id_pattern_literal_stays_in_sync_with_run_layout(self):
        # RUN_LAYOUT runs remotely and cannot reference module constants, so
        # the run-ID pattern is duplicated there; this fails on drift locally
        # instead of relying on the remote fullmatch backstop.
        self.assertIn("re.fullmatch(r'" + ncsa.RUN_ID_RE + "', run_id)", ncsa.RUN_LAYOUT)

    def test_normal_and_interactive_partition_bounds(self):
        for partition in sorted(ncsa.PARTITIONS):
            limit = 60 if partition.endswith('-interactive') else 120
            for minutes in (1, limit):
                with self.subTest(partition=partition, minutes=minutes):
                    cfg = dict(deepcopy(CONFIG), partition=partition, minutes=minutes)
                    self.assertEqual(ncsa.validate_config(cfg)['minutes'], minutes)
            for minutes in (limit + 1, 0, True, float(limit)):
                with self.subTest(partition=partition, invalid_minutes=minutes):
                    with self.assertRaises(ValueError):
                        ncsa.validate_config(dict(deepcopy(CONFIG), partition=partition, minutes=minutes))

    def test_cpu_memory_and_partition_limits_remain(self):
        for key, value in (('cpus', 17), ('cpus', True), ('memory_gb', 33),
                           ('memory_gb', True), ('partition', 'gpuA100x4-preempt')):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                ncsa.validate_config(dict(deepcopy(CONFIG), **{key: value}))

    def test_project_comes_from_field_remote_basename_never_dirname(self):
        without = {key: value for key, value in deepcopy(CONFIG).items() if key != 'project'}
        with self.assertRaises(ValueError):
            ncsa.validate_config(deepcopy(without))
        self.assertEqual(ncsa.validate_config(deepcopy(without), project_default='remote-name')['project'],
                         'remote-name')
        for bad in ('', '../evil', 'a/b', '.hidden', True, None):
            with self.subTest(project=bad), self.assertRaises(ValueError):
                ncsa.validate_config(dict(deepcopy(CONFIG), project=bad))
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            subprocess.run(['git', '-C', str(repo), 'remote', 'add', 'origin',
                            'git@example.com:group/kamino-research.git'], check=True)
            self.assertEqual(ncsa.git_remote_project(repo), 'kamino-research')
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(ncsa.git_remote_project(Path(folder)))

    def test_results_dir_defaults_and_detection(self):
        without = {key: value for key, value in deepcopy(CONFIG).items() if key != 'results_dir'}
        self.assertEqual(ncsa.validate_config(deepcopy(without))['results_dir'], 'results')
        self.assertEqual(ncsa.validate_config(deepcopy(without), results_default='artifacts')['results_dir'],
                         'artifacts')
        for bad in ('', '../evil', 'a/b', '.hidden', '/abs', True):
            with self.subTest(results_dir=bad), self.assertRaises(ValueError):
                ncsa.validate_config(dict(deepcopy(CONFIG), results_dir=bad))

    def test_run_layout_is_one_root_per_project_and_refuses_escapes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = {'compute_root': str(root / 'compute'), 'project': 'proj'}
            base, run_root, tmp = ncsa.run_layout(cfg, 'mylabel')
            self.assertEqual(run_root, root / 'compute' / 'proj' / 'runs' / 'mylabel')
            self.assertEqual(tmp, root / 'compute' / 'proj' / 'tmp')
            ncsa.ensure_run_layout(cfg, 'mylabel')
            for name in ('stage', 'results', 'logs'):
                self.assertTrue((run_root / name).is_dir(), name)
            self.assertTrue(tmp.is_dir())
            meta = ncsa.write_meta(run_root, {'run_id': 'mylabel', 'git_sha': None,
                                              'config_sha256': 'ab' * 32, 'host': 'delta'})
            self.assertEqual(sorted(json.loads(meta.read_text())),
                             ['config_sha256', 'git_sha', 'host', 'run_id'])
            with self.assertRaises(FileExistsError):
                ncsa.write_meta(run_root, {'run_id': 'mylabel'})
            for bad in ('', '..', '../escape', 'a/b', None, 5, 'x' * 65):
                with self.subTest(run_id=bad), self.assertRaises(ValueError):
                    ncsa.run_layout(cfg, bad)
            with self.assertRaises(FileExistsError):
                ncsa.ensure_run_layout(cfg, 'mylabel')
            outside = root / 'outside'
            outside.mkdir()
            linked = root / 'compute' / 'other'
            linked.mkdir()
            (linked / 'proj').symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(cfg, compute_root=str(linked)), 'new-run')
            (root / 'compute' / 'proj2').mkdir()
            (root / 'compute' / 'proj2' / 'runs').symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(cfg, project='proj2'), 'new-run')
            (root / 'compute' / 'proj3').mkdir()
            (root / 'compute' / 'proj3' / 'tmp').symlink_to(outside)
            with self.assertRaises(ValueError):
                ncsa.ensure_run_layout(dict(cfg, project='proj3'), 'new-run')

    def test_prepare_records_layout_meta_and_scratch_rule_without_transport(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ncsa, 'rpc', side_effect=AssertionError('no transport')):
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            (source / 'entry.py').write_text('# Synthetic frozen input; not executed.\n')
            config = root / 'config.json'
            config.write_text(json.dumps(CONFIG))
            output = root / 'run'
            args = SimpleNamespace(config=config, source=source, out=output,
                                   include=['entry.py'], entry=['python3', '-B', 'entry.py'],
                                   run_id='synthetic-label')
            ncsa.prepare(args)
            manifest = ncsa.load_run(output)
            self.assertEqual(manifest['run_id'], 'synthetic-label')
            self.assertEqual(manifest['gpu_count'], 1)
            self.assertEqual(manifest['config']['minutes'], 120)
            self.assertEqual(manifest['config']['cpus'], 16)
            self.assertIsNone(manifest['git_sha'])
            self.assertFalse((output / 'submission-attempt.json').exists())
            script = (output / 'stage/ncsa-job.sh').read_text()
            self.assertIn('export TMPDIR="${TMPDIR:-/tmp}"', script)
            self.assertIn('NCSA_TMP_ROOT=/work/hdd/verified/user/verified-user-repo/tmp', script)
            self.assertIn('NCSA_RESULTS=/work/hdd/verified/user/verified-user-repo/runs/synthetic-label/results', script)
            self.assertNotIn('"$HOME"', script)
            self.assertNotIn('mktemp', script)

    def test_prepare_run_id_falls_back_to_head_sha_then_content_digest(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ncsa, 'rpc', side_effect=AssertionError('no transport')):
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            (source / 'entry.py').write_text('# Synthetic frozen input; not executed.\n')
            config = root / 'config.json'
            config.write_text(json.dumps(deepcopy(CONFIG)))
            # No project in the config and no git remote: prepare must refuse
            # instead of falling back to the local directory name.
            stripped = {key: value for key, value in deepcopy(CONFIG).items() if key != 'project'}
            stripped_config = root / 'config-no-project.json'
            stripped_config.write_text(json.dumps(stripped))
            args = SimpleNamespace(config=stripped_config, source=source, out=root / 'run-a',
                                   include=['entry.py'], entry=['python3', '-B', 'entry.py'],
                                   run_id=None)
            with self.assertRaises(ValueError):
                ncsa.prepare(args)
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            subprocess.run(['git', '-C', str(source), 'add', 'entry.py'], check=True)
            subprocess.run(['git', '-C', str(source), '-c', 'user.email=t@example.com',
                            '-c', 'user.name=T', 'commit', '-qm', 'synthetic'], check=True)
            args = SimpleNamespace(config=config, source=source, out=root / 'run-b',
                                   include=['entry.py'], entry=['python3', '-B', 'entry.py'],
                                   run_id=None)
            result = ncsa.prepare(args)
            head = subprocess.run(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                                  text=True, capture_output=True, check=True).stdout.strip()
            self.assertEqual(result['run_id'], head[:12])
            for bad in ('../escape', 'a/b', ''):
                with self.subTest(run_id=bad), self.assertRaises(ValueError):
                    ncsa.prepare(SimpleNamespace(config=config, source=source, out=root / ('run-' + bad),
                                                 include=['entry.py'], entry=['python3', '-B', 'entry.py'],
                                                 run_id=bad))

    def test_ordinary_rpc_keeps_120_seconds_and_auth_controls(self):
        for action in ('doctor', 'status', 'stage_init', 'verify_stage', 'submit'):
            with self.subTest(action=action), patch.object(ncsa.subprocess, 'run') as run:
                run.return_value = subprocess.CompletedProcess([], 0, '{}', '')
                self.assertEqual(ncsa.rpc('delta', action), {})
                self.assertEqual(run.call_args.kwargs['timeout'], 120)
                self.assertEqual(run.call_args.args[0][:6], ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', 'delta'])
                self.assertEqual(json.loads(run.call_args.kwargs['input']), {'action': action})

    def test_only_inventory_rpc_accepts_larger_deadline(self):
        with patch.object(ncsa.subprocess, 'run') as run:
            run.return_value = subprocess.CompletedProcess([], 0, '{"files": []}', '')
            ncsa.rpc('delta', 'inventory', inventory_timeout_seconds=600, relative='results/named')
            self.assertEqual(run.call_args.kwargs['timeout'], 600)
            self.assertNotIn('inventory_timeout_seconds', json.loads(run.call_args.kwargs['input']))
        for action, value in (('inventory', 601), ('inventory', 0), ('inventory', True),
                              ('inventory', 600.0), ('submit', 600), ('status', 600), ('doctor', 600)):
            with self.subTest(action=action, deadline=value), patch.object(ncsa.subprocess, 'run') as run:
                with self.assertRaises(ValueError):
                    ncsa.rpc('delta', action, inventory_timeout_seconds=value)
                run.assert_not_called()

    def test_inventory_timeout_preserves_unknown_outcome_exception(self):
        with patch.object(ncsa.subprocess, 'run', side_effect=subprocess.TimeoutExpired('synthetic ssh', 600)):
            with self.assertRaisesRegex(RuntimeError, 'SSH outcome is unknown'):
                ncsa.rpc('delta', 'inventory', inventory_timeout_seconds=600)

    def prepare_synthetic_run(self, repo: Path, results_dir: str) -> dict:
        source = repo
        (source / 'scripts').mkdir(exist_ok=True)
        (source / 'scripts/entry.py').write_text('# Synthetic frozen input; not executed.\n')
        config_data = {key: value for key, value in deepcopy(CONFIG).items() if key != 'results_dir'}
        (source / '.ncsa').mkdir(exist_ok=True)
        (source / '.ncsa/config.json').write_text(json.dumps(config_data))
        args = SimpleNamespace(config=source / '.ncsa/config.json', source=source,
                               out=source / '.ncsa/runs/synthetic01',
                               include=['scripts'], entry=['python3', '-B', 'scripts/entry.py'],
                               run_id='synthetic01')
        ncsa.prepare(args)
        return ncsa.load_run(args.out)

    def test_fetch_lands_in_repo_locked_results_dir_with_receipt(self):
        for results_dir, storage, relative in (('artifacts', 'data', 'results/synthetic-result'),
                                               ('results', 'run', 'synthetic-metrics')):
            with self.subTest(results_dir=results_dir, storage=storage):
                with tempfile.TemporaryDirectory() as folder:
                    repo = Path(folder) / 'repo'
                    repo.mkdir()
                    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
                    manifest = self.prepare_synthetic_run(repo, results_dir)
                    manifest['config']['results_dir'] = results_dir
                    record_path = relative + '/result.json'
                    record = {'path': record_path, 'bytes': 3, 'sha256': ncsa.sha(b'{}\n'), 'mode': 0o644}
                    inventory = {'files': [record], 'remote_base': '/work/hdd/verified/user/verified-user-repo/runs/synthetic01/results'}
                    args = SimpleNamespace(run=repo / '.ncsa/runs/synthetic01', storage=storage,
                                           relative=relative, inventory_timeout_seconds=600)
                    destination = repo / results_dir / 'synthetic01'

                    def fake_rsync(command, **options):
                        self.assertEqual(command[0], 'rsync')
                        target = destination / record_path
                        target.parent.mkdir(parents=True)
                        target.write_bytes(b'{}\n')
                        target.chmod(0o644)
                        return subprocess.CompletedProcess(command, 0)

                    with patch.object(ncsa, 'rpc', return_value=inventory), \
                            patch.object(ncsa, 'git_output', return_value=str(repo)), \
                            patch.object(ncsa.subprocess, 'run', side_effect=fake_rsync):
                        result = ncsa.fetch(args, manifest)
                    self.assertTrue((destination / record_path).is_file())
                    receipt = json.loads((repo / results_dir / 'fetched/synthetic01.json').read_text())
                    self.assertEqual(receipt['run_id'], 'synthetic01')
                    self.assertEqual(receipt['manifest_sha256'], ncsa.manifest_digest(manifest))
                    self.assertEqual(receipt['remote_run_root'],
                                     '/work/hdd/verified/user/verified-user-repo/runs/synthetic01')
                    self.assertTrue(receipt['all_file_hashes_verified'])
                    self.assertTrue(result['close_out'][0].startswith('git -C '))
                    self.assertIn(f' add {results_dir}/synthetic01 {results_dir}/fetched/synthetic01.json',
                                  result['close_out'][0])
                    self.assertIn(' commit -m ', result['close_out'][1])
                    self.assertEqual(result['close_out'][2].rsplit(' ', 1)[-1], 'push')
                    # A second fetch of the same run never overwrites anything.
                    with patch.object(ncsa, 'rpc', side_effect=AssertionError('no second inventory')):
                        with self.assertRaises(FileExistsError):
                            ncsa.fetch(args, manifest)

    def test_fetch_refuses_run_directory_outside_a_git_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            plain = Path(folder) / 'plain'
            (plain / '.ncsa/runs/synthetic01').mkdir(parents=True)
            manifest = {'run_id': 'synthetic01', 'schema_version': 3, 'config': deepcopy(CONFIG), 'files': []}
            (plain / '.ncsa/runs/synthetic01/manifest.json').write_text(json.dumps(manifest))
            args = SimpleNamespace(run=plain / '.ncsa/runs/synthetic01', storage='run',
                                   relative='named', inventory_timeout_seconds=120)
            with patch.object(ncsa, 'rpc', side_effect=AssertionError('no transport')):
                with self.assertRaisesRegex(ValueError, 'git repository'):
                    ncsa.fetch(args, manifest)


if __name__ == '__main__':
    unittest.main()
