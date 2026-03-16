# Init Procedure — skill-architect-update

Follow these steps when `skill-architect-update` is invoked without a skill path or name.

## Step 1 — Present location options

```
Where should I look for the skill to update?
(A) ~/.claude/skills/     — Claude skills directory
(B) Current working directory
(C) Custom path — I will provide it
```

## Step 2 — Scan the selected location

- Use Glob to find all directories containing a `SKILL.md` file within the chosen location.
- A valid skill directory = any folder that contains `SKILL.md`.

## Step 3 — Present the skill menu

List all found skills as a numbered menu:

```
Found skills:
1. skill-architect              (~/.claude/skills/skill-architect)
2. skill-architect-proofing     (~/.claude/skills/skill-architect-proofing)
3. skill-architect-update       (~/.claude/skills/skill-architect-update)

> Enter a number to select, or type a custom path:
```

## Step 4 — Confirm selection

- Confirm the selected skill name and resolved path with the user.
- Set `skill_path` to the confirmed path.

## Step 5 — Hand off

- If `PENDING_MODE` is set: load `procedures/[PENDING_MODE]_procedure.md`.
- Otherwise: load `procedures/proofing_procedure.md` (default).

## Edge Cases

- **No skills found:** Inform the user, suggest checking the path or providing a custom one.
- **Custom path provided:** Validate it contains a `SKILL.md` before proceeding.
- **User types a name instead of a number:** Attempt to match against found skill names.
