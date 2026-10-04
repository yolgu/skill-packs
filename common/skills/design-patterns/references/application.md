# Patterns for Persistence Access and Business Rules

Consider practical patterns needed to clarify responsibilities in the current code. Do not expand this into a process for redefining the entire domain model or system architecture. First check the responsibilities already owned by the frameworks in use and the project's contracts.

## Persistence Access: Repository

- **When to consider it:** Business-facing query and persistence contracts must be separated from data access and mapping mechanisms.
- **Alternatives and distinctions:** Reuse the current repository or data access tool when it already provides the required contract. Do not add a generic repository that merely forwards ordinary CRUD. Its role may overlap with Adapter for external API contract conversion, but a repository expresses business-facing access to a collection of data.
- **Minimal form and cost:** Define the required query and persistence contracts and their implementation. Follow the project's contract for public models and return forms. Query expressiveness, conversion, and maintaining the boundary have costs.

A repository provides a contract for querying and changing a collection of stored objects. Assess the value of hiding storage technology details behind that contract; do not add a differently named layer on top of an existing repository without that value.

## Tracking and Coordinating Changes: Unit of Work

- **When to consider it:** A responsibility is needed to track objects changed within one business unit of work and coordinate persistence and concurrency handling.
- **Alternatives and distinctions:** First check whether the ORM session or persistence context already handles it. Distinguish the role of Unit of Work from that of a database transaction. Wrapping independent commits to multiple repositories in one object does not make them atomic.
- **Minimal form and cost:** Use existing change tracking and commit boundaries, and implement only actual missing responsibilities. Clarify transaction scope, partial failure, and when changes take effect. Do not broaden the scope into distributed processing coordination.

Identify both the owner of change tracking and the mechanism that guarantees atomic persistence. Collecting changed objects and guaranteeing that all of their changes are stored together are different things.

## Expressing Conditions Independently: Specification

- **When to consider it:** There is a real requirement to name, combine, and reuse eligibility or selection conditions.
- **Alternatives and distinctions:** A meaningful function may suffice for a single condition. Unlike Strategy, which changes how work is performed, Specification expresses whether a condition is satisfied. If reasons for the decision are also needed, represent a result that meets that requirement.
- **Minimal form and cost:** Define condition evaluation and only the combinations actually needed. If the same condition must run both in memory and in the database, check that its meaning remains equivalent. Do not switch to reading all data and checking it afterward.

Represent AND, OR, and NOT combinations when they are actually needed. Do not grow a single eligibility decision into a general-purpose rule engine. If conditions have side effects or depend on evaluation order, first check whether they can be composed freely.

## Meaning and Value Equality: Value Object

- **When to consider it:** Values such as coordinates or a time period form one meaningful concept, and equality must be based on value rather than identity. A single primitive value can also be a candidate when it has independent meaning and rules.
- **Alternatives and distinctions:** For simple value transfer, compare using an existing record or data structure. Do not wrap every string and identifier. Distinguish it from an entity with its own identity and lifecycle.
- **Minimal form and cost:** Express the meaningful value, its necessary operations, and value equality. Keeping it immutable usually clarifies sharing and comparison. Consider serialization, persistence conversion, and language-specific equality implementation costs.

The defining idea is determining sameness by value. Distinct instances containing the same coordinates can be equal by value. In languages where reference equality differs from value equality, make the necessary comparison contract explicit. Do not add a structure that rechecks established validity in every method.

## Assembling Dependencies: Dependency Injection

- **When to consider it:** An object needs to receive the collaborators required for its role rather than selecting or locating concrete collaborators internally.
- **Alternatives and distinctions:** Keep direct construction when it is a cohesive internal implementation detail. Unlike separating creation responsibility, the focus is the contract for what the consumer receives. Needing injection and needing a container are separate questions.
- **Minimal form and cost:** Pass the necessary roles through constructor or function arguments and select implementations at the composition point. Do not make consumers search for dependencies through a service locator. Manage composition responsibility and lifetimes.

Dependency injection means that a consumer receives the collaborators it needs from outside. With a service locator, the consumer accesses a lookup point to find collaborators, so it depends on that lookup mechanism itself. Exposing the required roles through constructor or function arguments makes composition and consumption responsibilities easier to distinguish.

## Normal Behavior for Absence: Null Object

- **When to consider it:** Absence is a normal situation with clearly defined behavior, and the same absence branch recurs.
- **Alternatives and distinctions:** Compare whether an optional value or explicit result type communicates absence more clearly. Do not merge failure, missing configuration, and normal absence into one no-op object.
- **Minimal form and cost:** Provide absence behavior that satisfies the same contract. Check the meaning of the result the caller receives, because failures that must be reported or required actions could otherwise be silently skipped.

For example, a no-op implementation can be appropriate when doing nothing is the normal contract for a disabled optional feature. Using that same implementation for a failed external connection required by a mandatory feature would hide the failure and is inappropriate.

## Combining Conditions Versus Explaining Failures

Needing only a condition's truth value differs from needing to show the user every reason for failure. Short-circuiting a combination at its first failure is not the same contract as collecting all validation errors. Distinguish condition evaluation from error collection according to the result needed.

If a condition queries a repository or changes external state, composition order and call count can affect results. Compare making it a pure decision over facts with collecting the required facts once in advance. Preserve evaluation semantics when converting between framework query conditions and business conditions.

## Value Immutability and Public Contracts

When an immutable object holds a mutable list, its value semantics depend on whether outside code can change that list. Check what existing immutable collections or creation contracts already guarantee, and break sharing only at necessary boundaries. If values used in equality or as keys in hash-based collections change while in use, lookups can fail.

Hiding the current time or external service queries inside a value object can make an operation with the same input produce different results depending on when it is called. Decide whether to pass current context as input or assign the work to a separate business calculation based on the actual responsibility.

Compare business-rule ownership and consistency boundaries in [Domain models and business flows](domain-models.md), and storage representation and concurrent updates in [Persistence and query patterns](persistence.md).
