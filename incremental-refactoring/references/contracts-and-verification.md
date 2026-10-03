# Contracts and Verification

Use this guidance to establish what a change must preserve and what evidence will detect a regression.

## Capture the Affected Behavior

Follow representative paths from their entry points to their consumers and effects. Depending on the feature, entry points can be screens, commands, HTTP handlers, scheduled jobs, or events.

Record only the dimensions that can affect the decision:

- inputs, preconditions, identity, and resource permissions;
- returned values, failures, and the result visible to the caller or user;
- persisted state and required consistency across changes;
- external calls, messages, notifications, files, or other effects;
- consumers that depend on the result, including other entry points into the same capability;
- timing, ordering, repeated execution, or concurrency when they create a plausible failure mode.

Distinguish source-level findings, observed execution results, and assumptions. Exercise the system in an appropriate environment with controlled inputs and effects. Do not treat source inspection as proof that a deployed path behaves identically.

## Characterize Before Interpreting

A characterization test records what the current implementation does. It helps detect behavioral changes without establishing that the behavior is desirable. Investigate surprising results and any consumer reliance before classifying them as defects. Preserve unresolved behavior until its intended treatment is established. See Michael Feathers, [Characterization Testing](https://michaelfeathers.silvrback.com/characterization-testing).

Choose representative normal, boundary, and failure cases for the affected path. If using captured outputs or snapshots, inspect their meaning before accepting a baseline. Exclude nondeterministic fields only when they are irrelevant to the contract; do not erase meaningful ordering, identity, or error differences.

During structural changes, keep contractual expectations stable. Test setup may change as dependencies are rearranged. During an authorized behavior correction, update only the affected expectations and keep the original failure represented by a regression case.

## Choose Evidence by the Claim

| Claim to establish | Suitable evidence |
|---|---|
| A business rule or state transition is preserved | Focused domain or application tests |
| A consumer can still use an interface | Contract checks through the affected boundary |
| State is stored correctly and failures preserve consistency | Persistence or transaction integration tests |
| A user sees the correct result and can complete the flow | Component, interaction, or focused end-to-end tests |
| An external effect is requested with the correct meaning | Adapter or interaction tests; actual integration checks when authorized and necessary |

Message compatibility and functional effects are different claims. A response test alone does not show that a record was saved or that an external effect occurred. Test business rules with their owner rather than duplicating every rule in consumer contracts. See Pact, [Contract Tests vs Functional Tests](https://docs.pact.io/consumer/contract_tests_not_functional_tests).

Favor assertions about observable results over incidental internal calls. Internal interactions are useful assertions when the interaction itself is part of the requirement. See Google Testing Blog, [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html).

Use maintained coverage for the same contract and case before adding tests. Add missing regression evidence for fixes. Do not infer completeness from a coverage percentage or introduce a universal coverage target.

## Enter Code That Is Hard to Test

Look for an existing boundary where a difficult dependency can be controlled. If none is usable, make a minimal extraction or delegation that keeps production behavior intact, then test through that boundary. Limit the initial change to enabling observation or control. Michael Feathers describes these substitution points in [Seams](https://www.informit.com/articles/article.aspx?p=359417&seqNum=2).

If the required baseline still cannot be established, explain the missing evidence and restrict the affected change accordingly. Continue independent, verifiable work. Do not compensate for missing evidence with a large redesign or treat a manual observation as an automated regression test.

## Interpret Failures

Identify whether a failure comes from the current change, an existing problem, an incorrect test expectation, or the execution environment. Use the last relevant passing state and the smallest failing scope to narrow the cause.

Repair introduced regressions before building on them. A pre-existing or unavailable check remains a limitation in the result. Broaden verification only when a specific unverified risk requires it, while retaining required project checks.
