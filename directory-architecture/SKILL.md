---
name: directory-architecture
description: Design, audit, or refactor backend and frontend directory architectures when domain boundaries, module contracts, dependency direction, configuration ownership, routing ownership, or framework-native boundary verification matter. Do not use for routine edits that do not change project structure or architectural boundaries.
---

# Directory Architecture

Treat a directory tree as the physical projection of logical modules with explicit responsibilities, public surfaces, ownership, and dependency contracts. Do not treat folders, layers, bounded contexts, aggregates, and deployment units as interchangeable concepts.

## Choose the Operating Mode

Infer the mode from the request and preserve its authorization boundary.

- **Design:** Propose a target structure. Remain read-only when the user asks to design, recommend, explain, review, or compare.
- **Audit:** Diagnose an existing structure and report evidence-backed violations. Remain read-only unless the user also asks for changes.
- **Refactor:** Create, move, rename, or reorganize files when the user asks to create, apply, restructure, organize, migrate, or refactor. Treat that request as authorization for safe, in-scope implementation and verification.

An explicit do-not-change constraint takes precedence. Otherwise, an explicit create, apply, migrate, or refactor instruction authorizes mutation for the stated scope even when the same request also asks for design or review.

Do not turn an advisory request into a mutation. Do not pause between ordinary analysis, safe edits, import repairs, and verification during an authorized change.

## Investigate Before Designing

Discover facts from the project instead of asking the user to repeat them.

1. Start with broad semantic or code search for the system flow and business capabilities.
2. Inspect manifests, build files, workspace configuration, entry points, bootstrapping, root routing, and global settings.
3. Trace routes or controllers through application use cases and domain behavior to repositories, schemas, migrations, and external adapters.
4. Inspect imports, public exports, package visibility, cycles, tests, fixtures, configuration keys, and generated-code conventions.
5. Identify the existing naming style, file layout, dependency direction, and the current source of truth for each rule.
6. Infer boundaries from vocabulary, business invariants, transaction scope, data ownership, change coupling, security constraints, and team ownership.

Trace important symbols to definitions and consumers. A directory name is evidence, not proof of a boundary.

Do not ask about facts available in code or configuration. When business information is incomplete, choose the most evidence-backed, reversible structure and report assumptions with confidence. Ask only when no safe reversible choice exists and a wrong decision would cause material or hard-to-recover consequences.

## Model the Boundary

For every non-trivial task, read [references/architecture-model.md](references/architecture-model.md) before deciding the structure.

Represent each meaningful module with a ModuleContract:

- identity and physical path
- architectural role and bounded-context scope
- one clear responsibility
- public and internal surfaces
- provided and required interfaces
- allowed and forbidden dependencies
- ownership of data, migrations, configuration, routes, and events
- invariants, owner, exceptions, and verification

Keep these representations distinct:

- **Context map:** business model and integration relationships
- **Dependency graph:** logical compile-time or runtime edges
- **Directory tree:** physical placement
- **Deployment topology:** process or service boundaries

## Apply the Core Decisions

- Prefer Bounded Context or cohesive business capability as the primary business axis.
- Put layers inside a context only when the responsibilities exist; do not create empty ceremonial folders.
- Keep dependencies directed inward: Presentation → Application → Domain, with Infrastructure implementing inward-defined ports and Composition wiring implementations.
- Keep framework, HTTP, ORM, database, and UI types outside the Domain boundary.
- Treat app, bootstrap, or config as a system composition scope, not a business domain.
- Keep domain-specific configuration with its owning context.
- Distinguish domain-neutral technical shared code from an explicitly co-owned Shared Kernel.
- Let event producers own published contracts; let consumers translate them.
- Let security, regulation, and trust boundaries subdivide a business context when necessary.
- Start with logical modularity; split deployment units only when independent deployment, scaling, data sovereignty, fault isolation, or ownership provides concrete evidence.
- Preserve framework-required paths while keeping their entries thin when those paths do not match the domain structure.

Do not force one universal tree. Prefer familiar framework names such as controller, repository, and config when they accurately express the role.

## Handle Existing Structures

For an audit or refactor, read [references/audit-and-migration.md](references/audit-and-migration.md).

- Map the current structure before proposing moves.
- Separate observed facts from inferred boundary hypotheses.
- Report concrete paths and dependency evidence for each finding.
- Compare plausible boundaries and select the strongest one rather than presenting arbitrary alternatives.
- Migrate one Bounded Context or vertical slice at a time.
- Update imports, exports, routing, dependency injection, configuration, tests, and build metadata with each move.
- Avoid unrelated cleanup and speculative abstractions.

## Verify Boundaries

Before enforcing rules or completing a refactor, read [references/verification.md](references/verification.md).

Prefer tools already present in the project and framework-native mechanisms. Add a new dependency only when its benefit is material and the request authorizes it. Verify observable behavior as well as directory shape.

## Load Only Relevant Framework Guidance

Read only the references that match the detected stack:

- Spring: [references/backend/spring.md](references/backend/spring.md)
- Django: [references/backend/django.md](references/backend/django.md)
- React: [references/frontend/react.md](references/frontend/react.md)
- Vue: [references/frontend/vue.md](references/frontend/vue.md)
- React Native: [references/frontend/react-native.md](references/frontend/react-native.md)
- Flutter: [references/frontend/flutter.md](references/frontend/flutter.md)

For a full-stack repository, load the relevant backend and frontend references together. Framework references contain only ecosystem-specific deltas; the architecture model remains the source of truth.

Use [references/evaluation-scenarios.md](references/evaluation-scenarios.md) only when creating, validating, or revising this skill, not during ordinary project work.

## Keep Authorized Work Moving

During an authorized change, continue through:

~~~text
discovery → provisional design → edits → reference repair → verification
→ failure correction → re-verification → result
~~~

Stop only for:

- destructive or difficult-to-recover changes outside an established recovery path
- a material expansion beyond the requested repository, system, or authority
- external effects on deployments, production data, accounts, or other people that were not requested
- incompatible boundary choices with no safe reversible default and materially different consequences
- missing credentials or permissions that cannot be worked around safely

Ordinary uncertainty is not a stopping condition. Record the assumption, choose the narrowest reversible option, and proceed.

## Report the Result

Lead with the outcome. Include only sections relevant to the task:

- evidence and assumptions
- context or module boundary map
- target directory tree
- ModuleContracts
- allowed and forbidden dependencies
- ownership of data, migrations, configuration, routes, and events
- current violations and their impact
- incremental migration plan
- explicit BoundaryExceptions
- verification commands and results
- remaining risks

Explain in the user's language. Use ecosystem-standard English names for code and directories.

Return reports in the conversation by default. Create a permanent architecture document only when the user requests it or the project already has an established architecture-document location.
