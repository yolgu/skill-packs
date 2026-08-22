# HTTP, DTO, and JSON Rules

## Table of contents

- [Boundary models](#boundary-models)
- [Conversions](#conversions)
- [Controller](#controller)
- [JSON contracts](#json-contracts)
- [Compatibility checks](#compatibility-checks)

## Boundary models

### DTO-001 — MUST

Represent HTTP input as `...Request` and output as `...Response`; do not share one type in both directions. The two contracts differ in validation, exposed fields, security, and change cadence. Do not share provider DTOs with local HTTP DTOs.

### DTO-002 — MUST

Use this flow by default for a new application boundary:

```text
ExportMembersRequest
→ ExportMembersCommand
→ ExportMembersUseCase
→ ExportMembersResult
→ ExportMembersResponse
```

If the existing project consistently uses `RequestDto/ResultDto`, retain that convention. Do not mix `Command/Result` and `RequestDto/ResultDto` arbitrarily within one application boundary. Distinguish state-changing intent as a Command and lookup criteria as a Query.

### DTO-003 — SHOULD NOT

Do not mechanically duplicate identical-field types to match the number of layers. Separate boundary types when at least one of the following materially differs:

- External and internal contracts
- Validation responsibilities
- Exposed fields and personal-data boundaries
- Business meaning
- Change cadence

For simple transfer within one layer, an existing explicit type may be reused. Separation among ORM, provider, and HTTP contracts remains valuable even when their fields happen to match.

### DTO-006 — SHOULD

Use a regular class with immutable constructor binding as the default for a new HTTP Request. Verify whether the project's ObjectMapper and compiler reliably discover constructor parameter names; declare `@JsonCreator` and `@JsonProperty` only when required.

```java
@Getter
public class ExportMembersRequest {

    @NotBlank
    private final String cityCode;

    @JsonCreator
    public ExportMembersRequest(
        @JsonProperty("cityCode") final String cityCode
    ) {
        this.cityCode = cityCode;
    }

    public ExportMembersCommand toCommand() {
        return ExportMembersCommand.of(cityCode);
    }
}
```

When existing field binding depends on private mutable fields and a restricted no-argument constructor, do not add public setters. Verify the narrow compatibility exception with an actual MockMvc or ObjectMapper deserialization test. Permit `@Jacksonized @Builder` only when the project already uses it consistently and verifies the real binding behavior.

## Conversions

### DTO-004 — MUST

Keep conversion and construction naming semantics fixed.

- `toXxx()`: convert the current object to a specified target type
- `from(source)`: construct from one primary source
- `of(values...)`: combine prepared values
- `create/issue/register`: apply new business-object rules
- `restore`: reconstruct persisted state

Use `toDto()` only when there is one contextually unambiguous target. When multiple targets exist, use a specific name such as `toExportCommand()`.

### DTO-005 — SHOULD

Use explicit manual field mapping by default for a small conversion. Use MapStruct only when the project already adopts it, fields are numerous, mechanical mappings repeat, and the build can detect omissions.

Do not put the following in a mapper:

- Authorization decisions
- Domain state transitions
- Repository lookups
- Provider calls
- Current-time or identifier generation
- Business default decisions

Do not use reflection-based bean copying or a global `CommonMapper`.

## Controller

### CONTROLLER-001 — MUST

Limit a Controller to this flow:

1. Declare the URL and HTTP method
2. Deserialize the Request and validate boundary syntax
3. Resolve the authenticated actor and work context
4. Convert to application input
5. Invoke the Use Case
6. Convert the application result to a Response

Do not put Repository access, JPA Entity manipulation, QueryDSL, SQL, transaction control, business authorization conditions, domain state transitions, provider SDK calls, or JSON Map assembly in a Controller. Do not translate business exceptions to HTTP errors with per-controller `try/catch`; use the appropriate Handler.

### CONTROLLER-002 — MUST NOT

Do not pass `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, or Spring `Authentication` into the Application or Domain. Convert only the required actor, organization, city, language, request channel, and correlation data to an explicit Context type.

### CONTROLLER-003 — SHOULD

Return a Response DTO directly when the successful status and body are fixed. Use `ResponseEntity` when actual HTTP control is required, such as:

- A dynamic status or creation `Location`
- Headers, ETag, or Last-Modified
- File download, redirect, or partial content
- A response with no body

If the project consistently uses `ResponseEntity` for every Controller, preserve that established convention.

### CONTROLLER-004 — MUST NOT

Do not return any of the following directly as a Controller Response:

- A JPA Entity or Domain Entity
- A QueryDSL projection or native QueryRow
- A provider Response or SDK object
- Spring Data `Page`
- Another business area's internal DTO

Define a Response containing only fields allowed for the external consumer.

### CONTROLLER-005 — MUST

Use Controller security annotations only for technical boundaries such as authenticated access. Do not encode role codes, specific account identifiers, city, language, ownership, or target-state conditions in SpEL or a custom annotation DSL. The Application Use Case must enforce actual business authorization by invoking a domain-specific authorization policy.

## JSON contracts

### JSON-001 — MUST

For an existing API, trace actual JSON, Controller contract tests, OpenAPI, client usage, the global ObjectMapper, and custom serializers together to identify the contract's single source of truth. When documentation and runtime behavior differ, first verify the observable runtime contract and its consumers.

### JSON-002 — MUST

Do not change the following solely as a code-style modification:

- JSON field names and types
- `null`, empty strings, empty collections, and omitted fields
- Boolean representations such as Y/N, 1/0, or strings
- Date formats and time zones
- External enum codes
- Large-integer and `BigDecimal` precision
- Error bodies and HTTP statuses

When an external name is fixed, preserve it with `@JsonProperty` even if the Java name improves, and verify it with a contract test. Do not bind an external contract implicitly to an enum's `name()` or `ordinal()`.

### JSON-003 — SHOULD

Use `@JsonInclude`, `@JsonIgnoreProperties`, `@JsonProperty`, and custom serializers or deserializers only when they express real contract semantics. Do not apply `NON_NULL` to every Response or `ignoreUnknown = true` to every Request. Assign clear ownership of date format and time zone to global configuration, a specific field, or a serializer.

### JSON-004 — MUST NOT

Do not create `new ObjectMapper()` in each class. Use the project-configured mapper. When a provider has a different contract, its adapter may own dedicated configuration. Do not impose a universal response wrapper or remove an existing wrapper solely for style.

### JSON-005 — MUST NOT

Do not serialize JPA or Domain Entities directly and then force the API contract to fit through `@JsonIgnore`, lazy-loading modules, or cyclic-reference annotations. Create a Response that contains only allowed fields from the beginning. Do not perform Repository lookup, authorization, external calls, or state changes inside a serializer.

### JSON-006 — MUST

Do not use Jackson Default Typing or open polymorphic deserialization based on internal implementation class names. When a real polymorphic contract exists, declare the permitted discriminator and type set explicitly, and verify unknown-type handling with contract tests.

## Compatibility checks

When an HTTP boundary changes, compare the URL, method, Request and Response fields, JSON types, null semantics, status codes, error responses, headers, session, cookies, redirects, sorting, pagination, and file results. Distinguish an ideal design for a new API from the actual compatibility contract of an existing API.
