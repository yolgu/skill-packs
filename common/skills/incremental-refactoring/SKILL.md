---
name: incremental-refactoring
description: Refactor an existing feature or domain through contract discovery, behavior-preserving changes, focused verification, and incremental migration when needed. Use when a change affects meaningful behavior or responsibility boundaries; not for greenfield implementation or purely mechanical edits.
---

# Incremental Refactoring

Make an existing feature easier and safer to change while preserving its required behavior. Work from the current domain model, architectural decisions, coding conventions, and verification practices. Reuse relevant contracts, investigation results, and accepted plans.

## Establish the Improvement

Respect the requested scope: investigate and propose for analysis or review; change code and verify it for an authorized refactor.

Identify the problem, its evidence, the intended improvement, and the completion criteria. When only a feature or domain is named, derive these from the current implementation and its consumers. Prefer improvements that reduce demonstrated change cost, unclear responsibility, duplicated policy, or failure risk. Do not infer a new business policy from unfamiliar code.

For a domain-wide request, map its capabilities and relationships, then divide the work into coherent changes. Investigate the next change deeply enough to act; do not require detailed tests for the entire domain before starting. Complete the requested outcomes across those changes rather than treating the first finished part as the whole task.

Keep the working plan proportional to the change. Use an existing target design when one is established, and investigate any incompatibility before departing from it.

## Establish the Observable Contract

Trace the affected entry points through their rules, state changes, persistence, external effects, and consumers. Include the return path: error handling and the result shown to a user can be part of the same contract.

Distinguish:

- observed behavior that must be preserved;
- intentional behavior changes with established expectations and authorization;
- defects or uncertainties to investigate or record for later.

Account for inputs, results, permissions, failure behavior, data changes, and external effects that the change can affect. Inspect side effects before exercising a path; a read-like name or HTTP method does not establish that execution is read-only.

Use existing tests where they protect the affected behavior. Read [contracts-and-verification.md](references/contracts-and-verification.md) when behavior is unclear, test coverage is insufficient, or state and external effects need separate verification.

## Make Small, Verifiable Changes

Repeat this sequence for each coherent change:

1. Establish the relevant behavior and a usable verification baseline.
2. Make a focused structural change toward the intended responsibility or boundary.
3. Repair affected consumers, imports, wiring, configuration, and tests together.
4. Run the narrowest checks that cover the change and its plausible regressions, along with required project checks.
5. Inspect failures before proceeding; fix an introduced regression or revise the change.

Keep each change understandable as one purpose. Its size is determined by what can be reasoned about and verified together, not a fixed number of files or lines. Follow a feature across repositories when necessary, while editing only the surfaces needed for the requested outcome.

When dependencies prevent testing, first create the smallest behavior-preserving separation that makes the affected path testable, then establish its tests before broader restructuring. This is a local entry into the workflow, not permission to redesign untested code wholesale.

Separate structural changes from intentional changes to observable behavior. For a defect fix, establish regression evidence and verify the corrected expectation. A structural refactor should not require changing the expected behavior merely to make tests pass.

Use the structures required by the target design and project conventions. Add discretionary abstractions, compatibility layers, or dependencies only for a concrete responsibility, test boundary, or migration need. Keep unrelated cleanup out of the change.

## Handle Existing Problems

Resolve confirmed defects within the authorized scope when their expected behavior is established and the change can be verified safely. Record a problem for later when its correction requires a separate policy decision, substantial scope expansion, unavailable authority, or an explicit decision to defer it.

Use the existing issue or follow-up document where available. Include the evidence and location, impact, reason for deferral, proposed correction or missing decision, and verification needed. Label an unconfirmed suspicion as uncertain. Continue work that is independent of the deferred problem.

Do not use a follow-up note to exclude a required outcome from the request. An error introduced by the current change must be resolved or the affected change withdrawn; it is not an existing defect to defer.

## Change Ownership or Published Contracts When Needed

Changes to APIs, schemas, execution ownership, or service boundaries can need a separate transition. Read [compatibility-and-migration.md](references/compatibility-and-migration.md) when the task includes such a change.

Keep implementation readiness, actual consumer or writer migration, and retirement of the old path distinct. Remove obsolete code and temporary connections when their consumers have moved and the replacement is verified. Report any remaining transition and its removal condition explicitly.

## Finish With Evidence

Assess the requested outcomes against the final code and the applicable verification results. Use the project's commands and test execution policy. Reuse passing evidence while its code, configuration, environment, and inputs remain applicable; rerun affected checks after relevant changes.

Report the improvement, preserved contracts, intentional behavior changes, verification results, and unresolved risks. Distinguish code that is ready from a transition or deployment that has actually occurred. Do not claim an unavailable or unrun check passed.

For substantial refactors, preserve the contract findings, design rationale, changes, verification, and follow-up work in the existing documentation or a cohesive task document. For small changes, summarize the result in the conversation and persist actionable follow-up items. Keep records focused enough that the next change can reuse them.
