# skill-architect-update

> Guided update workflow for Claude Code skills. Sub-skill of skill-architect, also independently invocable.

## Description

`skill-architect-update` loads an existing skill, accepts a change request, routes to the correct update mode, applies targeted edits following skill-architect standards, bumps the version (SemVer), and delegates validation to `skill-architect-proofing`.

It is the canonical update tool for the skill-architect ecosystem and replaces the legacy `skill-update` skill.

## Usage

```
/skill-architect-update                          ← discovery + default proof mode
/skill-architect-update skill-name               ← proof mode on named skill
/skill-architect-update patch skill-name         ← patch mode directly
/skill-architect-update minor skill-name         ← minor mode directly
/skill-architect-update major skill-name         ← major mode directly
/skill-architect-update proof                    ← proof mode, then discovery
```

## Modes

| Mode | Scope | Version bump | README update |
|---|---|---|---|
| `proof` (default) | Audit + fix proofing issues | PATCH (structural fixes) | If missing |
| `patch` | Bug fix, typo, ≤ 2 files | `0.0.X+1` | No |
| `minor` | New feature, backward-compatible | `0.X+1.0` | Yes |
| `major` | Architectural rewrite | `X+1.0.0` | Full rewrite |

## Routing Table

| Arguments | Action |
|---|---|
| No args | Discovery → proof mode |
| mode only | Store mode → discovery → mode |
| skill only | Skip discovery → proof mode |
| skill + mode | Skip discovery → mode directly |

## Git Operations

`skill-architect-update` handles local edits only. For Git-related operations use the dedicated sub-skills:

| Need | Sub-skill |
|---|---|
| Load or install a skill from a remote repo | `/skill-architect-git-load` |
| Publish a skill to a remote repo | `/skill-architect-git-upload` |

## Related Skills

- [`skill-architect`](../skill-architect/) — parent orchestrator
- [`skill-architect-proofing`](../skill-architect-proofing/) — proofing sub-skill
- [`skill-architect-git-load`](../skill-architect-git-load/) — load/install skills from Git
- [`skill-architect-git-upload`](../skill-architect-git-upload/) — publish skills to Git
