# Flutter Directory Boundaries

Apply the framework-neutral model in architecture-model.md. Adapt Flutter's UI, data, optional domain, routing, and package conventions to the project's actual complexity.

## Inspect the Project

Identify:

- pubspec packages and workspace shape
- main entry points and environment variants
- router or Navigator API
- dependency injection and application initialization
- state-management approach
- repository, service, generated client, and persistence libraries
- code generation and generated output
- assets, localization, themes, and platform projects
- unit, widget, integration, and golden tests

Do not move generated files or platform build roots without following their generators and build configuration.

## Domain-Oriented Shape

Use this as a scalable option, not a required template:

~~~text
lib/
├── app/
│   ├── router/
│   ├── bootstrap/
│   ├── config/
│   ├── theme/
│   └── errors/
├── domains/
│   └── orders/
│       ├── presentation/
│       │   ├── pages/
│       │   ├── widgets/
│       │   └── view_models/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       └── config/
├── features/
└── shared/
    └── ui/
~~~

For a simple data-centric application, Flutter's Views, ViewModels, Repositories, and Services may be sufficient. Add a Domain or Application layer only when business behavior and orchestration justify it.

## Map Flutter Roles

| Flutter concept | Architectural role |
|---|---|
| View, Page, Screen, Widget | Presentation |
| ViewModel, Controller, Notifier | usually Presentation state or Application orchestration; inspect responsibility |
| Use case, Interactor | Application |
| Entity, Value Object, Policy | Domain |
| Repository abstraction | inward data port |
| Repository implementation | Infrastructure coordination |
| Service for REST, local files, plugin | Infrastructure adapter |
| Router and app bootstrap | Composition |

Do not classify by suffix alone. A ViewModel containing pricing invariants has misplaced Domain behavior.

## Pages and Views

A page or view owns:

- widget composition and layout
- route argument conversion
- presentation lifecycle
- page-local state
- loading, empty, expected failure, and success rendering
- invoking commands or use cases

Keep data access, serialization, durable persistence, and business invariants outside Widgets.

Use list, detail, create, and edit for ordinary resource pages. Use business verbs for actions and flows.

## ViewModels and State

- ViewModels expose data and commands needed by one view or cohesive presentation feature.
- Keep pure business invariants in Domain.
- Keep multi-repository orchestration in Application when it exceeds presentation concerns.
- Keep page-local transient state close to Presentation.
- Keep session, locale, theme, and connectivity at app scope.
- Do not create one global provider, bloc, or store containing unrelated contexts.

Follow the project's existing state library. Directory architecture does not require replacing it.

## Repositories and Services

- A repository is the source-of-truth boundary seen by Application or Domain.
- A service is a stateless wrapper around an external API, platform plugin, or data source.
- Infrastructure maps JSON, database records, plugin values, and exceptions to explicit internal types.
- Repositories do not decide business policy.
- Widgets and ViewModels do not consume raw transport DTOs when a boundary mapping is needed.

Do not add interfaces without a real architectural boundary or variation.

## Routing

- Keep root router composition in app.
- Let domains expose page builders or typed route descriptors when the router supports it.
- Keep route names and argument schemas with the owning page or domain.
- Treat deep links as external input and validate them at the Presentation boundary.
- Do not model domains from URL path nesting alone.

If a router generates files, routes, or typed classes, keep generated artifacts at configured paths and adapt around them.

## Dart Package Boundaries

Within a reusable Dart package:

- expose the deliberate public API under lib
- keep internal implementation under lib/src
- avoid consumers importing another package's lib/src
- split a separate package only when a real reusable or ownership boundary warrants it

Do not turn every domain directory into a package. Package boundaries add build, versioning, dependency, and tooling overhead.

## Platform-Specific Code

- keep android, ios, web, macos, windows, and linux roots as platform adapters
- wrap plugins and platform channels behind Infrastructure contracts
- keep platform types out of Domain
- share domain and application behavior across platforms
- use separate Presentation implementations when interaction or layout materially differs

Do not duplicate domain rules in Dart and native platform code.

## Assets, Localization, and Configuration

Use the narrowest owner:

- page-specific assets and strings near the page when supported by project conventions
- domain vocabulary and assets in the domain
- themes, application locale setup, environment binding, and global assets in app
- package declarations and asset registration in pubspec as Composition

Keep translation keys, route names, and configuration schemas in one source of truth.

## Errors

- Infrastructure converts external exceptions into explicit adapter or application failures.
- Application and Domain expose meaningful expected results.
- Presentation renders expected states.
- app-level error handling reports unexpected failures.

Do not catch and silently flatten errors in every repository or ViewModel.

## Testing

- unit-test Domain rules and Application use cases
- unit-test ViewModels through explicit dependencies
- widget-test pages and reusable Presentation components
- integration-test repositories, services, plugins, routing, and end-to-end flows
- keep golden tests with the Presentation owner

After moves, run formatting, analyzer, affected tests, code generation checks, and platform builds in proportion to the change.

## Avoid

- a universal core or utils folder containing domain-specific code
- business rules in Widgets, route callbacks, or repositories
- one global state object for unrelated contexts
- forced Domain and UseCase folders for a trivial app
- consumers importing another package's lib/src
- raw API or plugin types leaking through the application
- package-per-folder over-modularization
- platform directories treated as business domains

## Official Documentation

- [Flutter app architecture](https://docs.flutter.dev/app-architecture)
- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
- [Flutter navigation](https://docs.flutter.dev/ui/navigation)
- [Dart package layout](https://dart.dev/tools/pub/package-layout)
