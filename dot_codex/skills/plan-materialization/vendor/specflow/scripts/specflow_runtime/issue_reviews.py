"""Created issue coverage, native review evidence, and assignment contracts."""

from .client import RuntimeFailure, canonical, digest
from .proposal import validate_proposal
from .issue_content import validate_content, plan_content

POLICY = "all-issues-before-assignment-v1"


def require(condition, message):
    if not condition:
        raise RuntimeFailure("invalid_issue_review", message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def created_issues(variables, issues):
    plan = variables.get("linearPlan", {})
    expected = {issue["key"] for issue in plan.get("issues", [])}
    project = variables.get("projectResourcesBinding", {}).get("project_id")
    require(
        expected and project, "Resolve the approved plan and resource project first."
    )
    require(
        isinstance(issues, list) and len(issues) == len(expected),
        "Read back every created issue before starting individual reviews.",
    )
    keys, ids, identifiers = set(), set(), set()
    for issue in issues:
        require(isinstance(issue, dict), "Supply a created issue record.")
        key, identity, identifier = (
            issue.get(k) for k in ("plan_key", "id", "identifier")
        )
        require(
            nonempty(key) and key in expected and key not in keys,
            "Created issues must cover the approved plan exactly once.",
        )
        require(
            nonempty(identity)
            and identity not in ids
            and nonempty(identifier)
            and identifier not in identifiers,
            "Retain unique Linear issue identities.",
        )
        require(
            issue.get("project_id") == project, "Create issues in the approved project."
        )
        require(
            "assignee_id" in issue and issue["assignee_id"] is None,
            "Created issues stay unassigned until all individual reviews finish.",
        )
        require(
            nonempty(issue.get("verified_at")) and nonempty(issue.get("evidence")),
            "Record the provider readback of issue creation and unassigned state.",
        )
        content = issue.get("content")
        validate_content(content)
        planned = next(item for item in plan["issues"] if item["key"] == key)
        require(
            content
            == dict(
                plan_content(planned),
                comments=planned.get("comments", []),
                document_attachments=planned.get("document_attachments", []),
            ),
            "Read back the exact approved issue content, including authored comments and document attachments.",
        )
        keys.add(key)
        ids.add(identity)
        identifiers.add(identifier)
    return issues


def approval_receipt(client, process_key, variables, completed=False):
    process = client.request("GET", "/process-instances/" + str(process_key))
    require(process.get("tenantId") == client.tenant, "Use a review in this tenant.")
    if completed:
        if process.get("state") == "ACTIVE":
            raise RuntimeFailure(
                "pending_engine_readback",
                "Wait for the completed issue review to appear in Camunda readback.",
            )
        require(
            process.get("state") == "COMPLETED",
            "Every issue review must finish before assignment.",
        )
    parent = str(variables.get("programProcessInstanceKey", ""))
    standalone = process.get("parentProcessInstanceKey") is None
    if standalone:
        require(
            all(
                variables.get(name) is None
                for name in ("programProcessInstanceKey", "programBinding", "createdIssue")
            ),
            "A standalone review cannot claim implementation program lineage.",
        )
    else:
        require(
            parent.isdigit() and str(process.get("parentProcessInstanceKey")) == parent,
            "The review must be a child of this implementation program.",
        )
    require(
        variables.get("ticketMode") == "REVIEW_ONLY",
        "Use a review-only ticket run.",
    )
    require(
        variables.get("frontierOutcome") == "RESOLVED"
        and variables.get("ticketReviewOutcome") == "READY",
        "Resolve this issue's human decisions and design findings first.",
    )
    response = variables.get("ticketDesignResponse", {})
    require(
        isinstance(response, dict)
        and response.get("action") == "approved"
        and nonempty(response.get("actor")),
        "Record this issue's human design approval.",
    )
    key = str(response.get("user_task_key", ""))
    require(key.isdigit(), "Identify the native ticket approval task.")
    task = client.request("GET", "/user-tasks/" + key)
    require(
        task.get("tenantId") == client.tenant
        and str(task.get("processInstanceKey")) == str(process_key)
        and task.get("elementId") == "approve_ticket_design",
        "Read back the completed approval from this exact issue review.",
    )
    if task.get("state") in {"CREATED", "COMPLETING"}:
        raise RuntimeFailure(
            "pending_engine_readback",
            "Wait for the completed ticket approval to appear in Camunda readback.",
        )
    require(
        task.get("state") == "COMPLETED", "The ticket approval task did not complete."
    )
    proposal = variables.get("designProposalBinding")
    design = variables.get("ticketDesignBinding")
    validate_proposal(proposal, "ticket", design)
    require(
        response.get("binding") == proposal,
        "The approval must match the current issue design document.",
    )
    receipt = {
        "schema_version": 1,
        "review_process_instance_key": str(process_key),
        "approval_task_key": key,
        "design": design,
        "proposal": proposal["document"],
    }
    if standalone:
        identifier = variables.get("linearIssueId")
        require(
            nonempty(identifier) and process.get("businessId") == "ticket:" + identifier,
            "Bind the standalone review to its native ticket business ID.",
        )
        issue = {"identifier": identifier}
        if variables.get("linearIssueUuid") is not None:
            require(nonempty(variables["linearIssueUuid"]), "Retain a valid Linear issue ID.")
            issue["id"] = variables["linearIssueUuid"]
        basis = variables.get("ticketBasisBinding")
        require(
            isinstance(basis, dict)
            and nonempty(basis.get("ref"))
            and nonempty(basis.get("hash")),
            "Retain the standalone ticket's basis binding.",
        )
        return dict(receipt, scope="standalone", issue=issue, basis=basis)
    issue = variables.get("createdIssue")
    require(
        isinstance(issue, dict) and nonempty(issue.get("id")),
        "Bind the review to its created issue.",
    )
    return dict(
        receipt,
        source=variables.get("programBinding"),
        issue=issue,
        program_process_instance_key=parent,
    )


def verify_receipt(client, receipt, source, issue, parent):
    require(
        isinstance(receipt, dict)
        and receipt.get("schema_version") == 1
        and receipt.get("scope", "program") == "program",
        "Supply a completed program issue review receipt.",
    )
    require(
        receipt.get("source") == source
        and receipt.get("issue") == issue
        and receipt.get("program_process_instance_key") == str(parent),
        "The review must belong to this issue and exact program.",
    )
    key = str(receipt.get("review_process_instance_key", ""))
    require(key.isdigit(), "Identify the completed review process.")
    current = client.variables(key)
    require(
        approval_receipt(client, key, current, completed=True) == receipt,
        "The recorded review changed or no longer matches its native approval.",
    )
    require(
        current.get("issueReviewReceipt") == receipt,
        "Use the receipt recorded by the completed review.",
    )
    return current


def verify_all(client, job):
    variables = job.get("variables", {})
    issues = created_issues(variables, variables.get("createdIssues"))
    receipts = variables.get("issueReviewReceipts")
    require(
        isinstance(receipts, list) and len(receipts) == len(issues),
        "Complete every individual issue review before assigning any issue.",
    )
    by_id = {issue["id"]: issue for issue in issues}
    seen, processes = set(), set()
    for receipt in receipts:
        require(
            isinstance(receipt, dict) and isinstance(receipt.get("issue"), dict),
            "Each created issue needs its own completed review.",
        )
        identity = receipt["issue"].get("id")
        process = receipt.get("review_process_instance_key")
        require(
            nonempty(identity)
            and identity in by_id
            and identity not in seen
            and nonempty(process)
            and process not in processes,
            "Cover every issue once with a distinct review process.",
        )
        verify_receipt(
            client,
            receipt,
            variables.get("programBinding"),
            by_id[identity],
            job["processInstanceKey"],
        )
        seen.add(identity)
        processes.add(process)
    return receipts


def assignment_binding(variables, binding):
    receipts = variables.get("issueReviewReceipts")
    require(
        isinstance(binding, dict)
        and binding.get("schema_version") == 1
        and binding.get("source") == variables.get("programBinding")
        and binding.get("review_set_hash") == digest(canonical(receipts)),
        "Bind team assignment to the complete reviewed issue set.",
    )
    owners = {
        issue["key"]: issue["owner"] for issue in variables["linearPlan"]["issues"]
    }
    expected = {
        issue["id"]: owners[issue["plan_key"]] for issue in variables["createdIssues"]
    }
    rows = binding.get("assignments")
    require(
        isinstance(rows, list) and len(rows) == len(expected),
        "Read back every issue's assignment to the approved workstream owner.",
    )
    seen, owner_ids = set(), {}
    for row in rows:
        require(isinstance(row, dict), "Supply an assignment readback record.")
        identity, owner, assignee = (
            row.get(k) for k in ("issue_id", "owner", "assignee_id")
        )
        require(
            nonempty(identity)
            and identity in expected
            and identity not in seen
            and owner == expected[identity],
            "Preserve the approved issue ownership.",
        )
        require(
            nonempty(assignee) and row.get("readback_assignee_id") == assignee,
            "Verify the actual Linear assignee after assignment.",
        )
        require(
            owner_ids.get(owner, assignee) == assignee,
            "One workstream owner must resolve to one Linear user.",
        )
        owner_ids[owner] = assignee
        seen.add(identity)
    require(
        len(set(owner_ids.values())) == len(owner_ids),
        "The three workstreams must resolve to three distinct team members.",
    )
    require(
        nonempty(binding.get("verified_at")) and nonempty(binding.get("evidence")),
        "Retain the provider assignment readback evidence.",
    )


def before_handler(client, job):
    headers = job.get("customHeaders", {})
    if (
        headers.get("issueReviewPolicy") == POLICY
        and headers.get("phase") == "dispatch_tickets"
    ):
        from .program import validate_completion as validate_program
        from .project_resources import validate_completion as validate_resources

        validate_program(job, {"status": "completed", "variables": {}})
        validate_resources(job, {"status": "completed", "variables": {}})
        verify_all(client, job)


def prepare_completion(client, job, result):
    headers = job.get("customHeaders", {})
    if (
        result.get("status") != "completed"
        or headers.get("issueReviewPolicy") != POLICY
    ):
        return result
    current = job.get("variables", {})
    output = dict(result.get("variables", {}))
    phase = headers.get("phase")
    for name in (
        "createdIssue",
        "createdIssues",
        "programBinding",
        "programProcessInstanceKey",
        "ticketMode",
        "issueReviewReceipts",
        "issueReviewReceipt",
    ):
        if phase == "publish_linear_program" and name in {
            "createdIssues",
            "programProcessInstanceKey",
        }:
            continue
        require(
            name not in output or output[name] == current.get(name),
            "Workers must preserve issue identity, program scope, and recorded reviews.",
        )
    if phase == "publish_linear_program":
        issues = result.get("variables", {}).get("createdIssues")
        created_issues(current, issues)
        output["createdIssues"] = issues
        output["programProcessInstanceKey"] = str(job["processInstanceKey"])
    elif phase == "finalize_ticket_design":
        outcome = output.get("ticketReviewOutcome")
        require(
            outcome in {"READY", "NEEDS_DECISIONS", "REVISE_DESIGN"},
            "Return the issue's design review outcome.",
        )
        require(
            current.get("frontierOutcome") == "RESOLVED",
            "Complete the issue decision loop before final design review.",
        )
        design = output.get("ticketDesignBinding", current.get("ticketDesignBinding"))
        require(
            isinstance(design, dict)
            and nonempty(design.get("ref"))
            and nonempty(design.get("hash")),
            "Bind the finalized issue design.",
        )
    elif phase == "record_issue_review":
        for name in (
            "linearIssueId",
            "linearIssueUuid",
            "ticketBasisBinding",
            "ticketDesignBinding",
            "designProposalBinding",
            "ticketDesignResponse",
            "frontierOutcome",
            "ticketReviewOutcome",
        ):
            require(
                name not in output or output[name] == current.get(name),
                "Preserve the reviewed inputs when recording their approval.",
            )
        output["issueReviewReceipt"] = approval_receipt(
            client, job["processInstanceKey"], current
        )
    elif phase in {"verify_all_issue_reviews", "dispatch_tickets"}:
        verify_all(client, job)
        if phase == "dispatch_tickets":
            assignment_binding(current, output.get("teamAssignmentBinding"))
    elif phase == "verify_ticket_review":
        require(
            current.get("ticketMode") != "REVIEW_ONLY",
            "A review-only run cannot enter implementation by reusing an execution receipt.",
        )
        receipt = current.get("issueReviewReceipt")
        require(
            isinstance(receipt, dict), "Supply the assigned issue's review receipt."
        )
        source = verify_receipt(
            client,
            receipt,
            current.get("programBinding"),
            current.get("createdIssue"),
            current.get("programProcessInstanceKey"),
        )
        parent = client.variables(receipt["program_process_instance_key"])
        assignment_binding(parent, parent.get("teamAssignmentBinding"))
        require(
            receipt in parent.get("issueReviewReceipts", []),
            "The assigned program must retain this exact issue review.",
        )
        for name in (
            "ticketBasisBinding",
            "ticketDesignBinding",
            "designProposalBinding",
            "ticketDesignResponse",
        ):
            require(
                name not in output or output[name] == source.get(name),
                "Reuse the exact approved design; changed scope needs a fresh review.",
            )
            require(
                name not in current or current[name] == source.get(name),
                "Changed ticket inputs require a fresh review rather than reuse of an old approval.",
            )
            output[name] = source.get(name)
    return dict(result, variables=output)
