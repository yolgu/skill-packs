---
name: code-principles
description: Apply language- and framework-agnostic code quality principles when writing, changing, refactoring, debugging, testing, or reviewing human-authored source code, tests, scripts, queries, build logic, infrastructure code, and executable configuration. Use for coding work that requires judgment about correctness, contracts, responsibility, ownership, state, side effects, duplication, abstraction, boundaries, errors, compatibility, or verification. Also use whenever authoring or modifying human-authored Python or TypeScript, including tests, migrations, runnable examples, and one-off or inline verification code, so explicit type declarations are applied consistently. Do not use for simple code explanations, running existing commands without authoring code, mechanical text edits, non-code work, or decisions about system architecture, database design, deployment, cost, or technology selection.
---

# Universal Code Principles

## Apply Specific Guidance First

Follow more specific project, language, framework, and task guidance when it applies. Apply these
universal principles to decisions that the more specific guidance does not settle.

Do not add a separate skill-discovery or routing step. Let normal skill selection and task context
determine any other applicable guidance; do not inventory, install, or summarize skills as part of
this workflow.

Treat explicit user constraints, project instructions, executable contracts, tool configuration,
and established verification commands as concrete guidance. Treat repeated legacy patterns as
evidence to evaluate, not automatic authority.

## Work in This Order

1. Establish the requested behavior, completion criteria, observable contracts, and permitted scope.
2. Inspect the relevant project rules, structure, names, definitions, usages, data sources, and tests.
3. Identify the authoritative owner of each affected fact, rule, state transition, and contract.
4. Reuse an existing concept when it already owns the responsibility; otherwise choose the smallest
   design that makes the responsibility clear.
5. Implement the change so the main path reads in problem order and important effects are visible.
6. Verify the changed behavior, critical invariants, and likely regression paths with the project's
   established tools.
7. Report the outcome, material trade-offs, completed verification, and remaining verification gaps.

Discover facts from the repository and available environment instead of guessing or asking the user
to supply facts that can be inspected. Ask for decisions only when the answer changes authorized
scope, observable behavior, or another material result.

## Resolve Principle Conflicts

Apply this quality order when desirable qualities compete:

1. Required behavior and real contracts
2. Security, data integrity, and safe failure
3. Clear intent, responsibility, and ownership
4. A single authoritative source for facts, rules, state, and contracts
5. Maintainability and controlled change impact
6. The simplest design that fully solves the current problem
7. Consistency with project and language conventions
8. Speculative extensibility, micro-optimization, and clever brevity

Adjust a lower-priority preference when necessary to protect a higher-priority quality. Do not use a
principle mechanically when doing so would weaken correctness or clarity.

## Preserve the Core Qualities

- Implement actual behavior and non-functional requirements, not merely code that compiles.
- Give each rule, fact, state, and mutation path one clear owner.
- Remove duplicated knowledge, not every repeated sequence of text.
- Introduce an abstraction only for a real concept, shared knowledge, or stable boundary.
- Make state ownership, mutation, and externally visible side effects explicit.
- Express public inputs, outputs, failure modes, semantic values, and local value types precisely.
  Apply the explicit Python and TypeScript declaration rule below.
- Validate untrusted boundaries, rely on established internal invariants, and never hide failures.
- Use intention-revealing names, cohesive units, narrative flow, and comments that explain why.
- Protect real change boundaries with small public surfaces; do not impose ceremonial layers.
- Preserve observable behavior during refactoring unless a behavior change is explicitly authorized.
- Apply the same correctness, clarity, and verification baseline to all code. Solve smaller problems
  with simpler designs, not weaker quality.
- Treat relevant security, performance, concurrency, and operability conditions as part of
  correctness, while leaving concrete techniques to more specific guidance.

Read [Universal Principles](references/universal-principles.md) in full for non-trivial creation,
behavior changes, contract or boundary work, stateful code, or structural refactoring.

## Make Python and TypeScript Types Explicit

When authoring new or modifying existing human-authored Python or TypeScript:

- Declare an explicit type for every variable declaration or first binding that the language grammar
  permits, including obvious literals and variables that store function-call results.
- Declare parameter and return types for every function, method, nested function, test function,
  callback, TypeScript arrow function, and asynchronous function whose syntax permits it.
- Do not repeat the annotation on later assignments to an already declared variable.
- Apply the rule to source, tests, code-based fixtures, migrations, one-off diagnostic or verification
  scripts, inline executable code, and runnable examples. In existing files, limit it to declarations
  added or materially changed by the current task. Exclude generated and vendored code.
- Permit omission only where the language grammar cannot express the annotation, such as Python
  comprehension, `for`, `with ... as ...`, `except ... as ...`, and lambda bindings.
- Avoid Python `Any` and TypeScript `any` except at an unavoidable untyped external boundary. Narrow
  TypeScript `unknown` to a concrete type before using it in trusted internal logic.
- Treat an annotation as a declared contract, not as conversion or runtime validation. Do not add
  casts, conversion calls, runtime checks, type-checker dependencies, or pipeline configuration only
  to satisfy this rule.

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

## Respect the Requested Work Mode

- **Implement or modify:** Change the necessary human-authored code and tests within the authorized
  scope. Do not broaden the task into repository-wide cleanup.
- **Refactor:** Preserve observable behavior by default. Characterize unclear behavior before changing
  its structure, and keep unrelated defect fixes separate.
- **Review:** Do not edit files without separate authorization. Report evidence-backed findings by
  actual impact rather than personal preference.
- **Explain or diagnose:** Inspect and explain the behavior or cause. Do not infer authorization to
  implement a fix.

Read [Review and Verification](references/review-and-verification.md) in full for reviews, debugging,
bug fixes, behavior-preserving refactors, test design, failed checks, or completion assessment.

## Finish on Evidence

Use the project's official wrappers and established checks. Verify observable behavior and important
invariants rather than implementation trivia. Add regression evidence for bug fixes. Classify failed
checks before retrying, and change the approach when the failure is not transient.

Do not claim that an unrun or unavailable check passed. Apply the principles quietly: keep generated
code, comments, documentation, and the final response free of compliance narration. Explain only
material design choices, intentional compatibility exceptions, verification results, and unresolved
gaps.
