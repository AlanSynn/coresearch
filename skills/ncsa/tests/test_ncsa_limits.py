"""Offline resource and read-only transport bounds; no SSH or Slurm execution."""
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
          'compute_root': '/work/hdd/verified/user/project', 'data_root': '/projects/verified/user/project',
          'filesystem_dependencies': ['projects', 'work'], 'partition': 'gpuA100x4',
          'minutes': 120, 'cpus': 16, 'memory_gb': 32, 'environment': {}}


class Limits(unittest.TestCase):
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

    def test_prepare_records_one_gpu_and_120_minutes_without_transport(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ncsa, 'rpc', side_effect=AssertionError('no transport')):
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            (source / 'entry.py').write_text('# Synthetic frozen input; not executed.\n')
            config = root / 'config.json'
            config.write_text(json.dumps(CONFIG))
            output = root / 'run'
            args = SimpleNamespace(config=config, source=source, out=output,
                                   include=['entry.py'], entry=['python3', '-B', 'entry.py'])
            ncsa.prepare(args)
            manifest = ncsa.load_run(output)
            self.assertEqual(manifest['gpu_count'], 1)
            self.assertEqual(manifest['config']['minutes'], 120)
            self.assertEqual(manifest['config']['cpus'], 16)
            self.assertNotIn('--requeue', (output / 'repo/ncsa-job.sh').read_text())
            self.assertFalse((output / 'submission-attempt.json').exists())

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

    def test_fetch_override_retains_exact_hash_and_mode_verification(self):
        for corrupt in (False, True):
            with self.subTest(corrupt=corrupt), tempfile.TemporaryDirectory() as folder:
                out = Path(folder) / 'received'
                relative = 'results/synthetic_result'
                record = {'path': relative + '/result.json', 'bytes': 3, 'sha256': ncsa.sha(b'{}\n'), 'mode': 0o644}
                inventory = {'files': [record], 'remote_base': '/projects/verified/user/project'}
                args = SimpleNamespace(storage='data', relative=relative, out=out, inventory_timeout_seconds=600)
                manifest = {'run_id': 'a' * 16, 'config': deepcopy(CONFIG)}

                def fake_rsync(command, **options):
                    self.assertEqual(command[0], 'rsync')
                    target = out / record['path']
                    target.parent.mkdir(parents=True)
                    target.write_bytes(b'bad' if corrupt else b'{}\n')
                    target.chmod(0o644)
                    return subprocess.CompletedProcess(command, 0)

                with patch.object(ncsa, 'rpc', return_value=inventory) as rpc, patch.object(ncsa.subprocess, 'run', side_effect=fake_rsync):
                    if corrupt:
                        with self.assertRaises(ValueError):
                            ncsa.fetch(args, manifest)
                        self.assertFalse((out / 'fetch-receipt.json').exists())
                    else:
                        ncsa.fetch(args, manifest)
                        receipt = json.loads((out / 'fetch-receipt.json').read_text())
                        self.assertEqual(receipt['files'], [record])
                        self.assertIs(receipt['all_file_hashes_verified'], True)
                    self.assertEqual(rpc.call_args.kwargs['inventory_timeout_seconds'], 600)
                    self.assertEqual(rpc.call_args.kwargs['relative'], relative)


if __name__ == '__main__':
    unittest.main()
