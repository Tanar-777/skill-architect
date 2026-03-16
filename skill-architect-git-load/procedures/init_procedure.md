# Init Procedure — skill-architect-git-load

Runs on first use (no config found) or when `mode: init` is explicitly passed.
Captures user preferences and writes config to disk.

---

## Step 1 — Determine config scope

Ask:
```
Where should these settings be saved?
  [global]   ~/.claude/skill-git.config.json       — applies to all projects
  [project]  [project-dir]/.claude/skill-git.config.json  — this project only
```

Store the chosen path as `CONFIG_PATH`.

If a config already exists at `CONFIG_PATH`, display its current values and ask:
```
Existing config found. Reconfigure it? [yes / no]
```
- `no` → exit init, return to caller.
- `yes` → continue with current values as defaults for each prompt below.

---

## Step 2 — Repo usage intent

Ask:
```
Do you intend to work with a remote skill repository? [yes / no]
```

- `no` → set `use_repo: false`. Skip to Step 5.
- `yes` → set `use_repo: true`. Continue.

---

## Step 3 — Default repo

Ask:
```
Do you want to set a default repository now? [yes / no / later]
```

- `no` / `later` → set `default_repo: null`. Continue.
- `yes` → ask:
  ```
  Enter the repository URL or local path:
  ```
  - Store as `PENDING_REPO`.
  - Load `procedures/resolve_repo_procedure.md` to validate the URL format.
  - Load `procedures/trust_gate_procedure.md` to verify access (do NOT download — check only).
  - If access confirmed → set `default_repo: PENDING_REPO`.
  - If access fails → warn, ask to retry or set `default_repo: null`.

---

## Step 4 — Update check behavior

Ask:
```
How should update checks behave when proofing or updating a skill?

  [manual]     Only when you explicitly run /skill-architect-git-load
  [on-proof]   Ask before each proofing/update run ("check for updates? [y/n]")
  [automatic]  Always check silently — only prompt if an update is found
```

Set `update_check_mode` to the chosen value.

---

## Step 5 — Review and confirm

Display the full config to be saved:
```
Config to save at [CONFIG_PATH]:
{
  "use_repo": ...,
  "update_check_mode": "...",
  "default_repo": "..." or null,
  "trusted_sources": []
}

Save this config? [yes / edit / cancel]
```

- `cancel` → exit without writing.
- `edit` → return to Step 2.
- `yes` → write config to `CONFIG_PATH` using Write tool.
  - If directory doesn't exist, create it first via Bash.

---

## Step 6 — Hand off

After saving:
- If called as `mode: init` (explicit reconfigure) → display: "Configuration saved. Run /skill-architect-git-load to use it."
- If called because no config existed (first run) → return to the routing table in SKILL.md and continue with the originally requested mode.
