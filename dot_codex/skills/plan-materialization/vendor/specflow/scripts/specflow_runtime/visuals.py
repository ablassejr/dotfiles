"""Graph renderer policy shared by workflow, publication, and packet boundaries."""

import json
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qs

from .client import RuntimeFailure, digest

POLICY = "graph-renderers-v1"
RENDERERS = {"figma", "likec4", "archify"}
NON_GRAPH_KINDS = {"screenshot", "photo", "video", "table", "code", "diff", "mockup"}


def require(condition, message):
    if not condition:
        raise RuntimeFailure("invalid_visual", message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def hashed_file(reference):
    require(isinstance(reference, dict), "Supply a file path and SHA-256 digest.")
    path, expected = reference.get("path"), reference.get("sha256")
    require(
        nonempty(path) and Path(path).is_absolute(),
        "Visual evidence needs an absolute file path.",
    )
    require(
        isinstance(expected, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", expected),
        "Visual evidence needs a SHA-256 digest.",
    )
    try:
        content = Path(path).read_bytes()
    except OSError as error:
        raise RuntimeFailure(
            "invalid_visual", "Visual evidence is unavailable: " + path
        ) from error
    require(digest(content) == expected, "Visual evidence changed: " + path)
    return content


def validate_visuals(visuals):
    require(
        isinstance(visuals, list),
        "Declare the complete visuals array; use [] when no visual is produced.",
    )
    for visual in visuals:
        require(
            isinstance(visual, dict) and nonempty(visual.get("ref")),
            "Every visual needs its reference.",
        )
        kind = visual.get("kind")
        require(
            isinstance(kind, str) and kind in NON_GRAPH_KINDS | {"graph"},
            "Classify visual content as graph, screenshot, photo, video, table, code, diff, or mockup; image and embed are formats.",
        )
        if kind != "graph":
            continue
        renderer = visual.get("renderer")
        require(
            isinstance(renderer, str) and renderer in RENDERERS,
            "Graph-like visuals must use figma, likec4, or archify.",
        )
        try:
            receipt = json.loads(hashed_file(visual.get("receipt")))
        except (ValueError, UnicodeError) as error:
            raise RuntimeFailure(
                "invalid_visual", "The render receipt must be JSON."
            ) from error
        require(
            isinstance(receipt, dict)
            and receipt.get("status") == "COMPLETED"
            and receipt.get("adapter") == renderer,
            "The completed render receipt must identify the selected renderer.",
        )
        require(
            nonempty(receipt.get("operationId"))
            and isinstance(receipt.get("inputHash"), str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", receipt["inputHash"]),
            "The receipt needs its render operation and input hash.",
        )
        artifact = visual.get("artifact")
        require(
            isinstance(artifact, dict),
            "Bind the displayed graph to its rendered artifact.",
        )
        if renderer in {"likec4", "archify"}:
            hashed_file(artifact)
            path = Path(artifact["path"]).resolve()
            manifest = receipt.get("manifest")
            require(
                nonempty(manifest)
                and Path(manifest).resolve()
                == Path(visual["receipt"]["path"]).resolve(),
                "Use the renderer's published manifest.",
            )
            require(
                path.parent == Path(manifest).resolve().parent
                and isinstance(receipt.get("files"), dict)
                and receipt["files"].get(path.name) == artifact["sha256"],
                "The graph must be an output in the render receipt.",
            )
        else:
            ref, sha = artifact.get("ref"), artifact.get("sha256")
            require(
                nonempty(ref)
                and isinstance(sha, str)
                and re.fullmatch(r"sha256:[0-9a-f]{64}", sha),
                "A Figma graph needs its node URL and read-back hash.",
            )
            url = urlparse(ref)
            require(
                url.scheme == "https"
                and url.hostname in {"figma.com", "www.figma.com"}
                and re.match(r"^/(design|file)/[^/]+", url.path)
                and parse_qs(url.query).get("node-id"),
                "Use a Figma Design node URL; FigJam boards are not graph renderers.",
            )
            result = receipt.get("result")
            read_back = (
                result.get("visual_artifact") if isinstance(result, dict) else None
            )
            require(
                isinstance(read_back, dict)
                and all(
                    read_back.get(key) == value
                    for key, value in {
                        "ref": ref,
                        "sha256": sha,
                        "file_type": "DESIGN",
                    }.items()
                ),
                "The Figma receipt must bind that exact Design node and read-back hash.",
            )


def validate_embedded_visuals(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "visuals":
                validate_visuals(item)
            else:
                validate_embedded_visuals(item)
    elif isinstance(value, list):
        for item in value:
            validate_embedded_visuals(item)


def validate_visual_completion(job, result):
    if result.get("status") != "completed":
        return
    variables = result.get("variables", {})
    require(isinstance(variables, dict), "Completion variables must be an object.")
    headers = job.get("customHeaders", {})
    binding_name = headers.get("visualBindingVariable")
    if binding_name:
        binding = variables.get(binding_name)
        require(
            isinstance(binding, dict) and "visuals" in binding,
            "This visual step must return " + binding_name + ".visuals.",
        )
    elif headers.get("visualInventory") == "required":
        require(
            "visuals" in variables,
            "This step must return its complete visuals inventory, including an explicit empty array when appropriate.",
        )
    validate_embedded_visuals(variables)
