# React Directory Boundaries

Apply the framework-neutral model in architecture-model.md. Detect the actual React framework and router before choosing physical paths.

## Inspect the Project

Identify:

- React framework and rendering mode
- router and whether routes are code-configured or file-based
- route loaders, actions, server functions, and error boundaries
- state-management libraries and provider placement
- data fetching, query caches, generated clients, and API mappings
- package exports, path aliases, lint rules, and monorepo boundaries
- component, route, integration, and end-to-end tests

Framework-required directories are part of its API. Preserve them and delegate to domain-owned modules when necessary.

## Domain-Oriented Shape

Use this as a concept, not a mandatory template:

~~~text
src/
├── app/
│   ├── router/
│   ├── providers/
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

Keep a smaller shape for a small application. Do not add domain and application folders when they would remain empty.

## Pages Are Presentation Adapters

A page owns:

- rendering and layout
- route-parameter and search-parameter conversion
- route lifecycle
- page-local interaction state
- expected loading, empty, and presentation error states
- calling an application command or query

A page does not own:

- domain invariants
- reusable business calculations
- raw API client configuration
- persistence decisions
- direct writes across domains

Use list, detail, create, and edit for ordinary resource pages. Use the business language for actions such as approve, cancel, checkout, or compare.

## Routes

Let each domain expose a small route descriptor or route module surface and let app compose it.

### React Router

React Router route modules can own rendering, loader, action, revalidation, and error-boundary entry points. Treat loader and action as inbound boundaries:

- validate and normalize route input
- call an application query or command
- return a presentation result
- avoid embedding domain decisions in route functions

Keep route modules thin when the router forces a physical route location. Generated route types may remain at that boundary.

### File-Based Frameworks

When a React framework derives routes from files:

- keep required route files at the framework path
- import or delegate to a domain-owned page
- keep business behavior outside layout and route-registration files
- avoid placing arbitrary utilities where the framework treats every file as a route

Do not copy the URL hierarchy mechanically into the domain model.

## State Ownership

| State | Owner |
|---|---|
| input focus, modal, selection, draft display | page or component |
| workflow state spanning a few pages | feature or application flow |
| business entity state and transitions | domain/application |
| server cache | data-query or infrastructure adapter |
| session, theme, locale, connectivity | app provider |

Do not place all state in one global store. Do not hide business transitions in generic store actions.

## Data Boundaries

- Keep generated API clients and transport DTOs in Infrastructure.
- Map external DTOs to domain or explicit presentation data before pages consume them.
- Keep query keys and cache invalidation near the data owner.
- Do not let page components call raw fetch clients throughout the tree.
- Return explicit result and error types from application operations.

Expected domain or application errors become page states. Unexpected errors reach the nearest deliberate error boundary and global reporting.

## Components

- Domain components express one domain's vocabulary and behavior.
- Shared UI contains domain-neutral primitives with proven multiple consumers.
- A component used twice inside one domain remains domain-owned.
- Hooks and providers follow the same ownership rules; hooks is not a universal shared dumping ground.
- Prefer composition to broad configurable components with business-mode flags.

## Access Control

- The identity or session module owns authentication state.
- A page or route declares its access requirement.
- The app router or guard applies navigation behavior.
- Backend authorization remains authoritative.
- Do not embed role strings and policy mappings in several pages.

## Public Surfaces and Imports

Expose a small domain entry point for consumers:

- route descriptor
- page exports needed by the router
- application commands and queries
- published domain types when genuinely shared

Block deep imports into domain internals with existing package exports, ESLint rules, or monorepo boundary tools.

## Testing

- test domain rules outside React
- test application commands and queries through explicit ports
- test pages for rendering, route input, user actions, and expected states
- test Infrastructure mappings at the adapter boundary
- keep end-to-end tests at app scope
- verify route composition, lazy loading, server/client boundaries, and provider placement after moves

## Avoid

- one global components, hooks, services, or stores directory containing every domain
- business rules in route loaders, actions, components, or store reducers
- pages importing raw API DTOs
- route folders treated as Bounded Contexts solely from URL shape
- shared components that switch behavior with many domain flags
- app providers importing domain internals
- domain modules importing browser or React types when the model should be portable

## Official Documentation

- [React Router routing](https://reactrouter.com/start/framework/routing)
- [React Router route modules](https://reactrouter.com/start/framework/route-module)

