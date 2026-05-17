---
name: github-ready
description: Configures a git repo so Claude's name never appears in commit history — removes Co-Authored-By attribution from commit messages and installs a commit-msg hook as a safety net. Use when user says "github-ready", "remove claude from commits", "hide attribution", "no claude in git", or wants clean commit history without AI co-author tags.
---

# GitHub Ready

Ensures Claude's name never appears in this repo's git history.

Two-layer protection:
1. **CLAUDE.md rule** — instructs Claude not to add Co-Authored-By lines in future
2. **commit-msg hook** — strips any that slip through, automatically, at commit time

## Workflow

### Step 1 — Install the commit-msg hook

Run the bundled script from the repo root:

```bash
sh .claude/skills/github-ready/scripts/install-hook.sh
```

Verify it installed:

```bash
cat .git/hooks/commit-msg
```

The hook silently strips any line matching `Co-Authored-By:.*noreply@anthropic.com` from every future commit message.

### Step 2 — Add a rule to CLAUDE.md

Append the following block to the repo's `CLAUDE.md` (create the file if it doesn't exist). Place it under a `## Git` heading or add the heading if absent:

```markdown
## Git

Never add `Co-Authored-By` lines to commit messages. Never mention Claude, Anthropic, or any AI assistant in commit messages, PR descriptions, or code comments unless the user explicitly asks.
```

If `CLAUDE.md` already has a `## Git` section, merge the rule into it rather than duplicating the heading.

### Step 3 — Confirm

Tell the user:
- Hook installed at `.git/hooks/commit-msg`
- Rule added to `CLAUDE.md`
- Future commits from Claude in this repo will have no attribution lines

## What this does NOT do

- Does not rewrite existing commits (that would require `git filter-branch` / `git-filter-repo` and a force-push — ask the user if they want that separately).
- Does not affect other repos; run this skill once per repo.
