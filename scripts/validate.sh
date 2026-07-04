#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

pass() {
  echo "PASS: $*"
}

python3 -m json.tool .codex-plugin/plugin.json >/dev/null
pass "plugin manifest JSON parses"

python3 - <<'PY'
from pathlib import Path

for rel in ("skills/research-pdfs/crawler.py", "scripts/harness.py"):
    text = Path(rel).read_text()
    compile(text, rel, "exec")
PY
pass "python utilities compile without pycache"

bash -n scripts/install.sh
bash -n scripts/validate.sh
bash -n bin/harness
bash -n harness
pass "shell scripts parse"

python3 - <<'PY'
from pathlib import Path
import json
import re

broken = []
files_with_cr = []
skip = {'.git', 'tmp', '.omx', '__pycache__'}
for path in Path('.').rglob('*'):
    parts = set(path.parts)
    if parts & skip:
        continue
    if path.is_symlink() and not path.exists():
        broken.append(str(path))
    if path.is_file() and not path.is_symlink() and (path.suffix in {'.md', '.py', '.sh', '.json'} or path.name == 'harness'):
        if b'\r' in path.read_bytes():
            files_with_cr.append(str(path))
assert not broken, broken
assert not files_with_cr, files_with_cr

readme = Path('README.md').read_text()
assert 'positional target is planned' not in readme
assert 'planned ergonomic alias' not in readme
assert 'harness init              # same as' not in readme
assert '/Users/alansynn' not in readme
assert 'Global skills vs. global AGENTS.md' in readme
assert 'harness link' in readme and 'harness global -y' in readme
assert 'defaults to . / full / apply' in readme

agents = Path('templates/research/AGENTS.md').read_text()
required = [
    '<!-- OMX:RUNTIME:START -->',
    '<!-- OMX:RUNTIME:END -->',
    '<!-- OMX:TEAM:WORKER:START -->',
    '<!-- OMX:TEAM:WORKER:END -->',
]
for marker in required:
    assert marker in agents, marker
assert 'PaperSmith' not in agents
assert '/project_brief.md' not in agents
assert 'Do not create separate `.agents/` chats' in agents
root_agents = Path('AGENTS.md').read_text()
assert 'Coresearch Bundle Development Guidelines' in root_agents
assert 'OMX Research Agent System' not in root_agents

manifest = json.loads(Path('.codex-plugin/plugin.json').read_text())
assert manifest['skills'] == './skills/'
for forbidden in ('agents', 'prompts', 'hooks'):
    assert forbidden not in manifest, forbidden

skill_manifest = json.loads(Path('skills/manifest.json').read_text())
expected = {item['name'] for item in skill_manifest['owned']}
assert 'coresearch' in expected
assert all(Path('skills', name, 'SKILL.md').exists() for name in expected)
assert 'aliases' not in skill_manifest
assert {item['name'] for item in skill_manifest.get('companions', [])}
assert {'caveman', 'ponytail'} <= set(skill_manifest.get('preferences', []))
assert set(skill_manifest.get('external_routes', []))

skills = []
for f in sorted(Path('skills').glob('*/SKILL.md')):
    text = f.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert m, f'Missing frontmatter: {f}'
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    assert fm.get('name') == f.parent.name, (f, fm)
    assert fm.get('description') and len(fm['description']) > 40, f
    skills.append(fm['name'])

assert set(skills) == expected, sorted(set(skills) ^ expected)
print(f'PASS: skill frontmatter and catalog set ({len(skills)} skills)')
PY

python3 skills/research-pdfs/crawler.py --help >/tmp/research-skills-pdf-help.txt
grep -q -- '--dry-run' /tmp/research-skills-pdf-help.txt
grep -q -- '--yes-large' /tmp/research-skills-pdf-help.txt
grep -q -- '--allow-publisher-pdf' /tmp/research-skills-pdf-help.txt
pass "research-pdfs safety flags exposed"

sample_dir="$(mktemp -d)"
cat > "$sample_dir/papers.md" <<'MD'
| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|
| 1 | Attention Is All You Need | Vaswani et al. | NeurIPS | 2017 |
MD
python3 skills/research-pdfs/crawler.py "$sample_dir/papers.md" --dry-run --limit 1 >/tmp/research-skills-pdf-dryrun.txt
if [[ -d "$sample_dir/pdf" ]] && find "$sample_dir/pdf" -type f | grep -q .; then
  fail "research-pdfs dry run created PDF files"
fi
pass "research-pdfs dry run does not download files"

user_home="$(mktemp -d)"
echo "GLOBAL HEADER" > "$user_home/AGENTS.md"
./scripts/install.sh --scope user --codex-home "$user_home" --global-bridge >/tmp/research-skills-install-user-1.txt
[[ -f "$user_home/skills/research-loop/SKILL.md" ]] || fail "user install missing research-loop"
[[ -f "$user_home/skills/research-pdfs/crawler.py" ]] || fail "user install missing crawler"
grep -q 'GLOBAL HEADER' "$user_home/AGENTS.md" || fail "existing global AGENTS content was not preserved"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md" || fail "user bridge missing"
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md")"
[[ "$count" == "1" ]] || fail "user bridge count after first install: $count"
./scripts/install.sh --scope user --codex-home "$user_home" --global-bridge >/tmp/research-skills-install-user-2.txt
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md")"
[[ "$count" == "1" ]] || fail "user bridge duplicated after second install: $count"
ls "$user_home"/AGENTS.md.bak.* >/dev/null 2>&1 || fail "bridge backup missing on second install"
pass "user install copy mode and bridge idempotency"

user_link_home="$(mktemp -d)"
mkdir -p "$user_link_home/skills"
ln -s "$ROOT_DIR/skills/paper-design" "$user_link_home/skills/paper-design"
mkdir -p "$user_link_home/skills/paper-review"
cat > "$user_link_home/skills/paper-review/SKILL.md" <<'MD'
---
name: paper-review
description: Venue-calibrated simulated review and score forecast for research papers.
---
# Paper Review
MD
ln -s "$user_link_home/not-coresearch" "$user_link_home/skills/claim-check"
./scripts/install.sh --scope user --codex-home "$user_link_home" --mode symlink --force >/tmp/research-skills-install-user-symlink.txt 2>/tmp/research-skills-install-user-symlink.err
[[ -L "$user_link_home/skills/research-design" ]] || fail "user symlink install missing research-design symlink"
[[ ! -e "$user_link_home/skills/paper-design" && ! -L "$user_link_home/skills/paper-design" ]] || fail "user symlink install unexpectedly kept paper-design alias"
[[ ! -e "$user_link_home/skills/paper-review" && ! -L "$user_link_home/skills/paper-review" ]] || fail "user symlink install unexpectedly kept copied paper-review alias"
[[ -L "$user_link_home/skills/claim-check" ]] || fail "user symlink install pruned non-Coresearch broken legacy-name symlink"
grep -q 'points outside Coresearch' /tmp/research-skills-install-user-symlink.err || fail "user symlink install did not warn for non-Coresearch broken legacy-name symlink"
[[ -L "$user_link_home/skills/research-loop" ]] || fail "user symlink install missing research-loop symlink"
resolved="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$user_link_home/skills/research-loop")"
[[ "$resolved" == "$ROOT_DIR/skills/research-loop" ]] || fail "user symlink target mismatch: $resolved"
pass "user install symlink mode for repo-auto-update"

harness_copy_home="$(mktemp -d)"
./harness install --scope user --codex-home "$harness_copy_home" >/tmp/research-skills-harness-install-user-copy.txt
[[ -f "$harness_copy_home/skills/research-loop/SKILL.md" ]] || fail "harness install user copy missing research-loop"
[[ ! -L "$harness_copy_home/skills/research-loop" ]] || fail "harness install user copy unexpectedly symlinked research-loop"
pass "harness install user copy mode"

harness_home="$(mktemp -d)"
./harness link --codex-home "$harness_home" >/tmp/research-skills-harness-link.txt
[[ -L "$harness_home/skills/research-loop" ]] || fail "harness link did not symlink research-loop"
./harness status --codex-home "$harness_home" --target . >/tmp/research-skills-harness-status.txt
grep -q 'research-loop: symlink:OK' /tmp/research-skills-harness-status.txt || fail "harness status did not report symlink OK"
pass "harness link/status"

both_codex_home="$(mktemp -d)"
both_claude_home="$(mktemp -d)"
./harness link --surface both --codex-home "$both_codex_home" --claude-home "$both_claude_home" >/tmp/research-skills-harness-link-both.txt
[[ -L "$both_codex_home/skills/coresearch" ]] || fail "harness link both missing codex coresearch"
[[ -L "$both_claude_home/skills/coresearch" ]] || fail "harness link both missing claude coresearch"
[[ -L "$both_claude_home/skills/research-design" ]] || fail "harness link both missing claude research-design"
[[ ! -e "$both_claude_home/skills/paper-design" && ! -L "$both_claude_home/skills/paper-design" ]] || fail "harness link both unexpectedly kept claude paper-design alias"
mkdir -p "$both_codex_home/plugins/cache/vendor/skills/pptx"
cat > "$both_codex_home/plugins/cache/vendor/skills/pptx/SKILL.md" <<'MD'
---
name: pptx
description: External Codex plugin PPTX skill with same name as Coresearch-owned skill.
---
# External PPTX
MD
mkdir -p "$both_claude_home/plugins/marketplaces/vendor/skills/pptx"
cat > "$both_claude_home/plugins/marketplaces/vendor/skills/pptx/SKILL.md" <<'MD'
---
name: pptx
description: External Claude plugin PPTX skill with same name as Coresearch-owned skill.
---
# External PPTX
MD
mkdir -p "$both_codex_home/plugins/cache/vendor/skills/ponytail"
cat > "$both_codex_home/plugins/cache/vendor/skills/ponytail/SKILL.md" <<'MD'
---
name: ponytail
description: External preference skill for over-engineering review.
---
# Ponytail
MD
ln -s "$both_codex_home/.orchestra/skills/old-research" "$both_codex_home/skills/old-research"
./harness inventory --codex-home "$both_codex_home" --claude-home "$both_claude_home" --include-plugins >/tmp/research-skills-harness-inventory-overlap.txt
grep -q $'codex-user\towned\tpptx' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify codex user pptx as owned"
grep -q $'claude-user\towned\tpptx' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify claude user pptx as owned"
grep -q $'codex-cache\tplugin-overlap\tpptx' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify codex cache pptx as plugin-overlap"
grep -q $'claude-marketplace\tplugin-overlap\tpptx' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify marketplace pptx as plugin-overlap"
grep -q $'codex-cache\tpreference\tponytail' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify ponytail as preference"
grep -q $'codex-user\tlegacy-orchestra\told-research' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not surface legacy orchestra symlink"
pass "harness link --surface both"

cmd_bin="$(mktemp -d)"
./harness self-install --bin-dir "$cmd_bin" >/tmp/research-skills-harness-self-install.txt
[[ -L "$cmd_bin/harness" ]] || fail "harness self-install did not create symlink"
"$cmd_bin/harness" status --codex-home "$harness_home" --target . >/tmp/research-skills-installed-command-status.txt
grep -q 'research-loop: symlink:OK' /tmp/research-skills-installed-command-status.txt || fail "installed harness command failed status"
./harness self-uninstall --bin-dir "$cmd_bin" >/tmp/research-skills-harness-self-uninstall.txt
[[ ! -e "$cmd_bin/harness" && ! -L "$cmd_bin/harness" ]] || fail "harness self-uninstall did not remove symlink"
pass "harness self-install/self-uninstall"

global_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$global_home/AGENTS.md"
./harness global --codex-home "$global_home" >/tmp/research-skills-harness-global-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-global-dry.txt || fail "harness global dry-run missing"
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global dry-run wrote file"
./harness global --codex-home "$global_home" -y >/tmp/research-skills-harness-global-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global apply missing bridge"
./harness global --codex-home "$global_home" --remove -y >/tmp/research-skills-harness-global-remove.txt
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global remove left bridge"
pass "harness global bridge dry/apply/remove"

doctor_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$doctor_home/AGENTS.md"
./harness link --codex-home "$doctor_home" >/tmp/research-skills-harness-doctor-link.txt
./harness doctor --codex-home "$doctor_home" --target . --strict >/tmp/research-skills-harness-doctor.txt
grep -q 'Doctor result: PASS' /tmp/research-skills-harness-doctor.txt || fail "harness doctor did not pass"
pass "harness doctor strict"

broken_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$broken_home/AGENTS.md"
./harness link --codex-home "$broken_home" >/tmp/research-skills-harness-broken-link-setup.txt
rm -f "$broken_home/skills/research-loop"
ln -s "$broken_home/does-not-exist" "$broken_home/skills/research-loop"
if ./harness doctor --codex-home "$broken_home" --target . --strict >/tmp/research-skills-harness-broken-link-doctor.txt 2>&1; then
  fail "harness doctor passed with a broken skill symlink"
fi
grep -q 'bad skill install: research-loop: symlink:BROKEN' /tmp/research-skills-harness-broken-link-doctor.txt || fail "harness doctor did not report broken research-loop symlink"
pass "harness doctor rejects broken skill symlinks"

repair_home="$(mktemp -d)"
repair_bin="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$repair_home/AGENTS.md"
./harness repair --codex-home "$repair_home" --bin-dir "$repair_bin" --target . --no-validate >/tmp/research-skills-harness-repair.txt
[[ -L "$repair_home/skills/research-loop" ]] || fail "harness repair did not relink research-loop"
[[ -L "$repair_bin/harness" ]] || fail "harness repair did not install harness command"
grep -q 'Doctor result: PASS' /tmp/research-skills-harness-repair.txt || fail "harness repair did not run strict doctor"
pass "harness repair relink/self-install/doctor"

update_home="$(mktemp -d)"
./harness update --codex-home "$update_home" --no-validate >/tmp/research-skills-harness-update.txt
[[ -L "$update_home/skills/research-loop" ]] || fail "harness update did not relink skills"
grep -q 'Update complete' /tmp/research-skills-harness-update.txt || fail "harness update did not complete"
pass "harness update relink"

update_both_codex_home="$(mktemp -d)"
update_both_claude_home="$(mktemp -d)"
./harness update --surface both --codex-home "$update_both_codex_home" --claude-home "$update_both_claude_home" --no-validate >/tmp/research-skills-harness-update-both.txt
[[ -L "$update_both_codex_home/skills/research-loop" ]] || fail "harness update --surface both missing codex link"
[[ -L "$update_both_claude_home/skills/research-loop" ]] || fail "harness update --surface both missing claude link"
pass "harness update --surface both relink"

harness_project="$(mktemp -d)"
./harness init "$harness_project" --bridge >/tmp/research-skills-harness-init-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-init-dry.txt || fail "harness init dry-run did not report dry run"
[[ ! -f "$harness_project/AGENTS.md" ]] || fail "harness init dry-run wrote AGENTS.md"
./harness init "$harness_project" --bridge -y >/tmp/research-skills-harness-init-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md" || fail "harness init bridge apply missing bridge"
./harness init --target "$harness_project" --mode bridge --apply >/tmp/research-skills-harness-init-apply-2.txt
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md")"
[[ "$count" == "1" ]] || fail "harness bridge duplicated: $count"
target_override_a="$(mktemp -d)"
target_override_b="$(mktemp -d)"
./harness init "$target_override_a" --target "$target_override_b" --bridge -y >/tmp/research-skills-harness-target-override.txt
[[ ! -f "$target_override_a/AGENTS.md" ]] || fail "--target did not override positional target"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$target_override_b/AGENTS.md" || fail "--target override did not write chosen target"
pass "harness init shorthand/target-override bridge dry/apply/idempotent"

noninteractive_init="$(mktemp -d)"
printf 'ORIGINAL\n' > "$noninteractive_init/AGENTS.md"
(cd "$noninteractive_init" && "$ROOT_DIR/harness" init </dev/null) >/tmp/research-skills-harness-init-nontty.txt
grep -q 'Dry run only' /tmp/research-skills-harness-init-nontty.txt || fail "harness init non-TTY did not stay dry-run"
! grep -q 'Interactive project setup' /tmp/research-skills-harness-init-nontty.txt || fail "harness init non-TTY opened wizard"
grep -q '^ORIGINAL$' "$noninteractive_init/AGENTS.md" || fail "harness init non-TTY modified existing AGENTS.md"

wizard_full="$(mktemp -d)"
(cd "$wizard_full" && printf '\n2\n2\n' | "$ROOT_DIR/harness" init --interactive) >/tmp/research-skills-harness-init-wizard.txt
grep -q 'Interactive project setup' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not start"
grep -q 'Selected mode: full' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not select full mode"
grep -q 'Selected action: apply' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not select apply action"
cmp -s templates/research/AGENTS.md "$wizard_full/AGENTS.md" || fail "harness init interactive wizard did not write full template"
pass "harness init non-TTY safe; explicit wizard defaults to . / full / apply"

rollback_project="$(mktemp -d)"
printf 'ORIGINAL\n' > "$rollback_project/AGENTS.md"
./harness init "$rollback_project" --bridge -y >/tmp/research-skills-harness-rollback-setup.txt
./harness rollback --scope project "$rollback_project" >/tmp/research-skills-harness-rollback-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-rollback-dry.txt || fail "harness rollback dry-run missing"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback dry-run modified file"
./harness rollback --scope project "$rollback_project" -y >/tmp/research-skills-harness-rollback-apply.txt
grep -q '^ORIGINAL$' "$rollback_project/AGENTS.md" || fail "rollback did not restore original"
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback left bridge"
pass "harness rollback positional dry/apply"

harness_full="$(mktemp -d)"
./harness init "$harness_full" --full -y >/tmp/research-skills-harness-full.txt
cmp -s templates/research/AGENTS.md "$harness_full/AGENTS.md" || fail "harness full init did not copy research template"
./harness diff "$harness_full" --full >/tmp/research-skills-harness-diff-full.txt
grep -q 'No AGENTS.md changes needed' /tmp/research-skills-harness-diff-full.txt || fail "harness diff positional full did not work"
legacy_full="$(mktemp -d)"
./harness init "$legacy_full" --mode full --apply >/tmp/research-skills-harness-legacy-full.txt
cmp -s templates/research/AGENTS.md "$legacy_full/AGENTS.md" || fail "legacy --mode full --apply did not copy research template"
pass "harness init full shorthand and legacy template copy"

project_dir="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_dir" --project-bridge --mode symlink >/tmp/research-skills-install-project.txt
[[ -L "$project_dir/.codex/skills/research-design" ]] || fail "project symlink install missing research-design symlink"
[[ ! -e "$project_dir/.codex/skills/paper-design" && ! -L "$project_dir/.codex/skills/paper-design" ]] || fail "project symlink install unexpectedly kept paper-design alias"
[[ -L "$project_dir/.codex/skills/research-loop" ]] || fail "project symlink install missing research-loop symlink"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$project_dir/AGENTS.md" || fail "project bridge missing"
pass "project install symlink mode and bridge"

harness_project_install="$(mktemp -d)"
./harness install --scope project --project-dir "$harness_project_install" --project-bridge >/tmp/research-skills-harness-install-project.txt
[[ -f "$harness_project_install/.codex/skills/research-loop/SKILL.md" ]] || fail "harness install project missing research-loop"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$harness_project_install/AGENTS.md" || fail "harness install project bridge missing"
pass "harness install project copy mode and bridge"

project_full="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_full" --full-project-agents >/tmp/research-skills-install-full-project.txt
cmp -s templates/research/AGENTS.md "$project_full/AGENTS.md" || fail "full project AGENTS install differs"
pass "full project AGENTS install when absent"

if command -v omx >/dev/null 2>&1; then
  omx --version >/tmp/research-skills-omx-version.txt 2>&1 || fail "omx exists but version failed"
  pass "omx available: $(head -n 1 /tmp/research-skills-omx-version.txt)"
else
  echo "WARN: omx not found on PATH; skipped runtime availability check"
fi

pass "all validations completed"
