# Review protocol and findings

## Walk the observable behavior

When a user or system reaches the changed entry point, explain what input is accepted, what decisions the application makes, what state it changes, and what the consumer observes. Follow material failure and recovery paths, including retries, cancellation, partial effects, concurrent actors, and compatibility where relevant. Distinguish source-confirmed behavior, executable evidence, proposals, and unverified assumptions.

Compare the change with authoritative local intent where supplied. Do not add requirements or universal architecture preferences. Evaluate the correctness and compatibility of the affected boundary, responsibility ownership, dependency direction, test evidence, and security/reliability consequences. Apply infrastructure analysis only when touched: local definitions can establish permission or dependency changes, but cannot prove live provider state, replacement behavior, deployment success, or effective production access.

For tests, assess returned values, events, persisted state, rendering, external protocols, and documented errors. Check whether the affected user/system boundary has end-to-end evidence and affected seams have integration evidence where the user's repository contract calls for them. Identify tests coupled to private collaborators, call order, internal state, or source text. In this read-only skill, report relevant gaps and a behavioral replacement proposal; do not rewrite tests. Do not require new tests for arbitrary implementation details or count assertions as coverage.

## Separate evidence strength from impact

Severity is BLOCKER, HIGH, MEDIUM, LOW, or INFO. Explain the consequence and reachable trigger; do not assign severity from a keyword. Confidence is CERTAIN, HIGH, MEDIUM, LOW, or CONFLICTED. CERTAIN requires reproducible deterministic proof or direct static proof; HIGH requires strong direct evidence; lower confidence reflects missing confirmation or conflicting evidence. Rationale labels and derivations remain separate.

Every kept finding has local evidence, an observable claim, an actionable recommendation, a PR relationship, and a counterevidence search. A candidate becomes a blocking defect only when it is introduced, worsened, or exposed by the change, is material to correctness or a stated contract, has CERTAIN/HIGH confidence, and survives a fresh-context challenge. Low-confidence serious concerns become explicit unresolved questions and can make the review INCOMPLETE; they do not become definitive defects. Pre-existing neighboring debt is nonblocking.

Counterevidence is not the phrase “none found.” Record what was inspected, what could disprove the claim, and the outcome. Consider alternate consumers, surrounding guards, intentional failure behavior, compatibility promises, feature flags, and relevant tests. Deduplicate by the same root behavioral problem and affected boundary, even when multiple lenses discover it. Corroborating evidence belongs on one finding.

## Fresh-context challenge

Use an independent local context for serious candidates and for the overall conclusion. The challenger reads the pinned raw artifacts and candidate claim without the generation transcript. It tries to demonstrate the reported trigger cannot occur, that the contract permits the behavior, or that omitted evidence changes the result. It also challenges a no-findings conclusion. Preserve its local artifact and identify the findings it covered. Concurrency is optional; context independence is the important property. Never send source to a remote agent.

The finalizing helper validates the challenger receipt and its coverage, but cannot prove that a model used a fresh context or that a semantic judgment is correct. Those are host/agent responsibilities explicitly labeled in the report. A missing fresh context yields INCOMPLETE. No second model is needed merely to run deterministic helpers.

## Local verdict

STALE means source, Git state, selected refs, or pinned evidence changed. HOLD means a supported material defect or a relevant executed deterministic failure remains. INCOMPLETE means a needed check, evidence item, coverage decision, local-host boundary, or challenge is missing. PASS_WITH_DEBT means the selected review work is complete and only nonblocking observations remain. PASS means that work is complete with no kept material observations.

When a known blocker and missing verification coexist, show HOLD and also set `complete` to false with the gaps. Do not hide a deterministic failure behind uncertainty. These are local recommendations. They do not enforce merging or prove anything about remote CI.
