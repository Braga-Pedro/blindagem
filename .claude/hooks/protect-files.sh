#!/usr/bin/env bash
# Hook PreToolUse (matcher Edit|Write) — bloqueia edição de arquivos que não deveriam mudar
# durante desenvolvimento normal: pipeline de CI, segredos, certificados, config de produção.
# Adaptado de https://github.com/nick-graham-tx/claude-spring-example (.claude/hooks/protect-files.sh).
#
# Exit 0 libera a edição. Exit 2 bloqueia (Claude vê o erro e para, sem tentar contornar).

set -euo pipefail

RAW_INPUT="$(cat)"
FILE_PATH="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1] or "{}").get("tool_input", {}).get("file_path", ""))' "$RAW_INPUT")"

if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

PROTECTED_PATTERNS=(
    ".github/workflows"
    ".env"
    "application-prod"
    ".pem" ".key" ".jks"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Bloqueado: '$FILE_PATH' bate com o padrão protegido '$pattern' (.claude/hooks/protect-files.sh). Edite manualmente se for intencional." >&2
        exit 2
    fi
done

exit 0
