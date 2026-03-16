# Scope Procedure — skill-architect-makeinto

Determines whether the input should be processed as Mode A (single skill) or Mode B (multi skill tree).

## Step 1 — Resolve input path

- Confirm `input_path` resolves to an existing file or directory.
- If file: set `input_type = file`, skip to Step 3.
- If directory: set `input_type = directory`, continue to Step 2.

## Step 2 — Scan directory (directory input only)

Run: `python ~/.claude/skills/skill-architect-makeinto/scripts/scan_repo.py [input_path]`

Collect:
- `file_count` — number of relevant source files found
- `file_list` — list of file paths with language tags

## Step 3 — Count logical units

For each source file, use Grep to count top-level function/class definitions:
- Python: `^def ` and `^class `
- JS/TS: `^function `, `^const .* = (async )?(\(|function)`, `^class `
- Other: adapt pattern to language

Sum all top-level units across files → `unit_count`

## Step 4 — Decide mode

| Condition | Mode |
|---|---|
| `file_count == 1` AND `unit_count <= 2` | **A — Single** |
| `file_count == 1` AND `unit_count >= 3` | **B — Multi** |
| `file_count >= 2` | **B — Multi** |

Present decision to user:
```
Scope detected: [Single / Multi]
Files: [N]  |  Logical units: [N]
Mode: [A — generating 1 skill / B — generating skill tree]
```

Ask: "Proceed with this mode, or override? [auto / single / multi]"

## Step 4.5 — Too-Big Check (Multi mode only)

Skip this step entirely if mode is A (Single).

Evaluate thresholds:

| Metric | Threshold |
|---|---|
| `file_count` | > 5 |
| `unit_count` | > 10 |

If **any threshold is exceeded**:

1. Check that `~/.claude/skills/skill-architect-multy-plan/SKILL.md` and `~/.claude/skills/skill-architect-multy-exec/SKILL.md` both exist.
2. If both exist, present:
   ```
   ⚠️  Large scope detected: [N files] / [N units]
   This exceeds the inline multi threshold.

     (inline)  Continue here — interactive, step-by-step generation
     (multy)   Delegate to skill-architect-multy — plan-first batch generation

   Which approach? [inline / multy]
   ```
3. `multy` chosen → invoke `skill-architect-multy-plan` with the `input_path` and a project idea string summarized from the source analysis. After the plan is produced, invoke `skill-architect-multy-exec` with the generated plan file path.
4. `inline` chosen → continue to Step 5 (hand off to `multi_procedure.md`) normally.
5. If either multy sub-skill is missing → warn: "skill-architect-multy-plan or -exec not found — falling back to inline." → continue to Step 5.

## Step 5 — Hand off

- Mode A → load `procedures/single_procedure.md`
- Mode B → load `procedures/multi_procedure.md`
