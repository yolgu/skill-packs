# Blocker Reporting and Investigation Contract

Use this reference before spawning to assign a report path, and whenever a child becomes blocked, stalls, or needs investigation.

## Allocate the Path Before Spawn

Use a workspace-relative path:

`blockers/<session-key>/<YYYYMMDD-HHMMSS>-<logical-agent-name>.md`

Apply these rules:

- Use the actual task or session identifier as `<session-key>` when available.
- Otherwise create one `YYYYMMDD-HHMMSS-<task-slug>` key and keep it stable for the full parent request.
- Assign a descriptive lowercase hyphenated logical agent name before spawn.
- Add `-02`, `-03`, and later suffixes when a logical name repeats.
- Create the session directory before spawn.
- Do not prewrite report content in the parent.
- Do not delete the session directory merely because it remains empty.
- Show the user an absolute path, but give the child the workspace-relative path.

For `blocker-investigator`, assign two distinct paths in its task prompt:

- Subject blocker report path: the existing report it must read, update, and return during normal investigation.
- Investigator-self blocker path: the unique path allocated to this investigator spawn and used only when a distinct problem blocks the investigation itself.

Create one report per blocked delegated task. Keep related symptoms in one report. Split only independent root causes. Let an investigator update the original report's `Investigation` section. If the investigator itself hits a distinct blocker, assign a new report under its own logical name.

## Write the Report Directly

Require the blocked child to write the complete report to the assigned path. Have it return only:

- One-sentence summary.
- Status.
- Whether the blocker stops the full required path.
- Report path.

Do not route the full body through the parent merely so the parent can write it again. Let the parent read it only when needed for progress, integration, investigation, or user action.

When a separate workspace is used, transfer the Markdown file as a required artifact. Confirm that it exists in the parent's workspace before spawning an investigator or closing the worker.

If direct writing or artifact transfer fails, return the full Markdown report as the only fallback. The parent must then save it at the assigned path. Treat this as loss prevention, not the preferred flow.

## Use These Statuses

- `open`: Recorded and not yet diagnosed.
- `investigating`: An investigator is actively narrowing the cause.
- `diagnosed`: The cause is established, but no validated fix has been applied.
- `needs-user`: A user decision, approval, credential, or external action is required.
- `resolved`: A responsible worker or the parent applied and verified the fix.

Do not mark a report `resolved` merely because the cause is known.

Set `blocking_scope` to `subtask` when other required work can continue. Set it to `full-required-path` when the blocker prevents all remaining required work and cannot be bypassed or solved locally.

Set `user_action_required` to `true` exactly when status is `needs-user`; set it to `false` for every other status. Keep the field synchronized whenever status changes.

## Use This Report Template

```markdown
---
id: {{blocker_id}}
status: open
created_at: {{iso_8601_timestamp}}
logical_agent_name: {{logical_agent_name}}
affected_task: {{affected_task}}
blocking_scope: {{subtask_or_full-required-path}}
user_action_required: {{true_when_needs-user_otherwise_false}}
---

# Blocker Report

## Goal
{{original_goal}}

## Completed Work
{{completed_work_before_blocker}}

## Blocked At
{{exact_step_that_could_not_continue}}

## Observed Evidence
{{actual_behavior_errors_commands_and_relevant_output}}

## Expected Result
{{expected_behavior}}

## Attempts
{{already_attempted_actions_and_results}}

## Changed Files
{{partial_or_completed_file_changes}}

## Impact
{{what_can_and_cannot_continue}}

## Investigation
{{investigator_findings_or_pending}}

## Resolution
{{applied_resolution_and_validation_or_pending}}

## Next Action
{{specific_next_action_owner_and_required_input}}
```

Preserve enough original error text to reproduce the failure. Remove or mask tokens, passwords, keys, personal data, and unrelated secrets.

## Continue Around Non-Critical Blockers

Do not stop the full user request merely because one child is blocked. Preserve the report, close the worker after artifact transfer, and continue all non-dependent work.

Ask the user only when the blocker prevents all remaining required work and the parent cannot bypass or solve it locally. Do not claim completion when a required outcome remains blocked. Report optional unresolved blockers accurately when the required outcome is otherwise complete.

## Decide Whether to Investigate

Consider `blocker-investigator` only for a documented blocker that evidence can narrow and when one bounded independent investigation is materially useful. Do not call it automatically for every diagnosable blocker. For an unresolved technically diagnosable blocker on the required path, run it once before requesting user action unless the parent can already solve the blocker directly. Qualifying examples include:

- Code defects.
- Non-reproducing or unexplained test failures.
- Tool behavior.
- Environment or configuration differences.
- Dependency conflicts.
- Runtime condition or state differences.

Do not use it for:

- Product or scope decisions only the user can make.
- Credential delivery.
- Approval.
- Waiting for external-service recovery.
- A known external state change that investigation cannot resolve.

Do not repeat investigation for the same blocker. Treat new evidence as a separate blocker only when it supports an independent new cause rather than a renamed retry.

## Select the Investigator Runtime

Prefer the custom `blocker-investigator` role with isolated context and `max` reasoning on an available supporting model. Give it the subject blocker report path and a unique investigator-self blocker path. If `max` is unavailable, use the highest supported effort and disclose the fallback. If the custom role cannot run, give the Generic Investigator Instructions below to a generic isolated subagent.

## Generic Investigator Instructions

```text
Investigate a documented blocker independently and produce evidence that narrows the real cause.

Read the supplied subject blocker report directly. Update and return that subject report during normal investigation. Use the separately assigned investigator-self blocker path only if a distinct problem blocks this investigation. Reproduce the failure when possible. Distinguish code defects, environment differences, dependency conflicts, permission boundaries, missing requirements, and external conditions. Record evidence, rejected hypotheses, the most likely cause, confidence, and a specific next action in the subject report.

You may run non-destructive diagnostics and create unavoidable temporary investigation artifacts. Do not modify product source files. Do not request fresh approval, credentials, or user input from this thread. If user action is required, set the report status to `needs-user` and state exactly what is needed and why.

Do not spawn, delegate to, or coordinate any other agent.

Use `investigating` while working, `diagnosed` when the cause is established but no validated fix has been applied, and `resolved` only after a fix has been applied and verified by the responsible worker or parent.

Return only a concise conclusion and the updated subject report path. If the investigation itself is blocked, return the investigator-self report status and path instead. Do not duplicate either report body unless direct file writing or artifact transfer fails.
```

After investigation, let the parent choose whether to fix directly, resume the original worker when its prior context materially helps, create a new safe implementation task, or request user action. Close the investigator after confirming report transfer.

## Handle an Unresponsive Agent

Before spawn, record a task-appropriate expected progress checkpoint and one grace interval after the single permitted status request. Do not impose a universal duration. When an agent passes that checkpoint without progress, send one status request. If it provides no response or artifact progress during the recorded grace interval, capture available artifacts and close it.

Because the child could not write a complete report, let the parent create this minimal exception report at the assigned path:

```markdown
---
id: {{blocker_id}}
status: open
created_at: {{iso_8601_timestamp}}
logical_agent_name: {{logical_agent_name}}
affected_task: {{affected_task}}
blocking_scope: {{subtask_or_full_path}}
user_action_required: false
kind: agent-unresponsive
---

# Agent Unresponsive Report

## Goal
{{assigned_goal}}

## Started At
{{start_timestamp}}

## Last Observed Status
{{last_status_and_timestamp}}

## Status Request
{{single_status_request_and_result}}

## Closed At
{{close_timestamp}}

## Preserved Artifacts
{{available_artifacts_or_none}}

## Impact
{{effect_on_parent_work}}

## Next Action
{{specific_owner_and_action}}
```

This parent-written report is permitted because no duplicate full child report exists.

## Preserve Resolution History

Keep every report, including resolved reports. When resolving, update the status and record:

- Confirmed cause.
- Applied fix.
- Verification command or check and result.
- Residual risk.

Do not automatically commit reports, add them to ignore files, delete them, or delete empty blocker session directories. Leave repository-history decisions to the user.
