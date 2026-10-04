---
name: code-mass-auditor
description: Audit planned code-mass budgets and independently verify committed measurements, removal legitimacy, anti-gaming constraints, milestone escrow, and Net Addition Gate evidence for one pull request.
---

# Code mass auditor

Use the project's selected source and work records under [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md). The code-mass and behavioral obligations apply to the approved scope. Commands that require a Linear/Notion manifest or fixed three-person plan apply only to that compatible profile. For other projects, perform and record the same independent normalized measurements, removal-credit checks, budgets, approved exceptions, and behavior verification against the actual source and dependency records using compatible repository tools. Do not fabricate provider fields, require three owners, or claim a packaged CLI result that was not obtained.

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run a planning pass after implementation alignment and before adversarial design review. Use the approved basis and lineage, Code Mass Opportunity Map, confirmed deletion Grounding Packets, proposed Code Mass Contract, dependency changes, planned behavioral verification, and milestone ledger. Verify the estimate, deletion provenance, locality, conceptual simplification, escrow, and any proposed exception without claiming that unbuilt code has been measured. Return `CODE_MASS_TARGETED` only when that planned contract is coherent.

Run a verification pass after a committed head exists and before the final Net Addition Gate. Add the exact repository base and head commits plus completed behavioral verification. Use fresh review context in both passes, and do not accept the implementation author's measurements as evidence by themselves.

For verification under the compatible Linear/Notion plan profile, retrieve current `specflow code-mass-policy` documentation before invoking it. Check out the exact committed head with no tracked modifications, run the repository-selected formatting check through the command, then measure the committed base and head:

```text
specflow code-mass-policy <repository> --base <base> --head <head> --plan <linear-plan.json> --issue <issue-key> --format-command-json '<json-array>' --json
```

The automated report counts normalized first-party production and test SLOC, lists excluded paths and detected renames, cancels pure code movement and formatter-only changes, compares the measured result with the issue's reported contract, evaluates `5R >= 6A`, and invokes the Net Addition Gate when the combined net is positive. Treat that report as measurement evidence, not proof that a deletion is legitimate.

Trace every claimed removal to the same responsibility domain and classify it as `VALID_REMOVAL`, `UNSAFE_REMOVAL`, `REMOVAL_REQUIRES_REPLACEMENT`, `REMOVAL_CREDIT_INVALID`, or `REMOVAL_PROVENANCE_UNKNOWN`. Count only `VALID_REMOVAL` and a `REMOVAL_REQUIRES_REPLACEMENT` whose replacement behavior and Ground Me confirmation are verified. Invalid credit includes useful-test deletion, code compression, relocation, generated-output accounting, dependency laundering, unrelated offsets, weakened safeguards, and abstraction inversion.

Review dependency API and configuration surface, transitive and supply-chain burden, upgrades, runtime behavior, wrappers, failure modes, and operational complexity. Verify that test consolidation preserves or strengthens observable protection; coverage percentage alone is not proof. Compare conceptual authorities and state space before and after so a physically smaller implementation cannot hide a more complex system.

For a positive measured net delta, record the verified measurements and keep the Net Addition Gate `REQUIRED`. The initial verification command may therefore report a pending-gate failure even when its measurements and removal-credit audit are verified. The later gate requires `ALIGNED` first-principles review, adversarial status with no blockers, auditor verification, named task-owner and code-owner approval, applicable security or platform approval, the explicit minimum-responsible-addition confirmation, all required validation and verification records, and one controlled `NET_ADDITION_EXCEPTION`. After those records are complete, repeat the policy assessment using the selected compatible tooling; rerun `code-mass-policy` only for its configured profile; do not treat the planning or initial measurement pass as gate approval.

Return `CODE_MASS_TARGETED`, `CODE_MASS_VERIFIED`, `CODE_MASS_REVISION_REQUIRED`, or `CODE_MASS_BLOCKED`. `CODE_MASS_TARGETED` is planning evidence; only the committed verification pass can return `CODE_MASS_VERIFIED`. Include production, test, and combined estimates or measurements; target deficit or surplus; validated removal total; rejected credit and reason; conceptual-complexity finding; dependency finding; escrow or exception status; exact evidence gaps; and the milestone-ledger update. Never create deletion credit from a different responsibility domain or transfer a deficit to an unrelated milestone.
