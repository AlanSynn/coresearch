#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_TEMPLATE = ROOT / "templates" / "research" / "AGENTS.md"
SKILL_MANIFEST = ROOT / "skills" / "manifest.json"


def skill_manifest() -> dict:
    return json.loads(SKILL_MANIFEST.read_text())


def owned_skill_names() -> list[str]:
    return [item["name"] for item in skill_manifest()["owned"]]


SKILLS = owned_skill_names()

START = "<!-- RESEARCH_AGENT_SKILLS:START -->"
END = "<!-- RESEARCH_AGENT_SKILLS:END -->"
OMX_SIGNATURE = "# oh-my-codex - Intelligent Multi-Agent Orchestration"
OMX_RUNTIME_MARKER = "<!-- OMX:RUNTIME:START -->"


def codex_home(value: str | None = None) -> Path:
    return Path(value or os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()


def claude_home(value: str | None = None) -> Path:
    return Path(value or os.environ.get("CLAUDE_HOME") or Path.home() / ".claude").expanduser().resolve()


def default_bin_dir() -> Path:
    return Path(os.environ.get("RESEARCH_HARNESS_BIN_DIR") or Path.home() / ".local" / "bin").expanduser().resolve()


def bridge_block() -> str:
    role_skills = ", ".join(f"`{name}`" for name in owned_skill_names() if name != "coresearch")
    return f"""{START}
Research Agent Skills are installed. For broad academic research tasks, load `coresearch` first; for narrow tasks, load the smallest matching skill: {role_skills}.
Keep research work cumulative in the current thread. Do not create `.agents/` chats or paper-state forests. Use `.omx/` only for explicit OMX workflows, hooks, recovery, or checkpointing. Verify current venue rules and citations from official/primary sources when exactness matters.
{END}
"""


def upsert_bridge_text(text: str) -> str:
    block = bridge_block().strip()
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _old, after = rest.split(END, 1)
        return (before.rstrip() + "\n\n" + block + "\n" + after.lstrip()).rstrip() + "\n"
    if text.strip():
        return text.rstrip() + "\n\n" + block + "\n"
    return block + "\n"


def remove_bridge_text(text: str) -> str:
    if START not in text or END not in text:
        return text
    before, rest = text.split(START, 1)
    _old, after = rest.split(END, 1)
    return (before.rstrip() + "\n\n" + after.lstrip()).rstrip() + "\n"


def project_agents_candidate(target: Path, mode: str, replace: bool) -> str:
    path = target / "AGENTS.md"
    current = path.read_text() if path.exists() else ""
    if mode == "bridge":
        return upsert_bridge_text(current)
    if mode == "full":
        return RESEARCH_TEMPLATE.read_text()
    raise ValueError(mode)


def unified_diff(old: str, new: str, fromfile: str, tofile: str) -> str:
    return "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=fromfile, tofile=tofile))


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    idx = 1
    while True:
        candidate = path.with_name(f"{path.name}.bak.{idx}")
        if not candidate.exists():
            shutil.copy2(path, candidate)
            return candidate
        idx += 1


def latest_backup(path: Path) -> Path | None:
    candidates = sorted(path.parent.glob(f"{path.name}.bak.*"), key=lambda p: p.stat().st_mtime if p.exists() else 0)
    return candidates[-1] if candidates else None


def path_has_dir(directory: Path) -> bool:
    paths = os.environ.get("PATH", "").split(os.pathsep)
    return str(directory) in paths


def is_repo_launcher(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False
    try:
        return path.resolve(strict=False) in {(ROOT / "harness").resolve(), (ROOT / "bin" / "harness").resolve(), (ROOT / "scripts" / "harness.py").resolve()}
    except OSError:
        return False


def run(cmd: list[str], *, cwd: Path | None = None) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None)


def arg_target(args: argparse.Namespace) -> str:
    return getattr(args, "target", None) or getattr(args, "target_arg", None) or "."


def add_mode_flags(parser: argparse.ArgumentParser) -> None:
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--mode", choices=["bridge", "full"], dest="mode", default=None, help="legacy explicit mode selector")
    mode.add_argument("--bridge", action="store_const", const="bridge", dest="mode", help="use the small project bridge block")
    mode.add_argument("--full", action="store_const", const="full", dest="mode", help="use the full research AGENTS.md template")
    parser.set_defaults(mode="bridge")


def add_apply_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-y", "--yes", "--apply", dest="apply", action="store_true", help="write changes; explicit commands default to dry-run diff")


def prompt_text(label: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{label}{suffix}: ").strip()
    except EOFError:
        value = ""
    return value or default


def prompt_bool(label: str, default: bool) -> bool:
    marker = "Y/n" if default else "y/N"
    try:
        value = input(f"{label} [{marker}]: ").strip().lower()
    except EOFError:
        value = ""
    if not value:
        return default
    return value in {"y", "yes", "1", "true", "t"}


def prompt_choice(label: str, choices: list[tuple[str, str]], default: str) -> str:
    print(label + ":")
    for idx, (value, description) in enumerate(choices, start=1):
        default_marker = " (default)" if value == default else ""
        print(f"  {idx}) {value}{default_marker} - {description}")
    valid_values = {value for value, _description in choices}
    while True:
        try:
            raw = input(f"Choose [default: {default}]: ").strip().lower()
        except EOFError:
            raw = ""
        if not raw:
            return default
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(choices):
                return choices[idx - 1][0]
        matches = [value for value in valid_values if value.startswith(raw)]
        if len(matches) == 1:
            return matches[0]
        print("Invalid choice. Enter a number or choice name.")


def should_interactive_init(args: argparse.Namespace) -> bool:
    if getattr(args, "interactive", False):
        return True
    raw_argv = getattr(args, "_raw_argv", [])
    return raw_argv == ["init"] and sys.stdin.isatty()


def explicit_init_mode(args: argparse.Namespace) -> str | None:
    raw_argv = getattr(args, "_raw_argv", [])
    for idx, token in enumerate(raw_argv):
        if idx == 0:
            continue
        if token == "--bridge":
            return "bridge"
        if token == "--full":
            return "full"
        if token == "--mode" and idx + 1 < len(raw_argv):
            return raw_argv[idx + 1]
        if token.startswith("--mode="):
            return token.split("=", 1)[1]
    return None


def apply_interactive_init(args: argparse.Namespace) -> None:
    print("# Interactive project setup")
    target = prompt_text("Target directory", arg_target(args))
    mode = prompt_choice(
        "Install mode",
        [
            ("bridge", "preserve AGENTS.md and add a small research bridge block"),
            ("full", "copy templates/research/AGENTS.md as the project AGENTS.md"),
        ],
        explicit_init_mode(args) or "full",
    )
    action = prompt_choice(
        "Action",
        [
            ("dry-run", "preview diff only"),
            ("apply", "write AGENTS.md, creating a backup first when needed"),
        ],
        "apply",
    )
    replace = getattr(args, "replace", False)
    target_path = Path(target).expanduser()
    if mode == "full" and (target_path / "AGENTS.md").exists():
        replace = prompt_bool("Existing AGENTS.md found. Allow full replacement?", replace)

    args.target = target
    args.target_arg = None
    args.mode = mode
    args.apply = action == "apply"
    args.replace = replace
    print()
    print(f"Selected target: {Path(target).expanduser().resolve()}")
    print(f"Selected mode: {args.mode}")
    print(f"Selected action: {'apply' if args.apply else 'dry-run'}")
    if args.mode == "full":
        print(f"Replace existing AGENTS.md: {'yes' if args.replace else 'no'}")
    print()


def assert_no_broken_repo_symlinks() -> list[Path]:
    broken: list[Path] = []
    skip = {".git", "tmp", ".omx", "__pycache__"}
    for path in ROOT.rglob("*"):
        if any(part in skip for part in path.relative_to(ROOT).parts):
            continue
        if path.is_symlink() and not path.exists():
            broken.append(path)
    return broken


def cmd_install(args: argparse.Namespace) -> int:
    script = ROOT / "scripts" / "install.sh"
    cmd = [str(script), "--scope", args.scope, "--surface", args.surface, "--mode", args.mode]
    if args.codex_home:
        cmd += ["--codex-home", str(codex_home(args.codex_home))]
    if args.claude_home:
        cmd += ["--claude-home", str(claude_home(args.claude_home))]
    if args.project_dir:
        cmd += ["--project-dir", str(Path(args.project_dir).expanduser().resolve())]
    if args.global_bridge:
        cmd.append("--global-bridge")
    if args.project_bridge:
        cmd.append("--project-bridge")
    if args.force:
        cmd.append("--force")
    return subprocess.call(cmd)


def cmd_link(args: argparse.Namespace) -> int:
    args.scope = "user"
    args.mode = "symlink"
    args.force = True
    if not hasattr(args, "surface") or not args.surface:
        args.surface = "codex"
    return cmd_install(args)


def cmd_self_install(args: argparse.Namespace) -> int:
    bin_dir = Path(args.bin_dir).expanduser().resolve() if args.bin_dir else default_bin_dir()
    dst = bin_dir / args.name
    src = (ROOT / "scripts" / "harness.py").resolve()
    bin_dir.mkdir(parents=True, exist_ok=True)

    if dst.exists() or dst.is_symlink():
        if is_repo_launcher(dst):
            print(f"Already installed: {dst} -> {dst.resolve(strict=False)}")
        elif args.force:
            backup = backup_file(dst) if dst.exists() and not dst.is_symlink() else None
            if dst.is_dir() and not dst.is_symlink():
                print(f"Refusing to replace directory: {dst}", file=sys.stderr)
                return 3
            dst.unlink()
            dst.symlink_to(src)
            print(f"Installed: {dst} -> {src}")
            if backup:
                print(f"Backup: {backup}")
        else:
            print(f"Refusing to replace existing command: {dst}", file=sys.stderr)
            print("Use --force only if you intentionally want to replace it.", file=sys.stderr)
            return 3
    else:
        dst.symlink_to(src)
        print(f"Installed: {dst} -> {src}")

    if not path_has_dir(bin_dir):
        print(f"WARN: {bin_dir} is not on PATH. Add it to your shell profile to run `{args.name}` globally.")
    else:
        print(f"OK: {bin_dir} is on PATH")
    return 0


def cmd_self_uninstall(args: argparse.Namespace) -> int:
    bin_dir = Path(args.bin_dir).expanduser().resolve() if args.bin_dir else default_bin_dir()
    dst = bin_dir / args.name
    if not dst.exists() and not dst.is_symlink():
        print(f"Not installed: {dst}")
        return 0
    if not is_repo_launcher(dst) and not args.force:
        print(f"Refusing to remove non-research-harness command: {dst}", file=sys.stderr)
        print("Use --force if you intentionally want to remove it.", file=sys.stderr)
        return 3
    dst.unlink()
    print(f"Removed: {dst}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    if should_interactive_init(args):
        apply_interactive_init(args)

    target = Path(arg_target(args)).expanduser().resolve()
    if not target.exists():
        if args.apply:
            target.mkdir(parents=True)
        else:
            print(f"Target does not exist: {target}")
            print("Re-run with --apply to create it.")
            return 2
    path = target / "AGENTS.md"
    old = path.read_text() if path.exists() else ""
    new = project_agents_candidate(target, args.mode, args.replace)
    diff = unified_diff(old, new, str(path) + " (current)", str(path) + f" ({args.mode})")

    print(f"Target: {target}")
    print(f"Mode: {args.mode}")
    print(f"AGENTS.md: {'exists' if path.exists() else 'absent'}")
    if args.mode == "full" and path.exists() and not args.replace and diff:
        print("Refusing to replace existing AGENTS.md without --replace.")
        if diff:
            print("\n--- Diff preview ---")
            print(diff, end="")
        return 3 if args.apply else 0

    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No AGENTS.md changes needed.")

    if not args.apply:
        print("\nDry run only. Re-run with --apply to write changes.")
        return 0

    backup = backup_file(path)
    path.write_text(new)
    print(f"\nWrote: {path}")
    if backup:
        print(f"Backup: {backup}")
    return 0


def cmd_global(args: argparse.Namespace) -> int:
    home = codex_home(args.codex_home)
    path = home / "AGENTS.md"
    old = path.read_text() if path.exists() else ""
    new = remove_bridge_text(old) if args.remove else upsert_bridge_text(old)
    label = "remove-bridge" if args.remove else "bridge"
    diff = unified_diff(old, new, str(path) + " (current)", str(path) + f" ({label})")
    print(f"Global AGENTS: {path}")
    print(f"Mode: {label}")
    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No global AGENTS.md changes needed.")
    if not args.apply:
        print("\nDry run only. Re-run with --apply to write changes.")
        return 0
    home.mkdir(parents=True, exist_ok=True)
    backup = backup_file(path)
    path.write_text(new)
    print(f"\nWrote: {path}")
    if backup:
        print(f"Backup: {backup}")
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    if args.scope == "global":
        path = codex_home(args.codex_home) / "AGENTS.md"
    else:
        path = Path(arg_target(args)).expanduser().resolve() / "AGENTS.md"
    backup = Path(args.backup).expanduser().resolve() if args.backup else latest_backup(path)
    if backup is None or not backup.exists():
        print(f"No backup found for {path}", file=sys.stderr)
        return 2
    old = path.read_text() if path.exists() else ""
    new = backup.read_text()
    diff = unified_diff(old, new, str(path) + " (current)", str(backup) + " (restore)")
    print(f"Rollback target: {path}")
    print(f"Backup: {backup}")
    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No changes needed; current file already equals backup.")
    if not args.apply:
        print("\nDry run only. Re-run with --apply to restore backup.")
        return 0
    pre_restore = backup_file(path)
    path.write_text(new)
    print(f"\nRestored: {path}")
    if pre_restore:
        print(f"Pre-restore backup: {pre_restore}")
    return 0


def skill_status(home: Path) -> list[str]:
    rows: list[str] = []
    for name in SKILLS:
        dst = home / "skills" / name
        src = ROOT / "skills" / name
        expected_skill = src / "SKILL.md"
        if dst.is_symlink():
            try:
                target = dst.resolve(strict=False)
            except OSError:
                target = Path(os.readlink(dst))
            if not dst.exists():
                rows.append(f"{name}: symlink:BROKEN -> {target}")
            elif target != src:
                rows.append(f"{name}: symlink:OTHER -> {target}")
            elif not expected_skill.exists():
                rows.append(f"{name}: symlink:BROKEN missing source SKILL.md -> {target}")
            else:
                rows.append(f"{name}: symlink:OK -> {target}")
        elif dst.exists():
            if (dst / "SKILL.md").exists():
                rows.append(f"{name}: copy/dir -> {dst}")
            else:
                rows.append(f"{name}: dir:BROKEN missing SKILL.md -> {dst}")
        else:
            rows.append(f"{name}: missing")
    return rows


def global_agents_status(home: Path) -> list[str]:
    path = home / "AGENTS.md"
    rows = [f"global AGENTS: {path}"]
    if not path.exists():
        rows.append("  missing")
        return rows
    text = path.read_text(errors="replace")
    is_omx = OMX_SIGNATURE in text and OMX_RUNTIME_MARKER in text
    rows.append(f"  omx-signature: {'yes' if is_omx else 'no'}")
    template = ROOT / "tmp" / "oh-my-codex" / "templates" / "AGENTS.md"
    if template.exists():
        tpl = template.read_text()
        exact = text == tpl
        normalized = text.rstrip("\n") == tpl.rstrip("\n")
        if exact:
            rows.append("  exact-local-template-match: yes")
        elif normalized:
            rows.append("  exact-local-template-match: yes (trailing-newline-only)")
        else:
            rows.append("  exact-local-template-match: no")
    rows.append(f"  research-bridge: {'yes' if START in text and END in text else 'no'}")
    return rows


def cmd_status(args: argparse.Namespace) -> int:
    home = codex_home(args.codex_home)
    target = Path(arg_target(args)).expanduser().resolve()
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {home}")
    print(f"Project target: {target}")
    print()
    for row in global_agents_status(home):
        print(row)
    print()
    project_agents = target / "AGENTS.md"
    if project_agents.exists():
        text = project_agents.read_text(errors="replace")
        print(f"project AGENTS: {project_agents}")
        print(f"  research-bridge: {'yes' if START in text and END in text else 'no'}")
        print(f"  full-research-template: {'yes' if 'OMX Research Agent System' in text else 'no'}")
    else:
        print(f"project AGENTS: missing ({project_agents})")
    print()
    print("Installed research skills:")
    for row in skill_status(home):
        print("  " + row)
    return 0


def read_skill_name_and_description(skill_dir: Path) -> tuple[str, str]:
    skill_file = skill_dir / "SKILL.md"
    name = skill_dir.name
    description = ""
    if not skill_file.exists():
        return name, description
    text = skill_file.read_text(errors="replace")
    if text.startswith("---\n"):
        try:
            frontmatter = text.split("---\n", 2)[1]
        except IndexError:
            frontmatter = ""
        for line in frontmatter.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip("\"'")
    return name, description


def inventory_roots(args: argparse.Namespace) -> list[tuple[str, Path]]:
    codex = codex_home(args.codex_home)
    claude = claude_home(args.claude_home)
    roots: list[tuple[str, Path]] = [
        ("codex-user", codex / "skills"),
        ("codex-system", codex / "skills" / ".system"),
        ("claude-user", claude / "skills"),
    ]
    if args.include_plugins:
        roots.extend(
            [
                ("codex-cache", codex / "plugins" / "cache"),
                ("claude-marketplace", claude / "plugins" / "marketplaces"),
                ("claude-cache", claude / "plugins" / "cache"),
            ]
        )
    return roots


def iter_skill_dirs(root: Path, *, recursive: bool) -> list[Path]:
    if not root.exists():
        return []
    pattern = "**/SKILL.md" if recursive else "*/SKILL.md"
    dirs = {path.parent for path in root.glob(pattern)}
    if not recursive:
        dirs.update(path for path in root.iterdir() if path.is_dir() or path.is_symlink())
    return sorted(dirs)


def classify_skill(name: str, surface: str, manifest: dict, skill_dir: Path) -> str:
    owned = {item["name"] for item in manifest["owned"]}
    companions = {item["name"] for item in manifest.get("companions", [])}
    external = set(manifest.get("external_routes", []))
    preferences = set(manifest.get("preferences", []))
    plugin_surface = surface in {"codex-cache", "claude-marketplace", "claude-cache"}
    if surface == "codex-system":
        return "system"
    if not (skill_dir / "SKILL.md").exists():
        target = str(skill_dir.resolve(strict=False)) if skill_dir.is_symlink() else ""
        if ".orchestra" in target:
            return "legacy-orchestra"
        return "non-skill"
    if name in owned:
        return "plugin-overlap" if plugin_surface else "owned"
    if name in companions:
        return "companion"
    if name in preferences or name.startswith(("caveman", "ponytail")) or name == "cavecrew":
        return "preference"
    if name in external or name.startswith("omx-"):
        return "external-route"
    return "unknown"


def cmd_inventory(args: argparse.Namespace) -> int:
    manifest = skill_manifest()
    print("# Coresearch skill inventory")
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {codex_home(args.codex_home)}")
    print(f"CLAUDE_HOME: {claude_home(args.claude_home)}")
    print()
    print("surface\tclass\tname\tkind\tpath\ttarget\tdescription")
    for surface, root in inventory_roots(args):
        recursive = "plugin" in surface or "marketplace" in surface or "cache" in surface
        for skill_dir in iter_skill_dirs(root, recursive=recursive):
            if ".system" in skill_dir.parts and surface != "codex-system":
                continue
            name, description = read_skill_name_and_description(skill_dir)
            kind = "symlink" if skill_dir.is_symlink() else "dir"
            target = str(skill_dir.resolve(strict=False)) if skill_dir.is_symlink() else ""
            klass = classify_skill(name, surface, manifest, skill_dir)
            print(
                "\t".join(
                    [
                        surface,
                        klass,
                        name,
                        kind,
                        str(skill_dir),
                        target,
                        description.replace("\t", " ")[:160],
                    ]
                )
            )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    home = codex_home(args.codex_home)
    target = Path(arg_target(args)).expanduser().resolve()
    failures: list[str] = []
    warnings: list[str] = []

    print("# Research Harness Doctor")
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {home}")
    print(f"Project target: {target}")
    print()

    global_path = home / "AGENTS.md"
    if not global_path.exists():
        warnings.append("global AGENTS.md missing")
    else:
        text = global_path.read_text(errors="replace")
        if OMX_SIGNATURE in text and OMX_RUNTIME_MARKER in text:
            print("PASS global AGENTS has OMX signature")
        else:
            failures.append("global AGENTS does not look like OMX default")
        if START in text and END in text:
            print("INFO global research bridge installed")
        else:
            print("INFO global research bridge not installed")

    for row in skill_status(home):
        if "symlink:OK" in row:
            print("PASS " + row)
        elif "BROKEN" in row or "missing" in row:
            failures.append("bad skill install: " + row)
        else:
            warnings.append("non-symlink or external skill: " + row)

    broken_repo_links = assert_no_broken_repo_symlinks()
    if broken_repo_links:
        for link in broken_repo_links:
            failures.append(f"broken repo symlink: {link}")
    else:
        print("PASS no broken symlinks in repo")

    command_path = shutil.which(args.command_name)
    if command_path:
        resolved = Path(command_path).resolve(strict=False)
        if resolved in {(ROOT / "harness").resolve(), (ROOT / "bin" / "harness").resolve(), (ROOT / "scripts" / "harness.py").resolve()}:
            print(f"PASS command `{args.command_name}` resolves to this repo: {command_path}")
        else:
            warnings.append(f"command `{args.command_name}` resolves elsewhere: {command_path}")
    else:
        warnings.append(f"command `{args.command_name}` not found on PATH")

    if shutil.which("omx"):
        proc = subprocess.run(["omx", "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode == 0:
            print("PASS omx available: " + proc.stdout.splitlines()[0])
        else:
            warnings.append("omx exists but `omx --version` failed")
    else:
        warnings.append("omx not found on PATH")

    project_agents = target / "AGENTS.md"
    if project_agents.exists():
        text = project_agents.read_text(errors="replace")
        if START in text and END in text:
            print("PASS project AGENTS has research bridge")
        elif "OMX Research Agent System" in text:
            print("PASS project AGENTS is full research template")
        else:
            print("INFO project AGENTS exists without research bridge/full prompt")
    else:
        print("INFO project AGENTS missing")

    if args.validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            failures.append(f"validate.sh failed with exit code {code}")

    print()
    for warning in warnings:
        print("WARN " + warning)
    for failure in failures:
        print("FAIL " + failure)
    if failures:
        print(f"Doctor result: FAIL ({len(failures)} failure(s), {len(warnings)} warning(s))")
        return 1 if args.strict else 0
    print(f"Doctor result: PASS ({len(warnings)} warning(s))")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    if args.pull:
        code = run(["git", "pull", "--ff-only"], cwd=ROOT)
        if code != 0:
            return code
    if not args.no_link:
        link_args = argparse.Namespace(
            codex_home=args.codex_home,
            claude_home=args.claude_home,
            surface=args.surface,
            global_bridge=args.global_bridge,
            project_bridge=False,
            project_dir=None,
            scope="user",
            mode="symlink",
            force=True,
        )
        code = cmd_link(link_args)
        if code != 0:
            return code
    if not args.no_validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            return code
    print("Update complete.")
    return 0


def cmd_repair(args: argparse.Namespace) -> int:
    link_args = argparse.Namespace(
        codex_home=args.codex_home,
        claude_home=getattr(args, "claude_home", None),
        surface=getattr(args, "surface", "codex"),
        global_bridge=args.global_bridge,
        project_bridge=False,
        project_dir=None,
        scope="user",
        mode="symlink",
        force=True,
    )
    code = cmd_link(link_args)
    if code != 0:
        return code
    if not args.no_self_install:
        code = cmd_self_install(argparse.Namespace(bin_dir=args.bin_dir, name=args.name, force=True))
        if code != 0:
            return code
    if not args.no_validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            return code
    doctor_args = argparse.Namespace(
        codex_home=args.codex_home,
        target=arg_target(args),
        target_arg=None,
        command_name=args.name,
        strict=True,
        validate=False,
    )
    return cmd_doctor(doctor_args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness", description="Research Agent Skills install/init/status harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    install = sub.add_parser("install", help="Install skills via scripts/install.sh")
    install.add_argument("--scope", choices=["user", "project"], default="user")
    install.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    install.add_argument("--mode", choices=["copy", "symlink"], default="copy")
    install.add_argument("--codex-home")
    install.add_argument("--claude-home")
    install.add_argument("--project-dir")
    install.add_argument("--global-bridge", action="store_true")
    install.add_argument("--project-bridge", action="store_true")
    install.add_argument("--force", action="store_true")
    install.set_defaults(func=cmd_install)

    link = sub.add_parser("link", help="Symlink user-scope skills so repo edits reflect locally")
    link.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    link.add_argument("--codex-home")
    link.add_argument("--claude-home")
    link.add_argument("--global-bridge", action="store_true")
    link.add_argument("--project-bridge", action="store_true")
    link.add_argument("--project-dir")
    link.set_defaults(func=cmd_link)

    self_install = sub.add_parser("self-install", help="Install the `harness` command into a bin directory")
    self_install.add_argument("--bin-dir")
    self_install.add_argument("--name", default="harness")
    self_install.add_argument("--force", action="store_true")
    self_install.set_defaults(func=cmd_self_install)

    self_uninstall = sub.add_parser("self-uninstall", help="Remove an installed harness command symlink")
    self_uninstall.add_argument("--bin-dir")
    self_uninstall.add_argument("--name", default="harness")
    self_uninstall.add_argument("--force", action="store_true")
    self_uninstall.set_defaults(func=cmd_self_uninstall)

    init = sub.add_parser("init", help="Initialize project AGENTS.md; bare TTY init opens the wizard")
    init.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    init.add_argument("--target", help="target directory (overrides positional target)")
    init.add_argument("-i", "--interactive", action="store_true", help="ask target/mode/action with a small built-in menu")
    add_mode_flags(init)
    add_apply_flag(init)
    init.add_argument("--replace", action="store_true", help="allow full mode to replace existing AGENTS.md")
    init.set_defaults(func=cmd_init)

    diff = sub.add_parser("diff", help="Alias for init/global dry-run diff")
    diff.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    diff.add_argument("--target", help="target directory (overrides positional target)")
    add_mode_flags(diff)
    diff.add_argument("--replace", action="store_true")
    diff.add_argument("--global", dest="global_", action="store_true", help="show global AGENTS bridge diff instead of project diff")
    diff.add_argument("--codex-home")
    diff.set_defaults(func=lambda a: cmd_global(argparse.Namespace(codex_home=a.codex_home, remove=False, apply=False)) if a.global_ else cmd_init(a), apply=False)

    global_cmd = sub.add_parser("global", help="Preview/apply/remove the global research bridge")
    global_cmd.add_argument("--codex-home")
    global_cmd.add_argument("--remove", action="store_true")
    add_apply_flag(global_cmd)
    global_cmd.set_defaults(func=cmd_global)

    rollback = sub.add_parser("rollback", help="Preview/apply rollback from latest AGENTS.md backup")
    rollback.add_argument("--scope", choices=["project", "global"], default="project")
    rollback.add_argument("target_arg", nargs="?", help="target directory for project rollback (default: .)")
    rollback.add_argument("--target", help="target directory (overrides positional target)")
    rollback.add_argument("--codex-home")
    rollback.add_argument("--backup")
    add_apply_flag(rollback)
    rollback.set_defaults(func=cmd_rollback)

    status = sub.add_parser("status", help="Show global/project/skill install status")
    status.add_argument("--codex-home")
    status.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    status.add_argument("--target", help="target directory (overrides positional target)")
    status.set_defaults(func=cmd_status)

    inventory = sub.add_parser("inventory", help="Audit Codex/Claude skills and classify Coresearch ownership")
    inventory.add_argument("--codex-home")
    inventory.add_argument("--claude-home")
    inventory.add_argument("--include-plugins", action="store_true", help="also scan Claude plugin marketplaces/cache")
    inventory.set_defaults(func=cmd_inventory)

    doctor = sub.add_parser("doctor", help="Run install/runtime checks")
    doctor.add_argument("--codex-home")
    doctor.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    doctor.add_argument("--target", help="target directory (overrides positional target)")
    doctor.add_argument("--command-name", default="harness")
    doctor.add_argument("--strict", action="store_true", help="return nonzero on failures")
    doctor.add_argument("--validate", action="store_true", help="also run scripts/validate.sh")
    doctor.set_defaults(func=cmd_doctor)

    repair = sub.add_parser("repair", help="Relink skills, reinstall harness command, validate, and run strict doctor")
    repair.add_argument("target_arg", nargs="?", help="target directory for doctor (default: .)")
    repair.add_argument("--target", help="target directory (overrides positional target)")
    repair.add_argument("--codex-home")
    repair.add_argument("--claude-home")
    repair.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    repair.add_argument("--bin-dir")
    repair.add_argument("--name", default="harness")
    repair.add_argument("--global-bridge", action="store_true")
    repair.add_argument("--no-self-install", action="store_true")
    repair.add_argument("--no-validate", action="store_true")
    repair.set_defaults(func=cmd_repair)

    update = sub.add_parser("update", help="Optionally pull, relink user skills, and validate")
    update.add_argument("--pull", action="store_true", help="run git pull --ff-only before relinking")
    update.add_argument("--codex-home")
    update.add_argument("--claude-home")
    update.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    update.add_argument("--global-bridge", action="store_true")
    update.add_argument("--no-link", action="store_true")
    update.add_argument("--no-validate", action="store_true")
    update.set_defaults(func=cmd_update)
    return p


def main(argv: list[str] | None = None) -> int:
    raw_argv = sys.argv[1:] if argv is None else list(argv)
    parser = build_parser()
    args = parser.parse_args(raw_argv)
    args._raw_argv = raw_argv
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
