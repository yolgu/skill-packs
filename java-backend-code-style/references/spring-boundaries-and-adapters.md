# Spring Boundary, Use Case, Adapter, Scheduler, and Batch Rules

## Table of contents

- [Use Cases and dependencies](#use-cases-and-dependencies)
- [Transactions](#transactions)
- [External Ports and Adapters](#external-ports-and-adapters)
- [Scheduler](#scheduler)
- [Batch](#batch)

## Use Cases and dependencies

### USECASE-001 — SHOULD

Decide whether to define a Use Case interface by the existence of an application entry boundary, not by implementation count. Define a `...UseCase` interface even with one implementation when:

- A Controller, Scheduler, Batch, or Message Consumer invokes the business capability
- More than one inbound adapter may invoke the same capability
- The caller must not know implementation technology or transaction details
- The input and result contracts merit independent expression
- The interface protects dependency direction rather than merely simplifying a test mock

Do not mechanically require one method per Use Case, but do not collect operations with different authorization, transaction, or change reasons in one enormous `MemberUseCase`.

### USECASE-002 — MUST

Make an Application Service orchestrate input and Context, authorization, Domain lookup, Domain behavior, persistence, external effects, and results. Do not reimplement role codes, state transitions, or calculation rules in long `if` statements; make an Entity, Value Object, or Policy own them.

Have the Use Case verify actual business authorization explicitly immediately before the protected action. Preserve enforcement when a Controller, Scheduler, or internal API invokes the same Use Case.

### USECASE-003 — SHOULD NOT

Do not create formal interfaces for an internal helper, small orchestration object, or implementation with no real boundary. Do not use `IExportMembersService`, `ExportMembersServiceImpl`, or unnecessary `Abstract...` and `Base...` types.

### USECASE-004 — MUST

Inject Spring dependencies through a constructor and make the fields `final`. Do not use field injection or setter injection. Write an explicit constructor when selecting among same-type implementations, using lazy resolution, or validating construction; otherwise, a limited `@RequiredArgsConstructor` is acceptable when already used by the project.

Convert Servlet, Session, and authentication-framework objects to explicit Actor and WorkContext types in the inbound adapter. Do not let an inner layer locate dependencies through `ApplicationContext.getBean()`.

## Transactions

### TRANSACTION-001 — MUST

Make the public entry method of an Application Use Case own the business transaction. Ensure lookup, Domain behavior, and persistence succeed or fail atomically within one business unit. A Repository performs data access but does not own overall business atomicity or hidden partial commits.

### TRANSACTION-002 — MUST

Use `@Transactional(readOnly = true)` for a genuinely read-only Use Case. A query that changes access history, last-login time, download count, or read status is not read-only; make that meaning visible in the Use Case name.

A class-level declaration is acceptable when the entire service has the same transaction semantics. When reads, writes, or propagation differ, declare them on methods and avoid nested defaults and overrides that make behavior difficult to trace.

### TRANSACTION-003 — MUST NOT

Do not put a business transaction on a Controller, Request, Response, Domain object, mapper, provider Client, or Scheduler entry method itself. Have those objects invoke an explicit Use Case.

### TRANSACTION-004 — SHOULD NOT

Do not hold a database connection and lock for a long-running external network call. Separate short database changes, the external call, and result application according to business atomicity. For a concern such as payment that requires external and internal consistency, do not merely move the call outside the transaction; design the state model, idempotency, retries, and compensation explicitly. Do not choose Outbox or Saga automatically.

### TRANSACTION-005 — MUST

Prefer the default `REQUIRED` propagation. Use `REQUIRES_NEW` only for a real independent-commit meaning, such as an audit record that must survive the main failure or an independent Batch unit. Verify partial commits, connection-pool impact, lock ordering, and the result when the outer transaction fails.

For multiple data sources, state the selected Transaction Manager explicitly. Do not wrap an entire large operation in one transaction; define chunk boundaries, partial failure, re-execution, and success, failure, and skip counts.

### TRANSACTION-006 — MUST

Do not expect same-object invocation or `@Transactional` on a private method to pass through a Spring proxy and create a new boundary. When a distinct transaction responsibility is real, extract a meaningful Application component.

## External Ports and Adapters

### EXTERNAL-001 — MUST

Have the business owner define a provider-independent Port, and reveal the provider in the implementation name.

```text
NotificationDeliveryPort
FcmNotificationDeliveryAdapter
FcmClient
FcmProviderRequest
FcmProviderResponse
FcmNotificationMapper
```

Do not put the provider name in the Port or obscure roles with names such as `ExternalService`, `ApiService`, `ThirdPartyManager`, or `FcmServiceImpl`. Make the Client handle raw HTTP or SDK communication, and the Adapter apply the business contract.

### EXTERNAL-002 — MUST NOT

Do not expose provider SDK objects, HTTP responses, provider JSON DTOs, error enums, authentication objects, or pagination types to the Domain or Application. Make the adapter convert local Port input to a provider Request and interpret the provider Response as a local Result.

### EXTERNAL-003 — MUST

Distinguish the provider's technical status from local business meaning. Do not overstate provider acceptance as confirmed end-user receipt. Limit a mapper to representation and provider-code conversion; it must not decide authorization, perform state transitions, query a Repository, obtain current time, or choose business retries.

### EXTERNAL-004 — MUST

Do not expose provider exceptions directly to inner layers. Translate authentication errors, rate limits, transient delivery failures, and permanent request errors into Port-level failure meanings while preserving the cause and a safe provider request identifier. Do not put credentials or a complete error body in an exception message.

### EXTERNAL-005 — MUST

Declare connection timeout, response timeout, and any required deadline explicitly. Own the values in configuration according to service and operational criteria. Do not rely on unlimited waits or ambiguous library defaults.

### EXTERNAL-006 — MUST

Before applying a retry, verify:

- Whether the failure is transient
- Whether the request is idempotent or carries an idempotency key
- Whether duplicate effects are acceptable
- Whether the caller and adapter would retry the same operation twice
- Whether a database transaction or lock would remain open too long

Do not normally retry authentication, format, authorization, or permanent failures. Do not add a retry or circuit-breaker library without a request that authorizes it.

### EXTERNAL-007 — MUST

Do not silently turn an external failure into an empty collection or success. When a fallback is acceptable to the business, let the Application or Policy decide and expose the degraded state in the Result. Do not prebuild a fallback structure without a confirmed need.

## Scheduler

### SCHEDULER-001 — MUST

Keep a Scheduler as a thin inbound adapter responsible only for:

- Declaring the execution time
- Building the execution Actor, Context, and reference time
- Invoking the Application Use Case
- Connecting result logs and metrics
- Applying the outermost failure policy

Do not run QueryDSL, combine Repositories, mutate Entity fields, interpret roles, execute bulk SQL, hold a long transaction, or call a provider SDK directly in a Scheduler.

When manual administrator execution and scheduled execution perform the same business operation, use the same Use Case and distinguish actor, audit, and execution scope through an explicit Command Context.

### SCHEDULER-002 — MUST

Separate cron and time zone into configuration. Cron determines execution time; target eligibility is a Domain rule. Establish one reference time per execution, pass it to every target, and account for DST gaps and duplicates.

### SCHEDULER-003 — SHOULD

When multiple instances, an unfinished prior execution, restart, external scheduler redelivery, or operator rerun are possible, make the following explicit:

- Whether an already processed target changes again
- Whether an external delivery can be duplicated
- The execution interval and execution identifier
- How the state model identifies duplicate execution

Do not introduce a distributed lock automatically without a confirmed need.

## Batch

### BATCH-001 — MUST

When using Spring Batch, separate the roles:

- Job: overall business execution unit and flow
- Step: transaction and restart unit
- Reader: input acquisition
- Processor: per-item transformation and decision
- Writer: result persistence and output

A Tasklet may suit one command, while a Chunk may suit many items; choose according to the project and processing semantics. Do not make a Processor or Writer assemble state through setters; invoke Domain behavior where practical.

### BATCH-002 — MUST

Do not load a large data set into memory with one `findAll()`. Choose cursor, paging, and chunk size according to row size, processing time, database locks, memory, provider rate limits, and failure-reprocessing cost. For a controlled bulk operation where per-Aggregate handling is impractical, follow the persistence rules for bulk exceptions.

### BATCH-003 — MUST

Use stable business-purpose Job and Step names such as `expireCouponsJob` and `loadExpirationCandidatesStep`. Do not change a name that serves as execution history or a restart key merely for style.

Pass reference time, processing interval, requester, and execution identifier as explicit Job Parameters. Do not obtain a new current time in every Step.

### BATCH-004 — MUST

Distinguish technical and business failures in Retry, Skip, and Restart behavior. Track skipped targets and reasons, success, failure, and skip counts, partial-failure meaning, restart position, and duplicate effects. Do not use unlimited Skip behavior to make a failed Job appear successful.

Avoid making many slow provider API calls inside a Chunk transaction. Review rate limits, idempotency, duplicate delivery, retry unit, result-persistence timing, and database-transaction lifetime together.
