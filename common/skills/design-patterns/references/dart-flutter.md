# Decisions in Dart and Flutter

Check the project's Dart SDK constraints, Flutter setup, and actual state management approach. First compare expressing the same roles through existing functions, value types, state owners, and object composition.

## Functions and Creation Approaches

An interchangeable policy (Strategy) with one operation can be expressed as a function type and callback. Consider an object when state or a coherent contract spanning multiple operations is needed. Pass required collaborators to constructors or functions, and use a small interface when there is a real external boundary or substitution contract.

Named constructors can express creation intent. A Dart factory constructor can return an existing instance or an instance of a subtype. Using this syntax alone does not mean that the GoF Factory Method or Abstract Factory is being applied.

Do not create a separate Builder when named arguments, constructors, and existing value-creation facilities suffice. Do not equate a widget's build method or a builder callback with the GoF Builder merely because of the name. Determine whether construction steps and assembly state genuinely need separation.

## State Types and State-Specific Behavior

Finite presentation states can be expressed through enums, sealed types where supported, or existing state tools. If explicit state-specific data and transitions are enough, do not split every state into a behavioral object. Consider State when grouping multiple actions and complex transitions by state makes them clearer.

Do not duplicate ownership of state and transitions between an existing Notifier, BLoC, or ViewModel and new state objects. Do not slip an SDK upgrade into the task just to use a particular type feature.

## Widget Composition and Observation

Use widget composition and callbacks within the current presentation approach. Do not create a large base widget and Template Method structure from a shared appearance or a few duplicated lines alone. Distinguish view composition from interchangeable business policies.

Check whether Listenable, Stream, or the current state tool already provides change notifications (Observer). Before adding another event bus, determine who actually needs to publish and who needs to react. Establish ownership of subscriptions, cancellation, dispose, and resource release, and check late asynchronous responses after the state owner terminates within the affected change scope.

Determine shared lifetimes within existing composition and state-management scopes. Do not introduce a mutable global Singleton simply for convenient access from every feature. Even if global access already exists, do not expand the current task into an unrelated wholesale replacement.

## Repository and Platform Boundaries

Use a Repository to provide the required data contract and isolate differences between external data sources. Its responsibility can overlap with an Adapter that translates platform or SDK inputs, results, and errors, so first check ownership in the existing implementation.

Work that needs only one repository call can remain in the current entry point. When a real responsibility emerges to coordinate multiple repositories and independent business rules, consider a small business object to own it. Do not add a separate layer for every pattern or a Use Case for every operation.

Check whether a new repository or adapter creates a second owner or duplicate cache for the same data. Do not repeat one conversion responsibility across a repository, client, and mapper.

## Example Decisions

Converting platform location-query results to the application's place-query contract can start as one implementation. A clearly typed callback may suffice for sorting selectable items. Even for complex presentation state, first make transitions explicit in the current state tool, then compare which responsibility separate state objects would clarify.

## Combining State with Different Lifetimes

A view's draft, query results shared across the application, and platform connections can have different lifetimes. If one ViewModel or Singleton owns them all, closing a view can close a shared connection, or view-specific state can remain retained indefinitely. Distinguish creation, borrowing, and shutdown responsibilities.

Use the scope supplied by a state tool when it manages object lifetimes and subscriptions. When adding an Observer, check whether both the existing subscription and the new one process the same change. Distinguish adding a notification layer from actually separating responsibilities.

Decide where to apply the result if the object awaiting an asynchronous task has terminated. Updating results in a shared repository may still be necessary, while changing the draft or navigation state of a closed view is a separate matter. Do not establish a blanket rule to cancel every task or apply every result.

Use [Presentation and interaction patterns](presentation.md) for presentation-state roles and [Concurrency and resource lifetimes](concurrency.md) for per-participant cancellation of shared work and resource ownership.
