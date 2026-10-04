# Object Creation and Assembly

First distinguish the responsibility for selecting what to create, the responsibility for assembling its dependencies, and the lifetime of the created object. A simple constructor or named creation function is also a valid alternative. Do not add an inheritance structure or factory interface merely because something is called a factory.

## Choosing a Creation Approach

### Consolidating Creation Knowledge

When multiple callers need to know concrete types and assembly rules, a meaningful creation function or small factory object can consolidate that knowledge. If the change only relocates a short piece of code that creates one fixed object, assess the benefit of the additional layer. This is a general separation of creation responsibility and does not necessarily have the same structure as the GoF Factory Method.

### Delegating Creation to Subtypes: Factory Method

- **When to consider it:** A common workflow must remain intact while meaningful subtypes decide which object to create.
- **Alternatives and distinctions:** If no relevant subtypes already exist, first compare passing a creation function or injecting the object directly. Unlike a simple static creation function, the defining feature is overriding a creation point through inheritance.
- **Minimal form and cost:** Keep only the creation point in the common flow and the necessary overrides. Subclasses become coupled to the parent's call order and contract.

### Creating Compatible Object Families: Abstract Factory

- **When to consider it:** Several compatible objects must be selected together by product family or environment, and the design needs to prevent incompatible combinations.
- **Alternatives and distinctions:** Simple assembly may be sufficient when selecting one object or when only configuration values differ. The central concern is consistency across a family of objects, rather than individual creation points.
- **Minimal form and cost:** Define only the necessary family creation contract and actual variants. Adding a new product type requires updating multiple factories.

### Separating Complex Construction Steps: Builder

- **When to consider it:** Stepwise assembly, construction order, or complex combinations of options spread the knowledge needed to create valid results across callers.
- **Alternatives and distinctions:** Compare constructors, named arguments, or a small input object. Merely turning the same argument list into a method chain does not justify a separate structure.
- **Minimal form and cost:** Keep the necessary assembly state and completion operation. Manage exposure of incomplete objects, builder reuse, and the meaning of defaults. A separate Director is needed only when there is an assembly procedure to reuse.

### Creating from an Existing Object: Prototype

- **When to consider it:** New instances must be created from a prototype configured at runtime, and copying expresses the requirement better than reconstruction.
- **Alternatives and distinctions:** Check whether construction with a few changed values or immutable-value copying is sufficient. Avoid directly cloning objects that hold resource connections or require lifetime management.
- **Minimal form and cost:** Define a copy operation that states which state is copied and which references are shared. Shallow versus deep copying, identifiers, and mutable references may have different meanings.

### A Single Instance and Access Point: Singleton

- **When to consider it:** There is a real requirement to limit instances to one within a specific scope, and that scope and its owner are clear.
- **Alternatives and distinctions:** First consider whether creating one object at the composition point and injecting it, or configuring the container's lifetime scope, is sufficient. Distinguish needing one instance from needing a global access point.
- **Minimal form and cost:** Guarantee only the required sharing scope. Hidden dependencies, shared mutable state, interference between tests, and shutdown ownership may arise. A single object within one process cannot guarantee uniqueness across multiple processes.

## Check After Adoption

Check whether object selection preserves existing results, how required and invalid combinations are handled, and who owns creation and shutdown. Verify the actual creation contract rather than the mere existence of a factory or builder.

If multiple constructors make the intent of calls unclear, a purpose-revealing creation function may suffice. If callers repeatedly select concrete types and assemble dependencies, collecting that knowledge in a small factory may fit better. Neither case automatically requires inheritance-based creation.

## Choosing Among Combined Creation Patterns

Compatibility across a product family is the concern of Abstract Factory; the assembly steps for one product are the concern of Builder; and the point where a subtype selects a product within a common procedure is the concern of Factory Method. These structures can be combined, but first establish whether there really are three distinct responsibilities to address. When all that is needed is to assemble two objects once for an environment, a configuration function may be clearer.

Selecting an object in a factory and selecting a policy during execution are different decisions. Choosing one implementation at startup and retaining it belongs to the composition point; choosing according to each request's business conditions belongs to the business selector. If both places branch on the same code value, it becomes unclear which selection is authoritative.

## Valid Builder Results and Failure Timing

A builder may exist without required values, but a completed result must not escape in an invalid state. There is no need to repeat conditions at every builder step when a constructor or existing creation contract already guarantees them. Define consistently what completion guarantees.

When many options are mutually incompatible, compare simplifying the representation of the selection state with providing separate, meaningful creation paths. Representing every sequence through typed builder stages can make the API grow with the number of combinations. Compare the benefit of expressing order through types for the current creation contract with the cost of the additional API. Do not require repeated usage errors as a prerequisite for adoption.

If the same builder creates multiple results, check whether its internal mutable lists are shared between those results. If the contract says that changing the builder after construction must not change earlier results, break that sharing.

## The Prototype Copy Contract

The meaning of an identifier differs depending on whether a copy represents a new business object or a temporary editing snapshot of the same object. A new object may need a different persistence identifier or version, while an editing copy may need to retain the original version for conflict detection.

Distinguish immutable values that may be shared, mutable state to copy, and resources that must not be copied. Serializing and restoring the entire object can lose connections, callbacks, or lifetime information. Specify the state covered by the copy contract instead of applying deep copying indiscriminately.

## Single Instances and Lifetime Boundaries

A configuration value, request context, external connection, and mutable cache may have different lifetimes. Grouping them in one Singleton can leak request-specific state into other requests or let one resource's shutdown affect the entire feature. Distinguish the facts to share from the objects to share.

When resource reuse and concurrent request handling are actual concerns, read [Concurrency and resource lifetimes](concurrency.md) instead of assuming that creating a single instance solves them.
