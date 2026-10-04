# Provenance classification

Classify the current state using one value:

- `INTENTIONAL_AND_CURRENT`: evidence shows a deliberate decision whose governing forces remain valid.
- `INTENTIONAL_BUT_POSSIBLY_OBSOLETE`: the decision was deliberate, but one or more supporting forces may have expired.
- `TEMPORARY_WORKAROUND`: evidence identifies a deliberately provisional state.
- `CONSTRAINT_DERIVED`: an external hard boundary substantially determined the state.
- `EMERGENT_OR_INCREMENTAL`: the state accumulated through local changes without one governing decision.
- `ACCIDENTAL`: the state has no meaningful connection to an approved requirement or deliberate decision.
- `POST_HOC_DOCUMENTED`: documentation explains or blesses a state only after implementation, without evidence that it drove the change.
- `CONFLICTED`: credible evidence supports incompatible classifications.
- `UNKNOWN`: the evidence cannot responsibly classify the state.

Classification describes provenance, not whether the current design should survive. Put that implication in `decision_implications`, validated against the approved First-Principles Basis by the parent decision loop.

