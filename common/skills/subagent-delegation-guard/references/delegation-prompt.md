# Delegation Prompt Contract

Use this reference immediately before every spawn. Build the prompt in memory and pass it directly to the spawn call. Do not save routine delegation prompts to disk, invoke `prompt-clarifier`, or pause for user confirmation unless a material user decision is genuinely required.

## Check Prompt Completeness

Do not spawn until all items are concrete:

1. Logical agent name.
2. Specific goal.
3. Concrete reason delegation is beneficial.
4. Included work.
5. Explicitly excluded work.
6. Minimum required inputs and context.
7. Context-fork decision and inherited assumptions.
8. Read scope.
9. Exact write boundary or no-write rule.
10. Success criteria observable by the parent.
11. Required evidence and verification.
12. Normal completion result schema.
13. `requires_review` value and risk rationale.
14. Unique blocker-report path.
15. Behavior for approval, credentials, user input, and external effects.
16. Prohibition on spawning or coordinating another agent.
17. Stop conditions, including a task-appropriate expected progress checkpoint and one grace interval after the single permitted status request.

If an item cannot be specified, keep the task in the parent or resolve the material ambiguity first.

## Decide Context Forking

Default to `fork_context: false`.

Keep it false for:

- Independent research and codebase exploration.
- Documentation checks.
- Hypothesis or counter-hypothesis testing.
- Independent review.
- Blocker investigation.
- Any task where independence reduces anchoring bias.

Set `fork_context: true` only for implementation when requirements and confirmed decisions are distributed across the current conversation, omission risk is material, continuity benefits clearly exceed token cost, noise, and bias, and the child does not need independent judgment from the implementer's assumptions. Record the comparison and a final boolean decision before spawn. Keep it false when the comparison is uncertain. Even with a fork, restate the task goal, boundaries, success criteria, and blocker path explicitly.

## Assign Identity and Blocker Path

Choose a descriptive lowercase hyphenated logical name such as `auth-api-worker` or `migration-risk-reviewer`. Add `-02`, `-03`, and later suffixes when a name would repeat.

Assign before spawn:

`blockers/<session-key>/<YYYYMMDD-HHMMSS>-<logical-agent-name>.md`

Use an available actual session or task identifier. Otherwise create one stable `YYYYMMDD-HHMMSS-<task-slug>` key for the complete parent request. Create the directory but do not prewrite report content.

For `blocker-investigator`, treat the assigned blocker path as the investigator-self blocker path. Also provide the original subject blocker report as a separate input. During normal investigation, update and return the subject report. Use the investigator-self path only if a distinct problem blocks the investigation itself.

For a resumed agent, treat the resumed turn as a new delegation attempt. Rerun preflight, keep the prior logical base name with the next numeric suffix, allocate a new unique blocker path, and never overwrite a prior report.

## Classify Review Before Code Changes

Set `requires_review: true` before spawn when complexity, ambiguity, or failure impact makes independent review materially useful. Typical triggers include authentication, authorization, security boundaries, payments, destructive data changes, migrations, concurrency, deployment configuration, public interfaces, compatibility, broad core logic, hard-to-test invariants, or complex multi-file behavior.

Usually set `requires_review: false` for narrow mechanical work, formatting, low-impact fixes, or changes with strong focused tests. Do not add review after completion merely because the result feels unfamiliar.

For read-only or otherwise non-code work, set `requires_review: false` with the rationale `no code changes` so every prompt has an explicit value without implying a code review.

## Use This Task Template

```markdown
# Delegated Task

## Identity
- Logical agent name: {{logical_agent_name}}
- Blocker report path: {{blocker_report_path}}
- Context forked: {{true_or_false}}

## Goal
{{specific_goal}}

## Why This Is Delegated
{{parallelism_or_independent_quality_benefit}}

## Scope
{{included_work}}

## Out of Scope
{{excluded_work}}

## Inputs and Context
{{minimum_required_context_and_confirmed_assumptions}}

## Ownership Boundaries
- Read scope: {{read_scope}}
- Write scope: {{disjoint_write_scope_or_none}}
- Shared mutable resources you must not change: {{shared_state_exclusions}}

## Success Criteria
{{observable_success_criteria}}

## Required Verification
{{commands_checks_or_evidence}}

## Review Classification
- requires_review: {{true_or_false}}
- rationale: {{risk_rationale}}

## Completion Output
For `reviewer` and `blocker-investigator`, the completion schema in their dedicated reference overrides this general normal-completion list. Keep this template's blocker, approval, external-effect, stop, and no-recursion rules.

Return only:
1. Whether the goal was achieved.
2. A concise summary of completed work.
3. Files changed, if any.
4. Verification performed and its result.
5. Residual risks or follow-up work.
6. What the parent must verify.

Do not return raw logs, long exploration notes, hidden reasoning, abandoned hypotheses, or self-assessment.

## Blocker Protocol
If blocked, write the complete blocker report directly to:
`{{blocker_report_path}}`

Return only:
- A one-sentence blocker summary.
- The blocker status.
- Whether it blocks the parent's full required path.
- The report path.

Do not duplicate the report body unless direct file writing or artifact transfer fails.

Do not request fresh approval, credentials, or user input from this child thread. Record the requirement with status `needs-user`. Do not perform deployments, remote writes, destructive actions, purchases, messages, publications, or other external effects.

## Stop Conditions
Expected progress checkpoint: {{task_appropriate_duration_or_observable_milestone}}

Grace interval after the single permitted status request: {{task_appropriate_grace_interval}}

Stop and follow the blocker protocol when:
- The goal or boundary cannot be satisfied without changing excluded scope.
- Required input or repository state is missing.
- New approval, credentials, user input, or an external effect is required.
- The assigned write scope conflicts with another active writer.
- Verification reveals a failure that cannot be safely resolved within scope.

## Delegation Boundary
Do not spawn, delegate to, steer, or coordinate any other agent.
```

## Check Before Sending

- Confirm that the reason describes actual time or quality benefit rather than generic thoroughness.
- Confirm that the parent's immediate next step does not depend on this result.
- Confirm that another active worker does not own the same mutable state.
- Confirm that an isolated workspace does not hide overlapping logical ownership of the same file, generated output, or final shared state.
- Confirm that paths are resolvable from the child's workspace.
- Confirm that a separate workspace can return file artifacts when required.
- Confirm that the parent can independently verify the success criteria.
- Confirm that the prompt contains no unnecessary secrets or personal data.
- Confirm that the parent has told the user what is delegated, why, and within which write boundary.

After spawning, continue non-overlapping parent work instead of waiting by default.
