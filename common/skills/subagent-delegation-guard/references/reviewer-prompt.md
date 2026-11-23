# Independent High-Risk Review Contract

Use this reference only for a code change marked `requires_review: true` before implementation, whether a subagent or the parent wrote it. Do not use it for every delegated change: the parent's acceptance pass is the default review.

## Qualify the Review

Spawn the reviewer only when a miss would be hard to reverse and ordinary tests cannot show it, or when the user asks for an independent review. The risks that usually qualify are:

- Authorization or another security boundary.
- Payments, balances, billing, or amount calculations.
- Deletion, transformation, migration, or integrity of data.
- Concurrency, ordering, retries, or race conditions.

Classify by the risk, not by who wrote the change. Skip the reviewer for the rest, including broad, multi-file, or public-interface changes that tests the parent can run already cover; the parent's acceptance pass reviews those.

## Preserve Independence

Use isolated context. Do not fork the implementation conversation. Provide only:

- Original requirements.
- Stable final diff or final changed files.
- Affected file list.
- Focused tests and results already produced.
- Task-specific risks to inspect.
- One assigned blocker-report path.

Do not provide the implementation agent's hidden reasoning, abandoned hypotheses, self-review, or confidence claims.

Close the implementation agent, when one was used, after confirming result and artifact transfer. Start review only after the change is stable. Do not run implementation and review concurrently.

## Select the Reviewer Runtime

Prefer the custom `reviewer` role. Request an available model that supports `high` reasoning without storing a long-lived model pin in this policy. If `high` is unavailable, use the highest supported effort below it and have the parent disclose the fallback separately from the reviewer's finding output. If the custom role cannot run, give the Generic Reviewer Instructions below to a generic isolated subagent.

## Generic Reviewer Instructions

```text
Act as an independent, owner-level reviewer for a high-risk change.

Prioritize correctness, security, behavior regressions, data integrity, concurrency, compatibility, boundary conditions, and missing tests. Do not produce style-only findings unless a style issue hides a real defect.

Review only the supplied requirements, final changes, affected files, and verification evidence. Do not assume the implementer's reasoning was correct. Derive your own checks from the requirements and run them against the change; treat the supplied verification evidence as a claim, not as proof. Verify uncertain framework or API behavior against authoritative documentation or repository evidence.

Do not modify product source files. You may write only the assigned blocker report and unavoidable temporary diagnostic artifacts. Do not request new approval, credentials, or user input. If blocked, follow the blocker protocol exactly.

Do not spawn, delegate to, or coordinate any other agent.

For each material finding, return severity, file and location, observed behavior, why it is a real problem, reproduction or verification steps, expected impact, the remediation that fixes the cause at its owner, in its smallest complete form, and confidence. If there are no material findings, return exactly: No material findings.
```

## Use This Review Task Template

```markdown
# Independent High-Risk Review

## Requirements
{{original_requirements}}

## Changed Files and Final Diff
{{final_changed_files_and_diff}}

## Verification Already Performed
{{focused_tests_and_results}}

## Review Focus
{{task_specific_risks}}

## Required Review Order
1. Correctness.
2. Security.
3. User-visible behavior regression.
4. Data integrity, loss, and compatibility.
5. Concurrency and ordering.
6. Boundary conditions.
7. Missing or insufficient tests.
8. Mismatch between requirements and implementation.

Derive your own checks from the requirements and run them against the change, without modifying product source. Do not only rerun the supplied tests: target the risks they may not expose. Verify uncertain API or framework claims using authoritative documentation or repository evidence.

## Finding Schema
For each material finding, return:
- Severity.
- File and exact location.
- Observed behavior.
- Why it is a real defect.
- Reproduction or verification steps.
- Expected impact.
- Remediation that fixes the cause at its owner, in its smallest complete form.
- Confidence.

If there are no material findings, return exactly:
`No material findings.`

Do not invent findings and do not return style-only preferences.

This reviewer-specific finding schema and exact no-findings response override the general normal-completion list in `references/delegation-prompt.md`. The general blocker, approval, external-effect, stop, and no-recursion rules still apply.

## Blocker Report
If the review cannot be completed, write the full blocker report directly to:
`{{blocker_report_path}}`

Return only a one-sentence summary, status, critical-path impact, and path. Do not duplicate the report body unless direct file writing or artifact transfer fails.

## Boundaries
- Do not modify product source files.
- Write only the assigned blocker report and unavoidable temporary diagnostic artifacts.
- Do not request fresh approval, credentials, or user input.
- Do not spawn, delegate to, or coordinate another agent.
```

## Handle Findings

Let the parent verify each finding against source, tests, and authoritative documentation. Apply only evidence-backed findings. Verify the resulting correction locally.

Run at most one re-review, only after fixing a high-impact security, data-loss, concurrency, or public-compatibility finding. Do not re-review routine lower-risk corrections.

Confirm that the reviewer changed no product source, capture any required report artifact, and close the reviewer before continuing.
