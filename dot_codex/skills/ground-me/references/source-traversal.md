# Source traversal

Start from the smallest concrete current target: a symbol, path, interface, schema, behavior, ticket, commit, architectural component, or decision question. Map its current implementation, consumers, tests, contracts, dependencies, ownership, and change surface before claiming why it exists.

Trace Git from the current line or behavior through modifying commits to the introducing change. Use blame as a lead, then inspect path history, `--follow`, pickaxe searches, diffs, branches, merge bases, tags, and releases as appropriate. Resolve the introducing and modifying commits to their pull requests; inspect review conversation and follow-up or revert work.

From the first issue, traverse the selected tracker's parents, children, native relations, project and milestone membership, comments, abandoned alternatives, ownership changes, and successor issues. From there, inspect the contemporaneous approved specification revision, ADRs, architecture views, and earlier implementation specifications. Record chronology so a post-hoc explanation is not mistaken for an originating decision.

Use exact historical documentation only for forces that plausibly came from a dependency, platform, protocol, regulation, or security standard. Compare that version with the current version and mark a removed limitation as expired rather than current.

The packaged scripts can normalize local Git evidence, correlate identifiers found in commit messages, and emit portable decision-graph model data for Figma Design, LikeC4, or Archify. They do not replace readback from the actual repository host, tracker, documentation source, or visual viewer, and their output is evidence to interpret rather than authority.

