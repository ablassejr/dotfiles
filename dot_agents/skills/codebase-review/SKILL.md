---
name: codebase-review
description: Use when reviewing code for design quality, evaluating module interfaces and depth, detecting information leakage or complexity issues, assessing naming and documentation, or conducting architecture reviews focused on long-term maintainability
---

# Codebase Review

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


## Overview

Systematic code review framework based on John Ousterhout's "A Philosophy of Software Design" (2nd Ed., 2021). **Core principle: the primary goal of software design is reducing complexity.** Complexity is anything that makes a system hard to understand or modify, measured by cost to developers — not by lines of code or class count.

**Complexity formula:** `C = Σ(cp × tp)` — weighted sum of each module's complexity (cp) times the fraction of development time spent on it (tp). Isolate unavoidable complexity in modules developers rarely touch.

## When to Use

- Reviewing PRs or changesets for design quality
- Evaluating module structure, interface design, and abstraction depth
- Assessing whether code changes make the system simpler or more complex
- Auditing a codebase for maintainability issues
- Deciding how to decompose a system into modules
- When code "works but feels wrong" and you need vocabulary for why

**Not for:** Style/formatting checks, performance optimization, security audits (see owasp-security), test coverage analysis.

## Review Framework

Evaluate code across these dimensions in priority order.

### 1. Module Depth

**Principle:** Deep modules have simple interfaces and powerful functionality. Shallow modules have complex interfaces relative to their implementation.

| Signal | Deep (Good) | Shallow (Bad) |
|--------|-------------|---------------|
| Interface-to-functionality ratio | Few params, rich behavior | Many params, thin wrapper |
| Caller burden | Caller thinks less | Caller manages details |
| Exemplar | Unix I/O: 5 calls hide disk complexity | Java I/O: 3 wrappers for basic file read |

**Ask:** "Does this module's interface hide significant complexity, or does it just reorganize it?"

### 2. Information Hiding & Leakage

**Principle:** Each module should encapsulate design decisions. Information leakage occurs when the same knowledge is embedded in multiple modules, creating backdoor dependencies.

**Detection patterns:**
- Two modules sharing format/protocol knowledge (e.g., FileReader + FileWriter both knowing CSV structure — when format changes, both break)
- Temporal decomposition: organizing by execution order (read→process→write) rather than by knowledge domains
- Changes to one data format requiring edits across multiple files

**Ask:** "If this design decision changes, how many modules need updating?"

### 3. Interface Quality

**Principles:**
- **Pull complexity downward:** Simple interfaces matter more than simple implementations. The module author should suffer, not callers.
- **General-purpose design:** Build "somewhat general-purpose" interfaces covering current needs + foreseeable common uses, without hypothetical features.
- **Different layer, different abstraction:** Adjacent layers with similar abstractions indicate poor decomposition. Each layer must provide meaningfully different abstraction.

**Ask:**
- "Is this interface simpler than the problem it solves?"
- "Could this method signature serve common use cases beyond the current one without adding parameters?"
- "Does each layer transform the abstraction, or just relay it?"

### 4. Pass-Through Detection

**Anti-patterns:**
- **Pass-through methods:** Methods that delegate with identical or near-identical signatures, adding no logic. Each adds interface complexity without functionality.
- **Pass-through variables:** Variables threaded through multiple call layers just to reach a distant consumer. Consider context objects or configuration registries.
- **Decorators without value:** Wrappers that reformat arguments but contribute nothing.

**Ask:** "Does this layer add functionality, or just relay?"

### 5. Error Handling

**Principle:** Define errors out of existence. Design APIs so error conditions cannot occur rather than catching and propagating exceptions up the stack.

| Approach | Example |
|----------|---------|
| **Broaden success definition** | Tcl `unset`: changed from "error if variable doesn't exist" to "ensure variable doesn't exist" — callers never need try/catch |
| **Absorb edge cases** | Python slicing: `list[0:1000]` on 3-element list returns 3 elements silently |
| **Exception masking** | Handle recoverable errors internally at low levels rather than propagating |

**Ask:** "Can this API be redesigned so the caller never needs to handle this error?"

**Caution:** This applies to API design, not to ignoring genuine failures. Truly exceptional conditions (disk full, network down) still need handling — but most "errors" can be designed away.

### 6. Naming & Consistency

**Principles:**
- Names should be **precise** (not vague like "data", "info", "result", "handle") and **consistent** (same concept → same name everywhere).
- Hard-to-pick name = design smell. If you can't name it clearly, the entity may have unclear responsibilities.
- Consistency is cognitive leverage: one learned pattern applied everywhere multiplies comprehension.
- Real-world consequence: a generic variable named "block" caused a 6-month bug because it failed to convey the object was a specific disk block type.

**Red flags:** Generic names, same concept with multiple names across modules, names requiring implementation reading to understand.

### 7. Comments & Documentation

**Principles:**
- Comments describe **what** and **why**, never **how** (implementation is visible in code).
- Interface comments describe the abstraction contract; implementation comments explain non-obvious logic.
- Comments-first development: write interface comments before implementation to validate the design.
- If a comment just repeats code, delete it. If it reveals the designer's intent, it's essential.

**Red flags:**
- Comment repeating code: `// increment i` above `i++`
- Implementation details in interface docs (leaks abstraction)
- No comments on non-obvious logic
- Very long comment suggesting the underlying abstraction is too complex to describe concisely

## Quick Reference: 14 Red Flags

| # | Red Flag | Detection |
|---|----------|-----------|
| 1 | **Shallow Module** | Interface complexity ≈ implementation complexity |
| 2 | **Information Leakage** | Same knowledge embedded in multiple modules |
| 3 | **Temporal Decomposition** | Modules organized by execution order, not information |
| 4 | **Overexposure** | API exposes internal details callers shouldn't need |
| 5 | **Pass-Through Method** | Method delegates with identical/near-identical signature |
| 6 | **Repetition** | Same code pattern duplicated across locations |
| 7 | **Special-General Mixture** | Special-case logic tangled with general-purpose mechanism |
| 8 | **Conjoined Methods** | Understanding method A requires reading method B |
| 9 | **Comment Repeats Code** | Comment says exactly what the code says |
| 10 | **Implementation in Interface Docs** | Interface documentation reveals implementation details |
| 11 | **Vague Name** | Name too generic to convey specific purpose |
| 12 | **Hard to Pick Name** | Difficulty naming suggests unclear responsibility |
| 13 | **Hard to Describe** | Difficulty documenting suggests design problem |
| 14 | **Nonobvious Code** | Reader can't understand behavior without deep study |

## Strategic vs Tactical Assessment

**Strategic programming:** Invest ~10-20% of development time in design improvement. Working code is not enough — code must minimize complexity for future developers.

**Tactical programming (anti-pattern):** Shipping the fastest solution without design consideration. The "tactical tornado" developer produces features rapidly but leaves compounding complexity debt that eventually paralyzes the team.

**Ask:** "Does this change make the system slightly better or slightly worse for the next developer who touches it?"

## Additional Principles

- **Design it twice:** Consider 2-3 radically different approaches before committing. Even if the first idea seems fine, alternatives often reveal better tradeoffs.
- **Complexity isolation:** Quarantine unavoidable complexity (parsing, protocol handling, legacy integration) in boundary modules developers rarely modify.
- **Composition over inheritance:** Implementation inheritance creates hidden dependencies between parent and child. Prefer composition with explicit interfaces.
- **Consistency:** Enforce naming conventions, parameter ordering, and structural patterns within and across modules. Inconsistency forces developers to re-learn familiar concepts.

## Review Output Structure

Organize findings by severity:

1. **Structural Issues** (red flags 1-4): Module depth, leakage, decomposition, overexposure
2. **Interface Issues** (red flags 5, 7-8): Pass-through, mixing, coupling
3. **Communication Issues** (red flags 9-14): Comments, naming, clarity
4. **Repetition** (red flag 6): Duplicated logic or knowledge

For each finding, provide:
- Which red flag is triggered
- The specific code location
- Why it increases complexity (which symptom: change amplification, cognitive load, or unknown unknowns)
- A concrete suggestion applying the relevant principle

## Common Review Mistakes

| Mistake | Reality |
|---------|---------|
| Fixating on method length | Short methods aren't inherently good; depth matters more than size |
| Requiring comments everywhere | Only non-obvious code and interfaces need comments |
| Splitting everything into tiny classes | Creates shallow modules; prefer fewer, deeper ones |
| Rejecting all duplication (DRY absolutism) | Some duplication is preferable to a wrong abstraction |
| Reviewing style instead of design | Formatting tools handle style; reviews target complexity |
| Accepting "it works" as sufficient | Working code that increases complexity is still a problem |
| Applying rules dogmatically | Ousterhout's principles are judgment-based, not mechanical rules; context determines application |
