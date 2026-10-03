# Domain, Validation, and Authorization Rules

## Table of contents

- [Business objects and Value Objects](#business-objects-and-value-objects)
- [Domain Services and Events](#domain-services-and-events)
- [Validation and Optional](#validation-and-optional)
- [Business authorization model](#business-authorization-model)
- [Authorization enforcement and query scope](#authorization-enforcement-and-query-scope)

## Business objects and Value Objects

<a id="domain-001"></a>
### Express business behavior in plain Java objects

**DOMAIN-001 · MUST**

Implement an actual business concept as a plain Java class that owns its state and rules. An identity-bearing business object may protect transitions, but it is distinct from an @Entity storage mapping.

For example, a Coupon business object may expose redeem(memberId, redeemedAt) and reject expiry. CouponJpaEntity only represents storage; the repository converts between storage and its public data contract.

Introduce business objects only for actual concepts or rules. Simple CRUD can use service and repository DTOs without a second class mirroring every table. The [JPA reference](persistence-jpa-querydsl-and-sql.md#jpa-entities-and-relationships) defines persistence constructors and accessors.

<a id="domain-002"></a>
### Distinguish new construction from restoration

**DOMAIN-002 · SHOULD**

Separate plain business-object factories only when new creation and restoration of existing state have different semantics. Use the [construction names](http-dto-and-json-style.md#conversions) consistently. Restore valid business state without turning restoration into a bypass for ordinary business invariants.

<a id="domain-003"></a>
### Use value objects for meaningful domain values

**DOMAIN-003 · MUST**

Use a Value Object when at least one of the following has real meaning:

- Dedicated validation or normalization
- Unit and precision
- Value equality
- Risk of confusing values with the same primitive type
- Repeated calculations
- Several values forming one business concept

By default, make a Value Object a `final` class with `private final` fields, no public setters, value equality, defensive collection copies, and a meaningful factory. Do not wrap every database primary key and every string mechanically.

<a id="domain-005"></a>
### Keep a separated domain independent of frameworks

**DOMAIN-005 · MUST NOT**

Keep business objects independent of Spring, Jakarta Persistence, HTTP, sessions, database drivers, QueryDSL Q-types, provider SDKs, or file and messaging implementations. Keep Domain inputs and returns in business types and Java standard types.

<a id="domain-006"></a>
### Pass time and identifiers into the domain

**DOMAIN-006 · MUST**

Do not call nondeterministic sources such as `LocalDateTime.now()`, `Instant.now()`, or `UUID.randomUUID()` inside the Domain. Pass the reference time and identifiers established once by the Application.

## Domain Services and Events

<a id="domain-004"></a>
### Keep domain services focused on pure business decisions

**DOMAIN-004 · SHOULD**

Use a Domain Service, Policy, or Calculator only for a pure business decision or calculation that does not belong naturally to one business object or Value Object. Name it according to its actual role.

Do not make a Domain Service handle HTTP, start transactions, implement a Repository, call a provider, manipulate a JPA Entity, convert DTOs, or orchestrate application-call order.

<a id="domain-007"></a>
### Use domain events for completed business facts

**DOMAIN-007 · SHOULD**

When the project already uses Domain Events, express a completed business fact in the past tense. Do not put a JPA Entity, HTTP Request, provider SDK object, Spring Event type, unnecessary personal data, or mutable collection in an Event.

Do not introduce an Event Bus, Message Broker, or Outbox solely as a style change. An explicit Application Port call may be more appropriate for a simple follow-up effect.

## Validation and Optional

<a id="validation-001"></a>
### Validate each concern at its owning layer

**VALIDATION-001 · MUST**

Divide validation responsibilities as follows.

| Layer | Responsibility |
|---|---|
| Presentation | Required values, length, basic format and range, relationships within the Request, Content-Type, and file size |
| Application | Target existence, duplicate checks requiring external state, another Aggregate's state, business authorization, work Context, and call order |
| Domain and Value Object | State transitions, invariants, meaningful normalization, and rules that every entry point must guarantee |
| Database constraint | Final data-integrity protection, including concurrency |

Use the project's `@Valid` and boundary-validation approach rather than listing syntactic validation `if` statements in a Controller. Translate a database constraint violation into a meaningful failure in Infrastructure.

<a id="validation-002"></a>
### Keep business constraints under domain ownership

**VALIDATION-002 · MUST**

A similar format constraint may exist at the HTTP boundary for faster feedback, but keep the Domain as the final owner of business rules and repeated constraint values. For example, do not maintain coupon-code length, travel-period ordering, or monetary scale independently across annotations, constants, and services.

<a id="validation-003"></a>
### Keep external lookups out of Bean Validators

**VALIDATION-003 · MUST NOT**

Do not inject a Repository, provider Client, session, current user, or authorization Policy into a custom Bean Validator. Perform validation requiring external state in the Application Use Case.

<a id="validation-004"></a>
### Give normalization one owner

**VALIDATION-004 · MUST**

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

<a id="optional-001"></a>
### Use Optional for a single result that may be absent

**OPTIONAL-001 · MUST**

Use `Optional<T>` as a return type only when a single lookup result may normally be absent. In a Use Case where the value must exist, convert absence to a meaningful exception with `orElseThrow`. Consider an explicit Result type when several absence reasons must be distinguished.

<a id="optional-002"></a>
### Keep Optional out of fields and parameters

**OPTIONAL-002 · MUST NOT**

Do not use Optional in:

- Method parameters
- Request, Response, or Application DTO fields
- Domain or JPA Entity fields
- Collection elements
- `Optional<List<T>>`

Encapsulate a nullable internal Domain state; an external query method may return Optional. Interpret nullable JPA values inside the repository implementation.

<a id="optional-003"></a>
### Return empty collections and choose fallbacks carefully

**OPTIONAL-003 · MUST**

Return an empty collection, not `null`, when a plural query has no result. Use `orElseGet` for an Optional fallback with cost or side effects, and do not repeat `isPresent()` and `get()` combinations.

## Business authorization model

<a id="auth-001"></a>
### Distinguish roles, actions, attributes, and policies

**AUTH-001 · MUST**

Separate these concepts:

- Role: a relatively stable organizational responsibility or job function
- Permission or Action: the business operation being attempted
- Attribute: a fact about the user, target, or environment
- Policy: a decision combining Role, Action, Attribute, and target state

Do not proliferate roles for assigned city, language, organization, target ownership, or a specific account exception.

<a id="auth-002"></a>
### Authorize business actions rather than role codes

**AUTH-002 · MUST**

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

<a id="auth-003"></a>
### Give each business area its own authorization policy

**AUTH-003 · MUST**

Define authorization policies by owning business area, such as members, coupons, or advertisements. Do not collect all authorization in one global `AuthorizationService`. Limit shared types to stable concepts such as `AuthorizationDecision`, common denial semantics, and small rule combinations that actually repeat.

<a id="auth-004"></a>
### Keep required authorization compatibility local

**AUTH-004 · MUST**

When an actual supported contract contains old role codes, account exceptions, or session-based scope semantics, normalize them at the owning boundary and centralize the required decision in the business area's policy. Do not let Controller, SQL, and UI reinterpret those conditions.

Do not assume such a contract exists or create a compatibility Policy merely because code is being refactored.

<a id="auth-005"></a>
### Introduce authorization abstractions only for real repetition

**AUTH-005 · SHOULD NOT**

When multiple roles perform the same operation, express the shared Permission first. Do not create role inheritance before a stable subset relationship is established. Do not introduce a general authorization DSL or rule engine before AND/OR conditions actually repeat; first express the existing rules explicitly inside the domain Policy.

## Authorization enforcement and query scope

<a id="auth-006"></a>
### Translate authorized scopes into query conditions

**AUTH-006 · MUST**

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

<a id="auth-007"></a>
### Enforce authorization before protected actions

**AUTH-007 · MUST**

- `isAllowed()`: inspect a decision for menu, button, or capability presentation
- `requireAllowed()`: enforce a protected query, create, update, delete, approval, download, external transmission, or manual Batch execution

Invoke `requireAllowed()` in the Application Use Case immediately before actual business execution. Ensure the check remains present when another inbound adapter invokes the same Use Case.

<a id="auth-008"></a>
### Deny unknown permissions and empty scopes

**AUTH-008 · MUST**

Deny unknown Role, Action, and Attribute combinations and an empty allowed Scope by default. Do not expose policy details such as internal role lists, hidden administrator accounts, or the existence of another organization in a denial response.

<a id="auth-009"></a>
### Use backend authorization as the security authority

**AUTH-009 · MUST NOT**

Do not treat hiding a UI button as security enforcement. Do not duplicate the same role condition in Controller SpEL, query predicates, and frontend menus. When a UI capability is required, use the Backend Policy result as the single source of truth, but do not automatically implement an out-of-scope capability API or a new authorization database.
