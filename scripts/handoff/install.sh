#!/usr/bin/env bash
# Instala o mecanismo de handoff Claude <-> Cursor neste checkout. Idempotente:
# rode quantas vezes quiser. Chamado por orca.yaml ao criar um worktree.
#
# Materializa a regra e a skill do Cursor, a skill do Claude, e liga o hook que
# grava o plano aprovado em .handoff/plan.md.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."
ROOT="$(pwd -P)"
TEMPLATES="$ROOT/scripts/handoff/templates"

log() { printf '\033[0;36m[handoff]\033[0m %s\n' "$*"; }

install_file() {
    local source="$1" target="$2"
    mkdir -p "$(dirname "$target")"
    if [[ -f "$target" ]] && cmp -s "$source" "$target"; then
        return
    fi
    cp "$source" "$target"
    log "${target#"$ROOT"/}"
}

install_file "$TEMPLATES/cursor-rule.mdc"  "$ROOT/.cursor/rules/handoff.mdc"
install_file "$TEMPLATES/cursor-skill.md"  "$ROOT/.cursor/skills/executar-plano/SKILL.md"
install_file "$TEMPLATES/claude-skill.md"  "$ROOT/.claude/skills/handoff/SKILL.md"

# O hook vai no settings.local.json (que ja e gitignored) e nao no settings.json,
# que e versionado: assim nenhum arquivo rastreado fica sujo na branch da feature.
python3 - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
settings_path = root / ".claude" / "settings.local.json"
settings_path.parent.mkdir(parents=True, exist_ok=True)

try:
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
except (OSError, ValueError):
    settings = {}

entry = {
    "matcher": "ExitPlanMode",
    "hooks": [
        {
            "type": "command",
            "command": 'python3 "$CLAUDE_PROJECT_DIR/scripts/handoff/write-plan.py"',
            "timeout": 15,
        }
    ],
}

hooks = settings.setdefault("hooks", {})
post = [
    item
    for item in hooks.get("PostToolUse", [])
    if "write-plan.py" not in json.dumps(item)
]
post.append(entry)
hooks["PostToolUse"] = post

settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("[handoff] .claude/settings.local.json (hook ExitPlanMode)")
PY

log "pronto — planos aprovados vao para .handoff/plan.md"
