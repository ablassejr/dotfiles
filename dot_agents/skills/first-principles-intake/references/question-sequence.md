# Question sequence

Ask only for information the allowed intake inputs do not already contain. Use the sequence to check coverage internally, not to administer a mandatory questionnaire. Explain why each missing fundamental changes the basis and stop asking when it is clear enough for the existing approval. Keep the language at the level of observable outcomes, problems, and invariants.

## Desired state

Ask what observable condition should become true. Preserve user-stated effects without translating them into components or mechanisms.

## Underlying problem

Ask which failure, unmet need, cost, or risk makes the desired state necessary. If the request names only a mechanism, ask the missing outcome or problem question; use a clear answer to resolve related fundamentals without paraphrased follow-up questions.

## Irreducible new behavior

Ask what behavior must exist after the change and cannot be removed from the problem. Describe responsibility and observable effect without guessing files, symbols, services, or code shape.

## Expected simplification

Ask which current responsibility, process, concept, or behavior should disappear or become simpler if the outcome succeeds. A conceptual answer is complete before context loading; the later subtractive analysis locates concrete candidates.

## Invariants

Ask what must remain true and what cannot be compromised. Record only explicit or approved invariants. A likely property of the existing implementation is not an invariant.

## Conditional scope question

Ask for the minimum sufficient change when the request has multiple plausible boundaries or includes work that is not needed to produce the outcome. Skip it when the request already establishes the narrowest acceptable result.

## Conditional proof question

Ask what evidence would demonstrate success when the desired state is not itself observable enough to establish completion. Skip it when the evidence follows directly from the stated outcome.

Ask one material question at a time. Record explicit forbidden tradeoffs with the invariants. When an answer changes an earlier premise, repair that premise before moving forward.
