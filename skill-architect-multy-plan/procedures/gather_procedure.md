# Gather Procedure — Conversational Input

## Purpose
Guide the user through providing (1) the suite overview and (2) a per-skill breakdown.
In delegated mode, section 1 is skipped (suite overview already known from prefill).

---

## Section 1 — Suite Overview (cold start only)

Ask the user:
> "What is the overall purpose of this skill suite?
> Please describe:
> - What problem does it solve?
> - Who will use it?
> - How do the skills work together?"

Wait for response. Store as `suite_overview`.

From `suite_overview`, propose a suite name:
> "Proposed suite name: `[inferred-name]`
> Confirm or provide a different name?"

Wait for confirmation. Store as `suite_name`.

---

## Section 2 — Per-Skill Breakdown

Present the following prompt:
> "Now describe each skill in the suite.
> For each skill, provide:
> 1. **Name:** short suffix after `[suite-name]-` (e.g. `ingest`, `transform`)
> 2. **Purpose:** what does it do in one sentence?
> 3. **Inputs:** what data or arguments does it take?
> 4. **Outputs:** what does it produce?
> 5. **Dependencies:** does it depend on another skill in this suite?
>
> List all skills at once or one by one — your choice."

Wait for response. Parse into a list of skill definitions.

---

## Validation Pass

For each skill, verify:
- [ ] Name produces a valid slug: `[suite-name]-[suffix]` (lowercase, hyphens, max 64 chars)
- [ ] Purpose is defined (not empty, not `[TO DEFINE]`)
- [ ] Inputs are specified (can be `none` or `conversational`)
- [ ] Outputs are specified
- [ ] No duplicate names within the suite

For any failing check: ask the user to fill in the missing field before continuing.

## Existing Skill Check

For each resolved skill name, check `~/.claude/skills/[name]/` using Glob.
If any exists:
> "Warning: `[name]` is already installed at ~/.claude/skills/[name]/. The plan will include it — exec will warn again before overwriting."

---

## Hand Off

Pass `suite_name`, `suite_overview`, and the validated skill list to `plan_procedure.md`.
