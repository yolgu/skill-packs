# Domain, Validation, and Authorization Rules

## Table of contents

- [Entities and Value Objects](#entities-and-value-objects)
- [Domain Services and Events](#domain-services-and-events)
- [Validation and Optional](#validation-and-optional)
- [Business authorization model](#business-authorization-model)
- [Authorization enforcement and query scope](#authorization-enforcement-and-query-scope)

## Entities and Value Objects

### DOMAIN-001 — MUST

Implement an Entity as an object that owns identity, state transitions, invariants, and meaningful behavior, not as a field container. Make a Service invoke the Entity's business verbs instead of assembling state through several setters.

```java
public void redeem(
    final MemberId memberId,
    final LocalDateTime redeemedAt
) {
    ensureIssued();
    ensureNotExpiredAt(redeemedAt);

    redemption = CouponRedemption.of(memberId, redeemedAt);
    status = CouponStatus.REDEEMED;
}
```

### DOMAIN-002 — SHOULD

Separate factories when new construction and persisted-state reconstruction have different meanings.

- `create`, `issue`, `register`: apply new-object rules and initial state
- `restore`: reconstruct a valid persisted state

Restrict access to `restore` where practical, and do not let ordinary business code use it as a path around invariants.

### DOMAIN-003 — MUST

Use a Value Object when at least one of the following has real meaning:

- Dedicated validation or normalization
- Unit and precision
- Value equality
- Risk of confusing values with the same primitive type
- Repeated calculations
- Several values forming one business concept

By default, make a Value Object a `final` class with `private final` fields, no public setters, value equality, defensive collection copies, and a meaningful factory. Do not wrap every database primary key and every string mechanically.

### DOMAIN-005 — MUST NOT

When the Domain model is separated as its own layer, do not make it depend on Spring, Jakarta Persistence, HTTP, sessions, database drivers, QueryDSL Q-types, provider SDKs, or file and messaging implementations. Keep Domain inputs and returns in business types and Java standard types.

### DOMAIN-006 — MUST

Do not call nondeterministic sources such as `LocalDateTime.now()`, `Instant.now()`, or `UUID.randomUUID()` inside the Domain. Pass the reference time and identifiers established once by the Application.

## Domain Services and Events

### DOMAIN-004 — SHOULD

Use a Domain Service, Policy, or Calculator only for a pure business decision or calculation that does not belong naturally to one Entity or Value Object. Name it according to its actual role.

Do not make a Domain Service handle HTTP, start transactions, implement a Repository, call a provider, manipulate a JPA Entity, convert DTOs, or orchestrate application-call order.

### DOMAIN-007 — SHOULD

When the project already uses Domain Events, express a completed business fact in the past tense. Do not put a JPA Entity, HTTP Request, provider SDK object, Spring Event type, unnecessary personal data, or mutable collection in an Event.

Do not introduce an Event Bus, Message Broker, or Outbox solely as a style change. An explicit Application Port call may be more appropriate for a simple follow-up effect.

## Validation and Optional

### VALIDATION-001 — MUST

Divide validation responsibilities as follows.

| Layer | Responsibility |
|---|---|
| Presentation | Required values, length, basic format and range, relationships within the Request, Content-Type, and file size |
| Application | Target existence, duplicate checks requiring external state, another Aggregate's state, business authorization, work Context, and call order |
| Domain and Value Object | State transitions, invariants, meaningful normalization, and rules that every entry point must guarantee |
| Database constraint | Final data-integrity protection, including concurrency |

Use the project's `@Valid` and boundary-validation approach rather than listing syntactic validation `if` statements in a Controller. Translate a database constraint violation into a meaningful failure in Infrastructure.

### VALIDATION-002 — MUST

A similar format constraint may exist at the HTTP boundary for faster feedback, but keep the Domain as the final owner of business rules and repeated constraint values. For example, do not maintain coupon-code length, travel-period ordering, or monetary scale independently across annotations, constants, and services.

### VALIDATION-003 — MUST NOT

Do not inject a Repository, provider Client, session, current user, or authorization Policy into a custom Bean Validator. Perform validation requiring external state in the Application Use Case.

### VALIDATION-004 — MUST

Use the following input-processing order by default and assign normalization to one owner.

```text
Deserialize external request
→ Validate boundary syntax
→ Convert to application input
→ Normalize and semantically validate Value Objects
→ Verify application preconditions
→ Execute domain behavior
→ Persist
```

Do not independently `trim`, change case, or adjust dates for the same string in several layers.

### OPTIONAL-001 — MUST

Use `Optional<T>` as a return type only when a single lookup result may normally be absent. In a Use Case where the value must exist, convert absence to a meaningful exception with `orElseThrow`. Consider an explicit Result type when several absence reasons must be distinguished.

### OPTIONAL-002 — MUST NOT

Do not use Optional in:

- Method parameters
- Request, Response, or Application DTO fields
- Domain or JPA Entity fields
- Collection elements
- `Optional<List<T>>`

Encapsulate a nullable internal Domain state; an external query method may return Optional. Interpret a nullable JPA value at the mapper boundary.

### OPTIONAL-003 — MUST

Return an empty collection, not `null`, when a plural query has no result. Use `orElseGet` for an Optional fallback with cost or side effects, and do not repeat `isPresent()` and `get()` combinations.

## Business authorization model

### AUTH-001 — MUST

Separate these concepts:

- Role: a relatively stable organizational responsibility or job function
- Permission or Action: the business operation being attempted
- Attribute: a fact about the user, target, or environment
- Policy: a decision combining Role, Action, Attribute, and target state

Do not proliferate roles for assigned city, language, organization, target ownership, or a specific account exception.

### AUTH-002 — MUST

Make a Use Case request authorization for a business Action, not a string role.

```java
authorization
    .decide(
        adminContext.getActor(),
        adminContext.getWorkContext(),
        MemberManagementAction.EXPORT_MEMBERS
    )
    .requireAllowed();
```

### AUTH-003 — MUST

Define authorization policies by owning business area, such as members, coupons, or advertisements. Do not collect all authorization in one global `AuthorizationService`. Limit shared types to stable concepts such as `AuthorizationDecision`, common denial semantics, and small rule combinations that actually repeat.

### AUTH-004 — MUST

Centralize legacy role codes, specific account identifiers, session city, region, and language, role-specific capabilities, target ownership and state, and internal operations-account exceptions in a domain-specific compatibility Policy implementation. Do not make the Controller, SQL, or UI reinterpret the same conditions.

### AUTH-005 — SHOULD NOT

When multiple roles perform the same operation, express the shared Permission first. Do not create role inheritance before a stable subset relationship is established. Do not introduce a general authorization DSL or rule engine before AND/OR conditions actually repeat; first express the existing rules explicitly inside the domain Policy.

## Authorization enforcement and query scope

### AUTH-006 — MUST

Do not load all data and filter authorization in Java. Make the Policy calculate an explicit allowed Scope, and make the query adapter translate that Scope into SQL predicates.

```java
final AuthorizedMemberScope authorizedScope =
    authorization.resolveScope(
        adminContext.getActor(),
        adminContext.getWorkContext(),
        MemberManagementAction.SEARCH_MEMBERS
    );

return memberQueryRepository.search(query, authorizedScope);
```

Do not let the query adapter decide role codes or specific-account exceptions. Never interpret an empty Scope as no condition and return all data.

### AUTH-007 — MUST

- `isAllowed()`: inspect a decision for menu, button, or capability presentation
- `requireAllowed()`: enforce a protected query, create, update, delete, approval, download, external transmission, or manual Batch execution

Invoke `requireAllowed()` in the Application Use Case immediately before actual business execution. Ensure the check remains present when another inbound adapter invokes the same Use Case.

### AUTH-008 — MUST

Deny unknown Role, Action, and Attribute combinations and an empty allowed Scope by default. Do not expose policy details such as internal role lists, hidden administrator accounts, or the existence of another organization in a denial response.

### AUTH-009 — MUST NOT

Do not treat hiding a UI button as security enforcement. Do not duplicate the same role condition in Controller SpEL, query predicates, and frontend menus. When a UI capability is required, use the Backend Policy result as the single source of truth, but do not automatically implement an out-of-scope capability API or a new authorization database.
