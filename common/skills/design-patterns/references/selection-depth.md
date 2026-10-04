# Deeper Criteria for Pattern Selection and Composition

Read this when several pattern names come to mind or when patterns seem individually appropriate but overlap in responsibility when combined. Compare not only what a pattern makes changeable, but also which changes it makes harder.

## Distinguish What Is Changing

| Current variation | Representations to compare first | Boundary to examine |
| --- | --- | --- |
| The calculation formula is the same; only rates and ranges differ. | Configuration values, condition tables, value objects | Who owns valid data combinations and ranges? |
| Procedures serving the same purpose differ. | Function passing, Strategy | Is there a reason to separate selection from execution? |
| An object's current state changes the operations it permits. | Transition tables, state types, State | Who jointly determines whether a transition is allowed and its resulting state? |
| New object types are added frequently. | Polymorphism, Strategy, composition | Where are existing operations implemented for the new type? |
| Object types are stable and new operations are added frequently. | Pattern matching, Visitor | How much does the new operation depend on internal representation? |
| External providers have different contracts. | Adapter | Must failure and partial-result meanings be translated as well as formats? |
| Combinations within object families change together. | Assembly functions, Abstract Factory | What goes wrong if different families are mixed? |
| Different read and write times cause conflicts. | Version checks, transaction boundaries | Changes to which values must be protected by one decision? |

Configuration values and policy objects can coexist. Making a separate class for each policy whose only difference is numbers in the same algorithm turns data variation into a proliferation of types. Conversely, putting implementations with different execution ordering and failure handling into a large configuration table turns the configuration itself into an interpreted language.

## Distinguish Policies, Conditions, and State

Eligibility for a rate is a condition (Specification), the calculation after eligibility is established is a policy (Strategy), and a rule prohibiting price changes after a reservation is confirmed concerns state and invariants. Putting all three into one strategy interface makes policy implementations own eligibility decisions and state transitions as well.

When selecting, establish the meaning in this order:

1. Identify the conditions that determine whether the current request is allowed.
2. Define the action and result when it is allowed.
3. Determine the object's state after the action.
4. Separate only the parts of these responsibilities that actually vary independently.

In a small feature, one cohesive method may express this entire flow clearly. Separation pays off when responsibilities change for different reasons or are reused. Do not use this as a formula that always creates one condition object, one policy object, and one state object.

State and Strategy have similar delegation structures. The distinction is whether the state determines an object's permitted actions and transitions or a strategy selects a way to perform the requested purpose. Establish ownership first: if multiple parties independently change state, different objects can hold contradictory versions of current state.

## Compare an Inherited Fixed Procedure with Composition

Consider Template Method when the order of a common procedure is itself a contract and subtypes must vary only specific steps. Beyond merely removing duplication, the following must be stable:

- Which steps are called and what state holds before and after them.
- Whether subsequent steps execute when a subtype implementation fails or stops.
- Whether a subtype implementation can work through the contract without depending on the parent's internal fields.

Strategy or composition of small collaborators may fit when execution mechanisms need to be replaced or combined independently. Composition also introduces selection and assembly responsibilities, so it is not always simpler. Implementing an existing framework's stable extension contract can be clearer than introducing another composition layer.

## Contract Differences Between Wrapping Structures

| Question | Adapter | Decorator | Proxy | Facade |
| --- | --- | --- | --- | --- |
| What does it solve? | Reconciles the meanings of different contracts. | Composes additional behavior for the same role. | Acts on behalf of a target and controls access to it. | Simplifies the procedure for using multiple components. |
| What contract does the consumer use? | The contract required internally. | The original role's contract is preserved. | The semantics of the represented target are preserved. | A new entry contract suited to the usage purpose. |
| What decision is often missed? | How are external partial failures and absence translated? | Does changing the order preserve the result? | Are deferred execution and failure timing visible? | Does exposing underlying implementations spread the procedure back into callers? |

One object can handle both external conversion and simple call proxying. Separate roles when there are independent reasons to change or real composition requirements. Do not require a separate class for each pattern name.

## The Cost of Extending Object Types and Operations

If document elements are fixed as headings, paragraphs, and images while output, statistics, and validation operations keep growing, Visitor or external operation functions are candidates. A new operation can be gathered into one implementation, but adding a new element type requires updating multiple operations.

If plugins continuously add element types, a visitor design with a closed list of every type conflicts with that requirement. Compare having each element provide a small behavioral role or expose necessary capabilities through separate contracts. Choose errors, ignoring, or fallback display for unknown types according to the actual contract.

Type-based branching is acceptable. Examine whether branches maintained independently in multiple places cause omissions that are hard to find, whether the language checks exhaustive handling, and whether new types or new operations actually change more often.

## When Composition Order Changes Results

A cache lookup outside a transaction can avoid opening the transaction on a hit. Writing changes made within a transaction to a shared cache before commit can leave rolled-back values in the cache. Adding a cache is a decision about read consistency and write timing, not merely another wrapper.

Retrying an entire call can repeat reads, state changes, and external effects. Retrying only the persistence portion can reuse a decision based on state that is now stale. When retry behavior is requested or already present, check the repeated scope and the effects of the previous attempt. Do not introduce retries merely to implement a pattern example.

Logging or measurement at the outermost layer records the user's total wait; placed inside, it records individual attempts or actual operation time. Failures observed outside an Adapter that converts errors into result values also differ from failures observed inside it. Choose the order according to the required meaning.

When composing wrappers, compare only orders that change semantics. Check combinations that affect the actual contract rather than mechanically testing every combination.

## Combine Patterns Without Duplicating Responsibility Ownership

For example, provider-specific Adapters, a pricing Strategy, and a creation Factory can be combined. Assign provider-error translation to the Adapter, calculation-method selection to the business policy selector, and object creation to the composition point. If every layer branches on the same provider code and repeats the same selection, composition loses its benefit.

When converting a condition (Specification) into a query representation (Query Object), distinguish the business condition's meaning from its storage-technology representation. Check whether all relevant conditions can execute with the same meaning in both places. Differences in in-memory string comparison, database collation, or null handling can make seemingly equivalent conditions return different sets.

## Comparing Behavior Before and After a Change

Establish the external input, result, and failure meanings first, then move responsibilities one at a time. Changing selection points, execution points, and state ownership all at once makes it harder to determine which move caused a defect.

While migrating to a new pattern, prevent the old and new paths from executing the same side effects twice. Pure calculations can be compared with representative inputs, but do not verify equivalence by performing writes and external requests twice.

Report the reason for the choice and its main cost briefly. Evaluate each candidate internally to the depth the actual task needs; there is no need to output all of that analysis as a long document for the user.
