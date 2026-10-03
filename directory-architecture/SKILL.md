---
name: directory-architecture
description: Design, audit, or refactor directory and package boundaries around cohesive responsibilities, public contracts, internal implementations, model ownership, and allowed imports. Covers backend and frontend framework paths and boundary verification. Excludes routine source edits that do not affect structure or module boundaries.
---

# Directory Architecture

## Scope and Mode

Map logical responsibilities to directories, packages, and modules. Each significant directory has a role, a public surface, internal paths, and permitted consumers. A directory is not automatically a bounded context, aggregate, or deployment unit.

This skill is independently usable. Its references own physical placement and package-boundary decisions, without requiring another skill.

Design and audit requests are read-only. An explicit request to apply or refactor authorizes in-scope moves, reference repairs, and verification; continue through those steps without intermediate approval unless the user requests a checkpoint.

## Inspect the Actual Boundary

Trace representative capabilities from their entry points to data or external systems. Inspect source roots, manifests, imports, public exports, runtime discovery, composition, routes, migrations, configuration ownership, and tests.

Distinguish the compile-time type graph from runtime calls. Return types, conversion parameters, annotations, and generic arguments can expose an internal package even without a direct call to its implementation.

Read [Architecture Model](references/architecture-model.md) before deciding a non-trivial structure. It defines directory responsibilities, contract questions, ownership, public/internal placement, and module dependencies. Keep the representation proportional to the task; do not create a contract file for every folder.

For existing structures, read [Audit and Migration](references/audit-and-migration.md). Separate observed edges from inferred boundaries, then move the smallest coherent slice and repair its imports, discovery, wiring, routing, and tests.

## Framework References

Read only the references for the actual stack:

| Stack | Reference |
|---|---|
| Spring | [Spring](references/backend/spring.md) |
| Django | [Django](references/backend/django.md) |
| React | [React](references/frontend/react.md) |
| Vue | [Vue](references/frontend/vue.md) |
| React Native | [React Native](references/frontend/react-native.md) |
| Flutter | [Flutter](references/frontend/flutter.md) |

Keep required framework paths and discovery mechanisms. Do not apply a Java class-naming convention or a Spring package example to every frontend or backend.

## Verify and Report

Read [Boundary Verification](references/verification.md) before enforcing a rule or completing a move. Use available resolver, module, build, and behavior checks; distinguish a manually reviewed boundary from an enforced one.

Report the responsibility map, relevant paths and dependency edges, repairs, verification evidence, and material exceptions. Prefer a concise response; create a permanent architecture document only when requested or required by the project's established documentation practice.

Read [Evaluation Scenarios](references/evaluation-scenarios.md) when revising or validating this skill, not during ordinary project work.
