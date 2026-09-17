#!/usr/bin/env python3
"""Grava o plano aprovado no plan mode em .handoff/plan.md.

Ligado como hook PostToolUse/ExitPlanMode no .claude/settings.local.json. Nunca
falha de forma visível: qualquer erro vai para .handoff/.hook.log e a saída
continua sendo `{}`, para não travar a aprovação do plano.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PLAN_KEYS = ("plan", "plan_text", "planText", "content")


def git(root: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return out.stdout.strip() if out.returncode == 0 else ""


def extract_plan(payload: dict) -> str:
    tool_input = payload.get("tool_input") or {}
    for source in (tool_input, payload):
        for key in PLAN_KEYS:
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return recent_plan_file()


def recent_plan_file() -> str:
    """Fallback: o plan mode também materializa o plano em ~/.claude/plans/."""
    plans = Path.home() / ".claude" / "plans"
    if not plans.is_dir():
        return ""
    recent = [p for p in plans.glob("*.md") if time.time() - p.stat().st_mtime < 600]
    if not recent:
        return ""
    newest = max(recent, key=lambda p: p.stat().st_mtime)
    return newest.read_text(encoding="utf-8").strip()


def issue_number(branch: str) -> str:
    for pattern in (r"issue[-_](\d+)", r"^[a-z]+/(\d+)[-_]"):
        found = re.search(pattern, branch)
        if found:
            return found.group(1)
    return ""


def base_sha(root: Path) -> str:
    for ref in ("origin/main", "main"):
        merge_base = git(root, "merge-base", ref, "HEAD")
        if merge_base:
            return merge_base
    return git(root, "rev-parse", "HEAD")


def environment(root: Path) -> str:
    script = root / "scripts" / "handoff" / "context.sh"
    if not script.is_file():
        return "_(`scripts/handoff/context.sh` ausente neste checkout.)_"
    out = subprocess.run(["bash", str(script)], capture_output=True, text=True, check=False)
    return out.stdout.strip() or "_(sem dados de ambiente.)_"


def archive_previous(handoff: Path) -> None:
    existing = [f for f in ("plan.md", "exec.md", "review.md") if (handoff / f).is_file()]
    if not existing:
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = handoff / "history" / stamp
    destination.mkdir(parents=True, exist_ok=True)
    for name in existing:
        shutil.move(str(handoff / name), str(destination / name))


def render(plan: str, root: Path) -> str:
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD") or "(desconhecida)"

    return f"""---
status: ready
issue: {issue_number(branch) or "null"}
branch: {branch}
base_sha: {base_sha(root)}
generated_at: {datetime.now(timezone.utc).isoformat(timespec="seconds")}
---

# Plano aprovado — `{branch}`

Este arquivo é o contrato desta rodada. Execute o que está aqui, nada além disso.
Ao terminar, escreva `.handoff/exec.md` e commite sem dar push.

## Ambiente

{environment(root)}

## Plano

{plan}
"""


def main() -> int:
    raw = sys.stdin.read()
    handoff = Path.cwd() / ".handoff"
    try:
        payload = json.loads(raw) if raw.strip() else {}
        root_path = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        root = Path(git(Path(root_path), "rev-parse", "--show-toplevel") or root_path)
        handoff = root / ".handoff"
        handoff.mkdir(parents=True, exist_ok=True)

        plan = extract_plan(payload)
        if not plan:
            raise ValueError(f"plano não encontrado no payload (chaves: {sorted(payload)})")

        archive_previous(handoff)
        (handoff / "plan.md").write_text(render(plan, root), encoding="utf-8")
    except Exception as error:  # noqa: BLE001 - o hook nunca pode derrubar o plan mode
        try:
            handoff.mkdir(parents=True, exist_ok=True)
            with (handoff / ".hook.log").open("a", encoding="utf-8") as log:
                log.write(f"{datetime.now(timezone.utc).isoformat()} {error}\n{raw[:2000]}\n\n")
        except OSError:
            pass
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
