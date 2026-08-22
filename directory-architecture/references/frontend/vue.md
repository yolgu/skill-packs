# Vue Directory Boundaries

Apply the framework-neutral model in architecture-model.md. Detect Vue Router, Nuxt or another file router, Pinia or other state tools, and the existing Composition API conventions before changing paths.

## Inspect the Project

Trace:

- createApp and plugin registration
- root router and route records
- layouts and file-based pages when applicable
- navigation guards and route metadata
- Pinia stores or other shared state
- composables, API clients, generated types, and DTO mappings
- aliases, auto-imports, build plugins, and test configuration

Auto-import and file-routing rules can make a directory part of the framework API. Preserve those rules or update their configuration deliberately.

## Domain-Oriented Shape

~~~text
src/
├── app/
│   ├── router/
│   ├── plugins/
│   ├── config/
│   └── errors/
├── domains/
│   └── orders/
│       ├── pages/
│       │   ├── list/
│       │   ├── detail/
│       │   ├── create/
│       │   ├── edit/
│       │   └── approve/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       ├── components/
│       ├── config/
│       └── routes.ts
├── features/
└── shared/
    └── ui/
~~~

Use existing names such as views when they are well established. The responsibility matters more than pages versus views.

## Pages and Views

A route page or view is a Presentation Adapter. It:

- receives route params and query values
- invokes application commands or queries
- coordinates view-local state
- renders loading, empty, expected error, and success states
- composes domain-owned components

Keep domain rules, transport clients, and cross-context writes outside the page.

Use resource-oriented list, detail, create, and edit names for ordinary CRUD. Use domain verbs for meaningful actions.

## Vue Router

Prefer domain-owned route records composed by the app router when routes are configured in code.

- Keep path, route name, component, and domain-owned meta together.
- Use dynamic imports for route-level code splitting when consistent with the project.
- Treat navigation guards as Presentation or Composition mechanics.
- Let route meta declare access requirements; keep the underlying authorization policy in one identity or domain source of truth.
- Type shared route meta rather than duplicating unstructured keys.
- Use URL namespaces and route names consistently.

When a file-based router owns the pages directory, keep required files thin and delegate to domains.

Do not use nested route shape as proof of nested domain ownership.

## Composables

A composable belongs to the narrowest owner:

- page composable for page lifecycle or view state
- domain composable for domain-facing presentation behavior
- app composable for session, locale, theme, or global connectivity
- shared composable only when domain-neutral reuse is proven

Do not move every function using ref or computed into a global composables directory.

## State

- component and page state stays local when no other owner needs it
- cross-page workflow state belongs to a feature or application flow
- business transitions belong to Domain/Application
- Pinia stores expose a cohesive state contract and do not become general service locators
- server cache and transport mapping remain at the data boundary

Keep role strings, statuses, and policy mappings in one typed source of truth.

## Data and Errors

- Keep HTTP clients and generated API DTOs in Infrastructure.
- Map DTOs before pages and domain behavior use them.
- Keep expected errors typed and convert them to page states.
- Let unexpected errors reach an app-level error boundary or reporting adapter.
- Avoid watchers that conceal cross-domain side effects.

## Components

- Domain components use business language and remain in the owning domain.
- Shared UI contains visual or interaction primitives without domain policy.
- Layouts belong to app or to the domain that owns their navigation shell.
- Avoid components controlled by many boolean flags for unrelated domain modes.

## Public Surfaces and Imports

Expose route records, pages required by composition, application operations, and deliberately shared types. Prevent deep imports into another domain using the project's aliases, ESLint configuration, package exports, or workspace rules.

## Testing

- test domain and application logic without Vue where possible
- test composables at their ownership scope
- test pages for route conversion, state, rendering, and user actions
- test router composition and guards
- test Infrastructure mappings separately
- retain end-to-end tests at app scope

After moves, verify auto-imports, aliases, route generation, lazy chunks, TypeScript, unit tests, and production build.

## Avoid

- global views, components, composables, stores, and services directories spanning unrelated domains
- domain decisions in route guards or Vue components
- pages consuming raw external DTOs
- one Pinia store for the entire application
- file-based route paths copied directly into the domain model
- route meta as the only enforcement of backend authorization
- auto-imports that silently bypass module public surfaces

## Official Documentation

- [Vue Router guide](https://router.vuejs.org/guide/)
- [Lazy loading routes](https://router.vuejs.org/guide/advanced/lazy-loading.html)
- [Route meta fields](https://router.vuejs.org/guide/advanced/meta)
