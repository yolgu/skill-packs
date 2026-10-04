# React Native Directory Boundaries

Apply the framework-neutral model in architecture-model.md. First distinguish Expo Router, React Navigation, another navigator, or a custom native shell.

## Inspect the Project

Identify:

- Expo-managed or Community CLI project
- navigation library and configuration style
- file-based route roots
- deep-link and universal-link configuration
- native ios and android projects
- platform-specific file extensions
- state, persistence, query, and networking libraries
- native modules, generated code, and platform permissions
- unit, component, device, and end-to-end tests

Do not reorganize native or generated directories as though they were ordinary JavaScript feature folders.

## Domain-Oriented Application Code

For code-configured navigation:

~~~text
src/
├── app/
│   ├── navigation/
│   ├── providers/
│   ├── config/
│   └── errors/
├── domains/
│   └── orders/
│       ├── screens/
│       │   ├── list/
│       │   ├── detail/
│       │   ├── create/
│       │   ├── edit/
│       │   └── approve/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       ├── components/
│       └── config/
├── features/
└── shared/
    └── ui/
~~~

Use pages if the project targets web and already uses that term. Screen and page are both Presentation Adapters, not domains.

## Expo Router

Expo Router derives routes from files. Preserve its route root and special files.

~~~text
src/
├── app/
│   ├── _layout.tsx
│   ├── orders/
│   │   ├── index.tsx
│   │   ├── [orderId].tsx
│   │   └── create.tsx
│   └── ...
└── domains/
    └── orders/
        └── screens/
            ├── list/
            ├── detail/
            └── create/
~~~

- Keep route files inside src/app because the router treats them as pages.
- Keep non-route components, hooks, domain code, and utilities outside src/app.
- Let route files validate route input and render or delegate to domain-owned screens.
- Keep root _layout.tsx focused on application initialization, providers, themes, splash handling, and navigation layout.
- Use route groups for navigation or layout concerns, not as automatic Bounded Contexts.
- Treat every route as deep-linkable and keep parameter contracts explicit.

If the project uses a different Expo Router version or configured root, follow the installed version and configuration rather than assuming one path.

## React Navigation

With React Navigation:

- keep navigator composition in app/navigation
- let domains export screen descriptors or screen components
- keep typed route parameter lists at the narrowest common owner
- separate deep-link configuration from domain behavior
- use navigator groups for navigation presentation or shared options, not for source-code ownership
- minimize navigator nesting; navigation nesting serves UI behavior, not code organization

Do not let navigation objects leak into Domain or portable Application code.

## Screens

A screen owns:

- layout and native interaction
- route-parameter conversion
- screen-local state and lifecycle
- keyboard, focus, gesture, and accessibility presentation
- expected loading and error states
- calling an application command or query

Business rules, durable storage, transport configuration, and cross-domain writes remain outside screens.

## Platform-Specific Code

Choose the smallest mechanism:

- Platform module for a small local difference
- .ios and .android files for substantial platform-specific implementations
- .native and default files for native versus web implementations
- native modules or components behind an Infrastructure port

Keep shared domain and application code independent of Platform, native bridge, permissions, and UI types.

Platform-specific files should implement one shared contract rather than duplicate business behavior.

## State and Persistence

- screen state stays with the screen
- cross-screen workflow state belongs to a feature or application flow
- session, theme, locale, and connectivity belong to app providers
- business transitions belong to Domain/Application
- secure storage, async storage, network clients, push notifications, and native SDKs are Infrastructure
- map external records before Domain or screens consume them

Do not turn a global store into the integration mechanism between contexts.

## Navigation and Access

- identity owns session state
- screens or route descriptors declare access requirements
- app navigation applies redirects or gated stacks
- backend authorization remains authoritative
- notification and deep-link inputs enter through adapters and become typed navigation or application inputs

Test cold starts, resumed links, invalid params, authentication transitions, and platform back behavior when they matter.

## Native Projects

Treat ios and android as platform adapter and build-system roots.

- keep native configuration and permissions close to the platform
- expose a narrow typed bridge to JavaScript
- do not copy domain rules into Swift, Objective-C, Kotlin, and TypeScript
- keep generated native code in its configured output and out of ordinary refactors
- verify CocoaPods, Gradle, codegen, and platform builds in proportion to touched files

## Testing

- domain and application tests avoid React Native
- screen tests verify rendering, route input, interaction, and expected states
- adapter tests verify storage, network, notification, and native mapping
- navigation tests verify composition and access behavior
- device or end-to-end tests cover platform integration

After moves, verify Metro resolution, TypeScript, route generation, deep links, tests, and affected native builds.

## Avoid

- placing non-routes in Expo Router's app directory
- treating navigator groups or URL segments as domain boundaries
- screens calling storage or raw network clients directly
- business rules duplicated in platform-specific files
- one global screens, components, hooks, or services directory
- deep navigator nesting used only to organize code
- native bridge types leaking into Domain

## Official Documentation

- [Expo Router core concepts](https://docs.expo.dev/router/basics/core-concepts/)
- [Expo and React Native navigation](https://docs.expo.dev/develop/app-navigation/)
- [React Navigation getting started](https://reactnavigation.org/docs/getting-started/)
- [React Navigation nesting guidance](https://reactnavigation.org/docs/nesting-navigators/)
- [React Native platform-specific code](https://reactnative.dev/docs/platform-specific-code)

