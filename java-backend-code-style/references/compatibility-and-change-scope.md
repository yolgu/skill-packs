# Compatibility and Change-Scope Rules

## Table of contents

- [Rule strengths and conflicts](#rule-strengths-and-conflicts)
- [External contracts](#external-contracts)
- [Compatibility exceptions](#compatibility-exceptions)
- [Change scope](#change-scope)
- [Review and completion reporting](#review-and-completion-reporting)

## Rule strengths and conflicts

Rule-strength meanings are defined in [Rule Application](../SKILL.md#rule-application).

<a id="compatibility-001"></a>
### Resolve Java rule conflicts from explicit contracts

**COMPATIBILITY-001 · MUST**

Apply the user's requested behavior and scope, explicit project instructions, and the actual Java, HTTP, data, and operational contracts. A formatter or framework discovery requirement settles that technical issue; repeated source patterns do not automatically justify a responsibility or data-integrity defect.

Use the strengths above for this skill's Java rules. Do not rank other skills as higher or lower authorities or require them to be loaded. Inspect the actual conflict and preserve required behavior without silently copying a security or data-loss defect.

## External contracts

<a id="compatibility-002"></a>
### Preserve public and operational contracts

**COMPATIBILITY-002 · MUST**

The following are public or operational contracts, not simple code-style details. Do not change them without an explicit request and verification:

- Public Java signatures and packages used by external modules
- API URLs, HTTP methods, fields, types, null behavior, status codes, error bodies, and headers
- Event and Message schemas
- Database schema and persistence-code meaning
- Configuration keys and Bean names
- Batch Job and Step names and execution parameters
- Serialization structure, sessions, cookies, redirects, sorting, pagination, and file results

Preserve external contracts through adapters and mappers even while improving names or separating objects internally.

<a id="compatibility-004"></a>
### Address security and data-loss risks explicitly

**COMPATIBILITY-004 · MUST**

When existing behavior contains an obvious security vulnerability or data-loss risk, do not reproduce it silently. Explain the dangerous behavior, affected contract, available preservation or correction choices, and verification method to the user, then follow the authorized decision.

## Compatibility exceptions

<a id="compatibility-003"></a>
### Keep compatibility exceptions narrow and traceable

**COMPATIBILITY-003 · MUST**

Isolate compatibility code that differs from a general rule at the narrowest adapter boundary, such as the affected Controller, Response conversion, or policy. Track:

- The excepted rule ID
- The external contract being preserved
- Why the general rule cannot be applied
- The permitted class and method scope
- The verification test
- The reconsideration condition

Do not assume a legacy system or introduce a compatibility component by default. When a real supported contract needs an exception, use a concise comment only if code and tests do not explain it.

```java
// COMPATIBILITY EXCEPTION: JSON-002
// The supported client treats an empty nickname as unregistered.
// Scope: MemberResponse
// Verification: MemberApiContractTest
// Revisit: when the supported client contract changes
return nickname == null ? "" : nickname;
```

Do not spread the exception behavior into general Domain rules or new APIs.

## Change scope

<a id="compatibility-005"></a>
### Limit refactoring to the requested work

**COMPATIBILITY-005 · MUST**

Change only what is causally necessary to complete the requested implementation, modification, or refactoring. The following directly related refactorings may be included:

- Consolidating a duplicated business rule into one source of truth
- Moving a misplaced decision to the correct object
- Extracting a Value Object or method required for the change
- Improving an ambiguous name
- Isolating an SDK or Entity type leaking across the current boundary
- Making the changed behavior testable

<a id="compatibility-006"></a>
### Avoid unrelated cleanup and unrequested features

**COMPATIBILITY-006 · MUST NOT**

Do not mass-fix unrelated existing violations. Do not rewrite a whole file or module or broadly move packages for a one-line change. Do not combine renaming every DTO, separating every JPA model, adding an interface to every Service, converting every SQL statement to QueryDSL, or replacing every Lombok annotation in one task.

Do not add an unrequested feature, API, database change, Event, dependency, framework, common wrapper, or authorization system under the label of code style. Do not claim to remove something that did not exist.

Apply the relevant `MUST` and `MUST NOT` rules to new code. Safely improve obvious violations and boundary leaks directly related to the current file change. Do not modify unrelated existing code; report it as a follow-up candidate only when it affects the current risk.

## Review and completion reporting

<a id="compatibility-007"></a>
### Keep reviews read-only unless changes are authorized

**COMPATIBILITY-007 · MUST**

Do not interpret a review request as authorization to modify files. Include the following in a review finding:

- Rule ID and strength
- Exact location
- Actual behavioral, security, or maintenance impact
- Recommended correction
- Contract and compatibility risk

Distinguish rule strength and actual impact; do not report a style preference as though it were a critical defect.

<a id="compatibility-008"></a>
### Report outcomes, verification, and remaining gaps

**COMPATIBILITY-008 · MUST**

Make an implementation completion report communicate the following instead of focusing on rule compliance itself:

- The actual changed outcome and boundaries
- Material design and style decisions
- Retained compatibility exceptions
- Executed test, formatter, and build commands and their results
- Verification that could not be completed and remaining risks

Classify a verification failure as caused by the current change, pre-existing, environment or permission related, a missing dependency service or database, transient network failure, or an incorrect command.
