## Principle: Subtractive Code Mass

Maintained first-party code, including production code and tests, is an ongoing correctness, comprehension, review, security, and maintenance obligation.

Every implementation first attempts to satisfy the required behavior by removing obsolete behavior, replacing an existing mechanism, consolidating duplicated mechanisms, reusing an existing capability, or generalizing an existing implementation only where a real variability boundary exists. New code is reserved for irreducible new behavior.

The default code-mass target is:

```text
5 × validated_removed_sloc >= 6 × validated_added_sloc
```

Equivalently, validated removed SLOC divided by validated added SLOC is at least `1.2`. Tests participate in additions and removals. Every positive net maintained-code delta passes the Net Addition Gate and receives explicit human approval.

The target cannot be satisfied by deleting useful tests, comments, or whitespace; compressing readable code; hiding behavior in configuration, generated code, metaprogramming, or a dependency; moving code outside the measured scope; deleting unrelated code; or weakening error handling, validation, observability, typing, security, operations, correctness, or comprehensibility.

When no safe deletion exists, the implementation reports the deficit and requests an explicit controlled exception. It does not manufacture harmful removals.
