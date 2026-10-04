# Context expansion and local history

When a changed function receives different input or produces a different result, identify the consumer that observes the change. Read the changed implementation, the nearest public boundary, and the tests that express its contract. When a caller supplies a surprising input, follow that caller far enough to establish whether the input is reachable. Stop expanding when the behavioral question is answered; do not collect unrelated code quality issues.

Record paths as changed, caller, callee, implementation, interface, test, configuration, coupled, or history. Each context record names the changed responsibility that justifies including it and cites local source evidence. Include parallel implementations when they express the same contract, and state readers/writers when the change moves authority or persistence. A directory neighbor alone is not a demonstrated relationship.

Use direct text/syntax retrieval when local graph tools are unavailable. Installed language servers, SCIP/LSIF indexes, AST tools, or dependency graphs can locate candidates, but verify relevant edges in the pinned source. Record an index's version, source revision, and unsupported language/dynamic behavior. No matches do not prove there are no consumers. Dynamic dispatch, plugin discovery, reflection, generated code, configuration names, serialization, and external consumers require explicit consideration.

The helper extracts Python function/class boundaries through the Python AST and records syntax failures. For other languages, it retains per-file diff hunks and explicitly marks symbol extraction unavailable. The agent uses an installed parser or direct source inspection to fill the context manifest. Do not present heuristic hunk headers as a complete symbol graph. Binary files, submodules, symlinks, LFS pointers, generated files, and sparse paths remain visible in the inventory, with coverage limitations as appropriate.

## History as an answer to a question

When the reviewer needs to understand why a mechanism exists, begin with a specific claim. Inspect local blame for surviving lines, local log and pickaxe searches for additions/removals, and the relevant commit's message and diff. Follow locally available ADRs, tests, comments, and supplied specifications. Missing remote discussions remain missing.

Use EXPLICIT when a local source directly states the reason; CORROBORATED when independent local evidence supports it; INFERRED when the explanation follows from chronology or structure; CONFLICTED when sources disagree; and UNKNOWN when the reason cannot be established. These labels describe rationale provenance separately from finding confidence. A comment can explain an implementation but cannot approve a requirement or decide a tradeoff.

Use a documented, sandboxed local Git command for history when needed. Do not retrieve all historical commits merely to make the packet look complete. Check whether a cached remote-tracking ref or shallow history is enough to answer the question. Local refs carry no claim about the provider's current state.

## Intent and depth

Quick reviews retain the same identity, evidence, and safety requirements while concentrating on the changed behavior and nearby tests. Standard reviews cover the affected responsibility domain across relevant lenses. Deep reviews add material historical questions and structural consequences; depth never grants whole-repository scope. No mode promises a fixed latency or number of findings.

When authoritative intent is unavailable, say: “Specification alignment was not evaluated because no authoritative description of intended behavior was available.” Continue the implementation review. Do not invent acceptance criteria from convenient existing tests. Ask for a missing behavioral decision only when it changes the conclusion.
