# Evidence classification

Classify the relationship between a source and a claim.

- `EXPLICIT`: the source directly states or demonstrates the claim.
- `CORROBORATED`: independent applicable evidence supports the same explanation.
- `STRUCTURALLY_DERIVED`: the claim follows from verified dependency, call, ownership, or data-flow structure.
- `CHRONOLOGICALLY_INFERRED`: the claim is inferred from ordering or change history.
- `BEHAVIORALLY_INFERRED`: the claim is inferred from a public contract, behavioral test, or observed outcome.
- `CONFLICTED`: credible applicable evidence supports incompatible conclusions.
- `UNKNOWN`: permitted research has not supplied enough evidence.

`EXPLICIT` describes a link, not a universal confidence level. A direct statement can still be obsolete, out of scope, or contradicted. Confidence combines evidence independence, applicability, completeness, and contradiction status.

Use `single_source`, `corroborated`, `conflicted`, or `unknown` for claim confidence. Do not upgrade an inference to explicit evidence because it is plausible. Preserve excerpts as short locators or hashes where licensing or privacy prevents embedding the text.
