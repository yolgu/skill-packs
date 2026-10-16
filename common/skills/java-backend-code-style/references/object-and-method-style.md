# Java Methods, Access, and Names

This reference owns Java expression and naming conventions. Package layout and general responsibility principles are outside its scope.

## Java expression

### Choose streams or loops for readability

**SHOULD**

Use streams for direct mapping, filtering, and aggregation. Use a loop for early exit, complex accumulation, ordered side effects, or exception handling. Extract an explicitly typed local when a stream chain hides intermediate meaning.

### Use explicit Java contract types

**MUST NOT**

Do not expose Map<String, Object>, Object[], raw collections, or an unmeaningful Object in business or application signatures. Convert untyped external values in the implementation that reads them. Use typed DTOs, business types, enums, collections, and explicit absence or failure contracts.

### Use Java access levels deliberately

**SHOULD**

Use the narrowest Java access compatible with callers and framework discovery. Use package-private implementations where practical. A public type needed by another internal package is not automatically a published application API.

Do not make production members public only for tests. Do not mechanically mark every class final; distinguish an immutable value class from a Spring component whose proxying may depend on subclassing.

## Naming

### Use English business identifiers

**MUST**

Write Java class, method, variable, package, and enum identifiers in English using the established business vocabulary. Use the same glossary term for the same concept instead of phonetic transliterations or several synonyms.

### Name Java implementation roles

**SHOULD**

| Role | Names |
|---|---|
| HTTP components | ...Controller, ...ApiExceptionHandler, ...ArgumentResolver |
| Application execution | ...Service; ...UseCase when an independent interface is needed |
| Business model | Business noun, ...Id, ...Status, ...Policy, ...Decision, ...Event, ...Calculator |
| Persistence contract | ...Repository, ...QueryRepository |
| Persistence implementation | Jpa...Repository, ...SpringDataRepository, ...JpaEntity, ...QueryRow |
| External implementation | Provider-prefixed Client or Adapter that describes its actual role |
| Configuration and Batch | ...Config, ...Properties, ...Scheduler, ...Job, ...Step, ...Reader, ...Processor, ...Writer |

These names describe roles that exist, not a list of types to generate. Input and result type names are defined in [HTTP and DTO models](http-dto-and-json-style.md#boundary-models).

### Name implementations without breaking framework discovery

**SHOULD NOT**

Prefer JpaForecastRepository over a role-free ForecastRepositoryImpl when the implementation technology is useful information. Preserve Impl or another configured suffix where Spring Data repository-fragment discovery requires it.

Use Handler and Processor for actual framework or pipeline roles. A provider implementation need not be split into Adapter, Client, and Mapper merely to use every suffix.

### Match Java method names to return and failure behavior

**MUST**

- get...: return a value expected to exist; report its absence meaningfully.
- find...: allow an ordinary absent result, commonly Optional<T>.
- exists... or has...: answer an existence question.
- can... or isAllowed...: inspect permission without changing state.
- calculate...: return a calculation without an external mutation.
- require... or ensure...: fail if the condition is not met.
- Business mutation: use the operation's actual business verb on its business owner.

Use [conversion names](http-dto-and-json-style.md#conversions) for object construction and representation changes. Do not make get return Optional or make find disguise ordinary absence as a technical failure.

### Name Boolean values, collections, and acronyms

**SHOULD**

Use readable Boolean names such as active, enabled, hasPermission, and canRedeem. Interpret database Y/N encodings inside persistence code instead of carrying statusYn into a business model.

Use plural collection names and meaningful keys, such as members, authorizedCityCodes, and membersById. Use consistent acronym casing such as Api, Http, Url, Id, Dto, Jpa, Sql, and Fcm.
