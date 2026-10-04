# Research and decisions

## Evidence that supports a decision

Start with the approved intent, affected behavior, pinned baseline, and known unknowns. Find the smallest relevant context that can establish or challenge the claim. Search broadly enough to discover consumers and contradictory evidence; do not equate a narrow search with absence.

For a material claim, record a stable reference, source location or URL, source version/date and retrieval time when relevant, the observation, interpretation, uncertainty, and affected requirement or decision. Keep decisive excerpts short. Label live source evidence, historical rationale, inference, proposal, and unavailable evidence distinctly. Never record secrets in evidence packets.

Follow applicable structural and semantic navigation tools, then verify claims in the source. For chronology, inspect the change that introduced the behavior as well as later modifications. For external contracts, use the exact applicable version and official or other primary sources. A current manual does not necessarily explain an old implementation's original constraint.

Investigate the favored explanation and credible alternatives. Record what would falsify the causal claim or change the design. If evidence conflicts, preserve both sources and explain the conflict's consequence. Do not hide uncertainty behind a confidence score or a large source count.

## Autonomous research gate

Choose one result and explain the decisive evidence, affected records, and next owning action:

| Result | When it applies | Next action |
|---|---|---|
| `REVISE_FIRST_PRINCIPLES` | Evidence changes the underlying problem, desired state, invariant, or approved boundary. | Return to the affected basis decision and preserve the previous basis. |
| `CONTINUE_RESEARCH` | A material factual gap has a credible accessible source or a safe authorized observation that could resolve it. | Perform that investigation and reassess. |
| `REQUEST_HITL` | Progress needs intended product behavior, priorities, risk acceptance, a material tradeoff, or inaccessible privileged evidence. | Ask the actual decision owner one unblocked question, or request the specific missing access. |
| `PROCEED` | The applicable facts are sufficient and another targeted search is unlikely to change a material design decision. | Proceed to design/review while separately respecting unresolved human choices. |

`PROCEED` requires traceability from the mandatory outcome to requirements and from each requirement to authorized intent or a verified constraint. There is no conflict concealed with an invariant or explicit non-goal. Blocking factual claims have applicable evidence. Material contradictions are resolved or explicitly routed to the human frontier. Decision-critical unknowns are resolved or clearly owned there. State why each applicable condition is satisfied.

An inaccessible source is not proof of sufficiency. A timebox, a number of searches, or an aggregate score is not a substitute for this assessment. Do not keep researching when the remaining uncertainty is a human value decision. Factual research readiness does not approve a design or make an unresolved material decision safe to ignore at handoff.

The research result names the next owning action. When a single-PR scope conflict needs a human choice before the basis can change, use `REQUEST_HITL` for that immediate action, identify the affected basis, and preserve it until the choice is made. The overall scope report can simultaneously be `SCOPE_DECISION_REQUIRED`; these describe different parts of the same unresolved work.

## One open-ended decision at a time

Maintain the material questions and their dependencies. Ask a question only when its prerequisites are established. Tell the human what the current situation is, why the choice changes behavior or risk, what the evidence supports, and what remains uncertain. Invite their answer in their own words and offer Ground Me.

Alternatives can clarify consequences, reversibility, complexity, operational risk, and cost. Do not require an exhaustive menu or invent numeric estimates. A recommendation is a proposal with reasons, not a substitute for the human's choice.

Preserve the human's actual answer and actor, the question revision, and supporting evidence. Analyze the answer against the basis and accepted decisions. When clear and consistent, record it and continue without a routine confirmation round.

When a material concern exists, show the specific conflict, evidence, or ambiguity and a suggested change. Challenge your prior recommendation too. The human may retain the answer, revise it freely, correct the assessment, or ask for grounding. A retained answer with acknowledged consequences remains theirs. If it changes an approved invariant, identify that change and follow the proper basis-revision route. Do not silently rewrite the invariant or repeatedly pressure the human to select the agent's preference.

During a genuine decision wait, continue authorized independent research or drafting. Do not fill the unanswered choice with a convenient assumption and advance dependent approval.

## Ground Me: provenance and understanding

Ground Me is available for any material question or uncertain deletion. It explains why the relevant behavior exists, how it evolved, and whether its original forces remain valid. It is not a generic code summary or a disguised vote for the author's preferred design.

Bind the investigation to the suspended question and revision, affected target, approved basis, repository baseline, and known evidence. In managed work, use the current `$ground-me` schemas, process, and response bindings. In standalone work, retain the equivalent facts in the local packet without claiming that a runtime task occurred.

Trace the following sources as they apply to the target:

1. Establish current behavior, callers, dependencies, tests, and affected contracts from the actual baseline.
2. Trace modifying and introducing commits through Git. A later refactor is not necessarily the originating decision.
3. Resolve relevant commits to pull requests and inspect descriptions, reviews, linked issues, reversions, failed approaches, and follow-ups.
4. Traverse relevant issue parents, predecessors, successors, and decision relationships. The rationale may live outside the immediate issue.
5. Compare decision records, ADRs, approved specifications, architecture models, and design artifacts chronologically. Distinguish a documented prior decision from an explanation written after the implementation.
6. Investigate historical external constraints using the version that applied, then check whether the constraint is still current.

Record each source family as examined with findings, searched without a result, unavailable, or not applicable, and say why. Follow a newly discovered rationale link when it could change the decision. Do not manufacture a respected-sounding reason when the trail ends.

Produce a compact grounding packet with a current-state explanation, affected surfaces, evidence timeline, requirement-to-decision-to-code lineage, decisive linked evidence, contradictions, provenance classification, current versus expired forces, uncertainties, and implications for the pending question. Use visuals when they materially help and preserve the applicable rendering rules. A lineage table and prose can communicate a small standalone case without inventing an architecture diagram requirement.

Conduct a distinct provenance review of the raw evidence. Challenge post-hoc intent, mistaken chronology, correlation described as causation, and constraints presumed permanent. Label explicit rationale separately from inference and unknown provenance.

Ask whether the reconstructed understanding matches, needs correction, or needs deeper grounding. A request for deeper grounding continues the investigation while keeping the choice unresolved. A correction updates the packet and any affected interpretation before proceeding.

Alignment alone leaves the decision unanswered. If the human explicitly confirms understanding and answers the decision together, record both actions against the same current packet and question. Accept the answer only after checking that neither binding nor premise changed, then apply the ordinary decision assessment. Do not infer a decision from “that explanation makes sense.”

If the evidence disproves the question's premise, explain that in the packet and complete the understanding alignment. Return `QUESTION_INVALIDATED`, preserve the prior question as history, and recompute the affected frontier. Do not apply the earlier answer to a replacement question. The owning workflow records decisions; the grounding branch returns evidence and actual human responses.

## Deletion and historical behavior

For a deletion candidate, establish its original reason, requirement or incident, current consumers, tests, still-valid constraint, possible replacement, observable semantic effect, and restoration path. Classify it as safe, safe with a verified replacement, requiring grounding, blocked by a current constraint, behavior still required, or unknown.

During specification, a replacement is usually proposed. Planned verification is not proof that it already replaces required behavior. Label the deletion and any size savings accordingly. A managed contract's removal-credit rules remain in force; the local packet cannot grant budget or committed credit. An absence of historical rationale is a gap to assess, not automatic permission to remove behavior.

## Re-entry and evidence expiry

New factual evidence can change the frame, requirement, design, or a prior decision. Identify the earliest affected record, preserve its prior revision, and refresh only dependent work. A presentation correction does not by itself reopen causal analysis. A changed public contract or contradicted approval does.

Record a compact decision history that explains the current outcome without duplicating investigation transcripts. Raw extractions, scratch timelines, temporary diagrams, and search indexes stay outside the implementation tree unless specifically chosen as deliverables. Retain durable conclusions and precise source links in the specification or its authorized existing home.
