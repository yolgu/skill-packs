# Decisions in TypeScript and React

Decide whether functions, objects, or components should express the pattern's roles. First check the project's state ownership and dependency assembly approach. Do not replace an entire state library or rendering structure merely to apply a pattern.

## Policy Functions and Object Contracts

If an interchangeable policy (Strategy) has one operation, compare a function type with explicit input and output and passing a function. Consider an object contract when several operations share state or invariants. A named function may suffice for simple creation. An Adapter around an external SDK can also be a small object or function.

Do not create a class for every function or a creation factory for every class just to match an object-oriented pattern diagram. A plugin registry is unnecessary without a real need to select among implementations. The project's explicit-type rules apply regardless of the implementation form.

## State Representation and Transitions

Data for a finite set of states such as loading, success, and failure can be expressed with a discriminated union. A common field with a distinct literal value in each type allows access to the corresponding state's data inside a branch that checks that value. Distinguishing each state's available data through types reduces unnecessary combinations of optional fields.

There is no need to replace this language feature with a State object hierarchy. Compare existing state tools, explicit transition functions, or reducers. Consider objects when grouping complex behavior by state has a benefit. Avoid duplicating responsibility for actual transitions and for applying asynchronous results.

## View Composition and Logic Reuse

First use variation already expressed through component composition, children, and necessary callbacks. Adding behavior to a view does not always require a separate Decorator or HOC. Create only currently needed variation points while preserving rendering structure and state ownership.

Custom hooks can reuse stateful logic, but calling the same hook does not share state by itself. Local state created by each call is independent. When state must be shared, first compare a common owner and a delivery path or an existing store. For state shared by the entire browser application, a single store with subscriptions is also an option. Do not reject it merely because there is one object; judge it by actual sharing scope, lifetime, and responsibility for changes.

Keep pure business calculations and external contract conversions as ordinary functions or objects when they do not need React facilities. Avoid designs that conditionally call hooks themselves like arbitrary strategies, and follow the project's hook invocation contract.

## Subscriptions and External State

Before introducing change notifications (Observer), check existing state tools and external libraries for subscription support. Passing values and callbacks may be sufficient for simple parent-child collaboration.

When connecting an external store to React rendering, compare the tool's React integration with useSyncExternalStore. The subscription function signals changes and returns an unsubscribe function, and the snapshot must return the same value while nothing has changed. Do not directly connect a read function that creates a new object every time. If server rendering is used, align the initial snapshot read on the server as well.

When simplifying or changing wrappers, check actual problems in the changed path, such as duplicate subscriptions, stale values, and missed cleanup. Do not turn every business call into a global event bus or create a separate duplicate of the state.

## Example Decisions

A single operation that changes the sorting criterion of the same list can be expressed as a clearly typed comparison function. A discriminated state type and the current state tool may suffice for request state in a view. A separate object may express a business policy more clearly when independent state and several operations must be maintained together.

## Separating State Transitions from External Effects

A reducer or pure transition function can determine the next state from current state and input. Hiding external persistence or requests inside that calculation can duplicate effects during re-execution and testing. Make responsibility clear for executing effects according to user intent and applying their results to state.

When introducing an object-based State pattern, do not make the state observed by React and the object's internal mutable state independently own current state. Changing only class fields can leave render state unchanged or require extra synchronization between the two. Compare separating behavior while preserving the existing state owner.

Check whether policy callbacks capture values from an old render. Before automatically adding memoization, decide what should be passed as an argument and what should be read from current state. Stable callback identity and fresh business values are different concerns.

For view models, drafts, and asynchronous-response conflicts, read [Presentation and interaction patterns](presentation.md) and compare the [Search-screen case](design-cases.md).
