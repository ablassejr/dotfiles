# Repository Guidelines

## User-Approved Requirements

- Do not introduce acceptance criteria or restrictions that haven't been explicitly approved or stated by the user.

## CLI Documentation Lookup

- Before invoking any CLI, first use `docs-mcp-server` to retrieve the current documentation for that CLI and the intended command, arguments, flags, and side effects.
- Build the invocation from the retrieved documentation; do not guess syntax or rely on memory.
- If the relevant documentation is missing or stale, index or refresh the CLI's official documentation in `docs-mcp-server` and wait for indexing to complete before invoking the CLI. If `docs-mcp-server` is unavailable, report the blocker rather than bypassing this requirement.

## Comments Inform; They Do Not Decide

- Do not put decision-making in comments. Use comments only for relevant context and light reasoning about the applied pattern, use case, framework, constraint, or other non-obvious behavior. Record decisions, alternatives, and material tradeoffs in the appropriate durable artifact instead.

## Documentation Describes the Current State

- Treat every documentation update as current-state documentation. State what the system is and does directly. Do not frame the content as an evolution of, comparison with, or modification to earlier documentation, and do not narrate what was replaced or removed. Prefer `<application> uses <new service>...` to `<application> now uses <new service> and no longer needs <old dependency>...`.

This repository contains personal dotfiles managed with `chezmoi`, targeting macOS on
Apple Silicon and Intel. It keeps a MacBook and a Mac mini on the same development
environment. Source files live here and are rendered into your home directory
(e.g., `dot_zshrc` → `~/.zshrc`, `dot_config/nvim/` → `~/.config/nvim/`).

## Project Structure & Module Organization

- Shell: `dot_zshrc`, `dot_zprofile`, `dot_bashrc`, `dot_bash_profile`, `dot_profile`.
  `dot_profile` owns PATH construction for every shell; `dot_zprofile` owns the
  interactive zsh setup.
- Secrets: `encrypted_private_dot_zshenv.age` → `~/.zshenv`, age-encrypted at rest and
  written with mode `0600`.
- Terminal tools: `dot_tmux.conf`.
- Git: `dot_gitconfig` holds the entire global config. Git reads
  `~/.config/git/config` first and `~/.gitconfig` second, and `git config --global`
  writes to `~/.gitconfig`, so one file avoids both shadowing and drift.
  `dot_config/git/ignore` stays separate as git's default `core.excludesFile`.
- Toolchain: `dot_config/mise/config.toml` pins global tool versions.
- App configs: `dot_config/**` (`dot_config/ghostty/`, `dot_config/nvim/`,
  `dot_config/nvim-personal/`, `dot_config/zed/`, `dot_config/mcphub/`,
  `dot_config/gh-dash/`, `dot_config/lazygit/`, `dot_config/direnv/`).
- Secret-bearing configs are added with `chezmoi add --encrypt` and carry
  `private_`: `~/mise.toml`, `~/.npmrc`, `~/.codex/config.toml`,
  `~/.config/opencode/opencode.json`, `~/.config/zed/settings.json`.
- Agent configs: `dot_claude/` → `~/.claude/`. `dot_claude/settings.json.tmpl` is a
  template so absolute paths derive from `.chezmoi.homeDir`.
- Repo tooling, excluded from the home directory via `.chezmoiignore`: `AGENTS.md`,
  `WARP.md`, `README.md`, `Brewfile`.
- Repo-specific guidance: deeper trees may include their own `AGENTS.md` (for Neovim
  see `dot_config/nvim/AGENTS.md`).

## Machine Portability

- `.chezmoi.toml.tmpl` generates the chezmoi config on `chezmoi init`, including the
  age encryption settings. The age identity (`~/.config/chezmoi/key.txt`) is not in the
  repository and must be copied to a new machine out of band.
- `.chezmoiversion` pins the minimum chezmoi version so both machines resolve the
  source state identically.
- `Brewfile` is the package manifest. `brew bundle --file=Brewfile` syncs a machine;
  `brew bundle check --file=Brewfile` reports drift.
- Prefer runtime guards over templates where a shell can test for itself. `path_prepend`
  skips missing directories, and `dot_zprofile` probes both Homebrew prefixes, so one
  file serves Apple Silicon and Intel without branching.

## Build, Test, and Development Commands

Run these from the repo root (`~/.local/share/chezmoi`):

- Preview changes: `chezmoi -S . diff`
- Apply changes: `chezmoi -S . apply`
- One-file edit flow: `chezmoi edit ~/.zshrc` (then `chezmoi apply`)
- Edit encrypted secrets: `chezmoi edit ~/.zshenv` (decrypts and re-encrypts around your editor)
- Check what is managed: `chezmoi managed`

## Coding Style & Naming Conventions

- macOS only. Do not add Linux-specific configuration, paths, or window-manager files.
- Prefer guarded/conditional logic in shell configs (e.g., `command -v brew >/dev/null && …`).
- Indentation: 2 spaces for shell/Lua configs unless the file's existing style differs.
- Naming: use chezmoi conventions (`dot_*`, `dot_config/<app>/…`) and keep new app configs
  grouped under `dot_config/<app>/`. For a regular file the prefix order is `encrypted_`,
  `private_`, `readonly_`, `empty_`, `executable_`, `dot_`.

## Testing Guidelines

No automated suite; do quick smoke checks after applying:

- Zsh parse: `zsh -n ~/.zshrc` and `zsh -n ~/.zprofile`
- Bash parse: `bash -n ~/.bashrc`
- Tmux config: `tmux -f ~/.tmux.conf -L test new -d && tmux -L test kill-server`
- Ghostty config: `ghostty +validate-config --config-file=dot_config/ghostty/config`
- Rendered templates: `chezmoi execute-template < dot_claude/settings.json.tmpl | python3 -m json.tool`
- Neovim config: follow `dot_config/nvim/AGENTS.md`

## Commit & Pull Request Guidelines

- Commit messages in history are short and imperative (commonly `Add …` / `Update …`,
  occasionally `fix:`). Follow that style and keep messages focused on the primary change.
- Don't commit machine-local artifacts (e.g., `.DS_Store`, caches, history files).
- PRs: describe intent, list the smoke checks run, and call out any user-visible behavior
  changes (prompt, keybindings, themes).

## Security & Configuration Tips

- **This repository is public.** Anything committed here is world-readable and stays in
  the git history after deletion. Treat every addition as a publication.
- Secrets belong in `encrypted_private_dot_zshenv.age`, edited via `chezmoi edit ~/.zshenv`.
  Never write a credential into a plaintext source file, and never paste one into a
  commit message or an alias.
- Add new secret-bearing files with `chezmoi add --encrypt`, and include the `private_`
  attribute so the rendered target is mode `0600`.
- Host names, IP addresses, and account identifiers are also disclosures. Reference them
  through variables set in the encrypted environment rather than inlining them.
- Avoid network actions during shell startup (no `git clone`/auto-install in `dot_zprofile`).

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

- Every feature must have at least one end-to-end test that exercises its observable behavior at the user or system boundary.
- Every seam between components, services, or external systems must have at least one integration test that exercises the declared contract across that seam.

- Assert positive outcomes at the closest stable public or user-visible boundary, such as returned values, emitted events, rendered output, persisted state, external protocol behavior, or documented errors.
- Do not assert private helpers or state, internal call order or counts, specific internal collaborators, incidental data structures, source text or code patterns, or any other mechanism that can change without changing behavior.
- Mock or fake only true external boundaries and nondeterministic dependencies. Do not mock the internal worker, helper, or unit whose behavior the test is meant to prove.
- Whenever a request touches code or tests, inspect all request-relevant existing tests for violations of this rule. Remove or rewrite any relevant white-box or implementation-coupled tests encountered, preserving or strengthening their intended behavioral coverage without expanding into unrelated tests.
- When a feature fails or errors unexpectedly, do not add an incident-specific regression test as part of the fix. Use the evidence gathered during diagnosis and repair to re-analyze the request-relevant testing strategy, identify the missing observable behavior or declared contract, and rewrite existing tests or create behavioral tests that would have caught that gap.
- Aim for the smallest non-redundant test set that provides 100% behavioral coverage of the affected, enumerated observable contracts and meaningful success and failure paths. Treat 100% as complete coverage of the behavior matrix, not line, branch, function, or implementation coverage. If any relevant behavior cannot be tested, state the uncovered behavior and why.
- Assert the intended positive contract. Use negative assertions only when absence is itself an externally observable requirement.
- If behavior cannot be observed at a stable boundary, improve the production seam or test harness rather than coupling the test to implementation.
