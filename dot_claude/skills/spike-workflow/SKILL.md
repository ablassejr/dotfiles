---
name: spike-workflow
description: Run a time-boxed spike or technical investigation with plan-materialization's rigor — approve the question and the decision it unblocks, gather evidence and throwaway experiments, attack the conclusion from fresh context, and deliver a decision-ready answer. Use for "spike", "investigate whether", "evaluate X vs Y", "is it feasible", proof of concept, or technology choice questions where nothing ships yet.
---

# Spike workflow

Answer one question well enough for a named person to decide, then stop. A spike ships knowledge, not behavior. Prototype code from a spike is evidence; it never becomes production code by promotion, because it was built without the specification and review that production code needs.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally or from memory does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. A required stage still pending blocks the answer.

## Human checkpoints

Ask the user only for: approval of the spike basis (stage 1); a material choice that changes what the spike investigates (inside stage 3); and the decision itself (stage 6), which belongs to the person the basis names.

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Spike basis | `$first-principles-intake` | The user approves the question, the decision it unblocks and who makes it, what must stay true for any acceptable answer, and what evidence would settle it. A time box is recorded only if the user states one. |
| 2 | Context | `$post-basis-context-loader`, then `$basis-context-reconciler` | Relevant systems, prior decisions, and versions are pinned. A prior decision that already answers the question ends the spike with that evidence. |
| 3 | Investigation | `$specification-research-loop`, gated by `$speckit-autonomous-research-gate`; `$prototype` for experiments | The gate returns `PROCEED`. Experiments live outside the implementation tree, each tied to the claim it tests, with the observed result recorded. Evidence that could disprove the favored answer was actively sought. |
| 4 | Adversarial review | `$adversarial-specification-review` | The reviewer receives the question, evidence, and conclusion, not the author's reasoning, and tries to disprove the conclusion. Material findings return to stage 3. |
| 5 | Write-up | `$multimodal-research-compiler` | One self-contained answer leads with the conclusion and its confidence, shows the decisive evidence, separates observed results from inference, and states what remains unknown. |
| 6 | Decision | `$human-decision-loop` | The named decider's answer is recorded against the exact write-up revision. If the decision leads to work, `$sdlc-router` classifies that work; the spike does not start it. |

## Results

Report `ANSWERED` with the recorded decision, `INCONCLUSIVE` with the specific evidence still missing and how to get it, or `REFRAMED` when the evidence showed the question itself was wrong, with the successor question for a new basis.
