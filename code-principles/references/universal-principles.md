# Universal Code Principles

## Contents

- [How to Use These Principles](#how-to-use-these-principles)
- [Core Principles](#core-principles)
  - [Honor Real Behavior and Contracts](#honor-real-behavior-and-contracts)
  - [Make Responsibility and Ownership Explicit](#make-responsibility-and-ownership-explicit)
  - [Keep One Authoritative Source for Knowledge](#keep-one-authoritative-source-for-knowledge)
  - [Use the Smallest Meaningful Abstraction](#use-the-smallest-meaningful-abstraction)
  - [Expose State Changes and Side Effects](#expose-state-changes-and-side-effects)
  - [Make Public Contracts Precise](#make-public-contracts-precise)
  - [Make Python and TypeScript Declarations Explicit](#make-python-and-typescript-declarations-explicit)
  - [Validate Boundaries and Preserve Failure Meaning](#validate-boundaries-and-preserve-failure-meaning)
  - [Write for Human Understanding](#write-for-human-understanding)
  - [Protect Real Change Boundaries](#protect-real-change-boundaries)
  - [Distinguish Rules from Existing Patterns](#distinguish-rules-from-existing-patterns)
  - [Control Change Scope and Compatibility](#control-change-scope-and-compatibility)
  - [Treat Relevant Quality Attributes as Correctness](#treat-relevant-quality-attributes-as-correctness)
  - [Keep the Same Core Quality Baseline](#keep-the-same-core-quality-baseline)
  - [Change the Authoritative Source, Not Generated Output](#change-the-authoritative-source-not-generated-output)
- [Resolve Competing Qualities](#resolve-competing-qualities)
- [Contextual Decisions](#contextual-decisions)

## How to Use These Principles

Use the core principles to protect qualities that every implementation needs. Resolve syntax and
tooling choices from explicit project rules, actual contracts, and established tools. Evaluate a
repeated implementation pattern against responsibility and contract requirements before reusing it.

Do not use these principles to force code into a uniform shape. Preserve their intent using the
clearest native expression available in the target context.

## Core Principles

### Honor Real Behavior and Contracts

**Principle.** Establish and preserve the behavior that callers and operators can actually observe.

**Why.** Internal structure is valuable only when the system still satisfies its functional and
non-functional contracts. Output shape, ordering, absent values, failures, event order, effect timing,
and file or data meaning may all be observable behavior.

**Decision test.** What can a caller, user, dependent component, stored dataset, or operator observe
before and after this change?

- Do not infer the full contract from one implementation detail or one passing test.
- Trace callers, schemas, configuration, tests, and runtime evidence when the contract is unclear.
- Treat required security, performance, and reliability properties as part of correct behavior.

### Make Responsibility and Ownership Explicit

**Principle.** Give each fact, rule, state transition, and mutation path one understandable owner.

**Why.** Clear ownership keeps decisions cohesive, limits change impact, and prevents multiple parts
of a system from independently interpreting or mutating the same concept.

**Decision test.** Which unit has the knowledge and authority required to make this decision, and
would it change for the same reason as the behavior placed there?

- Judge cohesion by reasons to change, not file length or the number of functions.
- Keep public surfaces no larger than their consumers require.
- Place problem-specific behavior near the data and rules it genuinely owns.
- Avoid vague names that conceal which decision or effect a unit owns.

### Keep One Authoritative Source for Knowledge

**Principle.** Centralize duplicated knowledge, not every repeated sequence of code.

**Why.** A fact, rule, schema, state meaning, or mapping that can diverge needs one authority. Similar
text that changes for independent reasons does not necessarily represent the same knowledge.

**Decision test.** Must these occurrences always change together for the same reason?

Centralize when occurrences encode the same:

- business or validation rule;
- state or code meaning;
- schema, contract, or configuration fact;
- transformation whose meaning must remain identical.

Keep separate when code is only structurally similar, changes independently, or would require flags,
branches, or a vague abstraction to share it.

### Use the Smallest Meaningful Abstraction

**Principle.** Introduce an abstraction only when it names a real concept, owns shared knowledge, or
protects a stable boundary.

**Why.** Abstractions can clarify responsibility and contain change, but speculative layers add
indirection, configuration, and coupling without protecting a real need.

**Decision test.** What concrete concept, shared knowledge, or boundary becomes clearer and safer
because this abstraction exists?

- Do not abstract only because another implementation might exist someday.
- Do not add a pattern merely because it can be applied.
- Do not create production abstractions solely to make mocking convenient.
- Allow a single implementation behind a boundary when the boundary itself is real.
- Keep multiple implementations separate when they do not share a stable semantic contract.

### Expose State Changes and Side Effects

**Principle.** Make the owner, path, and consequences of state changes and external effects visible.

**Why.** Hidden mutation, global state, and order-dependent effects make behavior difficult to reason
about, test, retry, and operate.

**Decision test.** Can a reader tell who may change this state, when it changes, and which external
effects a call can produce?

- Keep mutable state scoped to the smallest responsible owner and useful lifetime.
- Keep business decisions with their business owner. A data representation may use constructors and simple accessors; do not invent business methods for a storage or transfer object.
- A lookup, question, or calculation must not hide an externally observable mutation. A command may return a meaningful result; mutation does not imply a void return.
- Separate calculation from external effects when doing so makes the flow clearer.
- Keep network, storage, filesystem, time, randomness, and process effects at identifiable boundaries.
- Use immutability and pure computation when they improve clarity; do not treat them as mandatory
  syntax.

### Make Public Contracts Precise

**Principle.** Express public inputs, outputs, failure modes, optionality, semantic values, and major
effects precisely enough that callers do not need to inspect the implementation. Keep names,
interfaces, responses, and documentation consistent with the observable behavior consumers can
rely on.

**Why.** Precise contracts prevent accidental misuse and turn hidden assumptions into information
that tools and humans can check.

**Decision test.** What would a consumer reasonably expect from this contract, and does the actual
behavior fulfill that expectation in its scope, effects, completion timing, and failure outcomes?

- Establish the intended contract from requirements and consumer expectations before evaluating
  consistency.
- Distinguish values that share a primitive representation but carry different meaning.
- Expose nullability, optionality, partial success, units, formats, and state constraints when callers
  must handle them.
- Base communicated capabilities and states on the rules that actually determine them. Use indirect
  conditions only when they reliably represent the promised meaning.
- Resolve mismatches against the intended contract. Do not rename or redescribe incorrect behavior
  merely to make it appear consistent.
- Preserve implementation freedom behind the contract. Expose internal details only when they affect
  what consumers must know or can rely on.
- Avoid leaking broad, shapeless containers beyond a boundary when a meaningful structure exists.
- Follow the target context's type style except for the explicit Python and TypeScript declaration
  rule below.
- Do not introduce wrapper types that add no validation, meaning, ownership, or contract clarity.
- When behavior or its communicated meaning changes, check the affected contract and usages for
  consistency while respecting compatibility and task scope.

### Make Python and TypeScript Declarations Explicit

**Principle.** Declare types explicitly wherever Python or TypeScript grammar permits when authoring
new or modifying existing human-authored code.

**Why.** Explicit declarations let a reader see the expected type at each binding and callable
boundary without reconstructing it from an initializer, a called function, or distant contextual
inference. Small and temporary code still needs to be understandable when it fails or is reused.

**Decision test.** Can a reader determine every annotatable binding, input, and return type from the
declaration being read?

- Annotate every variable declaration or first binding, including obvious literals and variables
  that store function-call results even when the called function already declares its return type.
- Annotate the parameters and return of every function, method, nested function, test function,
  callback, TypeScript arrow function, and asynchronous function whose syntax permits it. Include
  `-> None` and `: void` where they describe no returned value.
- Apply the rule to product source, tests, code-based fixtures, migrations, one-off investigation,
  diagnostic and verification scripts, inline executable code, and runnable examples.
- Do not repeat an annotation on later assignments to an already declared variable.
- Permit omission only where the language grammar cannot express an annotation. Python
  comprehension, `for`, `with ... as ...`, `except ... as ...`, and lambda bindings are examples;
  do not create ceremonial pre-declarations merely to work around those syntax limits.
- Avoid Python `Any` and TypeScript `any` except at an unavoidable untyped external boundary, and do
  not let them spread into trusted internal logic. Narrow TypeScript `unknown` to a concrete type
  before using it there.
- Apply the rule to declarations added or materially changed by the current task. Do not mass-edit
  untouched existing code, generated output, installed dependencies, or vendored source.
- Do not confuse an annotation with a conversion or runtime check. Do not add `str()`, `String()`,
  casts, parsers, runtime validation, type-checker dependencies, or pipeline configuration merely to
  make the declaration explicit.

```python
def load_member(member_id: int) -> Member:
    member: Member = repository.get(member_id)
    return member
```

```typescript
function loadMember(memberId: number): Member {
  const member: Member = repository.get(memberId);
  return member;
}
```

### Validate Boundaries and Preserve Failure Meaning

**Principle.** Validate untrusted data at trust boundaries, rely on established internal invariants,
and never erase the meaning of failure.

**Why.** Boundary validation prevents invalid state from spreading, while repeated defensive checks
inside trusted code obscure the main flow and create competing validation rules.

**Decision test.** Where does this value become trusted, and how will a caller distinguish expected
failure from a programming defect?

- Validate user input, external responses, stored records, files, environment values, and other
  untrusted data when they enter a trusted context.
- Represent the established invariant through the target context's normal contract mechanisms.
- Do not repeat the same null, range, or format check at every internal call.
- Handle a failure, translate it without losing essential context, or propagate it clearly.
- Do not convert failure into an empty value, false success, ignored log entry, or partial mutation.

### Write for Human Understanding

**Principle.** Make names, unit boundaries, and top-level flow explain the problem in the order a
reader needs to understand it.

**Why.** Code is maintained through reading. Clever brevity and mechanical decomposition can make a
small diff expensive to understand and risky to change.

**Decision test.** Can a reader understand the purpose, main decisions, and effects without repeatedly
jumping into implementation details?

- Prefer intention and problem meaning over generic technical names.
- Keep a unit focused on one coherent purpose rather than a fixed line-count limit.
- Reduce deep nesting, hidden mode flags, and implicit call-order requirements.
- Use guard clauses when they expose failure conditions and reduce nesting. Choose clear operation names or semantic alternatives for execution modes; a genuine Boolean data attribute is not a mode flag.
- Use comments for external constraints, compatibility reasons, trade-offs, and non-obvious risks.
- Do not comment what the code already states clearly.

### Protect Real Change Boundaries

A consumer uses a provider's published contract. These are relative roles: an object can provide one capability and consume another. Choose the contract in terms of the consumer's task, without exposing the provider's private representation.

Trace static dependencies separately from runtime calls. A reference in a field, parameter, return type, generic argument, annotation, inheritance clause, or conversion method is a source dependency even if the method is static. Runtime delegation through an interface does not require the consumer to import the implementation.

Ask which implementation detail or independent reason to change the boundary protects:

- Define inputs, results, and failure meanings that the consumer can understand without inspecting the implementation.
- Keep implementations dependent on the protected contract when the consumer must remain independent of their technology.
- Keep conversions with code allowed to know both representations. A public model accepting an internal provider type in its factory still exposes that dependency.
- Separate public boundary models when ownership, meaning, validation, or change reasons differ, even when their fields currently match.
- Reuse an existing type for internal transfers that do not introduce a distinct contract. Do not add a copy at every method call.
- Keep the source graph acyclic and limit each consumer to the part of a contract it needs.
- Keep a single implementation behind an interface when that interface protects a real boundary. Do not require interfaces for every class or for mocking alone.

These are source-contract decisions; directory names and framework mechanisms are outside this reference's scope.

### Distinguish Rules from Existing Patterns

**Principle.** Follow explicit project rules and real contracts; evaluate repeated code patterns as
evidence rather than unquestioned authority.

**Why.** Existing code contains both deliberate conventions and copied historical mistakes. Blind
consistency can reproduce defects, obsolete techniques, and accidental complexity.

**Decision test.** Is this pattern required by an explicit rule or contract, or is it merely repeated?

Treat the following as concrete guidance:

- explicit user scope and requirements;
- project instruction and contribution files;
- compiler, type checker, formatter, and linter configuration;
- public interfaces, schemas, file formats, and other executable contracts;
- established verification commands and intentionally adopted structure.

Treat undocumented legacy patterns as context to understand. Do not clean up unrelated violations,
and do not copy a harmful pattern when the current change can use a clearer compatible approach.

### Control Change Scope and Compatibility

**Principle.** Change only what the authorized task requires, and preserve observable behavior during
refactoring unless a behavior change is explicitly authorized.

**Why.** Unrelated cleanup, hidden defect fixes, and mixed structural and behavioral changes increase
review cost and regression risk.

**Decision test.** Is each changed line necessary for the requested behavior, a directly related
quality improvement, or evidence that proves the change?

- Permit adjacent refactoring that is necessary to make the requested change clear and safe.
- Keep repository-wide cleanup and broad structural changes separate.
- Characterize unclear existing behavior before restructuring it.
- Keep unrelated defect fixes separate from a refactor.
- Record intentional compatibility differences and their observable impact.
- Do not preserve an obvious security vulnerability or data-loss risk silently; surface the conflict
  before expanding the authorized scope.
- Use completion verbs only after confirming that the referenced artifact or transition actually
  exists and has reached that state.

### Treat Relevant Quality Attributes as Correctness

**Principle.** Include relevant security, performance, concurrency, reliability, and operability
requirements in the definition of correct behavior.

**Why.** Functionally plausible code can still fail its real contract through unauthorized access,
data races, duplicate effects, unbounded work, or failures that cannot be diagnosed.

**Decision test.** Which quality attribute could invalidate this behavior under its real operating
conditions?

- Examine trust boundaries, authorization, sensitive information, and command execution when present.
- Examine shared state, asynchronous work, retries, duplicate delivery, and idempotency when present.
- Optimize from measured evidence, complexity analysis, or explicit scale requirements.
- Preserve enough failure context and observability to diagnose operationally important behavior.
- Leave concrete security, synchronization, caching, and observability techniques to more specific
  guidance.

### Keep the Same Core Quality Baseline

**Principle.** Apply the same correctness, clarity, and verification baseline to every piece of
human-authored code.

**Why.** Inferring that code is temporary, small, or unimportant gives an automated author permission
to omit investigation, contracts, error handling, and evidence without user authorization.

**Decision test.** Am I simplifying the design because the problem is simple, or weakening quality
because I guessed that the code matters less?

- Do not infer reduced quality from file size, location, or apparent lifetime.
- Do not assume the user values coding speed over correctness.
- Honor an explicitly limited experiment or verification scope without inventing one.
- Add rigor for identified risk without dropping established project checks for supposedly low risk.

Apply the same core quality principles to all code. Scale complexity down through simpler design, not
through weaker correctness, clarity, or verification.

### Change the Authoritative Source, Not Generated Output

**Principle.** Modify human-owned source definitions rather than generated, vendored, or build-owned
artifacts.

**Why.** Direct edits to derived artifacts are overwritten, break reproducibility, and create a second
source of truth.

**Decision test.** Which schema, declaration, configuration, dependency definition, or generator owns
this output?

- Apply the principles to application code, tests, scripts, queries, migrations, build logic,
  infrastructure code, executable configuration, and usable code examples.
- Change a generator input or configuration instead of generated output.
- Change a dependency declaration instead of vendored source when the normal dependency workflow owns
  that code.
- Let official tools update lock and build-owned artifacts through their supported workflows.

## Resolve Competing Qualities

When design qualities compete, prioritize:

1. Required behavior and real contracts
2. Security, data integrity, and safe failure
3. Clear responsibility and ownership
4. One authoritative source of knowledge
5. Maintainability and controlled change impact
6. The simplest design that satisfies the current need
7. Consistency with established language and project conventions
8. Speculative extensibility or clever brevity

A more specific syntax convention does not automatically resolve a responsibility or contract defect. Respect explicit instructions and actual external contracts; evaluate incidental patterns against the affected behavior.

## Contextual Decisions

Resolve these choices from the target language, project, and more specific guidance rather than from
this skill:

- programming paradigm and modeling style;
- module, package, directory, and architectural naming;
- local type annotation and inference style for languages other than the explicit Python and
  TypeScript rule above;
- exception, result, error-code, or other failure representation;
- mutable versus immutable representation;
- dependency injection and component lifecycle mechanisms;
- transaction, asynchronous, and concurrency mechanisms;
- test framework, test-double style, and fixture conventions;
- formatting, linting, serialization, persistence, and code-generation tools.
