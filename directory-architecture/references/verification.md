# Boundary Verification

Verify the contract, not only the folder shape. Select the smallest reliable mechanism that fits the detected project.

## Verification Order

1. Inspect existing build, lint, test, and architecture-check configuration.
2. Reuse the project's current package or module mechanism.
3. Add focused rules to an existing tool when authorized.
4. Add a lightweight architecture test when no current mechanism expresses the boundary.
5. Recommend a new dependency only when the rule is important, recurring, and cannot be checked reliably otherwise.

Do not replace a project's test runner or build system for this task.

## Contract Invariants

For each ModuleContract, check:

- only declared public entry points are imported
- internal paths are not imported from outside the owner
- forbidden dependency edges do not exist
- dependencies are acyclic at the intended module level
- Domain does not depend on Presentation, Infrastructure, or Composition
- data writes and migrations remain with one owner
- configuration has one schema and owner
- route files delegate to the owning page or controller
- event schemas are producer-owned and consumers translate them
- declared exceptions match their exact source, target, and scope

Directory naming alone cannot prove these invariants.

## General Static Checks

Use the language's actual resolver and build graph where possible.

- imports and package references
- public exports and module descriptors
- deep imports
- package visibility
- dependency cycles
- project references
- generated-code boundaries
- layer annotations or package markers

Exclude vendored, generated, cache, build-output, and dependency directories using the project's own conventions.

## Ecosystem Mechanisms

Use these only when the relevant ecosystem is detected.

### Spring and Java

- Spring Modulith module verification for application-module cycles, API exposure, and allowed dependencies
- ArchUnit rules when the project already uses ArchUnit or an architecture test is justified
- Java module descriptors when the project uses the Java module system
- package-private types and intentionally narrow exports

Verify Spring's runtime application context when module-level wiring changes.

### Django and Python

- explicit package entry points and underscore/internal conventions
- existing import-boundary tools if already configured
- focused tests that inspect forbidden imports when a durable rule is needed
- Django system checks, migration checks, and application tests

Python naming conventions alone are advisory. Do not claim enforcement unless a test or configured tool checks it.

### JavaScript and TypeScript

- package.json exports for package public surfaces
- ESLint import restrictions when ESLint is already present
- Nx enforce-module-boundaries when the repository uses Nx
- TypeScript project references or workspace package dependencies
- bundler and test resolution checks

Do not create broad barrel files that expose internals merely to simplify imports.

### Bazel

- visibility declarations for public and internal targets
- target-level dependency graph and cycle checks
- package groups only when several targets share the same intentional policy

### Go

- internal packages for compiler-enforced internals
- package import graph and cycle prevention
- small public packages with cohesive responsibilities

### Rust

- crate and module visibility
- workspace dependency graph
- pub, pub(crate), and private module surfaces

### Dart and Flutter

- Dart package public API under lib and internal implementation under lib/src
- analyzer and existing lint configuration
- separate packages when a real public boundary needs stronger enforcement
- Flutter unit, widget, and integration tests after route or presentation moves

Do not use a separate Dart package for every directory; reserve it for a meaningful public boundary.

## Runtime and Ownership Checks

Static imports do not expose every architectural edge. Also inspect:

- service locator or dependency injection lookups
- event publication and subscription
- queues and scheduled jobs
- direct database clients and raw queries
- cross-context table writes
- shared caches and filesystem paths
- environment-key access
- route registration and middleware order

Where possible, verify data ownership with integration tests or schema permissions. A folder rule cannot prevent an unauthorized runtime write by itself.

## Test Placement

- Domain rule tests stay with or near Domain.
- Application use-case tests verify orchestration through explicit inputs and outputs.
- Infrastructure integration tests verify adapters and mappings.
- Page, screen, widget, or component tests stay near Presentation.
- Module-boundary tests live at the narrowest scope that can observe the graph.
- End-to-end tests remain at the application or system scope.

Colocation communicates ownership, but tests should assert observable behavior rather than file placement alone.

## Verification After a Move

Determine the project's actual commands from manifests and CI. Run the narrowest relevant checks first, then broader checks in proportion to the change:

1. architecture or import-boundary check
2. focused domain or use-case tests
3. affected adapter or presentation tests
4. type check or compile
5. lint
6. broader test suite
7. build or framework system check

Repair failures caused by the authorized move and rerun the failed check. Do not rewrite unrelated failing tests.

## Adding Enforcement

Before adding a rule, identify:

- the ModuleContract invariant it protects
- the exact source and target scopes
- allowed exceptions
- the project's existing tool that can express it
- the command CI will run
- a negative fixture or representative violation proving that the rule catches the edge

Prefer a small explicit rule to a configurable universal checker.

## Verification Report

Report:

- commands or tools used
- which invariants they checked
- pass, fail, or not-run status
- failures fixed as part of the task
- pre-existing unrelated failures
- remaining gaps

Do not state that a boundary is enforced when it was only reviewed manually.

## Primary Documentation

- [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Node.js package exports](https://nodejs.org/api/packages.html#package-entry-points)
- [Bazel visibility](https://bazel.build/concepts/visibility)
- [Nx module boundary rule](https://nx.dev/features/enforce-module-boundaries)
- [Go internal directories](https://go.dev/doc/go1.4#internalpackages)
- [Java modules](https://openjdk.org/projects/jigsaw/spec/)
- [Rust visibility and privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html)
- [Dart package layout](https://dart.dev/tools/pub/package-layout)
