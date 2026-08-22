# Review and Verification

## Contents

- [Respect the Requested Mode](#respect-the-requested-mode)
- [Build Evidence Around Behavior](#build-evidence-around-behavior)
- [Characterize and Protect Existing Behavior](#characterize-and-protect-existing-behavior)
- [Use Project Verification as the Baseline](#use-project-verification-as-the-baseline)
- [Classify Failures Before Retrying](#classify-failures-before-retrying)
- [Review by Impact and Evidence](#review-by-impact-and-evidence)
- [Finish and Report Precisely](#finish-and-report-precisely)
- [Completion Checklist](#completion-checklist)

## Respect the Requested Mode

### Implement or Modify

- Change the human-authored code and tests required to satisfy the authorized behavior.
- Keep directly related cleanup inside the task; leave unrelated repository cleanup untouched.
- Reuse existing owners and contracts before adding new abstractions.
- Fix failures caused by the change within scope and distinguish unrelated existing failures.

### Refactor

- Preserve observable behavior unless a behavior change is explicitly authorized.
- Separate structural improvement from feature work, data-meaning changes, and unrelated defect fixes.
- Characterize behavior that lacks reliable evidence before changing its structure.
- Treat output shape, ordering, absent values, failures, events, stored meaning, and effect timing as
  possible compatibility surfaces.

### Review

- Keep the task read-only unless the user separately authorizes edits.
- Report defects and risks supported by code paths, contracts, tests, or runtime evidence.
- Distinguish confirmed defects from conditional risks and optional improvements.
- Do not manufacture findings when the reviewed change has no actionable issue.

### Explain or Diagnose

- Inspect enough context to explain the behavior, cause, and impact accurately.
- Do not treat explanation or diagnosis as authorization to implement a fix.
- State the evidence and the remaining uncertainty without exposing private reasoning traces.

## Build Evidence Around Behavior

**Principle.** Verify observable behavior and important invariants at the boundary that owns them.

Prefer evidence that answers questions such as:

- Does the operation return the required result for representative and boundary inputs?
- Does the state owner accept valid transitions and reject invalid ones?
- Does a public contract preserve its documented shape and failure behavior?
- Does an external boundary translate inputs, outputs, and failures correctly?
- Does retry or duplicate execution preserve the intended effect?
- Does the defect scenario remain fixed after future changes?

Avoid evidence that proves only incidental implementation details:

- private helper call order with no contractual meaning;
- exact internal collaboration counts that may change during safe refactoring;
- trivial accessors and generated behavior;
- the syntax used to construct a query rather than its result and contract;
- broad snapshots that hide the specific behavior under test.

Choose the narrowest evidence that exercises the real owner. Add integration evidence when the risk
depends on serialization, persistence, process boundaries, external protocols, concurrency, or tool
configuration.

## Characterize and Protect Existing Behavior

Use characterization evidence when existing behavior is observable but poorly documented or not
covered by reliable tests.

1. Identify the callers and compatibility surfaces affected by the structural change.
2. Capture representative successful, boundary, and failure behavior before refactoring.
3. Preserve those observations while changing the internal structure.
4. Record any intentionally authorized difference separately from the refactor.

For a defect fix, add regression evidence that fails for the original defect and passes for the fixed
behavior. Do not rewrite a test merely to agree with a new implementation when the external contract
has not changed.

## Use Project Verification as the Baseline

- Prefer the project's official wrapper, formatter, linter, type checker, compiler, test runner, and
  integration commands.
- Treat explicit project commands as the minimum baseline rather than optional suggestions.
- Start with focused checks for fast feedback, then run the required broader checks.
- Inspect exit status, reported errors, failed tests, and meaningful warnings before declaring success.
- Do not skip a baseline check because the file is small, appears temporary, or seems low risk.
- Add focused checks for the most consequential failure mode when the baseline does not cover it.
- Do not edit generated output to satisfy a check; change the authoritative source or tool input.

When a required service, database, platform, credential, or permission is unavailable, run every
meaningful check that remains possible and report the exact gap.

## Classify Failures Before Retrying

Classify a failed command or check as one of the following:

- caused by the current change;
- pre-existing in the target project;
- environment or permission related;
- missing external dependency, service, or database;
- transient network or service failure;
- incorrect input or command;
- incorrect implementation assumption.

Retry the same approach only when the failure is plausibly transient and the environment may have
changed. Otherwise change the variable that addresses the classified cause before retrying.

- Correct the changed code or test for a change-caused failure.
- Use the project's documented command or working directory for an incorrect command.
- Resolve or report a missing dependency instead of repeating the same failing check.
- Revisit the design or contract for an incorrect assumption.
- Keep unrelated pre-existing failures separate from the authorized change.

Do not treat the number of retries, commands, or tests as evidence of completion.

## Review by Impact and Evidence

Order findings by their effect on the system:

1. Incorrect behavior, security exposure, or data loss
2. Contract and compatibility breakage
3. Ambiguous ownership, hidden effects, and high change risk
4. Missing regression or boundary evidence
5. Clear violations of explicit project rules
6. Optional improvements with a demonstrated benefit

For each actionable finding, provide:

- the tightest useful location;
- the condition that triggers the issue;
- the observable or maintenance impact;
- the evidence supporting the conclusion;
- a correction direction;
- compatibility risk when relevant.

Do not report a personal preference as a defect. Do not equate a different but equivalent design with
an error. If a risk depends on an unverified condition, state the condition and confidence clearly.

## Finish and Report Precisely

Finish when the authorized behavior and completion criteria are satisfied, relevant project checks
have passed, and no significant contrary evidence remains.

- Do not claim an unrun, skipped, or unavailable check passed.
- Report warnings when they materially affect confidence or future work.
- State intentional compatibility exceptions and their scope.
- Explain only non-obvious design choices and meaningful trade-offs.
- Keep compliance narration, skill names, and private reasoning out of code, comments, documents, and
  the final response.
- If no actionable review finding exists, say so and identify any untested boundary that limits
  confidence.

## Completion Checklist

- Does the implementation satisfy the requested behavior and real contracts?
- Is each affected rule, state, and mutation path owned by the right unit?
- Is there one authoritative source for every changed fact and rule?
- Does each new abstraction protect a real concept, shared knowledge, or boundary?
- Are state changes, side effects, optionality, and failure modes visible?
- Are untrusted values validated at the correct boundary without repeated internal defenses?
- Does the code read in problem order with intention-revealing names?
- Is the public surface no larger than necessary?
- Are unrelated changes and defect fixes kept out of scope?
- Does a refactor preserve observable behavior unless a difference was explicitly authorized?
- Do tests and checks prove behavior and invariants rather than implementation trivia?
- Were the project's required checks actually run and their results inspected?
- Are unavailable checks and remaining risks reported accurately?
