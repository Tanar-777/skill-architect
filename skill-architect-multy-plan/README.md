# skill-architect-multy-plan

Plans the creation of a suite of interdependent Claude Code skills following the `skill-architect` philosophy. Outputs a structured, human-editable `[suite-name]-plan.md` consumed by `skill-architect-multy-exec`.

## Usage

```
/skill-architect-multy-plan
/skill-architect-multy-plan reference_file=path/to/brief.md
/skill-architect-multy-plan reference_file=path/to/brief.md output_path=./plans/
```

## Trigger Conditions

- **Manual:** invoke directly when starting a multi-skill project.
- **Delegated:** `skill-architect` invokes this skill at Step 2 when it identifies 3 or more distinct scripts or logical units, passing pre-fill context (name candidate, idea, Step 1 notes).

## Input Modes

| Mode | Condition | Behavior |
|---|---|---|
| Delegated | `prefill` object provided by skill-architect | Suite overview pre-filled; asks only for per-skill breakdown |
| File | `reference_file` argument provided | Parses file; supplements missing fields conversationally |
| Cold start | No arguments | Full conversational flow: suite overview then per-skill breakdown |

## Process

1. **Init** — detect mode, credential scan if file provided, check for existing plan file
2. **Gather** — collect suite name, overview, per-skill names/purposes/inputs/outputs/dependencies
3. **Synthesize** — topological sort by dependencies, complexity estimation, ASCII skill tree
4. **Validate** — present plan to user; apply renames, merges, splits, additions, removals
5. **Write** — save approved plan to `[suite-name]-plan.md` with `status: approved`

## Plan File Format

The output file uses YAML frontmatter for machine-readable state + Markdown body for human readability:

```yaml
---
suite: my-suite
plan_version: 1.0
created: 2026-03-16
last_updated: 2026-03-16
status: approved        # draft | approved | in_progress | complete
skills:
  - name: my-suite-ingest
    depends_on: []
    status: pending     # pending | in_progress | done | skipped
    generated_at: ~
  - name: my-suite-transform
    depends_on: [my-suite-ingest]
    status: pending
    generated_at: ~
---
```

- `status` (suite level): updated by `exec` as generation progresses
- `skills[].status`: updated by `exec` after each skill is generated
- `plan_version`: bumped by 0.1 each time the plan is revised
- `generated_at`: set by `exec` to the date the skill was generated

## Incremental Updates

Re-invoke with the same output path to update an existing plan:
```
/skill-architect-multy-plan output_path=./plans/
```
The skill detects the existing file, loads it, and enters revision mode. `plan_version` is incremented on save. Skills already marked `done` are preserved.

## Next Step

After the plan is written, run:
```
/skill-architect-multy-exec plan_file=[path]/[suite-name]-plan.md
```

## Dependencies

| Skill | Role |
|---|---|
| `skill-architect-multy-exec` | Consumes the plan file to drive sequential skill generation |

## Security

- Scans reference files for credentials (`sk-`, `Bearer`, `password =`, `-----BEGIN`, `api_key`) before parsing
- Never writes credential values into plan files
- Offers strip / review-manually / cancel on detection
