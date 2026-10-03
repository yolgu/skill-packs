# Java Language, Formatting, and Lombok Rules

## Table of contents

- [Project Java baseline](#project-java-baseline)
- [Language features and explicit types](#language-features-and-explicit-types)
- [Time, money, character sets, and collections](#time-money-character-sets-and-collections)
- [Source formatting](#source-formatting)
- [Lombok](#lombok)

## Project Java baseline

<a id="java-001"></a>
### Use Java features supported by the project

**JAVA-001 · MUST**

Inspect Maven Compiler `release/source/target`, the Gradle Toolchain, Spring Boot version, CI runtime, and production runtime. Use only Java features supported by their intersection. JDK distributions such as Temurin and Corretto are operational choices; this rule does not mandate a specific distribution or Java-version upgrade.

<a id="java-002"></a>
### Keep the existing javax or jakarta namespace

**JAVA-002 · MUST NOT**

Follow the framework generation and existing module configuration for `jakarta.*` versus `javax.*`. Do not mix them arbitrarily within one module or begin a namespace migration solely as a code-style change.

<a id="java-005"></a>
### Use preview features only when explicitly supported

**JAVA-005 · MUST**

Use a preview feature only when the build, CI, and production runtime all enable and support it explicitly. Do not introduce one merely because it compiles locally.

## Language features and explicit types

<a id="java-003"></a>
### Use regular classes instead of records

**JAVA-003 · MUST NOT**

Do not use Java `record`, including for Request, Response, DTO, Command, Query, Result, Value Object, Event, QueryRow, or configuration types. Use regular classes to make construction, validation, and exposure contracts explicit. Do not mass-convert unrelated existing records.

<a id="java-004"></a>
### Avoid Java var and Lombok val or var

**JAVA-004 · MUST NOT**

Do not use Java `var`, Lombok `val`, or Lombok `var`.

<a id="java-006"></a>
### Declare local variable types explicitly

**JAVA-006 · MUST**

Declare an explicit type for every local variable. The diamond operator is permitted when the owning declaration states the type. Declare lambda parameter types where Java syntax permits them; a method reference can use the referenced method's declared signature.

```java
final Optional<Member> member = memberRepository.findById(memberId);
final List<MemberSummary> summaries = members.stream()
    .map(MemberSummary::from)
    .toList();
```

<a id="java-007"></a>
### Make immutability clear without requiring final everywhere

**JAVA-007 · SHOULD**

- Make injected dependencies and constants `final`.
- Make immutable DTO, Value Object, and Event fields `private final` when the construction mechanism permits it.
- Do not reassign method parameters, and keep local variables single-assignment where practical.
- Do not mechanically require the `final` keyword on every parameter and local variable. Use it where it materially clarifies immutability.
- Keep immutable contracts immutable. For JPA data representations, use the constructor and accessor rules in [Persistence](persistence-jpa-querydsl-and-sql.md); do not turn immutability into a blanket setter ban.

## Time, money, character sets, and collections

<a id="java-008"></a>
### Choose types that preserve meaning and precision

**JAVA-008 · MUST**

Use standard types that match the meaning and required precision.

- Use `LocalDate` for a calendar date, `Instant` for a global point in time, `OffsetDateTime` when an offset belongs to the contract, `ZonedDateTime` when regional time-zone rules matter, `Duration` for elapsed time, and `Period` for a calendar period.
- Isolate conversions to legacy `Date`, `Calendar`, and `Timestamp` types in infrastructure adapters.
- Do not use `float` or `double` for money or exact decimal calculations.
- Construct `BigDecimal` from a string or integer representation, and state scale and rounding for division. Compare numeric values with `compareTo()` or a meaningful Value Object method.
- Specify a character set such as `StandardCharsets.UTF_8` for string-to-byte conversions.
- Return an empty collection when a plural result has no elements. Use defensive copies such as `List.copyOf` and `Set.copyOf` when exposing immutable collections.
- Represent a stable finite state with an enum or another explicit type, but do not use `ordinal()` as a database or external code.
- Do not map an unknown external status code to an arbitrary default.
- Use try-with-resources for resources the code directly owns and must close. Do not close framework-managed resources arbitrarily.
- Do not implement `Serializable` by habit; use it only when an actual session, cache, or message contract requires it.

When currency, scale, or rounding rules repeat, make a Value Object such as `Money` their single source of truth.

## Source formatting

<a id="format-001"></a>
### Follow the project's formatting rules

**FORMAT-001 · MUST**

Apply formatting rules in this order:

1. Project formatter
2. Checkstyle and static analysis
3. `.editorconfig`
4. Consistent existing repository style
5. Defaults in this reference

When the project tooling and examples wrap lines differently, follow the project tooling.

<a id="format-002"></a>
### Use consistent defaults when formatting rules are absent

**FORMAT-002 · SHOULD**

Use these defaults when the project defines no corresponding rule:

- Four spaces; no tabs
- UTF-8 and LF; exactly one final newline; no trailing whitespace
- One statement per line
- One public top-level type per file
- A filename matching its public type
- A soft limit of 120 characters per line

The 120-character limit is not an absolute cutoff that justifies obscuring meaning.

<a id="format-003"></a>
### Use braces and explicit imports

**FORMAT-003 · MUST**

- Use braces for every control statement.
- Do not leave wildcard imports or unused imports.
- Do not repeat long fully qualified names throughout the code.
- Use static imports sparingly when they improve sentence-like readability, as with AssertJ or Mockito.
- Put class and method annotations on separate lines by default.

<a id="format-004"></a>
### Format code to reveal the business flow

**FORMAT-004 · SHOULD**

Keep short, clear statements on one line. When code becomes long, wrap types, calls, and arguments by business unit. Split a long chain into explicitly typed local variables when it hides the business sequence. Use blank lines to separate narrative stages such as input, lookup, authorization, domain behavior, persistence, and result construction.

When the project defines no class-member order, default to constants, static fields, instance fields, constructors, static factories, public methods, narrower methods, and private helpers. Keep related behavior together instead when that better preserves the narrative flow.

<a id="format-005"></a>
### Keep formatting changes within the task's scope

**FORMAT-005 · MUST**

- Do not reformat an unrelated entire file during a functional change.
- If the formatter changes a whole file, inspect the diff size and repository policy.
- Separate pure formatting changes from behavioral changes when practical.
- Do not format or modify generated code directly; change its source or generator configuration.

## Lombok

<a id="lombok-001"></a>
### Use Lombok only when already adopted

**LOMBOK-001 · MUST NOT**

Do not add Lombok as a dependency merely to apply these rules. Apply the allowances below only when the project already uses Lombok.

<a id="lombok-002"></a>
### Limit generated getters and constructors to clear contracts

**LOMBOK-002 · SHOULD**

Use @Getter for deliberate read contracts and @RequiredArgsConstructor for straightforward constructor injection or immutable transfer data. Simple JPA data objects may use @Getter and @Setter for their data-access role. These annotations do not authorize business methods or DTO conversion on an Entity.

Write an explicit constructor when qualifiers, lazy dependencies, same-type dependencies, field ordering, or construction-time validation need to be visible.

<a id="lombok-003"></a>
### Use Lombok where framework conventions justify it

**LOMBOK-003 · MAY**

- For framework requirements such as JPA, use a restricted no-argument constructor such as `@NoArgsConstructor(access = AccessLevel.PROTECTED)`.
- Use `@Slf4j` when the project already uses Lombok and SLF4J.
- Use `@AllArgsConstructor` sparingly for a simple transfer object with no business rules. Write an explicit constructor when field ordering is easy to confuse or validation is meaningful.

<a id="lombok-004"></a>
### Reserve builders for objects with many optional fields

**LOMBOK-004 · SHOULD NOT**

Limit builders to boundary objects with many optional fields, such as:

- Controller responses
- Application results
- RequestDto or Query objects with many optional conditions
- Provider request payloads
- Test fixtures

Do not use a builder as the default construction mechanism for a Domain Entity, Value Object, JPA Entity, Spring Bean, or an object with only two or three required values. When a builder is justified, consider limiting it to a specific construction path rather than the entire class. Do not use `toBuilder = true` or `@Builder.Default` to bypass domain state transitions or collection immutability.

<a id="lombok-005"></a>
### Avoid Lombok annotations that obscure object behavior

**LOMBOK-005 · MUST NOT**

Do not use:

- `@Data`
- `@SneakyThrows`
- `@Accessors(chain = true)`
- `@UtilityClass`, `@Value`, `@SuperBuilder`, `@With`, `@Delegate`, `@ExtensionMethod`, or `@FieldDefaults` as defaults

If a project already standardizes `@Value` for safe internal value types, allow only a narrow exception after checking the type's construction, equality, and `toString` semantics.

<a id="lombok-006"></a>
### Generate equality and toString only for safe value types

**LOMBOK-006 · MUST**

- Use `@EqualsAndHashCode` only on a Value Object with clear value equality and immutable fields.
- Do not use automatic equality on a JPA Entity, Aggregate, lazy-loaded relationship, or object containing mutable fields.
- Use `@ToString` only on a small value object that is safe to expose in logs.
- Do not generate automatic `toString` for an entire Request, JPA Entity, bidirectional relationship, or a type containing secrets, tokens, personal data, large collections, or binary data.
