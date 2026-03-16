# Trust Gate Procedure — skill-architect-git-load

**This is a hard gate. No download command may execute until it passes.**

Runs after repo resolution, before any `git`, `gh`, or `curl` call.
Applies to ALL repositories — public repos are NOT auto-trusted.

---

## Step 1 — Check trusted_sources cache

Read `trusted_sources` array from the active config.

If `RESOLVED_REPO` is already listed:
```
Repository [RESOLVED_REPO] is in your trusted sources.
Proceed? [yes / remove-trust / cancel]
```
- `yes` → gate passes. Return to caller.
- `remove-trust` → remove from `trusted_sources`, continue to Step 2.
- `cancel` → exit.

---

## Step 2 — Determine visibility

Attempt to detect repository visibility:

- If local path → label `LOCAL`
- If URL contains known forge patterns:
  - Try a lightweight HEAD request (no auth) via Bash `curl -sI [url]`
  - HTTP 200 / 301 → `PUBLIC`
  - HTTP 401 / 403 → `PRIVATE (authentication required)`
  - HTTP 404 or network error → `UNKNOWN / NOT FOUND`

---

## Step 3 — Display trust gate prompt

```
⚠️  TRUST GATE — Confirm source before download

  Repository : [RESOLVED_REPO]
  Visibility : [PUBLIC / PRIVATE / LOCAL / UNKNOWN]
  Source     : [source_label from resolve_repo_procedure]

  No files will be downloaded until you confirm you know and trust this source.
  Public repositories are not automatically safe.

Do you know this source and want to proceed? [yes / no]
```

- `no` → exit. Display: "Download cancelled. No files were accessed."
- `yes` → continue to Step 4.

---

## Step 4 — Access test

Test that the repository is reachable using the least-invasive method available:

| Method | Command | Use when |
|--------|---------|----------|
| `git ls-remote` | `git ls-remote --exit-code [url] HEAD` | git installed |
| `gh repo view` | `gh repo view [owner/repo]` | gh CLI installed, GitHub URL |
| `curl HEAD` | `curl -sI --max-time 5 [url]` | HTTP URL, fallback |
| Local path stat | `ls [path]` | Local filesystem path |

If access succeeds → continue to Step 5.

If access fails:
```
⚠️  Could not reach repository: [RESOLVED_REPO]
    Error: [error message]

    Possible causes:
    - Repository does not exist or was moved
    - Authentication required (private repo — check credentials)
    - Network unavailable

[retry / change-repo / cancel]
```
- `retry` → re-run access test.
- `change-repo` → return to `resolve_repo_procedure.md` Level 5.
- `cancel` → exit.

---

## Step 5 — Add to trusted sources (optional)

```
Add [RESOLVED_REPO] to your trusted sources so you are not asked again?
  [yes-global]    Save in ~/.claude/git-load.config.json
  [yes-project]   Save in [project-dir]/.claude/git-load.config.json
  [no]            Trust for this session only
```

Write to config using Edit tool if user selects `yes-global` or `yes-project`.

---

## Gate result

Trust gate passed. Return `RESOLVED_REPO` and `visibility` to caller.
Caller may now execute download commands.
