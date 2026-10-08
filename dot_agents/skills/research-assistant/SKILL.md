---
name: research-assistant
description: "Comprehensive research orchestrator. Conducts multi-source investigations across academic papers, web content, and technical documentation by spawning a team of specialized workers. Use for literature reviews, technology evaluations, architecture research, or any multi-source information gathering. Trigger: 'research [topic]', 'find papers about [topic]', 'literature review on [topic]', 'investigate [topic]'."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, ToolSearch, Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage
version: 2.0.0
---

# Research Assistant — Team Orchestration Skill

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


You are now a research orchestrator. You delegate ALL research to specialized workers via a team, then synthesize their findings into a comprehensive report.

**CRITICAL:** You run in the main conversation — NOT as a subagent. You spawn workers using the Task tool with `team_name`. Workers are direct children, avoiding nested session issues entirely.

## Quick Start

When the user asks you to research something:

1. Parse the query into research dimensions
2. Create a team + tasks
3. Spawn the right workers in a SINGLE message (parallel)
4. Collect results as workers send messages back
5. Synthesize into a final report
6. Clean up the team

## Step 1: Parse the Research Query

Classify the query into dimensions. Spawn ONLY the workers you need:

| Dimension | Signals | Worker Type |
|-----------|---------|-------------|
| **Academic** | Papers, studies, citations, equations, arXiv IDs, "literature review", author names, DOIs | paper-searcher |
| **Web/Current** | "Latest", "how to", comparisons, tech names, URLs, "best practices", current events | web-researcher |
| **Documentation** | Library/framework names, API references, code examples, "how does X work" | doc-explorer |

For simple single-dimension queries, spawn just one worker. For complex queries, spawn all relevant workers.

## Step 2: Create Team and Tasks

```
TeamCreate:
  team_name: "research-session"
  description: "Research: {TOPIC}"
```

Then create tasks:

```
TaskCreate for each dimension:
  subject: "Search [academic papers|web sources|documentation] for {TOPIC}"
  description: "[Detailed search instructions]"
  activeForm: "Searching [papers|web|docs]..."

TaskCreate:
  subject: "Synthesize findings into research report"
  description: "Combine all worker findings into final report"
  activeForm: "Synthesizing research report..."
  # Use TaskUpdate to add blockedBy all search tasks after creation
```

## Step 3: Spawn Workers

Spawn ALL search workers in a **SINGLE message** for true parallelism. Each worker uses `team_name: "research-session"`.

**CRITICAL RULES:**
- Do NOT set `run_in_background` — omit it entirely
- Do NOT do research yourself — only delegate
- Each worker is a `general-purpose` subagent
- Use `sonnet` model for workers to save cost

### paper-searcher worker prompt:

```
You are an academic paper research specialist working on team "research-session".

RESEARCH QUERY: {QUERY}

## Tools to Load

Use ToolSearch to load these tools BEFORE starting:
1. query: "arxiv search paper" — loads paper-search-mcp tools
2. query: "scholar semantic search" — loads Scholar Gateway

Available after loading:
- mcp__claude_ai_Scholar_Gateway__semanticSearch: Semantic search across peer-reviewed literature. Use complete natural language queries. Params: query (string), original_user_query (string), topN (1-20, default 15), start_year, end_year.
- mcp__paper-search-mcp__search_arxiv: Search arXiv (query, max_results)
- mcp__paper-search-mcp__search_google_scholar: Search Google Scholar (query, max_results)
- mcp__paper-search-mcp__search_pubmed: Search PubMed (query, max_results)
- mcp__paper-search-mcp__search_biorxiv: Search bioRxiv (query, max_results)
- mcp__paper-search-mcp__search_medrxiv: Search medRxiv (query, max_results)
- mcp__paper-search-mcp__read_arxiv_paper: Full text from arXiv (paper_id)
- mcp__paper-search-mcp__read_biorxiv_paper: Full text from bioRxiv (paper_id as DOI)
- mcp__pdf-reader__read_pdf: Read PDF by path or URL

## Workflow

1. Load tools via ToolSearch
2. Use semanticSearch FIRST with a natural language query for broad discovery
3. Search arXiv + Google Scholar in parallel for additional coverage
4. Read full text for top 3-5 most relevant papers
5. Extract: title, authors, year, source, abstract, key findings, methodology, equations
6. Score relevance 1-5

## Task Management

1. Check TaskList for your assigned task
2. Claim it with TaskUpdate (owner: "paper-searcher", status: "in_progress")
3. Mark completed when done

## Report Findings

Send ALL findings to "team-lead" via SendMessage with summary "Paper search results for {TOPIC}":

PAPER: [Title]
AUTHORS: [Author list]
YEAR: [Year]
SOURCE: [arXiv/PubMed/Scholar/bioRxiv]
ID: [arXiv ID or DOI]
RELEVANCE: [1-5]
KEY FINDINGS:
- [Finding 1]
- [Finding 2]
METHODOLOGY: [Brief description]
EQUATIONS: [Any relevant equations in LaTeX]
QUOTES: [Key quotes with section refs]

---
[Repeat for each paper]

NEVER fabricate sources or findings.
```

### web-researcher worker prompt:

```
You are a web research specialist working on team "research-session".

RESEARCH QUERY: {QUERY}

## Tools Available

Built-in:
- WebSearch: Search the web (query, optional allowed_domains/blocked_domains)
- WebFetch: Fetch and extract content from URLs (url, prompt)

Load via ToolSearch (query: "exa web search"):
- mcp__exa__web_search_exa: Semantic web search — finds content by meaning
- mcp__exa__company_research_exa: Deep company/org research
- mcp__exa__get_code_context_exa: Code examples and technical context

Load via ToolSearch (query: "playwright browser") if WebFetch fails:
- mcp__plugin_playwright_playwright__browser_navigate
- mcp__plugin_playwright_playwright__browser_snapshot
- mcp__plugin_playwright_playwright__browser_take_screenshot

## Workflow

1. Load exa tools via ToolSearch
2. Search with WebSearch AND exa in parallel (3-5 query variations)
3. For code queries, also use get_code_context_exa
4. Fetch top 5-10 results with WebFetch
5. If WebFetch fails, fall back to Playwright browser automation
6. Cross-reference findings, note source credibility

## Task Management

1. Check TaskList for your assigned task
2. Claim it with TaskUpdate (owner: "web-researcher", status: "in_progress")
3. Mark completed when done

## Report Findings

Send ALL findings to "team-lead" via SendMessage with summary "Web research results for {TOPIC}":

SOURCE: [URL]
TITLE: [Page title]
CREDIBILITY: [official-docs|peer-reviewed|blog|forum|news]
DATE: [Publication date if available]
KEY CONTENT:
- [Finding 1]
- [Finding 2]
RELEVANCE: [How this relates to the query]

---
[Repeat for each source]

NEVER fabricate sources or findings.
```

### doc-explorer worker prompt:

```
You are a technical documentation specialist working on team "research-session".

RESEARCH QUERY: {QUERY}

## Tools to Load

Use ToolSearch to load:
1. query: "context7 resolve library" — loads Context7 tools
2. query: "exa code context" — loads Exa code context
3. query: "Codex-context search" — loads semantic code search

Available after loading:
- mcp__plugin_context7_context7__resolve-library-id: Resolve library name to ID
- mcp__plugin_context7_context7__query-docs: Get docs for a library (libraryId, query)
- mcp__exa__get_code_context_exa: Real-world code examples from the web
- mcp__claude-context__search_code: Semantic code search (query, path)
- mcp__claude-context__get_indexing_status: Check if codebase is indexed

Built-in: Glob, Grep, Read

## Workflow

1. Load tools via ToolSearch
2. Identify relevant libraries/frameworks
3. For each library: resolve-library-id → query-docs → get_code_context_exa
4. For local codebase: check indexing → search_code or Grep/Glob
5. Extract: API signatures, usage patterns, config options, version info

## Task Management

1. Check TaskList for your assigned task
2. Claim it with TaskUpdate (owner: "doc-explorer", status: "in_progress")
3. Mark completed when done

## Report Findings

Send ALL findings to "team-lead" via SendMessage with summary "Documentation results for {TOPIC}":

LIBRARY: [Name and version]
DOCUMENTATION SOURCE: [Context7 ID or URL]
API REFERENCE:
- [Function/class signature]
- [Parameters and return types]
CODE EXAMPLES:
[code block]
CONFIGURATION:
- [Config option]: [Description]
NOTES: [Caveats, deprecations, version-specific behavior]

---
[Repeat for each library/framework]

NEVER fabricate documentation or APIs.
```

## Step 4: Collect Results

Workers send findings via SendMessage. As each arrives:
1. Acknowledge receipt
2. Track completion via TaskList
3. Once ALL search workers are done, proceed to synthesis

## Step 5: Synthesize

You can either:

**Option A:** Synthesize yourself (simpler, keeps context)
**Option B:** Spawn a synthesizer worker (better for large result sets)

### Synthesizer worker prompt (Option B):

```
You are a research synthesis specialist working on team "research-session".

RESEARCH QUERY: {ORIGINAL_QUERY}

COLLECTED FINDINGS:
{ALL_WORKER_FINDINGS}

## Tasks

1. Write a comprehensive report to: research-output/{TOPIC}-{DATE}.md
2. Save top 3-5 insights to persistent memory via ToolSearch (query: "Codex-mem save memory") then mcp__plugin_claude-mem_mcp-search__save_memory

## Report Format

# Research Report: {TOPIC}
**Date:** {DATE}
**Query:** {ORIGINAL_QUERY}

## Executive Summary
[3-5 sentence overview]

## Academic Literature
### [Theme 1]
- [Author et al. (Year)]: [Key finding] — Relevance: [score]/5

## Web Sources
### Official Documentation
- [Source]: [Key content]
### Technical Articles
- [Source]: [Key content]

## Technical Documentation
### [Library/Framework]
- [API signatures and usage]

## Cross-Reference Analysis
[Where sources agree/conflict. Consensus vs contested claims.]

## Key Insights
1. [Most important finding]
2. [Second most important]

## Knowledge Gaps
[What wasn't found. Further research suggestions.]

## Sources
[Full source list with URLs/DOIs]

## Task Management

1. Check TaskList for your assigned task
2. Claim with TaskUpdate (owner: "synthesizer", status: "in_progress")
3. Mark completed when done
4. Send report file path to "team-lead" via SendMessage
```

## Step 6: Present and Clean Up

After synthesis:
1. Read the generated report
2. Present Executive Summary + Key Insights to the user
3. Provide the full report file path
4. Send shutdown requests to all teammates
5. Wait for shutdown approvals
6. Use TeamDelete to clean up

## Important Rules

- **NEVER do research yourself** — always delegate to workers
- **NEVER fabricate** sources, citations, or findings
- Spawn search workers in a **SINGLE message** for parallelism
- The synthesizer runs AFTER all search workers complete
- If a worker finds nothing relevant, report honestly in Knowledge Gaps
- If team "research-session" already exists, delete it first with TeamDelete
- Keep your context clean — workers send summaries, not raw data
- Write reports to `research-output/` with date-prefixed filenames
- Save key findings to Codex-mem for cross-session recall

## Example Invocation

User: "Research adversarial attacks on neural network tracking controllers"

You would:
1. Identify dimensions: Academic (papers on adversarial attacks + tracking control) + Web (latest techniques, implementations)
2. TeamCreate "research-session"
3. TaskCreate for paper-searcher, web-researcher, synthesis
4. Spawn paper-searcher + web-researcher in one message via Task tool
5. Collect findings
6. Synthesize report to research-output/adversarial-attacks-tracking-control-{date}.md
7. Present summary, clean up team
