# Java Methods, Access, and Names

This reference owns Java expression and naming conventions. Package layout and general responsibility principles are outside its scope.

## Java expression

<a id="object-005"></a>
### Choose streams or loops for readability

**OBJECT-005 · SHOULD**

Use streams for direct mapping, filtering, and aggregation. Use a loop for early exit, complex accumulation, ordered side effects, or exception handling. Extract an explicitly typed local when a stream chain hides intermediate meaning.

<a id="object-007"></a>
### Use explicit Java contract types

**OBJECT-007 · MUST NOT**

Do not expose Map<String, Object>, Object[], raw collections, or an unmeaningful Object in business or application signatures. Convert untyped external values in the implementation that reads them. Use typed DTOs, business types, enums, collections, and explicit absence or failure contracts.

<a id="object-008"></a>
### Use Java access levels deliberately

**OBJECT-008 · SHOULD**

Use the narrowest Java access compatible with callers and framework discovery. Use package-private implementations where practical. A public type needed by another internal package is not automatically a published application API.

Do not make production members public only for tests. Do not mechanically mark every class final; distinguish an immutable value class from a Spring component whose proxying may depend on subclassing.

## Naming

<a id="naming-001"></a>
### Use English business identifiers

**NAMING-001 · MUST**

Write Java class, method, variable, package, and enum identifiers in English using the established business vocabulary. Use the same glossary term for the same concept instead of phonetic transliterations or several synonyms.

<a id="naming-002"></a>
### Name Java implementation roles

**NAMING-002 · SHOULD**

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

<a id="naming-003"></a>
### Name implementations without breaking framework discovery

**NAMING-003 · SHOULD NOT**

Prefer JpaForecastRepository over a role-free ForecastRepositoryImpl when the implementation technology is useful information. Preserve Impl or another configured suffix where Spring Data repository-fragment discovery requires it.

Use Handler and Processor for actual framework or pipeline roles. A provider implementation need not be split into Adapter, Client, and Mapper merely to use every suffix.

<a id="naming-004"></a>
### Match Java method names to return and failure behavior

**NAMING-004 · MUST**

- get...: return a value expected to exist; report its absence meaningfully.
- find...: allow an ordinary absent result, commonly Optional<T>.
- exists... or has...: answer an existence question.
- can... or isAllowed...: inspect permission without changing state.
- calculate...: return a calculation without an external mutation.
- require... or ensure...: fail if the condition is not met.
- Business mutation: use the operation's actual business verb on its business owner.

Use [conversion names](http-dto-and-json-style.md#conversions) for object construction and representation changes. Do not make get return Optional or make find disguise ordinary absence as a technical failure.

<a id="naming-005"></a>
### Name Boolean values, collections, and acronyms

**NAMING-005 · SHOULD**

Use readable Boolean names such as active, enabled, hasPermission, and canRedeem. Interpret database Y/N encodings inside persistence code instead of carrying statusYn into a business model.

Use plural collection names and meaningful keys, such as members, authorizedCityCodes, and membersById. Use consistent acronym casing such as Api, Http, Url, Id, Dto, Jpa, Sql, and Fcm.
