# Resolve Repo Procedure — skill-architect-git-load

Determines the target repository through a 5-level priority chain.
Always ends with an explicit user confirmation before proceeding.

---

## Resolution Chain

Check each level in order. Stop at the first match.

### Level 1 — Explicit argument
- `repo_url` was passed directly to the skill.
- Source label: `"provided as argument"`
- → Skip to Confirmation.

### Level 2 — Skill-specific memory
- Read `~/.claude/skills/skill-architect-git-load/config.json` if present.
- Check for a `skill_repos` map: `{ "[skill_name]": "url" }`.
- If a match for the target skill exists:
  - Source label: `"saved for skill '[skill_name]'"`
  - → Skip to Confirmation.

### Level 3 — Project-scoped config
- Read `[project-dir]/.claude/skill-git.config.json`.
- Check `default_repo` field.
- If set:
  - Source label: `"project config"`
  - → Skip to Confirmation.

### Level 4 — Global config
- Read `~/.claude/skill-git.config.json`.
- Check `default_repo` field.
- If set:
  - Source label: `"global config"`
  - → Skip to Confirmation.

### Level 5 — No config found
- Ask:
  ```
  No repository configured. Enter the repository URL or local path:
  ```
- Accept:
  - Full HTTPS URL: `https://github.com/user/repo`
  - SSH URL (format: `git@[host]:[user]/[repo].git`)
  - Local path: `/path/to/local/repo` or `C:\path\to\repo`
- Validate format (basic pattern check, not access test — that's the trust gate).
- Source label: `"entered manually"`

---

## Confirmation

Display to the user:
```
Repository identified:
  URL/Path : [resolved_url]
  Source   : [source_label]

Is this the correct repository? [yes / change / cancel]
```

- `cancel` → exit.
- `change` → discard resolved value, jump to Level 5 (manual entry).
- `yes` → store as `RESOLVED_REPO` and return to caller.

---

## Post-resolution: Save offer

If the repo was entered manually (Level 5) or changed:
```
Save this repository for future use?
  [skill]    Save for skill '[skill_name]' only
  [project]  Save as project default
  [global]   Save as global default
  [no]       Use for this session only
```

- `skill` → write to `~/.claude/skills/skill-architect-git-load/config.json` under `skill_repos.[skill_name]`.
- `project` → write `default_repo` to `[project-dir]/.claude/skill-git.config.json`.
- `global` → write `default_repo` to `~/.claude/skill-git.config.json`.
- `no` → do not persist.

If saving a token alongside the URL, display:
```
⚠️  Warning: This value will be stored in plain text. Consider using SSH keys
    or your system keychain for credentials instead.
    Store anyway? [yes / no]
```
