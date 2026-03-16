# Sync Check Procedure — skill-architect-git-upload

Verifies the sync state between local skill and the remote branch before pushing.
Runs after branch confirmation, before staging files.

---

## Step 1 — Fetch remote branch state

```bash
git fetch origin [TARGET_BRANCH] 2>/dev/null || echo "branch-not-found"
```

If the branch does not exist on remote yet → state is `NEW_BRANCH`. Skip to Step 4.

---

## Step 2 — Compare local skill vs remote

Copy local skill files into the repo working directory (temp), then compare:

```bash
# Check how many commits local is ahead/behind remote
git rev-list --count HEAD..origin/[TARGET_BRANCH]   # behind count
git rev-list --count origin/[TARGET_BRANCH]..HEAD   # ahead count
```

Also compare the skill directory contents directly:
```bash
diff -rq ~/.claude/skills/[skill_name]/ [temp_dir]/[skill_path]/ --exclude=".git"
```

Determine state:

| State | Condition |
|-------|-----------|
| `UP_TO_DATE` | No diff, same commits |
| `LOCAL_AHEAD` | Local has changes remote doesn't — normal upload path |
| `REMOTE_AHEAD` | Remote has changes local doesn't — warn |
| `DIVERGED` | Both have changes the other doesn't — warn |
| `NEW_BRANCH` | Branch doesn't exist on remote yet |

---

## Step 3 — Handle non-clean states

### REMOTE_AHEAD
```
⚠️  Remote branch '[TARGET_BRANCH]' is ahead of your local skill.
    The remote has [N] change(s) you don't have locally.

    Pushing now would overwrite those remote changes.

    Options:
    [pull-first]    Pull remote changes, review, then re-upload
    [force-push]    Push anyway and overwrite remote (⚠️ destructive)
    [abort]         Cancel upload
```

- `pull-first` → run `git pull origin [TARGET_BRANCH]` in temp dir → display diff → return to caller to re-evaluate.
- `force-push` → set `FORCE_PUSH=true`, continue (force flag applied at push step).
- `abort` → exit.

### DIVERGED
```
⚠️  Local and remote have diverged on branch '[TARGET_BRANCH]'.

    Local changes  : [N] file(s) changed
    Remote changes : [M] file(s) changed

    Conflicting files:
    [list of differing files]

    Options:
    [pull-and-merge]   Pull remote, resolve conflicts manually, then re-upload
    [force-push]       Overwrite remote with local (⚠️ destructive — remote changes lost)
    [abort]            Cancel upload
```

- `pull-and-merge` → exit with instructions: pull, resolve, re-run `/skill-architect-git-upload`.
- `force-push` → require explicit second confirmation:
  ```
  ⛔  Force push will permanently overwrite [M] remote change(s).
      Type "force push" to confirm, or [cancel]:
  ```
  Only proceed on exact input `force push`.
- `abort` → exit.

### UP_TO_DATE
```
ℹ️  Local skill '[skill_name]' is already in sync with remote '[TARGET_BRANCH]'.
    Nothing to push.

    Push anyway to re-publish? [yes / no]
```

---

## Step 4 — Return sync result

Return to caller:
- `SYNC_STATE` — one of: `LOCAL_AHEAD`, `NEW_BRANCH`, `UP_TO_DATE`, `FORCE_PUSH`
- `FORCE_PUSH` flag (boolean)
- Caller proceeds to `upload_procedure.md`.
