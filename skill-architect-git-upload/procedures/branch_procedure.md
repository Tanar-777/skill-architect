# Branch Procedure — skill-architect-git-upload

Verifies the target branch before any push. Enforces double-confirmation for main/master.
Runs after repo resolution, before sync check.

---

## Step 1 — Clone / enter repo context

Determine how to access the repo for git operations:

- If the skill was loaded via git-load and a local clone exists in temp → reuse it.
- Otherwise: clone the repo to a temp directory (shallow, `--depth=1`) for branch operations only.

```bash
git clone --depth=1 [UPLOAD_REPO] [temp_dir]
cd [temp_dir]
```

---

## Step 2 — Fetch current remote state

```bash
git fetch origin
git branch -r
```

List all remote branches. Identify the current default branch (usually `main` or `master`).

---

## Step 3 — Determine target branch

Apply `default_branch_mode` from config:

| Mode | Action |
|------|--------|
| `new-branch` | Propose `skill/[skill-name]-v[version]` — go to Step 4 |
| `ask` | Ask user which branch to target — go to Step 4 |
| `allow-any` | Ask user which branch to target — go to Step 4 |

In all cases: present the list of existing remote branches for reference.

Proposed branch display:
```
Target branch for upload:

  Remote branches available:
    - main  ← default
    - skill/some-other-skill-v1.0.0

  Proposed (new): skill/[skill-name]-v[version]

  Options:
    [use-proposed]   Create and push to skill/[skill-name]-v[version]
    [existing]       Choose an existing branch
    [custom]         Enter a custom branch name
```

---

## Step 4 — Main/master hard warning

If the selected or entered branch is `main` or `master`:

```
⛔  WARNING — You are about to push directly to '[main/master]'.

    This is the default branch of the repository. Pushing directly to it
    may affect other users of this repo and cannot be easily undone.

    Are you absolutely sure? [yes-I-know-what-I-am-doing / no-use-new-branch]
```

- `no-use-new-branch` → revert to proposing `skill/[skill-name]-v[version]`, return to Step 3.
- `yes-I-know-what-I-am-doing` → show a second confirmation:

```
⛔  SECOND CONFIRMATION — Push to [main/master]?

    Repo   : [UPLOAD_REPO]
    Branch : main/master
    Skill  : [skill-name] v[version]

    Type "push to main" to confirm, or press [cancel]:
```

Only proceed if the user types `push to main` exactly.

---

## Step 5 — Create branch if new

If the branch does not exist on remote:
```bash
git checkout -b [branch_name]
```

If the branch already exists on remote:
```bash
git checkout [branch_name]
git pull origin [branch_name]
```

---

## Step 6 — Final branch confirmation

```
Branch confirmed:
  Repo   : [UPLOAD_REPO]
  Branch : [branch_name]  ([new] / [existing])

Proceed? [yes / change-branch / cancel]
```

- `change-branch` → return to Step 3.
- `yes` → store `TARGET_BRANCH`, return to caller.
