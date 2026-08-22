---
name: java-backend-code-style
description: Apply project-aware Java backend source-code rules when writing, modifying, refactoring, or reviewing Java code, including HTTP and DTO boundaries, domain and authorization logic, Spring components, JPA, QueryDSL, SQL, adapters, errors, logging, configuration, and tests.
---

# Java Backend Code Style

## Workflow

1. Classify the request as implementation, modification, refactoring, or review, and establish the permitted change scope.
2. Before changing code, inspect the target module's Java version, build files, formatter, static analysis, package structure, naming conventions, test style, and generated-code paths.
3. Trace the target behavior to its definition and every usage, then identify the single source of truth among API contracts, domain rules, schemas, configuration, constants, and tests.
4. Read the [rule index](references/rule-index.md), then read only the references required for the task, in full.
5. Apply the relevant rules while preserving the project's established structure and contracts. Introduce a new abstraction only for a real boundary or duplication that existing concepts cannot resolve.
6. For an implementation request, modify the necessary code and tests. For a review request, do not modify files without separate user authorization.
7. Run the narrowest relevant verification first, then expand to module tests, formatting, static analysis, compilation, and integration tests according to risk.
8. Report the outcome, material decisions, retained compatibility exceptions, completed verification, and remaining verification gaps concisely.

## Reference selection

Read the [rule index](references/rule-index.md) for every task. Use the following table to select additional references. Once selected, read each reference completely rather than skimming part of it.

| Task | References to read |
|---|---|
| Any Java source creation or modification | [Java language and Lombok](references/java-language-and-lombok.md), [object and method style](references/object-and-method-style.md) |
| Controller, HTTP DTO, or Jackson work | [HTTP, DTO, and JSON](references/http-dto-and-json-style.md) |
| Entity, Value Object, domain policy, or authorization work | [Domain and authorization](references/domain-and-authorization-style.md) |
| JPA, Repository, QueryDSL, or Native SQL work | [Persistence and queries](references/persistence-jpa-querydsl-and-sql.md) |
| Use Case, Spring Bean, transaction, external integration, Scheduler, or Batch work | [Spring boundaries and adapters](references/spring-boundaries-and-adapters.md) |
| Exception, HTTP Handler, logging, configuration, or Secret work | [Errors, logging, and configuration](references/errors-logging-and-configuration.md) |
| Test creation or code-change verification | [Testing and verification](references/testing-and-verification.md) |
| Refactoring, compatibility code, public contracts, or review | [Compatibility and change scope](references/compatibility-and-change-scope.md) |
| A complete cross-layer example is needed | [Examples](references/examples.md) |

Apply Spring, JPA, QueryDSL, Jackson, Lombok, and Spring Batch rules only when the target project actually uses the corresponding technology.

## Conflict resolution

Resolve conflicting rules in this order:

1. The business behavior and explicit constraints requested by the user
2. Existing external API, data, and operational compatibility
3. Project build, formatter, naming, and test rules
4. Domain invariants and data integrity
5. Security and sensitive-data protection
6. This skill's `MUST` and `MUST NOT` rules
7. `SHOULD` and `SHOULD NOT` rules
8. `MAY` rules

Do not silently reproduce an obvious security vulnerability or data-loss risk for compatibility. Explain the risk and available choices to the user, then act within the authorized scope.

## Application principles

- Apply every relevant `MUST` and `MUST NOT` rule to new code.
- Improve only violations directly related to the requested change when modifying existing code.
- Do not mass-clean unrelated legacy violations or move packages broadly.
- Do not impose a new package tree. Follow the current project's established package-by-feature or package-by-layer structure consistently.
- Do not mix synonymous conventions such as `controller/presentation`, `service/application`, or `repository/persistence` within the same scope.
- When an external contract requires behavior that differs from a general rule, isolate it as a `COMPATIBILITY EXCEPTION` at the narrowest adapter boundary and track its rationale, scope, verification, and reconsideration condition.
- Do not edit generated code directly. Modify its source schema or generator configuration.

## Verification and reporting

Prefer the project's wrapper and established commands. Classify failures as caused by the current change, pre-existing, environment or permission related, missing dependency service or database, transient network failure, or an incorrect command. Do not repeat the same failed approach without new evidence.

For reviews, include the rule ID, strength, location, actual impact, recommended correction, and compatibility risk. For implementations, include the changed behavior and boundary, test and build results, retained exceptions, and verification that could not be completed.
