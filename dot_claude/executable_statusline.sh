#!/usr/bin/env bash
# Claude Code custom status line.
# Reads session context as JSON on stdin; prints a single line to stdout.

input=$(cat)

model=$(printf '%s' "$input" | jq -r '.model.display_name // "Claude"')
cwd=$(printf '%s' "$input"   | jq -r '.workspace.current_dir // .cwd // ""')
project_dir=$(printf '%s' "$input" | jq -r '.workspace.project_dir // empty')
output_style=$(printf '%s' "$input" | jq -r '.output_style.name // empty')
ctx_pct=$(printf '%s' "$input" | jq -r '.context_window.used_percentage // empty')

[ -z "$cwd" ] && cwd="$PWD"

branch=""
dirty_marker=""
ahead_behind=""
if [ -d "$cwd" ] && git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null)
  porcelain=$(git -C "$cwd" --no-optional-locks status --porcelain 2>/dev/null)
  if [ -n "$porcelain" ]; then
    changes=$(printf '%s\n' "$porcelain" | wc -l | tr -d ' ')
    dirty_marker="*${changes}"
  fi
  upstream=$(git -C "$cwd" --no-optional-locks rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)
  if [ -n "$upstream" ]; then
    counts=$(git -C "$cwd" --no-optional-locks rev-list --left-right --count "${upstream}...HEAD" 2>/dev/null)
    behind=$(printf '%s' "$counts" | awk '{print $1}')
    ahead=$(printf '%s' "$counts"  | awk '{print $2}')
    [ "${ahead:-0}"  -gt 0 ] && ahead_behind="${ahead_behind}↑${ahead}"
    [ "${behind:-0}" -gt 0 ] && ahead_behind="${ahead_behind}↓${behind}"
  fi
fi

dir_label="${cwd##*/}"
[ -z "$dir_label" ] && dir_label="$cwd"

R=$'\033[0m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
CYAN=$'\033[36m'
YEL=$'\033[33m'
GRN=$'\033[32m'
MAG=$'\033[35m'
RED=$'\033[31m'

SEP=" ${DIM}|${R} "

line="${BOLD}${CYAN}${model}${R}"
line="${line}${SEP}${YEL}${dir_label}${R}"

if [ -n "$branch" ]; then
  git_part="${GRN}⎇ ${branch}${R}"
  [ -n "$dirty_marker"  ] && git_part="${git_part}${RED}${dirty_marker}${R}"
  [ -n "$ahead_behind"  ] && git_part="${git_part} ${MAG}${ahead_behind}${R}"
  line="${line}${SEP}${git_part}"
fi

if [ -n "$ctx_pct" ] && [ "$ctx_pct" != "null" ]; then
  ctx_int=$(printf '%.0f' "$ctx_pct" 2>/dev/null || printf '%s' "$ctx_pct")
  line="${line}${SEP}${DIM}ctx ${ctx_int}%${R}"
fi

if [ -n "$output_style" ] && [ "$output_style" != "default" ]; then
  line="${line}${SEP}${MAG}${output_style}${R}"
fi

printf '%s\n' "$line"
