---
name: executing-plans
description: Use when implementing an existing written plan through completion of the user-authorized scope, with progress updates and explicitly requested review checkpoints.
---

# Executing Plans

## Overview

Load the plan, review it critically, and implement the entire user-authorized scope with relevant verification and necessary integration.

**Core principle:** Plan tasks and implementation packages organize the work; the user's requested outcome determines completion. Continue across internal task boundaries without waiting for another instruction.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Identify the user-authorized scope, acceptance criteria, dependencies, and any checkpoints the user explicitly requested. If the user selected only part of a plan, complete that part.
3. Resolve routine concerns from available evidence. Ask only about a material decision or permission that is necessary to proceed, and continue independent work while it is pending.
4. Track the remaining authorized tasks using the available task tracker or the plan's existing status mechanism.
5. Determine whether tests must run in Docker or local environment before execution.

### Step 2: Implement and Verify

For each remaining authorized task, in dependency order:
1. Mark as in_progress
2. Implement the planned behavior, resolving routine implementation details within the agreed scope.
3. Run the relevant verification in accordance with repository test policy. Diagnose and repair failures within existing authority.
4. Mark as completed only when its acceptance criteria and required checks are satisfied.
5. Continue directly to the next remaining task.

### Step 3: Report Progress Without Ending Execution

- Briefly report meaningful completed work, verification results, and what comes next while continuing implementation.
- Do not stop after a fixed number of tasks, an implementation package, a phase, or a milestone.
- Do not say "Ready for feedback" or ask whether to continue while authorized work remains, unless the user explicitly requested a pause there.
- Incorporate user feedback into the remaining work without treating an ordinary status question as a stop request.

### Step 4: Complete the Requested Outcome

Before the final response, reconcile completed work with the full user-authorized scope. Finish remaining implementation, necessary integration, and relevant verification. Report the resulting behavior and verification evidence; identify any unresolved requirement explicitly rather than presenting partial work as complete.

## When to Pause

Pause at an explicit user checkpoint or stop request. Otherwise, pause only for a necessary decision or permission that is unavailable, or a demonstrated blocker that cannot be resolved within existing authority.

A test failure, missing dependency, or unclear implementation detail requires investigation first; it does not automatically justify stopping. Use evidence to distinguish a recoverable issue from a blocker requiring user input. Do not blindly repeat failed commands or guess material requirements.

When blocked, complete independent unblocked work first, then report the concrete blocker, attempted resolution, remaining scope, and exact input needed to resume. Keep the blocked work marked incomplete.

If the user changes the plan or evidence invalidates its approach, review the affected steps and continue within the authorized scope. Do not expand scope or infer authorization for external actions from the requirement to finish implementation.
