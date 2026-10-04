# Decisions in Java and Spring

Check the project's Java version, Spring configuration, and existing code contracts. Do not upgrade the language or change existing layers and public models just to implement a pattern. Use the criteria below to distinguish pattern implementation choices from responsibilities the framework already owns.

## Choosing Functions or Objects

If an interchangeable policy (Strategy) has one operation and no separate state or lifetime, compare a meaningful functional contract with a lambda or method reference. A small policy object may fit when several operations must remain coherent or when state or external dependencies are involved. Do not turn this into a fixed class set for each pattern.

An interface can be useful even with one implementation when a role isolates an external contract or requires actual substitution. There is no need for an interface/implementation pair for every internal collaborator. If the framework's extension contract requires inheritance, follow it without forcing business responsibilities into the common parent too.

## Creation and Container Lifetimes

- A named static creation method expresses creation intent. It is not by itself a Factory Method in which a subtype overrides a creation point.
- Use existing configuration and constructor injection to assemble dependencies. Do not recreate an equivalent factory layer on top of the container's construction configuration.
- Make selection responsibility explicit when a policy must be selected from several choices. Do not add a general-purpose registry when injecting one fixed policy is sufficient.
- Use existing contracts when a code generator supplies builders or value types. Do not create a separate Director merely because a builder exists or replace every constructor with a builder.

Spring's singleton scope is per container and bean definition. Do not confuse it with the GoF global-access structure or a guarantee that only one instance of a class exists across the entire process. If lifetime management is the goal, check whether an existing container scope suffices.

## Persistence and External Conversion

Before adding a Repository, check what Spring Data or the project's existing persistence contract provides. Compare extending the existing contract with introducing a separate repository. Do not stack generic repositories, mappers, and services that merely forward the same query to resemble a pattern.

An Adapter aligns external inputs, results, and failure meanings with the internal contract. One implementation may handle both the call and a simple conversion. Separate a Client or Mapper when it has an independent responsibility. Follow the project's existing contract for whether public results are domain objects or DTOs.

Do not reimplement change tracking (Unit of Work) or transactions already provided by the ORM and Spring. Use the actual entry-point contract to determine whether multiple operations must take effect as one business unit.

## Proxies and Wrapping

Check Spring's actual call path when changing behavior wrappers (Decorator) or call surrogates (Proxy). With proxy-based AOP, a direct call within the same object does not pass through the proxy. Moving a method or removing a wrapper can change whether transactions, caching, or other additional behavior apply.

Split a boundary only when a genuinely separate responsibility is needed, and verify proxy traversal through the behavior in question. Pure-object tests that bypass the proxy do not establish container behavior.

## Example Decisions

If one external place-query implementation produces a response different from the internal contract, a small contract and conversion implementation can be appropriate. Conversely, when two internal calculation branches are short and stable, retain explicit branching as the first choice. If creation and lifetimes are already configured, this decision does not require a separate factory or single-instance class.

## Shared Policy State and Actual Execution Paths

Storing request-specific members, reference times, or intermediate calculations in fields of a shared policy object lets another request overwrite them. Distinguish policy configuration from request facts, and first compare passing request-specific values as arguments. Receiving the same injected object is not evidence of thread safety.

A lambda capturing request state can have the same lifetime problems as an object. Do not assume something is stateless because it is a function. Check the lifetimes of retained functions and their captured references.

In projects that separate storage-only JPA entities from business objects, do not move behavior into existing JPA entities merely to introduce Domain Model. Express the required business objects within public-model and persistence contracts. Conversely, do not create a duplicate model with the same fields when there are no meaningful rules.

## Asynchronous Results and Actual Task Cancellation

Distinguish an object representing completion from the lifetime of the executing task. For example, canceling a CompletableFuture does not guarantee that in-progress I/O or a worker thread is automatically stopped. Check the cancellation contracts of the executor and client in use, and examine whether late results modify disposed state.

Use [Domain models and business flows](domain-models.md) for placing business rules, [Persistence and query patterns](persistence.md) for distinguishing persistence contexts from conflict handling, and [Concurrency and resource lifetimes](concurrency.md) for shared state and task lifetimes.
