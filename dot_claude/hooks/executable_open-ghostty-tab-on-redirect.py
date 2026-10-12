#!/usr/bin/env python3
import json
import os
import re
import shlex
import subprocess
import sys

LONGRUN = re.compile(
    r"(^|[;&|\s])((npm|pnpm|yarn|bun)( run)? (test|build|dev|start|install|ci)|npx (vitest|jest)|vitest|jest|pytest"
    r"|go test|cargo (test|build)|make|mvn|gradle|docker build|docker compose up|docker-compose up|pip install"
    r"|uv (sync|pip install)|brew install|nx (serve|run-many|test|build))([\s;&|]|$)"
)
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
STATEMENT_SEPARATORS = {";", ";;", "&&", "||", "&"}
SEPARATORS = STATEMENT_SEPARATORS | {"|", "|&", "(", ")"}
FILE_REDIRECTS = {">", ">>", "&>", "&>>"}
OPERATOR_CHARS = set("();<>|&")


def strip_heredocs(command):
    kept = []
    pending = []
    for line in command.replace("\\\n", " ").split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        kept.append(line)
        pending.extend(match.group(2) for match in HEREDOC.finditer(line))
    return " ; ".join(kept)


def is_word(token):
    return not set(token) <= OPERATOR_CHARS


def resolve(word, base):
    if re.search(r"[$`*?]", word):
        return None
    word = os.path.expanduser(word)
    if os.path.isabs(word):
        return os.path.normpath(word)
    if base is None:
        return None
    return os.path.normpath(os.path.join(base, word))


def statements(tokens):
    current = []
    depth = 0
    for token in tokens:
        depth += token.count("(") - token.count(")") if set(token) <= OPERATOR_CHARS else 0
        if depth == 0 and token in STATEMENT_SEPARATORS:
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def scan(statement, cwd):
    current = cwd
    target = None
    at_start = True
    i = 0
    while i < len(statement):
        token = statement[i]
        following = statement[i + 1] if i + 1 < len(statement) else None
        if token in SEPARATORS:
            at_start = True
        elif at_start and token == "cd" and following and is_word(following):
            current = resolve(following, current)
            i += 1
            at_start = False
        elif token in FILE_REDIRECTS and following and is_word(following):
            target = resolve(following, current) or target
            i += 1
        elif token == "tee":
            j = i + 1
            while j < len(statement) and statement[j].startswith("-"):
                j += 1
            if j < len(statement) and is_word(statement[j]):
                target = resolve(statement[j], current) or target
            at_start = False
        else:
            at_start = False
        i += 1
    return current, target


def destination(tokens, cwd):
    current = cwd
    found = None
    for statement in statements(tokens):
        if statement[0] == "cd":
            current, _ = scan(statement, current)
            continue
        _, target = scan(statement, current)
        if target and not target.startswith("/dev/") and LONGRUN.search(" ".join(statement)):
            found = target
    return found


def open_tab(path):
    tail = f"tail -n 200 -F {shlex.quote(path)}".replace("\\", "\\\\").replace('"', '\\"')
    script = f'''tell application "Ghostty"
  set cfg to new surface configuration
  set command of cfg to "{tail}"
  if (count of windows) is 0 then
    new window with configuration cfg
  else
    new tab in front window with configuration cfg
  end if
end tell'''
    subprocess.run(["osascript"], input=script, text=True, capture_output=True, timeout=10)


payload = json.load(sys.stdin)
command = strip_heredocs(payload.get("tool_input", {}).get("command", ""))
if not LONGRUN.search(command):
    sys.exit(0)

lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
lexer.whitespace_split = True
try:
    tokens = list(lexer)
except ValueError:
    sys.exit(0)

path = destination(tokens, payload.get("cwd"))
if path is None:
    sys.exit(0)

if os.environ.get("GHOSTTY_TAB_DRY_RUN"):
    print(path)
else:
    open_tab(path)
