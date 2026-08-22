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

Do not add every possible layer folder. A small module may expose one facade and keep a domain model plus one adapter without extra ceremony.

## Map Familiar Spring Names to Roles

| Spring name | Architectural role |
|---|---|
| controller | inbound Presentation adapter |
| application service or use case | Application orchestration |
| entity, aggregate, value object | Domain behavior and invariants |
| repository interface | inward-required persistence port |
| Spring Data repository or repository implementation | Infrastructure adapter |
| event listener | inbound adapter or cross-module integration adapter |
| configuration class | Composition for concrete wiring |
| scheduler or message listener | inbound adapter |

The package name service does not establish whether code is Application or Domain. Inspect its responsibility.

## Keep the Domain Inward

- Do not pass HttpServletRequest, ResponseEntity, Spring MVC types, message records, or database rows into Domain.
- Convert controller input into validated application or domain types at the edge.
- Keep business rules on entities, value objects, domain services, or policies rather than controllers and Spring configuration.
- Define repository and gateway contracts inward when they protect a boundary.
- Implement them with Spring Data, JDBC, JPA, messaging, or third-party SDKs in Infrastructure.
- Avoid duplicate domain and persistence models when they add no boundary value, but do not leak a volatile ORM mapping into a domain that is intended to stay framework-independent.

Follow the existing transaction strategy. A transaction should protect one context's invariant boundary; do not use a broad transaction as a substitute for explicit context integration.

## Composition and Configuration

Keep these near ShopApplication or a bootstrap/config package:

- concrete bean wiring
- environment property binding and validation
- top-level security filter chains
- root web or messaging configuration
- global serialization and error conversion

Keep context-specific properties and mapping with the owning context. Expose a typed configuration value to Domain or Application rather than letting inner code read Environment or global property objects directly.

Do not use ComponentScan expansion to erase module boundaries.

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

Add a focused test around ApplicationModules.of(...).verify() when Spring Modulith is used. Keep allowedDependencies consistent with the ModuleContract.

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

