---
name: design-patterns
description: Decide when to introduce, combine, retain, or simplify patterns for responsibilities and collaboration, business invariants, creation, persistence, presentation state, and concurrency within a process during code design, implementation, refactoring, and code review. Compare GoF, domain, and practical code patterns by alternatives, failure conditions, and change costs, and adapt them to Java/Spring, TypeScript/React, and Dart/Flutter. Do not use for trivial edits that do not affect responsibilities or collaboration, system-wide architecture selection, or distributed processing design.
---

# Selecting and Applying Design Patterns

Choose a structure that meets current requirements while making responsibilities and the impact of changes clear. Patterns are design knowledge that explains collaboration approaches and trade-offs for recurring problems. Judge them by the problem they solve, rather than their names or how many are used.

## Start with the Current Problem

Check the requested behavior and change scope, relevant code definitions and usages, existing contracts, and project guidance. Identify what varies independently, which changes spread into other responsibilities, and who owns state and side effects. First check which responsibilities the existing structure or framework already handles.

Apply a pattern from the initial design when its benefit is clear for current requirements. Do not make a fixed duplication count or implementation count a condition for adoption. Even a single external implementation may need a boundary that isolates a real contract difference. Conversely, having two calculation methods does not by itself require strategy objects.

## Select Only the References You Need

Read the references that match the current problem and the relevant technology-specific supplements. Do not read every reference at once or iterate through the full pattern catalog on every task.

| Current decision | Reference |
| --- | --- |
| Object selection, creation, assembly, and sharing scope | [Creational patterns](references/creation.md) |
| External contract differences, wrapping, composition, and structure | [Structural patterns](references/structure.md) |
| Policies, state transitions, request handling, and notifications | [Behavioral patterns](references/behavior.md) |
| Persistence access, business conditions, values, and dependency assembly | [Practical code patterns](references/application.md) |
| Choosing between similar candidates or combining multiple patterns | [Deeper selection and composition criteria](references/selection-depth.md) |
| Business procedures, invariants, identity, and consistency boundaries | [Domain models and business flows](references/domain-models.md) |
| Differences between objects and storage structures, query composition, and concurrent updates | [Persistence and query patterns](references/persistence.md) |
| Ownership of presentation logic, editing state, and asynchronous responses | [Presentation and interaction patterns](references/presentation.md) |
| Shared state, duplicate requests, and task lifetimes within a process | [Concurrency and resource lifetimes](references/concurrency.md) |
| Comparing design decisions and reassessment after changes in complex problems | [Design cases](references/design-cases.md) |
| Implementation decisions in Java and Spring | [Java and Spring](references/java-spring.md) |
| Implementation decisions in TypeScript and React | [TypeScript and React](references/typescript-react.md) |
| Implementation decisions in Dart and Flutter | [Dart and Flutter](references/dart-flutter.md) |

## Compare with Simpler Alternatives

Alongside pattern candidates, compare reusing the existing structure, small functions or objects, and explicit branches or tables. Consider the following factors when they affect the choice. There is no need to turn them into a fixed scorecard or report.

- **Problem solved:** Is this a concrete problem established by current requirements and code?
- **Isolation of change:** Which change is contained within which responsibility?
- **Contracts and collaboration:** Does the structure clarify inputs, results, failure meanings, and relationships between roles?
- **Added cost:** How much does it add in objects and call stages, selection and assembly, lifetime management, or execution ordering?
- **Simpler alternative:** Can the same requirements and contracts be met with clearer code and lower maintenance cost?

Do not create extension points, base classes, or general-purpose frameworks solely because they might be needed later. At the same time, do not mix necessary responsibilities and contracts just to reduce line or class counts. Compare the total implementation and maintenance cost of meeting current requirements.

When candidates are similar, compare both what they make easier to change and what they make harder to change. Separate distinct axes of change, such as adding types versus adding operations, changing data versus changing execution procedures, and object identity versus value equality. When combining patterns, also check how call order, consistency boundaries, and lifetime ownership change. Do not decide from superficial branch counts or code shape alone.

Reconsider a pattern when new requirements change the reasons for choosing it. Plan small changes that preserve existing contracts, and examine whether failure, interruption, and partial-completion semantics are preserved as well as return values. The concise-explanation principle in this document applies to reporting results; do not use it to reduce the depth of internal analysis or reference material needed for the design.

## Implement Only the Necessary Roles

Adapt patterns to the project's language, framework, and existing contracts. A function may be sufficient for a single callable role, while an object may fit state or a coherent contract spanning multiple operations. Consider composing and delegating small roles before depending on the internal behavior of a large parent class, while allowing inheritance that matches a real substitution relationship or a framework's extension contract.

Do not attach an interface, factory, or forwarding layer to every class without a real contract that separates implementation details. Do not reimplement responsibilities already supplied by existing implementations, language features, an ORM, or dependency injection tools. Place the necessary pattern roles while preserving the project's public models and dependency direction.

Evaluate existing patterns by the same criteria. Simplify or remove structures that do not contribute to current requirements within the authorized change scope. Check whether structural changes alter observable behavior such as error meanings, execution order, transactions, or resource lifetimes.

## Adapt the Judgment to the Task

- **Design:** Compare candidates and simpler alternatives against established requirements.
- **Implementation:** Implement the necessary roles and adjust the choice as new facts emerge.
- **Refactoring:** Establish the behavior to preserve, then decide whether to introduce, change, simplify, or remove a pattern.
- **Code review:** Explain findings using concrete change impacts and responsibility problems. Do not treat the absence of a pattern or a nontraditional structure as a defect by itself. Review findings do not themselves authorize edits.

Match verification to changed behavior and actual risks. Check contracts affected by the chosen structure, such as the results of policy substitution, state transitions, failure meanings in external conversions, subscriptions, and resource release. Reuse existing verification, and do not merely test pattern class names or resemblance to a pattern's structure.

## Explain Only Important Decisions

For a meaningful introduction or removal, concisely explain the problem, the reason for the choice, and the complexity added or removed. Expand only when a more detailed comparison is needed. Do not append a pattern review report to a trivial edit.

Example: We will use interchangeable pricing policies (Strategy) because the policies must change independently. Calculation changes are isolated within each policy, but selecting and assembling the policy to use becomes an additional responsibility.
