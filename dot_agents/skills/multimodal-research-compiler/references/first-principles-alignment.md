# First-principles alignment

Evaluate the recommendation against the approved basis, not against preference for the current architecture.

Determine whether it advances the desired state, addresses the underlying problem, preserves each invariant, avoids unnecessary responsibilities and duplicate authority, and avoids reliance on an accidental or expired constraint. Compare the simplest plausible system that satisfies the evidence.

For implementation research, identify irreducibly new behavior and mechanisms made unnecessary. Estimate additions and safe removals when useful, but treat any code-mass ratio as a diagnostic rather than a target that can override correctness, safety, or the user's scope.

Emit `ALIGNED`, `MISALIGNED`, or `BASIS_REVISION_REQUIRED`, with basis references, supported goals, preserved or violated invariants, unnecessary responsibilities, expired constraints, and any deletion candidates. A material violation blocks release.
