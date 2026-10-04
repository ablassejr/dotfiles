# Resume brief schema

Use this schema as the renderer contract. Strings should be concise enough to scan, but they may contain any Unicode text. Unknown keys are ignored so the format can evolve without breaking older renderers.

## Evidence object

Every material claim may carry an `evidence` object:

```json
{
  "status": "verified-now",
  "source": "git status",
  "freshness": "2026-09-03 14:20 CDT"
}
```

`status` is one of `verified-now`, `recorded`, `inferred`, or `unknown`. `source` identifies the compact user-visible basis for the claim. `freshness` is optional and is useful for mutable observations.

## Brief object

```json
{
  "title": "Export account data",
  "as_of": "2026-09-03 14:20 CDT",
  "scope": "Active Codex task and its workspace",
  "status": {
    "value": "in-progress",
    "evidence": {
      "status": "verified-now",
      "source": "active task state",
      "freshness": "2026-09-03 14:20 CDT"
    }
  },
  "objective": {
    "text": "Add an account export endpoint without changing the existing response contract.",
    "evidence": {
      "status": "recorded",
      "source": "user request"
    }
  },
  "why": [
    {
      "decision": {
        "text": "Preserve the response envelope",
        "evidence": {
          "status": "recorded",
          "source": "approved compatibility decision"
        }
      },
      "rationale": {
        "text": "The available evidence suggests the envelope was preserved because existing consumers depend on its fields.",
        "evidence": {
          "status": "inferred",
          "source": "consumer contract inspection",
          "freshness": "2026-09-03 14:20 CDT"
        }
      }
    }
  ],
  "current": {
    "text": "The endpoint works at the system boundary.",
    "evidence": {
      "status": "verified-now",
      "source": "end-to-end test and git status",
      "freshness": "2026-09-03 14:20 CDT"
    }
  },
  "narrative": [
    {
      "phase": "Intent",
      "title": "Compatibility goal recorded",
      "detail": "The export must fit the current client contract.",
      "state": "done",
      "evidence": {
        "status": "recorded",
        "source": "user request"
      }
    },
    {
      "phase": "Verification",
      "title": "Boundary behavior passes",
      "detail": "The user-visible export flow succeeds in the end-to-end test.",
      "state": "current",
      "evidence": {
        "status": "verified-now",
        "source": "test run"
      }
    }
  ],
  "next": {
    "text": "Review the diff and decide whether to publish it.",
    "kind": "proposed",
    "evidence": {
      "status": "inferred",
      "source": "current frontier"
    }
  },
  "blockers": [],
  "open_questions": [
    {
      "text": "Should the export be published in this task?",
      "evidence": {
        "status": "unknown",
        "source": "authorization not recorded"
      }
    }
  ],
  "conflicts": []
}
```

## Field notes

- `title`, `objective.text`, and `current.text` are required.
- `status` is optional. When present, it contains `value` and optional `evidence`; `value` may be `in-progress`, `blocked`, `ready`, `complete`, or `unknown`. A `complete` value requires both the status and current-state evidence to be recorded or verified now.
- `why`, `narrative`, `blockers`, `open_questions`, and `conflicts` are arrays and may be empty.
- A `why` item contains separate `decision` and `rationale` claim objects. Each contains `text` and optional `evidence` so a recorded choice and an inferred explanation never share provenance accidentally.
- A `narrative` item contains `phase`, `title`, `detail`, `state`, and optional `evidence`. `state` may be `done`, `current`, `next`, or `blocked`.
- A narrative may contain at most one `current` item. Include it when the exact frontier wording matters. If a nonempty narrative omits it, the renderer inserts the top-level `current` claim before the first `next` item so the visual always has a truthful `You are here` marker.
- A `next` object contains `text`, `kind`, and optional `evidence`. `kind` may be `recorded`, `proposed`, or `unknown`. A `recorded` continuation requires recorded or verified evidence; otherwise label it `proposed` or `unknown`.
- `blockers`, `open_questions`, and `conflicts` contain objects with `text` and optional `evidence`.
- Omit an optional claim when it is irrelevant. Use an explicit unknown claim when its absence is itself important to resuming safely.
- Every `verified-now`, `recorded`, or `inferred` evidence object requires a nonempty `source`. Unknown evidence may omit it and renders as `Source not recorded`.
