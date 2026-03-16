# Init Procedure — skill-architect-git-upload

Runs on first use (no config found) or when `mode: init` is explicitly passed.
Reads and merges with any existing shared config. Writes to `~/.claude/skill-git.config.json`.

---

## Step 1 — Determine config scope

Ask:
```
Where should these settings be saved?
  [global]   ~/.claude/skill-git.config.json              — applies to all projects
  [project]  [project-dir]/.claude/skill-git.config.json  — this project only
```

Store chosen path as `CONFIG_PATH`.

If config already exists at `CONFIG_PATH`, display current values and ask:
```
Existing config found at [CONFIG_PATH]. Reconfigure it? [yes / no]
```
- `no` → exit init, return to caller.
- `yes` → continue, using current values as defaults.

---

## Step 2 — Git enabled gate

Ask:
```
Do you want to use Git features (git-load and git-upload)? [yes / no]
```

- `no` → set `git_enabled: false`. Skip to Step 7.
- `yes` → set `git_enabled: true`. Continue.

**Note:** Setting `git_enabled: false` disables both git-load and git-upload globally for the selected scope. They will return silently when triggered by proofing or update.

---

## Step 3 — Default repository

Ask:
```
Do you want to set a default repository for uploads? [yes / no / later]
```

- `no` / `later` → set `default_repo: null`. Continue.
- `yes` → ask:
  ```
  Enter the repository URL:
  ```
  - Validate URL format (not access — that happens at push time).
  - Set `default_repo: [url]`.
  - Ask:
    ```
    Use the same repository for both loading and uploading? [yes / no]
    ```
    - `yes` → `default_repo` applies to both.
    - `no` → note that per-skill overrides can be set at upload time.

---

## Step 4 — Branch default behavior

Ask:
```
When uploading a skill, what should the default branch behavior be?

  [new-branch]    Always propose a new branch (skill/[name]-v[version])
  [ask]           Ask each time — no default
  [allow-any]     Allow pushing to any branch (main/master still requires double confirm)
```

Set `default_branch_mode` to chosen value.

---

## Step 5 — Commit message style

Ask:
```
How should commit messages be generated?

  [auto]           Auto-generate from CHANGELOG + version, commit immediately
  [auto-with-edit] Auto-generate, show for review, allow edit before committing
```

Set `commit_message_mode` to chosen value. Recommended: `auto-with-edit`.

---

## Step 6 — Update check mode (shared with git-load)

If `update_check_mode` is not yet set in config, ask:
```
How should update checks behave when proofing or updating a skill?

  [manual]     Only when you explicitly run /skill-architect-git-load or /skill-architect-git-upload
  [on-proof]   Ask before each proofing/update run
  [automatic]  Check silently — only prompt if update found
```

Set `update_check_mode` to chosen value.

---

## Step 7 — Review and confirm

Display full config to be saved:
```
Config to save at [CONFIG_PATH]:
{
  "git_enabled": ...,
  "update_check_mode": "...",
  "default_repo": "..." or null,
  "default_branch_mode": "...",
  "commit_message_mode": "...",
  "trusted_sources": [],
  "skill_repos": {}
}

Save this config? [yes / edit / cancel]
```

- `cancel` → exit without writing.
- `edit` → return to Step 2.
- `yes` → write config using Write/Edit tool. Merge with existing values — never overwrite `skill_repos` or `trusted_sources` that already exist.

---

## Step 8 — Hand off

- If called as `mode: init` → display: "Configuration saved."
- If called because no config existed → return to routing table and continue with originally requested mode.
