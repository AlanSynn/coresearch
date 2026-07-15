#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_HOME_DIR="${CLAUDE_HOME:-$HOME/.claude}"
PROJECT_DIR="$(pwd)"
SCOPE="user"
SURFACE="codex"
MODE="copy"
GLOBAL_BRIDGE=0
PROJECT_BRIDGE=0
FULL_PROJECT_AGENTS=0
FORCE=0

SKILLS=()
while IFS= read -r skill; do
  SKILLS+=("$skill")
done < <(python3 - "$ROOT_DIR/skills/manifest.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for item in data["owned"]:
    print(item["name"])
PY
)
ROLE_SKILLS="$(python3 - "$ROOT_DIR/skills/manifest.json" <<'PY'
import json, sys
names = [item["name"] for item in json.load(open(sys.argv[1]))["owned"] if item["name"] != "coresearch"]
print(", ".join(f"`{name}`" for name in names))
PY
)"
REMOVED_SKILLS=(
  paper-design
  paper-survey
  paper-figures
  paper-rewrite
  paper-review
  paper-proofread
  rebuttal-plan
  claim-check
  pdf-crawl
  research-guidelines
  pptx
  research-pdfs
)

usage() {
  cat <<USAGE
Usage: scripts/install.sh [options]

Install Coresearch skills without replacing your OMX global prompt.

Options:
  --scope user|project       Install to CODEX_HOME skills or project .codex skills. Default: user
  --surface codex|claude|both User/project skill surface. Default: codex
  --codex-home DIR           User-scope Codex home. Default: \${CODEX_HOME:-~/.codex}
  --claude-home DIR          User-scope Claude home. Default: \${CLAUDE_HOME:-~/.claude}
  --project-dir DIR          Project directory for project scope. Default: current directory
  --mode copy|symlink        Copy skill folders or symlink them to this repo. Default: copy
  --global-bridge            Append/update a small bridge block in CODEX_HOME/AGENTS.md
  --project-bridge           Append/update a small bridge block in PROJECT_DIR/AGENTS.md
  --full-project-agents      In project scope, install templates/research/AGENTS.md when none exists
  --force                    Allow replacing existing generated/symlinked skill dirs
  -h, --help                 Show this help

Recommended:
  scripts/install.sh --scope user
  scripts/install.sh --scope user --global-bridge
  scripts/install.sh --scope project --project-dir /path/to/research/repo --project-bridge
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) SCOPE="$2"; shift 2 ;;
    --surface) SURFACE="$2"; shift 2 ;;
    --codex-home) CODEX_HOME_DIR="$2"; shift 2 ;;
    --claude-home) CLAUDE_HOME_DIR="$2"; shift 2 ;;
    --project-dir) PROJECT_DIR="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --global-bridge) GLOBAL_BRIDGE=1; shift ;;
    --project-bridge) PROJECT_BRIDGE=1; shift ;;
    --full-project-agents) FULL_PROJECT_AGENTS=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ "$SCOPE" != "user" && "$SCOPE" != "project" ]]; then
  echo "--scope must be user or project" >&2
  exit 2
fi
if [[ "$SURFACE" != "codex" && "$SURFACE" != "claude" && "$SURFACE" != "both" ]]; then
  echo "--surface must be codex, claude, or both" >&2
  exit 2
fi
if [[ "$MODE" != "copy" && "$MODE" != "symlink" ]]; then
  echo "--mode must be copy or symlink" >&2
  exit 2
fi

if [[ "$SCOPE" == "project" ]]; then
  PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
fi

install_skill() {
  local name="$1"
  local skill_target="$2"
  local src="$ROOT_DIR/skills/$name"
  local dst="$skill_target/$name"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing skill source: $src" >&2
    exit 1
  fi
  mkdir -p "$skill_target"
  if [[ -e "$dst" || -L "$dst" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      rm -rf "$dst"
    elif [[ -L "$dst" ]]; then
      local existing_target
      existing_target="$(symlink_target_abs "$dst" 2>/dev/null || true)"
      if [[ "$existing_target" == "$ROOT_DIR/skills/"* ]]; then
        rm -rf "$dst"
      else
        echo "Skip existing symlink (points outside Coresearch; use --force to replace): $dst" >&2
        return
      fi
    else
      echo "Skip existing skill: $dst (use --force to replace)"
      return
    fi
  fi
  if [[ "$MODE" == "symlink" ]]; then
    ln -s "$src" "$dst"
  else
    mkdir -p "$dst"
    (cd "$src" && tar cf - .) | (cd "$dst" && tar xf -)
  fi
  echo "Installed skill: $dst"
}

install_all_to_target() {
  local skill_target="$1"
  prune_removed_skills "$skill_target"
  for skill in "${SKILLS[@]}"; do
    install_skill "$skill" "$skill_target"
  done
}

symlink_target_abs() {
  local link="$1"
  python3 - "$link" <<'PY'
from pathlib import Path
import os
import sys

link = Path(sys.argv[1])
target = Path(os.readlink(link))
if not target.is_absolute():
    target = link.parent / target
print(target.resolve(strict=False))
PY
}

is_legacy_coresearch_copy() {
  local skill="$1"
  local dst="$2"
  local file="$dst/SKILL.md"
  [[ -f "$file" ]] || return 1
  grep -Eq "^name:[[:space:]]*['\\\"]?$skill['\\\"]?[[:space:]]*$" "$file" || return 1
  if grep -qi 'compatibility shim' "$file"; then
    return 0
  fi
  case "$skill" in
    paper-design) grep -q 'Complete research planning workflow for paper ideas' "$file" ;;
    paper-survey) grep -q 'Verified literature survey and related-work synthesis for research topics' "$file" ;;
    paper-figures) grep -q 'Research figure planning and caption architecture' "$file" ;;
    paper-rewrite) grep -q 'Rewrite research paper sections with venue-aware argument' "$file" ;;
    paper-review) grep -q 'Venue-calibrated simulated review and score forecast for research papers' "$file" ;;
    paper-proofread) grep -q 'Final line-level proofreading workflow for academic manuscripts' "$file" ;;
    rebuttal-plan) grep -q 'Rebuttal and response-planning workflow for research paper reviews' "$file" ;;
    claim-check) grep -q 'Factual verification and hallucination detection for research text' "$file" ;;
    pdf-crawl) grep -q 'Batch-download open-access PDFs for papers listed in a markdown research roadmap' "$file" ;;
    research-guidelines) grep -q 'Compact behavioral guidelines for research assistance' "$file" ;;
    pptx) grep -q 'Coresearch-owned PowerPoint workflow' "$file" ;;
    research-pdfs) grep -q 'Batch-download open-access PDFs for papers listed in a markdown research roadmap or paper list' "$file" ;;
    *) return 1 ;;
  esac
}

prune_removed_skills() {
  local skill_target="$1"
  local skill dst target
  for skill in "${REMOVED_SKILLS[@]}"; do
    dst="$skill_target/$skill"
    if [[ -L "$dst" ]]; then
      target="$(symlink_target_abs "$dst" || true)"
      if [[ ! -e "$dst" || "$target" == "$ROOT_DIR/skills/"* || "$target" == "$ROOT_DIR/skills/$skill" ]]; then
        if [[ "$target" == "$ROOT_DIR/skills/"* || "$target" == "$ROOT_DIR/skills/$skill" ]]; then
          rm -rf "$dst"
          echo "Pruned removed skill alias: $dst"
        else
          echo "WARN: legacy skill-name symlink not pruned because it points outside Coresearch: $dst -> $target" >&2
        fi
      fi
    elif [[ -d "$dst" && -f "$dst/SKILL.md" ]]; then
      if is_legacy_coresearch_copy "$skill" "$dst"; then
        rm -rf "$dst"
        echo "Pruned removed skill alias: $dst"
      else
        echo "WARN: legacy skill-name dir not pruned because it is not a recognized Coresearch copy: $dst" >&2
      fi
    fi
  done
}

bridge_block() {
  cat <<BRIDGE
<!-- RESEARCH_AGENT_SKILLS:START -->
Coresearch skills are installed. For broad academic research tasks, load \`coresearch\` first; for narrow tasks, load the smallest matching skill: $ROLE_SKILLS.
For native subagents or team lanes, use installed OMX agent roles and pass Coresearch stage, skill, field, evidence, scope, validation, confidentiality context, and active Ponytail/Caveman mode when relevant.
Keep research work cumulative in the current thread. Do not create \`.agents/\` chats or paper-state forests. Use \`.omx/\` only for explicit OMX workflows, hooks, recovery, or checkpointing. Verify current venue rules and citations from official/primary sources when exactness matters.
<!-- RESEARCH_AGENT_SKILLS:END -->
BRIDGE
}

upsert_bridge() {
  local file="$1"
  mkdir -p "$(dirname "$file")"
  local tmp
  tmp="$(mktemp)"
  bridge_block > "$tmp"
  if [[ -f "$file" ]]; then
    cp "$file" "$file.bak.$(date +%Y%m%d%H%M%S)"
    python3 - "$file" "$tmp" <<'PY'
from pathlib import Path
import re, sys
path = Path(sys.argv[1])
block = Path(sys.argv[2]).read_text()
text = path.read_text() if path.exists() else ""
pat = re.compile(r"\n?<!-- RESEARCH_AGENT_SKILLS:START -->.*?<!-- RESEARCH_AGENT_SKILLS:END -->\n?", re.S)
if pat.search(text):
    text = pat.sub("\n" + block + "\n", text).rstrip() + "\n"
else:
    text = text.rstrip() + "\n\n" + block + "\n"
path.write_text(text)
PY
  else
    cp "$tmp" "$file"
  fi
  rm -f "$tmp"
  echo "Updated bridge: $file"
}

INSTALLED_TARGETS=()
if [[ "$SCOPE" == "user" ]]; then
  if [[ "$SURFACE" == "codex" || "$SURFACE" == "both" ]]; then
    install_all_to_target "$CODEX_HOME_DIR/skills"
    INSTALLED_TARGETS+=("$CODEX_HOME_DIR/skills")
  fi
  if [[ "$SURFACE" == "claude" || "$SURFACE" == "both" ]]; then
    install_all_to_target "$CLAUDE_HOME_DIR/skills"
    INSTALLED_TARGETS+=("$CLAUDE_HOME_DIR/skills")
  fi
else
  if [[ "$SURFACE" == "codex" || "$SURFACE" == "both" ]]; then
    install_all_to_target "$PROJECT_DIR/.codex/skills"
    INSTALLED_TARGETS+=("$PROJECT_DIR/.codex/skills")
  fi
  if [[ "$SURFACE" == "claude" || "$SURFACE" == "both" ]]; then
    install_all_to_target "$PROJECT_DIR/.claude/skills"
    INSTALLED_TARGETS+=("$PROJECT_DIR/.claude/skills")
  fi
fi

if [[ "$GLOBAL_BRIDGE" -eq 1 || "$PROJECT_BRIDGE" -eq 1 ]]; then
  if command -v omx >/dev/null 2>&1; then
    echo "omx detected: OMX-aware bridge will be applied."
  else
    echo "INFO omx not detected; bridge assumes omx (oh-my-codex). Install via npm/bun then 'omx setup'. Applying anyway (--bridge requested)."
  fi
fi

if [[ "$GLOBAL_BRIDGE" -eq 1 ]]; then
  upsert_bridge "$CODEX_HOME_DIR/AGENTS.md"
fi

if [[ "$PROJECT_BRIDGE" -eq 1 ]]; then
  upsert_bridge "$PROJECT_DIR/AGENTS.md"
fi

if [[ "$FULL_PROJECT_AGENTS" -eq 1 ]]; then
  if [[ "$SCOPE" != "project" ]]; then
    echo "--full-project-agents requires --scope project" >&2
    exit 2
  fi
  if [[ -f "$PROJECT_DIR/AGENTS.md" ]]; then
    echo "Project AGENTS.md already exists; not replacing. Use --project-bridge instead: $PROJECT_DIR/AGENTS.md" >&2
  else
    cp "$ROOT_DIR/templates/research/AGENTS.md" "$PROJECT_DIR/AGENTS.md"
    echo "Installed full research project AGENTS.md: $PROJECT_DIR/AGENTS.md"
  fi
fi

cat <<DONE

Done.
Skill target(s): ${INSTALLED_TARGETS[*]}
Mode: $MODE
Scope: $SCOPE
Surface: $SURFACE

Next:
- User scope: restart Codex/OMX and invoke skills such as \`\$research-design\`, \`\$research-review\`, or \`\$research-loop\`.
- Project scope: run from the project with OMX project setup or CODEX_HOME=.codex, e.g. \`omx setup --scope project --plugin\` or \`CODEX_HOME=.codex omx\`.
DONE
