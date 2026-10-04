# Personal PR review

This skill framework reviews local Git changes and technical debt inside their affected responsibility domain. It creates local Markdown, JSON, and self-contained HTML reports. It operates under the supplied offline/read-only boundary and has no remote integration or publishing command.

Start with [SKILL.md](SKILL.md). [Research and decisions](references/research-and-decisions.md) explains the evidence and implementation choices. [Command contract](references/command-contract.md) documents the runnable helper. [Validation](references/validation.md) describes the verified behavior and limits.

The package uses Python 3.9+ and local Git; its runtime has no third-party Python dependencies. The agent performs semantic review using a local model host. Repository-native tests and analyzers require an enforcing local execution host; the helper itself prepares evidence and validates supplied results, and does not run arbitrary repository commands.

From this directory:

```sh
python3 -B scripts/review.py prepare --repo /path/to/repository --base main --head HEAD --output /path/to/local-review
```

The output starts INCOMPLETE. Follow the skill to gather relevant evidence, execute applicable checks in the isolated host, challenge findings in a fresh local context, and complete `assessment.json`. Then:

```sh
python3 -B scripts/review.py finalize --output /path/to/local-review --assessment /path/to/local-review/assessment.json
```

The main reports are `review.md`, `technical-debt.md`, `findings.json`, and `analysis-summary.json`. A helper exit code of zero during preparation is not a PASS review. Missing native tools, unsupported parser/graph capabilities, unavailable model isolation, and unverified intent remain explicit.

To use the skill in a compatible agent, place the `personal-pr-review` directory in that agent's skill discovery location. The package includes Codex UI metadata, while the core instructions and scripts remain ordinary local files. A cloud-hosted agent does not meet the locked offline semantic-review requirement simply because the skill is installed.
