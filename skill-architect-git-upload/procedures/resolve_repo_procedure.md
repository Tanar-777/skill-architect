# Resolve Upload Repo Procedure — skill-architect-git-upload

Determines the upload repository for a given skill through a 5-level priority chain.
Reads shared config first — symmetry with git-load is the design goal.

---

## Resolution Chain

Check each level in order. Stop at the first match.

### Level 1 — Explicit argument
- `repo_url` was passed directly to the skill.
- Source label: `"provided as argument"`
- → Skip to Conflict Check.

### Level 2 — Per-skill upload override
- Read `skill_repos[skill_name].upload_repo` from active config.
- If set (not null):
  - Source label: `"saved upload repo for '[skill_name]'"`
  - → Skip to Conflict Check.

### Level 3 — Per-skill load repo (symmetry fallback)
- Read `skill_repos[skill_name].load_repo` from active config.
- If set:
  - Source label: `"load repo for '[skill_name]' (upload override not set)"`
  - → Skip to Conflict Check.

### Level 4 — Global default repo
- Read `default_repo` from active config.
- If set:
  - Source label: `"global default repo"`
  - → Skip to Conflict Check.

### Level 5 — No config found
- Ask:
  ```
  No upload repository configured for '[skill_name]'. Enter the repository URL:
  ```
- Validate format.
- Source label: `"entered manually"`

---

## Conflict Check (load ≠ upload warning)

Resolve both `load_repo` and `upload_repo` for the skill. If they differ:
```
ℹ️  Note: upload repo differs from load repo for '[skill_name]'.
    Load  : [load_repo]
    Upload: [upload_repo]

This is allowed — just making sure it's intentional.
```
Non-blocking. Continue to Confirmation.

---

## Confirmation

```
Upload repository:
  Skill  : [skill_name]
  Repo   : [resolved_url]
  Source : [source_label]

Proceed with this repository? [yes / change / cancel]
```

- `cancel` → exit.
- `change` → discard, jump to Level 5.
- `yes` → store as `UPLOAD_REPO`, return to caller.

---

## Post-resolution: Save offer

If repo was entered manually or changed:
```
Save this upload repository for '[skill_name]'?
  [skill]    Save as upload_repo for this skill only
  [global]   Save as global default_repo
  [no]       Use for this session only
```

- `skill` → write `skill_repos[skill_name].upload_repo` to config using Edit.
- `global` → write `default_repo` to config using Edit.
- `no` → do not persist.

If saving a token, warn about plain-text storage before writing.
