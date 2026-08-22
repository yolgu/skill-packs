# Compatibility and Change-Scope Rules

## Table of contents

- [Rule strengths and conflicts](#rule-strengths-and-conflicts)
- [External contracts](#external-contracts)
- [Compatibility exceptions](#compatibility-exceptions)
- [Change scope](#change-scope)
- [Review and completion reporting](#review-and-completion-reporting)

## Rule strengths and conflicts

Use rule strengths with these meanings:

- `MUST` and `MUST NOT`: requirements for normal new code
- `SHOULD` and `SHOULD NOT`: defaults to follow in most cases, while allowing a better project-specific choice
- `MAY`: an option permitted when its conditions are met
- `COMPATIBILITY EXCEPTION`: a narrow departure from a general rule required to preserve an existing external contract

### COMPATIBILITY-001 — MUST

Resolve conflicting rules in this authority order:

1. The actual business behavior and explicit constraints requested by the user
2. Existing external API, data, and operational compatibility
3. Project build, formatter, naming, and test rules
4. Domain invariants and data integrity
5. Security and sensitive-data protection
6. This skill's `MUST` and `MUST NOT` rules
7. `SHOULD` and `SHOULD NOT` rules
8. `MAY` rules

Do not promote a project convention that exposes sensitive data or bypasses authorization into a good rule.

## External contracts

### COMPATIBILITY-002 — MUST

The following are public or operational contracts, not simple code-style details. Do not change them without an explicit request and verification:

- Public Java signatures and packages used by external modules
- API URLs, HTTP methods, fields, types, null behavior, status codes, error bodies, and headers
- Event and Message schemas
- Database schema and persistence-code meaning
- Configuration keys and Bean names
- Batch Job and Step names and execution parameters
- Serialization structure, sessions, cookies, redirects, sorting, pagination, and file results

Preserve external contracts through adapters and mappers even while improving names or separating objects internally.

### COMPATIBILITY-004 — MUST

When existing behavior contains an obvious security vulnerability or data-loss risk, do not reproduce it silently. Explain the dangerous behavior, affected contract, available preservation or correction choices, and verification method to the user, then follow the authorized decision.

## Compatibility exceptions

### COMPATIBILITY-003 — MUST

Isolate compatibility code that differs from a general rule at the narrowest adapter boundary, such as a legacy Controller, Response, mapper, or compatibility Policy. Track:

- The excepted rule ID
- The external contract being preserved
- Why the general rule cannot be applied
- The permitted class and method scope
- The verification test
- The reconsideration condition

Use a concise format such as the following when a code comment is necessary.

```java
// COMPATIBILITY EXCEPTION: JSON-002
// Legacy client treats an empty nickname as unregistered.
// Scope: LegacyMemberResponse
// Verification: LegacyMemberApiCompatibilityTest
// Revisit: after legacy client support ends
return nickname == null ? "" : nickname;
```

Do not spread the exception behavior into general Domain rules or new APIs.

## Change scope

### COMPATIBILITY-005 — MUST

Change only what is causally necessary to complete the requested implementation, modification, or refactoring. The following directly related refactorings may be included:

- Consolidating a duplicated business rule into one source of truth
- Moving a misplaced decision to the correct object
- Extracting a Value Object or method required for the change
- Improving an ambiguous name
- Isolating an SDK or Entity type leaking across the current boundary
- Making the changed behavior testable

### COMPATIBILITY-006 — MUST NOT

Do not mass-fix unrelated legacy violations. Do not rewrite a whole file or module or broadly move packages for a one-line change. Do not combine renaming every DTO, separating every JPA model, adding an interface to every Service, converting every SQL statement to QueryDSL, or replacing every Lombok annotation in one task.

Do not add an unrequested feature, API, database change, Event, dependency, framework, common wrapper, or authorization system under the label of code style. Do not claim to remove something that did not exist.

Apply the relevant `MUST` and `MUST NOT` rules to new code. Safely improve obvious violations and boundary leaks directly related to the current file change. Do not modify unrelated existing code; report it as a follow-up candidate only when it affects the current risk.

## Review and completion reporting

### COMPATIBILITY-007 — MUST

Do not interpret a review request as authorization to modify files. Include the following in a review finding:

- Rule ID and strength
- Exact location
- Actual behavioral, security, or maintenance impact
- Recommended correction
- Contract and compatibility risk

Distinguish rule strength and actual impact; do not report a style preference as though it were a critical defect.

### COMPATIBILITY-008 — MUST

Make an implementation completion report communicate the following instead of focusing on rule compliance itself:

- The actual changed outcome and boundaries
- Material design and style decisions
- Retained compatibility exceptions
- Executed test, formatter, and build commands and their results
- Verification that could not be completed and remaining risks

Classify a verification failure as caused by the current change, pre-existing, environment or permission related, a missing dependency service or database, transient network failure, or an incorrect command.
