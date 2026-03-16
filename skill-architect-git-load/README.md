# skill-architect-git-load

> Load or update a Claude Code skill from a remote Git repository.

## Description

`skill-architect-git-load` safely fetches and installs Claude Code skills from a Git repository (GitHub, GitLab, Bitbucket, self-hosted, or local path) into `~/.claude/skills/`.

It enforces a hard trust gate before any download executes, handles all conflict scenarios with explicit user confirmation, and integrates with the `skill-architect` ecosystem as a sub-skill.

## Usage

```
/skill-architect-git-load
/skill-architect-git-load mode:init
/skill-architect-git-load repo_url:https://github.com/user/repo
/skill-architect-git-load skill_name:my-skill
```

No required arguments. On first run, initialization captures your preferences.

## Modes

| Mode | Description |
|------|-------------|
| `standalone` (default) | Full flow using current config settings |
| `init` | Run or re-run initialization to configure preferences |
| `check` | Compare local vs remote versions — no download, no write |
| `pull` | Download and install selected skills |

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | string | `init` \| `check` \| `pull` \| `standalone` |
| `repo_url` | string | Explicit URL or local path — overrides all saved config |
| `skill_name` | string | Target skill in repo — if omitted, discovery + selection runs |
| `caller` | string | `proofing` \| `update` \| `standalone` — governs update-check behavior |

## Initialization

On first use, the init procedure asks:

1. **Repo usage** — do you intend to work with a remote skill repository?
2. **Default repo** — set now, later, or not at all
3. **Update check mode** — how should proofing/update triggers behave?

Config is saved as plain-text JSON (no encryption):
- Global: `~/.claude/git-load.config.json`
- Project override: `[project-dir]/.claude/git-load.config.json`

## Update Check Modes

| Mode | Behavior when triggered from proofing or update |
|------|------------------------------------------------|
| `manual` | Skips silently — only runs when invoked directly |
| `on-proof` | Asks "Check for updates?" before each proofing/update run |
| `automatic` | Checks silently — prompts only if an update is found |

## Trust Gate

**No download command executes until the user explicitly confirms they know and trust the source.**

- Applies to ALL repositories — public repos are not auto-trusted
- Trust can be saved to config to avoid re-prompting
- Access is tested before any data is transferred

## Repo Structure Support

| Structure | Description |
|-----------|-------------|
| Root-is-skill | `SKILL.md` at repo root — single skill |
| Flat monorepo | `[name]/SKILL.md` — skills in subdirectories |
| Skills folder | `skills/[name]/SKILL.md` — skills under `/skills/` |
| Unstructured | Auto-scans for all `SKILL.md` files |

## Download Method Priority

1. `git sparse-checkout` — minimal transfer (preferred for monorepos)
2. `git clone --depth=1` — full clone
3. `gh repo clone` — GitHub CLI fallback
4. HTTP zip — last resort (GitHub and GitLab only)

## Integration

Called automatically by:
- `skill-architect` — when an existing skill is detected during Step 1
- `skill-architect-proofing` — per `update_check_mode` config *(future minor update)*
- `skill-architect-update` — per `update_check_mode` config *(future minor update)*

## Related Skills

- [`skill-architect`](../skill-architect/) — orchestrator, triggers git-load on existing skill detection
- [`skill-architect-proofing`](../skill-architect-proofing/) — quality gate
- [`skill-architect-update`](../skill-architect-update/) — guided update workflow
