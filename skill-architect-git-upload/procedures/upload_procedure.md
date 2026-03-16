# Upload Procedure — skill-architect-git-upload

Stages skill files, generates commit message, commits, and pushes to remote.
Runs after sync check passes. Operates inside the cloned temp repo directory.

---

## Step 1 — Determine repo structure for this skill

Check how the skill should be placed in the repo:

| Repo structure | Placement |
|---------------|-----------|
| Root-is-skill | Copy files directly to repo root |
| Flat monorepo (`[name]/`) | Copy to `[temp_dir]/[skill_name]/` |
| Skills folder (`skills/[name]/`) | Copy to `[temp_dir]/skills/[skill_name]/` |
| Unknown | Ask: "Where in the repo should '[skill_name]' live? (relative path):" |

If the skill already exists in the repo at a known path (from previous load/upload), use that path.

---

## Step 2 — Copy skill files to repo

Copy all files from `~/.claude/skills/[skill_name]/` to the resolved destination path in `[temp_dir]`:

```bash
cp -r ~/.claude/skills/[skill_name]/. [temp_dir]/[skill_destination]/
```

Exclude:
- `.git/` — never copy git metadata
- Any file matching `.env`, `*.key`, `*.pem` — warn and skip:
  ```
  ⚠️  Skipping '[filename]' — potential credentials file. Upload anyway? [yes / skip]
  ```

---

## Step 3 — Generate commit message

Read `~/.claude/skills/[skill_name]/CHANGELOG.md` using Read tool.
Extract the latest entry (first `## [version]` block).

Read `~/.claude/skills/[skill_name]/SKILL.md` frontmatter for `version`.

Auto-generate commit message:
```
chore: update [skill_name] to v[version]

[First CHANGELOG entry content — trimmed to first 10 lines if long]
```

If `commit_message_mode: auto-with-edit` (recommended):
```
Commit message:

  chore: update [skill_name] to v[version]

  ## [version] — YYYY-MM-DD
  ### Changed
  - ...

Edit this message? [yes / use-as-is]
```

- `use-as-is` → proceed.
- `yes` → display full message text, ask user to provide replacement. Accept the new message.

Store as `COMMIT_MSG`.

---

## Step 4 — Final upload confirmation

Display full summary before executing any git command:

```
Upload plan:
  Skill  : [skill_name]  v[version]
  Repo   : [UPLOAD_REPO]
  Branch : [TARGET_BRANCH]  ([new] / [existing])
  Files  : [N] files staged
  Force  : [yes / no]

Commit message:
  "[COMMIT_MSG first line]"

Execute upload? [yes / edit-message / cancel]
```

- `edit-message` → return to Step 3 message edit.
- `cancel` → exit, clean up temp dir.
- `yes` → proceed to Step 5.

---

## Step 5 — Execute git commands

Run in sequence inside `[temp_dir]`:

```bash
# Stage skill files
git add [skill_destination]/

# Commit
git commit -m "[COMMIT_MSG]"

# Push (with or without force)
git push origin [TARGET_BRANCH]
# or if FORCE_PUSH:
git push origin [TARGET_BRANCH] --force-with-lease
```

Note: `--force-with-lease` is used instead of `--force` — safer, fails if someone pushed to the branch between our fetch and push.

Capture output and exit codes at each step. If any step fails:
```
⚠️  Git command failed:
    Command : [command]
    Error   : [error output]

    Options:
    [retry]     Try the command again
    [abort]     Cancel upload and clean up
```

---

## Step 6 — Cleanup

Delete temp directory:
```bash
rm -rf [temp_dir]
```

---

## Step 7 — Upload report

```
Upload complete:

  ✅ [skill_name]  v[version]
     Repo   : [UPLOAD_REPO]
     Branch : [TARGET_BRANCH]
     Commit : [short commit hash] — "[COMMIT_MSG first line]"

  Remote URL : [UPLOAD_REPO]/tree/[TARGET_BRANCH]
```

If multiple skills were uploaded, show one line per skill.

Update `skill_repos[skill_name]` in shared config to record the upload:
```json
"[skill_name]": {
  "load_repo": "...",
  "upload_repo": "[UPLOAD_REPO]",
  "last_uploaded": "YYYY-MM-DD",
  "last_uploaded_branch": "[TARGET_BRANCH]"
}
```
