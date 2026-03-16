# Infer Procedure — skill-architect-makeinto

Shared procedure for extracting skill metadata from a source file. Used by both single_procedure.md and multi_procedure.md.

## Input

- `file_path` — absolute path to the source file to analyze
- `skill_name` (optional) — user-provided override

## Step 1 — Read the file

Use Read to load the full file content.

## Step 2 — Run inference script

Run: `python ~/.claude/skills/skill-architect-makeinto/scripts/infer_skill.py [file_path]`

The script outputs JSON:
```json
{
  "suggested_name": "...",
  "description": "...",
  "language": "python|js|ts|...",
  "functions": [
    {"name": "...", "params": [...], "returns": "...", "docstring": "..."}
  ],
  "classes": [
    {"name": "...", "methods": [...], "docstring": "..."}
  ],
  "imports": [...],
  "side_effects": "..."
}
```

## Step 3 — Derive skill metadata

From the script output, construct:

| Field | Source |
|---|---|
| `name` | `suggested_name` (or user override via `skill_name`) |
| `description` | `description` from script (max 1024 chars) |
| `inputs` | Union of all function params across top-level functions |
| `outputs` | Union of all return types |
| `side_effects` | `side_effects` field |
| `language` | `language` field |

## Step 4 — Validate name

- Apply slug rules: lowercase, hyphens only, max 64 chars
- Check `~/.claude/skills/[name]/` — if exists, warn user and ask: overwrite or rename?

## Step 5 — Return metadata

Return the structured metadata object to the calling procedure (single or multi).
