# Django Directory Boundaries

Apply the framework-neutral model in architecture-model.md. This document distinguishes Django's project and application conventions from DDD boundaries.

## Detect the Actual Django Shape

Inspect:

- manage.py and the selected DJANGO_SETTINGS_MODULE
- project packages containing settings, root urls, asgi, and wsgi
- INSTALLED_APPS and AppConfig classes
- URL includes and namespaces
- models, migrations, managers, views, serializers, forms, admin, signals, tasks, and management commands
- database routers and transaction usage
- test settings, fixtures, and test layout

Account for plugins or reusable applications installed outside the repository.

## Project Is Composition; App Is Not Automatically a Context

Django's project package commonly owns system composition:

~~~text
project/
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── domains/
    ├── ordering/
    └── billing/
~~~

The settings package, root URLconf, ASGI/WSGI entry points, and top-level middleware belong to Composition Scope.

A Django application is a framework feature package registered through INSTALLED_APPS. Treat it as a Bounded Context only when its language, rules, data ownership, and change cohesion support that interpretation.

## Context Package

A domain-oriented Django app can use:

~~~text
ordering/
├── apps.py
├── urls.py
├── models/                     # Django ORM persistence model package
├── migrations/
├── presentation/
│   ├── views/
│   ├── serializers/
│   └── forms/
├── application/
├── domain/
├── infrastructure/
├── admin.py
└── tests/
~~~

Adapt to the existing project. Django discovers particular modules and paths, so keep framework entry points at expected locations or use them as thin delegates.

Do not create empty packages. A small app may keep urls.py and a thin views.py while moving only substantial behavior into application and domain.

## Models and Domain

Distinguish:

- **Django ORM model:** persistence mapping, query integration, database constraints
- **Domain entity or value object:** business behavior and invariants

For a rich domain, keep domain objects independent from django.db and map them in Infrastructure. For a simple data-centric app, avoid duplicating models only to imitate DDD; still keep business rules cohesive and out of views and serializers.

Do not spread the same invariant across model clean methods, forms, serializers, and views. Choose one domain source of truth and convert external input at the boundary.

Managers and QuerySets express persistence queries. They should not become general business-decision services.

## Application and Presentation

### Application

Use explicit use cases or application services for:

- transaction orchestration
- loading domain objects
- invoking domain behavior
- persisting changes
- publishing effects
- returning explicit results

### Presentation

Views, REST viewsets, serializers, forms, and GraphQL resolvers:

- parse and validate external input
- call Application
- convert results to HTTP or presentation types
- do not contain core business policies
- do not coordinate several repositories directly

Keep framework request objects out of Application and Domain.

## Settings Ownership

Django uses one selected settings interface for the running process. Preserve it as application composition while keeping ownership explicit.

- Put environment selection, databases, middleware, installed apps, root URLs, templates, caches, and global security in project settings.
- Put a context-specific setting definition, schema, and default close to the owning context.
- Bind or validate context configuration in Composition and pass a typed value inward.
- Access configured settings through django.conf.settings at framework edges rather than importing a concrete settings module.
- Do not mutate settings at runtime.
- Do not duplicate the same business default in settings, serializers, and domain code.

Splitting settings into base and environment modules is an organization technique, not permission to duplicate keys.

## Routes

- Let each context expose its urlpatterns or a small URL registration surface.
- Let the root URLconf compose them with include.
- Use URL namespaces for stable ownership and reverse lookup when appropriate.
- Keep endpoint names in the owning context.
- Do not infer a Bounded Context solely from URL nesting.
- Keep custom root error handlers in Composition.

## AppConfig and Initialization

Use AppConfig for framework application metadata and narrowly scoped initialization. Avoid database access or business workflows during application-registry initialization. If signals are registered during ready, keep handlers as adapters that delegate to Application or Domain.

Do not use import-time side effects to coordinate contexts.

## Data and Migrations

- Keep migrations in the Django app that owns the model and data meaning.
- Give each table one logical writer.
- Use another context's public use case, query, event, or published read model instead of importing its ORM models for mutation.
- Treat cross-app ForeignKey declarations as architectural dependencies and review their ownership implications.
- Treat database routers and shared models as explicit infrastructure decisions, not invisible shortcuts.

When splitting an app, plan migration state, table names, content types, permissions, and historical-model imports before moving ORM classes.

## Admin, Tasks, Commands, and Signals

- admin is an inbound Presentation adapter.
- management commands are inbound application adapters.
- background tasks and schedulers are inbound adapters that call Application.
- signals are integration mechanics, not a home for hidden business workflows.

Make ownership and failure behavior visible. Prefer an explicit use case over implicit signal chains for essential synchronous behavior.

## Testing

- Domain tests run without Django when the domain is framework-independent.
- Application tests use explicit port fakes or the project's established test strategy.
- ORM and repository tests use Django database integration tests.
- view, serializer, form, and URL tests stay in Presentation.
- migration tests protect meaningful data transformations.
- system-level tests verify settings, app registration, middleware, and root routing.

Use Django's system checks and migration checks in addition to the project's test suite.

## Refactoring Safely

When moving a Django app or model:

1. identify app labels and dotted import paths
2. preserve or deliberately migrate database table identity
3. update INSTALLED_APPS and AppConfig
4. update URL includes and namespaces
5. update migration dependencies and historical imports
6. update content types, permissions, admin, signals, tasks, and commands
7. repair tests and fixtures
8. run system, migration, and focused behavior checks

Do not perform a large model move from folder aesthetics alone.

## Avoid

- treating every Django app as a Bounded Context
- putting unrelated domain rules in one global models or services package
- views or serializers writing several contexts' tables
- importing concrete settings modules from reusable code
- mutable runtime settings
- business workflows hidden in AppConfig.ready or signals
- cross-context ORM imports presented as harmless reuse
- duplicate domain and ORM models without a protected boundary

## Official Documentation

- [Django settings](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Django applications and AppConfig](https://docs.djangoproject.com/en/stable/ref/applications/)
- [Django URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Django migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django system checks](https://docs.djangoproject.com/en/stable/topics/checks/)
