# Choosing Persistence and Query Patterns

Read this when object identity, query cost, or concurrent-update problems remain after persistence access has been hidden. The basic responsibilities of Repository and Unit of Work are covered in [Practical code patterns](application.md); this reference addresses choices beneath and around those responsibilities.

## How Much an Object Knows About Persistence

### Separating Storage Representation from Business Objects: Data Mapper

Use this when business-object and storage structures differ, or business behavior needs to remain independent of database access. The mapping responsibility transfers values between objects and storage. Business objects do not necessarily need to know that the mapper exists.

Use the ORM or existing persistence implementation if it already performs this role. Do not introduce a mapping system that manually copies the same object through several stages. Aligning table/object relationships, identifiers, and change tracking has a cost, and round-trip conversions that omit fields can lose data.

### Combining a Row with Persistence Behavior: Active Record

An object holds a row's data together with querying and persistence behavior. This can be direct for simple, data-centric features in a framework that supports it. It may be unsuitable when a complex business model must remain independent of storage or when the project requires storage-only models.

Active Record and Data Mapper are alternatives for understanding an existing implementation and comparing choice costs. Do not replace the project's entire persistence approach merely to apply a pattern in one task. A class having persistence methods does not mean every business rule belongs there too.

### Table-Level and Row-Level Access

Table Data Gateway collects queries and updates for a table or view in one access object and is worth comparing for set-oriented data access. Row Data Gateway wraps persistence operations in an object representing a row, but is not itself a rich business model.

Neither has exactly the same meaning as a business-facing Repository contract. If an existing DAO or mapper already fills the role, do not create another object just to match the name. Replacing set updates with repeated per-row updates can change query counts, lock scope, and execution time.

## One Object for the Same Row: Identity Map

If reading the same identifier multiple times within a unit of work produces different mutable objects, reconciling changes to the copies becomes difficult. The purpose is to associate identifiers with objects within that scope and reuse the same instance.

Check whether the ORM's persistence context already provides this. Even if it does not, first establish a clear scope such as a request or unit of work. Unlike a global cache, its focus is object identity and consistency of changes.

Extending it to share mutable business objects across an entire process can cause interference between requests and stale state. Reusing the same instance also does not guarantee the latest database state. Check whether the lifetime of retained objects should also end when the work scope ends.

## Reading When Needed: Lazy Load

Defer reading related data that is not always used until it is actually accessed. Implementations can include lazy initialization, a virtual proxy standing in for the original object, a holder from which a value is explicitly retrieved, or a partially populated object. Check existing ORM facilities first.

The central decision is not simply to reduce the amount read initially. Determine whether a session or connection will still exist at the later read, whether apparently synchronous access performs I/O, and at what point in time related values should form a consistent result.

Reading related values for every item in a list can turn one initial query into an additional query per item. Compare explicit queries for only the columns the screen needs, joins, or batch loading. Exposing lazy objects directly outside the query layer can trigger unexpected I/O during serialization or rendering.

## Representing Queries: Query Object

Consider this when conditions, sorting, and query shape must be composed and representing them as objects is clearer than many dedicated query methods. The minimal form is the necessary query representation and execution responsibility. Do not create another interpreter when an existing query tool already supplies the representation.

A simple query-parameter DTO is not always a Query Object. Specification focuses on the business meaning of a condition; Query Object focuses on representing and composing persistence queries. If they are connected, check whether database and in-memory evaluation agree on nulls, string comparison, and time references.

Do not change an operation that must apply filters, sorting, and pagination in the database into reading everything and processing it in memory. Start with the expressions needed by the actual query contract rather than a general-purpose search language exposing every arbitrary field.

## Detecting Changes Since a User Read a Value: Optimistic Offline Lock

When other work can change values while a user has a screen open for editing, consider checking the version originally read against the current version at save time to prevent stale edits from overwriting newer changes. This fits when conflicts are infrequent and holding locks across long waits is impractical.

The version check and update must be part of the same atomic persistence operation. Reading and comparing the version first, then performing an unconditional update later, can miss changes in between. Treat the affected-row count or ORM conflict outcome as a meaningful conflict.

Simply retrying after a conflict is not always correct. User edits may require comparison with current values or reconfirmation. For a pure, repeatable calculation, consider rereading current state and making the decision again. Also check whether the previous attempt already caused external effects.

One row's version does not protect every invariant spanning multiple rows. If separate changes to different rows can break an overall constraint, assess whether atomic conditional updates, constraints, or a broader consistency boundary are needed.

## Coordinating Editing Rights Before a Conflict: Pessimistic Offline Lock

Consider logical editing ownership when a business editing process spanning several user interactions must be performed by only one party at a time. This differs from holding a row lock within a short database transaction. Do not confuse it with keeping a database connection and row lock open throughout user think time.

Even the minimal form needs an owner, release conditions, and recovery semantics after abnormal termination, so its cost is substantial. If detecting a conflict is sufficient, compare an optimistic approach first. Having Lock in an implementation's name does not solve expiration or ownership transfer.

Handle an earlier editor saving after ownership has expired or moved to someone else. Showing editing availability on screen is not sufficient: the actual write must atomically verify current ownership and any required version conditions. Checking ownership and then separately performing an unconditional write can miss a transfer in between.

If the current requirement is concurrent-update control within a single transaction, consider database atomic operations and short-lived locks. Do not add a multi-server lock service as the default implementation for this reference.

## Combining Query and Persistence Responsibilities

| Responsibility | What it owns | What it does not guarantee |
| --- | --- | --- |
| Repository | The data-access contract needed by the business | Objects always being up to date |
| Data Mapper | Conversion between objects and storage representations | Correctness of business rules |
| Identity Map | Mapping an identifier to the same object within one unit of work | Freshness across requests |
| Unit of Work | Change tracking and persistence coordination | Atomicity of all external effects |
| Version-based updates | Detecting changes that conflict with the version read | Every constraint involving other rows |
| Lazy Load | Reading data at the point of use | A fixed query count or connection lifetime |

There is no need to implement every responsibility as a separate class. Identify what current tools already provide and fill only missing contracts. Focus verification on changed behavior such as persistence round trips, the scope of instance identity, actual query counts, atomic conflict detection, and rollback results.
