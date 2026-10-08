---
name: override-writing-plans
description: >-
  Use ONLY when the user explicitly asks to install, apply, overwrite, replace,
  or humanize the superpowers:writing-plans skill. Trigger phrases include
  "run override-writing-plans", "install the human plan style", "overwrite
  superpowers writing-plans", "replace the writing-plans skill", or "apply the
  writing-plans override". Performs a one-time file modification: locates the
  installed superpowers:writing-plans SKILL.md on disk, backs it up, and
  replaces its contents with human-targeted plan-writing instructions bundled in
  this skill. DO NOT trigger on requests to actually write a plan; that is a
  different skill. This skill mutates files, so trigger only on deliberate,
  explicit invocation.
---

# Override `superpowers:writing-plans`

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


This skill performs a one-time file mutation. It locates the installed `superpowers:writing-plans` SKILL.md on the user's machine, backs it up, and replaces its contents with the human-targeted version bundled at `replacement-SKILL.md`.

This is an operational skill, not a behavior skill. Run only when the user explicitly invokes it.

## What "human-targeted" means

The replacement reframes the plan-writing skill so its consumer is the human user, not an agent. The replacement content (in `replacement-SKILL.md`) instructs Claude to produce concise plans with pseudocode and links instead of finished code, fronted by a linked keywords list. The user does not need to read the replacement content to run this skill — it's already complete.

## Procedure

Follow these steps in order. Do not skip the confirmation step.

### Step 1 — Locate the target file

Search the most likely install locations. Run each command until one returns a result:

```bash
# 1. Standard Claude Code plugin install (most likely)
find ~/.claude/plugins -type f -path "*/writing-plans/SKILL.md" 2>/dev/null

# 2. Alternate config dir (XDG-style installs)
find ~/.config/claude/plugins -type f -path "*/writing-plans/SKILL.md" 2>/dev/null

# 3. Fallback — anywhere under home matching the superpowers layout
find ~ -type f -path "*/superpowers/*/writing-plans/SKILL.md" 2>/dev/null

# 4. Last resort — anywhere under home for any writing-plans skill
find ~ -type f -path "*/writing-plans/SKILL.md" 2>/dev/null
```

**Outcomes:**

- **Zero matches:** Stop. Tell the user superpowers may not be installed, or the layout has changed. Ask them to point you at the path manually before proceeding.
- **One match:** Continue to Step 2 with that path.
- **Multiple matches:** Show all paths to the user and ask which one to overwrite. Do not pick one yourself.

### Step 2 — Idempotency check

Read the first 30 lines of the target file. If you see both of these markers:

- A YAML `name: writing-plans` line
- A heading `## Audience` near the top of the body

…the override is already applied. Stop and tell the user. Do not create another backup.

Otherwise, continue.

### Step 3 — Show the user what will change, and confirm

Display:

1. The full absolute path of the target file
2. The first ~20 lines of its current contents (so the user can confirm it is the right skill)
3. The backup path that will be created: `<target-path>.backup-<YYYYMMDD-HHMMSS>`

Then ask, verbatim or close to it: **"Proceed with the overwrite?"**

Wait for an affirmative reply (yes / proceed / go ahead / confirmed). On anything else, stop.

### Step 4 — Back up the original

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp "<target-path>" "<target-path>.backup-${TS}"
```

Echo the backup path back to the user.

### Step 5 — Overwrite with the replacement

The replacement content lives at `replacement-SKILL.md` adjacent to this SKILL.md. Resolve the path relative to wherever this skill is installed (typically `~/.claude/skills/superpowers-writing-plans-override/replacement-SKILL.md`), then copy it over the target:

```bash
cp "<this-skill-dir>/replacement-SKILL.md" "<target-path>"
```

### Step 6 — Verify

Read the first 10 lines of the target file. Confirm:

- YAML frontmatter is intact and starts with `name: writing-plans`
- The body opens with `# Writing Plans` followed shortly by `## Audience`

Report the result: target path overwritten, backup at `<backup-path>`, override now active.

## Failure modes and how to handle them

**Permission denied on `cp`.** Plugin directories are sometimes read-only. Do not attempt `sudo` or `chmod` automatically. Tell the user the path is read-only and offer two options:

1. They re-run the operation with elevated permissions themselves.
2. They install the replacement at `~/.claude/skills/writing-plans/SKILL.md` instead, which usually shadows the plugin version. Offer to copy `replacement-SKILL.md` there as a fallback (this needs its own confirmation).

**Disk full / write error.** Report the error and stop. The original is unmodified — the backup was a copy, not a move.

**`find` not available (Windows cmd.exe).** Claude Code on Windows typically runs under Git Bash or WSL where `find` is available. If the shell genuinely lacks `find`, ask the user for the path to the target file directly.

## Cross-platform notes

- macOS / Linux: the `find` and `cp` commands above work as written.
- Windows under Git Bash / WSL: same commands work.
- Windows under PowerShell: substitute `Get-ChildItem -Recurse -Filter SKILL.md | Where-Object FullName -like "*writing-plans*"` and `Copy-Item`. Only use this path if the user confirms PowerShell.

## After running

Tell the user:

1. Where the backup is, in case they want to revert (`mv <backup-path> <target-path>`).
2. That the next time `superpowers:writing-plans` is consulted, it will follow the new instructions.
3. That re-running this skill is safe — the idempotency check in Step 2 will catch a second invocation.
