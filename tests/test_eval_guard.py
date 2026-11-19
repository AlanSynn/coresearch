"""The evaluation names every model and runs Fable or Astra only within a grant the user made."""
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals/host-policy"
spec = importlib.util.spec_from_file_location("grants", EVAL / "grants.py")
grants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grants)


class GrantTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.now = dt.datetime(2026, 11, 19, 12, tzinfo=dt.timezone.utc)

    def test_families_and_indirect_names(self):
        for model, expected in [("fable", "fable"), ("claude-fable-5-2", "fable"), ("gpt-6.2-astra", "astra"),
                                ("GPT-6-Astra", "astra"), ("opus", None), ("haiku", None), ("gpt-6.2-sol", None)]:
            self.assertEqual(grants.family(model), expected, model)
        for alias in ("", "default", "best"):
            with self.assertRaisesRegex(ValueError, "name the model explicitly"):
                grants.family(alias)

    def test_reserve_needs_a_grant_and_counts_it_down(self):
        with self.assertRaisesRegex(PermissionError, "grants.py grant fable --runs 2"):
            grants.reserve({"fable": 2}, "test", self.home, self.now)
        grants.grant("fable", 3, 12, self.home, self.now)
        grants.reserve({"fable": 2, "astra": 0}, "test", self.home, self.now)
        with self.assertRaisesRegex(PermissionError, "fable: 2 runs needed, 1 granted"):
            grants.reserve({"fable": 2}, "test", self.home, self.now)
        grants.reserve({"fable": 1}, "test", self.home, self.now)
        entry = json.loads(grants.grants_path(self.home).read_text())["fable"]
        self.assertEqual(entry["runs"], 0)
        self.assertEqual([use["runs"] for use in entry["used"]], [2, 1])

    def test_reserve_takes_nothing_when_one_family_is_short(self):
        grants.grant("fable", 5, 12, self.home, self.now)
        with self.assertRaises(PermissionError):
            grants.reserve({"fable": 1, "astra": 1}, "test", self.home, self.now)
        self.assertEqual(json.loads(grants.grants_path(self.home).read_text())["fable"]["runs"], 5)

    def test_grant_lapses(self):
        grants.grant("astra", 5, 1, self.home, self.now)
        with self.assertRaises(PermissionError):
            grants.reserve({"astra": 1}, "test", self.home, self.now + dt.timedelta(hours=2))

    def test_grant_command_needs_the_users_terminal(self):
        # A new session has no controlling terminal, as in an agent's shell.
        result = subprocess.run([sys.executable, "-B", str(EVAL / "grants.py"), "grant", "fable", "--runs", "5"],
                                env={**os.environ, "HOME": str(self.home)}, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, start_new_session=True, timeout=60)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not granted", result.stderr)
        self.assertFalse(grants.grants_path(self.home).exists())

    def test_guard_denies_subagents_on_blocked_families(self):
        for tool, model in (("Agent", "fable"), ("collaborationspawn_agent", "gpt-6.2-astra")):
            event = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"model": model}}
            self.assertEqual(grants.guard(["fable", "astra"], event)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIsNone(grants.guard(["astra"], {"tool_name": "Agent", "tool_input": {"model": "fable"}}))
        self.assertIsNone(grants.guard(["fable"], {"tool_name": "Bash", "tool_input": {"command": "fable"}}))

    def test_guard_command_as_installed(self):
        command = grants.guard_command(["fable", "astra"], self.home)
        event = {"tool_name": "Agent", "tool_input": {"model": "fable", "prompt": "x"}}
        result = subprocess.run(command, shell=True, input=json.dumps(event), capture_output=True, text=True, timeout=60)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
        subprocess.run(command, shell=True, input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}}),
                       capture_output=True, text=True, timeout=60)
        self.assertEqual(grants.guard_log(self.home), [{"tool": "Agent", "model": "fable", "denied": True}])

    def test_model_choosing_variables_are_dropped(self):
        chosen = {"ANTHROPIC_MODEL": "fable", "ANTHROPIC_DEFAULT_OPUS_MODEL": "fable",
                  "CLAUDE_CODE_SUBAGENT_MODEL": "fable", "ANTHROPIC_BASE_URL": "kept"}
        with patch.dict(os.environ, chosen):
            environment = grants.model_free_env()
        self.assertEqual({key for key in chosen if key in environment}, {"ANTHROPIC_BASE_URL"})

    def test_codex_config_lines_cannot_choose_the_model(self):
        for line in ('model = "gpt-6.2-astra"', 'profile = "astra"', '[profiles.astra]', 'model_reasoning_effort = "max"',
                     '[agents.reviewer]'):
            self.assertTrue(grants.CODEX_MODEL_SETTING.search(f"allow_login_shell = false\n{line}"), line)
        self.assertIsNone(grants.CODEX_MODEL_SETTING.search('[sandbox_workspace_write]\nnetwork_access = true'))


class HarnessRefusalTests(unittest.TestCase):
    """run.py and judge.py refuse before any agent starts; stand-in claude and codex on PATH record any start."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.mark = self.root / "started"
        tools = self.root / "bin"
        tools.mkdir()
        for name in ("claude", "codex"):
            (tools / name).write_text(f'#!/bin/sh\necho {name} >> "{self.mark}"\nexit 1\n')
            (tools / name).chmod(0o755)
        (self.root / "home").mkdir()
        self.env = {**os.environ, "HOME": str(self.root / "home"), "PATH": f"{tools}:{os.environ['PATH']}"}

    def harness(self, script: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", str(EVAL / script), *args], env=self.env, capture_output=True,
                              text=True, timeout=120)

    def run_eval(self, *args: str) -> subprocess.CompletedProcess:
        return self.harness("run.py", "--baseline", str(self.root), "--out", str(self.root / "out"), *args)

    def tearDown(self):
        self.assertFalse(self.mark.exists(), "an agent was started")
        self.assertFalse((self.root / "out").exists(), "the run started")

    def test_run_needs_named_models(self):
        result = self.run_eval("--hosts", "claude")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--claude-model is required", result.stderr)
        result = self.run_eval("--hosts", "claude", "codex", "--claude-model", "opus")
        self.assertIn("--codex-model is required", result.stderr)
        self.assertIn("name the model explicitly", self.run_eval("--hosts", "claude", "--claude-model", "default").stderr)
        result = self.run_eval("--hosts", "codex", "--codex-model", "gpt-6.2-sol", "--candidate-codex-config", 'profile = "astra"')
        self.assertIn("not through config lines", result.stderr)

    def test_run_refuses_top_tier_models_without_a_grant(self):
        for host, model in (("claude", "fable"), ("claude", "claude-fable-5-2"), ("codex", "gpt-6.2-astra")):
            result = self.run_eval("--hosts", host, f"--{host}-model", model)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("ask the user to run, in their own terminal", result.stderr)
            self.assertIn("An agent never creates, edits or works around a grant.", result.stderr)

    def test_judge_needs_named_and_granted_models(self):
        runs = self.root / "runs"
        runs.mkdir()
        (runs / "results.jsonl").write_text("".join(json.dumps({"task": "t01", "host": host, "arm": "candidate", "exit": 0})
                                                    + "\n" for host in ("claude", "codex")))
        self.assertIn("--codex-judge is required", self.harness("judge.py", str(runs), "--claude-judge", "opus").stderr)
        self.assertIn("--claude-judge is required", self.harness("judge.py", str(runs), "--codex-judge", "gpt-6.2-sol").stderr)
        result = self.harness("judge.py", str(runs), "--codex-judge", "gpt-6.2-astra", "--claude-judge", "opus")
        self.assertEqual(result.returncode, 2)
        self.assertIn("astra: 1 runs needed, 0 granted", result.stderr)
        self.assertFalse((runs / "judgments.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
