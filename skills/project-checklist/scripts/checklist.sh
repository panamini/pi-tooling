#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-.}"
OUT_FILE="$ROOT_DIR/project-checklist.md"

cat > "$OUT_FILE" <<'EOF'
# Project Checklist

- [ ] Confirm project setup and dependencies
- [ ] Run tests/lint/typecheck before implementation
- [ ] Add/adjust tests for changed behavior
- [ ] Update docs or comments if behavior changed
- [ ] Review for formatting and edge cases
EOF

echo "Wrote $OUT_FILE"
