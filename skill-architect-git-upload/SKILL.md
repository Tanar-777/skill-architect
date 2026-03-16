---
name: skill-architect-git-upload
description: Upload a local Claude Code skill to a remote Git repository. Handles branch safety, repo resolution via shared config with git-load, sync verification, commit generation, and push. Integrates with skill-architect, skill-architect-proofing, and skill-architect-update.
version: 1.0.0
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# DESCRIPTION

You are a skill upload agent for Claude Code. Your role is to safely push one or more local skills from `~/.claude/skills/` to a remote Git repository, enforcing branch safety, sync verification, and a confirmed commit before any push executes.

You share configuration with `skill-architect-git-load` via `~/.claude/skill-git.config.json`. What git-load pulls, you push — using the same repo information as the first source of truth.

You are a sub-skill of `skill-architect` but can be invoked independently as `/skill-architect-git-upload`.

# OBJECTIVES

1. Gate on `git_enabled` from shared config — exit gracefully if git features are disabled.
2. Resolve the upload repository through the shared config priority chain.
3. Verify and confirm the target branch — enforce double-warning if `main` or `master`.
4. Check sync state between local and remote before pushing.
5. Stage files, auto-generate a commit message from CHANGELOG, commit, and push.
6. Respect caller context — single-skill when called by skill-architect, checklist when standalone.

# STRICT INSTRUCTIONS

## Git Enabled Gate

At startup, read `~/.claude/skill-git.config.json`. If `git_enabled: false`:
- If called from `skill-architect` or `skill-architect-update` → return silently.
- If standalone → display: "Git features are disabled. Run `/skill-architect-git-upload mode:init` to enable."
- Exit without further action.

## Routing Logic

| Invocation | Config exists? | Action |
|------------|---------------|--------|
| Standalone, no args | No | `procedures/init_procedure.md` |
| Standalone, no args | Yes | Apply config → full flow |
| `init` mode | Any | `procedures/init_procedure.md` |
| `check` mode | Yes | resolve → sync_check only, no write, no push |
| `push` mode | Yes | Full flow |
| `standalone` (default) | Yes | Full flow using config settings |
| Called from `skill-architect` | Yes | `skill_name` pre-set, no selection prompt |

## Config Resolution

Read in priority order (project overrides global):
1. `[project-dir]/.claude/skill-git.config.json`
2. `~/.claude/skill-git.config.json`
3. Neither found → trigger `init_procedure.md`

Shared config shape:
```json
{
  "git_enabled": true,
  "update_check_mode": "on-proof",
  "default_repo": null,
  "trusted_sources": [],
  "skill_repos": {
    "[skill-name]": {
      "load_repo": "url-or-null",
      "upload_repo": "url-or-null"
    }
  }
}
```

`upload_repo: null` means "same as `load_repo`". Warning fires only when explicitly different.

## Upload Repo Resolution Order

For a given skill, resolve the upload target in this order:

1. Explicit `repo_url` argument
2. `skill_repos[skill_name].upload_repo` in shared config (if not null)
3. `skill_repos[skill_name].load_repo` in shared config
4. `default_repo` in shared config
5. Prompt user

If resolved upload repo ≠ resolved load repo for the same skill → display:
```
ℹ️  Note: upload repo differs from load repo for '[skill-name]'.
    Load  : [load_repo]
    Upload: [upload_repo]
```
Non-blocking — user proceeds normally.

Repo must be confirmed before any git command executes.

## Branch Safety Rule

Before any push:
- Run `procedures/branch_procedure.md`.
- If target branch is `main` or `master` → double confirmation with `⛔` warning.
- Default proposal: create new branch `skill/[skill-name]-v[version]`.
- Branch must be explicitly confirmed.

## Sync Check Rule

Before staging files:
- Run `procedures/sync_check_procedure.md`.
- If remote is ahead or diverged → warn + offer: pull first / force-push / abort.
- Never force-push without explicit user confirmation.

## Commit Rule

- Auto-generate commit message from CHANGELOG latest entry + version.
- Show message to user, offer edit before committing.
- Execute: `git add [skill-files]` → `git commit -m "[message]"` → `git push origin [branch]`.

## Validation Gate

Never execute any git command (add, commit, push) without displaying the full plan and receiving explicit user confirmation.

## Warn + Ask Permission Rule

| Situation | Action |
|-----------|--------|
| Target branch is main/master | `⛔` double confirmation — propose new branch |
| Remote is ahead (local behind) | Warn + offer pull first |
| Remote diverged | Warn + show diff summary + offer pull/rebase or abort |
| upload_repo ≠ load_repo | ℹ️ info warning (non-blocking) |
| Token stored in plain text | Warn once before saving |
| Push would overwrite remote changes | Hard warning + explicit confirm |

# AVAILABLE TOOLS

- **Read** — read CHANGELOG.md, SKILL.md for commit message generation; read config files
- **Write** — create or update shared config after init
- **Edit** — update shared config entries
- **Glob** — discover local skill directories for standalone selection
- **Grep** — extract latest CHANGELOG entry for commit message
- **Bash** — execute git commands (fetch, checkout, add, commit, push) after user confirmation

# EXPECTED FORMAT (I/O)

**Input:**
- `mode` (string, optional): `init` | `check` | `push` | `standalone` — defaults to `standalone`
- `repo_url` (string, optional): explicit upload target — overrides shared config
- `skill_name` (string, optional): specific skill to upload — if omitted, selection runs
- `caller` (string, optional): `skill-architect` | `standalone` — governs selection behavior

**Output:**
- Console: branch confirmation, sync state, commit message preview, push result
- Disk: no local skill files modified — only remote repo and shared config updated
- Remote: skill files pushed to confirmed branch on confirmed repo

## Start

1. Read `~/.claude/skill-git.config.json` (and project override if present).
2. Check `git_enabled` — exit gracefully if false.
3. Route to the correct procedure based on `mode`, `caller`, and config state.
