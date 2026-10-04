# Exception, Logging, Configuration, and Documentation Rules

## Table of contents

- [Exception model](#exception-model)
- [HTTP exception translation](#http-exception-translation)
- [Logging and sensitive data](#logging-and-sensitive-data)
- [Comments and JavaDoc](#comments-and-javadoc)
- [Configuration and secrets](#configuration-and-secrets)

## Exception model

<a id="exception-001"></a>
### Represent failures according to their owning layer

**EXCEPTION-001 · MUST**

Separate failure meaning by layer.

- Domain Exception: invariant or state-transition violation
- Application Exception: missing target, unavailable Use Case execution, business-authorization denial, or work-Context mismatch
- Infrastructure Exception: translation of JDBC, JPA, provider, file, or serialization errors into Port or persistence meaning

Do not disguise a technical failure as the wrong business failure.

<a id="exception-002"></a>
### Choose exception types according to recovery needs

**EXCEPTION-002 · SHOULD**

Use an explicit Runtime Exception by default for a business failure. Use a checked exception only when the caller must make a real recovery choice.

<a id="exception-003"></a>
### Keep external contracts out of domain exceptions

**EXCEPTION-003 · MUST NOT**

Do not place an HTTP status, JSON structure, Spring `@ResponseStatus`, database code, or provider error code in a Domain Exception. Keep the Domain unaware of external representations.

<a id="exception-004"></a>
### Name exceptions after concrete business failures

**EXCEPTION-004 · MUST**

Reveal the business meaning of a failure with names such as `CouponExpiredException`, `MemberNotFoundException`, `MemberExportNotAllowedException`, and `NotificationDeliveryException`. Do not use `BusinessException`, `ServiceException`, `CommonException`, `CustomException`, or `ProcessFailedException`.

A business area may own specialized Exceptions and an exception hierarchy. Introduce a shallow base type only when a real error code, property, or handling behavior is shared; do not create deep inheritance for message differences alone.

<a id="exception-006"></a>
### Handle failures meaningfully and preserve their causes

**EXCEPTION-006 · MUST**

Do not catch an exception, log it, and then return as though the operation succeeded. Every catch must have a purpose: recovery, retry classification, failure-state recording, meaningful translation, or external-contract translation. Preserve the cause when translating an exception.

<a id="exception-007"></a>
### Limit broad catches to process boundaries

**EXCEPTION-007 · MUST**

Restrict `catch (Exception)` and `catch (Throwable)` to process boundaries such as per-item Batch isolation, the outer edge of a Scheduler, Message acknowledgement or rejection, or a global HTTP safety net. Do not erase every inner-layer failure as one generic exception.

<a id="exception-008"></a>
### Expose stable error codes rather than internal messages

**EXCEPTION-008 · MUST**

Use a stable error code as the client branching contract, not a human-readable message. Do not expose an exception message directly to an external consumer. The owning business area owns the error code; Presentation owns HTTP status and body mapping.

## HTTP exception translation

<a id="exception-005"></a>
### Translate business exceptions for each HTTP API

**EXCEPTION-005 · SHOULD**

Do not put an HTTP Handler in the Domain. Have a business-specific and adapter-specific Presentation Handler translate the same business exception into each external contract. For example, public, administrator, and internal APIs may express the same `MemberNotFoundException` with different status codes and bodies.

Keep a global Handler focused on business-independent boundary failures such as malformed JSON, Bean Validation, unsupported HTTP methods, authentication failures, and the final safety net.

## Logging and sensitive data

<a id="logging-001"></a>
### Use the established logger and parameterized messages

**LOGGING-001 · MUST**

Use `@Slf4j` when the project uses SLF4J and Lombok; otherwise, follow the established Logger convention. Use parameter binding or the project's structured logging API instead of string concatenation.

```java
log.info(
    "member export completed: adminId={}, count={}",
    adminId,
    exportedCount
);
```

<a id="logging-002"></a>
### Choose log levels by operational value

**LOGGING-002 · SHOULD**

Choose log levels according to operational value.

- ERROR: the business operation cannot complete, integrity may be damaged, retries are exhausted, a message may be lost, or manual intervention is required
- WARN: degraded functionality, fallback, abnormal external data, a pending retry, or repeated suspicious access
- INFO: a significant state transition, administrator export, Batch start or completion totals, or the final result of external delivery
- DEBUG or TRACE: a safe query-summary, retry count, cache hit, or branch selection

Do not record every normal input error or ordinary missing target as WARN, and do not log every method entry and exit as INFO.

<a id="logging-003"></a>
### Log each failure at one meaningful point

**LOGGING-003 · MUST NOT**

Do not have Repository, Service, and Handler each record the same exception as ERROR and rethrow it. Log at one meaningful point: the layer that actually recovers, an adapter that adds useful technical context, or the boundary that finally consumes the failure. A layer that merely rethrows must not log.

<a id="logging-004"></a>
### Preserve stack traces when logging exceptions

**LOGGING-004 · MUST**

Pass the exception object as the final logging argument so the stack trace and cause are preserved.

<a id="logging-005"></a>
### Keep logging frameworks out of a pure domain

**LOGGING-005 · MUST NOT**

Do not make a pure Domain object depend on SLF4J or Logback. Observe significant business events through Application results, state changes, an existing Event mechanism, or Application-level business logs.

<a id="logging-006"></a>
### Protect secrets and personal data in logs

**LOGGING-006 · MUST NOT**

Do not record the following in raw form:

- Passwords or password hashes
- Access or refresh tokens and Authorization headers
- Session identifiers and cookies
- API keys, secrets, encryption keys, or provider credentials
- Government identifiers, passport numbers, payment-card numbers, or bank-account numbers
- Raw personal-data files
- Complete Request or Response bodies
- Entire Entity or provider Response objects

Mask email addresses, phone numbers, names, addresses, and location data to the minimum necessary, or replace them with internal identifiers. Apply the same rule at DEBUG level. Do not generate automatic `toString()` for a sensitive type.

<a id="logging-007"></a>
### Propagate correlation identifiers consistently

**LOGGING-007 · MUST**

When the project uses a trace ID, request ID, Job execution ID, Message ID, or external request ID, propagate it consistently from the HTTP, Message, Scheduler, or Batch entry boundary. Do not let each Service invent a new correlation identifier.

When an audit mechanism already exists, record administrator exports and authorization changes structurally with Actor, Action, target scope, time, result, safe change summary, and correlation identifier. Do not create a new audit store solely as a code-style change.

## Comments and JavaDoc

<a id="comment-001"></a>
### Use consistent identifier and documentation languages

**COMMENT-001 · MUST**

Use the project's primary documentation language for comments and JavaDoc. Do not mix languages arbitrarily within one file or public API document. Follow [Java identifier naming](object-and-method-style.md#naming) for identifiers and glossary terms.

<a id="comment-002"></a>
### Explain reasons and constraints in comments

**COMMENT-002 · MUST**

Use a comment to explain information the code itself does not already state, such as:

- Why the implementation must work this way
- An external-system constraint
- Deliberate compatibility behavior
- Why the implementation differs from the normal approach
- Performance, concurrency, or transaction cautions
- A reconsideration condition

Do not repeat the code with comments such as `look up the member` or `save the member`.

<a id="comment-003"></a>
### Document public contracts when names and types are insufficient

**COMMENT-003 · SHOULD**

Do not require JavaDoc on every class, method, and field. Write it for a public contract whose name and types are insufficient, such as:

- A Port used by another module
- A non-obvious Domain rule or a Value Object with units, time-zone, or precision semantics
- A Use Case with retry, idempotency, or transaction meaning
- A required external-contract conversion
- An API whose call order or side effects must be understood

Do not repeat names with documentation such as `@param command command` or `@return result`. OpenAPI and JavaDoc serve different consumers; do not duplicate the same long text, and establish the source of truth for each document.

<a id="comment-004"></a>
### Remove stale code and make TODOs actionable

**COMMENT-004 · MUST NOT**

Do not retain commented-out historical code. Do not leave `TODO fix later` or a context-free `FIXME`; when necessary, include an issue identifier, rationale, completion condition, and reconsideration condition. Do not use logs such as `start`, `before save`, and `end` as flow-description comments.

## Configuration and secrets

<a id="config-001"></a>
### Group related settings in immutable configuration types

**CONFIG-001 · SHOULD**

Group related configuration values in an immutable `@ConfigurationProperties` type rather than scattered `@Value` fields. Check the project's Spring Boot version and established binding approach, then use constructor binding and defensive collection copies.

<a id="config-002"></a>
### Validate required configuration at startup

**CONFIG-002 · MUST**

Validate required endpoints, positive timeouts, permitted Batch sizes, mandatory identifiers, and contradictory combinations at startup. Do not put validation requiring a database or external API call in a Properties validator.

<a id="config-003"></a>
### Keep configuration focused on technical wiring

**CONFIG-003 · MUST**

Limit Config to:

- Bean construction and wiring
- Adapter implementation selection
- Technical Client and serializer configuration
- Properties activation
- Conditional Beans
- Repository scanning and Transaction Manager wiring

Do not put role-specific authorization, Domain state transitions, Repository lookup, external-call execution, or Batch business logic in Config. Do not register the same class both as a component and as an explicit `@Bean`.

<a id="config-004"></a>
### Declare dependencies instead of locating them globally

**CONFIG-004 · MUST NOT**

Do not use `ApplicationContext.getBean`, a static Context holder, or a service locator in business code. Declare dependencies through constructors.

<a id="config-005"></a>
### Select implementations at the configuration boundary

**CONFIG-005 · MUST**

Concentrate environment-specific implementation selection and profile branching at the outer Config boundary. Do not make a Service branch on the active-profile string. Use a role-revealing qualifier only when multiple implementations of the same type actually exist.

<a id="config-006"></a>
### Avoid dangerous defaults and secret exposure

**CONFIG-006 · MUST NOT**

Do not provide defaults for values whose absence is dangerous, such as an API key, production endpoint, administrator account, secret, or production bucket. Do not use automatic `toString()` on a configuration object containing secrets or log the entire object. Do not introduce a particular secret manager without an authorized request.

<a id="config-007"></a>
### Separate environment settings from business rules

**CONFIG-007 · MUST**

Let Config own environment-dependent endpoints, timeouts, and Batch sizes. Let the Domain own environment-independent state transitions, authorization Actions, and calculation rules. Do not move business rules into YAML so Config replaces the Domain, or hard-code operational values as Java constants.
