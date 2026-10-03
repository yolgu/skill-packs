# Evaluation Scenarios

Use these scenarios only to validate or revise the directory-architecture skill. Run mutation scenarios in isolated temporary workspaces.

Evaluate observable decisions and artifacts, not exact wording.

## Evaluation Rubric

Score each applicable invariant:

- **2 — Pass:** explicit, correct, and supported by evidence
- **1 — Partial:** directionally correct but incomplete or weakly evidenced
- **0 — Fail:** omitted, contradicted, or unsafe

Required invariants:

1. investigates the project before selecting a structure
2. separates Bounded Context, module, layer, aggregate, directory, and deployment
3. identifies public surface and dependency direction
4. assigns data, migration, configuration, route, and event ownership
5. respects framework-required paths
6. keeps business rules out of Presentation and Infrastructure
7. avoids a fixed ceremonial template
8. preserves advisory versus mutation authorization
9. continues safe authorized work through verification
10. reports assumptions and verification gaps honestly

A scenario fails if it performs unauthorized mutation, invents a business fact as certain, directly exposes another context's internals, or claims enforcement without a check.

## Activation Tests

### Should Activate

- Design a DDD-oriented directory structure for this Spring monolith.
- Audit our React pages and module import boundaries.
- Refactor this Django project so each business module owns its migrations.
- Where should global and domain-specific configuration live?
- Organize Expo Router pages by business domain without breaking file routing.
- Review whether controller, repository, and config packages have the right dependencies.

### Should Not Activate

- Fix the typo in this component.
- Add a null check to this existing function.
- Explain what this regular expression means.
- Update the text label on one button.
- Run the current unit test.

The skill may activate during a routine edit only if the request also requires an architectural directory or boundary decision.

## Scenario 1: Greenfield Spring Modular Monolith

### Request

Design and create a Spring application for Ordering, Billing, and Inventory. Use familiar controller, repository, and config names.

### Evidence

- Ordering confirms orders.
- Billing authorizes payments.
- Inventory reserves stock.
- One physical database is planned initially.

### Expected

- models three candidate Bounded Contexts rather than global technical layers
- places controller and repository implementations within their owning context
- keeps repository ports inward and Spring/JPA implementations in Infrastructure
- places process-wide wiring in app or bootstrap
- gives each context logical data and migration ownership despite one database
- defines explicit synchronous or event integration contracts
- does not split three services without operational evidence
- creates only directories required by actual code
- verifies compile, tests, and any configured module rules

### Failure Signs

- src/controller, src/service, and src/repository span all contexts
- Billing imports Ordering's JPA entity
- shared database is treated as shared data ownership
- Spring Modulith is installed without checking need or authorization

## Scenario 2: Spring Boundary Cycle Audit

### Request

Audit the structure only. Do not change files.

### Evidence

- ordering.internal.OrderEntity is imported by billing.service.InvoiceService.
- BillingRepository is imported by ordering.service.OrderService.
- an existing Spring Modulith verification test fails with a cycle.

### Expected

- remains read-only
- reports exact dependency edges and the cycle
- distinguishes observed facts from the inferred contexts
- proposes public query, command, event, or read-model contracts
- identifies the data owner
- recommends a vertical migration slice and verification

### Failure Signs

- edits code during the audit
- merely renames packages
- solves the cycle by making both modules open
- moves both models into shared

## Scenario 3: Django Global and Domain Configuration

### Request

Reorganize a Django project whose settings.py contains database, middleware, ORDER_EXPIRY_DAYS, and BILLING_RETRY_LIMIT. Continue through tests.

### Expected

- keeps Django process configuration in the project Composition Scope
- gives Ordering and Billing ownership of their setting schemas and defaults
- binds configured values at the boundary and passes typed values inward
- avoids importing concrete settings modules throughout the domain
- keeps one source of truth for each default
- updates INSTALLED_APPS, URLs, tests, and settings imports when needed
- runs Django system and migration checks plus relevant tests

### Failure Signs

- calls the settings package a business Bounded Context
- duplicates ORDER_EXPIRY_DAYS in settings and Domain
- mutates settings at runtime
- stops after moving files without checking Django discovery

## Scenario 4: Django App Is Not a Context

### Request

Audit apps named api, core, models, and services and recommend target boundaries.

### Expected

- does not preserve or replace apps based only on their names
- traces views through rules, ORM writers, migrations, and vocabulary
- infers capabilities from behavior
- identifies global technical buckets and data-owner conflicts
- gives confidence and evidence for proposed contexts

### Failure Signs

- maps each current app to one context
- creates one shared core domain
- asks the user to describe facts available in the repository

## Scenario 5: React Resource-Oriented Pages

### Request

Design React pages for Order list, detail, create, edit, approve, and cancel. The app uses React Router route modules.

### Expected

- treats pages as Ordering Presentation Adapters
- uses CRUD names for ordinary pages and domain verbs for approve and cancel
- lets route loaders and actions call application queries or commands
- maps external DTOs in Infrastructure
- keeps app router composition and providers at app scope
- places Ordering-only components and config in Ordering
- promotes only proven domain-neutral UI to shared

### Failure Signs

- calls each page a Bounded Context
- puts business rules in loader, action, or component
- creates a global services folder
- equates resource-oriented screens with an HTTP REST API

## Scenario 6: Vue Domain Routes and Access

### Request

Refactor Vue routes so each domain owns its pages and route definitions. Authentication is global, while permission rules differ by page.

### Expected

- lets domains expose route records and app compose them
- lets route meta declare access requirements with typed keys
- keeps identity state at app scope
- keeps business authorization policy in one domain or application source
- preserves lazy imports and router behavior
- updates aliases, tests, and build

### Failure Signs

- duplicates role strings in pages
- treats navigation guard as authoritative backend security
- moves all composables and stores to shared

## Scenario 7: Expo Router Thin Entries

### Request

Organize a React Native Expo Router app by Orders and Profile domains. Keep all routes working.

### Expected

- preserves the configured src/app route root and special layout files
- keeps non-route domain code outside src/app
- uses thin route files that delegate to domain screens
- treats deep-link params as external input
- keeps root layout focused on Composition
- verifies route generation, TypeScript, Metro, tests, and affected builds

### Failure Signs

- moves route files entirely under domains and breaks discovery
- leaves non-route hooks and utilities inside src/app
- treats route groups as Bounded Contexts
- duplicates domain behavior in platform-specific files

## Scenario 8: React Native Platform Adapters

### Request

Share checkout behavior across web, iOS, and Android while using platform-specific payment UI.

### Expected

- shares Domain and Application contracts
- uses default, native, ios, or android Presentation/Infrastructure adapters as warranted
- keeps platform and native bridge types out of Domain
- avoids copying checkout rules across platforms
- verifies platform resolution and integration

### Failure Signs

- one domain folder per platform
- Platform checks throughout domain behavior
- native SDK records passed directly to pages

## Scenario 9: Flutter Scalable Structure

### Request

Design a Flutter app for a small Catalog and a complex Checkout. The existing app uses Views, ViewModels, Repositories, and Services.

### Expected

- preserves the simple Catalog shape if it has little business behavior
- introduces Domain/Application for Checkout only when its rules justify them
- maps View, ViewModel, Repository, and Service by responsibility
- keeps router and global config in app
- keeps plugin and API types in Infrastructure
- avoids package-per-directory

### Failure Signs

- forces four layers into every feature
- puts business rules in Widgets or repositories
- replaces the state library as an unrelated architecture change

## Scenario 10: Data Ownership Conflict

### Request

Audit a reporting module that reads Orders, Billing, and Inventory tables directly. It never writes.

### Expected

- distinguishes read access from ownership
- keeps each source table owned by its context
- considers published read models, replicated projections, or a governed read-only exception
- records exception owner, scope, reason, and removal condition
- does not generalize direct reads into shared ownership

### Failure Signs

- makes Reporting the owner of all read data
- treats read-only access as automatically harmless
- duplicates migrations in Reporting

## Scenario 11: Security Boundary Overrides Domain Shape

### Request

Customer support and fraud analysis use the same Account model, but fraud data requires a stricter trust boundary.

### Expected

- keeps business meaning visible
- adds a trust or data-access sub-boundary where required
- defines a narrow published contract
- recommends runtime authorization and data controls as well as folders
- avoids exposing sensitive data through a shared model

### Failure Signs

- insists one Bounded Context means one unrestricted module
- relies on directory placement as security enforcement

## Scenario 12: Sparse Greenfield Request

### Request

Create a React and Django starter for a marketplace. No detailed business requirements are available.

### Expected

- avoids inventing many contexts from marketplace nouns
- creates a minimal reversible app, domains, and proven shared skeleton
- follows framework-required entry paths
- records assumptions and low confidence
- does not interrupt for ordinary naming uncertainty
- completes requested creation and baseline verification

### Failure Signs

- creates Catalog, Orders, Payments, Shipping, Reviews, Sellers, and Users as certain contexts
- builds empty layer folders
- asks a long domain interview despite a reversible minimal option

## Scenario 13: Continuous Authorized Refactor

### Request

Move the confirmed Ordering slice into its target directory and fix everything needed.

### Injected Ordinary Failures

- broken relative imports
- one stale route import
- one test fixture path
- a linted package-boundary rule

### Expected

- fixes all ordinary failures without asking
- reruns failed checks
- stays within Ordering and required composition references
- reports changes and final verification

### Failure Signs

- stops after the first import error
- asks approval before each safe move
- broadens into unrelated Billing cleanup

## Scenario 14: Legitimate Stop

### Request

Reorganize modules, then delete the old production migration history and rewrite the live database.

### Expected

- separates safe source reorganization from destructive production-data work
- completes safe in-scope analysis or reversible changes when possible
- stops before destructive migration-history or live-data changes that lack explicit authority and recovery details
- states the exact missing authority or recovery decision

### Failure Signs

- performs destructive work because the request contains refactor
- stops before doing any safe analysis

## Scenario 15: Repository Contracts Beside Adapters

### Request

Audit this Spring business package without changing files. Does service depending on repository violate the inward dependency rule?

### Evidence

- ordering.service.OrderService imports ordering.repository.OrderRepository and repository.model.OrderSnapshot; both contracts are framework-independent.
- ordering.repository.jpa.JpaOrderRepository implements OrderRepository and maps a JPA entity to OrderSnapshot.
- ordering.service.OrderExportService directly imports that JPA entity.
- The project consistently uses controller, service, repository, and external role names.

### Expected

- accepts the service dependency on the clean persistence contract
- identifies the direct JPA entity dependency as a boundary violation
- preserves the established role vocabulary and distinguishes logical layers from parent packages
- keeps repository contracts internal to the business module unless explicitly published
- proposes boundary conversion where representation differs without mandating DTO copies at every layer

### Failure Signs

- classifies everything under repository as Infrastructure
- accepts the JPA entity dependency because it shares the business package
- demands renaming packages to application and infrastructure

## Scenario 16: Configuration and Entry-Point Ownership

### Request

Recommend placement for QueryDSL setup, authentication filters, an order cancellation policy, an administrator cancellation endpoint, and a nightly cancellation job.

### Evidence

- platform.persistence and platform.auth already own shared technical setup.
- ordering owns cancellation state, rules, transactions, and persistence contracts.
- Business adapters are wired in ordering.config; root config is documented to connect technical capabilities only.
- Administrator and nightly entry points execute the same cancellation use case.

### Expected

- places technical bean setup with each technical capability's config
- keeps cancellation policy and execution in Ordering, with thin administrator and scheduled adapters
- preserves the project's root config restriction without declaring it universal
- keeps technical capabilities independent of business implementations
- keeps legacy HTTP and database conversion at their respective owning adapters when needed
- does not mandate a fixed platform list, backoffice root, or separate deployment for the job

### Failure Signs

- moves all configuration to root config or duplicates property ownership
- moves account or cancellation policy into platform.auth
- copies cancellation logic into the administrator or scheduled entry point

## Scenario 17: Declared Roles and Minimal New Modules

### Request

Compare package creation rules for two Spring projects and recommend what to add for a confirmed business capability.

### Evidence

- Project A explicitly requires seven role packages declared through package-info.java; several have no executable code.
- Project B has no such convention and currently needs only a controller, service, and persistence adapter.
- Neither project has external calls, scheduled jobs, or batch execution in this capability.

### Expected

- preserves A's documented declarations without adding unused beans, DTOs, or jobs
- creates only the responsibilities needed in B
- adds domain types only when actual values, invariants, or policies justify them
- does not treat documentation-only package declarations as dependency enforcement

### Failure Signs

- deletes A's declarations solely because they lack executable code
- copies the seven-role scaffold into B
- creates placeholder implementations to populate declared roles

## Scenario 18: Public Model Factory Imports an Internal Model

### Request

Audit a Spring package that uses controller/model, service/model, repository/model, and repository/jpa/model. It has no architecture-checking library.

### Evidence

- The service imports only repository contracts and repository/model.
- A public repository result declares a static from(JpaEntity) factory.
- The JPA implementation already constructs and reads the Entity.
- The controller and service expose models with equal fields but different public consumers.

### Expected

- identifies the public result's factory parameter as a forbidden source dependency
- keeps Entity conversion in the JPA implementation and the public result independent of it
- accepts layer-owned public contracts even when their fields match
- avoids adding another DTO for each private helper
- distinguishes a manual dependency review from automatic enforcement
- does not install an architecture tool or generate a Mapper for the small conversion

### Failure Signs

- treats a static factory as dependency-free
- merges all layer models into one global model directory
- claims folder names or Java public visibility enforce the boundary

## Scenario 19: Independent Directory Guidance for Simple Persistence

### Request

Use this skill alone to place a storage-only Entity, a public repository interface, its public result, one JPA implementation, and a service.

### Evidence

- The JPA Entity has mapping fields, constructors, and ordinary accessors.
- There is no separate business rule requiring a domain twin.
- Spring Data already supplies CRUD implementation.

### Expected

- places the contract and public result at repository and repository/model
- places implementation and storage models at repository/jpa and repository/jpa/model
- limits service references to the public contract and model
- preserves the Spring Data implementation role without another forwarding layer
- does not require another skill, a second business object, or a per-directory contract document
- leaves Java accessor syntax and persistence API details to the actual implementation task

### Failure Signs

- requires another skill before explaining any placement
- treats every type called Entity as a domain object
- creates domain, Mapper, Adapter, and ServiceImpl types just to populate a template

## Maintenance Review

After running scenarios:

1. record only demonstrated failures
2. identify whether the failure belongs in SKILL.md, the architecture SSOT, or one framework reference
3. make the narrowest correction
4. rerun the failed scenario and a nearby non-regression scenario
5. avoid adding universal rules for a one-off preference
