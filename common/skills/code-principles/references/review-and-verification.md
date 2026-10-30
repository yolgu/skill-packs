# Review and Verification

## Contents

- [Respect the Requested Mode](#respect-the-requested-mode)
- [Build Evidence Around Behavior](#build-evidence-around-behavior)
- [Test Each Element by Its Role](#test-each-element-by-its-role)
- [Characterize and Protect Existing Behavior](#characterize-and-protect-existing-behavior)
- [Keep Tests Honest and Deterministic](#keep-tests-honest-and-deterministic)
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

## Test Each Element by Its Role

**Principle.** Decide which tests exist from what each element is for, not from a list of layers, and
pair every test double with a test that runs the real implementation it stands for.

The test map, the double rules, and the refactoring judgment below are one rule set whose parts point
at each other: the service row names its doubles, and the double rules require the outbound adapter
row's contract test as their pair. The language and framework rules own the concrete forms (annotations,
test libraries, slice setups), and the client UI rules own the frontend forms.

### The Element Test Map

| Element | Test | Doubles |
| --- | --- | --- |
| Promoted domain object | Framework-free unit tests of its public methods by their outputs; they own the boundary values | None |
| Use case service | Unit tests that call its public methods; they own the business-rule branches | Its immediate-neighbour role interfaces: repository contracts, ports, and other use cases' input contracts. Helpers and deterministic shared calculation components stay real |
| Inbound adapter (HTTP controller, scheduler entry method, message consumer, event listener) | The narrowest test of the adapter. For HTTP, a web slice test (the web layer alone) owns per-field input validation, status codes, and the error response format produced by the exception handlers, and checks the command sent to the use case | The use case's input contract |
| Outbound adapter (persistence adapter, external API client, message publisher) | An integration test against the real target (a database, a broker) or a stand-in server. It is also the contract test for every method a service test doubles and confirms that method's meaning: the value returned when nothing matches, ordering, affected-row counts. Queries with logic of their own (conditions, paging, joins) and the interpretation of the last line of defense are tested here as well: a constraint violation is translated into the same failure meaning, with the same error code, that the pre-check path reports for that business failure, and zero affected rows from a conditional update is read as a conflict | None |
| Main paths | Real-database end-to-end tests, as described below | Only unmanaged outside dependencies (external HTTP APIs, payment, outgoing messages, email and SMS) and time, through the shared end-to-end execution base; the system's own database is real |

- An interface doubled in one row is run against its real implementation in another row, and that run
  is its contract test: the outbound adapter's integration test for a repository contract or a port,
  and the service's own tests for a use case's input contract.
- Every use case that an inbound adapter calls therefore has a narrow input contract interface. Its
  standing as a real contract is set by the interface rules in
  [Feature Implementation Flow](feature-implementation-flow.md#top-down-implementation).

### What Real-Database End-to-End Tests Prove

- Write one normal-flow end-to-end test per use case first, in a failing state; it is the outer loop
  of the slice.
- Add a failure end-to-end test only for what element tests cannot prove:
  - rollback and atomicity: a failure after a write leaves no half-saved state; the assertions on
    execution outside the atomic unit and on after-commit follow-up belong here too;
  - the failure log count across layers: a technical failure leaves exactly one entry at WARN or
    above, a business failure leaves none, and an entry the framework already writes counts as that
    one;
  - authorization denial over the assembled path from authentication to ownership, as one
    parameterized test.
- Leave the rest to the element that owns it: per-field input validation, status codes, and the error
  response format to the web slice test; business-rule branches to the service test; boundary values
  to the domain test; an integrity constraint violation to the adapter integration test (its
  translation) and the web slice test (its response); the last line of defense against concurrent
  requests to the adapter integration test, asserted directly and without threads.
- How each end-to-end assertion is proven (rollback read back from the database, log capture, the
  resulting states of after-commit work, the denial rows) is in
  [Feature Implementation Flow](feature-implementation-flow.md#failure-paths).

### Helpers Inside One Service

- A helper used only inside one service (a validator, a converter, a calculator) has no tests of its
  own. The service tests run through the real helper, and the helper is never doubled.
- When its cases grow too many to cover through the service tests, promote the rule to a domain object
  or to an element with a public contract, and test that element by its row in the map.
- A component that several use cases or modules share is not such a helper; the next rule covers it.

### Shared Components

- A component that several use cases or modules use (a shared validator, converter, or calculator, or
  technical support code) is an element of the map. Test it directly through its public API:
  - a business rule takes the domain object row, a unit test without doubles;
  - technical shared code gets its own unit tests;
  - a component that touches an outside system takes the outbound adapter row, an integration test
    against the real target.
- In the service tests that use it, keep a deterministic calculation component real; when it is a
  role interface with side effects, double it under the rules below.
- Whether a component counts as shared is judged by the shared-code criteria of the
  directory-architecture skill (its architecture model, "Control Shared Code and Integration"): the
  technical shared conditions for technical code, and the Shared Kernel conditions for a shared model
  with business meaning.

### Test Doubles and Contract Tests

- Double a role interface the system owns when it is the immediate neighbour of the code under test:
  a repository contract, a port, or another use case's input contract.
- Stub queries and never verify them. Verify outgoing commands, by expecting the call or by asserting
  what a recording fake captured; this covers commands sent to an owned neighbour (a repository
  contract, another use case's input contract) as well as those sent outward through a port.
- Do not mock values, third-party types, or concrete classes. When a concrete class seems to need a
  mock, expose that relationship as an interface. Many mocks around one unit signal that it has too
  many responsibilities.
- Give every doubled interface a contract test that runs its real implementation; without that pair, a
  double can drift from the real behavior unnoticed. A service test mocks a repository contract by
  stubbing its queries and expecting its commands, and the persistence adapter's real-database
  integration test confirms the meaning of every method so doubled.
- Real-database end-to-end tests then prove only what doubles cannot, as listed above.

### Tests That Break Under Refactoring

- A pure refactoring changes no contract: neither an HTTP contract, nor a use case's input and result,
  nor a role interface's signature and meaning. A test that breaks under it is over-specified (it
  verifies a query, asserts call order, or asserts internal values); fix the test.
- Changing a role interface is a contract change. Its double tests and its contract test changing
  together is expected; when such changes are frequent, revisit the interface design.
- Check this in review.

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

## Keep Tests Honest and Deterministic

**Principle.** A test should fail only when the behavior it names breaks, and should not reshape
production code to make itself convenient.

- Follow the project's test framework and naming style, and name a test for its condition and
  expected behavior.
- Choose test doubles by [Test Doubles and Contract Tests](#test-doubles-and-contract-tests): owned
  role interfaces at the immediate neighbour, including the clock and identifier generator ports, are
  doubled; value objects, input and result models, and plain business objects stay real.
- Do not widen production visibility or add constructors, setters, or bypass methods only for test
  convenience. Put repeated valid-object construction in test fixtures or builders, and keep the
  boundary values that matter visible in the test rather than hidden in fixture defaults.
- Use fixed times and identifiers or the existing clock and generator boundaries instead of reading
  the current time or generating random values directly.
- Wait on a condition or synchronization point instead of a fixed sleep.
- Do not depend on test order, data created by another test, or shared mutable module-level fixtures.
  Restore environment variables, files, and global state that a test changes.
- Assert an exception's type, error code, or meaningful properties when its message is not a public
  contract.
- Keep ordinary unit tests from calling live external providers.

## Use Project Verification as the Baseline

- Prefer the project's official wrapper, formatter, linter, type checker, compiler, test runner, and
  integration commands.
- Treat explicit project commands as the minimum baseline rather than optional suggestions.
- Run the narrowest checks covering the changed contract and plausible regressions. Broaden only for an identified unverified risk or an explicitly required check; do not run the full suite by default.
- Do not rerun a passing check unless relevant code, configuration, dependencies, environment, or inputs changed.
- Inspect exit status, reported errors, failed tests, and meaningful warnings before declaring success.
- Do not skip a baseline check because the file is small, appears temporary, or seems low risk.
- Add focused checks for the most consequential failure mode when the baseline does not cover it.
- Do not edit generated output to satisfy a check; change the authoritative source or tool input.
- Keep lint, type-checker, and analyzer suppressions on the narrowest statement or declaration, name
  the specific rule, and state the reason, plus a reconsideration condition when the constraint is
  temporary. Do not use blanket or file-wide suppressions to make a check pass.

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
- Does each fix in this change correct the rule or data that owns the cause rather than special-casing the reported case?
- Does each new abstraction protect a real concept, shared knowledge, or boundary?
- Are state changes, side effects, optionality, and failure modes visible?
- Are untrusted values validated at the correct boundary without repeated internal defenses?
- Do external calls have explicit time bounds, deliberate retry conditions, and translated failures?
- Are broad catches limited to isolation boundaries, and is each failure logged once without secrets?
- Does the code read in problem order with intention-revealing names?
- Is the public surface no larger than necessary?
- Are unrelated changes and defect fixes kept out of scope?
- Does a refactor preserve observable behavior unless a difference was explicitly authorized?
- Do tests and checks prove behavior and invariants rather than implementation trivia?
- Do test doubles replace only owned role interfaces at the immediate neighbour, does every doubled
  interface have a contract test against its real implementation, and are tests deterministic and
  independent?
- Were the project's required checks actually run and their results inspected?
- Are unavailable checks and remaining risks reported accurately?
