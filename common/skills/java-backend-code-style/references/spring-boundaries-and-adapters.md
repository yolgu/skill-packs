# Spring Boundary, Use Case, Adapter, Scheduler, and Batch Rules

## Table of contents

- [Use Cases and dependencies](#use-cases-and-dependencies)
- [Transactions](#transactions)
- [External Ports and Adapters](#external-ports-and-adapters)
- [Scheduler](#scheduler)
- [Batch](#batch)

## Use Cases and dependencies

### Expose a Use Case interface when its contract needs separation

**SHOULD**

A Spring @Service can be the application entry point directly. A Controller, Scheduler, or Batch caller does not by itself require a Service/Impl pair or a ...UseCase interface.

Use an interface when the application contract needs independent publication, implementation isolation, or actual polymorphism. One implementation is sufficient when that boundary is real. Keep the interface in application vocabulary and avoid collecting unrelated operations into one enormous Use Case.

### Implement the application flow through public contracts

**MUST**

An application service coordinates input/context, required lookups, authorization, plain business-object behavior, persistence, external effects, and a service ResultDto. Enforce authorization before the protected action so other inbound entry points receive the same enforcement.

Use the repository's public DTO contract. Convert its result to a service result, and send already-decided storage values back through a repository request. Do not import JPA Entities into the service or call Entity setters there.

For simple CRUD, direct service-to-repository orchestration is sufficient. Add business objects only for actual business concepts or rules.

### Keep Spring components direct

**SHOULD NOT**

Use a concrete component for a small internal collaborator. Do not add I-prefixed interfaces, ...ServiceImpl pairs, Abstract/Base components, or a forwarding transaction wrapper merely because Spring supports them.

When an actual distinct transaction needs a separate proxied component, name that responsibility explicitly.

### Inject dependencies through constructors

**MUST**

Inject Spring dependencies through a constructor and make the fields `final`. Do not use field injection or setter injection. Write an explicit constructor when selecting among same-type implementations, using lazy resolution, or validating construction; otherwise, a limited `@RequiredArgsConstructor` is acceptable when already used by the project.

HTTP context conversion is defined in [HTTP boundary rules](http-dto-and-json-style.md#controller); service-locator restrictions are defined in [Configuration](errors-logging-and-configuration.md#configuration-and-secrets).

## Transactions

### Let the application use case own the transaction

**MUST**

Make the public entry method of an Application Use Case own the business transaction. Ensure lookup, Domain behavior, and persistence succeed or fail atomically within one business unit. A Repository performs data access but does not own overall business atomicity or hidden partial commits.

### Use read-only transactions only for read-only work

**MUST**

Use `@Transactional(readOnly = true)` for a genuinely read-only Use Case. A query that changes access history, last-login time, download count, or read status is not read-only; make that meaning visible in the Use Case name.

A class-level declaration is acceptable when the entire service has the same transaction semantics. When reads, writes, or propagation differ, declare them on methods and avoid nested defaults and overrides that make behavior difficult to trace.

### Keep business transactions at the application layer

**MUST NOT**

Do not put a business transaction on a Controller, Request, Response, Domain object, mapper, provider Client, or Scheduler entry method itself. Put it on the application's service entry method; an interface is optional under the Use Case rule above. Inbound entry points call that service, while data models remain data.

### Avoid holding database locks during slow external calls

**SHOULD NOT**

Do not hold a database connection and lock for a long-running external network call. Separate short database changes, the external call, and result application according to business atomicity. For a concern such as payment that requires external and internal consistency, do not merely move the call outside the transaction; design the state model, idempotency, retries, and compensation explicitly. Do not choose Outbox or Saga automatically.

### Verify independent commits and partial failure behavior

**MUST**

Prefer the default `REQUIRED` propagation. Use `REQUIRES_NEW` only for a real independent-commit meaning, such as an audit record that must survive the main failure or an independent Batch unit. Verify partial commits, connection-pool impact, lock ordering, and the result when the outer transaction fails.

For multiple data sources, state the selected Transaction Manager explicitly. Do not wrap an entire large operation in one transaction; define chunk boundaries, partial failure, re-execution, and success, failure, and skip counts.

### Account for Spring proxy transaction boundaries

**MUST**

Do not expect same-object invocation or `@Transactional` on a private method to pass through a Spring proxy and create a new boundary. When a distinct transaction responsibility is real, extract a meaningful Application component.

## External Ports and Adapters

### Implement provider-independent Java contracts

**MUST**

Publish an interface with provider-independent inputs, results, and failure meanings. Name its implementation for the provider, for example NotificationDeliveryPort with FcmNotificationClient.

One implementation may perform both the protocol call and straightforward representation conversion. Split an Adapter, raw Client, or Mapper only when it has a distinct responsibility or actual reuse; do not generate a fixed class set.

Keep provider names and SDK types out of the published Java signature. Implementation selection belongs in Spring configuration.

### Keep provider types inside adapters

**MUST NOT**

Do not expose provider SDK objects, HTTP responses, provider JSON DTOs, error enums, authentication objects, or pagination types to the Domain or Application. Make the adapter convert local Port input to a provider Request and interpret the provider Response as a local Result.

### Translate provider results into accurate business outcomes

**MUST**

Distinguish the provider's technical status from local business meaning. Do not overstate provider acceptance as confirmed end-user receipt. Limit a mapper to representation and provider-code conversion; it must not decide authorization, perform state transitions, query a Repository, obtain current time, or choose business retries.

### Translate provider errors while preserving their causes

**MUST**

Do not expose provider exceptions directly to inner layers. Translate authentication errors, rate limits, transient delivery failures, and permanent request errors into Port-level failure meanings while preserving the cause and a safe provider request identifier. Do not put credentials or a complete error body in an exception message.

### Set network timeouts explicitly

**MUST**

Declare connection timeout, response timeout, and any required deadline explicitly. Own the values in configuration according to service and operational criteria. Do not rely on unlimited waits or ambiguous library defaults.

### Retry only when failure and duplication semantics permit it

**MUST**

Before applying a retry, verify:

- Whether the failure is transient
- Whether the request is idempotent or carries an idempotency key
- Whether duplicate effects are acceptable
- Whether the caller and adapter would retry the same operation twice
- Whether a database transaction or lock would remain open too long

Do not normally retry authentication, format, authorization, or permanent failures. Do not add a retry or circuit-breaker library without a request that authorizes it.

### Expose external failures and approved fallback states

**MUST**

Do not silently turn an external failure into an empty collection or success. When a fallback is acceptable to the business, let the Application or Policy decide and expose the degraded state in the Result. Do not prebuild a fallback structure without a confirmed need.

## Scheduler

### Keep schedulers focused on invoking use cases

**MUST**

Keep a Scheduler as a thin inbound adapter responsible only for:

- Declaring the execution time
- Building the execution Actor, Context, and reference time
- Invoking the Application Use Case
- Connecting result logs and metrics
- Applying the outermost failure policy

Do not run QueryDSL, combine Repositories, mutate Entity fields, interpret roles, execute bulk SQL, hold a long transaction, or call a provider SDK directly in a Scheduler.

When manual administrator execution and scheduled execution perform the same business operation, use the same Use Case and distinguish actor, audit, and execution scope through an explicit request context.

### Configure schedules and establish one execution time

**MUST**

Separate cron and time zone into configuration. Cron determines execution time; target eligibility is a Domain rule. Establish one reference time per execution, pass it to every target, and account for DST gaps and duplicates.

### Define behavior for duplicate execution

**SHOULD**

When multiple instances, an unfinished prior execution, restart, external scheduler redelivery, or operator rerun are possible, make the following explicit:

- Whether an already processed target changes again
- Whether an external delivery can be duplicated
- The execution interval and execution identifier
- How the state model identifies duplicate execution

Do not introduce a distributed lock automatically without a confirmed need.

## Batch

### Separate Spring Batch responsibilities

**MUST**

When using Spring Batch, separate the roles:

- Job: overall business execution unit and flow
- Step: transaction and restart unit
- Reader: input acquisition
- Processor: per-item transformation and decision
- Writer: result persistence and output

A Tasklet may suit one command, while a Chunk may suit many items; choose according to the project and processing semantics. Let a Processor invoke plain business behavior where needed; a Writer delegates persistence to the storage implementation, which can use simple Entity accessors.

### Process large datasets in manageable units

**MUST**

Do not load a large data set into memory with one `findAll()`. Choose cursor, paging, and chunk size according to row size, processing time, database locks, memory, provider rate limits, and failure-reprocessing cost. For a controlled bulk operation where per-Aggregate handling is impractical, follow the persistence rules for bulk exceptions.

### Use stable job names and explicit execution parameters

**MUST**

Use stable business-purpose Job and Step names such as `expireCouponsJob` and `loadExpirationCandidatesStep`. Do not change a name that serves as execution history or a restart key merely for style.

Pass reference time, processing interval, requester, and execution identifier as explicit Job Parameters. Do not obtain a new current time in every Step.

### Define retry, skip, restart, and partial failure behavior

**MUST**

Distinguish technical and business failures in Retry, Skip, and Restart behavior. Track skipped targets and reasons, success, failure, and skip counts, partial-failure meaning, restart position, and duplicate effects. Do not use unlimited Skip behavior to make a failed Job appear successful.

Avoid making many slow provider API calls inside a Chunk transaction. Review rate limits, idempotency, duplicate delivery, retry unit, result-persistence timing, and database-transaction lifetime together.
