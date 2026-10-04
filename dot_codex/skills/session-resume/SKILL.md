---
name: session-resume
description: Build an evidence-grounded visual briefing of the active or named Codex task when the user asks to resume, catch up, remember what we were doing, understand why the work took its current direction, or see where to continue. Use for continuity within an existing task; do not use for generic topic summaries, forward planning with no prior work, or multi-task standups.
---

# Session Resume

Produce one compact visual that answers, in order: what the user wanted, why the work took its current direction, where the work stands, and what the recorded continuation is.

## Build the briefing

1. Resolve the target. Use the active task unless the user explicitly names another task. Read another task with the task-management tools instead of reconstructing it from memory. If the target remains ambiguous, render the truthful context that can be established and then ask one concise scope question.
2. Reconstruct the narrative from evidence. Prefer the user's requests and corrections for intent; explicit decisions, approved specifications, and durable artifacts for rationale; and fresh read-only observations for mutable current state. Treat summaries and persistent memory as historical leads, not live confirmation.
3. Separate what is known from what is reconstructed. Mark each material claim as `verified-now`, `recorded`, `inferred`, or `unknown`. Surface contradictions. Say that a reason was not captured when no recorded rationale exists. Never expose hidden chain-of-thought as rationale.
4. Read [references/brief-schema.md](references/brief-schema.md), create the smallest complete JSON brief, and keep source labels short. Include only facts that help the user resume; omit secrets, raw environment values, transcript noise, and private implementation detail.
5. Resolve this skill's directory, then render the brief with the renderer's absolute path into a writable, task-owned visualization directory. Prefer the thread visualization directory when available, otherwise use the task's `work/` directory. The renderer creates or replaces the requested output file with an inline HTML fragment for Codex:

   ```bash
   python3 "/absolute/path/to/session-resume/scripts/render_resume.py" \
     "/absolute/path/to/brief.json" \
     "/absolute/path/to/session-resume.html"
   ```

6. Read back the fragment and, when browser inspection is available, check the useful first view at normal and narrow widths. Correct clipped text, empty sections, placeholders, unsupported claims, and inconsistent evidence labels before presenting it.
7. Present the visual with the Codex visualization content reference on its own line. Add at most one short sentence outside the visual when the user needs a clarification or a material caveat.

   ```text
   visualize{"path":"/absolute/path/to/session-resume.html"}
   ```

## Evidence rules

- Use `verified-now` only for mutable state observed during the current invocation.
- Use `recorded` for a direct statement or earlier result whose historical occurrence is evidenced.
- Use `inferred` for a reasonable synthesis that was not explicitly recorded, and phrase it as an inference.
- Use `unknown` for missing, stale, or conflicting evidence that cannot be resolved.
- Treat an earlier passing test as history when later changes or a fresh failure make it stale.
- Treat proposed next moves as proposals unless the user already agreed to them.
- Do not show a completion percentage unless it is derived from a real, enumerated checklist.
- Do not equate implementation, a passing command, deployment, or service readiness unless the relevant boundary was actually verified.

## Visual composition

Keep one dominant narrative spine from intent through the current frontier. Put the compact What / Why / Now orientation above it and the continuation edge below it. Show parallel lanes only when concurrency materially explains the state. Keep evidence details secondary but available. A sparse session should produce a sparse, honest visual rather than invented work.
