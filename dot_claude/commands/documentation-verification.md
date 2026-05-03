# Documentation Verification & Sync

You are the **team lead** of a documentation verification swarm for the PulseframeOS monorepo. Your job is to detect and fix documentation drift — places where docs no longer match the actual codebase.

## Execution Model: Agent Team (Swarm Pattern)

You orchestrate a **self-organizing team** of specialist workers. Each worker claims tasks from a shared queue, performs verification, applies fixes, and reports findings back to you (team lead).

### Lifecycle

```
1. Tool search — discover all available tools and skills, write to log file
2. TeamCreate("doc-verify")
3. TaskCreate (all verification tasks — independent, no blockedBy)
4. Spawn 5 teammates (parallel workers via Agent with team_name + name)
5. Workers self-organize: claim tasks, verify, fix, report
6. You synthesize findings into Drift Report
7. SendMessage shutdown to each worker
8. TeamDelete cleanup + delete tools log file
```

---

## Step 1: Tool Search

Load ALL available tools and skills. Use ToolSearch to enumerate every deferred tool, MCP server capability, and available skill. Create a temporary log file at `/tmp/doc-verify-tools.log` containing all relevant tools grouped by category (file ops, MCP servers, git, search, etc.). Each worker loads this file on startup so they have full awareness of available capabilities — no hardcoded tool lists.

This ensures the team adapts to whatever MCP servers and tools are currently active in the session.

---

## Step 2: Create Team & Tasks

Create the team, then create ALL tasks upfront as a shared pool. Workers will self-assign.

```
TeamCreate({ team_name: "doc-verify", description: "Documentation verification and sync for PulseframeOS" })
```

Then create these tasks (ALL independent — no `blockedBy` dependencies — workers race to claim):

### Structural Integrity Tasks

**Task: link-integrity**
> Verify every relative markdown link in these files resolves to an existing file:
> - `pulseframe-documentation/DOCUMENTATION-INDEX.md`
> - `pulseframe-documentation/README.md`
> - `pulseframe-documentation/architecture/README.md`
> - `pulseframe-documentation/engineering/README.md`
> - `pulseframe-documentation/CLAUDE.md`
> - Root `CLAUDE.md`
> - Root `KNOWLEDGE_BASE.md`
>
> For each file, extract all `[text](relative/path)` patterns and check if the target file exists via Glob. Report broken links with source file, line number, and dead target. Auto-fix by removing dead links or correcting paths if the target was moved.

**Task: claude-md-cascade**
> Cross-reference EVERY `CLAUDE.md` file under `pulseframe-documentation/` (~40 files) against the actual directory contents where it lives. Each CLAUDE.md describes its sibling files — verify those siblings actually exist. Use `Glob("pulseframe-documentation/**/CLAUDE.md")` to find them all, then for each, read it, extract file references, and verify with Glob. Auto-fix stale references.

**Task: stale-dates**
> For every doc file with a `Last Updated` header/field, compare the stated date against `git log -1 --format=%ci -- <file>`. Flag any where the git modification date is >14 days newer than the stated "Last Updated" date. Auto-fix by updating the date to match git.

### Codebase Cross-Reference Tasks

**Task: service-topology**
> Read `compose.yml` and extract: service names, ports, images, profiles, networks, volumes, depends_on, environment variables. Cross-reference against:
> - Root `CLAUDE.md` (Service Architecture tables)
> - `pulseframe-documentation/architecture/inter-service-communication.md`
> - `pulseframe-documentation/architecture/CLAUDE.md` (Service Topology Quick Reference)
>
> Check specifically: port numbers, Docker network name consistency (`devnet` vs `pulseframe-network`), service/container names, profile assignments (minimal vs full), volume names, environment variable completeness, PomoDojo references (verify if code exists or still PLANNED-only). Auto-fix any verifiable discrepancies.

**Task: agentic-subsystem-verify**
> Read actual Python source and cross-reference against docs:
> - **Agents** in `agentic-subsystem/src/agent/` vs `pulseframe-documentation/architecture/agentic-subsystem/`
> - **Tools** (`@function_tool` decorators) in `agentic-subsystem/src/agent/tools/` vs `agent-system.md`
> - **Models** in `agentic-subsystem/src/models/` vs `data-models.md`
> - **API routes** in `agentic-subsystem/api/` vs `api-reference.md`
> - **Python version** in `pyproject.toml` vs docs
> - **Dependencies** in `pyproject.toml` vs documented tech stack
>
> Auto-fix documentation where code is authoritative.

**Task: pulseframe-api-verify**
> Read actual source and cross-reference against docs:
> - **Express routes** in `pulseframe/app/src/routes/` vs `pulseframe-documentation/architecture/pulseframe/`
> - **Database schema** in `pulseframe/db/` vs `database.md`
> - **WebSocket events** in source vs `chat-socket-events.md` and `websocket-events.md`
> - **package.json** dependencies vs documented tech stack
>
> Auto-fix documentation where code is authoritative.

**Task: aida-verify**
> Read actual source and cross-reference against docs:
> - **Backend routes** in `aida/aida-backend/` (general-routes/, mobile-only-routes/, desktop-only-routes/) vs `pulseframe-documentation/architecture/aida/backend/`
> - **Mobile components** in `aida/mobile/` vs `frontend/mobile.md`
> - **Desktop components** in `aida/desktop/` vs `frontend/web.md`
> - **package.json** files vs documented tech stack
> - **Tauri config** in `aida/desktop/src-tauri/` vs desktop architecture docs
>
> Auto-fix documentation where code is authoritative.

**Task: devtools-infra-verify**
> Cross-reference:
> - `dev-tools/devenv.sh` capabilities vs `pulseframe-documentation/engineering/tools/devenv.md`
> - `devlocal.sh` commands vs root `CLAUDE.md` devlocal section
> - `.env.compose.example` variables vs root `CLAUDE.md` environment variable documentation
> - DigitalOcean production topology (use DO MCP: `apps-list`, `apps-get-info`, `db-cluster-list`) vs documented infrastructure
> - MongoDB collections (use MongoDB MCP: `list-collections`) vs documented collections
>
> Auto-fix documentation where infrastructure state is authoritative.

### Content Quality Tasks

**Task: stale-references-audit**
> Search ALL documentation (`pulseframe-documentation/**/*.md`) for references to:
> - Old directory structures (`01-Product`, `06-Templates`, `engineering/conventions/`, `implementation/`)
> - Removed infrastructure (Upsun, Azure, non-existent services)
> - Incorrect absolute paths (e.g., `/Users/Apple/Work/PulseframeOS/` — note case: actual is `/Users/Apple/work/pulseframeos/`)
> - Deprecated patterns or APIs that have been superseded
>
> Use Grep to find these patterns. Auto-fix path case issues and remove/update stale references.

**Task: in-progress-plans**
> Read each plan in `pulseframe-documentation/engineering/_in-progress/` and verify:
> - Are "in progress" items actually still in progress, or completed/abandoned?
> - Do phase status markers match actual codebase state?
> - Should completed features be archived out of `_in-progress/`?
>
> Flag ambiguous status for human review. Auto-fix clearly completed items.

**Task: feature-registry-sync**
> Read `pulseframe-documentation/engineering/features/_registry.md` and verify:
> - Every registered feature has corresponding feature doc files
> - Feature status markers (planned, in-progress, complete) match reality
> - No features in codebase are missing from the registry
>
> Auto-fix status markers where codebase state is clear. Flag ambiguous cases.

---

## Step 3: Spawn Worker Team

Spawn **5 workers** in a single message (all `run_in_background: true`). Each gets the same swarm worker prompt. Use `subagent_type: "general-purpose"` so they can both read AND edit files.

### Worker Prompt Template

Each worker receives this prompt (with their name substituted):

```
You are a documentation verification worker on team "doc-verify". Your name is {worker-name}.

## Your Loop

1. Call TaskList() to see available tasks
2. Find a task with status "pending" and no owner
3. Claim it: TaskUpdate({ taskId: "N", owner: "{worker-name}", status: "in_progress" })
4. Execute the verification described in the task description
5. Apply auto-fixes directly using the Edit tool (do NOT just report — fix it)
6. Complete it: TaskUpdate({ taskId: "N", status: "completed" })
7. Send your findings to team-lead via SendMessage:
   - What you checked
   - What you fixed (file, line, before/after)
   - What needs human review (ambiguous issues)
8. Check TaskList() again. If more pending tasks exist, go to step 2.
9. If no tasks remain, send a final "all done" message to team-lead.

## Fixing Rules

- **Auto-fix** (just do it): Broken links, wrong port numbers, wrong file paths, stale directory references, incorrect service names, wrong network names, outdated "Last Updated" dates, case-incorrect paths
- **Auto-fix with note**: Missing files referenced by index docs (remove dead link), PomoDojo references (add "PLANNED" markers where missing)
- **Flag for human review**: Ambiguous architectural claims, feature status disputes, anything where the "correct" state is unclear

## Key Paths

Root:           /Users/Apple/work/pulseframeos/
Docs:           /Users/Apple/work/pulseframeos/pulseframe-documentation/
Agentic:        /Users/Apple/work/pulseframeos/agentic-subsystem/
AIDA:           /Users/Apple/work/pulseframeos/aida/
Pulseframe:     /Users/Apple/work/pulseframeos/pulseframe/
Dev-Tools:      /Users/Apple/work/pulseframeos/dev-tools/
Compose:        /Users/Apple/work/pulseframeos/compose.yml

## Available Tools

Read `/tmp/doc-verify-tools.log` for the full list of available tools and MCP servers for this session. Key categories:
- **File ops**: Glob, Grep, Read, Edit
- **Git**: Bash (git log only — for date checks)
- **Infrastructure**: DigitalOcean MCP, MongoDB MCP (if available)
- See the tools log for all other available MCP servers and capabilities
```

Spawn with these names: `verifier-1`, `verifier-2`, `verifier-3`, `verifier-4`, `verifier-5`

---

## Step 4: Monitor & Synthesize

As workers send you findings via SendMessage, collect them. When all tasks are completed (check TaskList), synthesize everything into a single **Drift Report**.

### Drift Report Format

Output this to the user:

```markdown
# Documentation Drift Report — {YYYY-MM-DD}

## Summary
- Tasks completed: N/N
- Files checked: ~N
- Issues found: N
- Auto-fixed: N
- Flagged for review: N

## Auto-Fixed Issues
| File | Line | Issue | Fix Applied |
|------|------|-------|-------------|

## Flagged for Human Review
| File | Line | Issue | Why Ambiguous |
|------|------|-------|---------------|

## Verification Coverage
| Area | Worker | Status | Notes |
|------|--------|--------|-------|
| Link integrity | | pass/warn/fail | |
| CLAUDE.md cascade | | pass/warn/fail | |
| Stale dates | | pass/warn/fail | |
| Service topology | | pass/warn/fail | |
| Agentic-subsystem | | pass/warn/fail | |
| Pulseframe API | | pass/warn/fail | |
| AIDA ecosystem | | pass/warn/fail | |
| Dev-tools & infra | | pass/warn/fail | |
| Stale references | | pass/warn/fail | |
| In-progress plans | | pass/warn/fail | |
| Feature registry | | pass/warn/fail | |
```

---

## Step 5: Cleanup

After the report is complete:

1. Search for any documentation files (*.md) that are NOT in `pulseframe-documentation/` and are NOT `CLAUDE.md` files — delete stray docs to prevent repo clutter
2. Send shutdown to each worker: `SendMessage({ to: "verifier-N", message: { type: "shutdown_request", reason: "Verification complete" } })`
3. Wait for shutdown approvals
4. `TeamDelete()` to clean up team and task files
5. Delete `/tmp/doc-verify-tools.log` (the tools log created in Step 1)

---

## Tool Reference

| Tool | Purpose |
|------|---------|
| `TeamCreate` | Create the "doc-verify" team |
| `TaskCreate` | Create verification tasks in the shared pool |
| `TaskList` | Monitor task progress |
| `TaskUpdate` | Workers claim and complete tasks |
| `Agent` (with `team_name` + `name`) | Spawn worker teammates |
| `SendMessage` | Workers report findings; leader sends shutdown |
| `TeamDelete` | Clean up after completion |
| `Glob/Grep/Read/Edit` | File operations for verification and fixes |
| `Bash` | Git log for date checks only |
| `mcp__digitalocean__*` | Production infrastructure verification |
| `mcp__MongoDB__*` | MongoDB collection verification |
