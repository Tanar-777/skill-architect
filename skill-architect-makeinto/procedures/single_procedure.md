# Single Procedure — skill-architect-makeinto (Mode A)

Generates one skill from one file or one dominant logical unit.

## Step 1 — Infer metadata

Load and execute `procedures/infer_procedure.md` with the source `file_path`.

Returns: `name`, `description`, `inputs`, `outputs`, `side_effects`, `language`, `functions`, `classes`.

## Step 2 — Draft skill files

Using the inferred metadata, draft the following (display to user, do NOT write yet):

### SKILL.md draft
- Frontmatter: `name`, `version: 1.0.0`, `description`, `allowed-tools`
- All 5 mandatory sections populated from inferred data
- `# STRICT INSTRUCTIONS` includes the core logic summary extracted from the source code
- `# EXPECTED FORMAT (I/O)` lists all inferred inputs and outputs

### schema.json draft
- One property per inferred input parameter, with type and description
- `required` array for non-optional params

### README.md draft
- Usage section with example invocation
- Parameters table
- Output structure

### tests/test_[name].py draft
```python
def test_[name]():
    # TODO: implement based on inferred inputs/outputs
    # Input: [inferred inputs]
    # Expected output: [inferred outputs]
    assert True  # placeholder
    print("OK: test_[name] placeholder passed")

if __name__ == "__main__":
    test_[name]()
```

## Step 3 — Present and confirm

Display all drafted file contents clearly labeled. Ask:

```
Ready to generate skill '[name]' from [file_path].
Files to write:
  ~/.claude/skills/[name]/SKILL.md
  ~/.claude/skills/[name]/schema.json
  ~/.claude/skills/[name]/README.md
  ~/.claude/skills/[name]/tests/test_[name].py

Proceed? [yes / edit / cancel]
```

- `yes` → write all files
- `edit` → ask what to change, re-draft, re-present
- `cancel` → exit

## Step 4 — Write files

Write all four files using Write tool.

## Step 5 — Proof

Invoke `skill-architect-proofing` on the generated skill directory (Branch 1).
Pass `skill_path = ~/.claude/skills/[name]/`.

## Step 6 — Done

Report result. If proofing found issues, offer to fix via `skill-architect-update`.
