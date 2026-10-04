"""Validated local records. The exported schemas come from these models."""
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

Text = Annotated[str, Field(min_length=1, pattern=r"\S")]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Count = Annotated[int, Field(ge=0)]
Names = list[Text]
Category = Literal["production", "tests", "tooling", "configuration", "support", "generated", "vendor", "excluded", "unclassified"]
MAINTAINED = {"production", "tests", "tooling", "configuration"}


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Rule(Record):
    pattern: Text
    category: Category
    reason: Text


class Inventory(Record):
    rules: list[Rule]


class Obligation(Record):
    id: Text
    behavior: Text


class Basis(Record):
    authorization: Text
    preserve: Annotated[list[Obligation], Field(min_length=1)]
    roots: Annotated[Names, Field(min_length=1)]
    variants: Annotated[Names, Field(min_length=1)]
    seams: Names
    unknown_consumers: Names
    approved_retirements: Names


class FileRecord(Record):
    kind: Literal["file", "symlink", "special"]
    sha256: Hash
    mode: Count
    size: Count
    category: Category


class Run(Record):
    format_version: Literal[1]
    original: Text
    original_hash: Hash
    metadata_hash: Hash
    baseline_hash: Hash
    inventory_hash: Hash
    basis_hash: Hash
    inventory: Inventory
    basis: Basis
    files: dict[str, FileRecord]
    gaps: Names


class Candidate(Record):
    id: Text
    responsibility: Text
    change: Literal["retirement", "consolidation", "re-expression"]
    canonical_owner: Text
    preserve: Annotated[Names, Field(min_length=1)]
    consumers: Annotated[Names, Field(min_length=1)]
    unknown_consumers: Names
    retired_behavior: Names
    eliminate: Annotated[Names, Field(min_length=1)]
    removal_paths: Annotated[Names, Field(min_length=1)]
    evidence: Annotated[Names, Field(min_length=1)]
    rationale: Literal["still-required", "replaceable", "obsolete", "temporary", "accidental", "unknown"]
    depends_on: Names
    target: Text


class CandidateSet(Record):
    baseline_hash: Hash
    candidates: Annotated[list[Candidate], Field(min_length=1)]


class Check(Record):
    id: Annotated[str, Field(pattern=r"^[A-Za-z0-9_-]+$")]
    kind: Literal["e2e", "integration", "behavior", "analyzer"]
    argv: Annotated[Names, Field(min_length=1)]
    version_argv: Annotated[Names, Field(min_length=1)]
    obligations: Names
    seams: Names
    exercised_scope: Annotated[Names, Field(min_length=1)]
    skipped_scope: Names


class Checks(Record):
    checks: Annotated[list[Check], Field(min_length=1)]


class Runtime(Record):
    docker: Text
    socket: Text
    image: Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]
    platform: Literal["linux/amd64", "linux/arm64"]
    cloc: Text
    cloc_library: Text | None = None
    timeout_seconds: Annotated[int, Field(ge=1, le=3600)] = 120


class Authorization(Record):
    baseline_hash: Hash
    source: Text
    allowed_paths: Annotated[Names, Field(min_length=1)]
    expires: Text


class Review(Record):
    patch_hash: Hash
    reviewer: Text
    evidence_hash: Hash
    structural_improvement: Text
    counterexamples: Names
    unresolved: Names
    anti_gaming: Text


class ExceptionApproval(Record):
    patch_hash: Hash
    waived: Annotated[list[Literal["ratio", "net_growth"]], Field(min_length=1)]
    source: Text
    rationale: Text
    expires: Text


class Measurement(Record):
    before: Count
    after: Count
    added: Count
    removed: Count
    net: int
    ratio_met: bool
    by_category: dict[str, dict[str, Count]]
    file_counts: dict[str, dict[str, Count]]
    excluded_files: dict[str, Names]
    moved_files: list[list[Text]]
    counter_version: Text
    counter_hash: Hash


class Execution(Record):
    argv: Annotated[Names, Field(min_length=1)]
    exit_code: int
    log: Text
    log_hash: Hash
    timed_out: bool


class Receipt(Record):
    subject: Literal["baseline", "candidate"]
    snapshot_hash: Hash
    check: Check
    image: Text
    rules_hash: Hash
    version: Execution
    execution: Execution


class Verification(Record):
    format_version: Literal[1]
    status: Literal["VERIFIED", "VERIFIED_WITH_EXCEPTIONS", "INCOMPLETE", "FAILED"]
    patch_hash: Hash
    baseline_hash: Hash
    candidate_hash: Hash
    inventory_hash: Hash
    basis_hash: Hash
    checks_hash: Hash
    engine_hash: Hash
    runtime_hash: Hash
    measurement: Measurement | None
    receipts: list[Receipt]
    measurement_receipts: list[Execution]
    failures: Names
    gaps: Names
    waivers: Names
    evidence_hash: Hash
    review_hash: Hash | None
    exception_hash: Hash | None


if __name__ == "__main__":
    import json
    from pathlib import Path
    for name, model in {"run": Run, "candidate": CandidateSet, "verification": Verification,
                        "inventory": Inventory, "basis": Basis, "checks": Checks,
                        "runtime": Runtime, "authorization": Authorization,
                        "review": Review, "exception": ExceptionApproval}.items():
        (Path(__file__).resolve().parents[1] / "schemas" / f"{name}.schema.json").write_text(
            json.dumps(model.model_json_schema(), indent=2) + "\n")
