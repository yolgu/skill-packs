---
name: writing-plans
description: Use only when the agent will actually implement a code or configuration change in the current task and needs a multi-step implementation plan before coding. Do not use for standalone plans, strategy, brainstorming, roadmaps, analysis, recommendations, or hypothetical future work that the agent will not implement as part of the same task.
disable-model-invocation: true
---

# Writing Plans

## Overview

Your mission is not to turn the user's request into a simple to-do list, but to convert it into a top-tier plan that a real team, agent, or developer can execute immediately.

Keep the following five perspectives at the same time.

1. Product Strategist: Define why this work is being done and which success criteria it must satisfy.
2. System Architect: Design the structure, boundaries, data flow, dependencies, and interfaces.
3. Execution Lead: Break the work into steps and set dependencies, priorities, and parallelizability.
4. QA / TDD Lead: Attach verification criteria, failure checks, pass checks, and regression prevention to each step.
5. Risk / Handoff Owner: State risks, rollback, security, privacy, operational side effects, and the handoff to the next operator.

Important:

- Do not write concrete implementation code right away. First maximize the quality of the plan.
- Do not output hidden reasoning. Instead, present the basis for each judgment as a concise summary.
- Do not settle uncertain content by guessing; separate it into “Assumption”, “Open Question”, and “Revisit Trigger”.
- A plan must be a contract that can be executed, verified, rolled back, and handed off, not a document that merely looks impressive.

---

# INPUT

The user may give only part of the format below. Set reasonable defaults for empty items, but state important uncertainties.

<TASK>
The goal the user wants to achieve:
{{USER_TASK}}
</TASK>

<CONTEXT>
Current situation, previous attempts, related files, reference documents, constraints:
{{PROJECT_CONTEXT}}
</CONTEXT>

<STACK_OR_DOMAIN>
Tech stack, domain, platform, language, tools:
{{STACK_OR_DOMAIN}}
</STACK_OR_DOMAIN>

<CONSTRAINTS>
Time, cost, security, policy, quality, deployment, and compatibility constraints:
{{CONSTRAINTS}}
</CONSTRAINTS>

<QUALITY_BAR>
The level the user wants:
e.g. MVP, production-ready, enterprise-grade, research-grade, “20000억원 가치급” (worth 2 trillion won)
{{QUALITY_BAR}}
</QUALITY_BAR>

---

# OPERATING PRINCIPLES

## 1. Context First

First, extract the following from the user's input.

- Core goal
- Current state
- Stated requirements
- Implicit requirements
- Prohibitions / non-goals
- Quality bar
- Related resources, files, APIs, and systems
- External dependencies
- How success will be verified
- Important variables the user has not decided yet

Do not stop right away just because the input is insufficient.  
However, present at most one “Blocking Question” only when one of the following applies.

- The goal itself is contradictory.
- Where or on what to execute is completely unclear.
- A security-risky action may be required.
- There is a key choice that could change the direction of the plan entirely.

Otherwise, set reasonable assumptions and continue.

---

## 2. Three-Layer Plan Model

Every plan must have the following three layers.

### Layer A: Strategic Plan

Why it is done, what counts as success, and what is not done.

Must include:

- Goal
- Non-goals
- Success criteria
- Stakeholders / users
- Constraints
- Assumptions
- Open questions

### Layer B: Architecture / System Plan

What belongs where, and through which boundaries and contracts it operates.

Must include:

- Domain model or conceptual model
- System boundaries
- Public interfaces
- Data flow or state transitions
- File/module/resource mapping
- External dependencies
- Security/privacy considerations
- Failure behavior

### Layer C: Execution Plan

In what order, who does what, and how it is verified as it proceeds.

Must include:

- Milestones
- Dependencies
- Parallelizable or not
- Required skills
- Files/resources to create/modify/test
- Completion criteria
- TDD or validation steps
- Risk
- Rollback
- Verification commands/checks
- Handoff notes

---

## 3. Plan Bundle Contract

Do not output the plan only as a single chat message; save it as one master plan and one independent file per P-item.

### Save location

Determine the save location by the following priority.

1. The location the user specified
2. If there is a folder that holds a design document (`design.md`), that folder (place `plan.md` and `items/` next to the design document)
3. A compatible plan-document convention that already exists in the repository
4. Default: `docs/plans/YYYY-MM-DD-<topic>/`

Default structure:

```text
docs/plans/YYYY-MM-DD-<topic>/
|-- plan.md
`-- items/
    |-- P0.md
    |-- P1.md
    `-- ...
```

Rules:

- Write `<topic>` in short lowercase kebab-case.
- The `P0`, `P1`, ... identifiers are stable work IDs, not an execution order. Express order through dependencies.
- Fix file names as `P{number}.md` so links do not break when a title changes.
- Put exactly one P-item in each `items/P{number}.md`.
- When adding or removing a P-item, do not renumber existing IDs unnecessarily.

### Source of truth and references

- `plan.md` is the entry point of the overall plan and owns the Strategic Plan, the Architecture / System Plan, the milestone index, the overall dependency diagram, the regression matrix, the side-effect review, common verification, and the handoff.
- `items/P{number}.md` is the Single Source of Truth for that task's details and its status, dependencies, files/resources, risk, rollback, completion criteria, and TDD / validation steps.
- The milestone index in `plan.md` must reference every P-item with a relative link. Do not duplicate the full body of a P-item in `plan.md`.
- Each P-item references `../plan.md` as its parent plan at the top and, when it has dependencies, references the corresponding P-item files in the same directory with relative links.
- Derived information needed for the overall view, such as the master's dependency diagram and regression matrix, is allowed, but synchronize it in the same work whenever a P-item changes.
- Do not use absolute paths, `file://` URIs, or chat-only references for links between documents.
- In the final response, present only the `plan.md` link and the number of P-items created, concisely, and do not paste the full file contents again.

### Bundle creation order

1. Inventory the full scope and set the P-item boundaries. For a feature implementation plan, the item boundaries and order follow the feature implementation flow document of code-principles (`references/feature-implementation-flow.md`): one base work item, thin vertical slices that each run from an entry point to storage, and a pre-exposure gate item last.
2. Fix stable P-IDs and dependencies.
3. Write each `items/P{number}.md`.
4. Write `plan.md`, referencing every P-item.
5. Verify links, IDs, dependencies, and omissions.

---

## 4. Plan Item Contract

Each work item must follow the contract below in its own independent `items/P{number}.md` file.

Put the five fields `Entry point`, `Design decisions`, `Concern check`, `Behavior list`, and `Claim (at completion)` only in feature slice items that have an entry point. Do not put them in items that change only documents or configuration, or in the base work item. Make the pre-exposure gate item the last item in the same format, but write `Readiness level` (one line: how ready it is for users to start using it openly) instead of `Design decisions`, and list in its completion criteria the readiness items and each item's prerequisites. Write follow-up work after release in the Revisit triggers of `plan.md`, not in that item.

```markdown
# [P{number}] {Task Name}

Parent plan:

- [Overall plan](../plan.md)

Status:

- {Pending|In Progress|Blocked|Done}

Purpose:

- Explain in one sentence why this task is needed.

Goal linkage:

- Link which Goal or Success Criteria it satisfies.

Dependencies:

- depends_on: [] or [[P0](P0.md), [P1](P1.md), ...]
- parallelizable: true/false

Required skills:

- [skill-1, skill-2, ...]

Boundary mapping:

- Public interface:
- Implementation boundary:
- Out-of-scope adjacent behavior:
- Regression scenarios:

Entry point:

- One of HTTP, Scheduler, Batch, Consumer, Listener, Screen. This value determines the shape of the outer-loop test and the transaction owner.

Design decisions:

- Write only the values decided at design time. Do not copy rule text.
- Transaction boundary: Up to which step is one atomic unit. If there is an external call, whether that call comes before or after the atomic unit, and the reason if it is placed inside. The state left behind, and how it is handled, when the call fails or its result is unknown at that position. For how the boundary is opened, only the value, in the terms of the technical rules.
- Failure meaning: For each failure, its classification (business failure, technical failure), error code, response status, and the state left behind (atomic-unit rollback or compensation).
- Log points:
- Authorization check:
- Domain promotion: none, or yes (promotion condition number)
- Entry-point specifics: Values decided per entry point, such as the idempotency key, retry classification, and chunk size

Concern check:

- Change type triggers: The change-type triggers this slice fires
- Applied: Every always-on item and every fired trigger item, listed by rule title without omission
- Intentionally excluded (reason):

Behavior list:

- For each item: number, kind (normal, failure, boundary, atomicity), the behavior in one line, the representative partition, and one line on what is guaranteed under which hypothesis when it passes. Do not write implementation structure.
- The first normal item is the outer-loop test of TDD step 1. Turn only one item into a test at a time.
- Plan writing drafts it. Items revealed during implementation are only appended by plan execution, marked "(added during execution)". Preserving existing behavior is the job of Regression scenarios in Boundary mapping. Do not add a status column.

Files / Resources:

- Create:
- Modify:
- Test:
- Delete:

Difficulty:

- 🟢 Low / 🟡 Medium / 🔴 High

Risk:

- Write the biggest possibility of failure.

Rollback:

- Write how to revert when this task fails.

Completion criteria:

- [ ] Measurable completion criterion 1
- [ ] Measurable completion criterion 2
- [ ] Measurable completion criterion 3

TDD / Validation steps:

1. Failing probe or failing test:
   - Outer boundary test: Which test at which boundary (feature slice items)
   - Command/check:
   - Expected before implementation: For feature slice items, the assertion failure message (a compile error or build failure is not red). For other items, the value observed before the change
2. Minimal implementation:
   - Action:
3. Passing verification:
   - Command/check:
   - Expected after implementation:
4. Regression lock:
   - What is locked so that it does not break again?

Claim (at completion):

- Covered specification items: Numbers from the Behavior list
- Hypotheses relied on:
- Risks not verified:
- Plan writing leaves these three lines empty, and plan execution fills them when marking the item complete.

Notes:

- Important judgments, limits, and cautions.
```

---

## 5. Anti-Vagueness Rules

Forbid the following expressions or make them concrete immediately.

Forbidden:

- “구현한다” (implement)
- “연동한다” (integrate)
- “최적화한다” (optimize)
- “테스트한다” (test)
- “보안 고려” (consider security)
- “필요시” (if needed)
- “나중에” (later)

Replace with:

- What is created, modified, or deleted
- Which file, module, API, DB, or tool is involved
- What the inputs and outputs are
- Which command or check confirms that it passes
- What state results on failure and how it is recovered
- What is not done now

---

## 6. Missing-Work Prevention

Long work, large documents, and work that spans several modules must include a missing-work prevention strategy.

Include:

- How the full scope is inventoried
- The criteria for splitting into chunks or modules
- A sequence number for each chunk/module
- How each file's processing status is tracked through the P-item links in `plan.md`
- How to retry only the failed chunks
- The final merge method
- A checklist for verifying nothing is missing

---

## 7. Context Ledger Requirement

Long-running, agent, automation, plugin, and multi-step implementation plans must design an observable state store.

Include:

- state
- events
- context snapshot
- plan
- artifacts
- cancellation / resume state
- user intervention requests

Rules:

- Do not store hidden reasoning.
- Only observable events, summaries, tool calls, results, and state changes are stored.
- If the user asks midway, “How far along is it now?”, it must be possible to answer.

---

## 8. Progressive Context / Skill Loading

When a lot of context is available, do not read all of it; load it progressively.

Priority:

1. Context the user provided directly in this request
2. Explicit instructions in the current working directory or the current conversation
3. Higher-scope policy/project instructions
4. The relevant skill catalog or document list
5. The detailed document or SKILL.md at the moment it is actually needed

Rules:

- Do not read every skill/document body indiscriminately.
- Record which context was used.
- For conflicting instructions, state the priority and the reason.

---

## 9. Output Format

The final deliverable must be split into `plan.md` and P-item files.

### Master file: `plan.md`

`plan.md` follows the structure below.

```markdown
# {Plan Title}

## 1. Executive Summary

- Summarize the goal, approach, key risks, and success criteria in one paragraph.

## 2. Extracted Context

- User goal:
- Current situation:
- Constraints:
- Existing assets:
- Assumptions:
- Open questions:

## 3. Success Criteria

| Goal | Measure | Verification |
| ---- | ------- | ------------ |

## 4. Scope Guard

### In scope

- ...

### Out of scope

- ...

### Revisit triggers

- ...

## 5. Architecture / System Model

- Domain concepts:
- Components:
- Public interfaces:
- Data/state flow:
- Storage/artifacts:
- Security/privacy:

## 6. Milestone Index

| Item | Purpose | Depends on | Parallelizable |
| ---- | ------- | ---------- | -------------- |
| [P0 - {Task Name}](items/P0.md) | ... | - | true/false |
| [P1 - {Task Name}](items/P1.md) | ... | [P0](items/P0.md) | true/false |

List every P-item without omission, but write the detailed contract only in each linked file.

## 7. Dependency Diagram

Show it as a text diagram.

Example:
P0 -> P1
P1 -> P2
P1 -> P3
P2, P3 -> P4

## 8. Regression Matrix

| Scenario | Setup | Action | Expected result | Locked by |
| -------- | ----- | ------ | --------------- | --------- |

## 9. Side Effect Review

| Area | Risk | Mitigation | Verification |
| ---- | ---- | ---------- | ------------ |

## 10. Verification Commands / Checks

- Command/check:
  - Expected:

## 11. Handoff Context

- Current status:
- Key decisions:
- Watchouts:
- Next operator starts from:
- Do not do:

## 12. Self-Audit Before Final

Check the items below, reinforce whatever is lacking, and then give the final answer.

- [ ] Every Success Criterion has a verification method.
- [ ] Every P-item exists in exactly one independent `items/P{number}.md` file.
- [ ] `plan.md` references every P-item with a relative link and does not duplicate P-item bodies.
- [ ] Every P-item has a parent plan, dependencies, risk, rollback, and validation.
- [ ] Every P-ID is unique and every dependency link resolves to a real file.
- [ ] There are no orphan P-items and no broken links.
- [ ] Every important constraint is reflected in the Scope Guard.
- [ ] There is a missing-work prevention strategy.
- [ ] There is a regression matrix.
- [ ] There are verification commands or checks.
- [ ] Hidden reasoning is not exposed.
- [ ] Uncertainty is separated into Assumption/Open Question.
- [ ] It is at a level the next operator can execute immediately.
- [ ] Every feature slice item has `Design decisions`, `Concern check`, and `Behavior list` filled with values.
- [ ] If it is a feature implementation plan, the last item is the pre-exposure gate.
```

### P-item files: `items/P{number}.md`

- Write each task, starting from P0, in a separate file in the “Plan Item Contract” format above.
- Do not create a P-item file that is not in the master, or a milestone entry that has no file.
- Do not repeat common explanations; link to the needed master section.
- Assume the executor reads `plan.md` first and then reads the P-item file to execute.

---

# RESPONSE STYLE

- Write in Korean.
- Unless the user wants it, do not give lengthy theoretical explanations.
- The plan must be concrete, but keep implementation code to a minimum until it is requested.
- Where judgment is needed, do not assert; present it as a “recommended default” (권장 기본값) and a “revisit condition” (재검토 조건).
- When the user asks for “20000억원 가치급” (worth 2 trillion won), interpret it not as exaggerated marketing copy but as a plan that meets the following criteria.
  - Executability
  - Verifiability
  - Extensibility
  - Operability
  - Failure recoverability
  - Handoff readiness
  - Security/privacy consideration
  - Context traceability
