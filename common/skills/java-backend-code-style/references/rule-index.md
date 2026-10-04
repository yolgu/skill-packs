# Java Rule Index

Navigation only. Definitions and strengths are recorded once in the linked rule sections.
Select the relevant topic; the examples illustrate those rules and do not define additional requirements.

## Java Language, Formatting, and Lombok Rules

| ID | Rule section |
|---|---|
| JAVA-001 | [Use Java features supported by the project](java-language-and-lombok.md#java-001) |
| JAVA-002 | [Keep the existing javax or jakarta namespace](java-language-and-lombok.md#java-002) |
| JAVA-005 | [Use preview features only when explicitly supported](java-language-and-lombok.md#java-005) |
| JAVA-003 | [Use regular classes instead of records](java-language-and-lombok.md#java-003) |
| JAVA-004 | [Avoid Java var and Lombok val or var](java-language-and-lombok.md#java-004) |
| JAVA-006 | [Declare local variable types explicitly](java-language-and-lombok.md#java-006) |
| JAVA-007 | [Make immutability clear without requiring final everywhere](java-language-and-lombok.md#java-007) |
| JAVA-008 | [Choose types that preserve meaning and precision](java-language-and-lombok.md#java-008) |
| FORMAT-001 | [Follow the project's formatting rules](java-language-and-lombok.md#format-001) |
| FORMAT-002 | [Use consistent defaults when formatting rules are absent](java-language-and-lombok.md#format-002) |
| FORMAT-003 | [Use braces and explicit imports](java-language-and-lombok.md#format-003) |
| FORMAT-004 | [Format code to reveal the business flow](java-language-and-lombok.md#format-004) |
| FORMAT-005 | [Keep formatting changes within the task's scope](java-language-and-lombok.md#format-005) |
| LOMBOK-001 | [Use Lombok only when already adopted](java-language-and-lombok.md#lombok-001) |
| LOMBOK-002 | [Limit generated getters and constructors to clear contracts](java-language-and-lombok.md#lombok-002) |
| LOMBOK-003 | [Use Lombok where framework conventions justify it](java-language-and-lombok.md#lombok-003) |
| LOMBOK-004 | [Reserve builders for objects with many optional fields](java-language-and-lombok.md#lombok-004) |
| LOMBOK-005 | [Avoid Lombok annotations that obscure object behavior](java-language-and-lombok.md#lombok-005) |
| LOMBOK-006 | [Generate equality and toString only for safe value types](java-language-and-lombok.md#lombok-006) |

## Java Methods, Access, and Names

| ID | Rule section |
|---|---|
| OBJECT-005 | [Choose streams or loops for readability](object-and-method-style.md#object-005) |
| OBJECT-007 | [Use explicit Java contract types](object-and-method-style.md#object-007) |
| OBJECT-008 | [Use Java access levels deliberately](object-and-method-style.md#object-008) |
| NAMING-001 | [Use English business identifiers](object-and-method-style.md#naming-001) |
| NAMING-002 | [Name Java implementation roles](object-and-method-style.md#naming-002) |
| NAMING-003 | [Name implementations without breaking framework discovery](object-and-method-style.md#naming-003) |
| NAMING-004 | [Match Java method names to return and failure behavior](object-and-method-style.md#naming-004) |
| NAMING-005 | [Name Boolean values, collections, and acronyms](object-and-method-style.md#naming-005) |

## HTTP, DTO, and JSON Rules

| ID | Rule section |
|---|---|
| DTO-001 | [Separate HTTP request and response types](http-dto-and-json-style.md#dto-001) |
| DTO-002 | [Use consistent application input and result types](http-dto-and-json-style.md#dto-002) |
| DTO-003 | [Separate DTOs when their contracts differ](http-dto-and-json-style.md#dto-003) |
| DTO-006 | [Prefer immutable constructor binding for HTTP requests](http-dto-and-json-style.md#dto-006) |
| DTO-004 | [Distinguish conversion from object construction](http-dto-and-json-style.md#dto-004) |
| DTO-005 | [Keep mappings explicit and free of business decisions](http-dto-and-json-style.md#dto-005) |
| CONTROLLER-001 | [Keep controllers focused on HTTP and use case invocation](http-dto-and-json-style.md#controller-001) |
| CONTROLLER-002 | [Convert framework context before entering inner layers](http-dto-and-json-style.md#controller-002) |
| CONTROLLER-003 | [Use ResponseEntity when HTTP control is needed](http-dto-and-json-style.md#controller-003) |
| CONTROLLER-004 | [Return only dedicated API response types](http-dto-and-json-style.md#controller-004) |
| CONTROLLER-005 | [Enforce business authorization in the use case](http-dto-and-json-style.md#controller-005) |
| JSON-001 | [Identify the actual JSON contract](http-dto-and-json-style.md#json-001) |
| JSON-002 | [Preserve existing JSON and HTTP behavior](http-dto-and-json-style.md#json-002) |
| JSON-003 | [Use Jackson annotations for real contract differences](http-dto-and-json-style.md#json-003) |
| JSON-004 | [Reuse configured mappers and existing response conventions](http-dto-and-json-style.md#json-004) |
| JSON-005 | [Keep entity serialization out of API contracts](http-dto-and-json-style.md#json-005) |
| JSON-006 | [Restrict polymorphic deserialization to permitted types](http-dto-and-json-style.md#json-006) |

## Domain, Validation, and Authorization Rules

| ID | Rule section |
|---|---|
| DOMAIN-001 | [Express business behavior in plain Java objects](domain-and-authorization-style.md#domain-001) |
| DOMAIN-002 | [Distinguish new construction from restoration](domain-and-authorization-style.md#domain-002) |
| DOMAIN-003 | [Use value objects for meaningful domain values](domain-and-authorization-style.md#domain-003) |
| DOMAIN-005 | [Keep a separated domain independent of frameworks](domain-and-authorization-style.md#domain-005) |
| DOMAIN-006 | [Pass time and identifiers into the domain](domain-and-authorization-style.md#domain-006) |
| DOMAIN-004 | [Keep domain services focused on pure business decisions](domain-and-authorization-style.md#domain-004) |
| DOMAIN-007 | [Use domain events for completed business facts](domain-and-authorization-style.md#domain-007) |
| VALIDATION-001 | [Validate each concern at its owning layer](domain-and-authorization-style.md#validation-001) |
| VALIDATION-002 | [Keep business constraints under domain ownership](domain-and-authorization-style.md#validation-002) |
| VALIDATION-003 | [Keep external lookups out of Bean Validators](domain-and-authorization-style.md#validation-003) |
| VALIDATION-004 | [Give normalization one owner](domain-and-authorization-style.md#validation-004) |
| OPTIONAL-001 | [Use Optional for a single result that may be absent](domain-and-authorization-style.md#optional-001) |
| OPTIONAL-002 | [Keep Optional out of fields and parameters](domain-and-authorization-style.md#optional-002) |
| OPTIONAL-003 | [Return empty collections and choose fallbacks carefully](domain-and-authorization-style.md#optional-003) |
| AUTH-001 | [Distinguish roles, actions, attributes, and policies](domain-and-authorization-style.md#auth-001) |
| AUTH-002 | [Authorize business actions rather than role codes](domain-and-authorization-style.md#auth-002) |
| AUTH-003 | [Give each business area its own authorization policy](domain-and-authorization-style.md#auth-003) |
| AUTH-004 | [Keep required authorization compatibility local](domain-and-authorization-style.md#auth-004) |
| AUTH-005 | [Introduce authorization abstractions only for real repetition](domain-and-authorization-style.md#auth-005) |
| AUTH-006 | [Translate authorized scopes into query conditions](domain-and-authorization-style.md#auth-006) |
| AUTH-007 | [Enforce authorization before protected actions](domain-and-authorization-style.md#auth-007) |
| AUTH-008 | [Deny unknown permissions and empty scopes](domain-and-authorization-style.md#auth-008) |
| AUTH-009 | [Use backend authorization as the security authority](domain-and-authorization-style.md#auth-009) |

## JPA, QueryDSL, and SQL Rules

| ID | Rule section |
|---|---|
| JPA-001 | [Keep business behavior separate from JPA storage](persistence-jpa-querydsl-and-sql.md#jpa-001) |
| JPA-002 | [Keep the public repository contract independent of JPA](persistence-jpa-querydsl-and-sql.md#jpa-002) |
| JPA-003 | [Use ordinary JPA data construction and access](persistence-jpa-querydsl-and-sql.md#jpa-003) |
| JPA-004 | [Avoid generated behavior that weakens JPA entities](persistence-jpa-querydsl-and-sql.md#jpa-004) |
| JPA-005 | [Model required relationships with explicit lazy loading](persistence-jpa-querydsl-and-sql.md#jpa-005) |
| JPA-006 | [Use cascading only for owned lifecycles](persistence-jpa-querydsl-and-sql.md#jpa-006) |
| JPA-007 | [Keep persistence relationships consistent inside the implementation](persistence-jpa-querydsl-and-sql.md#jpa-007) |
| JPA-008 | [Define entity equality only for a real need](persistence-jpa-querydsl-and-sql.md#jpa-008) |
| QUERY-001 | [Keep repositories focused on persistence](persistence-jpa-querydsl-and-sql.md#query-001) |
| QUERY-002 | [Separate complex reads when responsibilities differ](persistence-jpa-querydsl-and-sql.md#query-002) |
| QUERY-003 | [Choose the simplest suitable query tool](persistence-jpa-querydsl-and-sql.md#query-003) |
| QUERY-004 | [Prefer composition for QueryDSL repositories](persistence-jpa-querydsl-and-sql.md#query-004) |
| QUERY-005 | [Make bulk update behavior and bypassed rules explicit](persistence-jpa-querydsl-and-sql.md#query-005) |
| QUERY-006 | [Limit nullable predicates to simple optional filters](persistence-jpa-querydsl-and-sql.md#query-006) |
| QUERY-007 | [Compose authorization scopes and complex conditions explicitly](persistence-jpa-querydsl-and-sql.md#query-007) |
| QUERY-008 | [Keep QueryDSL types inside infrastructure](persistence-jpa-querydsl-and-sql.md#query-008) |
| QUERY-009 | [Use explicit query results and stable pagination](persistence-jpa-querydsl-and-sql.md#query-009) |
| SQL-001 | [Keep complex SQL near its owning business code](persistence-jpa-querydsl-and-sql.md#sql-001) |
| SQL-002 | [Make SQL inputs and results explicit](persistence-jpa-querydsl-and-sql.md#sql-002) |
| SQL-003 | [Document complex SQL contracts and ownership](persistence-jpa-querydsl-and-sql.md#sql-003) |
| SQL-004 | [Respect each business area's table ownership](persistence-jpa-querydsl-and-sql.md#sql-004) |
| SQL-005 | [Verify database-specific queries on the supported database](persistence-jpa-querydsl-and-sql.md#sql-005) |

## Spring Boundary, Use Case, Adapter, Scheduler, and Batch Rules

| ID | Rule section |
|---|---|
| USECASE-001 | [Expose a Use Case interface when its contract needs separation](spring-boundaries-and-adapters.md#usecase-001) |
| USECASE-002 | [Implement the application flow through public contracts](spring-boundaries-and-adapters.md#usecase-002) |
| USECASE-003 | [Keep Spring components direct](spring-boundaries-and-adapters.md#usecase-003) |
| USECASE-004 | [Inject dependencies through constructors](spring-boundaries-and-adapters.md#usecase-004) |
| TRANSACTION-001 | [Let the application use case own the transaction](spring-boundaries-and-adapters.md#transaction-001) |
| TRANSACTION-002 | [Use read-only transactions only for read-only work](spring-boundaries-and-adapters.md#transaction-002) |
| TRANSACTION-003 | [Keep business transactions at the application layer](spring-boundaries-and-adapters.md#transaction-003) |
| TRANSACTION-004 | [Avoid holding database locks during slow external calls](spring-boundaries-and-adapters.md#transaction-004) |
| TRANSACTION-005 | [Verify independent commits and partial failure behavior](spring-boundaries-and-adapters.md#transaction-005) |
| TRANSACTION-006 | [Account for Spring proxy transaction boundaries](spring-boundaries-and-adapters.md#transaction-006) |
| EXTERNAL-001 | [Implement provider-independent Java contracts](spring-boundaries-and-adapters.md#external-001) |
| EXTERNAL-002 | [Keep provider types inside adapters](spring-boundaries-and-adapters.md#external-002) |
| EXTERNAL-003 | [Translate provider results into accurate business outcomes](spring-boundaries-and-adapters.md#external-003) |
| EXTERNAL-004 | [Translate provider errors while preserving their causes](spring-boundaries-and-adapters.md#external-004) |
| EXTERNAL-005 | [Set network timeouts explicitly](spring-boundaries-and-adapters.md#external-005) |
| EXTERNAL-006 | [Retry only when failure and duplication semantics permit it](spring-boundaries-and-adapters.md#external-006) |
| EXTERNAL-007 | [Expose external failures and approved fallback states](spring-boundaries-and-adapters.md#external-007) |
| SCHEDULER-001 | [Keep schedulers focused on invoking use cases](spring-boundaries-and-adapters.md#scheduler-001) |
| SCHEDULER-002 | [Configure schedules and establish one execution time](spring-boundaries-and-adapters.md#scheduler-002) |
| SCHEDULER-003 | [Define behavior for duplicate execution](spring-boundaries-and-adapters.md#scheduler-003) |
| BATCH-001 | [Separate Spring Batch responsibilities](spring-boundaries-and-adapters.md#batch-001) |
| BATCH-002 | [Process large datasets in manageable units](spring-boundaries-and-adapters.md#batch-002) |
| BATCH-003 | [Use stable job names and explicit execution parameters](spring-boundaries-and-adapters.md#batch-003) |
| BATCH-004 | [Define retry, skip, restart, and partial failure behavior](spring-boundaries-and-adapters.md#batch-004) |

## Exception, Logging, Configuration, and Documentation Rules

| ID | Rule section |
|---|---|
| EXCEPTION-001 | [Represent failures according to their owning layer](errors-logging-and-configuration.md#exception-001) |
| EXCEPTION-002 | [Choose exception types according to recovery needs](errors-logging-and-configuration.md#exception-002) |
| EXCEPTION-003 | [Keep external contracts out of domain exceptions](errors-logging-and-configuration.md#exception-003) |
| EXCEPTION-004 | [Name exceptions after concrete business failures](errors-logging-and-configuration.md#exception-004) |
| EXCEPTION-006 | [Handle failures meaningfully and preserve their causes](errors-logging-and-configuration.md#exception-006) |
| EXCEPTION-007 | [Limit broad catches to process boundaries](errors-logging-and-configuration.md#exception-007) |
| EXCEPTION-008 | [Expose stable error codes rather than internal messages](errors-logging-and-configuration.md#exception-008) |
| EXCEPTION-005 | [Translate business exceptions for each HTTP API](errors-logging-and-configuration.md#exception-005) |
| LOGGING-001 | [Use the established logger and parameterized messages](errors-logging-and-configuration.md#logging-001) |
| LOGGING-002 | [Choose log levels by operational value](errors-logging-and-configuration.md#logging-002) |
| LOGGING-003 | [Log each failure at one meaningful point](errors-logging-and-configuration.md#logging-003) |
| LOGGING-004 | [Preserve stack traces when logging exceptions](errors-logging-and-configuration.md#logging-004) |
| LOGGING-005 | [Keep logging frameworks out of a pure domain](errors-logging-and-configuration.md#logging-005) |
| LOGGING-006 | [Protect secrets and personal data in logs](errors-logging-and-configuration.md#logging-006) |
| LOGGING-007 | [Propagate correlation identifiers consistently](errors-logging-and-configuration.md#logging-007) |
| COMMENT-001 | [Use consistent identifier and documentation languages](errors-logging-and-configuration.md#comment-001) |
| COMMENT-002 | [Explain reasons and constraints in comments](errors-logging-and-configuration.md#comment-002) |
| COMMENT-003 | [Document public contracts when names and types are insufficient](errors-logging-and-configuration.md#comment-003) |
| COMMENT-004 | [Remove stale code and make TODOs actionable](errors-logging-and-configuration.md#comment-004) |
| CONFIG-001 | [Group related settings in immutable configuration types](errors-logging-and-configuration.md#config-001) |
| CONFIG-002 | [Validate required configuration at startup](errors-logging-and-configuration.md#config-002) |
| CONFIG-003 | [Keep configuration focused on technical wiring](errors-logging-and-configuration.md#config-003) |
| CONFIG-004 | [Declare dependencies instead of locating them globally](errors-logging-and-configuration.md#config-004) |
| CONFIG-005 | [Select implementations at the configuration boundary](errors-logging-and-configuration.md#config-005) |
| CONFIG-006 | [Avoid dangerous defaults and secret exposure](errors-logging-and-configuration.md#config-006) |
| CONFIG-007 | [Separate environment settings from business rules](errors-logging-and-configuration.md#config-007) |

## Testing and Verification Rules

| ID | Rule section |
|---|---|
| TEST-001 | [Follow existing testing tools and conventions](testing-and-verification.md#test-001) |
| TEST-002 | [Test observable business behavior](testing-and-verification.md#test-002) |
| TEST-005 | [Verify interactions when side effects are the contract](testing-and-verification.md#test-005) |
| TEST-008 | [Prioritize important behavior over coverage numbers](testing-and-verification.md#test-008) |
| TEST-003 | [Test each responsibility at its owning layer](testing-and-verification.md#test-003) |
| TEST-004 | [Use real domain objects and mock actual boundaries](testing-and-verification.md#test-004) |
| TEST-006 | [Keep test fixtures from weakening production encapsulation](testing-and-verification.md#test-006) |
| TEST-007 | [Make tests deterministic and independent](testing-and-verification.md#test-007) |
| TEST-009 | [Use compatibility comparisons when replacing a system](testing-and-verification.md#test-009) |
| TOOLING-001 | [Inspect the module's build and verification setup](testing-and-verification.md#tooling-001) |
| TOOLING-002 | [Use project wrappers and established verification commands](testing-and-verification.md#tooling-002) |
| TOOLING-003 | [Add verification tools only when requested](testing-and-verification.md#tooling-003) |
| TOOLING-004 | [Check search results in their code context](testing-and-verification.md#tooling-004) |
| TOOLING-005 | [Choose focused Java verification by risk](testing-and-verification.md#tooling-005) |
| TOOLING-006 | [Keep suppressions narrow and justified](testing-and-verification.md#tooling-006) |
| TOOLING-007 | [Change generator inputs instead of generated code](testing-and-verification.md#tooling-007) |

## Compatibility and Change-Scope Rules

| ID | Rule section |
|---|---|
| COMPATIBILITY-001 | [Resolve Java rule conflicts from explicit contracts](compatibility-and-change-scope.md#compatibility-001) |
| COMPATIBILITY-002 | [Preserve public and operational contracts](compatibility-and-change-scope.md#compatibility-002) |
| COMPATIBILITY-004 | [Address security and data-loss risks explicitly](compatibility-and-change-scope.md#compatibility-004) |
| COMPATIBILITY-003 | [Keep compatibility exceptions narrow and traceable](compatibility-and-change-scope.md#compatibility-003) |
| COMPATIBILITY-005 | [Limit refactoring to the requested work](compatibility-and-change-scope.md#compatibility-005) |
| COMPATIBILITY-006 | [Avoid unrelated cleanup and unrequested features](compatibility-and-change-scope.md#compatibility-006) |
| COMPATIBILITY-007 | [Keep reviews read-only unless changes are authorized](compatibility-and-change-scope.md#compatibility-007) |
| COMPATIBILITY-008 | [Report outcomes, verification, and remaining gaps](compatibility-and-change-scope.md#compatibility-008) |
