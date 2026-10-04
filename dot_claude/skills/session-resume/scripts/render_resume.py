#!/usr/bin/env python3
"""Render an evidence-grounded session resume as a Codex HTML fragment."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path
from typing import Any


EVIDENCE_LABELS = {
    "verified-now": "Verified now",
    "recorded": "Recorded",
    "inferred": "Inferred",
    "unknown": "Unknown",
}

STATUS_LABELS = {
    "in-progress": "In progress",
    "blocked": "Blocked",
    "ready": "Ready",
    "complete": "Complete",
    "unknown": "Status unknown",
}

STATE_LABELS = {
    "done": "Done",
    "current": "You are here",
    "next": "Next",
    "blocked": "Blocked",
}


class BriefError(ValueError):
    """Raised when the public brief contract is invalid."""


def text(value: Any, field: str, *, required: bool = False) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str) or (required and not value.strip()):
        qualifier = "a non-empty string" if required else "a string"
        raise BriefError(f"{field} must be {qualifier}")
    return value.strip()


def object_value(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BriefError(f"{field} must be an object")
    return value


def list_value(value: Any, field: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise BriefError(f"{field} must be an array")
    return value


def evidence(value: Any, field: str) -> dict[str, str]:
    if value is None:
        return {"status": "unknown", "source": "Source not recorded", "freshness": ""}
    item = object_value(value, field)
    status = text(item.get("status", "unknown"), f"{field}.status") or "unknown"
    if status not in EVIDENCE_LABELS:
        allowed = ", ".join(EVIDENCE_LABELS)
        raise BriefError(f"{field}.status must be one of: {allowed}")
    source = text(item.get("source", ""), f"{field}.source")
    if status != "unknown" and not source:
        raise BriefError(f"{field}.source must identify the basis for {status} evidence")
    freshness = text(item.get("freshness", ""), f"{field}.freshness")
    return {
        "status": status,
        "source": source or "Source not recorded",
        "freshness": freshness,
    }


def claim(value: Any, field: str, *, required: bool = False) -> dict[str, Any]:
    item = object_value(value, field)
    return {
        "text": text(item.get("text"), f"{field}.text", required=required),
        "evidence": evidence(item.get("evidence"), f"{field}.evidence"),
    }


def normalize_brief(raw: Any) -> dict[str, Any]:
    brief = object_value(raw, "brief")
    objective_item = claim(brief.get("objective"), "objective", required=True)
    current_item = claim(brief.get("current"), "current", required=True)

    raw_status = brief.get("status")
    if raw_status is None:
        status_item = {
            "value": "unknown",
            "evidence": evidence(None, "status.evidence"),
        }
    else:
        status_object = object_value(raw_status, "status")
        status_item = {
            "value": text(status_object.get("value"), "status.value", required=True),
            "evidence": evidence(status_object.get("evidence"), "status.evidence"),
        }
    if status_item["value"] not in STATUS_LABELS:
        allowed = ", ".join(STATUS_LABELS)
        raise BriefError(f"status.value must be one of: {allowed}")
    completion_evidence = {"verified-now", "recorded"}
    if status_item["value"] == "complete" and (
        status_item["evidence"]["status"] not in completion_evidence
        or current_item["evidence"]["status"] not in completion_evidence
    ):
        raise BriefError(
            "complete status requires recorded or verified status and current-state evidence"
        )

    why_items = []
    for index, raw_item in enumerate(list_value(brief.get("why"), "why")):
        item = object_value(raw_item, f"why[{index}]")
        why_items.append(
            {
                "decision": claim(
                    item.get("decision"), f"why[{index}].decision", required=True
                ),
                "rationale": claim(
                    item.get("rationale"), f"why[{index}].rationale", required=True
                ),
            }
        )

    narrative_items = []
    for index, raw_item in enumerate(list_value(brief.get("narrative"), "narrative")):
        item = object_value(raw_item, f"narrative[{index}]")
        state = text(item.get("state", "done"), f"narrative[{index}].state") or "done"
        if state not in STATE_LABELS:
            allowed = ", ".join(STATE_LABELS)
            raise BriefError(f"narrative[{index}].state must be one of: {allowed}")
        narrative_items.append(
            {
                "phase": text(item.get("phase", "Progress"), f"narrative[{index}].phase") or "Progress",
                "title": text(item.get("title"), f"narrative[{index}].title", required=True),
                "detail": text(item.get("detail", ""), f"narrative[{index}].detail"),
                "state": state,
                "evidence": evidence(item.get("evidence"), f"narrative[{index}].evidence"),
            }
        )

    current_markers = sum(item["state"] == "current" for item in narrative_items)
    if current_markers > 1:
        raise BriefError("narrative may contain at most one current item")
    if narrative_items and current_markers == 0:
        frontier = {
            "phase": "Frontier",
            "title": "Current state",
            "detail": current_item["text"],
            "state": "current",
            "evidence": current_item["evidence"],
        }
        insertion_index = next(
            (
                index
                for index, item in enumerate(narrative_items)
                if item["state"] == "next"
            ),
            len(narrative_items),
        )
        narrative_items.insert(insertion_index, frontier)

    def claim_list(name: str) -> list[dict[str, Any]]:
        return [
            claim(item, f"{name}[{index}]", required=True)
            for index, item in enumerate(list_value(brief.get(name), name))
        ]

    next_value = brief.get("next")
    if next_value is None:
        next_item = {
            "text": "No continuation has been recorded.",
            "kind": "unknown",
            "evidence": evidence(None, "next.evidence"),
        }
    else:
        item = object_value(next_value, "next")
        kind = text(item.get("kind", "unknown"), "next.kind") or "unknown"
        if kind not in {"recorded", "proposed", "unknown"}:
            raise BriefError("next.kind must be one of: recorded, proposed, unknown")
        next_evidence = evidence(item.get("evidence"), "next.evidence")
        if kind == "recorded" and next_evidence["status"] not in {
            "verified-now",
            "recorded",
        }:
            raise BriefError(
                "recorded next.kind requires recorded or verified evidence"
            )
        next_item = {
            "text": text(item.get("text"), "next.text", required=True),
            "kind": kind,
            "evidence": next_evidence,
        }

    return {
        "title": text(brief.get("title"), "title", required=True),
        "as_of": text(brief.get("as_of", ""), "as_of"),
        "scope": text(brief.get("scope", "Active task"), "scope") or "Active task",
        "status": status_item,
        "objective": objective_item,
        "why": why_items,
        "current": current_item,
        "narrative": narrative_items,
        "next": next_item,
        "blockers": claim_list("blockers"),
        "open_questions": claim_list("open_questions"),
        "conflicts": claim_list("conflicts"),
    }


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def evidence_markup(item: dict[str, str]) -> str:
    label = EVIDENCE_LABELS[item["status"]]
    details = item["source"]
    if item["freshness"]:
        details = f"{details} · {item['freshness']}"
    return (
        f'<span class="viz-badge sr-evidence" data-evidence="{esc(item["status"])}">'
        f'{esc(label)}</span><span class="text-small text-muted">{esc(details)}</span>'
    )


def claim_markup(label: str, item: dict[str, Any], class_name: str) -> str:
    return (
        f'<section class="{class_name}">'
        f'<h2 class="sr-kicker">{esc(label)}</h2>'
        f'<p class="sr-claim">{esc(item["text"])}</p>'
        f'<div class="sr-source">{evidence_markup(item["evidence"])}</div>'
        '</section>'
    )


def list_section(title: str, items: list[dict[str, Any]], kind: str) -> str:
    if not items:
        return ""
    rows = "".join(
        '<li>'
        f'<span>{esc(item["text"])}</span>'
        f'<span class="sr-source">{evidence_markup(item["evidence"])}</span>'
        '</li>'
        for item in items
    )
    return (
        f'<section class="sr-edge-list" data-kind="{esc(kind)}">'
        f'<h3>{esc(title)}</h3><ul>{rows}</ul></section>'
    )


def render(brief: dict[str, Any]) -> str:
    digest = hashlib.sha1(
        json.dumps(brief, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:10]
    root_id = f"session-resume-{digest}"

    if brief["why"]:
        why_body = "".join(
            '<article class="sr-reason">'
            '<p class="text-small text-muted sr-kicker">Decision</p>'
            f'<h3>{esc(item["decision"]["text"])}</h3>'
            f'<div class="sr-source">{evidence_markup(item["decision"]["evidence"])}</div>'
            '<p class="text-small text-muted sr-kicker sr-rationale-label">Rationale</p>'
            f'<p>{esc(item["rationale"]["text"])}</p>'
            f'<div class="sr-source">{evidence_markup(item["rationale"]["evidence"])}</div>'
            '</article>'
            for item in brief["why"]
        )
    else:
        why_body = (
            '<article class="sr-reason">'
            '<h3>Reason not captured</h3>'
            '<p>The available record does not establish why this direction was chosen.</p>'
            '<div class="sr-source"><span class="viz-badge sr-evidence" '
            'data-evidence="unknown">Unknown</span>'
            '<span class="text-small text-muted">No recorded rationale</span></div>'
            '</article>'
        )

    if brief["narrative"]:
        narrative = "".join(
            '<li class="sr-step" data-state="{state}">'
            '<div class="sr-marker" aria-hidden="true"></div>'
            '<div class="sr-step-copy">'
            '<div class="sr-step-head">'
            '<span class="text-small text-muted">{phase}</span>'
            '<span class="viz-badge">{state_label}</span>'
            '</div>'
            '<h3>{title}</h3>'
            '{detail}'
            '<div class="sr-source">{evidence}</div>'
            '</div></li>'.format(
                state=esc(item["state"]),
                phase=esc(item["phase"]),
                state_label=esc(STATE_LABELS[item["state"]]),
                title=esc(item["title"]),
                detail=f'<p>{esc(item["detail"])}</p>' if item["detail"] else "",
                evidence=evidence_markup(item["evidence"]),
            )
            for item in brief["narrative"]
        )
    else:
        narrative = (
            '<li class="sr-step" data-state="current">'
            '<div class="sr-marker" aria-hidden="true"></div>'
            '<div class="sr-step-copy"><div class="sr-step-head">'
            '<span class="text-small text-muted">Frontier</span>'
            '<span class="viz-badge">You are here</span></div>'
            '<h3>No work history was established</h3>'
            '<p>The briefing contains only the current known state.</p>'
            '<div class="sr-source"><span class="viz-badge sr-evidence" '
            'data-evidence="unknown">Unknown</span>'
            '<span class="text-small text-muted">History unavailable</span></div>'
            '</div></li>'
        )

    why_section = (
        '<section class="sr-why"><h2 class="sr-kicker">Why</h2>'
        f'{why_body}</section>'
    )
    as_of = f' · As of {esc(brief["as_of"])}' if brief["as_of"] else ""
    next_kind = brief["next"]["kind"].capitalize()
    edge_sections = "".join(
        [
            list_section("Blockers", brief["blockers"], "blocked"),
            list_section("Open questions", brief["open_questions"], "question"),
            list_section("Conflicting evidence", brief["conflicts"], "conflict"),
        ]
    )
    edge_grid = f'<div class="sr-edge-grid">{edge_sections}</div>' if edge_sections else ""

    fragment = f'''<style>
#{root_id} {{ color: var(--foreground); display: grid; gap: 24px; overflow-wrap: anywhere; width: 100%; }}
#{root_id} * {{ box-sizing: border-box; }}
#{root_id} h1, #{root_id} h2, #{root_id} h3, #{root_id} p {{ margin-block: 0; }}
#{root_id} h1 {{ max-width: 28ch; }}
#{root_id} h2 {{ margin-bottom: 12px; }}
#{root_id} h3 {{ font-weight: 500; }}
#{root_id} .sr-header {{ display: grid; gap: 8px; }}
#{root_id} .sr-meta {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
#{root_id} .sr-orientation {{ border-block: 1px solid var(--border); display: grid; grid-template-columns: 1.1fr 1.4fr 1.1fr; }}
#{root_id} .sr-orientation > section {{ min-width: 0; padding: 18px; }}
#{root_id} .sr-orientation > section + section {{ border-inline-start: 1px solid var(--border); }}
#{root_id} .sr-orientation h2 {{ margin-bottom: 0; }}
#{root_id} .sr-kicker {{ font-weight: 500; letter-spacing: .04em; text-transform: uppercase; }}
#{root_id} .sr-claim {{ margin-top: 8px; }}
#{root_id} .sr-source {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 10px; }}
#{root_id} .sr-reason + .sr-reason {{ border-top: 1px solid var(--border); margin-top: 14px; padding-top: 14px; }}
#{root_id} .sr-reason p {{ margin-top: 6px; }}
#{root_id} .sr-reason .sr-rationale-label {{ margin-top: 14px; }}
#{root_id} .sr-spine {{ list-style: none; margin: 0; padding: 0; position: relative; }}
#{root_id} .sr-spine::before {{ background: var(--border); content: ""; inset-block: 10px; inset-inline-start: 11px; position: absolute; width: 2px; }}
#{root_id} .sr-step {{ display: grid; gap: 14px; grid-template-columns: 24px minmax(0, 1fr); padding-bottom: 20px; position: relative; }}
#{root_id} .sr-step:last-child {{ padding-bottom: 0; }}
#{root_id} .sr-marker {{ background: var(--background); border: 2px solid var(--muted-foreground); border-radius: 50%; height: 14px; margin: 5px; position: relative; width: 14px; z-index: 1; }}
#{root_id} .sr-step[data-state="current"] .sr-marker {{ background: var(--viz-series-1); border-color: var(--viz-series-1); box-shadow: 0 0 0 5px color-mix(in srgb, var(--viz-series-1) 18%, transparent); }}
#{root_id} .sr-step[data-state="blocked"] .sr-marker {{ background: var(--red); border-color: var(--red); }}
#{root_id} .sr-step[data-state="next"] .sr-marker {{ border-color: var(--viz-series-2); }}
#{root_id} .sr-step-copy {{ min-width: 0; padding-bottom: 2px; }}
#{root_id} .sr-step-head {{ align-items: center; display: flex; flex-wrap: wrap; gap: 8px; justify-content: space-between; }}
#{root_id} .sr-step-copy h3 {{ margin-top: 4px; }}
#{root_id} .sr-step-copy > p {{ margin-top: 6px; }}
#{root_id} .sr-continuation {{ border-block-start: 1px solid var(--border); display: grid; gap: 18px; padding-top: 18px; }}
#{root_id} .sr-next {{ border-inline-start: 4px solid var(--viz-series-2); padding-inline-start: 14px; }}
#{root_id} .sr-next p {{ margin-top: 6px; }}
#{root_id} .sr-edge-grid {{ display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
#{root_id} .sr-edge-list h3 {{ margin-bottom: 8px; }}
#{root_id} .sr-edge-list ul {{ display: grid; gap: 10px; margin: 0; padding-inline-start: 20px; }}
#{root_id} .sr-edge-list li > span:first-child {{ display: block; }}
#{root_id} .sr-edge-list[data-kind="blocked"] {{ color: var(--red); }}
#{root_id} .sr-edge-list[data-kind="blocked"] .sr-source,
#{root_id} .sr-edge-list[data-kind="conflict"] .sr-source {{ color: var(--foreground); }}
@media (max-width: 640px) {{
  #{root_id} .sr-orientation {{ grid-template-columns: 1fr; }}
  #{root_id} .sr-orientation > section {{ padding-inline: 0; }}
  #{root_id} .sr-orientation > section + section {{ border-inline-start: 0; border-top: 1px solid var(--border); }}
  #{root_id} .sr-edge-grid {{ grid-template-columns: 1fr; }}
}}
</style>
<article id="{root_id}" aria-label="Session resume for {esc(brief['title'])}">
  <header class="sr-header">
    <div class="sr-meta">
      <span class="viz-badge">{esc(STATUS_LABELS[brief['status']['value']])}</span>
      {evidence_markup(brief['status']['evidence'])}
      <span class="text-small text-muted">{esc(brief['scope'])}{as_of}</span>
    </div>
    <h1>{esc(brief['title'])}</h1>
  </header>

  <div class="sr-orientation">
    {claim_markup("What", brief["objective"], "sr-what")}
    {why_section}
    {claim_markup("Now", brief["current"], "sr-now")}
  </div>

  <section aria-labelledby="{root_id}-journey">
    <h2 id="{root_id}-journey">How we got here</h2>
    <ol class="sr-spine" role="list">{narrative}</ol>
  </section>

  <section class="sr-continuation" aria-labelledby="{root_id}-continue">
    <div class="sr-next">
      <h2 class="sr-kicker" id="{root_id}-continue">Continuation · {esc(next_kind)}</h2>
      <p>{esc(brief['next']['text'])}</p>
      <div class="sr-source">{evidence_markup(brief['next']['evidence'])}</div>
    </div>
    {edge_grid}
  </section>
</article>
'''
    if len(fragment.encode("utf-8")) >= 1_000_000:
        raise BriefError("rendered fragment exceeds the 1 MB Codex visualization limit")
    return fragment


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a session resume JSON brief as a Codex HTML fragment."
    )
    parser.add_argument("input", type=Path, help="Path to the JSON brief")
    parser.add_argument("output", type=Path, help="Path for the rendered HTML fragment")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        fragment = render(normalize_brief(raw))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(fragment, encoding="utf-8")
    except (OSError, json.JSONDecodeError, BriefError) as error:
        print(f"session-resume: {error}", file=sys.stderr)
        return 2
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
