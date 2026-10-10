# Repository Guidelines

## User-Approved Requirements

- Derive minimal, behavior-driven acceptance criteria from the user's stated intent, first principles, and established contracts. Do not introduce new requirements, restrictions, or arbitrary thresholds that the user has not stated or approved.

## Repository Analysis and Search

- For any repository or codebase task, invoke `claude-context` first to load relevant project context before taking investigative or implementation actions. Treat its output as context to verify, not as authoritative evidence.
- Consider the `graphify` skill when repository or codebase analysis, architecture questions, file-relationship investigations, or code searches would benefit from a persistent relationship graph.
- When `graphify-out/graph.json` exists and is relevant to the task, consider querying it before other search tools. Build or update the graph only when graph-based analysis is likely to add useful context; otherwise use the most appropriate search tools directly.

## CLI Documentation Lookup

- Before invoking any CLI, first use `docs-mcp-server` to retrieve the current documentation for that CLI and the intended command, arguments, flags, and side effects.
- Build the invocation from the retrieved documentation; do not guess syntax or rely on memory.
- If the relevant documentation is missing or stale, index or refresh the CLI's official documentation in `docs-mcp-server` and wait for indexing to complete before invoking the CLI. If `docs-mcp-server` is unavailable, report the blocker rather than bypassing this requirement.

## Comments Inform; They Do Not Decide

- Do not put decision-making in comments. Use comments only for relevant context and light reasoning about the applied pattern, use case, framework, constraint, or other non-obvious behavior. Record decisions, alternatives, and material tradeoffs in the appropriate durable artifact instead.

## Documentation Describes the Current State

- Treat every documentation update as current-state documentation. State what the system is and does directly. Do not frame the content as an evolution of, comparison with, or modification to earlier documentation, and do not narrate what was replaced or removed. Prefer `<application> uses <new service>...` to `<application> now uses <new service> and no longer needs <old dependency>...`.

## Documentation Lookups

- Always use the `@arabold/docs-mcp-server` MCP server when checking for documentation. For any library, framework, platform, tool, or API claim — and during any validation, verification, review, or checking — consult the relevant indexed documentation through docs-mcp-server before proceeding.
- If the needed documentation is not indexed, or the docs-mcp-server is not running, inform the user, start the server, index the full relevant documentation corpus, wait until indexing completes, then use the indexed documentation before proceeding.
- Do not rely on training-data recollection for documentation that docs-mcp-server can provide.

This repository contains personal dotfiles managed with `chezmoi`. Source files live here and are rendered into your home directory (e.g., `dot_zshrc` → `~/.zshrc`, `dot_config/nvim/` → `~/.config/nvim/`).

## Project Structure & Module Organization

- Shell: `dot_zshrc`, `dot_bashrc`, `dot_profile` (login/interactive configuration).
- Terminal tools: `dot_tmux.conf`.
- App configs: `dot_config/**` (e.g., `dot_config/ghostty/`, `dot_config/kitty/`, `dot_config/nvim/`).
- Repo-specific guidance: deeper trees may include their own `AGENTS.md` (for Neovim see `dot_config/nvim/AGENTS.md`).

## Build, Test, and Development Commands

Run these from the repo root (`~/.local/share/chezmoi`):

- Preview changes: `chezmoi -S . diff`
- Apply changes: `chezmoi -S . apply`
- One-file edit flow: `chezmoi edit ~/.zshrc` (then `chezmoi apply`)
- Check what’s managed: `chezmoi managed`

## Coding Style & Naming Conventions

- Keep configs OS-appropriate (avoid hardcoded Linux paths in macOS-targeted files).
- Prefer guarded/conditional logic in shell configs (e.g., `command -v brew >/dev/null && …`).
- Indentation: 2 spaces for shell/Lua configs unless the file’s existing style differs.
- Naming: use chezmoi conventions (`dot_*`, `dot_config/<app>/…`) and keep new app configs grouped under `dot_config/<app>/`.

## Testing Guidelines

No automated suite; do quick smoke checks after applying:

- Zsh parse: `zsh -n ~/.zshrc`
- Tmux config: `tmux -f ~/.tmux.conf -L test new -d \; kill-server`
- Neovim config: follow `dot_config/nvim/AGENTS.md`

## Commit & Pull Request Guidelines

- Commit messages in history are short and imperative (commonly `Add …` / `Update …`, occasionally `fix:`). Follow that style and keep messages focused on the primary change.
- Don’t commit machine-local artifacts (e.g., `.DS_Store`, caches, history files).
- PRs: describe intent, list the smoke checks run, and call out any user-visible behavior changes (prompt, keybindings, themes).

## Security & Configuration Tips

- Never commit secrets; prefer `~/.env` (ignored/unmanaged) or environment variables.
- Avoid network actions during shell startup (no `git clone`/auto-install in `dot_zshrc`).


<!-- nx configuration start-->
<!-- Leave the start & end comments to automatically receive updates. -->

## General Guidelines for working with Nx

- For navigating/exploring the workspace, invoke the `nx-workspace` skill first - it has patterns for querying projects, targets, and dependencies
- When running tasks (for example build, lint, test, e2e, etc.), always prefer running the task through `nx` (i.e. `nx run`, `nx run-many`, `nx affected`) instead of using the underlying tooling directly
- Prefix nx commands with the workspace's package manager (e.g., `pnpm nx build`, `npm exec nx test`) - avoids using globally installed CLI
- You have access to the Nx MCP server and its tools, use them to help the user
- For Nx plugin best practices, check `node_modules/@nx/<plugin>/PLUGIN.md`. Not all plugins have this file - proceed without it if unavailable.
- NEVER guess CLI flags - always check nx_docs or `--help` first when unsure

## Scaffolding & Generators

- For scaffolding tasks (creating apps, libs, project structure, setup), ALWAYS invoke the `nx-generate` skill FIRST before exploring or calling MCP tools

## When to use nx_docs

- USE for: advanced config options, unfamiliar flags, migration guides, plugin configuration, edge cases
- DON'T USE for: basic generator syntax (`nx g @nx/react:app`), standard commands, things you already know
- The `nx-generate` skill handles generator discovery internally - don't call nx_docs just to look up generator syntax


<!-- nx configuration end-->

## Post-Edit Memory and Public Interface Reporting

After completing any request that edits files:

- Persist a concise memory of the completed changes and verification in `claude-mem` when available; otherwise use the agent platform's native memory. Never store secrets, credentials, tokens, or other sensitive data in memory.
- In the final user-facing response, include a `Public interface changes` section for every public interface added, removed, changed, or proposed by the request. Identify the interface and file, then show the consumer-facing shape or a realistic usage example, such as a function call, request and response, command invocation, event payload, configuration block, component props, or file or protocol format.
- For a changed public interface, show `before -> after` using shapes or usage examples and explain any compatibility or observable behavior impact. Do not substitute declaration signatures or inventory private helpers, internal objects, or body-only changes that do not affect how callers use the system.
- If no public interface changed or was proposed, explicitly write `Public interface changes: none`.


## Human-Readable Pseudocode for Ideas

When proposing, comparing, or explaining an idea, design, workflow, algorithm, architecture, or behavioral change, use plain-English pseudocode that reads like a natural explanation of what happens from beginning to end. It should feel like normal prose, not a technical rundown, source-code imitation, or checklist of control-flow mechanics.

- Write complete sentences and short paragraphs. Prefer “When the customer submits the form, the application checks whether the required information is present” to `IF`, `ELSE`, `FOR EACH`, arrows, variable declarations, or terse step labels.
- Introduce actors and prerequisites in context, then weave inputs, decisions, state changes, side effects, integrations, failure handling, recovery, and success into the explanation where they matter. Do not catalog those categories mechanically.
- Clearly distinguish current verified behavior, proposed behavior, assumptions, and unresolved choices. Never present proposed behavior as implemented or verified.
- Include material branches, concurrency, edge cases, tradeoffs, and unresolved choices, but describe them as natural alternatives and consequences. Completeness means a reader can understand the behavior and outcomes without translating a technical outline.
- After completing an implementation, include a concise, clearly labeled plain-English pseudocode summary in the final user-facing response. Ground it in the code and verification actually completed, narrate the entry point, key decisions, state changes, side effects, failures, recovery, and observable outcomes naturally, and identify any paths that remain unverified.

## Behavior-Only Testing

Test observable behavior and declared contracts only. Never test implementation details, including in regression tests. This applies to unit, regression, integration, contract, end-to-end, and every other kind of test.

- Use the smallest nonredundant suite of behavior-driven acceptance tests that verifies the stated functionality, fix, or other change. Map the minimal acceptance criteria to observable outcomes and reuse or adapt existing coverage before adding tests. Prefer end-to-end tests through the real user or system entry point when a usable environment can exercise the path. When end-to-end execution is unavailable or impractical, use integration tests through the closest stable public boundary with the real affected components; state the concrete limitation, the boundary exercised, and what remains unverified. Do not silently substitute unit tests or count mocked provider behavior as end-to-end proof. Add separate integration checks only for material contract gaps the selected suite does not exercise, not automatically for every seam. Cover intended success and meaningful in-scope failure or recovery cases without multiplying tests for internal paths or arbitrary coverage quotas.

- Assert positive outcomes at the closest stable public or user-visible boundary, such as returned values, emitted events, rendered output, persisted state, external protocol behavior, or documented errors.
- Do not assert private helpers or state, internal call order or counts, specific internal collaborators, incidental data structures, source text or code patterns, or any other mechanism that can change without changing behavior.
- Mock or fake only true external boundaries and nondeterministic dependencies. Do not mock the internal worker, helper, or unit whose behavior the test is meant to prove.
- Whenever a request touches code or tests, inspect all request-relevant existing tests for violations of this rule. Remove or rewrite any relevant white-box or implementation-coupled tests encountered, preserving or strengthening their intended behavioral coverage without expanding into unrelated tests.
- When a feature fails or errors unexpectedly, do not add an incident-specific regression test as part of the fix. Use the evidence gathered during diagnosis and repair to re-analyze the request-relevant testing strategy, identify the missing observable behavior or declared contract, and rewrite existing tests or create behavioral tests that would have caught that gap.
- Aim for the smallest non-redundant test set that provides 100% behavioral coverage of the affected, enumerated observable contracts and meaningful success and failure paths. Treat 100% as complete coverage of the behavior matrix, not line, branch, function, or implementation coverage. If any relevant behavior cannot be tested, state the uncovered behavior and why.
- Assert the intended positive contract. Use negative assertions only when absence is itself an externally observable requirement.
- If behavior cannot be observed at a stable boundary, improve the production seam or test harness rather than coupling the test to implementation.
