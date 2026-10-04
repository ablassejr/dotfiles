# Source authority

Choose authority for the claim being established, not for the research project as a whole.

| Claim | Primary authority | Useful corroboration |
|---|---|---|
| Desired product behavior | Approved specification release and First-Principles Basis | Human decision record, accepted risk record |
| Current code behavior | Repository at the pinned commit, public contracts, behavioral tests, runtime evidence | CodeGraph or semantic retrieval |
| Technical rationale | ADR, explicit issue decision, pull-request discussion, review record | Chronology and code inference, clearly labeled |
| Implementation evolution | Git and pull-request history | Issue chronology |
| Planned work and ownership | Current issue, milestone, project, and native relations | Repository branch or pull request |
| Dependency or API guarantee | Exact-version official documentation | Source release notes or conformance tests |
| Alternatives and prior art | Primary external sources | Independent authoritative analysis |
| Formal architecture | Applicable architecture model | Code and runtime evidence |
| Visual communication | The visual artifact | Its referenced Research Model records |
| Whether a constraint still applies | Current implementation and current official documentation | Historical comparison |

Record each source's locator, source class, applicable scope, version or revision, retrieval time, and the claim types it can establish. A supplied file is authoritative only for claims it is positioned to know.

When sources appear to conflict, first test whether they describe different dates, versions, environments, desired versus current behavior, or formal intent versus accidental behavior. If none applies, preserve both claims as a contradiction until evidence or a human decision resolves it.
