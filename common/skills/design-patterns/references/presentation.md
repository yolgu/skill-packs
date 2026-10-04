# Presentation and Interaction Patterns

Read this when business data and presentation state are mixed, multiple components independently modify the same state, or asynchronous responses overwrite user input. Visual design and directory restructuring are outside its scope.

## What to Move Out of the View

Displayed data, selection state, input drafts, saving status, and displayed errors have different meanings. Treating committed server data and a user's in-progress edits as one object can let fresh query results overwrite drafts or let cancellation change data that was already committed.

Do not move all state into one service or hook merely to make the view lightweight. First assess whether the state's lifetime and the actions that change it belong to the same responsibility. The following patterns offer alternatives for the contract around which presentation logic is organized.

## Presentation State Independent of the View: Presentation Model

Represent displayed values, selection, action availability, and view actions in a model independent of the UI technology. This is useful when several views use the same state or interaction rules must be checked without widgets.

The minimal form is the necessary presentation state and meaningful operations that change it. The purpose is not to duplicate domain objects verbatim. If a separate copy of server facts is retained, decide when it is synchronized and how drafts differ from committed values.

Storing derivable state can introduce contradictions. Prefer a computed value for a selection count that can be calculated from the selected-item list. If performance or user experience requires retaining it separately, define the owner and update timing.

Look at the actual responsibility even when the name is ViewModel. Renaming something or adding an object that simply forwards existing state offers little benefit. Reuse the existing structure if a React state model or Flutter state owner already fills the role.

## Keeping the View to a Minimal Display Contract: Passive View

The view forwards input and executes display instructions; the Presenter owns presentation decisions and coordination. Compare this when directly testing the UI technology is difficult or behavior needs verification through an explicit display contract.

The minimal form is the necessary input events, display contract, and coordination responsibility. Abstracting every widget property one for one creates a second UI API to maintain. Dozens of imperative display methods are costly when passing state to a declarative view would suffice.

Even with presentation decisions in the Presenter, actual input wiring and rendering integration remain. Presenter call tests alone do not establish that users saw the correct result. Check behavior rules and actual wiring to the extent needed for each.

## Separating Simple Binding from Complex Coordination: Supervising Controller

Leave simple data-to-display connections to the view's binding facilities and put complex interaction coordination in a controller. Compare this when the framework handles basic presentation well and moving every display instruction behind a separate contract would be costly.

The responsibility split between view and controller matters. If business rules spread into view binding expressions or callbacks beyond simple display logic, maintaining the same rules along other paths becomes difficult. State which decisions remain in the view and which belong to the controller.

Presentation Model emphasizes an independent representation of view state; Passive View minimizes decisions made by the view; Supervising Controller divides responsibilities while using simple binding. Choose the approach that most clearly expresses the necessary state and interactions in the current technology.

## Asynchronous Requests and State Lifetimes

A user can change a search term and start request B after request A, yet receive B's response first. Assigning every response to current results in completion order lets stale A overwrite newer B. Adding global events or making each request a State object does not solve this.

Distinguish which request is eligible to update the current result. Use request keys and cancellation from existing data tools, or a minimal approach that compares identity established at request time and current input. Canceling an earlier request and ignoring a response that has arrived are different responsibilities.

Judge duplicate save requests differently from queries. Whether two save clicks represent the same operation or different changes determines their treatment. Disabling a button does not prevent duplicate execution across the entire persistence path. Distinguish the scope guaranteed by the current task from the server contract.

## Editing and Undo

Undoing a local draft can be represented by a Memento or immutable snapshot retaining prior state. If undo and redo are needed at the granularity of user commands, compare Command and change records.

Decide whether to retain each keystroke as a separate command or group them into one editing action so history matches user intent. Undoing a result already saved to the server requires more than overwriting a local snapshot. Check for conflicts with later changes and the server's contract for reversing a change.

Do not introduce a separate command bus if a form library's change tracking and draft state already serve the purpose. Do not duplicate patterns by creating both Memento and Command for every field.

## Criteria for Changing a Presentation Pattern

| Established problem | Change to compare |
| --- | --- |
| The same presentation rules repeat across views. | Move them into pure calculations or a cohesive presentation model. |
| Copies of state hold different values. | Establish the actual owner and distinguish derived values from drafts. |
| External effects unrelated to state are coupled to rendering. | Move execution responsibility to match user intent or a lifetime boundary. |
| Maintaining the display contract is more complex than the actual view. | Compare declarative state passing or the current framework's composition mechanisms. |
| Stale responses change current state. | Define request identity, eligibility to apply results, and termination semantics. |

Match verification to user-visible state transitions and interactions rather than the internal structure of render functions. Check input, request completion and failure, retry or cancellation, and view termination when the change actually affects those paths.
