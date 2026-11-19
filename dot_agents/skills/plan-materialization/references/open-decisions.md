# Open-ended human decisions

Apply the underlying decision, approval-reuse, and progress-reporting behavior to the current scope's records and authorized interaction surface. Process keys, native user tasks, response-envelope fields, and runtime commands below apply only to an actually configured orchestrator. Without it, bind explicit human decisions to the question and exact reviewed content without fabricating engine state. See [workspace and destinations](workspace-and-destinations.md).

Apply [review and artifact design](review-and-artifact-design.md) before creating a question. Reuse settled intent and decisions, research accessible facts, and handle routine details within approved scope. If an unresolved material human choice remains, ask one question in plain language and invite the human to answer in their own words. Explain the consequential choice, why this person needs to decide now, and what their answer unlocks. Possibilities can help explain the choice, but they are not a closed menu and need no mandatory recommendation before the answer. Ground Me remains available. Preserve the human's exact words and named actor; interpret clear intent without a routine confirmation round.

After the answer, analyze its meaning and consequences against the approved basis, applicable evidence, accepted decisions, and the human's stated priorities. Challenge the agent's own prior recommendation as well as the new choice. Resolve factual uncertainty through available authorized research before asking the human to adjudicate facts. Keep unknowns explicit; do not manufacture a conflict or an estimate to fill a field.

If the answer has no material concern, record it and continue automatically. If there is a reasoned disagreement, conflicting constraint or prior decision, evidence that could change the choice, or consequential ambiguity, surface the concern before relying on the answer. Explain why it matters and suggest a concrete change or clarification. Cite factual and conflict claims; label inference, uncertainty, and value judgments honestly. Present only the material difference, without repeating the whole design.

The human can keep the choice, revise it freely, correct the assessment, or request grounding. Record an explicit choice to retain it together with the concern and rationale, then continue. Reassess a revised answer automatically. Do not repeat an acknowledged concern to pressure the human into agreement; reopen it only for materially new evidence, changed intent, or a different consequence. An agent's disagreement does not supersede the human's decision. A conflict with an approved invariant must identify which intent or constraint the human is changing and use the existing basis-revision route; retaining a preference does not silently rewrite an approval.

A clear free-text decision needs no extra confirmation just because it was not anticipated. Clarification is for ambiguity that changes behavior, scope, or authorization. Explicit approval tasks also accept natural-language feedback, but their existing approval meaning and evidence bindings remain intact. Assessment is automatic work, not a new universal approval gate. Continue independent authorized work during a genuine human wait.

## Question artifact

Keep the complete question artifact and assessment in workflow evidence. Present the decision and its material consequences through the current conversation or owning proposal section; use descriptive shared links for optional depth. A completed analysis is not another report the user must approve.

New questions use schema version 3. `options` and `recommendation` are optional explanatory material; `actions` is `["answer", "ground_me"]`. A question can be open without inventing alternatives. Version 2 artifacts remain readable, including named-option and custom-answer inputs. When explanatory alternatives include estimates, use only grounded estimates; unavailable values remain `UNKNOWN` under the parent accounting contract.

## Camunda answer and assessment

The technical action `select_answer` carries any nonempty answer, not an option enum. Prepare the exact response read-only, then submit only the human's actual answer:

```text
specflow prepare-response TASK_KEY --actor "Named supervisor" --action select_answer --answer "Keep local files during the pilot; revisit shared storage after we measure collaboration needs." --json
specflow complete-task response.json --json
```

`specflow.analyze-decision` receives the current `decisionBinding` and `decisionResponse`. Its configured authoring command or directly acting agent returns:

```json
{
  "status": "completed",
  "variables": {
    "decisionAnalysis": {
      "schema_version": 1,
      "decisionBinding": {"ref": "DEC-1", "hash": "sha256:question", "frontierRevision": 1},
      "response": {
        "user_task_key": "TASK_KEY",
        "process_instance_key": "PROCESS_KEY",
        "element_id": "answer_question",
        "actor": "Named supervisor",
        "action": "select_answer",
        "binding": {"ref": "DEC-1", "hash": "sha256:question", "frontierRevision": 1},
        "answer": "Keep local files during the pilot."
      },
      "summary": "The pilot uses local storage and accepts a single-machine working copy.",
      "findings": [{
        "id": "CONCERN-1",
        "kind": "CONFLICT",
        "reason": "The approved pilot includes simultaneous editing from two machines.",
        "evidence_refs": ["FPB-1/INV-2"],
        "suggested_change": "Use shared storage for the pilot, or explicitly revise its collaboration scope."
      }]
    }
  }
}
```

Copy the complete input response into the assessment, including any grounding or reconsideration provenance. `summary` explains the interpreted answer and consequences. `findings` is empty when no material concern was found. Finding kinds are `DISAGREEMENT`, `CONFLICT`, `EVIDENCE`, and `CLARIFICATION`; every finding supplies an ID, reason, suggested change, and evidence-reference array. Conflict and evidence findings require references. Reasoned disagreement or clarification can have an empty reference array when no factual source is being claimed.

The runtime validates the exact question/answer binding, derives `decisionAnalysisOutcome`, and hashes the assessment into `decisionAnalysisBinding`. An empty findings list continues to `record_decision`. Findings activate `consider_decision`, where `status` and `resume` display the assessment and suggestions. The named human's free-text response is represented internally as `keep_answer`, `revise_answer` with `answer`, or `ground_me`. These are routing values, not a required multiple-choice presentation. Keeping an answer requires a completed task bound to the exact assessment; revision returns to analysis; grounding retains the unresolved choice. The runtime supplies `recordedDecision` with the exact answer, actor, assessment, and applicable follow-up provenance.

Both ordinary answers and verified combined Ground Me answers pass through assessment. Missing or stale analysis cannot complete the protected recording step. An unconfigured analysis handler waits for an authorized capable agent or command; it never fabricates semantic judgment. Authoring quality and whether evidence could change a person's mind require reasoning and are not established by shape or hash validation.

Definitions carrying `decisionPolicy: open-decisions-v1` implement this path. Existing instances retain their deployed definition and use the shared agent policy within their existing tasks; they are not migrated automatically. Direct Camunda API operators remain responsible for equivalent checks.

## Local artifact helper

```text
python3 scripts/advance_decision.py question.json action.json --json
```

An action such as `{"type":"answer","answer":"Use a local pilot first.","actor":"Named supervisor"}` returns `decision_analysis_required` with `analysis_input`; the frontier is unchanged. Add an `analysis` object binding that exact input and invoke the same helper. A clean assessment returns `decision_recorded`. Findings return `decision_discussion_required` and an `analysis_binding`.

After an actual human response that keeps the answer, add `followup: {"action":"keep_answer","actor":"Named supervisor","binding":<returned analysis_binding>}`. A revised answer needs a matching revised assessment. The helper retains legacy `option` and `custom_answer` actions and `confirmed_by` as an actor alias. It validates artifact records only; it neither completes Camunda tasks nor grants publication authority.
