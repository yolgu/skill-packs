# JPA, QueryDSL, and SQL Rules

## Table of contents

- [Domain and JPA models](#domain-and-jpa-models)
- [JPA Entities and relationships](#jpa-entities-and-relationships)
- [Repositories and query tools](#repositories-and-query-tools)
- [QueryDSL](#querydsl)
- [SQL](#sql)

## Domain and JPA models

<a id="jpa-001"></a>
### Keep business behavior separate from JPA storage

**JPA-001 · MUST**

Treat a JPA Entity as a DB-mapped data representation. Business decisions, calculations, business state-transition rules, and DTO interpretation belong outside it.

A plain business object is needed only when there is actual business meaning or behavior to model. Simple storage and lookup can use service and repository DTOs; do not create a domain twin for every table. Do not introduce a combined behavioral Domain/JPA model as a CRUD shortcut or assume a legacy schema by default.

<a id="jpa-002"></a>
### Keep the public repository contract independent of JPA

**JPA-002 · MUST**

Expose a Java repository interface whose inputs and results are public repository DTOs or standard Java values. It must not extend JpaRepository or expose EntityManager, JPA Entities, QueryDSL types, or provider-specific rows.

One JPA implementation owns database access and Entity conversion. It may compose a Spring Data interface for actual CRUD or use an appropriate query tool directly. Reuse the framework's generated access code instead of implementing it again.

Construct public DTOs from values inside that implementation. Use a separate Mapper only for a distinct conversion responsibility or repeated mapping. Do not add another Adapter or forwarding Service over the same contract.

Use the concrete type names in [Java naming](object-and-method-style.md#naming).

## JPA Entities and relationships

<a id="jpa-003"></a>
### Use ordinary JPA data construction and access

**JPA-003 · MUST**

Give JPA its required protected no-argument constructor. Allow value-based construction and simple getters/setters for the storage role. Entity accessors only read or assign values; they do not decide business policy or interpret DTOs.

The repository implementation loads an Entity, applies already-decided values, and lets the transaction persist the result. Services use the public repository contract rather than manipulating Entity fields.

With field access, JPA does not require setters. Create an Entity with prepared values for insertion. For ordinary updates, simple assignment to a managed Entity is sufficient; do not force an Entity rebuild or an UPDATE query merely to avoid a setter.

Spring Data save selects persist or merge according to new-state detection. Rebuilding a partial Entity and merging it is not a PATCH operation: omitted state can overwrite existing values. Choose a direct UPDATE for a concrete query requirement, using the bulk-DML guidance below. Do not establish several update strategies or field-by-field enforcement machinery as a style prerequisite.

<a id="jpa-004"></a>
### Avoid generated behavior that weakens JPA entities

**JPA-004 · MUST NOT**

Do not use the following on a JPA Entity:

- `@Data`
- A public no-argument or public all-arguments constructor
- A class-level builder
- Automatic `toString()`
- Lombok-generated `@EqualsAndHashCode`
- Jackson annotations for API serialization

<a id="jpa-005"></a>
### Model required relationships with explicit lazy loading

**JPA-005 · MUST**

Do not turn every foreign key into an object relationship. Declare a relationship only when actual traversal is needed within the same Aggregate and lifecycle boundaries align. Use explicit `FetchType.LAZY` by default for relationships, including `ManyToOne` and `OneToOne`.

Do not hide N+1 behavior with EAGER loading. Resolve it according to the Use Case with an appropriate fetch join, EntityGraph, QueryDSL projection, Query Repository, or batch fetch, and inspect the generated SQL. Reference another business owner's Aggregate by identifier by default.

<a id="jpa-006"></a>
### Use cascading only for owned lifecycles

**JPA-006 · MUST**

Use cascading and `orphanRemoval` only when the parent genuinely owns the child's lifecycle. Do not use `CascadeType.ALL` for convenience between independent Aggregates.

<a id="jpa-007"></a>
### Keep persistence relationships consistent inside the implementation

**JPA-007 · MUST**

Use bidirectional JPA relationships only when both traversal directions are actually needed. Keep both sides consistent in the persistence implementation while constructing or assigning storage state.

Expose public repository results as data values, not mutable Entity collections. Do not require an Entity add/remove business method, a relationship helper class, or a generic association framework to satisfy the mapping.

<a id="jpa-008"></a>
### Define entity equality only for a real need

**JPA-008 · MUST**

Implement JPA Entity equality explicitly only for a real need such as use as a Set element or Map key, while accounting for proxies, pre- and post-persistence identifiers, and hash stability. Do not base equality unconditionally on a database-generated nullable identifier. A JpaEntity with no special need should retain reference identity. Use a stable Domain identifier for Domain Entity equality when required, and value equality for Value Objects.

## Repositories and query tools

<a id="query-001"></a>
### Keep repositories focused on persistence

**QUERY-001 · MUST**

Treat an Aggregate Repository as a persistence boundary for lookup and storage. It must not perform:

- Role or authorization composition
- State-transition, approval, discount, or refund decisions
- Controller Response construction
- A mixture of provider calls and database persistence
- Hidden partial commits within the overall business transaction

<a id="query-002"></a>
### Separate complex reads when responsibilities differ

**QUERY-002 · SHOULD**

Separate a `...QueryRepository` when a complex query's result and reason to change materially differ from Aggregate persistence. Do not create both a formal Command Repository and Query Repository for a simple domain.

<a id="query-003"></a>
### Choose the simplest suitable query tool

**QUERY-003 · MUST**

Choose the simplest clear tool for the query purpose.

| Purpose | Default choice |
|---|---|
| Single lookup by identifier, Aggregate save or delete, short fixed conditions | Spring Data JPA |
| Optional search criteria, dynamic filters, sorting and pagination, nearby joins | QueryDSL JPA with `JPAQueryFactory` |
| Many-table joins, UNION, complex aggregation, database functions, reports, database-specific expressions | QueryDSL SQL, JPASQLQuery, or managed Native SQL |

Determine in order whether QueryDSL JPA is clear and efficient, whether QueryDSL SQL offers useful type safety, and whether Native SQL is the more direct contract. Do not treat Native SQL itself as a failure.

<a id="query-004"></a>
### Prefer composition for QueryDSL repositories

**QUERY-004 · MUST NOT**

Do not require every QueryDSL implementation to extend `QuerydslRepositorySupport`. Use composition with `JPAQueryFactory` by default when the project has no different established standard.

<a id="query-005"></a>
### Make bulk update behavior and bypassed rules explicit

**QUERY-005 · MUST**

Direct QueryDSL/JPQL UPDATE and native DML do not synchronize already-managed Entity state automatically. JPQL bulk updates also bypass automatic optimistic version checks. Business decisions must already have been made before persistence. Use them only for an explicit reason such as large-scale operations, Batch, migration, or existing-SQL compatibility. Track the following in code and tests:

- Bypassed Domain rules and allowed states
- Transaction scope
- Persistence-context flush, clear, and synchronization behavior
- Re-execution and idempotency
- Expected and actual affected-row counts

## QueryDSL

<a id="query-006"></a>
### Limit nullable predicates to simple optional filters

**QUERY-006 · MUST**

Permit a nullable `BooleanExpression` helper only for a simple optional `AND` condition inside an infrastructure query adapter.

```java
private BooleanExpression cityCodeEquals(final String cityCode) {
    if (cityCode == null || cityCode.isBlank()) {
        return null;
    }

    return member.cityCode.eq(cityCode);
}
```

Do not extend this convention into permission for `null` returns in the Domain, Application, or general Repository code. When the project uses nullness annotations, mark the nullable return semantics.

<a id="query-007"></a>
### Compose authorization scopes and complex conditions explicitly

**QUERY-007 · MUST**

Represent complex OR groups, parenthesized conditions, authorization Scopes, and empty collections with a `BooleanBuilder`, explicit Predicate composition, or a Scope type. Do not convert an empty authorization range to `null` and accidentally perform an unrestricted query. A Predicate helper may handle value presence, SQL comparison, date ranges, and search escaping; it must not interpret roles, access sessions, query a Repository, or call an external service.

<a id="query-008"></a>
### Keep QueryDSL types inside infrastructure

**QUERY-008 · MUST NOT**

Do not expose Q-types, `BooleanExpression`, or QueryDSL annotations through Domain or Application contracts. Do not create a global `QueryDslUtils` or universal Predicate builder that accepts Q-types from other business areas.

<a id="query-009"></a>
### Use explicit query results and stable pagination

**QUERY-009 · MUST**

Receive a complex query in a typed internal QueryRow or projection, not Object[], a raw Map, or a partially initialized Entity. Publish a repository ResultDto constructed from values. A plain DTO projection may be used directly when no internal representation is needed. Do not attach @QueryProjection to a public application or repository DTO.

Use stable ordering and a tie-breaking identifier for pagination. Map client-provided sort strings to query paths through an allowlist. Separate a count query when it need not repeat joins from the data query, and verify duplicate rows and in-memory pagination caused by fetch joins against the actual SQL.

## SQL

<a id="sql-001"></a>
### Keep complex SQL near its owning business code

**SQL-001 · SHOULD**

When the project uses business modules, keep complex SQL near the owning code. Use business-purpose filenames such as `find-authorized-members-for-export.sql` and `summarize-daily-coupon-redemptions.sql`; do not use `query1.sql`, `common.sql`, or `temp.sql`.

Place complex joins, aggregations, CTEs, UNIONs, database-specific functions, compatibility behavior, or performance-tuning history in a separate file when they need to be read and verified as an independent contract. A short fixed native query may remain in Java code when the project manages that convention consistently.

<a id="sql-002"></a>
### Make SQL inputs and results explicit

**SQL-002 · MUST**

- Do not use `SELECT *`.
- Declare returned columns and QueryRow aliases explicitly.
- Do not concatenate external input into SQL strings; prefer meaningful named parameters.
- Qualify column ownership when several tables are involved.
- Do not rely on default database ordering, and add a tie-breaking identifier for pagination.
- Express a date range as `start <= value < end` where practical.
- Distinguish `NULL`, empty string, zero, and Y/N semantics.
- Do not maintain status codes and business literals independently across several SQL statements.
- Do not retain commented-out historical SQL.

<a id="sql-003"></a>
### Document complex SQL contracts and ownership

**SQL-003 · MUST**

Make the owning business area, purpose, read and write tables, result-row meaning, database-specific syntax, time-zone and period boundaries, deduplication, null handling, actual compatibility rationale, when applicable, and related tests traceable for complex or database-specific SQL. Do not copy a verbose comment template into every file; document only information that code and tests do not reveal.

For write SQL, make the owned tables, allowed states, expected row count, re-execution safety, follow-up behavior, and persistence-context handling explicit.

<a id="sql-004"></a>
### Respect each business area's table ownership

**SQL-004 · MUST NOT**

Do not modify tables owned by another business area. Keep cross-area read SQL in a read-only query implementation; translate any internal QueryRow into its public repository result. Ownership of that result contract does not transfer ownership of source-data meaning or write authority.

<a id="sql-005"></a>
### Verify database-specific queries on the supported database

**SQL-005 · SHOULD**

Verify database-specific syntax and complex queries against the actual supported database for:

- Empty results, NULL values, duplicates, and period boundaries
- Stable sorting and pagination
- Result equivalence with existing SQL
- Affected-row counts for bulk operations
- Execution plans and performance criteria at a representative scale

Do not treat passing H2 tests as proof of production-database behavior specific to CUBRID, PostgreSQL, Oracle, or another database.
