---
name: owasp-security
description: Use when reviewing code, configs, APIs, authentication, authorization, input handling, dependency exposure, or deployment changes for OWASP-style security risks.
---

# OWASP Security Review

Use this skill to evaluate security-sensitive implementation work against the OWASP Top 10 and API Security Top 10.

## Workflow

1. Identify the trust boundaries, entry points, authentication state, and data stores affected by the change.
2. Check authorization before authentication-adjacent details: object ownership, tenant boundaries, role checks, and bypass paths.
3. Review input handling for injection, unsafe deserialization, path traversal, SSRF, command execution, and file upload risks.
4. Inspect secret handling, logging, error responses, dependency usage, browser exposure, and transport settings.
5. Report concrete findings with file paths, exploit preconditions, impact, and the smallest practical remediation.

## Output

Lead with confirmed issues ordered by severity. If no issues are found, state the residual risk and the checks performed.
