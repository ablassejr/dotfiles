# Cross-session resumption

Persist a compact Research Session Manifest at every pause, human checkpoint, and release. It records the request and release identifiers, current phase, root and completed questions, unresolved questions, pinned source snapshot, evidence-graph version, output locations, next action, and model digest. Never place credentials, tokens, or sensitive source contents in it.

On resume, compare the current repository commit, specification release, issue revision, architecture model revision, and external-documentation applicability with the snapshot. Reopen only the questions and downstream projections affected by drift. If the basis has changed materially, stop at `REVISE_FIRST_PRINCIPLES`. If only an output link changed without semantic drift, refresh the manifest without rerunning research.

Conversation memory can help locate the manifest but cannot replace snapshot verification.
