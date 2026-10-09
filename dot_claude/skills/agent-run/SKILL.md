---
name: agent-run
description: "Run long-running shell commands (builds, test suites, installs, migrations, dev servers, scrapes) through `agent-run` so the output streams live into a Ghostty window the user can watch while the command runs in the background. Use whenever a command is expected to take more than a minute or two, or when the user wants to see progress in real time."
---

# agent-run

`agent-run <command> [args...]` runs a command, appends its output to a log, and opens a Ghostty window that follows the log so the user sees progress as it happens.

## Usage

Start the command with the Bash tool using `run_in_background: true`:

```bash
agent-run pnpm nx run-many -t test
```

- The log is `/tmp/agent.log`, or the path in `$AGENT_LOG`.
- Each run writes a header line `[timestamp] $ command`, the command output, and a final `[exit N]` line. The `[exit N]` line marks completion and carries the command's exit status.
- `agent-run` exits with the wrapped command's exit status, so the background-task notification reports success or failure.
- Read progress with Read on the log file, or with Monitor for a live wait. The log accumulates across runs, so read from the latest header.

## Ghostty window

- The first run opens a separate Ghostty instance running `tail -n 20 -F <log>`. It opens without taking focus.
- Later runs against the same log reuse that window. Closing the window ends the follow; the next run opens a new one.
- `AGENT_RUN_NO_WINDOW=1 agent-run <command>` skips the window and still writes the log.
- Use a distinct `AGENT_LOG=/tmp/<name>.log` per task to give a task its own log and window.

## Behavior

- The command runs under `script`, so it sees a pseudo-terminal and keeps colored and progress output.
- Standard input is closed, so commands that prompt for input fail instead of waiting.
- Pass the command as separate arguments. Wrap pipelines and compound commands with `sh -c '...'`.
