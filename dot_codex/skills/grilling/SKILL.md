---
name: grilling
description: Stress-test a plan or idea when the user requests an interview; within the epic framework, resolve only remaining material human choices after first principles.
---

For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


When the user explicitly requests a broad stress-test, explore the material assumptions within that request. Within the epic framework after first principles, use a focused decision conversation and stop when the current consequential choice is settled. Do not treat the skill name as permission for relentless questioning or a fresh interview at every stage. Map this as a **design tree**: every material decision branches into the decisions that hang off it. When the skill runs inside the epic framework, begin from the approved First-Principles Basis, reconciled current state, provisional frame, and supported requirements rather than treating every imaginable design branch as relevant.

The **frontier** is every decision whose prerequisites are already settled: the questions that can be asked without guessing at answers not yet received. Use `$decision-frontier-manager` to select one material question from that frontier. Ask only that question with enough context to answer in the user's own words. Assess the actual answer before recording it and recomputing the tree.

Present the decision ID, the question, and why it matters. Invite an answer in the user's own words and offer Ground Me. Alternatives can explain the tradeoff without becoming a required menu. After the answer, surface any material disagreement, conflict, or decision-changing evidence and suggest a concrete change through the shared decision loop.

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier, remove branches that cannot materially change the approved outcome, and select the next single question. A question whose answer depends on another unresolved choice remains blocked.

Finding _facts_ is the agent's job, never the user's. When a question needs a fact from the environment, investigate it before asking; use a bounded research worker only when the host and user permit delegation. Treat unfinished research as an unsettled prerequisite. When provenance or the present validity of the current state would materially help, offer `Ground me`; suspend the decision, invoke `$ground-me`, align understanding, and return to the same unresolved question unless its premise is invalidated. The _decisions_ are the user's. A value-dependent frame choice or a retention, deletion, or restoration decision with material product or risk consequences belongs here; evidence gathering and requirement-source discovery do not.

The workflow interview is done when the material frontier is empty: every consequential branch of the design tree is resolved or explicitly deferred, and nothing material remains silently assumed. Do not preserve a branch merely because it can be imagined. The owning scope retains its existing approval boundary for subsequent work.
