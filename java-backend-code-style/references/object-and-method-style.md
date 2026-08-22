# Object, Method, Naming, and Package Rules

## Table of contents

- [Responsibilities and flow](#responsibilities-and-flow)
- [Method expression](#method-expression)
- [Encapsulation and reuse](#encapsulation-and-reuse)
- [Naming vocabulary](#naming-vocabulary)
- [Package consistency](#package-consistency)

## Responsibilities and flow

### OBJECT-001 — MUST

Give each class one cohesive business capability and one clear reason to change. Do not limit the number of methods mechanically; determine whether the methods share the same responsibility and reason to change. Do not mix Controller, Repository, external Client, and domain decisions in one service.

### OBJECT-002 — SHOULD

Make an application flow read in this order where practical:

1. Validate input and work context
2. Load the required objects
3. Verify authorization and execution preconditions
4. Execute domain behavior
5. Persist state
6. Deliver follow-up effects
7. Return an explicit result

Use mixed abstraction levels, long conditionals, hidden side effects, independently testable decisions, or interleaved database, external-call, and Response-conversion logic as stronger extraction signals than line count.

### OBJECT-003 — SHOULD

Use a guard clause when it exposes a failure condition first and reduces nesting. Do not mechanically require early returns or a single return point in every method.

```java
public void redeem(
    final MemberId memberId,
    final LocalDateTime redeemedAt
) {
    if (status != CouponStatus.ISSUED) {
        throw new CouponNotRedeemableException(id, status);
    }

    if (expirationPeriod.isExpiredAt(redeemedAt)) {
        throw new CouponExpiredException(id);
    }

    completeRedemption(memberId, redeemedAt);
}
```

## Method expression

### OBJECT-004 — SHOULD NOT

Do not use a Boolean flag that changes method behavior. Express the choice through a distinct verb or a meaningful business type.

```java
// Avoid.
exportMembers(command, true);

// Reveal the intent.
exportMemberSummary(command);
exportMembers(command, MemberExportFormat.FULL);
```

Distinguish a real Boolean domain attribute from a flag that selects an execution path. When several values form one business concept, group them into a Value Object or Command, but do not create a meaningless `Data` or `Context` type solely to reduce parameter count.

### OBJECT-005 — SHOULD

Use streams for straightforward transformations, filtering, and aggregation. Use an explicit loop for early termination, complex state accumulation, multiple side effects, exception handling, or ordered business meaning. Prefer a readable business sequence over a shorter functional expression.

### OBJECT-006 — MUST

Make the primary side effects predictable from the method name. A method that reads like a lookup or question, such as `find`, `get`, `calculate`, or `can`, must not change externally observable state. A Command may return a generated identifier or change result; do not require every Command to return `void`.

### OBJECT-007 — MUST NOT

Do not use `Map<String, Object>`, `Object[]`, raw collections, or an unmeaningful `Object` in a Domain or Application public contract. When unavoidable at an external boundary, convert it immediately in the adapter to a validated explicit type. Do not duplicate magic literals such as role codes, states, and retry limits, but do not create named constants for every contextually obvious number.

## Encapsulation and reuse

### OBJECT-008 — SHOULD

- Use the narrowest required access level.
- Do not make a private method public for testing.
- Use package-private visibility for internal implementations that are not external contracts where appropriate.
- Prefer composition over inheritance.
- Do not create a Base or Abstract class without a stable, genuine subtype relationship.
- Do not inherit solely to reuse common fields, a logger, a stored repository, or test fixtures.
- Do not move code to `common`, `util`, or `helper` merely because it appears twice. Extract a named concept only when meaning, ownership, and reason to change are the same.
- Do not mechanically make every class `final` solely because inheritance is not currently intended.

## Naming vocabulary

### NAMING-001 — MUST

Write class, method, variable, package, and enum identifiers in English and make them reflect the business language directly. Avoid phonetic transliterations of non-English terms and vague names such as `data`, `item`, `process`, `executeData`, `doWork`, `handleInfo`, and `manage`.

Good examples include `approveAdvertisement`, `redeemCoupon`, `reserveInventory`, `exportMembers`, and `calculateRefundAmount`. A short verb such as `Order.cancel()` is acceptable when the surrounding type already supplies the context.

### NAMING-002 — SHOULD

Use the following role suffixes when the project has no different established vocabulary.

| Area | Names |
|---|---|
| HTTP | `...Request`, `...Response`, `...Controller`, `...ApiExceptionHandler`, `...ArgumentResolver` |
| Application | `...Command`, `...Query`, `...Result`, `...UseCase`, `...Service` |
| Established Application DTO convention | `...RequestDto`, `...ResultDto`, `...Dto` |
| Domain | Business noun, `...Id`, `...Status`, `...Action`, `...Policy`, `...Authorization`, `...Decision`, `...Event`, `...Calculator` |
| Persistence | `...Repository`, `...QueryRepository`, `...SpringDataRepository`, `Jpa...RepositoryAdapter`, `QueryDsl...QueryRepository`, `...QueryRow`, `...JpaEntity`, `...PersistenceMapper` |
| External | `...Port`, `{Provider}...Adapter`, `{Provider}...Client`, `{Provider}...ProviderRequest`, `{Provider}...ProviderResponse`, `{Provider}...Mapper` |
| Configuration and Batch | `...Config`, `...Properties`, `...Scheduler`, `...Job`, `...Step`, `...Reader`, `...Processor`, `...Writer` |

Make `Port` mean a business contract, `Adapter` mean a provider implementation, and `Client` mean a raw protocol call.

### NAMING-003 — SHOULD NOT

- Do not use `Impl` when the implementation technology or role can be named directly.
- Do not use `Manager` unless the type represents an actual framework concept or resource lifecycle manager.
- Do not use `Helper`, `Utils`, or `Common` when they conceal a concrete responsibility.
- Use `Handler` only when the handled subject is explicit, as with an Exception, Event, or Message.
- Use `Processor` only for a genuine role such as a Spring Batch processor or an explicit pipeline stage.

For example, prefer `CreateMemberService` to `MemberServiceImpl`, and `FcmNotificationDeliveryAdapter` to `FcmServiceImpl`.

### NAMING-004 — MUST

Align method names with their return and failure semantics.

- Lookup expected to exist: `get...`
- Lookup that may be absent: `find...`
- Existence: `exists...`, `has...`
- Permission: `can...`, `isAllowed...`
- Calculation: `calculate...`
- Conversion: `to...`, `from`, `of`
- New construction: `create...`, `issue...`, `register...`
- Validation that fails on violation: `require...`, `ensure...`
- State change: the actual business verb

Do not make `get` return `Optional`, or make `find` always throw a technical exception when the value is absent.

### NAMING-005 — SHOULD

- Make a Boolean read as a state or question, such as `active`, `enabled`, `hasPermission`, `canRedeem`, or `shouldRetry`.
- Do not use `flag`, `check`, or `statusYn` in the Domain. Convert legacy database Y/N values to a business Boolean or enum in the mapper.
- Name collections to reveal plurality and key meaning, such as `members`, `authorizedCityCodes`, or `membersById`.
- Standardize acronym casing within the project, such as `Api`, `Http`, `Url`, `Id`, `Dto`, `Jpa`, `Sql`, and `Fcm`.

## Package consistency

### PACKAGE-001 — MUST

Before placing code, determine whether the project establishes package-by-feature, package-by-layer, a multi-module structure, or a deliberate hybrid. Inspect the current directory, adjacent features, dependency direction, and test placement together.

### PACKAGE-002 — MUST NOT

Do not mix synonymous naming systems such as `controller/presentation`, `service/application`, or `repository/persistence` within the same feature scope. Use the vocabulary of the existing structure.

### PACKAGE-003 — MUST NOT

Do not impose a specific tree such as `presentation/application/infrastructure` or `controller/service/repository` as a universal answer under the label of code style. Do not broadly move existing packages or reselect the top-level architecture.

### PACKAGE-004 — SHOULD

When the project already uses business modules, place dedicated Config, SQL, Adapter, Scheduler, and Batch code near the owning business code. Do not hide business concepts under `common`, `util`, `helper`, `misc`, or `temp`. Place Scheduler and Batch code as execution entry points owned by the relevant business area, not as independent domain names.
