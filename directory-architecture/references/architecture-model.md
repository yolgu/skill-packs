# Architecture Decision Model

Use this document as the single source of truth for framework-neutral directory and module decisions.

## Contents

1. Distinguish the representations
2. Describe modules with contracts
3. Infer Bounded Contexts
4. Select the primary directory axis
5. Apply layer responsibilities
6. Assign ownership
7. Control shared code and integration
8. Consider deployment, teams, and trust
9. Detect structural smells

## 1. Distinguish the Representations

Do not use one structure to stand in for all architectural views.

| View | Answers | Typical form |
|---|---|---|
| Problem-space map | Which business capabilities exist? | Subdomains |
| Model boundary map | Where is a model and language consistent? | Bounded Contexts and Context Map |
| Module graph | Who may depend on whom? | Directed graph and public interfaces |
| Directory tree | Where are source files placed? | Folders and packages |
| Runtime view | Which components call or publish to others? | Ports, adapters, events |
| Deployment view | What ships and fails independently? | Processes, services, packages |
| Ownership view | Who changes and governs each area? | Team or owner map |

A directory can provide a useful public surface only when the project also defines which entry points are public, which paths are internal, and how the rule is verified.

## 2. Describe Modules with Contracts

Use this conceptual schema when a module boundary affects design or enforcement. Tailor the level of detail to the task; do not generate empty fields for trivial modules.

~~~yaml
ModuleContract:
  identity:
    name: ordering
    path: src/domains/ordering
    kind: bounded-context
  scope:
    business_context: Ordering
    architectural_role: mixed
  responsibility: Accept and progress customer orders
  public_surface:
    commands:
      - PlaceOrder
    queries:
      - GetOrder
    events:
      - OrderPlaced
  internal_surface:
    - domain/model
    - infrastructure/persistence
  required_interfaces:
    - CatalogProductSnapshot
    - PaymentAuthorization
  dependencies:
    allowed:
      - app/contracts
    forbidden:
      - domains/billing/infrastructure
  ownership:
    data:
      - orders
      - order_lines
    migrations:
      - ordering migrations
    configuration:
      - order expiry policy
    routes:
      - /orders
    events:
      - OrderPlaced
  invariants:
    - An order cannot be confirmed without at least one line
  owner:
    - ordering team
  verification:
    - module boundary test
~~~

### Required Contract Questions

For each significant directory or package, answer:

1. What single responsibility makes this unit cohesive?
2. What may consumers use without reading internals?
3. Which paths must remain internal?
4. What does the unit require from other modules?
5. Which data, migrations, routes, configuration, and events does it own?
6. Which dependencies are allowed and forbidden?
7. How will the contract be checked?

If these answers are unclear, a new abstraction or top-level directory is premature.

## 3. Infer Bounded Contexts

### Strong Signals

Give more weight to business evidence than to the current folder names.

| Signal | Boundary implication |
|---|---|
| The same word has different definitions or invariants | Separate model boundaries are likely |
| Rules and terminology change together | Keep them in one context |
| A transaction must maintain one set of invariants atomically | Keep that consistency boundary together |
| One group owns the data and accepts changes to its meaning | Strong ownership boundary |
| Consumers need only a stable published contract | Hide the producer's internals |
| Separate regulatory or trust requirements apply | Introduce a harder boundary |
| Code is commonly changed together for the same business reason | Increase cohesion |
| Code is reused separately and changes for unrelated reasons | Separate it |

### Weak Signals

Do not decide a Bounded Context from these alone:

- one database table
- one REST resource
- one screen or route
- one CRUD noun
- one framework package
- one team at a moment in time
- one deployable service
- repeated file names such as service or manager

### Subdomain, Context, Module, and Aggregate

- A **Subdomain** describes a business problem area.
- A **Bounded Context** defines where one domain model and language apply.
- A **Module** organizes code and exposes a contract inside or across a context.
- An **Aggregate** protects an invariant and transaction boundary inside a context.
- A **Directory** is one physical representation of a module.

Do not mechanically map one concept to another.

### Context Integration

When contexts collaborate, identify the relationship and translation point. Prefer explicit APIs, published events, or anti-corruption adapters. Do not share internal entities, ORM models, or mutable database records as integration contracts.

## 4. Select the Primary Directory Axis

### Default

For systems with meaningful business behavior, organize first by Bounded Context or cohesive business capability. Add layers inside each context when the code warrants them.

~~~text
domains/
├── ordering/
│   ├── presentation/
│   ├── application/
│   ├── domain/
│   └── infrastructure/
└── billing/
    └── ...
~~~

This keeps code that changes for the same business reason close and prevents global technical folders from becoming coupling hubs.

### Small or Technical Applications

A simple application with little domain behavior may use a smaller feature or framework-native structure. Do not manufacture DDD vocabulary or four empty layers.

### Vertical Slices

Use a vertical feature slice when a user-visible behavior has its own input, use case, rules, adapter interaction, and tests. Keep shared domain invariants in domain objects rather than duplicating them across slices.

### Cross-Context Features

Place a cross-context user journey in an application-level feature or process manager that orchestrates published context interfaces. Do not move the participating contexts' business rules into the feature.

### Composition Scope

Use app, bootstrap, or config for system-wide composition:

- dependency injection and implementation wiring
- process startup
- root routing
- environment loading and validation
- global middleware or interceptors
- top-level error conversion

Composition is a logical module with a contract, but it is not a business domain.

## 5. Apply Layer Responsibilities

Dependencies point inward. The exact folder names may follow the framework, but responsibilities do not change.

### Domain

Own:

- entities and aggregates
- value objects
- domain services when behavior belongs to no one object
- domain events
- business policies and invariants
- repository or gateway abstractions when the domain requires them

Must not depend on:

- HTTP requests or responses
- framework decorators and containers
- ORM records or database clients
- UI components or navigation objects
- filesystem, queues, caches, or third-party SDKs

### Application

Own:

- use cases and application services
- command and query orchestration
- transaction orchestration
- authorization decisions that require use-case context
- ports needed to coordinate external effects
- explicit application result types

Keep business invariants in Domain. Keep framework input conversion in Presentation.

### Infrastructure

Own:

- repository and gateway implementations
- ORM mapping
- database migrations when colocated with the owning context
- HTTP, queue, cache, filesystem, and third-party adapters
- serialization at external boundaries

Infrastructure implements inward-defined contracts. It does not decide business outcomes.

### Presentation

Own:

- controllers, route modules, pages, screens, view models
- request, route, form, or gesture input conversion
- response and rendering conversion
- page-local state and lifecycle
- expected presentation states

Presentation calls Application or a narrow query interface. It does not contain domain rules or persistence decisions.

### Composition

Own:

- concrete dependency wiring
- global configuration loading
- root router composition
- middleware registration
- process or application startup

Composition may know concrete adapters. Inner layers must not depend on Composition.

## 6. Assign Ownership

### Data and Migrations

- Give every table, collection, file format, or durable state one logical owning context.
- Keep migrations with the owner even when multiple contexts share one physical database.
- Other contexts use the owner's published interface or an explicitly governed read model.
- Treat direct cross-context writes as a severe boundary violation.
- Treat direct reads as an exception requiring scope, owner, and removal condition unless the data is explicitly published for reading.

### Configuration

Scope configuration to the narrowest owner:

| Scope | Examples | Location |
|---|---|---|
| Page | table columns, page-local feature presentation | page directory |
| Context | cancellation window, mapping policy, domain feature switch | context config |
| Application | environment endpoints, root routes, DI, global middleware | app/bootstrap/config |

Keep one source of truth for every key, default, schema, and mapping. Validate environment and external configuration at the composition boundary.

### Routes

- Let a domain page or controller own its route descriptor or endpoint contract.
- Let the application router compose owned route descriptors.
- If the framework derives routes from files, keep route files thin and delegate to domain-owned modules.
- Do not treat URL nesting as proof of a domain boundary.

### Events

- The producer owns the published event contract.
- Consumers translate the event into their own language.
- Version or evolve published contracts deliberately.
- Do not expose the producer's internal entity as an event payload.

## 7. Control Shared Code and Integration

### Technical Shared

Move code into technical shared only when it is:

- domain-neutral
- used by multiple real consumers
- stable for the same reason across those consumers
- free of inward dependencies on business modules

Examples include a design-system primitive, a generic clock adapter contract, or domain-neutral tracing support.

### Shared Kernel

Use a Shared Kernel only when:

- the shared model has real business meaning
- all participating contexts intentionally co-own it
- changes are coordinated
- the kernel is smaller than duplicating or translating the concept

Otherwise prefer duplicated local models with explicit translation.

### Cross-Cutting Concerns

Put technical mechanics such as logging, tracing, authentication-context propagation, serialization, and retry transport in middleware, interceptors, decorators, or adapters. Put business decisions such as refund eligibility and approval rules in Domain.

### Public Surface and Internals

Expose a small stable surface through the ecosystem's native mechanism:

- package exports or index entry points
- module descriptors
- package visibility
- explicit interfaces and event contracts

Block deep imports into internals. A public barrel that re-exports everything is not encapsulation.

### Package Cohesion and Stability

- Group code that changes for the same reason; separate code that changes for unrelated reasons.
- Do not force a consumer to depend on a large package when it uses only a small, independently varying part.
- Treat a reusable published package as a coherent release and versioning unit.
- Keep the module dependency graph acyclic.
- Direct dependencies toward stable contracts and owned public surfaces rather than volatile implementations.
- A stable module that must support variation should expose a narrow abstraction, but do not add an interface without a real boundary or variation.
- Balance cohesion against excessive fragmentation: a smaller folder count is preferable when separate units would always change, test, and release together.

## 8. Consider Deployment, Teams, and Trust

### Deployment

Logical modularity comes first. Split a module into an independent deployment only when evidence supports at least one material need:

- independent release cadence
- independent scaling
- data sovereignty
- fault isolation
- distinct runtime constraints
- stable team ownership

Record the additional operational cost and integration model.

### Team Ownership

Use ownership as evidence and a governance mechanism, not as the sole business model. A module should have one accountable owner even when contributors span teams.

### Trust and Regulation

Security, privacy, tenancy, and regulation can require a stricter sub-boundary within one business context. Enforce it with runtime authorization and data controls as well as folder placement.

## 9. Structural Smells

Investigate these patterns rather than automatically rewriting them:

- global controllers, services, and repositories containing unrelated domains
- domain code importing framework, ORM, HTTP, or UI types
- pages calling database or raw network clients
- deep imports into another context's internal folders
- bidirectional or cyclic module dependencies
- shared folders containing business-specific code
- one table written by several contexts
- migrations stored outside the data owner
- global config containing context-specific business policy
- context config duplicated in global settings
- one generic service, manager, helper, or utils package with many change reasons
- route structure mechanically copied into the domain model
- empty layer folders added only to match a template
- service boundaries with no independent operational need

For each smell, trace actual consumers and change reasons before choosing a correction.

## Sources

- [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- [DDD Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html)
- [On the Criteria To Be Used in Decomposing Systems into Modules](https://doi.org/10.1145/361598.361623)
- [Principles and Patterns](https://objectmentor.com/resources/articles/Principles_and_Patterns.pdf)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
- [How Do Committees Invent?](https://www.melconway.com/Home/Committees_Paper.html)
- [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/)
