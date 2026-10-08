# Personal PR review

This skill reviews local Git changes and technical debt inside their affected responsibility domain for the user on their machine. It runs in the existing Codex or Claude Code session and writes local Markdown, JSON, and self-contained HTML reports. A configured hosted model is supported; no separate model server, offline inference setup, or mandatory sandbox infrastructure is required.

Start with [SKILL.md](SKILL.md). [Research and decisions](references/research-and-decisions.md) explains the evidence and implementation choices. [Command contract](references/command-contract.md) documents the runnable helper. [Validation](references/validation.md) describes the verified behavior and limits.

The helper uses Python 3.9+ and local Git with no third-party Python runtime dependencies. The current agent session performs semantic review and selects applicable checks under its existing permissions. The helper prepares evidence and validates supplied results; it does not invoke inference or run arbitrary repository commands.

From this directory:

```sh
python3 -B scripts/review.py prepare --repo /path/to/repository --base main --head HEAD --output /path/to/local-review
```

The output starts INCOMPLETE. Follow the skill to gather relevant evidence, execute applicable checks, challenge findings against counterevidence, and complete `assessment.json`. Then:

```sh
python3 -B scripts/review.py finalize --output /path/to/local-review --assessment /path/to/local-review/assessment.json
```

The main reports are `review.md`, `technical-debt.md`, `findings.json`, and `analysis-summary.json`. A helper exit code of zero during preparation is not a PASS review. Missing native tools, unsupported parser/graph capabilities, unverified intent, and unperformed review work remain explicit.

To use the skill, place the personal-pr-review directory in the agent’s skill discovery location and invoke it from that agent session. Codex UI metadata accompanies portable instructions and scripts. “Personal” identifies the review’s audience and local checkout/report workflow, not where the configured model performs inference.