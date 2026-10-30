# Feature Implementation Flow

This document owns the language-agnostic order for implementing one feature through every layer,
from its entry point to the database: what to decide before the first test, which test comes first,
how implementation descends through the layers, how failure paths are proven, and what the last work
item before user exposure checks. Which tests each element has, how test doubles are chosen, and how a
test that breaks under refactoring is judged belong to the test map in
[Review and Verification](review-and-verification.md#test-each-element-by-its-role); this document
places those tests in the order. Concrete techniques (annotations,
test libraries, container setup, framework-specific forms) belong to the language and framework rules
loaded together with this skill; the client UI rules own the frontend forms. The plan fields named here
(`Entry point`, `Design decisions`, `Concern check`, `Behavior list`, `Claim (at completion)`) are
filled by the planning skill and completed by the executing skill.

Read this document in full when implementing a feature slice or writing the plan for one.

## Contents

- [Thin Vertical Slices](#thin-vertical-slices)
- [The Base Work Item](#the-base-work-item)
- [Design Decisions and the Behavior List](#design-decisions-and-the-behavior-list)
- [Outer-Loop Red](#outer-loop-red)
- [Top-Down Implementation](#top-down-implementation)
- [The Test Map](#the-test-map)
- [Green and Refactor](#green-and-refactor)
- [Failure Paths](#failure-paths)
- [Completion and the Claim](#completion-and-the-claim)
- [The Pre-Exposure Gate](#the-pre-exposure-gate)
- [Other Entry Points](#other-entry-points)
- [The Concern List](#the-concern-list)

## Thin Vertical Slices

Bundle one use case into one thin slice that passes through every layer from the entry point to the
database, and close each slice inside one work item: the failing test, the implementation, and the
rollback and error response verification. Do not split work by layer (all tables and adapters, then
all services, then all controllers).

A feature plan therefore reads: one base work item, one work item per slice, and the pre-exposure
gate as the last item.

<!-- source: design 2.1 intro -->

## The Base Work Item

Place exactly one base work item before the first slice, and put into it only what several slices
actually share.

- The end-to-end execution base: a real database (a container or a test database), a data cleanup
  rule (per-table reset or per-test unique keys), and one execution configuration shared by every
  end-to-end test (settings, profile, double registration, database preparation). Do not vary the
  execution configuration per test; reset double state per test. The concrete form belongs to the
  language test rules.
- The global exception handler and the error response format. This is the controller-stage contract of
  every slice; the per-API handler that presents a business failure is written in the slice that needs
  it and uses the same response format.
- Shared configuration.
- Items decided once per project. This document names them neutrally and the language rules own the
  concrete values: the time source and the stored time basis, the money type, the association loading
  policy, pool sizes with executor queue limits and default timeouts, where secrets live, the health
  endpoint and graceful shutdown, and validation of configuration objects. In an existing project,
  record the current values instead of deciding them again.
- One machine-check confirmation line: confirm that secret scanning, static analysis, and dependency
  vulnerability checks exist in the project's build or CI, and propose adding them when absent. Do not
  keep a tool candidate list here; propose rather than add, consistent with adding verification tools
  only when asked.
- Database confirmation items, only when the project's database is missing from the framework's
  exception translation table or has no official test container module: whether it can run as a test
  container (otherwise a shared test database with an isolation rule), how a constraint violation is
  translated, the lock wait default, the DDL lock scope, and whether a write that joined an already
  finished transaction gets committed by auto-commit restoration during connection cleanup. Record the
  answers in the language rules, one line each.
- Where transaction propagation lives for after-commit follow-up work is recorded in the language
  rules after the base work item verifies it on the real stack; do not assume it.
- Table SQL is not written here. Write it in the slice that first uses the table; applying SQL first
  is a deployment order, not a development order.

<!-- source: design 2.0 -->

## Design Decisions and the Behavior List

Write these before the first test of the slice, in one place, and record only the decided values in
the plan fields `Entry point`, `Design decisions`, `Concern check`, and `Behavior list`. Do not copy
rule text into the plan.

### Decisions to record

- Entry point: HTTP, scheduler, batch, consumer, listener, or screen. This value determines the shape
  of the outer-loop test and the transaction owner.
- Public boundary: the HTTP contract, the message schema, or the port used by another module. Fix it
  before implementation after a short comparison of alternatives (design it twice), and change it only
  through the compatibility procedure.
- Transaction boundary, failure meaning with error codes, the log points to leave, and the
  authorization check: who may do what to which object and field. Object ownership is checked in the
  application service or a domain policy; feature-level access is checked by method security.
- Failure classification, per failure: a business failure that callers expect and branch on
  (rejection, missing target, conflict) or a technical failure (infrastructure, external call,
  unexpected error). The code form (result value or exception) and the log level follow the
  classification and are set by the language rules.
- External calls: narrow the single atomic unit to the database-changing step and place the external
  call before it or after the boundary has closed, so that no transaction or lock stays open while
  waiting on the outside. When the outside and the inside must agree, do not merely move the call:
  record the state model, the idempotency key, retry, compensation, and the unknown-outcome state in
  the design field, and do not choose the guarantee mechanism (after-commit processing, an outbox, and
  so on) automatically. A write that depends on a value read outside the narrowed boundary uses a
  conditional update or a version check. How the boundary is opened follows the language rules.
- Domain promotion: "none" or "yes (condition number)". When a condition already holds, write the
  domain object from the start. The conditions, judged on the code as it is now:
  1. The same condition or calculation already exists in another use case or entry point, or this
     slice needs it a second time.
  2. It is an invariant that must hold from every entry point.
  3. The allowed state transitions are defined.
  4. A caller must change two or more fields in a fixed order to reach a valid state.
  5. Logic and dependencies are so mixed that testing the rule would need a repository or external
     call double.
  6. A validation, calculation, or derivation has several branches and boundary values.
  7. One value carries dedicated validation, normalization, a unit, or a risk of confusion with
     another value of the same primitive type (a value object).

  Not reasons to promote: likely future reuse, matching a table or query result shape, a plain null
  check or sum, data movement and DTO conversion, another feature being built that way. Start from the
  smallest form: a method on an existing business object, then a value object, then a domain service
  of pure calculation. For the full set of owner candidates (value object, entity, specification,
  domain service, domain event) use the table "Concrete Criteria for Placing Rules" in the
  design-patterns skill. A rule that needs external state (a duplicate check, loading another
  aggregate) stays in the application service even when a condition holds. The business object meant
  here is a separate object, not the persistence mapping entity. On the frontend, add the axis "does
  the server already own this rule" (see Other Entry Points).
- Entry-point specifics: the idempotency key, the retry classification, the chunk size, and the other
  items in the entry-point table.
- Concern check: record each always-on concern as applied, and each change-type trigger as applied or
  intentionally excluded with the reason (see The Concern List).

### The behavior list

In the same place, write the numbered behavior list with normal, failure, boundary, and atomicity
items. Attach one line to each: which partition this test represents, and what a pass guarantees
under which hypothesis. Cover each partition with one example, both sides of each boundary, and zero,
one, and many. Add property tests only where a rule is naturally a short universal statement (money
calculation, sorting and de-duplication, conversion and its inverse, state transitions), and make
impossible states unrepresentable in types instead of testing them. Do not designate as the default a
property-testing library whose maintainers have declined agent use (jqwik has); implement partitions,
boundaries, and small-scope exhaustion with the language's parameterized test facility. Run mutation
testing only on changed core domain code, only when the project has the tool or the user asked for
it, and without a whole-project score target; when the tool is absent, propose it the way the base
work item's machine-check line does, and when it could not run, record that in the Claim as an
unverified risk.

The planning skill writes the initial list. During execution, behaviors discovered while implementing
are appended and marked as added during execution; nothing is removed or weakened silently. Read
[Testing Theory](testing-theory.md) while designing the list when you need the reasoning behind
partitions, hypotheses, and what a passing test lets you claim.

<!-- source: design 2.1 ㄱ -->

## Outer-Loop Red

- Write first one failing acceptance test for the normal flow that passes in one pass from the entry
  point's real stimulus to the real database (the persistence boundary). For HTTP this is an
  end-to-end test from the request to the real database.
- Red means an assertion failure, not a compile error. Write the expected assertion failure message
  before implementing, in the plan item's first TDD step.
- The code shape at the use case entrance (the public method name, the shape of the input and result
  models, how failure is expressed) and the public methods of domain objects are decided at the moment
  the scenario's test is written, and may change later by refactoring within the same code base. How
  failure is expressed follows the language rules' default. The transaction boundary and the failure
  meaning (classification, error code, response status, remaining state) are design values from the
  previous step, and the test asserts them. If a design value looks wrong while the test is being
  written, do not change it: stop and report with evidence. One scenario at a time; do not define
  every interface of the use case up front.
- End-to-end tests per use case: the one normal flow, plus a failure scenario only for what element
  tests cannot prove (rollback and atomicity, the failure log count across layers, and authorization
  denial as one parameterized test), as
  [Review and Verification](review-and-verification.md#what-real-database-end-to-end-tests-prove)
  lists them. Status codes, per-field validation, the error response format, business-rule branches,
  and boundary values belong to the element tests the test map assigns. Decide the failure scenarios
  here; Failure Paths proves them.

<!-- source: design 2.1 ㄴ; end-to-end share from test-isolation-and-layout design 2.2 -->

## Top-Down Implementation

- Order: the top layer of the entry point (the controller for HTTP), then the application service,
  then the domain object when promotion applies, then the persistence adapter (for example a JPA
  repository or a MyBatis mapper). Build in a lower layer only what the layer above actually needs.
- Inner loop: write each element's tests together with the element as implementation descends, as
  the test map in [Review and Verification](review-and-verification.md#the-element-test-map) assigns
  them.
- Programming by intention: write the flow first by calling methods that do not exist yet under
  intention-revealing names, then fill in the empty signatures the compiler and IDE create. Make each
  public method body read as steps at one level of abstraction, and inline a helper that is used once
  and whose name says no more than its body.
- Private helpers and internal collaborators get a name first, are not tested, and may change at any
  time.
- Create an interface only for a real contract: a public boundary, the input contract of a use case
  that an inbound adapter calls, a port for an unmanaged dependency, real polymorphism, or a repository
  contract that hides a storage representation (an entity, a row structure) that the persistence
  technology would otherwise expose in a public signature. Each use case that an inbound adapter calls
  gets a narrow input contract named after that use case and implemented by its service; it is the
  role the adapter depends on, not an interface for tests. When the framework generates the
  implementation of an interface that already exposes only business types, that interface is the
  contract; do not add another on top. Do not create interfaces for transactions or for tests. The
  concrete forms of the repository contract and the use case input contract are set by the language
  rules.
- Forbidden failure modes: creating a collaborator interface for every step of the flow in advance and
  verifying call order with mocks; making a private helper public in order to test it; creating a
  Service and Impl pair for every service, that is, an interface that copies a service class's whole
  method set instead of naming one use case's input.
- Cross-cutting concerns go in as code while their layer is being written, not in a later hardening
  step: the transaction declaration with the application service, technical exception translation
  with the adapter, error response mapping and the failure log with the exception handler (the
  per-API presentation handler for business exceptions, the global handler for failures unrelated to
  business), and the success record after commit.
- The persistence mapping entity is a storage representation only. Business decisions and state
  transitions live in a separate business object, with no exceptions. A mapper that maps query results
  straight into business objects or result records through constructors has no such conflict.
- Table SQL is written in the slice that first uses the table.

<!-- source: design 2.1 ㄷ; interface rules and inner loop from test-isolation-and-layout design 2.7 and 3 -->

## The Test Map

Which tests each element has is decided by the element test map in
[Review and Verification](review-and-verification.md#test-each-element-by-its-role), together with its
rules for helpers, shared components, test doubles and their contract tests, and tests that break
under refactoring. This document only places those tests in the flow: the normal-flow end-to-end test
opens the slice (Outer-Loop Red), each element's tests are written with the element (Top-Down
Implementation), and the failure end-to-end tests close it (Failure Paths).

<!-- source: test-isolation-and-layout design 3 -->

## Green and Refactor

- Make one test runnable at a time. Adjust the step size to confidence: implement directly when the
  path is clear, retreat to a smaller test on an unexpected failure, triangulate with a second example
  when the generalization is uncertain. When the expected result cannot be stated in advance, learn
  with a spike, throw it away, and rewrite with tests. The second-by-second strictness of the three
  laws, the transformation priority premise, and the ZOMBIES order are options, not rules.
- When writing a test, decide only how the code is called (signature, inputs, result, how failure is
  expressed). Decide the implementation structure after the test passes, in refactoring.
- Anti-tampering, stated as text rather than enforced by a mechanism: if a test looks wrong while
  implementing, do not fix it; stop and report with evidence. Never edit, weaken, or disable a test or
  an assertion to make it pass.

<!-- source: design 2.1 ㅁ -->

## Failure Paths

After the normal flow passes, add the failure end-to-end tests decided in Outer-Loop Red to the outer
loop. The always-on concerns are proven inside the slice: here when only an end-to-end test can prove
them, and otherwise by the element test the test map assigns. One failure scenario may carry several
of the end-to-end assertions below.

- Rollback: do not rely on a test transaction (a persistence-slice test's default rollback hides a
  missing service boundary, a deferred flush exception, and after-commit behavior). After the failing
  request, read the database directly and assert that nothing changed. Leave the test method without a
  transaction or turn the test transaction off.
- Error response contract: assert the status code and the error body format in the inbound adapter's
  web slice test, with the exception handlers (per-API and global) inside the slice and the use case's
  input contract doubled to fail with each failure meaning. Of 400, 401, 403, 404, 409, 422, and 500,
  cover the ones that apply to the use case, one representative each.
- Failure log: the expected count comes from the failure classification. A technical failure path
  leaves exactly one log at WARN or above, with the required fields (request id, error code) and no
  secret values. A business failure path leaves none at WARN or above. A failure the framework already
  logs (an after-commit listener exception, a consumer's or batch job's default error handling) counts
  as that one, and the application does not add another. Attach the log assertion to one failure path
  per use case, preferring a technical one, and assert counts and fields, not message strings. The
  language test rules name the capture facility.
- Execution outside the atomic unit and after-commit follow-up: have the fake record whether a real
  transaction was active at the moment it was called, and assert that the external call happened
  outside the atomic unit. Use this assertion only for calls before the atomic unit or after the
  transactional method has returned. Inside after-commit listeners and after-commit synchronization
  callbacks (including the success record) the transaction still reads as active before cleanup, so do
  not use it there; assert the resulting state instead: (1) when the original work rolls back, no
  follow-up effect exists; (2) when it succeeds, the follow-up change exists when read fresh after the
  request has finished; (3) when the follow-up fails after its own write, that partial change does not
  remain and the original change does. Verify after-commit behavior only with the test transaction
  turned off.
- Authorization denial (the one parameterized end-to-end test: unauthenticated 401, another role 403,
  another user's object 403 or 404), duplicate requests (whether an idempotency key is required; the
  409 or 422 response in the web slice test), and integrity constraint violations (exception
  translation in the adapter integration test, the response in the web slice test).
- Concurrent requests: assert the last line of defense (a unique constraint, a conditional update)
  directly and deterministically in the adapter integration test, without threads. An HTTP-level
  concurrent test is optional; when used, start the requests on one start signal so they merely get
  the chance to overlap, and assert only invariants that hold in any completion order (one success,
  the others the designed conflict response, the final state reflected once). A start signal aligns
  departure, not interleaving, so this test is not evidence for the line of defense. Do not add test
  pause points to production code, and do not buy confidence with fixed waits or repetition counts.

<!-- source: design 2.1 ㅂ; response placement from test-isolation-and-layout design 2.2 -->

## Completion and the Claim

Check the completion criteria, then write three lines into the plan item's `Claim (at completion)`
field: the specification items covered, the hypotheses relied on, and the risks not verified. A
passing test proves its specification item only under its hypotheses; the third line is where mutation
testing that did not run, partitions not covered, and environment differences are recorded.

<!-- source: design 2.1 ㅅ -->

## The Pre-Exposure Gate

- Place it as the last work item of the feature plan, after the last slice (or after the single
  slice). It is not where definition-of-done work is deferred to; error handling, tests, transactions,
  logs, access control, idempotency, and integrity constraints all belong in the slices. It is where
  what each slice proved is checked against the whole feature and the operational view.
- The boundary is "before user exposure", not "before production deployment", so it includes checks
  that are possible only after a deployment with no user impact: that dashboards and alerts actually
  show.
- Selection and prerequisites, not a fixed order. One readiness question (does the feature handle
  personal data, money, or irreversible data changes?) selects which items are on. Each item carries
  what must exist before it can be trusted: alerting before automatic rollback, an idempotency judgment
  before retry, instrumentation before load testing, backward compatibility before production
  deployment, an SLO before levels and alert thresholds, a harmless production deployment before
  dashboard and alert verification, alerting before a runbook. The completion check does not accept a
  verification result whose prerequisite is missing as evidence.
- What stays here: cross-feature reconciliation (the per-endpoint authorization table, schema review),
  numbers set by measurement (throughput and size limits, timeout and pool and circuit thresholds),
  and the classification of machine-check results. Do not have the agent regenerate code at the gate.
- Post-release follow-up: numeric tuning that needs real measurements, caching once the need is
  confirmed, cleanup after a migration completes (contracting migrations, flag removal). Record these
  in the plan as revisit triggers (measure what, revisit when), not as work items.
- Deferral test: would attaching it later require changing data, a contract, or code spread across the
  feature? If yes, decide it inside the slice; if no, defer it until after measurement.
- No release-level stabilization or hardening sprint.

<!-- source: design 2.2 -->

## Other Entry Points

The principle does not change: write first the outer-loop test that passes in one pass from the entry
point's real stimulus to the persistence boundary, then descend from that entry point's top layer.
Only four things change per entry point: (1) the shape of the outer-loop test, (2) the top layer,
(3) the transaction owner, and (4) the risk list to decide at design time. The language rules and the
client UI rules own the concrete test forms and tools.

| Entry point | Outer-loop test | Top layer and order | Transaction owner | Decide at design time |
| --- | --- | --- | --- | --- |
| HTTP | End-to-end from the request to the real database | Controller, then service, then domain object when promoted, then persistence adapter | Application service | The list in Design Decisions |
| Frontend feature screen | Enter the route, operate it as a user would, and assert the rendered result, doubling only the network. End-to-end against the real backend only for the app's few core journeys | Route and page, then components and command or query hooks used only by that page (or the page's view model), then a pure domain object only when a real rule exists, then request declarations and the API client (or the repository implementation) | None | The screen state list (initial, loading, empty, success, failure, retry), the rule that maps server error responses to screen states, cache invalidation after changes, the duplicate submission policy, which state the URL owns, log and analytics event points |
| Scheduler (including an outbox relay) | Call the entry method directly at a fixed time from a clock double and assert database state and the external-effect doubles; do not wait for the schedule | Schedule entry method (thin adapter), then the use case service, then below | The use case service; the entry method carries no business transaction | Concurrent runs across instances, duplicate effects on re-run (a lock only prevents concurrent runs; correctness is the state model's job), failure isolation per target, time zone |
| Batch job | Run the job end to end on the real database and the job metadata store with identifying parameters, and assert the exit status, step counts, and result tables | Because reading comes first, decide the item type, chunk size, and restart and skip policies at job design time and implement reading last | The chunk step (the stated exception to "the business transaction belongs to the application service") | Run identification, restart position, duplicate effects when a failed chunk is reprocessed, the skip limit, external calls inside a chunk |
| Message consumer | Publish to a real broker and wait for the database state to assert; in a failure path publish the same message twice and assert it is applied once | Listener (thin adapter), then the use case service, then below | The use case service; a listener that combines a broker transaction with the database transaction is a stated exception | The at-least-once premise and the idempotency key, the order of database commit and offset commit or acknowledgment (keep the processing record in the same database transaction as the business change), which exceptions to retry and which not, dead-letter handling, the broker's default requeue trap; do not duplicate the error log the framework already writes once |
| After-commit event listener | It does not run inside a rolled-back test transaction, so verify with the test transaction off and assert the follow-up by its resulting state (see Failure Paths) | Listener (thin adapter), then the use case, then below | A new transaction for the use case the listener calls. In the after-commit phase the default propagation joins the finished transaction and does not commit, so the place to set propagation must be decided; it is recorded in the language rules after the base work item verifies it | The publish moment (after commit); compensation or reprocessing, because a listener exception does not reach the publisher; one extra connection when synchronous (pool size); the executor queue limit and loss handling when asynchronous |

Frontend supplement, principles only (the client UI rules own the forms): add to the promotion
conditions the axis "does the server already own this rule". When it does, the client keeps only form
guidance validation, preview calculation, offline behavior, and screen state transitions, and reuses
the server's computed result. Promote a shared UI component only when a second page needs it with the
same meaning and the same direction of change. Only work whose product is the reusable part itself (a
design system, a shared UI kit) proceeds bottom-up. Close the slice with failure paths and
accessibility.

<!-- source: design 2.3 -->

## The Concern List

Write each item as a name, a one-line action, and a verification method, not as prose. This document
owns the meaning; the language rules and the client UI rules own the concrete techniques. The list has
four columns.

- Always on (every use case; decided at design time and proven inside the slice by failure-path
  tests): authorization (who may do what to which object and field; object ownership in the
  application service or a domain policy, feature level by method security; tests that request as
  another user, as another role, and unauthenticated); domain values and concurrency invariants
  (negatives, ranges, and state transitions; limits and balances; a unique constraint and a
  conditional update as the last line of defense, with their interpretation asserted directly in the
  adapter integration test); the meaning of a duplicate request (whether an idempotency key is
  required; 409 or 422); data integrity constraints (in the first migration; translation of a
  violation in the adapter integration test on the real database, the response in the web slice
  test); the failure meaning of external calls (a timeout exists and
  has an initial value, unknown outcomes are handled, retry only after the idempotency judgment and
  outside the transaction); secrets only through configuration; input sinks (no string substitution
  into queries, path normalization, structured log fields).
- Change-type triggers (on only when they apply; the plan records each as applied or intentionally
  excluded with the reason): a table or column change: the compatibility grade and the number of
  deployments (expand, then contract), old-code compatibility on rollback, the index together with the
  query. A new external call: the timeout value, retry and idempotency, a fault-injection test. Money,
  points, or state changes: the locking approach, the audit trail (history before its introduction
  cannot be recovered), metrics. Authentication or personal data: encrypted fields, access logs,
  masking. A new public endpoint: input limits, whether a rate limit is needed, the error format. Lists
  and bulk processing: the paging contract (method, count, size limit, sort key), an assertion that the
  query count does not grow with the item count, the execution plan. Scheduled work: duplicate runs
  across instances. A feature where the server calls a user-supplied URL: an SSRF allow list. A
  security setting change: the recorded reason for turning a default (such as CSRF protection) off.
- Once per project: the base work item's list.
- Machine checks (kept out of this list; the project's CI owns them): secret scanning, static analysis
  (injection sinks, cryptographic APIs, threading patterns, resource leaks), dependency
  vulnerabilities, a search for string-substitution markers in query templates. This skill keeps only
  the base work item's confirmation line.
- Left to the pre-exposure gate: that item's list.

<!-- source: design 2.4 -->
