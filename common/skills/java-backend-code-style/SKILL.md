---
name: java-backend-code-style
description: Write, modify, refactor, or review Java backend implementation using explicit Java types, role-based names, DTO construction and conversion, storage-only JPA entities, Spring Data, QueryDSL, SQL, Spring transactions, and framework-specific tests. Use for concrete Java and framework decisions, not for selecting an overall directory architecture.
---

# Java Backend Code Style

## Scope

Own concrete Java source and framework rules. Use this skill independently; no other skill is a prerequisite. Preserve explicit project contracts and the authorized change scope. Existing code patterns are evidence, not automatic exceptions to these rules.

Inspect the module's Java/toolchain version, build and formatter settings, package declarations, annotation processors, public signatures, and relevant tests. Apply framework rules only when that technology is actually used.

## Select References

The [rule index](references/rule-index.md) is a navigation catalog. Rule definitions and strengths live in the linked sections. Read only the references relevant to the work, in full.

| Work | Reference |
|---|---|
| Java syntax, types, formatting, or Lombok | [Java language and Lombok](references/java-language-and-lombok.md) |
| Java method expression, access, or names | [Object and method style](references/object-and-method-style.md) |
| HTTP models, DTO conversion, or Jackson | [HTTP, DTO, and JSON](references/http-dto-and-json-style.md) |
| Pure business objects, validation, Optional, or authorization | [Domain and authorization](references/domain-and-authorization-style.md) |
| JPA Entity, Repository, QueryDSL, or SQL | [Persistence and queries](references/persistence-jpa-querydsl-and-sql.md) |
| Service, Spring Bean, transaction, provider, Scheduler, or Batch | [Spring boundaries and adapters](references/spring-boundaries-and-adapters.md) |
| Exception, logging, JavaDoc, configuration, or secret | [Errors, logging, and configuration](references/errors-logging-and-configuration.md) |
| Tests or code-change verification | [Testing and verification](references/testing-and-verification.md) |
| Public contract changes, refactoring, or review | [Compatibility and change scope](references/compatibility-and-change-scope.md) |
| A connected Java example | [Examples](references/examples.md) |

Any Java source change reads the language and object references. A change crossing DTO, persistence, and transaction code reads those references together.

## Rule Application

MUST and MUST NOT are requirements; SHOULD and SHOULD NOT are defaults; MAY is optional under its stated conditions. Existing external contracts can require a narrow, evidenced compatibility exception. Use the compatibility reference for that decision; do not infer a legacy migration or add a compatibility layer by default.

Review findings identify the rule or section and actual impact. Implementation reports identify the resulting behavior, focused verification, and material remaining gaps.
