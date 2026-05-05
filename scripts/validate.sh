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

python3 -m py_compile skills/pdf-crawl/crawler.py
python3 -m py_compile scripts/harness.py
pass "python utilities compile"

bash -n scripts/install.sh
bash -n scripts/validate.sh
bash -n bin/harness
bash -n harness
pass "shell scripts parse"

python3 - <<'PY'
from pathlib import Path
import json
import re

agents = Path('AGENTS.md').read_text()
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

manifest = json.loads(Path('.codex-plugin/plugin.json').read_text())
assert manifest['skills'] == './skills/'
for forbidden in ('agents', 'prompts', 'hooks'):
    assert forbidden not in manifest, forbidden

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

expected = {
    'claim-check', 'paper-design', 'paper-figures', 'paper-proofread',
    'paper-review', 'paper-rewrite', 'paper-survey', 'pdf-crawl',
    'rebuttal-plan', 'research-engineer', 'research-guidelines',
    'research-loop', 'research-slides'
}
assert set(skills) == expected, sorted(set(skills) ^ expected)
print(f'PASS: skill frontmatter and catalog set ({len(skills)} skills)')
PY

python3 skills/pdf-crawl/crawler.py --help >/tmp/research-skills-pdf-help.txt
grep -q -- '--dry-run' /tmp/research-skills-pdf-help.txt
grep -q -- '--yes-large' /tmp/research-skills-pdf-help.txt
grep -q -- '--allow-publisher-pdf' /tmp/research-skills-pdf-help.txt
pass "pdf-crawl safety flags exposed"

sample_dir="$(mktemp -d)"
cat > "$sample_dir/papers.md" <<'MD'
| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|
| 1 | Attention Is All You Need | Vaswani et al. | NeurIPS | 2017 |
MD
python3 skills/pdf-crawl/crawler.py "$sample_dir/papers.md" --dry-run --limit 1 >/tmp/research-skills-pdf-dryrun.txt
if [[ -d "$sample_dir/pdf" ]] && find "$sample_dir/pdf" -type f | grep -q .; then
  fail "pdf-crawl dry run created PDF files"
fi
pass "pdf-crawl dry run does not download files"

user_home="$(mktemp -d)"
echo "GLOBAL HEADER" > "$user_home/AGENTS.md"
./scripts/install.sh --scope user --codex-home "$user_home" --global-bridge >/tmp/research-skills-install-user-1.txt
[[ -f "$user_home/skills/research-loop/SKILL.md" ]] || fail "user install missing research-loop"
[[ -f "$user_home/skills/pdf-crawl/crawler.py" ]] || fail "user install missing crawler"
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
./scripts/install.sh --scope user --codex-home "$user_link_home" --mode symlink --force >/tmp/research-skills-install-user-symlink.txt
[[ -L "$user_link_home/skills/paper-design" ]] || fail "user symlink install missing paper-design symlink"
[[ -L "$user_link_home/skills/research-loop" ]] || fail "user symlink install missing research-loop symlink"
resolved="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$user_link_home/skills/research-loop")"
[[ "$resolved" == "$ROOT_DIR/skills/research-loop" ]] || fail "user symlink target mismatch: $resolved"
pass "user install symlink mode for repo-auto-update"

harness_home="$(mktemp -d)"
./harness link --codex-home "$harness_home" >/tmp/research-skills-harness-link.txt
[[ -L "$harness_home/skills/research-loop" ]] || fail "harness link did not symlink research-loop"
./harness status --codex-home "$harness_home" --target . >/tmp/research-skills-harness-status.txt
grep -q 'research-loop: symlink:OK' /tmp/research-skills-harness-status.txt || fail "harness status did not report symlink OK"
pass "harness link/status"

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
./harness global --codex-home "$global_home" --apply >/tmp/research-skills-harness-global-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global apply missing bridge"
./harness global --codex-home "$global_home" --remove --apply >/tmp/research-skills-harness-global-remove.txt
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global remove left bridge"
pass "harness global bridge dry/apply/remove"

doctor_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$doctor_home/AGENTS.md"
./harness link --codex-home "$doctor_home" >/tmp/research-skills-harness-doctor-link.txt
./harness doctor --codex-home "$doctor_home" --target . --strict >/tmp/research-skills-harness-doctor.txt
grep -q 'Doctor result: PASS' /tmp/research-skills-harness-doctor.txt || fail "harness doctor did not pass"
pass "harness doctor strict"

update_home="$(mktemp -d)"
./harness update --codex-home "$update_home" --no-validate >/tmp/research-skills-harness-update.txt
[[ -L "$update_home/skills/research-loop" ]] || fail "harness update did not relink skills"
grep -q 'Update complete' /tmp/research-skills-harness-update.txt || fail "harness update did not complete"
pass "harness update relink"

harness_project="$(mktemp -d)"
./harness init --target "$harness_project" --mode bridge >/tmp/research-skills-harness-init-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-init-dry.txt || fail "harness init dry-run did not report dry run"
[[ ! -f "$harness_project/AGENTS.md" ]] || fail "harness init dry-run wrote AGENTS.md"
./harness init --target "$harness_project" --mode bridge --apply >/tmp/research-skills-harness-init-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md" || fail "harness init bridge apply missing bridge"
./harness init --target "$harness_project" --mode bridge --apply >/tmp/research-skills-harness-init-apply-2.txt
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md")"
[[ "$count" == "1" ]] || fail "harness bridge duplicated: $count"
pass "harness init bridge dry/apply/idempotent"

rollback_project="$(mktemp -d)"
printf 'ORIGINAL\n' > "$rollback_project/AGENTS.md"
./harness init --target "$rollback_project" --mode bridge --apply >/tmp/research-skills-harness-rollback-setup.txt
./harness rollback --scope project --target "$rollback_project" >/tmp/research-skills-harness-rollback-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-rollback-dry.txt || fail "harness rollback dry-run missing"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback dry-run modified file"
./harness rollback --scope project --target "$rollback_project" --apply >/tmp/research-skills-harness-rollback-apply.txt
grep -q '^ORIGINAL$' "$rollback_project/AGENTS.md" || fail "rollback did not restore original"
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback left bridge"
pass "harness rollback dry/apply"

harness_full="$(mktemp -d)"
./harness init --target "$harness_full" --mode full --apply >/tmp/research-skills-harness-full.txt
cmp -s AGENTS.md "$harness_full/AGENTS.md" || fail "harness full init did not copy full AGENTS"
pass "harness init full copy"

project_dir="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_dir" --project-bridge --mode symlink >/tmp/research-skills-install-project.txt
[[ -L "$project_dir/.codex/skills/paper-design" ]] || fail "project symlink install missing paper-design symlink"
[[ -L "$project_dir/.codex/skills/research-loop" ]] || fail "project symlink install missing research-loop symlink"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$project_dir/AGENTS.md" || fail "project bridge missing"
pass "project install symlink mode and bridge"

project_full="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_full" --full-project-agents >/tmp/research-skills-install-full-project.txt
cmp -s AGENTS.md "$project_full/AGENTS.md" || fail "full project AGENTS install differs"
pass "full project AGENTS install when absent"

if command -v omx >/dev/null 2>&1; then
  omx --version >/tmp/research-skills-omx-version.txt 2>&1 || fail "omx exists but version failed"
  pass "omx available: $(head -n 1 /tmp/research-skills-omx-version.txt)"
else
  echo "WARN: omx not found on PATH; skipped runtime availability check"
fi

pass "all validations completed"
