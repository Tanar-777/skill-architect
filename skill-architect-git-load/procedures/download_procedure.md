# Download Procedure — skill-architect-git-load

Fetches the repository content to a temporary location.
Runs after the trust gate passes. Uses a tool priority chain with automatic fallback.

---

## Temp directory

Use a system temp path: `[temp]/skill-git-load-[timestamp]/`

Create it via Bash before any download attempt.

---

## Tool priority chain

Attempt methods in this order. Move to the next if the current method is unavailable or fails.

### Method 1 — git sparse-checkout (preferred for monorepos)

**Use when:** `git` is installed AND only specific skill subdirectories are needed.

```bash
git init [temp_dir]
cd [temp_dir]
git remote add origin [RESOLVED_REPO]
git sparse-checkout init --cone
git sparse-checkout set [skill_subpath_1] [skill_subpath_2] ...
git pull origin HEAD --depth=1
```

Advantages: minimal data transfer, no full repo clone.

### Method 2 — git clone (full)

**Use when:** `git` is installed AND sparse-checkout failed or repo is `root-is-skill`.

```bash
git clone --depth=1 [RESOLVED_REPO] [temp_dir]
```

### Method 3 — gh CLI

**Use when:** `gh` is installed AND it's a GitHub URL AND Methods 1–2 failed.

```bash
gh repo clone [owner/repo] [temp_dir] -- --depth=1
```

### Method 4 — HTTP zip download (last resort)

**Use when:** No `git` or `gh` available, or all above failed. Requires HTTPS URL.

For GitHub:
```bash
curl -L -o [temp_dir]/repo.zip "https://github.com/[owner]/[repo]/archive/refs/heads/[branch].zip"
unzip [temp_dir]/repo.zip -d [temp_dir]/unzipped/
```

For GitLab:
```bash
curl -L -o [temp_dir]/repo.zip "[gitlab_url]/-/archive/[branch]/[repo]-[branch].zip"
```

**Note:** HTTP zip is not available for all forge types. If the URL is not GitHub or GitLab, display:
```
⚠️  HTTP zip download is not supported for this repository type.
    Please install git to continue.
```
And exit.

---

## Failure handling

If all methods fail:
```
⚠️  Could not download repository: [RESOLVED_REPO]

  Methods attempted:
  - git sparse-checkout : [result]
  - git clone           : [result]
  - gh CLI              : [result]
  - HTTP zip            : [result]

  Suggestions:
  - Verify the repository URL is correct
  - Check network connectivity
  - Ensure credentials are valid for private repos
  - Install git: https://git-scm.com/

[retry / change-repo / cancel]
```

---

## Auth errors (private repos)

If any method returns HTTP 401 / 403 / `authentication failed`:
```
⚠️  Authentication failed for [RESOLVED_REPO]

  For HTTPS: ensure your token has repo read access.
  For SSH:   ensure your SSH key is added to the forge account.
  For gh:    run `gh auth login` first.

[retry-with-credentials / cancel]
```
- `retry-with-credentials` → ask for token (warn about plain-text storage) → retry Method 1 or 2 with token injected in URL or env var.

---

## Success

Return `TEMP_DIR` (path to downloaded repo content) to caller (`install_procedure.md`).

Clean up `TEMP_DIR` after install completes or is cancelled (caller responsibility).
