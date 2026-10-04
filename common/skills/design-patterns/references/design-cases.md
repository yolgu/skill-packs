# Design Cases for Combined Problems

Each case connects requirements, candidate comparison, responsibility placement, change order, and behavior to check. Read the conditions that would change the decision rather than copying the case's objects into another task. Concrete class names are examples; use the project's business vocabulary.

## Pricing Rules and Eligibility Conditions Grow Together

### Requirements and the Current Problem

Prices within a product family are calculated from a base unit price and quantity. Rates differ by member category, and some promotions have period and eligibility conditions. A capped price with a different calculation procedure has been introduced for a particular product family. The existing method contains nested branches for members, products, and promotions.

### Comparing Candidates

| Candidate | Where it helps | Concern in this case |
| --- | --- | --- |
| Create a strategy class for every combination. | Each implementation's calculation is independent. | Classes multiply for every member/product/promotion combination, and rate data spreads through the code. |
| Put every rule in a configuration table. | Data differences such as rates and periods are easy to represent. | Representing different execution procedures in the table creates an implicit interpreted language. |
| Distinguish eligibility conditions, calculation data, and actual algorithm differences. | Only responsibilities that change independently need separation. | Establish selection points so multiple responsibilities do not evaluate the same condition redundantly. |

### Choice and Minimal Contracts

Represent rates and periods as meaningful values and configuration. Consider conditions (Specification) if promotion eligibility is combined across multiple use cases; keep a short condition used in one place as a named function. Treat calculations with a different procedure, such as capped pricing, as candidates for policies (Strategy).

| Responsibility | Input | Result |
| --- | --- | --- |
| Gather necessary facts | Product, quantity, member, and calculation reference time | Consistent facts needed for calculation |
| Determine eligibility | Calculation facts and promotion conditions | Eligibility and any required reasons |
| Select a policy | Business conditions that determine the actual calculation method | The calculation role to execute |
| Calculate the amount | Calculation facts and established configuration | Amount and any required calculation details |

If each policy independently reads the current time or external member data during calculation, even one request can use inconsistent reference facts. Compare collecting necessary facts first with whether a policy really needs to own external state.

### Change Order and Verification

First extract pure calculations that preserve current results. Distinguish branches that differ only in numbers from branches with different procedures, then move only actual procedural variants into separate policies. Consolidate selection into one point and do not repeat promotion conditions in every policy.

Check period boundaries, the order of caps and discounts, and the contract when no policy or multiple policies apply. If explaining a result or reproducing a past calculation is an actual requirement, decide how to retain the policy version and reference values used at the time. Do not add a history system without that requirement.

## Concurrent Requests for the Last Available Reservation Place

### Requirements and the Current Problem

There are nine registrations for a capacity of ten. If two requests both read nine and each add a registration, the result can be eleven. Each request uses a Repository, and the reservation target also has a rule-checking method.

### Comparing Candidates and Choosing

The presence of a repository and business object does not guarantee concurrency safety. First determine the unit in which the capacity rule must be protected together with persistence.

- If a quantity in one record suffices, compare an atomic update with a capacity condition and checking its outcome.
- If more rules must be read and calculated, compare writing conditionally on the version read and reconsidering the decision using current state after a conflict.
- Locking within a short transaction may also fit, but do not retain a connection and locks across user think time.

A consistency boundary (Aggregate) can be modeled if registration records and overall capacity have a rule that must hold together. Loading every registration into memory each time is not mandatory. Connect the rule expressed by the business model to the atomicity actually guaranteed by persistence.

If updating the place count and creating a registration record together represent one registration, both changes must commit together. Check whether it is acceptable for the count to change and registration persistence to fail, or for the registration to be saved while the count update fails. Within one database operation, handling both within the necessary transaction boundary is a candidate.

### Failures and Follow-Up Effects

A conflict can be an expected business outcome. Before automatically retrying, assess whether the registration intent is still valid and whether other effects have already occurred. Sending a success notification before persistence tells the user it succeeded even if the subsequent write fails.

When follow-up notifications are needed, determine the relationship between success determination, commit, and notification timing. Local notification after commit does not guarantee delivery if the process terminates. Expose that limit when stronger delivery is required; do not imply that a simple event object solves it.

### Execution Order to Check

Control the save order after both requests have read the same version and verify that capacity is not exceeded. Within the current change scope, also check that one request's failure does not undo another request's committed result and that rejected requests do not emit success notifications.

## Connecting Two External Place-Search APIs to an Internal Feature

### Requirements and the Current Problem

The first provider returns an empty list when there are no results. The second separately reports unsupported regions and rate-limit exhaustion. The internal view must distinguish search success, no results, and temporary search unavailability.

### Choice and Contract

An external-contract Adapter does more than rename JSON fields. It must align each provider's absence and failure meanings with the internal contract. Turning an unsupported region into an empty list can make users think there are no places in that region.

| Internal outcome | Meaning |
| --- | --- |
| Success with a result list | The search was performed and produced results. |
| Success with an empty list | The search was performed and found no matches. |
| Unsupported conditions | The provider cannot handle the requested search scope. |
| Temporary failure | The search result cannot currently be determined. |

Distinguish these outcomes only when the actual internal requirement needs them. Do not copy every external error code into an internal enum.

If one provider is selected at startup, injecting its implementation at the composition point is sufficient. If requests must select providers by region, selection becomes a separate responsibility. Do not commit to a structure with one Factory, one Strategy, and one Adapter before establishing this distinction.

### Combining with Caching or Fallback Calls

If a cache already exists, check that a valid empty result and a temporary failure are not stored as the same value. Do not arbitrarily add automatic calls to a fallback provider to hide failures when that behavior was not requested. If it is required, first check whether the providers' search scopes and result meanings are genuinely substitutable.

Connect verification of each external-response conversion to the internal result and what the caller displays. Do not merely check the number of Adapter objects or the existence of a common interface.

## Adding Output and Validation Operations to a Document Tree

### Requirements and the Current Problem

A document contains headings, paragraphs, images, and groups. Groups can contain other elements. The product contract defines a closed set of element types, and different contributors keep adding operations such as output, statistics, and accessibility checks.

### Comparing Candidates

Composite is a candidate when individual elements and groups should be traversed with the same meaning. Do not force child-addition operations onto elements for which the common operation is meaningless. Examine whether view editing and read-only traversal actually have different roles.

Continuously adding operations to each element makes changes to different operations converge in the same element files. Compare Visitor when object types are stable and gathering responsibilities by operation has substantial benefit. Keep closed types and pattern matching as an alternative when the language can express the operations clearly that way.

The minimal structure is the document shape, traversal responsibility, and implementations for each operation. Decide whether visitors recurse themselves or a shared traversal calls visitors. If both traverse children, calculations are duplicated; if each assumes the other does it, child elements are skipped.

### Conditions That Change the Choice

If plugins must be able to add arbitrary element types, the cost of a closed visitor contract grows. Reconsider whether to define small output and validation capabilities for new types or provide an extension registration point. The original Visitor choice is not permanently correct.

Focus checks on nested groups, empty groups, and new operation results. If movement and copying are requested, also check parent ownership, shared references, and the meaning of identifiers in copies.

## Stale Search Responses Conflict with an Editing Draft

### Requirements and the Current Problem

A user changes the search term and the newer request completes first. The earlier request finishes late and overwrites the results. The user is editing a note on one result, and a new query response also overwrites the draft.

### Separating the Problems and Choosing

The first problem is completion order and eligibility to update current results. The second is ownership of server facts and local drafts. Neither is solved merely by a global event bus or a hierarchy of State classes.

The state owner manages current request identity and input criteria. Use request keys and cancellation when existing data tools provide them. Separate server results from local drafts, and use the contract for user interactions to decide whether fresh results should preserve or reset the draft.

Consider Presentation Model if presentation state and action availability are shared across views. If state and transition functions suffice for one small view, do not add a separate model object. A custom hook can reuse the logic, but each call's local state is not automatically shared.

### Alternatives That Are Easy to Misapply

Single Flight coalesces concurrent requests that need the same result. Coalescing does not solve stale responses for different search terms, because the input difference produces a result difference.

A previous snapshot of the local draft may suffice for undo. Canceling unsaved edits does not require a general-purpose Command bus or persistent history store. If undo after a server save is also required, assess conflict and reversal contracts separately.

### State Transitions to Check

Start requests A and B, complete them in B-then-A order, and check that the current result is retained. Verify user behavior actually affected by the change, such as a query completing during editing, a request completing after the view closes, and retention of the draft after a failed save.
