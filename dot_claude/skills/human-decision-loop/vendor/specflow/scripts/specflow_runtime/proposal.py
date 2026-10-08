"""Publication evidence for the supervisor's existing final planning review."""

import re
from urllib.parse import urlparse

from .client import RuntimeFailure
from .visuals import validate_visuals

CONTRACT = "linear-design-proposal-v1"


def validate_proposal(binding, scope, source):
    def require(condition, message):
        if not condition:
            raise RuntimeFailure("invalid_design_proposal", message)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    require(isinstance(binding, dict), "Supply designProposalBinding.")
    require(
        type(binding.get("schema_version")) is int and binding["schema_version"] == 1,
        "Use design proposal schema version 1.",
    )
    require(
        scope in {"semantic", "program", "ticket"} and binding.get("scope") == scope,
        "The proposal must belong to this planning scope.",
    )
    require(
        isinstance(source, dict)
        and text(source.get("ref"))
        and text(source.get("hash")),
        "The planning source needs its reference and hash.",
    )
    require(
        binding.get("source") == source,
        "The proposal must explain the exact current planning source.",
    )
    document = binding.get("document")
    require(
        isinstance(document, dict), "Supply the published Linear document identity."
    )
    require(
        all(text(document.get(k)) for k in ("id", "url", "revision", "hash")),
        "Supply the document ID, URL, revision, and content hash.",
    )
    url = urlparse(document["url"])
    require(
        url.scheme == "https"
        and url.hostname == "linear.app"
        and bool(url.path.strip("/")),
        "The proposal must link to a Linear document.",
    )
    require(
        bool(re.fullmatch(r"sha256:[0-9a-f]{64}", document["hash"])),
        "Use a SHA-256 content hash.",
    )
    readback = binding.get("readback")
    require(
        isinstance(readback, dict)
        and readback.get("revision") == document["revision"]
        and readback.get("hash") == document["hash"],
        "The published and read-back document revision and hash must match.",
    )
    visuals = binding.get("visuals")
    validate_visuals(visuals)
    require(
        isinstance(visuals, list)
        and bool(visuals)
        and all(
            isinstance(v, dict) and text(v.get("ref")) and text(v.get("kind"))
            for v in visuals
        ),
        "Identify the proposal's in-document visuals.",
    )


def validate_completion(job, result):
    headers = job.get("customHeaders", {})
    if result.get("status") != "completed" or headers.get("resultContract") != CONTRACT:
        return
    source_name = headers.get("sourceBindingVariable")
    source = job.get("variables", {}).get(source_name)
    variables = result.get("variables", {})
    validate_proposal(
        variables.get("designProposalBinding"), headers.get("planningScope"), source
    )
    if variables.get(source_name, source) != source:
        raise RuntimeFailure(
            "invalid_design_proposal", "Publication cannot replace its planning source."
        )
