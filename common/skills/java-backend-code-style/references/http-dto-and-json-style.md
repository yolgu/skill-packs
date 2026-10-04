# HTTP, DTO, and JSON Rules

## Table of contents

- [Boundary models](#boundary-models)
- [Conversions](#conversions)
- [Controller](#controller)
- [JSON contracts](#json-contracts)
- [Compatibility checks](#compatibility-checks)

## Boundary models

<a id="dto-001"></a>
### Separate HTTP request and response types

**DTO-001 · MUST**

Represent HTTP input as `...Request` and output as `...Response`; do not share one type in both directions. The two contracts differ in validation, exposed fields, security, and change cadence. Do not share provider DTOs with local HTTP DTOs.

<a id="dto-002"></a>
### Use consistent application input and result types

**DTO-002 · MUST**

Use ...Request and ...Response for HTTP input and output. Use ...RequestDto and ...ResultDto for new service and public repository inputs and outputs:

~~~text
ExportMembersRequest.toDto()
→ ExportMembersRequestDto
→ ExportMembersService
→ ExportMembersResultDto
→ ExportMembersResponse.from(result)
~~~

Name models for the operation or data they describe. A collection result and a repository row result can have different business prefixes. Keep existing external Java signatures compatible when required; do not mix Command/Query/Result and RequestDto/ResultDto arbitrarily within the same new boundary.

Business values and provider wire models retain names that describe their own meaning.

<a id="dto-003"></a>
### Separate DTOs when their contracts differ

**DTO-003 · SHOULD NOT**

Do not mechanically duplicate identical-field types to match the number of layers. Separate boundary types when at least one of the following materially differs:

- Public contract ownership and consumers
- External and internal contracts
- Validation responsibilities
- Exposed fields and personal-data boundaries
- Business meaning
- Change cadence

Each layer owns its public input and output contracts. Equal fields do not erase different ownership or consumers. Reuse an existing explicit type for internal calls that do not introduce a new contract. Keep ORM, provider, and HTTP representations distinct.

<a id="dto-006"></a>
### Prefer immutable constructor binding for HTTP requests

**DTO-006 · SHOULD**

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

    public ExportMembersRequestDto toDto() {
        return ExportMembersRequestDto.of(cityCode);
    }
}
```

When existing field binding depends on private mutable fields and a restricted no-argument constructor, do not add public setters. Verify the narrow compatibility exception with an actual MockMvc or ObjectMapper deserialization test. Permit `@Jacksonized @Builder` only when the project already uses it consistently and verifies the real binding behavior.

## Conversions

<a id="dto-004"></a>
### Distinguish conversion from object construction

**DTO-004 · MUST**

- of(values...): create an object from prepared values.
- from(source): translate a different representation into this type.
- toDto(): translate this object to one contextually unambiguous DTO.
- toXxx(): name the target explicitly when more than one conversion is possible.
- create, issue, register: express new business-object creation when it has that meaning.
- restore: reconstruct business state when that operation differs from new creation.

Choose of and from by meaning, not argument count. A one-value of is valid. A static factory's source parameter still creates a type dependency.

<a id="dto-005"></a>
### Keep mappings explicit and free of business decisions

**DTO-005 · SHOULD**

Use direct field mapping, constructors, or short conversion methods for small models. Extract a Mapper only when conversion has a distinct responsibility or real duplication. Use MapStruct for substantial repeated mechanical mappings when already supported by the project and the build reports unmapped fields.

| Conversion | Java owner |
|---|---|
| HTTP request to service input | Request.toDto() |
| Service result to HTTP response | Response.from(serviceResult) |
| Repository result to service result | service ResultDto.from(repositoryResult) |
| JPA Entity to or from repository data | repository implementation |
| Provider response to integration result | provider implementation |

A public repository DTO must not declare from(JpaEntity). The implementation reads Entity fields and constructs the DTO from values. A JPA Entity must not interpret a DTO in update(dto), from(dto), or a similar method.

Keep authorization, business state transitions, repository lookups, provider calls, clock/identifier generation, and business defaults out of conversion code. Do not use reflection-based bean copying or a global CommonMapper.

## Controller

<a id="controller-001"></a>
### Keep controllers focused on HTTP and use case invocation

**CONTROLLER-001 · MUST**

Limit a Controller to this flow:

1. Declare the URL and HTTP method
2. Deserialize the Request and validate boundary syntax
3. Resolve the authenticated actor and work context
4. Convert to application input
5. Invoke the Use Case
6. Convert the application result to a Response

Do not put Repository access, JPA Entity manipulation, QueryDSL, SQL, transaction control, business authorization conditions, domain state transitions, provider SDK calls, or JSON Map assembly in a Controller. Do not translate business exceptions to HTTP errors with per-controller `try/catch`; use the appropriate Handler.

<a id="controller-002"></a>
### Convert framework context before entering inner layers

**CONTROLLER-002 · MUST NOT**

Do not pass `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, or Spring `Authentication` into the Application or Domain. Convert only the required actor, organization, city, language, request channel, and correlation data to an explicit Context type.

<a id="controller-003"></a>
### Use ResponseEntity when HTTP control is needed

**CONTROLLER-003 · SHOULD**

Return a Response DTO directly when the successful status and body are fixed. Use `ResponseEntity` when actual HTTP control is required, such as:

- A dynamic status or creation `Location`
- Headers, ETag, or Last-Modified
- File download, redirect, or partial content
- A response with no body

If the project consistently uses `ResponseEntity` for every Controller, preserve that established convention.

<a id="controller-004"></a>
### Return only dedicated API response types

**CONTROLLER-004 · MUST NOT**

Do not return any of the following directly as a Controller Response:

- A JPA Entity or Domain Entity
- A QueryDSL projection or native QueryRow
- A provider Response or SDK object
- Spring Data `Page`
- Another business area's internal DTO

Define a Response containing only fields allowed for the external consumer.

<a id="controller-005"></a>
### Enforce business authorization in the use case

**CONTROLLER-005 · MUST**

Use Controller security annotations only for technical boundaries such as authenticated access. Do not encode role codes, specific account identifiers, city, language, ownership, or target-state conditions in SpEL or a custom annotation DSL. The Application Use Case must enforce actual business authorization by invoking a domain-specific authorization policy.

## JSON contracts

<a id="json-001"></a>
### Identify the actual JSON contract

**JSON-001 · MUST**

For an existing API, trace actual JSON, Controller contract tests, OpenAPI, client usage, the global ObjectMapper, and custom serializers together to identify the contract's single source of truth. When documentation and runtime behavior differ, first verify the observable runtime contract and its consumers.

<a id="json-002"></a>
### Preserve existing JSON and HTTP behavior

**JSON-002 · MUST**

Do not change the following solely as a code-style modification:

- JSON field names and types
- `null`, empty strings, empty collections, and omitted fields
- Boolean representations such as Y/N, 1/0, or strings
- Date formats and time zones
- External enum codes
- Large-integer and `BigDecimal` precision
- Error bodies and HTTP statuses

When an external name is fixed, preserve it with `@JsonProperty` even if the Java name improves, and verify it with a contract test. Do not bind an external contract implicitly to an enum's `name()` or `ordinal()`.

<a id="json-003"></a>
### Use Jackson annotations for real contract differences

**JSON-003 · SHOULD**

Use `@JsonInclude`, `@JsonIgnoreProperties`, `@JsonProperty`, and custom serializers or deserializers only when they express real contract semantics. Do not apply `NON_NULL` to every Response or `ignoreUnknown = true` to every Request. Assign clear ownership of date format and time zone to global configuration, a specific field, or a serializer.

<a id="json-004"></a>
### Reuse configured mappers and existing response conventions

**JSON-004 · MUST NOT**

Do not create `new ObjectMapper()` in each class. Use the project-configured mapper. When a provider has a different contract, its adapter may own dedicated configuration. Do not impose a universal response wrapper or remove an existing wrapper solely for style.

<a id="json-005"></a>
### Keep entity serialization out of API contracts

**JSON-005 · MUST NOT**

Do not serialize JPA or Domain Entities directly and then force the API contract to fit through `@JsonIgnore`, lazy-loading modules, or cyclic-reference annotations. Create a Response that contains only allowed fields from the beginning. Do not perform Repository lookup, authorization, external calls, or state changes inside a serializer.

<a id="json-006"></a>
### Restrict polymorphic deserialization to permitted types

**JSON-006 · MUST**

Do not use Jackson Default Typing or open polymorphic deserialization based on internal implementation class names. When a real polymorphic contract exists, declare the permitted discriminator and type set explicitly, and verify unknown-type handling with contract tests.

## Compatibility checks

When an HTTP boundary changes, compare the URL, method, Request and Response fields, JSON types, null semantics, status codes, error responses, headers, session, cookies, redirects, sorting, pagination, and file results. Distinguish an ideal design for a new API from the actual compatibility contract of an existing API.
