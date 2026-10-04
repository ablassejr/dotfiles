---
name: writing-plans
description: Use whenever the user asks to write an implementation plan, planning document, plan.md, design plan, refactor plan, feature plan, fix plan, or any step-by-step guide for building/fixing/refactoring code. Also trigger on phrases like "plan this out", "write a plan for X", "create a plan", "planning phase", or "design doc". The plan is a guide a HUMAN will read and execute — never an agent. Pseudocode and documentation links only, never finished code.
---

# Writing Plans

> **Save all plans to:** `pulseframeos/pulseframeos/pulseframe-documentation/_engineering/_in-progress/*`

## Audience

The reader is a human user, not an agent. Humans read far slower than agents and pay attention cost per word. Every sentence must earn its place. The plan is a guide the user will follow themselves — you are not the implementer.

## What the plan is, and is not

| Is                                     | Is not                             |
| -------------------------------------- | ---------------------------------- |
| A walkthrough of what the user must do | The implementation                 |
| Pseudocode where logic is non-obvious  | Finished, runnable code            |
| Links to canonical docs and references | Inline regurgitation of those docs |
| Brief rationale for design choices     | Essays defending design choices    |
| The minimum needed for the user to act | Everything you happen to know      |

If you find yourself writing real code, stop. The user wants a guide, not a deliverable.

## Required document structure

The plan must open with these two sections, in this order, before anything else.

### 1. Keywords

A bulleted list of every technical term, abbreviation, library, protocol, or concept the document will use. **Each entry is a hyperlink to its canonical definition** — official docs, MDN, RFC, the library's own reference, Wikipedia, or a high-quality Stack Overflow answer if no better source exists.

**Do not define terms inline.** The user can follow the link if they need a definition. The point of this section is to let the rest of the document drop term explanations entirely.

Example:

```markdown
## Keywords

- [JWT](https://datatracker.ietf.org/doc/html/rfc7519)
- [bcrypt](https://en.wikipedia.org/wiki/Bcrypt)
- [middleware (Express)](https://expressjs.com/en/guide/using-middleware.html)
- [HOC](https://legacy.reactjs.org/docs/higher-order-components.html)
- [WAL](https://www.postgresql.org/docs/current/wal-intro.html)
```

### 2. Overview

One short paragraph. What is being built or changed, and the one-line rationale for the chosen approach. Not a sales pitch. Not a recap of the user's request.

## The body of the plan

After Keywords and Overview, walk through the work as numbered steps. For each step:

- **One sentence** stating what to do.
- **Pseudocode** only if the logic is non-obvious. Skip it for trivial steps.
- **A link** to the relevant doc, file path in the codebase, or library reference.
- **If a design pattern or decision is involved**, explain in one or two sentences why this choice — then move on. No paragraphs.

## Hard rules

1. **No real code.** Pseudocode only. Use a `pseudo` or language-tagged fence and write in a deliberately abstract style — no full imports, no boilerplate, no error-handling scaffolding unless it's the _point_ of the step.
2. **Link instead of explain.** If a doc page exists, link it. Do not paraphrase what the docs already say.
3. **Single-sentence design rationale.** "Using a [decorator](link) here because the cross-cutting concern repeats in three places." That's the whole explanation.
4. **Cut load-bearing-only.** No throat-clearing ("Great question!"), no restating the user's request, no hedging ("you might want to maybe consider possibly..."), no recaps at the end.
5. **Lists for steps, prose for narrative.** Don't pad list items with explanations that belong in prose. Don't bury sequential steps inside paragraphs.
6. **End with open questions, not a summary.** If there are decisions the user must make before starting, list them. Otherwise stop.

## Template

Use this verbatim as the skeleton:

````markdown
# [Feature / Fix / Refactor name] — Plan

## Keywords

- [term](link)
- [term](link)

## Overview

[One paragraph. What and why-this-approach.]

## Steps

### 1. [Step name]

[One sentence on what to do.]

```pseudo
// only if logic is non-obvious
```

Reference: [link to doc / file path / library reference]

### 2. [Step name]

[...]

## Open questions

- [Decision the user must make before starting]
- [Ambiguity that needs resolution]
````

## Examples of what to cut

| Tempting to write                                                                | Cut to                                                                                      |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| "JSON Web Tokens (JWTs) are a compact, URL-safe means of representing claims..." | (delete; link [JWT](https://datatracker.ietf.org/doc/html/rfc7519) in Keywords)             |
| "First, we'll need to set up the database. Databases are important because..."   | "1. Add a `users` table. Reference: [migrations docs](link)."                               |
| "Now that we've added the route, let's discuss what we just did..."              | (delete entirely)                                                                           |
| "You could use either bcrypt or argon2; bcrypt has been around longer and..."    | "Use [argon2](link) — bcrypt is acceptable but argon2 is the current OWASP recommendation." |

## Self-check before delivering

Before you hand the plan to the user, scan it for:

- [ ] Keywords section present, every term linked, no inline definitions
- [ ] No real code anywhere — only pseudocode in non-obvious spots
- [ ] Every step has a link (doc, file, or library ref)
- [ ] No paragraph longer than 3 sentences
- [ ] No restatement of the user's request
- [ ] No closing summary

If any check fails, revise before delivering.
