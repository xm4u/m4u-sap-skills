#!/bin/zsh
# macOS: double-click, or run from a shell. Reuses a ready bridge when available.
SCRIPT_DIR="${0:A:h}"
exec python3 "$SCRIPT_DIR/java-shell.py" --start "$@"
