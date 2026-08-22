# Testing and Verification Rules

## Table of contents

- [Core testing principles](#core-testing-principles)
- [Tests by layer](#tests-by-layer)
- [Fixtures and determinism](#fixtures-and-determinism)
- [Compatibility tests](#compatibility-tests)
- [Tool inspection and verification execution](#tool-inspection-and-verification-execution)

## Core testing principles

### TEST-001 — MUST

Follow the project's existing JUnit, AssertJ, Mockito, Testcontainers, fixture, test-naming, and Given–When–Then or Arrange–Act–Assert conventions. Do not change a major version or testing framework solely to apply code style.

Name a test to express its condition and expected behavior, such as `cannotRedeemExpiredCoupon` or the established project form `cannot_redeem_expired_coupon`. Do not mix both styles arbitrarily within one area. Use `@DisplayName` only when a natural-language explanation adds value.

### TEST-002 — MUST

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

### TEST-005 — SHOULD

Verify an interaction when the side effect itself is the contract, such as Repository persistence or message delivery. Do not overconstrain internal mapper and helper call order or add `verifyNoMoreInteractions()` mechanically to every test.

### TEST-008 — SHOULD

Prioritize important Domain branches, authorization, state transitions, boundary values, retry and duplication, external contracts, and database queries over a coverage number. Do not inflate coverage with getter or Lombok tests. When an exception message is not a public contract, verify its type and business-relevant properties rather than the entire string.

## Tests by layer

### TEST-003 — MUST

Verify behavior at the layer that owns the responsibility.

#### Domain

Verify invariants, state transitions, and Value Objects with pure unit tests that do not start a Spring context.

#### Application

Replace actual boundaries such as Repositories, authorization Policies, and external Ports. Verify lookup, authorization result application, Domain behavior, persistence, external effects, returned results, and absence of side effects on failure.

#### Controller

Verify URL, HTTP method, deserialization, Bean Validation, authentication boundary, input conversion, JSON Response, and Exception Handler translation. Do not duplicate the entire set of Domain rules.

#### Repository and Query

Verify JPA mappings, cascading, QueryDSL joins and projections, Native SQL, database constraints, sorting and pagination, dates and nulls, database functions, and bulk affected-row counts with meaningful persistence integration tests. Do not prove production-database-specific syntax with H2 alone.

#### External Adapter

Verify local-input-to-provider-Request conversion, provider-Response-to-local-Result conversion, error, nullable, date, and numeric handling, timeout wiring, retry classification, and non-exposure of sensitive data. Do not let an ordinary unit test call a live provider.

#### Scheduler and Batch

For a Scheduler, verify reference time, Context, Use Case invocation, and outermost failure policy; do not wait for a cron time with sleep. For Batch, verify Job Parameters, scope, chunks, restart, duplication, retry, skip, partial failure, and affected-row counts.

### TEST-004 — MUST NOT

Do not mock a Domain Entity, Value Object, Command, or Result DTO. Use real value objects and test fixtures. Limit mocks to real boundaries such as a Repository, Port, Clock, or identifier generator.

## Fixtures and determinism

### TEST-006 — MUST

Repeated valid-object construction may be organized in a test-only fixture or builder. Do not hide an important boundary value in a fixture default; expose it in the test. Do not add a public constructor, setter, or bypass method to production code for test convenience.

### TEST-007 — MUST

- Do not create current time or random identifiers directly in tests; use fixed values or the existing Clock or generator Port.
- Use condition polling or synchronization instead of a fixed sleep.
- Do not depend on execution order or database data created by another test.
- Do not use a shared mutable static fixture.
- Clean up modified system properties, files, and database state.
- Account for parallel execution and data contamination.

## Compatibility tests

### TEST-009 — MAY

Use the following conditionally when replacing an existing system or reimplementing the same API:

- A Characterization Test recording pre-change behavior
- An approved Golden Master for a complex response or file
- A Differential Test comparing existing and new APIs or query results
- A result-equivalence test between existing SQL and new JPA, QueryDSL, or SQL

Do not add a Golden Master mechanically to an ordinary new feature. For a large contract, compare representative successful, error, null, sorting, pagination, session, file, and scheduled-execution scenarios.

## Tool inspection and verification execution

### TOOLING-001 — MUST

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

### TOOLING-002 — MUST

Prefer the project wrapper, such as `./mvnw` or `./gradlew`, and established formatter, lint, and test commands. Do not produce different results with a system-global tool.

### TOOLING-003 — MUST NOT

Do not add Checkstyle, Spotless, PMD, SpotBugs, Error Prone, NullAway, ArchUnit, a Sonar plugin, JaCoCo, or mutation testing to the build without a user request. Treat changes to build time, baseline, CI, and IDE behavior as separate decisions.

### TOOLING-004 — MUST

Use text search such as `rg` to find candidate occurrences of `record`, `var`, `@Data`, or `@Setter`. Inspect comments, strings, generated code, access scope, and usage context before deciding that an occurrence violates a rule. Do not add a custom regular-expression linter to this skill.

### TOOLING-005 — MUST

Select the required scope from this sequence according to risk and cost:

```text
Relevant unit tests
→ Target module tests
→ Formatter and lint
→ Compilation
→ Required integration tests
→ Full build when risk warrants it
```

Do not finish a persistence or API-contract change with one narrow unit test. Classify a failure as caused by the current change, pre-existing, environment or permission related, a missing dependency service or database, transient network failure, or an incorrect command or input. Do not repeat the same failed approach without new evidence.

For a pre-existing failure, report the command, failed target, evidence that it is unrelated to the current change, and the remaining verification gap. Resolve a new warning caused by the current change, but do not introduce `-Werror` merely because the project already has many warnings.

### TOOLING-006 — MUST

Do not use `@SuppressWarnings("all")` or a broad Checkstyle exclusion. When an external constraint requires suppression, apply it to the narrowest class, method, or statement and state the reason and reconsideration condition.

### TOOLING-007 — MUST NOT

Do not edit generated QueryDSL Q-types, OpenAPI, Protobuf, JOOQ, or similar output directly. Modify the source schema or generator configuration and exclude only the required generated path from static analysis.
