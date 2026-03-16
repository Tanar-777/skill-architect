# Init Procedure — skill-architect-proofing (no argument mode)

Follow these steps when `skill-architect-proofing` is invoked with no skill path or name.

## Step 1 — Ask where to look

Present the user with these options:

```
Where should I look for the skill to proof?
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

## Step 4 — Confirm and proceed

- Confirm the selected skill name and path with the user.
- Proceed with proofing on the confirmed path.

## Edge cases

- **No skills found:** Inform the user, suggest checking the path or providing a custom one.
- **Custom path provided:** Validate it contains a `SKILL.md` before proceeding.
- **User types a name instead of a number:** Attempt to match against found skill names.
