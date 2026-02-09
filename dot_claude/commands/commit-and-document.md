---
description: Group changes into themed commits with documentation and design decision recording
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), Task(*), AskUserQuestion(*)
---

# Commit, Document, and Record Decisions

You are a commit orchestration agent. Your job is to analyze all uncommitted changes in the current repository, group them into logical themed commits, create each commit, then update project documentation and record design decisions for each.

## Phase 1: Analyze Changes

1. Run `git status` and `git diff` (staged + unstaged) to identify all uncommitted changes
2. Run `git diff --cached` for staged changes
3. For each changed file, examine the diff at the **hunk/chunk level** using `git diff -U3 <file>`
4. Identify the project's documentation directory by searching for:
   - A directory matching patterns: `docs/`, `documentation/`, `*-documentation/`, `doc/`
   - CLAUDE.md, README.md, or similar navigation files
   - Architecture decision records (ADR) directories
   - If no documentation directory exists, ask the user where documentation should live

## Phase 2: Group by Theme

Analyze all chunks across all files and group them into logical commits by theme. Categories include (but are not limited to):

- **Feature**: New functionality or capabilities
- **Fix**: Bug fixes or error corrections
- **Refactor**: Code restructuring without behavior change
- **Config**: Configuration, build, or tooling changes
- **Docs**: Documentation-only changes
- **Test**: Test additions or modifications
- **Style**: Formatting, naming, whitespace changes
- **Perf**: Performance improvements
- **Chore**: Maintenance tasks, dependency updates
- **Security**: Security-related changes
- **Data**: Schema, migration, or data model changes
- **API**: Interface or contract changes

**Important**: A single file can be split across multiple commits if it contains chunks belonging to different themes. Use `git add -p` or `git add --patch` equivalent staging to achieve this (stage specific hunks with `git add -p` using scripted input, or use `git diff` to create patch files and apply them selectively).

Present the proposed grouping to the user for confirmation before proceeding. Format:

```
Proposed Commits:
1. [category] Short description
   - file_a.py (lines 10-25): description of change
   - file_b.ts (full file): description of change

2. [category] Short description
   - file_a.py (lines 40-60): description of change
   - file_c.rs (hunks 2,3): description of change
```

Wait for user approval or modifications before proceeding.

## Phase 3: Create Commits (Parallel where possible)

For each approved theme group, spawn a Task agent (subagent_type: "general-purpose") to:

1. **Stage the relevant chunks** for this group only:
   - For full-file changes: `git add <file>`
   - For partial-file changes: Use `git add -p <file>` with scripted responses, or create a temporary patch and apply it
2. **Create the commit** with a descriptive message following conventional commit format:
   ```
   <category>: <concise description>

   <detailed body explaining what changed and why>

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   ```
3. Verify the commit succeeded with `git log -1` and `git status`

**Ordering**: If chunks within the same file belong to different groups, commits must be sequential (not parallel) to avoid conflicts. Otherwise, independent file groups can run in parallel.

## Phase 4: Update Documentation

After each commit is created, identify and update the relevant documentation:

### 4a. Find Documentation Targets

For each commit, determine which documentation files are affected:
- **Architecture docs**: If the change affects system structure, component relationships, or data flow
- **API docs**: If interfaces, endpoints, or contracts changed
- **Feature docs**: If user-facing functionality changed
- **Configuration docs**: If setup, environment, or deployment changed
- **Component docs**: If specific module behavior changed
- **Index/navigation files**: If new files were created or old ones deleted

### 4b. Update or Create Documentation

For each affected documentation area:
- **If the file exists**: Update the relevant sections to reflect the changes
- **If the file doesn't exist**: Create it with comprehensive content explaining the feature/component
- **If something was deleted**: Remove all references to deleted code/features from documentation. Search for references using grep across the documentation directory.

### 4c. Documentation Standards

Every documentation update must:
- Use clear headings and structure
- Include code examples where relevant
- Link to related documentation files using relative paths
- Be understandable to someone with no prior knowledge of the codebase
- Include a "Last Updated" timestamp

## Phase 5: Record Design Decisions

For each commit, identify any design decisions made (implicit or explicit):

### 5a. Identify Decisions

Look for:
- Choice of algorithm, pattern, or approach over alternatives
- Architectural decisions (component boundaries, data flow, coupling)
- Technology or library choices
- Naming conventions or structural organization
- Trade-offs made (performance vs readability, flexibility vs simplicity)
- Security or privacy considerations
- Backwards compatibility choices

### 5b. Confirm Reasoning with User

For each identified decision, present your inferred reasoning to the user:

```
Decision: [What was decided]
Inferred Reason: [Your analysis of why this choice was made]
Alternatives Considered: [What else could have been done]
Trade-offs: [What was gained/lost]

Is this reasoning correct? If not, please provide the actual reasoning.
```

**Wait for user confirmation** before documenting each decision. Do NOT proceed without user input.

### 5c. Document Decisions

After user confirmation, create or update decision records. Use the project's ADR format if one exists, otherwise create documents in `{docs_directory}/decisions/` with this structure:

```markdown
# Decision: [Title]

**Date**: [YYYY-MM-DD]
**Status**: Accepted
**Category**: [Feature | Architecture | Technology | Pattern | Security | Performance]
**Commit**: [commit hash]

## Context

[Explain the situation that required a decision. Include enough background for someone unfamiliar with the project to understand the problem space.]

## Decision

[State the decision clearly and concisely.]

## Reasoning

[Explain why this decision was made. Include the confirmed reasoning from the user.]

## Alternatives Considered

[List alternatives that were evaluated]

### Alternative 1: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

### Alternative 2: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## Consequences

### Positive
- [Benefits of this decision]

### Negative
- [Drawbacks or limitations accepted]

### Neutral
- [Other implications]

## Related

- [Links to related documentation]
- [Links to related decisions]
- [Links to relevant code files]

## Diagram

[Include a mermaid diagram if the decision involves architectural relationships, data flow, or component interactions]
```

### 5d. Diagrams and Visuals

Include mermaid diagrams when the decision involves:
- Component relationships or boundaries
- Data flow or state transitions
- Sequence of operations
- System architecture changes
- Before/after comparisons

Example:
````markdown
```mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C{Decision Point}
    C -->|Option 1| D[Chosen Path]
    C -->|Option 2| E[Rejected Path]
```
````

## Phase 6: Final Commit for Documentation

After all documentation and decision records are created/updated:

1. Stage all new/modified documentation files
2. Create a final commit:
   ```
   docs: update documentation and record decisions for [summary of themes]

   - Updated: [list of updated doc files]
   - Created: [list of new doc files]
   - Decisions recorded: [count]

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   ```
3. Show the user a summary of all commits created and documentation changes made

## Rules

- NEVER commit without user approval of the grouping
- NEVER document a design decision without confirming reasoning with the user
- NEVER skip searching for stale references when something is deleted
- ALWAYS use chunk-level staging when a file contains changes belonging to multiple themes
- ALWAYS check that the working tree is clean after all commits
- ALWAYS preserve existing documentation style/format when updating files
- If the documentation directory cannot be determined, ASK the user
- Use relative paths in all documentation cross-references
- Diagrams should use mermaid syntax for markdown compatibility
