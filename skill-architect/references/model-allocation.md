# Model Allocation Reference

Decision framework for selecting the right Claude model when generating a skill's `model:` frontmatter field.

## How the `model:` Field Works

- **Current conversation (Skill tool):** the active model handles everything regardless of this field — no automatic switch occurs.
- **Subagent dispatch (Agent tool):** when an orchestrator spawns this skill as a subagent, it reads `model:` and passes it as the `model` parameter — the subagent actually runs on that model.
- **Standalone use:** serves as documentation — tells the user which model to configure when running Claude Code with this skill (e.g. `claude --model haiku /my-skill`).

## Benchmark Summary

| Model | Input / Output (per MTok) | Context | Max output | Latency | Adaptive thinking |
|---|---|---|---|---|---|
| Haiku 4.5 | $1 / $5 | 200k | 64k | Fastest | No |
| Sonnet 4.6 | $3 / $15 | 1M | 64k | Fast | Yes |
| Opus 4.6 | $5 / $25 | 1M | 128k | Moderate | Yes |

## Decision Framework

| Signal | → `haiku` | → `sonnet` (default) | → `opus` |
|---|---|---|---|
| Task complexity | Simple, deterministic | Moderate, multi-step | Complex, ambiguous, novel |
| Reasoning depth | Minimal | Moderate | Deep / multi-phase |
| Agentic role | Sub-agent executor | Orchestrator / main agent | Planner, architect |
| Output length | Short (< 1 page) | Medium | Long / comprehensive |
| Call frequency | High-volume, parallel | Regular | Low-frequency, critical |
| Cost priority | Maximum economy | Balanced | Quality over cost |

## Rule of Thumb

**Default: `sonnet`** — unless there is a clear reason to go cheaper or smarter.

**Use `haiku`** when the skill does: data extraction, file parsing, simple formatting, sub-agent execution, high-throughput parallel operations, no complex reasoning required.

**Use `opus`** when the skill does: complex multi-phase research synthesis, architectural planning, high-stakes ambiguous decisions, orchestration of other agents, tasks where output quality outweighs cost.

## Field Values

```yaml
model: haiku    # claude-haiku-4-5-20251001
model: sonnet   # claude-sonnet-4-6
model: opus     # claude-opus-4-6
```
