# Testing and Verification Rules

## Table of contents

- [Core testing principles](#core-testing-principles)
- [Tests by layer](#tests-by-layer)
- [Fixtures and determinism](#fixtures-and-determinism)
- [Compatibility tests](#compatibility-tests)
- [Tool inspection and verification execution](#tool-inspection-and-verification-execution)

## Core testing principles

<a id="test-001"></a>
### Follow existing testing tools and conventions

**TEST-001 · MUST**

Follow the project's existing JUnit, AssertJ, Mockito, Testcontainers, fixture, test-naming, and Given–When–Then or Arrange–Act–Assert conventions. Do not change a major version or testing framework solely to apply code style.

Name a test to express its condition and expected behavior, such as `cannotRedeemExpiredCoupon` or the established project form `cannot_redeem_expired_coupon`. Do not mix both styles arbitrarily within one area. Use `@DisplayName` only when a natural-language explanation adds value.

<a id="test-002"></a>
### Test observable business behavior

**TEST-002 · MUST**

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

<a id="test-005"></a>
### Verify interactions when side effects are the contract

**TEST-005 · SHOULD**

Verify an interaction when the side effect itself is the contract, such as Repository persistence or message delivery. Do not overconstrain internal mapper and helper call order or add `verifyNoMoreInteractions()` mechanically to every test.

<a id="test-008"></a>
### Prioritize important behavior over coverage numbers

**TEST-008 · SHOULD**

Prioritize important Domain branches, authorization, state transitions, boundary values, retry and duplication, external contracts, and database queries over a coverage number. Do not inflate coverage with getter or Lombok tests. When an exception message is not a public contract, verify its type and business-relevant properties rather than the entire string.

## Tests by layer

<a id="test-003"></a>
### Test each responsibility at its owning layer

**TEST-003 · MUST**

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

<a id="test-004"></a>
### Use real domain objects and mock actual boundaries

**TEST-004 · MUST NOT**

Do not mock a plain business object, Value Object, or input/result DTO. Use real value objects and test fixtures. Limit mocks to real boundaries such as a Repository, Port, Clock, or identifier generator.

## Fixtures and determinism

<a id="test-006"></a>
### Keep test fixtures from weakening production encapsulation

**TEST-006 · MUST**

Repeated valid-object construction may be organized in a test-only fixture or builder. Do not hide an important boundary value in a fixture default; expose it in the test. Do not add a public constructor, setter, or bypass method to production code for test convenience.

<a id="test-007"></a>
### Make tests deterministic and independent

**TEST-007 · MUST**

- Do not create current time or random identifiers directly in tests; use fixed values or the existing Clock or generator Port.
- Use condition polling or synchronization instead of a fixed sleep.
- Do not depend on execution order or database data created by another test.
- Do not use a shared mutable static fixture.
- Clean up modified system properties, files, and database state.
- Account for parallel execution and data contamination.

## Compatibility tests

<a id="test-009"></a>
### Use compatibility comparisons when replacing a system

**TEST-009 · MAY**

Use the following conditionally when replacing an existing system or reimplementing the same API:

- A Characterization Test recording pre-change behavior
- An approved Golden Master for a complex response or file
- A Differential Test comparing existing and new APIs or query results
- A result-equivalence test between existing SQL and new JPA, QueryDSL, or SQL

Do not add a Golden Master mechanically to an ordinary new feature. For a large contract, compare representative successful, error, null, sorting, pagination, session, file, and scheduled-execution scenarios.

## Tool inspection and verification execution

<a id="tooling-001"></a>
### Inspect the module's build and verification setup

**TOOLING-001 · MUST**

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

<a id="tooling-002"></a>
### Use project wrappers and established verification commands

**TOOLING-002 · MUST**

Prefer the project wrapper, such as `./mvnw` or `./gradlew`, and established formatter, lint, and test commands. Do not produce different results with a system-global tool.

<a id="tooling-003"></a>
### Add verification tools only when requested

**TOOLING-003 · MUST NOT**

Do not add Checkstyle, Spotless, PMD, SpotBugs, Error Prone, NullAway, ArchUnit, a Sonar plugin, JaCoCo, or mutation testing to the build without a user request. Treat changes to build time, baseline, CI, and IDE behavior as separate decisions.

<a id="tooling-004"></a>
### Check search results in their code context

**TOOLING-004 · MUST**

Use text search such as `rg` to find candidate occurrences of `record`, `var`, `@Data`, or `@Setter`. Inspect comments, strings, generated code, access scope, and usage context before deciding that an occurrence violates a rule. Do not add a custom regular-expression linter to this skill.

<a id="tooling-005"></a>
### Choose focused Java verification by risk

**TOOLING-005 · MUST**

Run the narrowest existing checks that exercise the changed Java or framework contract. Choose the necessary combination of unit tests, compilation, formatting/static analysis, Spring context checks, HTTP binding tests, and repository integration tests. Broaden only for a concrete unverified risk or an explicitly required check.

Do not run the repository-wide suite or full build by default, and do not repeat a passing command unless relevant inputs changed. A real JPA mapping or JSON binding change needs evidence for that boundary, not just a mocked service test.

Classify failures as change-caused, pre-existing, environment/permission related, missing service/database, transient network, or incorrect command. Fix the cause or explain the gap instead of repeating the same failed approach. Resolve new warnings in scope without introducing a new -Werror policy.

<a id="tooling-006"></a>
### Keep suppressions narrow and justified

**TOOLING-006 · MUST**

Do not use `@SuppressWarnings("all")` or a broad Checkstyle exclusion. When an external constraint requires suppression, apply it to the narrowest class, method, or statement and state the reason and reconsideration condition.

<a id="tooling-007"></a>
### Change generator inputs instead of generated code

**TOOLING-007 · MUST NOT**

Do not edit generated QueryDSL Q-types, OpenAPI, Protobuf, JOOQ, or similar output directly. Modify the source schema or generator configuration and exclude only the required generated path from static analysis.
