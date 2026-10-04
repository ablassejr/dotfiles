# Adversarial review

Give the reviewer the normalized Research Model, source locators, proposed synthesis, and first-principles basis. Do not provide private chain-of-thought, the desired verdict, suspected defect, or a defense of the recommendation.

Challenge whether cited sources support the claims; chronology is being mistaken for causation; current behavior is being treated as intended behavior; versions and scopes apply; counterevidence or plausible alternatives were omitted; the recommendation merely preserves existing architecture; uncertainty is hidden by polished language or visuals; and additive or subtractive implementation paths were inadequately evaluated.

Use an independent fresh-context reviewer when available and authorized. When it is unavailable, run the same review and record `review_kind: SELF_REVIEWED`. Never represent a self-review as independent.

Classify findings as `EVIDENCE_BLOCKER`, `CONTRADICTION_BLOCKER`, `SCOPE_BLOCKER`, `FIRST_PRINCIPLES_CONFLICT`, `HITL_DECISION_REQUIRED`, `OUTPUT_REVISION_REQUIRED`, or `NONBLOCKING_NOTE`. Route each defect to the earliest repair stage and repeat affected downstream checks. Any unresolved blocker prevents a reviewed release.
