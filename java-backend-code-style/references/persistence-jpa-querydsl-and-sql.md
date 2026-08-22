# JPA, QueryDSL, and SQL Rules

## Table of contents

- [Domain and JPA models](#domain-and-jpa-models)
- [JPA Entities and relationships](#jpa-entities-and-relationships)
- [Repositories and query tools](#repositories-and-query-tools)
- [QueryDSL](#querydsl)
- [SQL](#sql)

## Domain and JPA models

### JPA-001 — MUST

Decide whether to separate Domain and JPA models according to actual need.

Signals that separation is warranted include:

- Meaningful state transitions and invariants
- A mismatch between a legacy schema and the business model
- A multi-table Aggregate or a shared legacy table
- Composite keys, Y/N values, irregular columns, or database codes that distort the Domain
- A mismatch between JPA relationships and the Domain lifecycle
- Different write and read models
- Real value in isolating framework and database coupling

A combined model may be acceptable when the Aggregate is simple CRUD, the table and business object nearly match, lifecycle and ownership align, and a separate model would add no business meaning. Do not mechanically create an `Xxx` and `XxxJpaEntity` pair for every table, and do not mix strategies arbitrarily within one Aggregate.

### JPA-002 — MUST

Make a separated persistence model explicit as a storage representation with names such as `...JpaEntity`, `...QueryRow` for a complex read row, and `...PersistenceMapper` for conversion. Do not make a Domain or Application Repository extend a Spring Data Repository directly; have an infrastructure adapter combine Spring Data and a mapper. When models are separated, the Domain is the single source of truth for business rules.

## JPA Entities and relationships

### JPA-003 — MUST

Restrict a JPA Entity's no-argument constructor to protected access. In a combined Domain/JPA Entity, use business behavior methods rather than public setters. In a separated JpaEntity, expose only the minimum mutation paths required to create and restore persisted state, and do not place business Policies in it.

```java
@Entity
@Table(name = "MEMBER_TB")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class MemberJpaEntity {

    @Id
    @Column(name = "MEMBER_ID")
    private Long memberId;
}
```

### JPA-004 — MUST NOT

Do not use the following on a JPA Entity:

- `@Data` or class-level `@Setter`
- A public no-argument or public all-arguments constructor
- A class-level builder
- Automatic `toString()`
- Lombok-generated `@EqualsAndHashCode`
- Jackson annotations for API serialization

### JPA-005 — MUST

Do not turn every foreign key into an object relationship. Declare a relationship only when actual traversal is needed within the same Aggregate and lifecycle boundaries align. Use explicit `FetchType.LAZY` by default for relationships, including `ManyToOne` and `OneToOne`.

Do not hide N+1 behavior with EAGER loading. Resolve it according to the Use Case with an appropriate fetch join, EntityGraph, QueryDSL projection, Query Repository, or batch fetch, and inspect the generated SQL. Reference another business owner's Aggregate by identifier by default.

### JPA-006 — MUST

Use cascading and `orphanRemoval` only when the parent genuinely owns the child's lifecycle. Do not use `CascadeType.ALL` for convenience between independent Aggregates.

### JPA-007 — MUST

Expose an immutable view so external code cannot modify an Entity collection directly. Create a bidirectional relationship only when bidirectional traversal is actually needed, and have one meaningful `add/remove` method maintain both sides consistently.

### JPA-008 — MUST

Implement JPA Entity equality explicitly only for a real need such as use as a Set element or Map key, while accounting for proxies, pre- and post-persistence identifiers, and hash stability. Do not base equality unconditionally on a database-generated nullable identifier. A separated JpaEntity with no special need should retain reference identity. Use a stable Domain identifier for Domain Entity equality when required, and value equality for Value Objects.

## Repositories and query tools

### QUERY-001 — MUST

Treat an Aggregate Repository as a persistence boundary for lookup and storage. It must not perform:

- Role or authorization composition
- State-transition, approval, discount, or refund decisions
- Controller Response construction
- A mixture of provider calls and database persistence
- Hidden partial commits within the overall business transaction

### QUERY-002 — SHOULD

Separate a `...QueryRepository` when a complex query's result and reason to change materially differ from Aggregate persistence. Do not create both a formal Command Repository and Query Repository for a simple domain.

### QUERY-003 — MUST

Choose the simplest clear tool for the query purpose.

| Purpose | Default choice |
|---|---|
| Single lookup by identifier, Aggregate save or delete, short fixed conditions | Spring Data JPA |
| Optional search criteria, dynamic filters, sorting and pagination, nearby joins | QueryDSL JPA with `JPAQueryFactory` |
| Many-table joins, UNION, complex aggregation, database functions, reports, legacy equivalence | QueryDSL SQL, JPASQLQuery, or managed Native SQL |

Determine in order whether QueryDSL JPA is clear and efficient, whether QueryDSL SQL offers useful type safety, and whether Native SQL is the more direct contract. Do not treat Native SQL itself as a failure.

### QUERY-004 — MUST NOT

Do not require every QueryDSL implementation to extend `QuerydslRepositorySupport`. Use composition with `JPAQueryFactory` by default when the project has no different established standard.

### QUERY-005 — MUST

QueryDSL Update, JPQL Bulk, and Native DML bypass the persistence context and Domain behavior. Use them only for an explicit reason such as large-scale operations, Batch, migration, or existing-SQL compatibility. Track the following in code and tests:

- Bypassed Domain rules and allowed states
- Transaction scope
- Persistence-context flush, clear, and synchronization behavior
- Re-execution and idempotency
- Expected and actual affected-row counts

## QueryDSL

### QUERY-006 — MUST

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

### QUERY-007 — MUST

Represent complex OR groups, parenthesized conditions, authorization Scopes, and empty collections with a `BooleanBuilder`, explicit Predicate composition, or a Scope type. Do not convert an empty authorization range to `null` and accidentally perform an unrestricted query. A Predicate helper may handle value presence, SQL comparison, date ranges, and search escaping; it must not interpret roles, access sessions, query a Repository, or call an external service.

### QUERY-008 — MUST NOT

Do not expose Q-types, `BooleanExpression`, or QueryDSL annotations through Domain or Application contracts. Do not create a global `QueryDslUtils` or universal Predicate builder that accepts Q-types from other business areas.

### QUERY-009 — MUST

Receive a complex query result in a dedicated `...QueryRow`, `...Summary`, or `...Result`, not `Object[]`, a raw Map, or a partially initialized JPA Entity. Do not attach `@QueryProjection` to an Application Result; convert an infrastructure projection when necessary.

Use stable ordering and a tie-breaking identifier for pagination. Map client-provided sort strings to query paths through an allowlist. Separate a count query when it need not repeat joins from the data query, and verify duplicate rows and in-memory pagination caused by fetch joins against the actual SQL.

## SQL

### SQL-001 — SHOULD

When the project uses business modules, keep complex SQL near the owning code. Use business-purpose filenames such as `find-authorized-members-for-export.sql` and `summarize-daily-coupon-redemptions.sql`; do not use `query1.sql`, `common.sql`, or `temp.sql`.

Place complex joins, aggregations, CTEs, UNIONs, database-specific functions, compatibility behavior, or performance-tuning history in a separate file when they need to be read and verified as an independent contract. A short fixed native query may remain in Java code when the project manages that convention consistently.

### SQL-002 — MUST

- Do not use `SELECT *`.
- Declare returned columns and QueryRow aliases explicitly.
- Do not concatenate external input into SQL strings; prefer meaningful named parameters.
- Qualify column ownership when several tables are involved.
- Do not rely on default database ordering, and add a tie-breaking identifier for pagination.
- Express a date range as `start <= value < end` where practical.
- Distinguish `NULL`, empty string, zero, and Y/N semantics.
- Do not maintain status codes and business literals independently across several SQL statements.
- Do not retain commented-out historical SQL.

### SQL-003 — MUST

Make the owning business area, purpose, read and write tables, result-row meaning, database-specific syntax, time-zone and period boundaries, deduplication, null handling, legacy compatibility rationale, and related tests traceable for complex or database-specific SQL. Do not copy a verbose comment template into every file; document only information that code and tests do not reveal.

For write SQL, make the owned tables, allowed states, expected row count, re-execution safety, follow-up behavior, and persistence-context handling explicit.

### SQL-004 — MUST NOT

Do not modify tables owned by another business area. Isolate a query that joins several business areas' tables in a read-only Query Repository returning a dedicated QueryRow. Ownership of the query result contract does not transfer ownership of source-data meaning or write authority.

### SQL-005 — SHOULD

Verify database-specific syntax and complex queries against the actual supported database for:

- Empty results, NULL values, duplicates, and period boundaries
- Stable sorting and pagination
- Result equivalence with existing SQL
- Affected-row counts for bulk operations
- Execution plans and performance criteria at a representative scale

Do not treat passing H2 tests as proof of production-database behavior specific to CUBRID, PostgreSQL, Oracle, or another database.
