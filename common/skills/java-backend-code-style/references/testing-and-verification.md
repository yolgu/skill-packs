# Testing and Verification Rules

## Table of contents

- [Core testing principles](#core-testing-principles)
- [Tests by layer](#tests-by-layer)
- [Feature flow test forms](#feature-flow-test-forms)
- [Fixtures and determinism](#fixtures-and-determinism)
- [Compatibility tests](#compatibility-tests)
- [Tool inspection and verification execution](#tool-inspection-and-verification-execution)

## Core testing principles

### Follow existing testing tools and conventions

**MUST**

Follow the project's existing JUnit, AssertJ, Mockito, Testcontainers, fixture, test-naming, and Given–When–Then or Arrange–Act–Assert conventions. Do not change a major version or testing framework solely to apply code style.

Name a test to express its condition and expected behavior, such as `cannotRedeemExpiredCoupon` or the established project form `cannot_redeem_expired_coupon`. Do not mix both styles arbitrarily within one area. Use `@DisplayName` only when a natural-language explanation adds value.

### Test observable business behavior

**MUST**

Verify observable business behavior rather than implementation details.

Prioritize:

- State transitions and invariants
- Authorization allowance and denial
- Persistence and external side effects
- Empty results, boundary values, and stable ordering
- Re-execution and duplicate effects
- API JSON, status, and error contracts

Avoid:

- Invocation counts for private helpers
- Counts of QueryDSL helpers created
- Simple getters and Lombok-generated code
- Internal local-variable ordering

Make one test verify one business scenario. Multiple assertions describing one result are acceptable; separate success, failure, and boundary scenarios.

### Verify interactions when side effects are the contract

**SHOULD**

Verify an interaction only for an outgoing command: a call that changes state behind an outward Port (message delivery, an outgoing call) or behind an owned neighbour role interface (a Repository contract's write, another Use Case's input contract). Verify it with Mockito `verify` or by asserting what a recording fake captured. Stub queries and never verify them. Asserting stored state by reading the real database belongs to the persistence adapter's contract test and to the end-to-end tests. Do not overconstrain internal mapper and helper call order or add `verifyNoMoreInteractions()` mechanically to every test.

### Prioritize important behavior over coverage numbers

**SHOULD**

Prioritize important Domain branches, authorization, state transitions, boundary values, retry and duplication, external contracts, and database queries over a coverage number. Do not inflate coverage with getter or Lombok tests. When an exception message is not a public contract, verify its type and business-relevant properties rather than the entire string.

## Tests by layer

### Test each responsibility at its owning layer

**MUST**

Verify behavior at the layer that owns the responsibility, following the element test map of the code-principles review and verification document. This section owns its Java and Spring forms.

#### Domain

Verify invariants, state transitions, and Value Objects with pure unit tests that do not start a Spring context.

#### Application

Unit-test an application service through its public methods, without a Spring context, with Mockito doubles for its immediate-neighbour role interfaces: Repository contracts, Ports, and other Use Cases' input contracts. Use real Domain objects, Value Objects, input and result DTOs, the helpers only this service uses, and deterministic shared calculation components. The business-rule branches are asserted here.

#### Controller

Write a web slice test with `@WebMvcTest` that loads the controller with its API-specific and global exception handlers, and replace the Use Case input contract with `@MockitoBean`. Assert the URL and HTTP method mapping, deserialization, Bean Validation per field, input conversion, the JSON Response, and the handlers' translation of each failure meaning into its status code and error body format, and verify the command sent to the Use Case. Do not duplicate the Domain rules here.

#### Repository and Query

Integration-test each persistence adapter (a JPA repository or a MyBatis mapper) against the real database as the contract test of every repository method a service test doubles: assert that method's meaning there (the value returned when nothing matches, ordering, affected-row counts). The same tests cover (1) queries with their own logic (QueryDSL joins and projections, Native SQL, database functions, sorting and pagination, dates and nulls, bulk affected-row counts) and (2) the interpretation of the last line of defense: a constraint violation translated into the defined failure meaning with the same error code the pre-check path reports, and zero affected rows on a conditional update read as a conflict. Do not prove production-database-specific syntax with H2 alone.

#### External Adapter

Integration-test the adapter against a stand-in HTTP server as the contract test of the Port that service tests double. Verify local-input-to-provider-Request conversion, provider-Response-to-local-Result conversion, error, nullable, date, and numeric handling, timeout wiring, retry classification, and non-exposure of sensitive data. Do not let an ordinary unit test call a live provider.

#### Scheduler, Batch, consumer, and listener entry points

Test entry code that calls a Use Case narrowly, with that Use Case's input contract replaced by a Mockito double: a Scheduler entry method, a Kafka or RabbitMQ listener, an after-commit event listener, or a Batch step component that delegates to a Use Case. Call it directly, with a fixed `Clock` double where time matters, and verify the reference time, Context, the command sent to the Use Case, and the outermost failure policy; do not wait for a cron time with sleep. The outer-loop test of each entry point follows the entry-point table below: the scheduler test there asserts the resulting database state, and the Batch Job runs end to end with Job Parameters, scope, chunks, restart, duplication, retry, skip, partial failure, and affected-row counts verified.

#### End-to-end

Write the real-database end-to-end tests (a Testcontainers container or a dedicated test database, with the exception handlers in the context) for the normal flow and for the failures only they can prove, in the forms of Feature flow test forms below.

### Double owned role interfaces and pair each with a contract test

**MUST**

Double a role interface the system owns when it is the immediate neighbour of the code under test: a Repository contract, a Port, or another Use Case's input contract; stub and verify it as "Verify interactions when side effects are the contract" describes. Do not mock a plain business object, Value Object, input/result DTO, concrete class, or third-party SDK type; when a concrete class seems to need a mock, expose that relationship as an interface. Supply time and identifiers through their Ports with fixed values. Give every doubled interface a contract test that runs its real implementation: the persistence adapter's real-database integration test for a Repository contract, the stand-in server integration test for an external Port, and the service's own tests for a Use Case input contract.

## Feature flow test forms

The language-agnostic flow (slice order, failure paths, the pre-exposure gate) is owned by the code-principles feature implementation flow document, and the element test map, the test double rules, and the judgment of tests that break under refactoring are owned by its review and verification document ("Test Each Element by Its Role"). This section owns their Java and Spring forms.

### Share one end-to-end execution base

**MUST**

Keep one shared execution configuration for every end-to-end test: a common abstract base class or one composed meta-annotation that carries the profile, properties, and bean replacements, so that the Spring context cache serves all of them. Do not use `@DirtiesContext`. Register containers as beans or hold them in a static singleton; do not use a static `@Container` field with the JUnit extension, because a cached context would keep referencing a container the extension has already stopped. Container reuse is a local convenience, not a rule. Declare `@MockitoBean` in the base class under one field name so the context key stays identical. Clean data per table or use per-test unique keys, and reset double state before each test.

When the project's database is missing from Spring's SQL error code table (`sql-error-codes.xml`) or has no official Testcontainers module (CUBRID is an example), the base work item confirms before the first slice: whether it runs as a test container or needs a shared test database with an isolation rule, which exception a unique constraint violation translates to, the lock wait default, the DDL lock scope, and whether a write that joined an already finished transaction is committed by auto-commit restoration during connection cleanup. Record each result here as one line.

### Choose the outer-loop test by entry point

**MUST**

| Entry point | Outer-loop test |
|---|---|
| HTTP | End-to-end from the request through the exception handlers to the real database |
| Scheduler | Call the entry method directly with a fixed `Clock` double and assert the database state and the external-effect fakes; never wait for a cron time |
| Spring Batch | Run the Job end to end on the real database and the JDBC job repository with identifying parameters through Spring Batch 6's `JobOperatorTestUtils`, and assert exit status, Step counts, and result tables. The default in-memory repository of 6.0 keeps no metadata, so restart scenarios need the JDBC repository |
| Kafka or RabbitMQ consumer | Publish to a real broker (a Testcontainers broker, or Kafka's embedded KRaft broker; RabbitMQ has no embedded broker) and wait for the database state with Awaitility. In a failure path publish the same message twice and assert a single effect |
| After-commit event listener | It is not invoked inside a rolled-back test transaction; run with the test transaction off and assert the follow-up by its resulting state |

### Prove failure paths at the outer boundary

**MUST**

- Rollback: leave the test method without a transaction or declare `@Transactional(propagation = NOT_SUPPORTED)` on it, then read the database directly after the failing request and assert that nothing changed. Do not rely on a test transaction's rollback.
- Error response: the status code and the error body format are asserted in the controller's web slice test (see Tests by layer), not in the end-to-end failure tests.
- Failure log: capture with a Logback `ListAppender` attached to the relevant logger or with Spring Boot's `OutputCaptureExtension`, and assert counts and fields, not message text. The expected count follows the failure classification in [Errors, logging, and configuration](errors-logging-and-configuration.md): a technical failure path logs exactly one entry at WARN or above, a business failure path logs none, and a failure the framework already logs counts as that one.
- Execution outside the atomic unit: let the fake record `TransactionSynchronizationManager.isActualTransactionActive()` at call time and assert that it was false. Use this only for calls before the atomic unit or after the transactional method has returned. Inside an after-commit listener or an after-commit synchronization callback it still returns true before cleanup, so do not assert it there; assert the resulting state instead: no follow-up effect when the original work rolled back, the follow-up change readable after the request when it committed, and no partial follow-up change when the follow-up failed after its own write while the original change remains.
- Authorization denial: one `@ParameterizedTest` whose rows are the requesting principal and the expected status (unauthenticated 401, another role 403, another user's object 403 or 404 by project rule).
- Concurrency: prove the last line of defense (unique constraint, conditional update) in the adapter integration test without threads. An HTTP-level concurrent test is optional; release the requests on one `CountDownLatch`, assert only invariants that hold in any completion order, and do not add pause points to production code or buy confidence with fixed sleeps or repetition counts.

## Fixtures and determinism

### Keep test fixtures from weakening production encapsulation

**MUST**

Repeated valid-object construction may be organized in a test-only fixture or builder. Do not hide an important boundary value in a fixture default; expose it in the test. Do not add a public constructor, setter, or bypass method to production code for test convenience.

### Make tests deterministic and independent

**MUST**

- Do not create current time or random identifiers directly in tests; use fixed values or the existing Clock or generator Port.
- Use condition polling or synchronization instead of a fixed sleep.
- Do not depend on execution order or database data created by another test.
- Do not use a shared mutable static fixture.
- Clean up modified system properties, files, and database state.
- Account for parallel execution and data contamination.
- In a concurrent test, a start latch only aligns departure and does not guarantee interleaving; set a lock wait timeout so that a blocked request fails instead of hanging.

## Compatibility tests

### Use compatibility comparisons when replacing a system

**MAY**

Use the following conditionally when replacing an existing system or reimplementing the same API:

- A Characterization Test recording pre-change behavior
- An approved Golden Master for a complex response or file
- A Differential Test comparing existing and new APIs or query results
- A result-equivalence test between existing SQL and new JPA, QueryDSL, or SQL

Do not add a Golden Master mechanically to an ordinary new feature. For a large contract, compare representative successful, error, null, sorting, pagination, session, file, and scheduled-execution scenarios.

## Tool inspection and verification execution

### Inspect the module's build and verification setup

**MUST**

Before modifying or reviewing code, inspect the target module and the following files and systems:

```text
pom.xml
build.gradle / build.gradle.kts
settings.gradle
gradle.properties
.editorconfig
Checkstyle / Spotless / PMD / SpotBugs / Error Prone
ArchUnit
CI Workflow
IDE Formatter
Annotation Processor and generated-code paths
```

Identify the Java target, formatter, import order, prohibited APIs, Lombok and QueryDSL generation, test commands, generated-code exclusions, and CI gates.

### Use project wrappers and established verification commands

**MUST**

Prefer the project wrapper, such as `./mvnw` or `./gradlew`, and established formatter, lint, and test commands. Do not produce different results with a system-global tool.

### Name tests by whether they need a real target

**SHOULD**

End the class name of a test that needs no real target in `Test`, and that of a test that needs a real database, broker, or container (adapter integration tests and end-to-end tests) in `IT`, so the two kinds run separately without a second test source root. With Failsafe declared in the build, Maven's default patterns already split them: Surefire runs `**/Test*.java`, `**/*Test.java`, `**/*Tests.java`, and `**/*TestCase.java`, and Failsafe runs `**/IT*.java`, `**/*IT.java`, and `**/*ITCase.java` and judges their result in the `verify` phase, so integration environment teardown still runs after a failure. In Gradle, give each kind its own `Test` task with a class-name include or exclude pattern.

### Add verification tools only when requested

**MUST NOT**

Do not add Checkstyle, Spotless, PMD, SpotBugs, Error Prone, NullAway, ArchUnit, a Sonar plugin, JaCoCo, or mutation testing to the build without a user request. Treat changes to build time, baseline, CI, and IDE behavior as separate decisions.

### Check search results in their code context

**MUST**

Use text search such as `rg` to find candidate occurrences of `record`, `var`, `@Data`, or `@Setter`. Inspect comments, strings, generated code, access scope, and usage context before deciding that an occurrence violates a rule. Do not add a custom regular-expression linter to this skill.

### Choose focused Java verification by risk

**MUST**

Run the narrowest existing checks that exercise the changed Java or framework contract. Choose the necessary combination of unit tests, compilation, formatting/static analysis, Spring context checks, HTTP binding tests, and repository integration tests. Broaden only for a concrete unverified risk or an explicitly required check.

Do not run the repository-wide suite or full build by default, and do not repeat a passing command unless relevant inputs changed. A real JPA mapping or JSON binding change needs evidence for that boundary, not just a mocked service test.

Classify failures as change-caused, pre-existing, environment/permission related, missing service/database, transient network, or incorrect command. Fix the cause or explain the gap instead of repeating the same failed approach. Resolve new warnings in scope without introducing a new -Werror policy.

### Keep suppressions narrow and justified

**MUST**

Do not use `@SuppressWarnings("all")` or a broad Checkstyle exclusion. When an external constraint requires suppression, apply it to the narrowest class, method, or statement and state the reason and reconsideration condition.

### Change generator inputs instead of generated code

**MUST NOT**

Do not edit generated QueryDSL Q-types, OpenAPI, Protobuf, JOOQ, or similar output directly. Modify the source schema or generator configuration and exclude only the required generated path from static analysis.
