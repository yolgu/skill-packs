# Audit and Migration

Read this document for an existing project. Preserve the difference between diagnosing a structure and changing it.

## Audit Outcome

An audit must explain:

1. what the project currently does
2. which boundaries are observed
3. which boundaries are inferred
4. which dependency or ownership rules are violated
5. why each violation matters
6. the smallest coherent correction

A folder tree without import, call, and ownership evidence is not an audit.

## 1. Establish the Current Architecture

### Repository and Build Shape

Inspect:

- repository roots and workspaces
- build and package manifests
- source roots
- executable entry points
- generated-code roots
- test roots
- deployment units
- monorepo or package-boundary configuration

Do not move framework-owned or generated paths before understanding how they are discovered.

### Composition

Trace:

- application startup
- dependency injection
- root routing
- global settings and environment validation
- middleware, interceptors, and error conversion
- framework registration or plugin discovery

Identify whether composition concerns are duplicated inside business modules.

### End-to-End Flows

Start with representative capabilities, not isolated filenames. Trace:

~~~text
route/controller/page
→ input conversion
→ application use case
→ domain behavior
→ port
→ infrastructure adapter
→ data or external system
~~~

Trace return types, errors, and events back to their consumers.

### Dependency Graph

Inspect:

- imports and public exports
- deep imports
- compile-time package references
- runtime service lookups
- event subscriptions
- shared database access
- test-only boundary bypasses
- cycles

Distinguish production edges from test or tooling edges.

### Ownership

Build an ownership table.

| Asset | Current owner | Actual writers | Consumers | Evidence |
|---|---|---|---|---|
| table or state | module | modules | modules | repository and migration paths |
| migration | module | module | deployment | migration discovery |
| configuration key | scope | readers | readers | schema and access sites |
| route | page or controller | composer | callers | router registration |
| event | producer | publisher | consumers | schema and subscription |

Conflicting writers or duplicated configuration schemas are high-value findings.

## 2. Separate Facts from Hypotheses

Use explicit labels.

### Observed

Facts directly supported by source, configuration, tests, version control, or generated metadata.

Example:

> Observed: billing/repository imports ordering/internal/order.py and writes the orders table.

### Inferred

A boundary interpretation supported by several observations.

Example:

> Inferred with high confidence: Ordering owns the order lifecycle because its terminology, invariants, migrations, and write paths change together.

### Assumed

A reversible decision made because evidence is incomplete.

Example:

> Assumed with medium confidence: Refund is part of Billing until separate vocabulary or ownership appears.

Do not present assumptions as established business facts.

## 3. Compare Boundary Hypotheses

When the current structure is ambiguous, compare candidates using the same criteria.

| Criterion | Evidence to collect |
|---|---|
| Language cohesion | terms, type names, tests, user-facing copy |
| Rule cohesion | invariants and policies that change together |
| Transaction cohesion | atomic writes and consistency requirements |
| Data ownership | writers, migrations, schemas |
| Change coupling | files commonly changed for one capability |
| Public interface | stable commands, queries, events |
| Independence | separate consumers or release reasons |
| Trust boundary | permissions, tenancy, regulatory controls |
| Team ownership | accountable maintainers and review paths |

Choose the highest-evidence hypothesis. If two choices remain close, prefer the one with fewer cross-boundary writes, fewer cycles, a smaller public surface, and a more reversible migration.

Do not ask the user to choose between weakly researched alternatives. Ask only when business meaning cannot be recovered and the alternatives have materially different, non-reversible consequences.

## 4. Classify Findings

Use severity based on impact, not aesthetic preference.

### Critical

- cross-context write that can violate invariants or corrupt ownership
- trust or authorization boundary bypass
- migration ownership conflict that can damage data

### High

- dependency cycle across intended contexts
- Domain dependency on a volatile external framework or persistence implementation
- consumer reliance on another context's mutable internal model
- duplicated business rule with observable divergence

### Medium

- deep import bypassing a public surface
- page or controller orchestrating business rules
- context-specific configuration stored globally and duplicated
- shared module coupling otherwise independent contexts

### Low

- misleading name
- inconsistent colocated tests
- minor placement that does not alter dependency direction or ownership

Do not manufacture severity for stylistic differences that do not affect behavior or changeability.

### Finding Format

~~~yaml
Finding:
  severity: high
  evidence:
    - exact path and symbol
    - dependency or write edge
  violated_contract: Ordering.internal_surface
  impact: Billing changes can bypass Ordering invariants
  correction: Introduce PlaceOrder or OrderReadModel public contract
  migration_unit: billing order lookup slice
  verification: boundary test plus behavior test
~~~

## 5. Design the Target Without Erasing Context

- Preserve established names unless they conflict with the business language.
- Preserve framework-native locations when they are part of runtime discovery.
- Preserve useful public contracts before moving internals.
- Centralize a fact only in its rightful owner; do not create a larger global shared package.
- Introduce an interface only at a real architectural boundary or for multiple implementations.
- Avoid new base classes, factories, and registries unless current variation requires them.
- Do not rewrite unrelated contexts.

Map every proposed directory to a responsibility and every moved dependency to a contract.

## 6. Build an Incremental Migration

Migrate one Bounded Context or vertical slice at a time.

### Slice Selection

Prefer a slice that:

- has clear inputs and outputs
- owns or can cleanly claim its data
- has representative tests
- reduces a meaningful cycle or deep import
- does not require a big-bang shared rewrite

### Per-Slice Sequence

1. Capture observable behavior with existing or focused regression tests.
2. Define or tighten the public contract.
3. Move the domain and application behavior while preserving consumers.
4. Move or adapt infrastructure behind inward-defined ports.
5. Move presentation entry points or delegate framework-owned entries.
6. Assign data, migrations, settings, routes, and events to the owner.
7. Repair imports, exports, DI, routing, build metadata, and tests.
8. Add or update a boundary check.
9. Run focused verification.
10. Remove the obsolete path only after consumers are migrated.

Avoid temporary compatibility layers unless they make the migration safer. Give every temporary bridge an owner and removal condition.

### Cross-Context Data

When moving data ownership:

- name one current and one target owner
- prevent new writers before moving old ones
- define the public command, query, event, or read model
- migrate consumers incrementally
- verify invariants and data access
- remove direct access last

Do not copy a mapping or validation rule into both old and new locations as a permanent solution.

## 7. Maintain Momentum During Authorized Work

When refactoring is authorized:

- make a provisional plan internally
- proceed through safe moves and reference repairs
- run verification after each coherent slice
- fix ordinary import, type, route, and test failures without asking
- report assumptions after the work

Pause only when the skill's stopping conditions apply. A failed test, unfamiliar file, or need for additional investigation is not by itself a reason to stop.

If an expected tool is absent, use the project's available checks or a read-only analysis and clearly report the verification gap. Do not install unrelated tooling merely to continue.

## 8. Report the Migration

Lead with what is now true.

### For Audit Only

- current boundary summary
- evidence-backed findings ordered by severity
- target boundary map
- minimal migration sequence
- assumptions and confidence
- verification recommendations

### For Completed Refactor

- contexts or slices moved
- public contracts introduced or preserved
- ownership changes
- import, route, DI, config, and migration repairs
- checks run and their results
- deliberate exceptions
- remaining slices or risks

Do not report every command or mechanical file move when a concise architectural summary is clearer.
