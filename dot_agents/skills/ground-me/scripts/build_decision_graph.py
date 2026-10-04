#!/usr/bin/env python3
"""Build decision-lineage model data for a permitted graph renderer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build decision-lineage graph JSON.")
    parser.add_argument("packet", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        with arguments.packet.open("r", encoding="utf-8") as stream:
            payload: Any = json.load(stream)
    except FileNotFoundError:
        error = {"code": "file_not_found", "message": "The packet file does not exist."}
        payload = None
    except json.JSONDecodeError as exception:
        error = {
            "code": "invalid_json",
            "message": f"JSON parsing failed at line {exception.lineno}, column {exception.colno}.",
        }
        payload = None
    except OSError as exception:
        error = {"code": "read_failed", "message": str(exception)}
        payload = None
    else:
        error = None

    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    if isinstance(payload, dict):
        target = payload.get("target")
        lineage = payload.get("decision_lineage")
        if not isinstance(target, dict) or not isinstance(target.get("identifier"), str):
            error = {"code": "invalid_target", "message": "Expected a target identifier."}
        elif not isinstance(lineage, list):
            error = {"code": "invalid_lineage", "message": "Expected a decision_lineage array."}
        else:
            target_id = f"target:{target['identifier']}"
            nodes.append(
                {
                    "id": target_id,
                    "type": str(target.get("type", "target")),
                    "label": target["identifier"],
                }
            )
            seen = {target_id}
            for item in lineage:
                if not isinstance(item, dict):
                    continue
                source_type = item.get("source_type")
                source_ref = item.get("source_ref")
                relationship = item.get("relationship")
                if not all(isinstance(value, str) and value.strip() for value in (source_type, source_ref, relationship)):
                    continue
                node_id = f"{source_type}:{source_ref}"
                if node_id not in seen:
                    nodes.append({"id": node_id, "type": source_type, "label": source_ref})
                    seen.add(node_id)
                edges.append({"source": node_id, "target": target_id, "relationship": relationship})
    elif error is None:
        error = {"code": "invalid_document", "message": "Expected a JSON object."}

    result = {
        "status": "ok" if error is None else "error",
        "packet": str(arguments.packet),
        "nodes": nodes,
        "edges": edges,
        "errors": [] if error is None else [error],
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif error is not None:
        print(f"{error['code']}: {error['message']}", file=sys.stderr)
    else:
        print(json.dumps({"nodes": nodes, "edges": edges}, indent=2, sort_keys=True))
    return 0 if error is None else 2


if __name__ == "__main__":
    sys.exit(main())
