# Concurrency and Resource Lifetimes Within a Process

Read this when multiple tasks access the same memory or resources, requests overlap, or task termination and resource release do not align. Distinguish concurrency patterns and implementation techniques used alongside classical patterns. Do not introduce new distributed systems or operational restrictions by default.

## Distinguish a Single Instance from Concurrency Guarantees

Singleton and container single-instance scopes are decisions about object count and lifetime. They do not guarantee that concurrent requests can safely mutate the object. First check whether mutable state is actually shared and whether request-specific state in local variables would suffice.

Even in a single-threaded event loop, other tasks can change state across an asynchronous wait. A read-wait-update flow must determine whether the conditions observed at the read still hold. Using one object does not by itself serialize business processing.

## A Single State Owner and Serialized Work

Consider assigning one party to modify shared state while other tasks send requests to it. An Actor or serial execution queue can serve this role, but a separate framework is not mandatory.

The minimal form is a state owner, input requests, and processing order. Decide whether another request may be accepted while one task waits for an external call, and what the state means during that interval. Message ordering does not automatically make a sequence of requests atomic.

Long-running work delays other requests, and a reentrant call waiting for completion on the same queue can stall progress. Do not add a new work queue when simple synchronous calls to the current owner are sufficient.

## Immutable Snapshots and Copying Before Replacement

When reads are frequent and a change must expose one consistent set of values, compare completing a new snapshot before replacing the reference. A reader consistently uses either the old snapshot or the new one.

The minimal form distinguishes the draft being changed from the published immutable state. Safe publication and replacement of the reference must be guaranteed by the runtime's concurrency mechanisms. Copying only the outer object while sharing internal lists may not produce an immutable snapshot.

Readers seeing a consistent snapshot and writers avoiding lost updates are separate concerns. If multiple tasks calculate new values from the same prior state, even an atomic reference replacement can overwrite an earlier change. When such updates overlap, serialize the update from read through replacement or use an atomic update based on the current value. Do not add locks or checks when the existing state owner or tool already provides that guarantee.

Frequent writes or large data increase copying and memory costs. Compare whether briefly locking a small state object or using an existing immutable-state tool is clearer. A snapshot is not the same concept as a caching strategy that guarantees the latest storage values.

## Coalescing Concurrent Duplicate Requests: Single Flight

When overlapping concurrent queries for the same result create significant cost, one in-progress task per key can be shared. Unlike caching, which retains completed results, the focus is coalescing duplicates while work is in progress.

The key must express result equivalence. The same place identifier may not imply the same request if language, query conditions, or access scope differ. Include input differences that matter. Writes that look identical can represent different intentions, so do not coalesce them by the same rules as queries.

The minimal form is registering an in-progress task, joining it, and removing its registration after completion. Clean up registration when the shared task terminates through success, failure, or cancellation. If the implementation can remove a registration and start new work under the same key before the earlier task finishes, prevent the earlier task's late cleanup from removing the new registration. Do not add a separate identity check for this when no such replacement path exists.

One participant stopping its wait differs from canceling the operation shared by everyone. Decide whether one caller's cancellation may also eliminate the result for other participants. Do not automatically expand this into permanent caching, duplicate suppression across processes, or retries.

## Producers, Consumers, and Throughput Control

When the rate of task creation differs from processing speed enough to exceed memory or actual resource limits, consider adjusting a work queue and consumer count. First understand current throughput, response-time, and resource-limit requirements.

Even the minimal form must distinguish queued tasks from running tasks. Limiting worker count while allowing an unbounded queue can still let memory usage grow indefinitely. Decide which response to a full queue is valid for the business: waiting, rejection, coalescing, or dropping work.

Dropping or rejecting work changes the actual contract, so do not choose it arbitrarily. Use existing executor or data-tool queue settings when they suffice. Do not treat this as a rule to add queues and limits to every call.

## Reusing Borrowed Resources: Object Pool

Consider a reuse pool when creation and shutdown are expensive or the number of external resources available concurrently is limited. An ad hoc pool for lightweight ordinary objects can instead add initialization and concurrency costs.

Make borrowing and returning resources, restoring their normal state, and discarding unusable resources explicit. State from a previous user must not remain. Borrowing a resource and then waiting for another from the same pool can exhaust resources and stall progress.

Do not wrap framework-owned resources, such as connections in an established connection pool, in a second pool. Do not hide the cause of slow work merely by increasing pool size.

## Resource Release and Cancellation at the Appropriate Scope

Decide whether the creator or consumer owns a resource. Make the contract explicit, for example by assigning ownership to the creator and prohibiting borrowers from closing it. Use the language's resource-scoping facilities or try/finally, dispose, and release callbacks.

Owned resources must be released on exceptions, early returns, and cancellation as well as success. Check whether callbacks can still modify state after the object that started a subscription or task is gone.

Distinguish cancellation offered by the task API, stopping a wait, and ignoring a result. JavaScript's native Promise and Dart's native Future do not themselves have cancellation methods. Handle actual task termination and result application according to the API's contract; requesting cancellation or stopping a wait does not imply that I/O or a worker thread has stopped. Do not create a separate cancellation layer when ignoring the result is sufficient. Prevent late completion from registering resources again or reviving disposed state.

## Concrete Execution Orders to Verify

Do not require a whole-system load test by default. First examine small execution sequences that can break the changed contract.

- Two requests start under the same key, the first fails, and a new request arrives.
- One participant cancels while another still awaits the result.
- Asynchronous completion arrives after an object has been disposed.
- A slow consumer causes the queue to fill.
- An exception occurs after a resource is borrowed, or nested borrowing is attempted.

Select only sequences with actual risk and reuse existing tests that cover the behavior. If further verification is needed, use a sufficient method with current tools, such as a small test that controls request completion order. Do not require a separate executor. The mere presence of a concurrency pattern or lock is not evidence of a correct design.
