"""Read-only stage presentation derived from observed Camunda work items."""

from datetime import datetime, timezone
import json
from pathlib import Path

CATALOG = json.loads((Path(__file__).with_name("stage-catalog.json")).read_text())[
    "workflows"
]
TERMINAL = {"COMPLETED", "CANCELED", "TERMINATED"}
LABELS = {
    "RUNNING": "Agent work",
    "RETRYING": "Retrying technical work",
    "WAITING_FOR_HUMAN": "Waiting for human review",
    "WAITING_FOR_EVENT": "Waiting for an external event",
    "NEEDS_REPAIR": "Recovery needed",
    "EVIDENCE_INCOMPLETE": "Evidence needs repair",
    "SYNCING": "Refreshing engine position",
    "UNMAPPED": "Stage label unavailable",
    "COMPLETED": "Completed",
    "CANCELED": "Canceled",
    "TERMINATED": "Terminated",
}


def workflow(process):
    known = CATALOG.get(process.get("processDefinitionId"))
    if known:
        return known
    return next(
        (
            w
            for w in CATALOG.values()
            if w["processName"] == process.get("processDefinitionName")
        ),
        {
            "label": process.get("processDefinitionName")
            or process.get("processDefinitionId", "Workflow"),
            "stages": [],
        },
    )


def stage_for(model, element_id):
    for number, stage in enumerate(model["stages"], 1):
        if element_id in stage["elements"]:
            return {
                "id": stage["id"],
                "label": stage["label"],
                "number": number,
                "total": len(model["stages"]),
                "purpose": stage["purpose"],
            }
    return {
        "id": None,
        "label": "Unmapped stage",
        "number": None,
        "total": len(model["stages"]),
        "purpose": "Inspect the deployed model before assigning a stage label.",
    }


def stage_progress(snapshot):
    states = {str(s["process"]["processInstanceKey"]): s for s in snapshot["instances"]}
    root = snapshot["root"]
    root_key = str(root["processInstanceKey"])
    root_model = workflow(root)
    root_variables = states.get(root_key, {}).get("variables", {})
    if (
        root_model["label"] == "Ticket implementation"
        and root_variables.get("ticketMode") == "REVIEW_ONLY"
    ):
        receipt = root_variables.get("issueReviewReceipt")
        root_model = dict(
            root_model,
            label="Ticket review",
            completion=(
                "Standalone issue review is complete. Implementation requires a separate authorized invocation."
                if isinstance(receipt, dict) and receipt.get("scope") == "standalone"
                else "Issue review is complete. The program waits for every issue before team assignment."
            ),
        )
    cards, completed, observed_root = [], [], set()

    def context(key, element_id):
        path, seen = [], set()
        while key in states and key not in seen:
            seen.add(key)
            state = states[key]
            process = state["process"]
            model = workflow(process)
            stage = stage_for(model, element_id)
            path.insert(
                0, {"scope": model["label"], "processInstanceKey": key, **stage}
            )
            parent_key = str(process.get("parentProcessInstanceKey"))
            parent = states.get(parent_key)
            parent_element = (
                next(
                    (
                        e
                        for e in parent.get("element-instances", [])
                        if str(e.get("elementInstanceKey"))
                        == str(process.get("parentElementInstanceKey"))
                    ),
                    None,
                )
                if parent
                else None
            )
            key, element_id = parent_key, (
                parent_element.get("elementId") if parent_element else None
            )
        return path

    for key, state in states.items():
        process = state["process"]
        elements = state.get("element-instances", [])
        element_by_key = {str(e.get("elementInstanceKey")): e for e in elements}
        active_elements = {
            str(e.get("elementInstanceKey")): e for e in state.get("activeElements", [])
        }
        work_types = {
            "SERVICE_TASK",
            "USER_TASK",
            "CALL_ACTIVITY",
            "INTERMEDIATE_CATCH_EVENT",
        }
        for element in elements:
            if key == root_key and element.get("state") in {"ACTIVE", "COMPLETED"}:
                stage = stage_for(root_model, element.get("elementId"))
                if stage["id"]:
                    observed_root.add(stage["id"])
            if (
                element.get("state") == "COMPLETED"
                and element.get("type") in work_types
            ):
                completed.append(
                    {
                        "processInstanceKey": key,
                        "elementInstanceKey": str(element["elementInstanceKey"]),
                        "elementId": element["elementId"],
                        "label": element.get("elementName")
                        or element["elementId"].replace("_", " ").capitalize(),
                        "completedAt": element.get("endDate"),
                        "path": context(key, element["elementId"]),
                    }
                )
        if root.get("state") in TERMINAL or process.get("state") != "ACTIVE":
            continue
        covered = set()

        def add(item, status, kind):
            element_key = str(item.get("elementInstanceKey", ""))
            if element_key and element_key in covered:
                return
            covered.add(element_key)
            element = element_by_key.get(element_key, {})
            element_id = item.get("elementId") or element.get("elementId")
            path = context(key, element_id)
            current = path[-1]
            card = {
                "processInstanceKey": key,
                "elementInstanceKey": element_key,
                "elementId": element_id,
                "label": item.get("name")
                or element.get("elementName")
                or (element_id or "Unindexed work item").replace("_", " ").capitalize(),
                "kind": kind,
                "state": status,
                "stage": current,
                "path": path,
                "revisited": any(
                    e.get("elementId") == element_id and e.get("state") == "COMPLETED"
                    for e in elements
                ),
            }
            issue = state.get("variables", {}).get("createdIssue")
            if isinstance(issue, dict) and issue.get("identifier"):
                card["issue"] = {
                    name: issue.get(name) for name in ("id", "identifier", "plan_key")
                }
            for name in (
                "jobKey",
                "userTaskKey",
                "incidentKey",
                "assignee",
                "messageName",
                "retries",
            ):
                if name in item:
                    card[name] = item[name]
            actions = item.get("customHeaders", {}).get("actions")
            if actions:
                card["actions"] = actions.split(",")
            if item.get("customHeaders", {}).get("responseMode") == "open_ended":
                card["responseMode"] = "open_ended"
                if element_id == "consider_decision":
                    card["decisionAnalysis"] = state.get("variables", {}).get(
                        "decisionAnalysis"
                    )
            cards.append(card)

        for item in state.get("activeIncidents", []):
            add(item, "NEEDS_REPAIR", "incident")
        for item in state.get("activeUserTasks", []):
            add(item, "WAITING_FOR_HUMAN", "human_task")
        for item in state.get("activeJobs", []):
            status = (
                "NEEDS_REPAIR"
                if item.get("retries") == 0
                else "RETRYING" if item.get("state") == "FAILED" else "RUNNING"
            )
            add(item, status, "job")
        for item in state.get("waitingMessages", []):
            if str(item.get("elementInstanceKey")) in active_elements:
                add(item, "WAITING_FOR_EVENT", "event")
        for element_key, element in active_elements.items():
            if element.get("type") not in work_types or element_key in covered:
                continue
            children = [
                s
                for s in states.values()
                if str(s["process"].get("parentElementInstanceKey")) == element_key
                and s["process"].get("state") == "ACTIVE"
            ]
            if element.get("type") == "CALL_ACTIVITY" and children:
                continue
            add(element, "SYNCING", "engine_element")

    priority = {
        state: i
        for i, state in enumerate(
            [
                "NEEDS_REPAIR",
                "WAITING_FOR_HUMAN",
                "RETRYING",
                "RUNNING",
                "WAITING_FOR_EVENT",
                "SYNCING",
            ]
        )
    }
    cards.sort(
        key=lambda c: (
            priority[c["state"]],
            c["processInstanceKey"],
            c["elementInstanceKey"],
        )
    )
    root_current = {
        c["path"][0]["id"]
        for c in cards
        if c["path"] and c["path"][0]["processInstanceKey"] == root_key
    }
    # A called subprocess can be visible before its own work items are indexed.
    for element in states.get(root_key, {}).get("activeElements", []):
        if element.get("type") in {
            "SERVICE_TASK",
            "USER_TASK",
            "CALL_ACTIVITY",
            "INTERMEDIATE_CATCH_EVENT",
        }:
            root_current.add(stage_for(root_model, element.get("elementId"))["id"])
    if root.get("state") in TERMINAL:
        root_current.clear()
    timeline = [
        {
            "id": s["id"],
            "label": s["label"],
            "number": i,
            "state": (
                "CURRENT"
                if s["id"] in root_current
                else "VISITED" if s["id"] in observed_root else "NOT_OBSERVED"
            ),
        }
        for i, s in enumerate(root_model["stages"], 1)
    ]
    state = (
        root.get("state")
        if root.get("state") in TERMINAL
        else cards[0]["state"] if cards else "SYNCING"
    )
    if (
        cards
        and not any(c["stage"]["id"] for c in cards)
        and state not in {"NEEDS_REPAIR", "WAITING_FOR_HUMAN"}
    ):
        state = "UNMAPPED"
    validation = snapshot.get("validation", {}).get("status", "not_checked")
    if validation == "incomplete":
        state = "EVIDENCE_INCOMPLETE"
    completed.sort(
        key=lambda e: (e["completedAt"] or "", int(e["elementInstanceKey"])),
        reverse=True,
    )
    return {
        "schema_version": 1,
        "source": "camunda",
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "consistency": snapshot.get("consistency", "eventually_consistent"),
        "scope": root_model["label"],
        "processInstanceKey": root_key,
        "state": state,
        "stateLabel": LABELS[state],
        "evidenceStatus": validation,
        "current": cards,
        "stages": timeline,
        "recentCompleted": completed[:5],
        "humanActionRequired": any(c["state"] == "WAITING_FOR_HUMAN" for c in cards),
        "revision": (
            "presentation"
            if states.get(root_key, {}).get("variables", {}).get("revisionGuard")
            else None
        ),
        "scopeBoundary": (
            root_model.get("completion") if root.get("state") == "COMPLETED" else None
        ),
        "completionMeaning": "Engine work-item completion; not independent approval or external verification.",
    }


def render_progress(result):
    progress = result["progress"]
    root = result.get("root", result)
    current = [s for s in progress["stages"] if s["state"] == "CURRENT"]
    position = ", ".join(
        f'{s["number"]}/{len(progress["stages"])} {s["label"]}' for s in current
    )
    lines = [
        f'{progress["scope"]} | {position or progress["stateLabel"]}',
        f'Status: {progress["stateLabel"]}',
    ]
    if progress["revision"]:
        lines.append(
            "Revision: presentation only; planning source bindings are preserved."
        )
    if progress["scopeBoundary"]:
        lines.append(progress["scopeBoundary"])
    for card in progress["current"]:
        path = " / ".join(p["label"] for p in card["path"])
        suffix = " (revisited)" if card["revisited"] else ""
        lines.append(f'Now: {path} | {card["label"]} | {LABELS[card["state"]]}{suffix}')
        if card.get("issue"):
            lines.append(f'Issue: {card["issue"]["identifier"]}')
        lines.append(f'This stage: {card["stage"]["purpose"]}')
        if card.get("actions"):
            owner = f' ({card["assignee"]})' if card.get("assignee") else ""
            action_text = (
                "pending until the referenced evidence is repaired"
                if progress["evidenceStatus"] == "incomplete"
                else (
                    "Respond in your own words; you can also ask for grounding."
                    if card.get("responseMode") == "open_ended"
                    else ", ".join(a.replace("_", " ") for a in card["actions"])
                )
            )
            lines.append(f"Human action{owner}: " + action_text)
        analysis = card.get("decisionAnalysis")
        if isinstance(analysis, dict):
            lines.append("Assessment: " + analysis.get("summary", ""))
            for finding in analysis.get("findings", []):
                lines.append(finding["kind"].capitalize() + ": " + finding["reason"])
                if finding.get("evidence_refs"):
                    lines.append("Evidence: " + ", ".join(finding["evidence_refs"]))
                lines.append("Suggested change: " + finding["suggested_change"])
        if card.get("messageName"):
            lines.append("Waiting for: " + card["messageName"])
    if not progress["current"] and progress["state"] == "SYNCING":
        lines.append(
            "Now: no active work item is indexed yet; refresh to confirm the stage."
        )
    if progress["recentCompleted"]:
        last = progress["recentCompleted"][0]
        lines.append("Last completed work: " + last["label"])
    if progress["stages"]:
        lines.append("Stage map (order, not percent complete):")
        for stage in progress["stages"]:
            label = {
                "CURRENT": "CURRENT",
                "VISITED": "visited",
                "NOT_OBSERVED": "not observed",
            }[stage["state"]]
            lines.append(f'  {stage["number"]}. {stage["label"]} [{label}]')
    evidence = (
        "not checked; use resume for referenced-evidence checks"
        if progress["evidenceStatus"] == "not_checked"
        else progress["evidenceStatus"]
    )
    lines.extend(
        [
            "Evidence: " + evidence,
            f'Process: {progress["processInstanceKey"]} | definition version {root.get("processDefinitionVersion", "unknown")}',
            "Observed: " + progress["observedAt"] + " (eventually consistent)",
        ]
    )
    return "\n".join(lines)
