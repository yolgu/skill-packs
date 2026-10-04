# Policies, State, and Collaboration

Do not make eliminating branches a goal in itself. First distinguish whether a branch selects an interchangeable policy, behavior allowed in the current state, or a request to execute. Keep small conditionals or explicit transition tables when they are sufficient.

## Policies and State

### Interchanging Policies: Strategy

- **When to consider it:** Calculations or policies serving the same purpose must be changed or selected independently of the calling flow.
- **Alternatives and distinctions:** Compare short, stable branches or passing a function. Unlike State, which represents internal state and transitions, Strategy selects how to perform the same role.
- **Minimal form and cost:** Define the necessary policy contract, implementations, and responsibility for choosing the policy to use. A function may suffice for one operation. Maintain the selection point and the additional delegation step.

Different pricing policies that change independently are a good candidate. The existence of two conditions alone does not require separate policy classes.

### State-Specific Behavior and Transitions: State

- **When to consider it:** Multiple operations depend on current state and transition rules are intertwined, so grouping responsibilities by state makes them clearer.
- **Alternatives and distinctions:** Compare state values and a transition table, type-based branching, or a reducer. Do not create an object hierarchy simply because the screen has different states.
- **Minimal form and cost:** Decide who owns current state, state-specific behavior, and transitions. Do not duplicate transition decisions in both state objects and a separate service. Manage the structure that grows with the number of states and the meaning of prohibited transitions.

Distinguish when state objects with behavior are useful from when state types that classify data are sufficient.

### A Common Procedure with Overridable Steps: Template Method

- **When to consider it:** A fixed procedure and ordering are a real common contract, and subtypes must vary only some steps.
- **Alternatives and distinctions:** If the variable steps are independent, first compare composing functions or Strategies. Do not create a common parent from a few similar lines of code alone.
- **Minimal form and cost:** Keep the method that owns the procedure and only the necessary override points. Subclasses are coupled to the parent's calling context, so the permitted scope and order of overrides become part of the contract.

## Requests and Collaboration

### Representing an Execution Request as a Value or Object: Command

- **When to consider it:** Request creation and execution must occur at different times, or requests must be retained, recorded, or undone.
- **Alternatives and distinctions:** A function or method suffices for a simple, immediate call. Strategy focuses on interchanging the way work is performed; Command focuses on representing and passing a request independently.
- **Minimal form and cost:** Make the necessary input and execution responsibility explicit. Add queues, dispatchers, and undo structures only when those requirements exist. Creating a request object does not make repeating or undoing it safe.

### Change Notifications and Subscriptions: Observer

- **When to consider it:** A publisher must connect subscribers to react to changes without knowing their concrete types.
- **Alternatives and distinctions:** Compare direct calls when there is an explicit business sequence or a simple flow with fixed recipients. Use existing subscription facilities or state tools when available.
- **Minimal form and cost:** Define event meaning, subscription and unsubscription, and notification behavior. Ordering, reentrancy, and error propagation can become hidden. Local events alone do not guarantee durable delivery, retries, or consistency across services.

### Passing Requests Along Connected Handlers: Chain of Responsibility

- **When to consider it:** The handler of a request or the conditions for passing it onward vary, and callers need not know individual handlers.
- **Alternatives and distinctions:** An explicit call sequence is sufficient for a few fixed steps. Distinguish a pipeline where every step must execute from a responsibility chain that stops after handling.
- **Minimal form and cost:** Clearly represent forwarding, handling, termination, and unhandled results. Step order and stopping conditions affect the result, and hidden control flow increases.

### Coordinating Interactions Among Participants: Mediator

- **When to consider it:** Participants reference each other and their interaction rules are scattered across multiple places.
- **Alternatives and distinctions:** Reuse an existing business coordinator if it already owns the responsibility. Compare Observer for one-way notifications and Facade for an entry point that simplifies use of a subsystem.
- **Minimal form and cost:** Assign responsibility for coordinating one cohesive set of interactions. Dependencies among participants decrease, but unrelated rules can accumulate in the coordinator.

## Patterns to Consider for Specific Requirements

| Pattern and signal | Simpler alternatives and distinctions | Minimal form and cost |
| --- | --- | --- |
| Traversal without exposing internal representation (Iterator): distinct traversal rules or lazy exploration are needed. | Keep the language's iteration and collection interfaces when they suffice. Its purpose differs from Composite, which recursively groups a data structure. | Separate traversal state and provision of the next element. Manage the meaning of modifications during traversal, resource closure, and consumable iteration. |
| Capturing and restoring internal state (Memento): state must be restored to a point in time without exposing its internal representation externally. | Compare a snapshot of a small immutable value or existing history facilities. Unlike Command, which records execution requests, Memento retains state. | The state owner defines capture and restoration. Manage storage cost and restoration scope; do not assume that external effects already performed are also undone. |
| Adding operations to stable object types (Visitor): object types are stable and new operations are added frequently. | Compare type-based branching or pattern matching when the set of types is small and explicit. Frequent new object types increase the cost of updating Visitor implementations together. | Define operation contracts for object types and traversal responsibility only as needed. Consider the different costs of extending operations versus extending types. |
| Interpreting the rules of a small language (Interpreter): expressions in an actual, defined small grammar must be represented and evaluated. | Check whether configuration values, condition functions, or a proven existing parser suffice. Do not invent a grammar for ordinary conditional branching. | Define the grammar, expressions, and evaluation context. Maintaining grammar extensions, error locations, and evaluation semantics has a cost. |

## Check After Adoption

According to the actual change, check policy results, allowed and prohibited transitions, handling order, unhandled results, unsubscription, and error propagation. Do not add undo, retries, or durable event facilities when those requirements do not exist.

In refactoring, first identify the actual problem and select only candidates that reduce it. An existing policy object that no longer serves a distinct role can be collapsed into a direct call, and state objects that merely separate data can be simplified into explicit state types. Preserved behavior and contracts are the basis for the decision.

## State Transitions and Side-Effect Ordering

A transition can be understood as a decision based on current state and an input event, the determination of the next state, and the effects needed. Changing state before an external call has different failure semantics from changing it after success. Decide which state other callers can observe at each point.

Use the business contract to decide whether an effect failure permits returning to the original state, requires retaining a failure state, or calls for an in-progress state. Creating a new State object does not make persistence and external effects atomic. The state owner must connect the actual transition with its persistence outcome.

## Undo Semantics in Command and Memento

Check whether undoing a Command can really be achieved by calling an inverse method. If another person has modified an item after it was added, simply deleting it can lose that later change. First distinguish local editing history from the history of changes to shared state.

Memento must capture the state to restore. Retaining only a reference to the original mutable object can let later modifications change the history itself. Compare full snapshots and change records by memory cost, restoration frequency, and meaning. External requests and already-committed writes are separate from restoring an in-memory snapshot.

When undoing a group of commands, decide how failures of intermediate commands and partial completion are represented. Do not add a general-purpose history engine without an actual requirement.

## Observer Reentrancy and Recipient Ordering

Check whether a recipient can change publisher state again or unsubscribe another recipient during notification. Use the traversal and reentrancy guarantees of the actual subscription tool rather than implementing the same guarantees again.

If recipient B must read a value produced by recipient A, the relationship may be an ordered business procedure rather than simple observation. Compare direct coordination or an explicit pipeline. Whether a recipient's error stops the whole operation or notifications continue to other recipients must match the current contract.

## Type Boundaries in Visitor and Interpreter

Visitor can lower the cost of adding multiple operations to stable object types, but adding a new type may require updating visitor implementations. Moving type branches into visitors does not automatically eliminate omissions of new types. Make the owners of type-specific visits and traversal clear.

If Interpreter is selected, grammar, operator precedence, name resolution, and error locations become part of the contract. Processing condition data and providing a language in which users can write expressions have different maintenance costs. Reuse an existing parser when it supports the actual grammar, and do not substitute arbitrary code execution for rule evaluation.

## Iterator Consumption and Resources

Iterating an in-memory list differs from lazily traversing a database cursor or file in failure behavior and resource lifetimes. Check whether resources are released when traversal ends early and whether the same iterator may be reused. If callers expect to traverse again, decide between providing a fresh iterator and retaining the results, considering the cost.

Read [Deeper selection and composition criteria](selection-depth.md) when choosing among alternatives, especially to distinguish Strategy, Specification, and State or to compare Visitor with type-based branching.
