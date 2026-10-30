# Spring Boundary, Use Case, Adapter, Scheduler, Batch, Consumer, and Listener Rules

## Table of contents

- [Use Cases and dependencies](#use-cases-and-dependencies)
- [Transactions](#transactions)
- [External Ports and Adapters](#external-ports-and-adapters)
- [Scheduler](#scheduler)
- [Batch](#batch)
- [Message consumers](#message-consumers)
- [After-commit event listeners](#after-commit-event-listeners)

## Use Cases and dependencies

### Give each Use Case a narrow input contract

**MUST**

Every Use Case that an inbound adapter (a Controller, Scheduler, Batch step, message listener, or event listener) calls gets a narrow input contract interface named after the Use Case, such as `PlaceOrderUseCase`, implemented by the application service (`PlaceOrderService`). The adapter depends on that contract, and the adapter's tests replace it with a double. One implementation is sufficient: the contract is the role the adapter depends on, not a test convenience.

Keep the contract in application vocabulary with the Use Case's own input and result models, and do not collect unrelated operations into one enormous Use Case. An interface that copies a service class's whole method set is not this contract; Keep Spring components direct still rules out ...ServiceImpl pairs.

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

Stated exceptions, each recorded in the plan item's design field rather than inferred:

- A Spring Batch chunk Step owns the transaction of its chunk.
- A listener that combines a Kafka transaction with the database transaction owns that combined boundary.
- When a Use Case includes a slow external call, the entry method coordinates the steps without a transaction, and only the database-changing step opens one, through a declaration on a separate component named for that responsibility or through `TransactionTemplate`.

### Use read-only transactions only for read-only work

**MUST**

Use `@Transactional(readOnly = true)` for a genuinely read-only Use Case. A query that changes access history, last-login time, download count, or read status is not read-only; make that meaning visible in the Use Case name.

A class-level declaration is acceptable when the entire service has the same transaction semantics. When reads, writes, or propagation differ, declare them on methods and avoid nested defaults and overrides that make behavior difficult to trace.

### Keep business transactions at the application layer

**MUST NOT**

Do not put a business transaction on a Controller, Request, Response, Domain object, mapper, provider Client, or Scheduler entry method itself. Put it on the application's service entry method; an interface is optional under the Use Case rule above. Inbound entry points call that service, while data models remain data.

### Avoid holding database locks during slow external calls

**SHOULD NOT**

Do not hold a database connection and lock for a long-running external network call. Narrow the atomic unit to the database-changing step and place the external call before it or after it has committed, using the stated exception under "Let the application use case own the transaction": the entry method coordinates without a transaction and the database step opens its own. A write that depends on a value read outside that narrowed boundary uses a conditional update or a version check instead of trusting the earlier read. For a concern such as payment that requires external and internal consistency, do not merely move the call outside the transaction; design the state model, idempotency, retries, compensation, and the unknown-outcome state explicitly. Do not choose Outbox or Saga automatically.

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

See code-principles, Make External Calls Explicit.

### Retry only when failure and duplication semantics permit it

**MUST**

See code-principles, Make External Calls Explicit.

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

### Decide scheduler risks at design time

**SHOULD**

Record in the plan item's design field, before the first test: how concurrent runs across multiple instances are prevented or tolerated; that a lock only prevents concurrent runs while correctness on re-execution (whether an already processed target changes again) is the state model's responsibility; how failures are isolated per target so that one failing target does not abort the run; and which time zone the schedule and the reference time use. The outer-loop test calls the entry method directly with a fixed reference time instead of waiting for cron; its form is in [Testing and verification](testing-and-verification.md).

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

### Decide batch policies at job design time

**MUST**

Because reading comes first in a Job, decide the item type, chunk size, restart policy, and skip policy when designing the Job, and implement the Reader last, after the Processor and Writer exist against that item type. Record in the plan item's design field: run identification (the identifying Job Parameters), the restart position, duplicate effects when a failed chunk is reprocessed, the skip limit, and any external call inside a chunk. The chunk Step owns the transaction, as the stated exception under "Let the application use case own the transaction".

## Message consumers

### Keep consumers as thin adapters that invoke use cases

**MUST**

Keep a Kafka or RabbitMQ listener as a thin inbound adapter: deserialize and validate the message, build the execution context, invoke the Application Use Case, and apply the outermost failure policy. The Use Case service owns the business transaction; the listener method does not. A listener that combines a Kafka transaction with the database transaction is the stated exception and names that combined boundary explicitly.

### Design consumers for at-least-once delivery

**MUST**

Assume redelivery. Derive an idempotency key from the message and keep the processing record in the same database transaction as the business change, so that a message redelivered after a crash between commit and acknowledgment is recognized. Acknowledge or commit the offset only after the database transaction has committed; never acknowledge first.

### Classify consumer failures before retrying

**MUST**

Decide per exception whether the message is retried (transient infrastructure failures) or not (deserialization and validation failures, business rejections, and other poison messages), and route non-retryable and exhausted messages to a dead-letter topic or queue with the failure reason. With RabbitMQ an exception requeues the message by default, so a poison message loops; reject without requeue or configure retry with a dead-letter queue. The framework's error handler already logs each consumer failure once, and the application does not log it again (see [Errors, logging, and configuration](errors-logging-and-configuration.md)).

## After-commit event listeners

### Keep after-commit listeners as thin adapters

**MUST**

Keep an `@TransactionalEventListener` as a thin adapter that invokes an Application Use Case for the follow-up work. Publish the event from the Use Case and let the listener phase, not the publisher, decide that it runs after commit. The change the listener triggers must commit in its own new transaction; it must not join the finished transaction.

### Decide where propagation lives after verifying it

**MUST**

In the after-commit phase the default propagation joins the already completed transaction, so a write made there does not commit. This behavior is confirmed from source reading only, so the base work item verifies it on the project's stack before the first listener is written: whether `NOT_SUPPORTED` on a synchronous listener method makes the Use Case it calls commit anew, whether the transaction reads as inactive inside it, and whether a write without any declaration gets committed on the JDBC path by auto-commit restoration. Record the result here, one line. Until then, prefer `NOT_SUPPORTED` on the listener method or asynchronous execution, and treat `REQUIRES_NEW` as a recorded exception under "Verify independent commits and partial failure behavior". Spring 6.1 rejects a listener method declared with other propagation values at startup but does not catch a missing declaration; check it in review.

### Handle listener failures and resources explicitly

**MUST**

A listener exception is logged once at ERROR by the framework and is not propagated to the publisher, so record compensation or reprocessing in the plan item's design field and do not log the same failure again. A synchronous listener uses one additional connection during the after-commit phase; account for it in the pool size. An asynchronous listener needs an executor with a bounded queue and a decision about what happens when the queue is full. The test form (test transaction off, assertions by resulting state) is in [Testing and verification](testing-and-verification.md).
