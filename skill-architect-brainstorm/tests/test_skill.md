# Behavioral Tests — skill-architect-brainstorm

## Test 1 — Intent Mode via `-brainstorm` Argument

**Setup:** User invokes `/skill-architect-brainstorm` directly with no parameters.

**Expected behavior:**
- Agent detects intent mode (no `skill_path`, no `caller`).
- Checks for existing `brainstorm-*.md` in current directory — none found.
- Runs Block 1: asks user to describe the skill idea they want to brainstorm.
- Pauses after each block for user input.
- Writes progress to `brainstorm-[skill-name]-[YYYY-MM-DD].md` after each block.
- At session end, asks: "Keep the brainstorm file? [yes / no]"
- Passes structured summary as inline context.

**Pass criteria:**
- Agent does NOT skip blocks.
- Agent writes to `.md` file after each block.
- Agent asks keep-file question at session end.
- No `brainstorm:` frontmatter update (no skill_path provided).

---

## Test 2 — Standalone Mode with Existing Skill

**Setup:** User invokes `/skill-architect-brainstorm skill_path=~/.claude/skills/my-skill`.

**Expected behavior:**
- Agent detects standalone mode (skill_path provided, no caller).
- Checks for existing `brainstorm-my-skill-*.md` in current directory — none found.
- Reads `~/.claude/skills/my-skill/SKILL.md`.
- Runs Block 1: summarizes current skill state, asks what is unclear or worth questioning.
- Runs Blocks 2–6 in sequence, pausing after each.
- At session end: updates `brainstorm:` field in `~/.claude/skills/my-skill/SKILL.md` frontmatter.
- Asks: "Pass these conclusions to skill-architect-update? [yes / no]"

**Pass criteria:**
- Agent reads SKILL.md before Block 1.
- Agent updates `brainstorm:` frontmatter after session.
- Agent offers to pass conclusions to skill-architect-update.

---

## Test 3 — Session Flag Detection (Re-invocation)

**Setup:** A `brainstorm-my-skill-2026-03-20.md` file already exists in the current directory. User invokes `/skill-architect-brainstorm skill_path=~/.claude/skills/my-skill`.

**Expected behavior:**
- Agent detects existing brainstorm file.
- Informs user: "A brainstorm session already exists for this skill (brainstorm-my-skill-2026-03-20.md)."
- Asks: "Resume, start fresh, or use existing output as-is? [resume / fresh / use-as-is]"
- Does NOT run a new session without user confirmation.

**Pass criteria:**
- Agent does NOT proceed to Block 1 without user input.
- Agent correctly names the existing file.
- All three options are offered.

---

## Test 4 — No-Findings Path

**Setup:** User runs brainstorm in intent mode. Blocks 3 and 4 yield: 1 major trade-off and 1 major edge case (below both thresholds).

**Expected behavior:**
- Agent completes Blocks 1–5 normally.
- At Block 6: agent informs user "No major trade-offs or edge cases found. Brainstorm complete — proceeding."
- Agent does NOT write a `.md` file.
- If `skill_path` was provided: agent still updates `brainstorm:` frontmatter.
- Summary is passed as inline context only.

**Pass criteria:**
- No `.md` file written.
- Frontmatter updated if applicable.
- Inline summary still provided.

---

## Test 5 — Called from skill-architect-multy-plan

**Setup:** `skill-architect-multy-plan` delegates to brainstorm with `caller=skill-architect-multy-plan`.

**Expected behavior:**
- Agent detects intent mode (caller provided).
- Runs full 6-block protocol focused on the suite concept: which skills are needed, how they interact, dependency risks, trade-off in suite architecture.
- Brainstorm always runs (threshold bypassed — multy context is inherently complex).
- After session: injects structured summary as prefill context into `init_procedure.md`.
- Updates `brainstorm:` field in the plan file frontmatter (if plan file already exists).

**Pass criteria:**
- Agent does NOT apply the 2/3 threshold — brainstorm always runs.
- Summary injected into init_procedure.md context.
- Plan file frontmatter updated if plan file exists.
- Result `.md` file excluded from any git upload.
