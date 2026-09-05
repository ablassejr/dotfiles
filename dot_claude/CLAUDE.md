Avoid confirmation bias at all costs. Challenge ideas when they are not supported by first principles.

## User-Approved Requirements

- Do not introduce acceptance criteria or restrictions that haven't been explicitly approved or stated by the user.

## Dedicated Tool Preference

- When a dedicated tool can perform an action, prefer it over invoking Bash or Python for the same work. For example, use the Read tool to inspect files and the Edit tool to make targeted changes. This is guidance, not a prohibition; use Bash or Python when they are the clearer, safer, or more capable choice.

## Repository Analysis and Search

- For any repository or codebase task, invoke `claude-context` first to load relevant project context before taking investigative or implementation actions. Treat its output as context to verify, not as authoritative evidence.

## CLI Documentation Lookup

- Before invoking any CLI, first use `docs-mcp-server` to retrieve the current documentation for that CLI and the intended command, arguments, flags, and side effects.
- Build the invocation from the retrieved documentation; do not guess syntax or rely on memory.
- If the relevant documentation is missing or stale, index or refresh the CLI's official documentation in `docs-mcp-server` and wait for indexing to complete before invoking the CLI. If `docs-mcp-server` is unavailable, report the blocker rather than bypassing this requirement.

## Comments Inform; They Do Not Decide

- Do not put decision-making in comments. Use comments only for relevant context and light reasoning about the applied pattern, use case, framework, constraint, or other non-obvious behavior. Record decisions, alternatives, and material tradeoffs in the appropriate durable artifact instead.

## Documentation Describes the Current State

- Treat every documentation update as current-state documentation. State what the system is and does directly. Do not frame the content as an evolution of, comparison with, or modification to earlier documentation, and do not narrate what was replaced or removed. Prefer `<application> uses <new service>...` to `<application> now uses <new service> and no longer needs <old dependency>...`.

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
