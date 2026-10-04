# Evidence ranking

Assign confidence to each material explanation, not to the packet as a rhetorical whole.

- `EXPLICIT` means an authoritative source directly states the rationale.
- `CORROBORATED` means independent sources support the same rationale without a material conflict.
- `INFERRED` means code, chronology, tests, or consequences support the explanation, but no source states it directly.
- `CONFLICTED` means credible sources give incompatible explanations that have not been reconciled.
- `UNKNOWN` means no responsible explanation can be established.

Prefer contemporaneous decision evidence over later recollection. Prefer an approved semantic or architectural source over an implementation comment for intent, and source plus observable behavior over a comment for current state. A test proves protected behavior, not the reason it was chosen. A commit timestamp proves chronology, not causality. Later documentation may be accurate while still being post hoc.

Keep a decisive excerpt short and link it to the exact source. Record contrary evidence alongside supporting evidence. If the strongest support is inference, say so and preserve the facts from which the inference follows.

