# Rule Index

Rule strengths are `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, and `COMPATIBILITY EXCEPTION`. Follow the linked reference for detailed decisions and exceptions.

## Table of contents

- [Java language, formatting, and Lombok](#java-language-formatting-and-lombok)
- [Objects, methods, naming, and packages](#objects-methods-naming-and-packages)
- [HTTP, DTO, and JSON](#http-dto-and-json)
- [Domain, validation, and authorization](#domain-validation-and-authorization)
- [JPA, QueryDSL, and SQL](#jpa-querydsl-and-sql)
- [Use Cases, Spring, external boundaries, and operational entry points](#use-cases-spring-external-boundaries-and-operational-entry-points)
- [Exceptions, logging, configuration, and documentation](#exceptions-logging-configuration-and-documentation)
- [Testing, tooling, and change scope](#testing-tooling-and-change-scope)

## Java language, formatting, and Lombok

| ID | Strength | Summary | Details |
|---|---|---|---|
| JAVA-001 | MUST | Use the project toolchain and runtime as the source of truth for available Java features. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-002 | MUST NOT | Do not begin a `javax` or `jakarta` migration solely as a code-style task. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-003 | MUST NOT | Do not use Java `record`. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-004 | MUST NOT | Do not use Java `var` or Lombok `val` and `var`. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-005 | MUST | Use preview features only when the project explicitly enables and supports them. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-006 | MUST | Use explicit types for local variables. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-007 | SHOULD | Make dependencies, constants, and immutable fields `final` without mechanically requiring `final` on every parameter and local variable. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-008 | MUST | Use types for time, money, character sets, enums, and collections that preserve meaning and precision. | [Java language and Lombok](java-language-and-lombok.md) |
| JAVA-009 | MUST | Establish the reference time and identifiers for a business decision at the execution boundary and pass them inward. | [Java language and Lombok](java-language-and-lombok.md) |
| FORMAT-001 | MUST | Prefer the project formatter, static analysis, and EditorConfig. | [Java language and Lombok](java-language-and-lombok.md) |
| FORMAT-002 | SHOULD | Use the agreed fallback formatting when the project defines no rule. | [Java language and Lombok](java-language-and-lombok.md) |
| FORMAT-003 | MUST | Use braces and prohibit wildcard imports. | [Java language and Lombok](java-language-and-lombok.md) |
| FORMAT-004 | SHOULD | Use line wrapping and blank lines to reveal the business flow. | [Java language and Lombok](java-language-and-lombok.md) |
| FORMAT-005 | MUST | Avoid unrelated whole-file formatting and direct edits to generated code. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-001 | MUST NOT | Do not add Lombok solely to apply code style. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-002 | SHOULD | Limit `@Getter` and `@RequiredArgsConstructor` to public contracts and straightforward injection. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-003 | MAY | Use restricted framework constructors and the project's `@Slf4j` convention when applicable. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-004 | SHOULD NOT | Do not use a builder as the default construction mechanism for Domain, JPA, or Spring Bean types. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-005 | MUST NOT | Do not use `@Data`, class-level `@Setter`, `@SneakyThrows`, or chained setters. | [Java language and Lombok](java-language-and-lombok.md) |
| LOMBOK-006 | MUST | Limit automatic equality and `toString` to safe value types. | [Java language and Lombok](java-language-and-lombok.md) |

## Objects, methods, naming, and packages

| ID | Strength | Summary | Details |
|---|---|---|---|
| OBJECT-001 | MUST | Give a class and method one cohesive responsibility and a clear reason to change. | [Object and method style](object-and-method-style.md) |
| OBJECT-002 | SHOULD | Make a Use Case read in the business order of input, lookup, decision, behavior, persistence, effects, and result. | [Object and method style](object-and-method-style.md) |
| OBJECT-003 | SHOULD | Use a guard clause when it reduces nesting and exposes a failure condition. | [Object and method style](object-and-method-style.md) |
| OBJECT-004 | SHOULD NOT | Do not use a Boolean flag to switch behavior. | [Object and method style](object-and-method-style.md) |
| OBJECT-005 | SHOULD | Choose between a stream and a loop according to which expresses the business meaning more clearly. | [Object and method style](object-and-method-style.md) |
| OBJECT-006 | MUST | Do not hide a state change inside a method that appears to be a query. | [Object and method style](object-and-method-style.md) |
| OBJECT-007 | MUST NOT | Do not use `Map<String, Object>`, `Object[]`, or raw types in Domain or Application contracts. | [Object and method style](object-and-method-style.md) |
| OBJECT-008 | SHOULD | Prefer the narrowest access and composition, and avoid premature generalization. | [Object and method style](object-and-method-style.md) |
| NAMING-001 | MUST | Use English business terms and intention-revealing names. | [Object and method style](object-and-method-style.md) |
| NAMING-002 | SHOULD | Use established suffixes that reveal the layer and role. | [Object and method style](object-and-method-style.md) |
| NAMING-003 | SHOULD NOT | Avoid vague names such as `Impl`, `Manager`, `Helper`, `Utils`, and `Common`. | [Object and method style](object-and-method-style.md) |
| NAMING-004 | MUST | Align the return and failure semantics of `get/find/exists/can/calculate/create/require` names. | [Object and method style](object-and-method-style.md) |
| NAMING-005 | SHOULD | Name Booleans, collections, and acronyms so questions, plurality, and key meaning are clear. | [Object and method style](object-and-method-style.md) |
| PACKAGE-001 | MUST | First identify whether the existing project is organized by business module or by layer. | [Object and method style](object-and-method-style.md) |
| PACKAGE-002 | MUST NOT | Do not mix synonymous package conventions for the same role within one scope. | [Object and method style](object-and-method-style.md) |
| PACKAGE-003 | MUST NOT | Do not impose a new package tree or broad package movement under the label of code style. | [Object and method style](object-and-method-style.md) |
| PACKAGE-004 | SHOULD | In an existing business module, keep Config, SQL, Adapter, Scheduler, and Batch code near its owner. | [Object and method style](object-and-method-style.md) |

## HTTP, DTO, and JSON

| ID | Strength | Summary | Details |
|---|---|---|---|
| DTO-001 | MUST | Do not share an HTTP Request and Response type. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| DTO-002 | MUST | Use either `Command/Query/Result` or the existing `RequestDto/ResultDto` convention consistently at an Application boundary. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| DTO-003 | SHOULD NOT | Do not duplicate identical-field DTOs mechanically according to layer count. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| DTO-004 | MUST | Distinguish the conversion and construction meanings of `toXxx/from/of/create/restore`. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| DTO-005 | SHOULD | Map small objects explicitly and limit MapStruct to repeated mechanical mappings. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| DTO-006 | SHOULD | Use verifiable immutable constructor binding for a new HTTP Request. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| CONTROLLER-001 | MUST | Keep a Controller focused on HTTP conversion and Use Case invocation. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| CONTROLLER-002 | MUST NOT | Do not pass Servlet, Session, or authentication-framework objects into the Application or Domain. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| CONTROLLER-003 | SHOULD | Return a Response DTO directly when no actual HTTP control is required. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| CONTROLLER-004 | MUST NOT | Do not expose JPA, Domain, Query, or provider models through the API. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| CONTROLLER-005 | MUST | Use Controller security annotations only for the authentication boundary. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-001 | MUST | Treat existing JSON, ObjectMapper configuration, and contract tests as the source of truth for the external contract. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-002 | MUST | Preserve field names, types, nulls, omission, dates, enums, and status codes. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-003 | SHOULD | Declare Jackson annotations only when they express an actual contract difference. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-004 | MUST NOT | Do not create a new `ObjectMapper` in each class or impose a common response wrapper. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-005 | MUST NOT | Do not distort an external contract for convenient internal Entity serialization. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |
| JSON-006 | MUST | Declare the permitted discriminator and types for polymorphic deserialization. | [HTTP, DTO, and JSON](http-dto-and-json-style.md) |

## Domain, validation, and authorization

| ID | Strength | Summary | Details |
|---|---|---|---|
| DOMAIN-001 | MUST | Make an Entity protect its own invariants and state transitions. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-002 | SHOULD | Distinguish new construction from persisted-state restoration. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-003 | MUST | Model only genuinely meaningful values as immutable Value Objects. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-004 | SHOULD | Use a Domain Service or Policy only for a pure decision or calculation that does not belong naturally to one object. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-005 | MUST NOT | Do not make a separated Domain depend on Spring, JPA, HTTP, QueryDSL, or a provider SDK. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-006 | MUST | Do not generate current time or identifiers directly inside the Domain. | [Domain and authorization](domain-and-authorization-style.md) |
| DOMAIN-007 | SHOULD | When the project already uses Domain Events, express only completed business facts. | [Domain and authorization](domain-and-authorization-style.md) |
| VALIDATION-001 | MUST | Place syntax, external-state, and invariant validation in the appropriate Presentation, Application, or Domain layer. | [Domain and authorization](domain-and-authorization-style.md) |
| VALIDATION-002 | MUST | Keep the Domain as the final authority and value owner for repeated business constraints. | [Domain and authorization](domain-and-authorization-style.md) |
| VALIDATION-003 | MUST NOT | Do not inject a Repository, provider, Session, or authorization Policy into a Bean Validator. | [Domain and authorization](domain-and-authorization-style.md) |
| VALIDATION-004 | MUST | Assign normalization to one owner and avoid duplicate adjustment across layers. | [Domain and authorization](domain-and-authorization-style.md) |
| OPTIONAL-001 | MUST | Use `Optional<T>` only for a single return value that may normally be absent. | [Domain and authorization](domain-and-authorization-style.md) |
| OPTIONAL-002 | MUST NOT | Do not use Optional in parameters, DTO fields, Entity fields, or collection elements. | [Domain and authorization](domain-and-authorization-style.md) |
| OPTIONAL-003 | MUST | Return an empty collection for an absent plural result. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-001 | MUST | Separate Role, Permission or Action, Attribute, and Policy. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-002 | MUST | Make a Use Case request authorization for a business Action rather than a role code. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-003 | MUST | Make a domain-specific Policy own authorization decisions for each business area. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-004 | MUST | Centralize legacy role, account, and Session exceptions in a compatibility Policy. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-005 | SHOULD NOT | Do not create a general authorization DSL, rule engine, or role inheritance before actual repetition exists. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-006 | MUST | Make a Policy calculate an allowed Scope and a query adapter translate it to SQL conditions. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-007 | MUST | Distinguish visibility checks with `isAllowed()` from actual enforcement with `requireAllowed()`. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-008 | MUST | Deny unknown authorization combinations and an empty allowed range by default. | [Domain and authorization](domain-and-authorization-style.md) |
| AUTH-009 | MUST NOT | Do not treat UI hiding as security enforcement or duplicate authorization conditions in Controller, SQL, and UI code. | [Domain and authorization](domain-and-authorization-style.md) |

## JPA, QueryDSL, and SQL

| ID | Strength | Summary | Details |
|---|---|---|---|
| JPA-001 | MUST | Separate Domain and JPA models conditionally according to business meaning and schema distortion. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-002 | MUST | Reveal a separated persistence model as a storage representation through names and a mapper. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-003 | MUST | Use restricted constructors and mutation paths for a JPA Entity. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-004 | MUST NOT | Do not use public setters, builders, automatic equality, or automatic `toString` on a JPA Entity. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-005 | MUST | Define relationships only for actual Aggregate traversal and use explicit LAZY loading by default. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-006 | MUST | Use cascading and orphan removal only with lifecycle ownership. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-007 | MUST | Encapsulate Entity collections and maintain both sides of a bidirectional relationship in one method. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| JPA-008 | MUST | Implement Entity equality explicitly only when needed, accounting for proxies and identifier lifecycle. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-001 | MUST | Treat a Repository as a persistence boundary, not a business decision maker. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-002 | SHOULD | Separate a Query Repository only when a complex read has a genuinely different reason to change. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-003 | MUST | Select JPA, QueryDSL, or SQL according to simple CRUD, dynamic lookup, or complex-query needs. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-004 | MUST NOT | Do not require `QuerydslRepositorySupport` for every QueryDSL implementation. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-005 | MUST | For bulk DML, state bypassed rules, transaction, synchronization, re-execution, and row-count behavior. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-006 | MUST | Limit nullable Predicate helpers to simple optional AND conditions. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-007 | MUST | Compose complex OR groups, authorization Scopes, and empty-collection conditions explicitly. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-008 | MUST NOT | Do not expose Q-types or QueryDSL dependencies to the Domain or Application. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| QUERY-009 | MUST | Receive a complex read in an explicit QueryRow, Projection, or Result and use stable pagination. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| SQL-001 | SHOULD | Manage complex SQL near its owning code with a business-purpose name. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| SQL-002 | MUST | Define an SQL contract with explicit columns, aliases, parameters, ordering, nulls, and period boundaries. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| SQL-003 | MUST | Track ownership, result meaning, database specificity, and compatibility rationale for complex SQL. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| SQL-004 | MUST NOT | Do not write to a table owned by another business area. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |
| SQL-005 | SHOULD | Verify a database-specific query against the supported database and representative boundary values. | [Persistence and queries](persistence-jpa-querydsl-and-sql.md) |

## Use Cases, Spring, external boundaries, and operational entry points

| ID | Strength | Summary | Details |
|---|---|---|---|
| USECASE-001 | SHOULD | Define a Use Case interface for a real Application entry boundary even with one implementation. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| USECASE-002 | MUST | Make a Use Case orchestrate the business flow and boundary calls without reimplementing Domain rules. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| USECASE-003 | SHOULD NOT | Do not create a formal interface or Base class for a helper with no real boundary. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| USECASE-004 | MUST | Inject Spring dependencies through constructors. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-001 | MUST | Make the public Application Use Case entry point own the business transaction. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-002 | MUST | Use `readOnly = true` only for a genuinely read-only Use Case. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-003 | MUST NOT | Do not put business transactions on Controller, Domain, mapper, provider Client, or Scheduler code. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-004 | SHOULD NOT | Do not hold a database transaction and lock during a slow external call. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-005 | MUST | Use `REQUIRES_NEW` and partial commits only after verifying independent-commit meaning and failure effects. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| TRANSACTION-006 | MUST | Do not expect self-invocation or a private method to create a new Spring transaction boundary. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-001 | MUST | Have the business owner define a provider-independent Port and reveal the provider in the implementation name. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-002 | MUST NOT | Do not expose provider SDKs, DTOs, errors, or authentication objects to the Domain or Application. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-003 | MUST | Translate a provider result accurately into its actual local business meaning. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-004 | MUST | Translate external errors into Port meaning while preserving the cause and a safe identifier. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-005 | MUST | Declare network timeouts explicitly. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-006 | MUST | Apply retries only after reviewing transience, idempotency, duplicate effects, and duplicate retry layers. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| EXTERNAL-007 | MUST | Express an authorized fallback as an explicit degraded result. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| SCHEDULER-001 | MUST | Keep a Scheduler as a thin entry point that builds Context and reference time and invokes a Use Case. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| SCHEDULER-002 | MUST | Declare cron, time zone, re-execution range, and one reference time per execution. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| SCHEDULER-003 | SHOULD | Make idempotency and execution identity explicit when duplicate execution is possible. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| BATCH-001 | MUST | Separate Job, Step, Reader, Processor, and Writer responsibilities. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| BATCH-002 | MUST | Use Chunk, paging, cursor, or another scale-appropriate strategy for large processing. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| BATCH-003 | MUST | Use stable business Job and Step names and explicit parameters. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |
| BATCH-004 | MUST | Define the meaning of retry, skip, restart, partial failure, and duplicate effects. | [Spring boundaries and adapters](spring-boundaries-and-adapters.md) |

## Exceptions, logging, configuration, and documentation

| ID | Strength | Summary | Details |
|---|---|---|---|
| EXCEPTION-001 | MUST | Separate Domain, Application, and Infrastructure failure meanings. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-002 | SHOULD | Use Runtime Exception by default for business failure and checked exceptions only for a real recovery choice. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-003 | MUST NOT | Do not put HTTP, Spring, database, or provider contracts in a Domain Exception. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-004 | MUST | Use concrete business names and a shallow domain-specific hierarchy only when needed. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-005 | SHOULD | Have API-specific Handlers translate the same business exception into the applicable external contract. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-006 | MUST | Do not swallow exceptions, and preserve the cause when translating them. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-007 | MUST | Limit broad catch clauses to the outermost process boundary. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| EXCEPTION-008 | MUST | Use a stable error code for client branching and do not expose internal messages. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-001 | MUST | Use the project Logger and parameterized or structured logging. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-002 | SHOULD | Choose ERROR, WARN, INFO, or DEBUG according to operational value. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-003 | MUST NOT | Do not record and rethrow the same failure at several layers. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-004 | MUST | Pass the exception object as the final log argument. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-005 | MUST NOT | Do not make a pure Domain depend on a logging framework. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-006 | MUST NOT | Do not log secrets, tokens, sessions, personal data, or entire objects. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| LOGGING-007 | MUST | Propagate correlation identifiers consistently from the execution entry boundary. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| COMMENT-001 | MUST | Write identifiers in English and use the project's documentation language consistently. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| COMMENT-002 | MUST | Make comments explain rationale, constraints, compatibility, and reconsideration conditions. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| COMMENT-003 | SHOULD | Write JavaDoc only for non-obvious public contracts and business meaning. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| COMMENT-004 | MUST NOT | Do not leave commented-out historical code or a context-free TODO. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-001 | SHOULD | Group related settings in immutable `ConfigurationProperties`. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-002 | MUST | Validate required settings and safe ranges at startup. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-003 | MUST | Limit Config to Bean wiring and technical implementation selection. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-004 | MUST NOT | Do not use a service locator or static ApplicationContext access. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-005 | MUST | Keep profile and implementation selection at the Config boundary, not in a business Service. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-006 | MUST NOT | Do not use dangerous defaults, automatic `toString`, or whole-object logging for secrets and production endpoints. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |
| CONFIG-007 | MUST | Separate ownership of environment values from immutable business rules. | [Errors, logging, and configuration](errors-logging-and-configuration.md) |

## Testing, tooling, and change scope

| ID | Strength | Summary | Details |
|---|---|---|---|
| TEST-001 | MUST | Follow the project's existing test tools, naming, and fixture conventions. | [Testing and verification](testing-and-verification.md) |
| TEST-002 | MUST | Verify observable business behavior rather than implementation details. | [Testing and verification](testing-and-verification.md) |
| TEST-003 | MUST | Test each responsibility at the layer that owns it. | [Testing and verification](testing-and-verification.md) |
| TEST-004 | MUST NOT | Do not mock Domain objects, Value Objects, or DTOs. | [Testing and verification](testing-and-verification.md) |
| TEST-005 | SHOULD | Verify interactions only when the side effect itself is the contract. | [Testing and verification](testing-and-verification.md) |
| TEST-006 | MUST | Do not weaken production encapsulation for test convenience. | [Testing and verification](testing-and-verification.md) |
| TEST-007 | MUST | Control time, identifiers, asynchronous behavior, and data deterministically and independently. | [Testing and verification](testing-and-verification.md) |
| TEST-008 | SHOULD | Prioritize important branches and contracts, and avoid tests written only to increase coverage. | [Testing and verification](testing-and-verification.md) |
| TEST-009 | MAY | Use Characterization, Golden Master, and Differential Tests for system-replacement work. | [Testing and verification](testing-and-verification.md) |
| TOOLING-001 | MUST | First inspect the target module's build, formatter, static analysis, CI, and generation settings. | [Testing and verification](testing-and-verification.md) |
| TOOLING-002 | MUST | Prefer the project wrapper and established verification commands. | [Testing and verification](testing-and-verification.md) |
| TOOLING-003 | MUST NOT | Do not add a new static-analysis, coverage, or architecture-checking tool to the build without a request. | [Testing and verification](testing-and-verification.md) |
| TOOLING-004 | MUST | Treat search results as candidates and decide violations from context and types. | [Testing and verification](testing-and-verification.md) |
| TOOLING-005 | MUST | Choose verification according to risk and classify failure causes. | [Testing and verification](testing-and-verification.md) |
| TOOLING-006 | MUST | Apply a suppression at the narrowest scope with a rationale and reconsideration condition. | [Testing and verification](testing-and-verification.md) |
| TOOLING-007 | MUST NOT | Do not edit generated code directly. | [Testing and verification](testing-and-verification.md) |
| COMPATIBILITY-001 | MUST | Resolve conflicts in the order of user behavior, external contracts, project rules, integrity, and security. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-002 | MUST | Do not change existing API, data, configuration, Bean, Job, or package contracts without an explicit request. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-003 | MUST | Isolate a general-rule exception narrowly and track its rationale, scope, verification, and reconsideration condition. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-004 | MUST | Do not silently reproduce a security vulnerability or data-loss risk. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-005 | MUST | Limit changes to the requested scope and directly related refactoring. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-006 | MUST NOT | Do not mass-fix unrelated legacy violations or add new features, dependencies, or structures. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-007 | MUST | Do not interpret a review request as authorization to modify files. | [Compatibility and change scope](compatibility-and-change-scope.md) |
| COMPATIBILITY-008 | MUST | Include outcomes, decisions, verification, exceptions, and verification gaps in completion reporting. | [Compatibility and change scope](compatibility-and-change-scope.md) |
