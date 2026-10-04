---
name: using-superpowers
description: Use at the start of a conversation to establish how to find and apply relevant skills before responding or acting.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

Then announce the skills you loaded and what each is for, and follow them. If one has a checklist, create a todo per item.

## Skill Routing

A process skill decides how to work; it does not carry the language, domain, or delegation rules. Stopping after the process skill is the most common miss, so route across all four axes before the first non-skill tool call:

1. **Process**: debugging, receiving review, brainstorming, planning, implementing, verifying.
2. **Artifact**: code touched or specified by a plan (Python, TypeScript, Java, Dart), tests, SQL, configuration.
3. **Domain**: MCP tool contracts on either side (server or consumer), module or directory boundaries, DB release, UI.
4. **Delegation**: subagents suggested (including by plan mode) or considered.

Collect every skill whose description matches any axis and load them together in one parallel batch of Skill calls. Announce one line with the loaded skills and any near-miss skipped because its own exclusion clause applies.

Route again when the phase changes, such as review → plan → implementation or entering plan mode. Later calls to this skill only return "already loaded", so this step has to be run from memory each turn.

## Skill Priority

When multiple skills apply, process skills set the approach and implementation or domain skills (frontend-visual-design, etc.) carry it out. Load both in the same batch; the order describes how they are applied, not a later loading step. Brainstorming and systematic-debugging are Superpowers' most common process skills, but the rule holds for any of them.

- "Let's build X" → brainstorming plus the implementation skills.
- "Fix this bug" → systematic-debugging plus the domain skills.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Platform Adaptation

If your harness appears here, read its reference file for special instructions:

- Claude Code: invoke skills with the `Skill` tool; no reference file needed.
- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Hermes Agent: `references/hermes-tools.md`

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
