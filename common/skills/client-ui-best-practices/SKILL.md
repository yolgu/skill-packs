---
name: client-ui-best-practices
description: Design, implement, refactor, diagnose, and review state ownership, component and widget boundaries, feature structure, server state, forms, routing, asynchronous flows, tests, accessibility, performance, and security in Vite + React + TypeScript and Flutter + Dart client code, fitted to the repository's context. Use for React and Flutter work where UI architecture, state management, data flow, or feature boundaries matter. Do not use for pure styling, deployment, backend-only work, or unrelated simple edits. Use it with code-principles loaded alongside.
---

# Client UI Best Practices

First confirm the repository's current contracts and state ownership, then design and carry out Vite + React + TypeScript or Flutter + Dart client work in the smallest scope. Do not impose library preferences or folder templates; produce correct ownership, explicit data flow, and verifiable user behavior.

## Determine the Request Mode

Determine the mode first from the user's verbs and explicit scope.

- **Review**: Find defects read-only. Do not modify files. Always also read [review-rubric.md](references/review-rubric.md).
- **Diagnosis**: Trace the cause and its evidence. If the user did not request a fix, do not modify files.
- **Design**: Present boundaries and options that fit the repository's actual structure and constraints. If there is no implementation request, do not modify files.
- **Implementation, modification, or refactoring**: Change the files and tests the request needs, and run the project's verification commands.
- **Mixed request**: Perform only the explicitly requested changes, and separate the rest into a separate proposal.

If the mode is ambiguous, perform read-only exploration first. Do not expand a read-only request into implementation authority.

## Identify the Target Technology and Select References

Before asking the user, check the manifest, lockfile, configuration, imports, and target files.

1. When the target is `package.json`, the lockfile, Vite configuration, `tsconfig`, React imports, and actual source, read [react-typescript.md](references/react-typescript.md).
2. When the target is `pubspec.yaml`, the lockfile, Flutter and Dart SDK constraints, Flutter imports, and actual source, read [flutter-dart.md](references/flutter-dart.md).
3. Even when a monorepo contains both technologies, read only the reference for the feature or file the user specified.
4. Read both references only when one request actually changes both clients together.
5. Read [review-rubric.md](references/review-rubric.md) together with the technology reference only in review mode.

Do not conclude the target technology or deployment platform merely because a configuration file exists. Cross-check actual imports, build configuration, and usages.

## Workflow

### 1. Understand the Scope and Repository Contracts

- Summarize the user's goal, completion criteria, non-goals, and changeable scope in one sentence each.
- Check existing user changes in the working tree and preserve unrelated changes.
- Check architecture and layer boundaries, naming, file layout, dependency direction, and test conventions.
- Check state management, server state, routing, forms, serialization, test tools, and their actual versions in the manifest, lockfile, and imports.
- Find the actual build, typecheck, lint, analysis, and test commands in package scripts, tool configuration, and project documentation.

### 2. Trace Definitions and Usages

- First perform a broad semantic search that covers the feature, data flow, and state ownership.
- Search for the same concept several times with different wording.
- Trace the target symbol's definition, creation points, transformations, all major consumers, and tests.
- Determine which of the API contract, schema, type, config, constant, or fixture is the single source of truth.
- Do not create a new abstraction before checking whether an existing abstraction already solves the request.

### 3. Classify State Ownership

For each state, determine its meaning, authoritative owner, consumers, mutators, lifecycle, restoration requirements, and disposal point. Place it in the following order.

1. If it can be computed from other values, derive it instead of storing it.
2. Transient presentation state is owned by the nearest component or widget that uses it.
3. In-progress drafts and displayed errors are owned by the form boundary.
4. If sharing, bookmarking, refresh, or back-navigation restoration is needed, the URL, router, or navigation owns it.
5. Remote data and its freshness, loading, and error are owned by the query/cache layer.
6. For values persisted on the device, make the storage repository the authoritative boundary.
7. Client domain state that several screens modify together is owned by a feature-scoped state object.
8. Promote to app global only state with an app-wide lifecycle, such as the authentication session.

Do not duplicate the same server data in the query cache, global store, and local state. Do not store the same URL value in both the router and a store. If duplication is unavoidable, state its purpose, authority, synchronization direction, conflicts, expiry, and disposal.

### 4. Design Responsibilities and Data Flow

Make the following flow readable in the code.

`User input → intention-revealing command → state object / Use Case → Repository / external boundary → explicit state transition → UI`

- Reveal user intent, as in `submitOrder`, `retryPayment`, and `selectDeliveryAddress`, rather than `setLoading` or a generic setter.
- UI focuses on rendering, composition, and passing input along.
- Domain does not depend on the framework, HTTP, storage, or the router.
- Application and Use Case coordinate domain behavior and external boundaries.
- Infrastructure implements APIs, storage, analytics, and platform APIs.
- Assemble dependencies at the app's starting point or a clear composition root.
- Do not create mutable global singletons or a service locator accessible from anywhere.

Apply DDD, Clean Architecture, and OOP in proportion to the actual domain complexity. Introduce an Entity when there is identity and a lifecycle, a Value Object when there is meaning and validation rules, a Use Case when coordinating several boundaries, and a Repository or interface when protecting a real external boundary. Do not create empty layers or decorative abstractions with only one implementation for simple CRUD.

### 5. Decide Component and Widget Boundaries

Split by responsibility, state ownership, lifecycle, and reason for change, not by line count.

- Consider splitting when there is independent state, effects, async work, error handling, or a test contract.
- Consider splitting when it changes for a different reason than its parent, or is used repeatedly with the same meaning and contract.
- Do not split based only on a long JSX or widget tree, speculation about future reuse, or a fixed file size.
- If after splitting you pass many implementation-detail props straight through, reconsider the boundary.
- When boolean flags multiply and one element takes on several roles, consider composition, explicit variants, or slots and children.
- Proceed through a feature screen slice top-down, in this order: the route and page, then the components and command or query hooks used only within that page (the ViewModel in Flutter), pure domain only when there are real rules, and last the request declarations and the API client (the repository implementation in Flutter). Lower layers build only what the upper layer actually needs.
- Only work that builds the reusable parts themselves, such as a design system or a shared UI kit, proceeds bottom-up (Component-Driven Development).
- Do not promote something to `shared` merely because it is used twice. Make it shared only when a second page needs it with the same meaning and the same direction of change, and the same contract and clear ownership are also confirmed.
- Keep shared UI primitives from depending on a specific feature store, API client, or route.

### 6. Settle the Async, Server, Form, and Routing Contracts

- For important async flows, model exclusively only the states actually needed among `initial`, `loading`, `success(data)`, `empty`, `refreshing(previousData)`, and `failure(error, previousData?)`.
- For overlapping requests, deliberately choose one of latest-wins, duplicate blocking, or sequential execution.
- Decide the authoritative cache update or invalidation policy after a mutation.
- Use optimistic updates only when there is user value and a rollback contract.
- Decide the list of screen states at design time, as the async states above plus retry, and write as a rule which screen state each server error response maps to.
- Decide at design time the state the URL will own and the log and analytics event points.
- Separate the owners of form drafts, client guidance validation, domain rules, and server validation. For each rule, first ask "Does the server already own this rule?"; if the server owns it, the client keeps only form guidance validation, preview calculation, offline behavior, and screen state transitions, and reuses the server's computed results. Guard against the weakness of network doubles drifting from the real contract with OpenAPI-based type and handler generation and runtime schema parsing of responses.
- Parse the URL path, query, and deep links as external input, and keep the serialization and deserialization rules in one place.
- Do not hide state that must be restored in memory-only route extras or a temporary store.

### 7. Judge Rule Strength and Change Scope

Classify rules into the following three levels.

- **Required contract**: A rule that prevents actual malfunctions, data inconsistency, or security and privacy risks. Do not copy a violation as it is.
- **Strong default**: Feature-first, local state first, intent-centered APIs, a dedicated server-state owner, accessibility as a completion criterion, and so on. Allow an exception when there is repository evidence.
- **Situational heuristic**: Specific store, form, or router tools, memoization, codegen, file splits, and so on. Choose by the current version, team standards, and measurement results.

Do not replace existing Redux, Zustand, BLoC, Provider, ChangeNotifier, and the like out of personal preference. Change only the minimum scope that fixes an actual defect, and separate broad migrations into a separate proposal. Do not use “because it is a best practice” as the reason for a change.

## Required Contracts

- Give one fact one authoritative owner.
- Do not run side effects such as network, persistence, or analytics during React render or Flutter build.
- Convert external input such as APIs, storage, URLs, environment, files, deep links, and platform channels into internal types with runtime validation or an explicit parser.
- Do not assume external data is valid based only on a static type assertion or cast.
- Do not silently swallow errors or turn them into unrelated defaults. Distinguish recoverable errors from contract and program errors.
- Make clear the owner and the cleanup and cancellation of resources such as subscriptions, controllers, streams, animations, and requests.
- Do not treat client route guards and hidden UI as final authorization.
- Do not put secrets, tokens, passwords, or unnecessary personal data in the client bundle, binary, logs, analytics, or error reports.
- Check the trust boundary and the validation and sanitization of raw HTML, WebView content, external URLs, redirects, and file paths.
- Decide the disposal scope of per-user cache and sensitive state at logout and account switch.
- Treat accessibility as a feature completion criterion, not optional after-the-fact work.
- Do not use user-facing strings as state codes or domain decision values. Domain and Application return meaningful codes and types instead of translated sentences.

## Performance, Offline, and Observability

- Use stable domain identifiers as list keys, and limit the scope of state subscriptions to the actual consumption scope.
- Do not store derived state and server state redundantly, and avoid repeated heavy computation in render and build.
- Apply broad memoization, caching, normalization, and virtualization when there are reproduction conditions and measured evidence.
- The default is online-first. Do not mistake the cache for an authoritative offline-first local model.
- Only when offline editing is an explicit requirement, design the command queue, idempotency, conflicts, retention, account isolation, and recovery as a separate synchronization domain.
- Put logs, error reports, and analytics behind a provider-neutral Infrastructure boundary.
- Do not record the same error at several layers, and manage event contracts as a typed single source.

## Versions, Dependencies, and Code Generation

- Check the current API from the installed manifest, lockfile, imports, and official documentation.
- Do not upgrade a dependency merely because it is the latest, or perform a major migration that was not requested.
- Add greenfield dependencies minimally, after checking the stable official documentation at the time of work and the actual need.
- Use code generation only when deriving repeated contracts from an authoritative declaration such as an OpenAPI or GraphQL schema, serialization declarations, or typed route declarations.
- Do not edit generated files directly. Keep the declaration as the single source of truth and reproduce the generate and validate commands.

## Tests and Completion Criteria

For behavior changes, add or update tests at the nearest responsibility boundary. For a feature screen slice, write the outer-loop test first.

- The outer-loop test enters the route, operates like a user, and asserts the screen result, with only the network replaced by a double. Its form is a page or feature-area integration test using MSW for React, and a widget test given a fake repository for Flutter. Write one normal flow first in a failing state, and after it passes, close the slice with failure paths and accessibility.
- Verify domain rules with framework-free unit tests.
- Verify Use Cases and state transitions with controllable doubles of external boundaries.
- Test the real implementation of each repository or API client that Use Case and screen tests double against a network double (MSW for React, a fake HTTP client for Flutter); that test is the double's contract test.
- Verify components and widgets by the results the user sees and the interactions, rather than internal implementation.
- Verify the actual branches, such as loading, success, empty, failure, retry, duplicate submission, and routing.
- Keep E2E tests that go all the way to the real backend only for app-scope core user journeys with a high cost of failure.

In implementation mode, run the relevant tests, typecheck, lint, Dart analysis, format check, and the needed build defined by the repository. Classifying failures, retrying, and reporting verification that could not be run follow the verification rules of code-principles.

In review, diagnosis, and design modes, keep files unchanged and present conclusions with their evidence. The final response delivers the result first and briefly summarizes only the changed files, key judgments, passed verification, and remaining verification gaps.
