# skill-architect-git-upload

> Upload a local Claude Code skill to a remote Git repository.

## Description

`skill-architect-git-upload` safely pushes one or more local skills from `~/.claude/skills/` to a remote Git repository. It shares configuration with `skill-architect-git-load` via `~/.claude/skill-git.config.json` — what git-load pulls, git-upload pushes, using the same repo as the first source of truth.

## Usage

```
/skill-architect-git-upload
/skill-architect-git-upload mode:init
/skill-architect-git-upload skill_name:my-skill
/skill-architect-git-upload skill_name:my-skill repo_url:https://github.com/user/repo
```

No required arguments. On first run, initialization captures your preferences.

## Modes

| Mode | Description |
|------|-------------|
| `standalone` (default) | Full flow using current config settings |
| `init` | Run or re-run initialization to configure preferences |
| `check` | Verify sync state between local and remote — no push |
| `push` | Run the full upload flow |

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | string | `init` \| `check` \| `push` \| `standalone` |
| `repo_url` | string | Explicit upload URL — overrides all saved config |
| `skill_name` | string | Target skill — if omitted, selection checklist runs |
| `caller` | string | `skill-architect` \| `standalone` — governs selection behavior |

## Shared Config

Both `skill-architect-git-load` and `skill-architect-git-upload` share:

```
~/.claude/skill-git.config.json     ← global
[project]/.claude/skill-git.config.json  ← project override
```

Config shape:
```json
{
  "git_enabled": true,
  "update_check_mode": "on-proof",
  "default_repo": null,
  "default_branch_mode": "new-branch",
  "commit_message_mode": "auto-with-edit",
  "trusted_sources": [],
  "skill_repos": {
    "skill-name": {
      "load_repo": "url",
      "upload_repo": null,
      "last_uploaded": "YYYY-MM-DD",
      "last_uploaded_branch": "branch-name"
    }
  }
}
```

`upload_repo: null` = same as `load_repo`. A small info note appears if they differ.

## Upload Repo Resolution Order

1. Explicit `repo_url` argument
2. `skill_repos[skill_name].upload_repo` in shared config
3. `skill_repos[skill_name].load_repo` in shared config (symmetry fallback)
4. `default_repo` in shared config
5. Prompt

## Branch Safety

- Fetches remote branch state before any push
- Proposes `skill/[skill-name]-v[version]` as default new branch
- **Pushing to `main` or `master`** requires double confirmation — the second requires typing `push to main` exactly
- `--force-with-lease` used instead of `--force` for all force pushes

## Sync Check

Before staging files:
- `LOCAL_AHEAD` → normal push path
- `NEW_BRANCH` → normal push path
- `REMOTE_AHEAD` → warn, offer pull-first or force-push
- `DIVERGED` → warn with file list, force-push requires typed confirmation
- `UP_TO_DATE` → warn, ask to push anyway

## Commit Flow

1. Read `CHANGELOG.md` latest entry + `SKILL.md` version
2. Auto-generate: `chore: update [skill-name] to v[version]\n\n[CHANGELOG entry]`
3. Show for review (if `commit_message_mode: auto-with-edit`)
4. `git add` → `git commit` → `git push origin [branch]`

## Skill Selection

| Context | Behavior |
|---------|----------|
| Standalone | Checklist of all local skills — select one / multiple / all |
| Called by `skill-architect` | Only the designed skill — no selection prompt |

## Related Skills

- [`skill-architect-git-load`](../skill-architect-git-load/) — symmetric load sub-skill, shares config
- [`skill-architect`](../skill-architect/) — orchestrator, triggers git-upload after skill generation
- [`skill-architect-proofing`](../skill-architect-proofing/) — quality gate
- [`skill-architect-update`](../skill-architect-update/) — guided update workflow
