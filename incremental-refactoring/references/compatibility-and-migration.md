# Compatibility and Migration

Use this guidance when the requested improvement changes a published interface, persistent representation, execution owner, or boundary between independently running components.

## Identify Who Must Move

Establish the current and target responsibilities, actual writers, callers, readers, and independently released consumers. Preserve the meaning of different execution triggers, such as manual and scheduled actions, even when they share a use case.

An interface whose callers can be changed together has different constraints from one used by consumers outside the codebase. Inspect the actual reach of the change before choosing a transition strategy. See Martin Fowler, [Published Interface](https://martinfowler.com/bliki/PublishedInterface.html).

Distinguish the ability to prepare code locally from authority and evidence to change a deployed execution path. Keep existing repository, data, and deployment decisions unless changing them is part of the request.

## Choose the Smallest Transition

When a coordinated change can update all relevant consumers safely, a temporary compatibility layer may be unnecessary. When old and new consumers must coexist, retain a compatible boundary while moving them incrementally.

An abstraction can allow an implementation to be replaced gradually behind the same interaction contract. Introduce it for that transition or an enduring responsibility, and determine whether it is still useful afterward. See Martin Fowler, [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html).

For an incompatible contract change, use the applicable parts of this sequence:

1. **Expand:** Prepare the new contract or representation while keeping required existing behavior usable.
2. **Migrate:** Move consumers or execution responsibility in verifiable increments. Check failures as well as successful results.
3. **Retire:** Remove the old contract, representation, implementation, and temporary connection once their remaining uses are resolved.

The transition is unfinished while the old version is still required. Record why it remains and what evidence permits removal. See Danilo Sato, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html).

## Preserve State and Execution Semantics

When moving writes or work across processes, assess the conditions introduced by that move:

- transaction and consistency boundaries;
- timeouts or lost responses after work may already have completed;
- retries, duplicate requests, and overlapping old and new workers;
- work already in flight during the transition;
- ordering, partial failure, and external effects;
- recovery from a failed transition, including data already written.

Choose handling based on the operation's actual contract. Do not assume that replacing a direct call with a network call preserves its failure behavior, or add retries without understanding duplicate effects.

Make write authority explicit during the transition. Comparing implementations must not accidentally execute real side effects twice. Use controlled inputs and isolated effects when comparison is needed; use live systems only within the established authorization.

Schema, technology, ownership, and behavior changes can each introduce different risks. Separate them when doing so makes the result easier to verify and recover. Use existing recovery procedures where sufficient.

## Verify Retirement

Check remaining uses through source, configuration, runtime discovery, and known external consumers as applicable. An empty text search alone may miss reflection, scheduled execution, or independently deployed clients.

Remove obsolete code and tests within the changed surface after their contract has moved or been intentionally retired. Preserve tests for behavior that still exists. Update configuration and documentation that would otherwise direct future work to the old path.

Report separately what was implemented, what execution actually moved, and what was removed. A locally verified replacement does not establish that production traffic or deployed writers have switched.
