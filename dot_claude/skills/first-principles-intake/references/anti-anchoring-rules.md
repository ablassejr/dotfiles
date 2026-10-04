# Anti-anchoring rules

Allowed inputs are the raw request, the selected ticket's title and stated outcome, directly applicable approved product goals, and explicit constraints from an authoritative source.

Do not expose source code, tests, schemas, current architecture, Git history, pull-request discussion, implementation-oriented ticket history, repository vocabulary, or existing implementation patterns to the intake agent.

The intake may repeat a term the user introduced, but it must not silently import the repository's meaning for that term. It may describe an observable capability, but it must not propose how a component provides it. It may record an explicit hard constraint, but it must not promote a present implementation choice into a constraint.

If the parent already knows the implementation, a separate no-history invocation is the reliable boundary. Passing a prompt that says "ignore what you know" is not equivalent. When isolation cannot be achieved, label the result as restricted-context rather than fresh-context and keep the approval gate visible.

