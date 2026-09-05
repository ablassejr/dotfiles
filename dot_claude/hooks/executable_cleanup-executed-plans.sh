#!/bin/sh
INPUT=$(cat)

SKILL=$(printf '%s' "$INPUT" | jq -r '.tool_input.skill // ""')

case "$SKILL" in
  "superpowers:executing-plans"|"executing-plans") ;;
  *) exit 0 ;;
esac

CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // ""')
[ -z "$CWD" ] && CWD="$PWD"

DOCS_DIR="$CWD/docs"
[ -d "$DOCS_DIR" ] || exit 0

UNCOMPLETED=$(grep -rl -- '- \[ \]' "$DOCS_DIR" 2>/dev/null | wc -l | tr -d ' ')
[ "$UNCOMPLETED" -gt 0 ] && exit 0

rm -rf "$DOCS_DIR"
printf 'Cleaned up docs/ — all plans in %s are executed.\n' "$DOCS_DIR" >&2
