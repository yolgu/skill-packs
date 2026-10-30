---
name: java-backend-code-style
description: Write, modify, refactor, or review Java backend implementation on top of code-principles, using explicit Java types, role-based names, DTO construction and conversion, storage-only JPA entities, Spring Data, QueryDSL, SQL, MyBatis mappers, Spring transactions, message consumers and after-commit listeners, and the Java forms of the feature implementation flow including the end-to-end test base. Use for concrete Java and framework decisions, not for selecting an overall directory architecture.
---

# Java Backend Code Style

## Scope

Own the concrete Java and Spring forms of the rules; code-principles is the base layer underneath this skill and owns the language-agnostic principles and the feature implementation flow, so load it alongside and do not restate it here. Preserve explicit project contracts and the authorized change scope. Existing code patterns are evidence, not automatic exceptions to these rules.

Inspect the module's Java/toolchain version, build and formatter settings, package declarations, annotation processors, public signatures, and relevant tests. Apply framework rules only when that technology is actually used.

## Select References

Read only the references relevant to the work, in full.

| Work | Reference |
|---|---|
| Java syntax, types, formatting, or Lombok | [Java language and Lombok](references/java-language-and-lombok.md) |
| Java method expression, access, or names | [Object and method style](references/object-and-method-style.md) |
| HTTP models, DTO conversion, or Jackson | [HTTP, DTO, and JSON](references/http-dto-and-json-style.md) |
| Pure business objects, validation, Optional, or authorization | [Domain and authorization](references/domain-and-authorization-style.md) |
| JPA Entity, Repository, QueryDSL, SQL, or MyBatis mapper | [Persistence and queries](references/persistence-jpa-querydsl-and-sql.md) |
| Service, Spring Bean, transaction, provider, Scheduler, Batch, message consumer (Kafka, RabbitMQ), or after-commit event listener | [Spring boundaries and adapters](references/spring-boundaries-and-adapters.md) |
| Exception, logging, JavaDoc, configuration, or secret | [Errors, logging, and configuration](references/errors-logging-and-configuration.md) |
| Tests, web slice tests, test doubles and contract tests, `*Test` and `*IT` names, the end-to-end test base, entry-point outer-loop tests, failure-path tests, or code-change verification | [Testing and verification](references/testing-and-verification.md) |
| Public contract changes, refactoring, or review | [Compatibility and change scope](references/compatibility-and-change-scope.md) |
| A connected Java example | [Examples](references/examples.md) |

Any Java source change reads the language and object references. A change crossing DTO, persistence, and transaction code reads those references together.

## Rule Application

MUST and MUST NOT are requirements; SHOULD and SHOULD NOT are defaults; MAY is optional under its stated conditions. Existing external contracts can require a narrow, evidenced compatibility exception. Use the compatibility reference for that decision; do not infer a legacy migration or add a compatibility layer by default.

Review findings state the problem and its actual impact first, and cite the violated rule by its title as supporting evidence. Implementation reports identify the resulting behavior, focused verification, and material remaining gaps.
