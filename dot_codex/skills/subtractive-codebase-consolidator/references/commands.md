# Commands and local records

Use an existing Python 3.10 or newer environment with `pydantic==2.13.5`. The package never installs its dependencies. The executable image needs Python 3, a full Perl runtime, and the repository's own tools. All paths below are examples; choose the actual local repository, package, and run directory from the user's request.

From the package directory, first discover the files and prepare the preservation basis and classification policy outside the original repository.

```sh
python scripts/snapshot.py inventory /repos/example /reviews/discovery.json
python scripts/snapshot.py init /repos/example /reviews/run-001 --inventory /reviews/inventory.json --basis /reviews/basis.json
```

`inventory.json` uses first-match patterns over POSIX relative paths. `*` can match a slash, so put specific rules first. There are no automatic build, generated, vendor, or extension exclusions. Unmatched files remain unclassified. Explicit exclusions need a reason; inspect credentials and private runtime paths before making a runnable snapshot.

```json
{
  "rules": [
    {"pattern": ".env", "category": "excluded", "reason": "Local credentials are outside this analysis"},
    {"pattern": "tests/*", "category": "tests", "reason": "Maintained behavior tests"},
    {"pattern": "generated/*", "category": "generated", "reason": "Derived output from the canonical schema"},
    {"pattern": "*.py", "category": "production", "reason": "Maintained Python source"},
    {"pattern": "*.md", "category": "support", "reason": "Local rationale and documentation"}
  ]
}
```

`basis.json` records the actual authorization source and observable obligations. Identifiers connect the behavior to checks; they are not inferred from test filenames.

```json
{
  "authorization": "User requested a read-only audit of text normalization",
  "preserve": [{"id": "normalize", "behavior": "API and batch inputs produce the same canonical text and documented errors"}],
  "roots": ["API handler", "batch command"],
  "variants": ["API", "batch"],
  "seams": ["input transport to normalizer"],
  "unknown_consumers": [],
  "approved_retirements": []
}
```

The resulting `run.json` contains the file inventory and the original, metadata, baseline, inventory, and basis hashes. `baseline/` is an independent source copy. Do not edit it; create a new run when its basis changes.

When evidence supports a candidate, supply `candidates.json` with the recorded baseline hash. Each removal path is a file present in the original inventory. Closures can overlap without producing duplicate savings.

```json
{
  "baseline_hash": "REPLACE_WITH_RUN_BASELINE_HASH",
  "candidates": [{
    "id": "C1",
    "responsibility": "Text normalization",
    "change": "consolidation",
    "canonical_owner": "normalize_input",
    "preserve": ["normalize"],
    "consumers": ["API handler", "batch command"],
    "unknown_consumers": [],
    "retired_behavior": [],
    "eliminate": ["Batch-local duplicate normalizer"],
    "removal_paths": ["src/batch_normalizer.py"],
    "evidence": ["Boundary cases in the local analyzer and contract reports"],
    "rationale": "replaceable",
    "depends_on": [],
    "target": "Both consumers use the same normalizer while preserving their transport contracts and errors."
  }]
}
```

```sh
python scripts/plan.py /reviews/run-001 /reviews/candidates.json
python scripts/report.py /reviews/run-001
```

`plan.json` lists ordered candidates, reasons a candidate is blocked, overlaps, and unique removal paths. It deliberately does not turn file counts into a source-line estimate. `report.md` is local Markdown.

When the user authorizes an experiment, record that existing permission in `authorization.json`. The source field points to the actual user instruction; do not manufacture an approval. The expiration uses an ISO 8601 timestamp with timezone.

```json
{
  "baseline_hash": "REPLACE_WITH_RUN_BASELINE_HASH",
  "source": "User authorized the normalization experiment in this task",
  "allowed_paths": ["src/*", "tests/*"],
  "expires": "2026-09-30T23:59:59+00:00"
}
```

```sh
python scripts/snapshot.py experiment /reviews/run-001 --authorization /reviews/authorization.json
```

The helper creates `candidate/`. The assistant makes the authorized changes there. A separately prepared patch can instead be copied for read-only verification; this command does not grant permission to edit its source.

```sh
python scripts/snapshot.py candidate /reviews/run-001 /reviews/already-prepared-patch
```

Use `checks.json` to declare actual commands. An end-to-end check can also cover a seam when it exercises that integration. An analyzer-only check does not satisfy a preservation obligation. Command arguments are arrays, not shell expressions.

```json
{
  "checks": [{
    "id": "normalization-contract",
    "kind": "e2e",
    "argv": ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"],
    "version_argv": ["python3", "--version"],
    "obligations": ["normalize"],
    "seams": ["input transport to normalizer"],
    "exercised_scope": ["API and batch modes; valid and malformed input"],
    "skipped_scope": []
  }]
}
```

`runtime.json` pins a locally installed tool image by its full `sha256:` image ID and platform. Supply the Perl cloc script, not a shell wrapper. `cloc_library` is optional for standalone cloc; package-manager installations may need their existing Perl library directory. Those files are hashed and streamed into the container with the inputs.

```json
{
  "docker": "/usr/local/bin/docker",
  "socket": "/var/run/docker.sock",
  "image": "sha256:REPLACE_WITH_64_HEXADECIMAL_IMAGE_ID",
  "platform": "linux/arm64",
  "cloc": "/local/tools/cloc.pl",
  "cloc_library": null,
  "timeout_seconds": 120
}
```

Collect analyzer evidence alone with `collect.py`, or collect preservation checks and measurements together with `verify.py`. Neither executes on the host or downloads a missing tool.

```sh
python scripts/collect.py /reviews/run-001 --checks /reviews/checks.json --runtime /reviews/runtime.json --subject baseline
python scripts/verify.py /reviews/run-001 --checks /reviews/checks.json --runtime /reviews/runtime.json
```

`collect.py` writes subject receipts and command logs. Each `*.attempt.json` file identifies the owned container and its lifecycle state so an interrupted attempt can be diagnosed. `verify.py` writes `verification.json` with source measurements and executed receipts. The first verification phase returns exit code 2 while independent review is pending; that is a usable evidence packet, not a final pass.

The reviewer receives the actual snapshots, contracts, consumers, check definitions, logs, patch hash, and evidence hash. The review is a typed local record such as the following.

```json
{
  "patch_hash": "REPLACE_WITH_VERIFICATION_PATCH_HASH",
  "evidence_hash": "REPLACE_WITH_VERIFICATION_EVIDENCE_HASH",
  "reviewer": "Independent reviewer context",
  "structural_improvement": "API and batch consumers share one normalization authority",
  "counterexamples": [],
  "unresolved": [],
  "anti_gaming": "The patch removes the duplicate mechanism and retains the declared boundary tests"
}
```

```sh
python scripts/verify.py /reviews/run-001 --finalize --review /reviews/review.json
python scripts/report.py /reviews/run-001
```

When the user approves a numerical exception, supply a patch-bound record using the `exception` schema and add `--exception /reviews/exception.json` during finalization. The only permitted waiver names are `ratio` and `net_growth`. Fields are `patch_hash`, `waived`, `source`, `rationale`, and `expires`. A ratio waiver does not waive growth or any evidence requirement. There is no `--allow-ratio-exception` bypass flag.

Successful finalization returns a shape such as `{"status":"VERIFIED","measurement":{"before":120,"after":90,"added":10,"removed":40,"net":-30,"ratio_met":true,...},...}`. These numbers are illustrative. Missing or malformed evidence produces INCOMPLETE; failed checks and unwaived numerical policy produce FAILED. Exit codes are 0 for verified results, 1 for failed results, 2 for incomplete results, and 130 for an interrupted command. Analyzer collection uses exit code 1 when any declared command failed.

All JSON inputs reject unknown fields and wrong types, including booleans in integer measurement fields. The generated schemas describe the consumer-facing records. Schemas are regenerated from `contracts.py`; changes to them belong with changes to the public contract.

Run the static tests through Python's standard test runner. Set `SUBTRACTIVE_TEST_RUNTIME` to an existing runtime JSON to include the real Docker and cloc tests. Without it, those tests explicitly report skips.

```sh
python -m unittest discover -s tests -v
```
