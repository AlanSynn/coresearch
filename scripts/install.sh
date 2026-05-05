#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
PROJECT_DIR="$(pwd)"
SCOPE="user"
MODE="copy"
GLOBAL_BRIDGE=0
PROJECT_BRIDGE=0
FULL_PROJECT_AGENTS=0
FORCE=0

SKILLS=(
  claim-check
  paper-design
  paper-figures
  paper-proofread
  paper-review
  paper-rewrite
  paper-survey
  pdf-crawl
  rebuttal-plan
  research-engineer
  research-guidelines
  research-loop
  research-slides
)

usage() {
  cat <<USAGE
Usage: scripts/install.sh [options]

Install Research Agent Skills without replacing your OMX global prompt.

Options:
  --scope user|project       Install to CODEX_HOME skills or project .codex skills. Default: user
  --codex-home DIR           User-scope Codex home. Default: \${CODEX_HOME:-~/.codex}
  --project-dir DIR          Project directory for project scope. Default: current directory
  --mode copy|symlink        Copy skill folders or symlink them to this repo. Default: copy
  --global-bridge            Append/update a small bridge block in CODEX_HOME/AGENTS.md
  --project-bridge           Append/update a small bridge block in PROJECT_DIR/AGENTS.md
  --full-project-agents      In project scope, install this repo's full AGENTS.md when none exists
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
    --codex-home) CODEX_HOME_DIR="$2"; shift 2 ;;
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
if [[ "$MODE" != "copy" && "$MODE" != "symlink" ]]; then
  echo "--mode must be copy or symlink" >&2
  exit 2
fi

if [[ "$SCOPE" == "user" ]]; then
  SKILL_TARGET="$CODEX_HOME_DIR/skills"
else
  PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
  SKILL_TARGET="$PROJECT_DIR/.codex/skills"
fi

install_skill() {
  local name="$1"
  local src="$ROOT_DIR/skills/$name"
  local dst="$SKILL_TARGET/$name"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing skill source: $src" >&2
    exit 1
  fi
  mkdir -p "$SKILL_TARGET"
  if [[ -e "$dst" || -L "$dst" ]]; then
    if [[ "$FORCE" -eq 1 || -L "$dst" ]]; then
      rm -rf "$dst"
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

bridge_block() {
  cat <<'BRIDGE'
<!-- RESEARCH_AGENT_SKILLS:START -->
Research Agent Skills are installed. For academic research tasks, load `research-guidelines` plus the smallest matching skill: `paper-design`, `paper-rewrite`, `paper-review`, `paper-survey`, `claim-check`, `rebuttal-plan`, `paper-figures`, `paper-proofread`, `research-engineer`, `research-loop`, `research-slides`, or `pdf-crawl`.
Keep research work cumulative in the current thread. Do not create `.agents/` chats or paper-state forests. Use `.omx/` only for explicit OMX workflows, hooks, recovery, or checkpointing. Verify current venue rules and citations from official/primary sources when exactness matters.
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

for skill in "${SKILLS[@]}"; do
  install_skill "$skill"
done

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
    cp "$ROOT_DIR/AGENTS.md" "$PROJECT_DIR/AGENTS.md"
    echo "Installed full project AGENTS.md: $PROJECT_DIR/AGENTS.md"
  fi
fi

cat <<DONE

Done.
Skill target: $SKILL_TARGET
Mode: $MODE
Scope: $SCOPE

Next:
- User scope: restart Codex/OMX and invoke skills such as \`\$paper-design\`, \`\$paper-review\`, or \`\$research-loop\`.
- Project scope: run from the project with OMX project setup or CODEX_HOME=.codex, e.g. \`omx setup --scope project --plugin\` or \`CODEX_HOME=.codex omx\`.
DONE
