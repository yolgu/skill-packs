# Business Models and Consistency Boundaries

Read this when business rules are scattered across entry points or when it is unclear which object guarantees a rule despite dividing the objects. This addresses responsibility allocation within one application; it does not require splitting services or adopting a new system architecture. Use [Practical code patterns](application.md) alongside it for basic choices about values, conditions, and persistence access.

## Three Ways to Organize Business Rules

### A Procedure per Request: Transaction Script

Gather the handling of one request into a readable procedure. This fits when reading the necessary data, applying rules, and storing the result form a simple flow without complex invariants shared across requests.

The minimal form is a cohesive business entry method and genuinely shared calculations. Being procedural does not mean putting all logic in one enormous method or mixing in data access. The project's existing persistence boundary can still be used.

Its limits become visible when multiple procedures change the same rule differently or callers must remember the sequence needed to produce valid state. An object that owns shared rules can then be introduced. There is no need to move every simple CRUD feature into a complex object model.

### Modeling Data and Behavior Together: Domain Model

When the rules and state transitions of the same business object must hold across multiple use cases, express their meaning through object behavior. Model independent values, identified objects, and their relationships according to actual business concepts.

The minimal form is objects that own rules and the collaboration they need. A duplicate of every data record or a separate layer is not mandatory. Moving a method into an entity still leaves invariant ownership unclear if external services can arbitrarily change its internal fields.

The benefit is coherent changes to rules and state; the cost is managing object lifetimes, relationships, and differences from the storage representation. That cost can outweigh the benefit in features that mainly move data. Do not require the same degree of modeling for every feature in an application.

### Business Logic Organized by Table: Table Module

Define a class for a table or view, with one object handling the business logic for its rows. Instead of creating a business object per order, an object responsible for the orders table handles rules for multiple orders. Consider this when organizing business rules around row sets is natural; a function that computes over a list or a batch-processing module is not this pattern merely for that reason.

Compare Domain Model when individual records need rich behavior and identity. Do not turn set processing into repeated per-object operations that greatly increase query and update counts. Conversely, do not group unrelated business rules into one module solely because of table structure.

The three approaches can coexist according to the nature of each feature. Do not rank them by how sophisticated their names sound or by the number of layers.

## A Business Entry Contract: Service Layer

Define a cohesive entry contract when screens, batches, or external inputs invoke the same business operation and its execution order and transaction boundary must remain consistent. Coordinate the necessary queries, business behavior, and result persistence rather than merely forwarding calls.

With Domain Model, the entry layer coordinates which data to obtain and which behavior to invoke, while business objects decide their own rules. In a feature using Transaction Script, the entry method itself may own the procedure.

Do not create an interface/implementation pair just because there are many external callers. Assess whether an independently stable public contract is actually needed. Do not duplicate core rules in each controller merely because multiple entry points exist.

## Identity and the Lifecycle of Values: Entity

Model around identity when something must be tracked as the same business object even after its name or attributes change. Compare Value Object when equal values mean the same thing. A primary key in a database table does not make every object a business entity.

Check whether equality or collection membership changes before and after an identifier is assigned. Do not confuse the lifetime of an editing copy or transfer object with the lifecycle of the actual business object. Express the rules that state-changing behavior must guarantee through the object's public operations.

A business Entity and an ORM entity designation are different concepts. If the project uses storage-only entities, keep business behavior in separate objects while preserving its existing persistence contract.

## A Boundary for Rules That Must Hold Together: Aggregate

Consider a consistency boundary when changes to multiple objects must jointly satisfy an invariant. Its root controls changes inside the boundary and exposes the necessary behavior externally. A containment relationship or an entire connected set of foreign keys does not automatically define the boundary.

For example, a rule that the total number of registrations must not exceed capacity is difficult to uphold through an operation that looks at only one registration. Decide who evaluates the overall rule and how that decision remains connected to persistence under concurrent updates.

The minimal form is an entry point to the boundary, the data to protect together, and change operations. A huge object that loads all related data into memory is not required. An overly broad boundary increases concurrent-update conflicts and read costs, while an overly narrow boundary scatters rules across boundaries.

A root method checking a rule does not automatically prevent concurrent database updates. Connect the rule to an actual persistence contract, such as version conditions, atomic updates, or locking. Do not use a pattern slogan to prohibit a current requirement to change multiple objects in one transaction. Consider necessary atomicity and boundary size together.

## Business Calculations That Belong to No Single Object: Domain Service

Use this when a calculation or decision expresses a relationship among business concepts and would be unnatural as the behavior of one particular object. Its name, inputs, and results should reveal business meaning.

The minimal form is an operation that receives the necessary facts and makes a decision or calculation. Keep it stateless if there is no reason to retain state. Decide whether it also handles repository access or external effects according to its actual role and the project's dependency contracts; do not collect every rule in services by default.

If services increasingly extract an object's internal fields to repeat the same calculations, examine whether rule ownership is misplaced. Using multiple objects does not by itself require a Domain Service. Simple execution coordination can belong in the Service Layer.

## A Business Fact That Has Already Occurred: Domain Event

Consider this when a meaningful business occurrence must be represented and responsibilities reacting to it need separation. Distinguish a request to do something (Command) from a fact about what has happened (Event).

The minimal form is the fact's meaning, the necessary data from that time, and the publication point. Passing a mutable business object directly can let recipients observe values different from those at the time of the event. Decide which identifiers and historical values to include and on what basis.

Do not delegate actions needed to uphold mandatory invariants to events with unclear recipient ordering. For local synchronous processing, check whether recipient failure fails the publishing operation and whether execution occurs before or after commit. Running after commit reduces propagation of rolled-back facts, but does not guarantee delivery if the process terminates.

If durable delivery or consistency across services is required, a separate guarantee mechanism must be chosen. Do not assume local events solve it, and do not automatically add distributed processing infrastructure that was not part of the current task.

## Concrete Criteria for Placing Rules

| Question | Natural owner candidates |
| --- | --- |
| Does it concern the meaning and operations of one value? | Value Object |
| Does it concern the state and behavior of an identified object? | Entity or its consistency boundary |
| Does it combine eligibility conditions across values? | Specification or a named condition function |
| Is it a business calculation that belongs to no single object? | Domain Service |
| Does it coordinate the order of queries, behavior, persistence, and external effects? | Service Layer or Transaction Script |
| Does it notify another responsibility of an established business fact? | Domain Event |

This table is not a list of objects to create. Use it to find the current owner of a rule and reduce duplicated decisions. When moving roles, check that the same invariants hold across different input paths.
