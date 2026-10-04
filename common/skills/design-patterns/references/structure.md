# Contract Conversion and Object Structure

Even when wrappers look alike, their roles differ depending on whether they transform a contract, control access, or add behavior. Start with the distinctions below and implement only the combinations actually needed.

## External Contracts and Wrapping

### Adapting Contract Differences: Adapter

- **When to consider it:** Inputs, results, and failure meanings from an external API or existing component must be adapted to the consumer's contract. It can be appropriate even with a single external implementation when there is a real difference to isolate.
- **Alternatives and distinctions:** Do not add a forwarding layer around an object that already provides the same contract. Its purpose differs from Proxy, which controls access, and Decorator, which adds behavior.
- **Minimal form and cost:** Define the contract required internally and an implementation responsible for the external call and conversion. Do not mechanically split one conversion responsibility into Client, Mapper, and Adapter. Correctly translating error and data meanings has a cost.

Example: A boundary that converts an external map response into an internal place-query result can be valid even with one integration. Turning the original failure into an empty search result may change the contract.

### Simplifying a Complex Usage Procedure: Facade

- **When to consider it:** Callers repeatedly need to know several underlying components and their execution procedure.
- **Alternatives and distinctions:** Reuse an existing business entry point if it already owns the procedure. Adapter addresses contract compatibility; Facade simplifies how something is used.
- **Minimal form and cost:** Provide an entry point and coordination for one cohesive purpose. Combining unrelated features or exposing the underlying objects directly blurs the boundary.

### Composing Behavior Under the Same Contract: Decorator

- **When to consider it:** Independent additional behavior must be composed or maintained separately from the original implementation while preserving the existing contract.
- **Alternatives and distinctions:** Compare the costs of direct implementation, existing middleware, and wrapping. A wrapper may fit even when there is only one fixed additional behavior if the original implementation cannot be modified or the behavior has an independent reason to change. Do not stack wrappers without a benefit in separating responsibilities or composing behavior.
- **Minimal form and cost:** A wrapper preserves the original contract and delegates to its target. Wrapping order can change results, errors, and resource lifetimes. A language's decorator syntax does not itself imply this design intent.

### Controlling Access Through a Surrogate: Proxy

- **When to consider it:** A surrogate serving the same role must control access to a target, its lazy creation, or remote calls.
- **Alternatives and distinctions:** Do not duplicate proxying already provided by a framework or client. Although its structure resembles Decorator, the central concern is controlling how the target is accessed.
- **Minimal form and cost:** Keep a contract-preserving surrogate and only the necessary control. Check actual behavioral differences, such as deferred failures, stale cached values, or changes in call count.

## Composition and Axes of Change

### Treating Individual Items and Groups Uniformly: Composite

- **When to consider it:** The same meaningful operation is applied recursively to individual tree elements and groups of child elements.
- **Alternatives and distinctions:** A list and explicit branches may be enough for a flat collection or items with different behavior. Do not force meaningless operations onto every child element.
- **Minimal form and cost:** Define the common operation, individual elements, and groups containing child elements. Traversal, ownership, and change impact can become more complex.

### Separating Two Axes of Change: Bridge

- **When to consider it:** The kinds of functionality offered to users and the means of carrying it out grow independently, producing a class for each combination.
- **Alternatives and distinctions:** If only one side varies, first consider Strategy or simple delegation. Unlike Adapter, which reconciles existing contract differences, Bridge aims to design the two axes independently.
- **Minimal form and cost:** Have the functional role delegate to a small contract for the execution mechanism. Maintain the two abstraction axes and their composition relationships.

### Sharing Repeated Immutable State: Flyweight

- **When to consider it:** Given the number of objects and the size of their repeated state under current requirements, sharing can meaningfully reduce memory cost, and that common state can be shared safely.
- **Alternatives and distinctions:** Compare the cost with ordinary objects or the language's existing sharing facilities. Use the current required data scale or measurements as evidence; do not make measurement a prerequisite for adoption. Unlike Singleton, it does not limit the entire object to a single instance.
- **Minimal form and cost:** Separate shared immutable state from per-call state. A shared store, lookup cost, and passing individual state are added, and incorrectly sharing mutable state can corrupt results.

## Check After Adoption

Check the parts that actually change among contract conversion, delegation order, failure propagation, and resource ownership. When simplifying, also examine whether a responsibility owned by an existing wrapper disappears.

For example, a small display-conversion function or object may be enough when only changing the string shown on screen. Creating a decorator layer that forwards every method of the original object for this purpose can create more structure to maintain than the problem warrants.

## Composite Substitutability and Ownership

For individual elements and groups to serve the same role, common operations must be meaningful for both. Instead of exposing child-addition methods on every element and always failing on leaves, consider separating the common traversal role from the editing roles actually needed. For a small tree that does not need this role separation, distinct data types and traversal functions may suffice.

If multiple parents share a child, the structure has graph characteristics rather than being a tree. Deletion, movement, and aggregation semantics change, and cycles become possible. First check whether the current data structure already guarantees a tree; do not add redundant general-purpose graph checks to a structure whose shape is already guaranteed.

Decide who updates parent and child references together when an object moves. Also compare whether read-only traversal and structural editing need to share one responsibility.

## Axes of Change in Bridge and Adapter

When multiple document-output features and multiple output devices vary independently, Bridge is a candidate: the feature object delegates to an output mechanism. If a particular device's external API differs from the internal output contract, an Adapter may be needed on the implementation side. They can coexist because one separates two axes of change while the other translates contract differences.

If output devices are the only axis that actually varies, a small output contract and delegation may be sufficient. Bridge does not require both the abstraction and implementation sides to become inheritance hierarchies.

## Flyweight Sharing Criteria and Cleanup

The key used to find shared state must represent actual equivalence. Even the same character shape may be a different shared object when its font or size differs. Storing per-call position or selection state in the shared object overwrites the state of other users or elements.

If keys keep accumulating in the shared store, retention can cost more than the savings on individual objects. Choose a retention scope that fits the actual data set and lifetime. Do not create a global cache first and decide its policy later.

Compare Decorator and Proxy nesting order, cache-write timing, and error-conversion combinations in [Deeper selection and composition criteria](selection-depth.md).
