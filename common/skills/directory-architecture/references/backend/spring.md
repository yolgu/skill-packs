# Spring Directory Boundaries

Apply the framework-neutral model in architecture-model.md. This document covers Spring-specific discovery, package conventions, and verification.

## Detect the Actual Spring Shape

Inspect:

- Maven or Gradle modules and source sets
- the class annotated with SpringBootApplication
- component-scan and entity-scan roots
- Spring Modulith or ArchUnit dependencies
- package-info.java or Kotlin module metadata
- controller, listener, scheduler, repository, and configuration beans
- JPA entities, migrations, transaction boundaries, and event publication
- test slices and application-context tests

Do not assume a Maven or Gradle subproject is a Bounded Context. Do not assume every Spring bean package is an architectural module.

## Prefer Business Modules Under the Application Root

A modular monolith can use one package per Bounded Context or cohesive capability:

~~~text
com.example.shop
├── ShopApplication
├── ordering
│   ├── OrderingFacade
│   ├── PlaceOrder
│   ├── application
│   ├── domain
│   ├── infrastructure
│   └── presentation
├── billing
│   └── ...
└── bootstrap
    └── ...
~~~

Keep the module's public surface small. If Spring Modulith is used, its default package model treats the application module's base package as its API and subpackages as internal. Place only deliberate public types at the base or expose a named interface explicitly.

A small module may expose one facade and keep a domain model plus one adapter without extra ceremony. The following role-oriented layout is equally valid when it matches the project's vocabulary.

## Role-Oriented Business Packages

Use controller, service, repository, and external when those are the project's role names. Do not add presentation, application, or infrastructure as competing synonyms inside the same capability.

~~~text
<business-capability>/
├── controller/
│   └── model/             # HTTP contracts
├── service/
│   └── model/             # application inputs and results
├── repository/
│   ├── ForecastRepository.java       # public persistence contract
│   ├── model/                         # public persistence inputs/results
│   └── jpa/
│       ├── JpaForecastRepository.java
│       ├── ForecastSpringDataRepository.java
│       └── model/                     # JPA mappings and internal query rows
├── external/
│   ├── model/             # provider-independent contract data
│   └── <provider>/
│       └── model/         # provider wire data
├── domain/                # actual business objects and rules, when needed
├── scheduler/
├── batch/
└── config/
~~~

The repository example has a public interface and one JPA implementation. Add the Spring Data interface only when Spring Data supplies actual database access. This does not require another Adapter, Mapper, or forwarding Service.

Each directory owns the role named by the tree. Create only roles used by the capability. A simple CRUD capability need not have a duplicate domain object for each JPA mapping. Preserve explicitly required package documentation without filling empty roles with unused code.

The allowed source edges are:

~~~text
controller / scheduler / batch → service and its public model
service → repository contract and model / external contract and model / domain
repository.jpa → repository contract and model / repository.jpa.model
external.<provider> → external contract and model / its own provider model
business config → locally owned contracts and implementations
~~~

The service does not import repository.jpa or a concrete external provider. Public model factories must also obey this rule: repository/model cannot take repository/jpa/model as an input type.

If client is the established integration name, apply the same layout to client/model and client/<provider>/model. Other business modules use a deliberately published application surface, not this capability's internal repository.

For Spring Modulith, align this layout with the configured module discovery and NamedInterface metadata. Java public visibility or the repository folder name does not automatically publish a cross-module API.

## Map Familiar Spring Names to Roles

| Spring name | Architectural role |
|---|---|
| controller | inbound Presentation adapter |
| application service or use case | Application orchestration |
| pure business object, aggregate, value object | Domain behavior and invariants |
| JPA entity | persistence implementation model |
| repository interface | inward-required persistence port |
| Spring Data repository or repository implementation | Infrastructure adapter |
| event listener | inbound adapter or cross-module integration adapter |
| configuration class | Composition for concrete wiring |
| scheduler or message listener | inbound adapter |

The package name service does not establish whether code is Application or Domain. Inspect its responsibility.

## Keep the Domain Inward

Keep pure business types under the domain owner and ORM records under the persistence implementation. Service contracts use their own models and repository public models; they do not expose JPA mappings, QueryDSL Q-types, or provider SDK types.

Domain packages do not import Spring MVC, Jakarta Persistence, database clients, provider implementations, or composition. Business rules belong with domain objects, while a storage-only capability can use its service and repository contracts without manufacturing domain types.

Preserve the transaction boundary and domain behavior while moving packages. A directory move does not authorize a different commit boundary or distributed consistency model.

## Composition and Configuration

Assign Spring configuration to the narrowest owner:

| Owner | Examples | Placement |
|---|---|---|
| Business capability | local bean selection, business-specific properties | business config |
| Shared technical capability | DataSource and QueryDSL beans, security filters, MVC/Jackson setup, scheduler engine, tracing | technical capability's config |
| Final application composition | process startup and wiring across owners | near the application class or bootstrap/config |

For a project with a platform package, platform.persistence.config can own shared persistence setup while each business repository owns its entities and queries. platform.auth.config can own authentication transport wiring while account policies and resource authorization remain business-owned. Names and the set of technical capabilities follow actual responsibilities.

A small application without distinct technical modules may keep these beans near its application class. Do not introduce platform merely to match the example. Preserve a documented restriction on root config dependencies when business wiring is local; do not impose that restriction on projects whose root composition assembles business adapters.

Keep context-specific properties and mapping with the owning context. Expose a typed configuration value to Domain or Application rather than letting inner code read Environment or global property objects directly.

Do not use ComponentScan expansion to erase module boundaries.

Administrative controllers may have their own entry package while calling the owning business service. Create a separate administrative business boundary only when its own model, such as operator identity, warrants it. Keep translation for a required existing HTTP or database contract under its actual owner; do not introduce a compatibility package without a separate responsibility.

## Data and Migrations

- Assign each entity mapping, table, and migration to one context.
- Keep module-specific migration resources visibly owned by that module when the build and migration tool support it.
- Do not let one module use another module's Spring Data repository implementation.
- Publish a command, query interface, event, or read model instead.
- Treat direct cross-context writes as a severe violation.

If the physical database is shared, retain logical schema and migration ownership.

## Events

- Define published event contracts in the producing module's public surface.
- Keep internal domain events internal unless they are deliberately published.
- Translate external events in the consuming module's adapter.
- Prefer events over direct bean coupling only when eventual consistency and failure behavior are acceptable.
- Test duplicate delivery, ordering, transaction publication, and retry semantics when they matter.

## Spring Modulith

Use Spring Modulith only when it is present or its addition is justified and authorized.

### Module Metadata

- Use ApplicationModule metadata to declare a module identity or allowed dependencies.
- Use NamedInterface for an intentionally exposed additional package.
- Reference a named interface with the module-and-interface notation supported by the installed version.
- Keep modules closed unless openness is a deliberate compatibility choice.

Do not annotate packages merely to make an accidental dependency pass. Change the code or ModuleContract first.

### Verification

ApplicationModules verification can check:

- cycles between application modules
- access to another module through its API rather than internals
- explicitly allowed dependencies when declared

Use the project's existing ApplicationModules.of(...).verify() check when present. Add focused coverage only for a changed boundary that it does not already verify. Keep allowedDependencies consistent with the ModuleContract.

### Module Tests

Use application-module tests to verify one module and the dependencies it intentionally includes. A module that needs many other modules' beans is evidence of high coupling; investigate the boundary instead of always widening the test bootstrap.

## ArchUnit

When ArchUnit is already present or a focused architecture test is warranted, encode stable invariants such as:

- domain packages must not depend on Spring MVC or persistence packages
- presentation may call application but not infrastructure implementations
- modules may access another module only through public packages
- the intended module graph is acyclic

Test a representative prohibited edge so the rule is known to catch violations.

## Verification

Determine the project's actual commands, then run relevant checks:

- Spring Modulith verification
- ArchUnit tests
- focused domain and application tests
- repository integration tests
- application-context or module tests
- compile, test, and build
- migration validation

After moving Spring components, verify component scanning, bean ambiguity, entity scanning, repository discovery, transaction behavior, and serialization.

## Avoid

- global controller, service, and repository packages spanning unrelated contexts
- public module roots that expose most internal types
- business decisions in controllers, bean configuration, serializers, or repositories
- direct use of another module's JPA entities or repositories
- configuration properties duplicated globally and inside a module
- events used to conceal an actually synchronous invariant
- allowed-dependency annotations that document accidental coupling

## Official Documentation

- [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Spring Modulith verification](https://docs.spring.io/spring-modulith/reference/verification.html)
- [Spring Modulith module testing](https://docs.spring.io/spring-modulith/reference/testing.html)
- [Spring Modulith runtime support](https://docs.spring.io/spring-modulith/reference/runtime.html)
