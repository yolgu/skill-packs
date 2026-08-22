# Complete Flow Examples

## Table of contents

- [How to use these examples](#how-to-use-these-examples)
- [From HTTP to Domain persistence](#from-http-to-domain-persistence)
- [External provider adapter](#external-provider-adapter)
- [QueryDSL result conversion](#querydsl-result-conversion)
- [Legacy adapter with a shared Use Case](#legacy-adapter-with-a-shared-use-case)

## How to use these examples

The following snippets are abbreviated examples of responsibility connections. They do not impose a package tree, framework version, or common response structure. Apply the target project's Java, Spring, Jackson, exception, and test conventions first, and reuse only the responsibility boundaries demonstrated here.

## From HTTP to Domain persistence

Flow:

```text
HTTP Request
→ Command
→ Use Case
→ Authorization
→ Domain Entity
→ Repository
→ Result
→ HTTP Response
```

### HTTP model and Controller

```java
@Getter
public class ApproveAdvertisementRequest {

    @NotBlank
    private final String approvalReason;

    @JsonCreator
    public ApproveAdvertisementRequest(
        @JsonProperty("approvalReason") final String approvalReason
    ) {
        this.approvalReason = approvalReason;
    }

    public ApproveAdvertisementCommand toCommand(
        final Long advertisementId
    ) {
        return ApproveAdvertisementCommand.of(
            AdvertisementId.of(advertisementId),
            ApprovalReason.of(approvalReason)
        );
    }
}
```

```java
@RestController
@RequiredArgsConstructor
public class AdvertisementController {

    private final ApproveAdvertisementUseCase approveAdvertisementUseCase;

    @PreAuthorize("isAuthenticated()")
    @PostMapping("/advertisements/{advertisementId}/approval")
    public AdvertisementApprovalResponse approve(
        @CurrentAdmin final AdminCommandContext adminContext,
        @PathVariable final Long advertisementId,
        @Valid @RequestBody final ApproveAdvertisementRequest request
    ) {
        final ApproveAdvertisementResult result =
            approveAdvertisementUseCase.approve(
                adminContext,
                request.toCommand(advertisementId)
            );

        return AdvertisementApprovalResponse.from(result);
    }
}
```

### Application boundary

```java
public interface ApproveAdvertisementUseCase {

    ApproveAdvertisementResult approve(
        AdminCommandContext adminContext,
        ApproveAdvertisementCommand command
    );
}
```

```java
@Service
@RequiredArgsConstructor
public class ApproveAdvertisementService
    implements ApproveAdvertisementUseCase {

    private final AdvertisementRepository advertisementRepository;
    private final AdvertisementManagementAuthorization authorization;
    private final Clock clock;

    @Override
    @Transactional
    public ApproveAdvertisementResult approve(
        final AdminCommandContext adminContext,
        final ApproveAdvertisementCommand command
    ) {
        authorization
            .decide(
                adminContext.getActor(),
                adminContext.getWorkContext(),
                AdvertisementManagementAction.APPROVE_ADVERTISEMENT
            )
            .requireAllowed();

        final Advertisement advertisement = advertisementRepository
            .findById(command.getAdvertisementId())
            .orElseThrow(
                () -> new AdvertisementNotFoundException(
                    command.getAdvertisementId()
                )
            );

        final Instant approvedAt = clock.instant();
        advertisement.approve(
            adminContext.getActor().getAdminId(),
            command.getApprovalReason(),
            approvedAt
        );

        final Advertisement savedAdvertisement =
            advertisementRepository.save(advertisement);

        return ApproveAdvertisementResult.from(savedAdvertisement);
    }
}
```

### Domain behavior

```java
public void approve(
    final AdminId approvedBy,
    final ApprovalReason approvalReason,
    final Instant approvedAt
) {
    if (status != AdvertisementStatus.REVIEW_PENDING) {
        throw new AdvertisementNotApprovableException(id, status);
    }

    approval = AdvertisementApproval.of(
        approvedBy,
        approvalReason,
        approvedAt
    );
    status = AdvertisementStatus.APPROVED;
}
```

In this flow, the Controller annotation verifies authentication only, while the Use Case enforces actual business authorization. The Application establishes the reference time once, and the Domain does not query current time directly.

## External provider adapter

Flow:

```text
Application Port
→ Provider Adapter
→ Provider Client
→ Provider response and error translation
→ Local Result
```

```java
public interface NotificationDeliveryPort {

    NotificationDeliveryResult deliver(
        NotificationDeliveryRequest request
    );
}
```

```java
@Component
@RequiredArgsConstructor
public class FcmNotificationDeliveryAdapter
    implements NotificationDeliveryPort {

    private final FcmClient fcmClient;
    private final FcmNotificationMapper mapper;

    @Override
    public NotificationDeliveryResult deliver(
        final NotificationDeliveryRequest request
    ) {
        final FcmProviderRequest providerRequest =
            mapper.toProviderRequest(request);

        try {
            final FcmProviderResponse providerResponse =
                fcmClient.send(providerRequest);

            return mapper.toDeliveryResult(providerResponse);
        } catch (FcmRateLimitException exception) {
            throw new NotificationDeliveryTemporarilyUnavailableException(
                exception.getSafeRequestId(),
                exception
            );
        } catch (FcmInvalidRequestException exception) {
            throw new NotificationDeliveryRejectedException(
                exception.getSafeRequestId(),
                exception
            );
        }
    }
}
```

If `FcmProviderResponse` means successful acceptance, make `NotificationDeliveryResult` express acceptance as well. Do not overstate it as confirmed end-user receipt. Declare timeout and retry behavior at the Client and Adapter boundary, and do not create duplicate retries for the same Application call.

## QueryDSL result conversion

Flow:

```text
Application Query + Authorized Scope
→ QueryDSL Predicate
→ QueryRow
→ Application Result
→ HTTP Response
```

```java
@Repository
@RequiredArgsConstructor
public class QueryDslMemberQueryRepository
    implements MemberQueryRepository {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<MemberSummaryResult> search(
        final SearchMembersQuery query,
        final AuthorizedMemberScope authorizedScope
    ) {
        if (authorizedScope.isEmpty()) {
            return List.of();
        }

        final BooleanBuilder predicate = new BooleanBuilder();
        predicate.and(scopePredicate(authorizedScope));
        predicate.and(cityCodeEquals(query.getCityCode()));
        predicate.and(statusEquals(query.getStatus()));

        final List<MemberSummaryQueryRow> rows = queryFactory
            .select(
                Projections.constructor(
                    MemberSummaryQueryRow.class,
                    member.id,
                    member.nickname,
                    member.status
                )
            )
            .from(member)
            .where(predicate)
            .orderBy(
                member.createdAt.desc(),
                member.id.desc()
            )
            .limit(query.getPageSize())
            .fetch();

        return rows.stream()
            .map(MemberSummaryResult::from)
            .toList();
    }

    private BooleanExpression cityCodeEquals(final String cityCode) {
        if (cityCode == null || cityCode.isBlank()) {
            return null;
        }

        return member.cityCode.eq(cityCode);
    }
}
```

Use a nullable Predicate helper only for a simple optional filter, and handle authorization Scope explicitly. Prevent an empty Scope from becoming an unrestricted query. Do not return a Q-type or QueryRow beyond the Application boundary.

## Legacy adapter with a shared Use Case

Flow:

```text
Legacy Controller → Legacy Request conversion ┐
                                               ├→ Shared Use Case
Admin Controller  → Admin Command conversion  ┘
                                               ├→ Legacy Response
                                               └→ Admin Response
```

```java
@RestController
@RequiredArgsConstructor
public class LegacyMemberController {

    private final SearchMembersUseCase searchMembersUseCase;

    @GetMapping("/legacy/member/list")
    public LegacyMemberSearchResponse search(
        @CurrentAdmin final AdminQueryContext adminContext,
        final LegacyMemberSearchRequest request
    ) {
        final SearchMembersResult result =
            searchMembersUseCase.search(
                adminContext,
                request.toQuery()
            );

        return LegacyMemberSearchResponse.from(result);
    }
}
```

```java
public static LegacyMemberResponse from(
    final MemberSummaryResult result
) {
    // COMPATIBILITY EXCEPTION: JSON-002
    // The supported legacy client treats an empty nickname as unregistered.
    // Scope: LegacyMemberResponse
    // Verification: LegacyMemberApiCompatibilityTest
    final String nickname = result.getNickname() == null
        ? ""
        : result.getNickname();

    return new LegacyMemberResponse(
        result.getMemberId(),
        nickname,
        result.getStatusCode()
    );
}
```

Legacy and new Controllers may invoke the same Use Case and authorization Policy, but each external contract owns its Request, Response, and error Handler. Keep compatibility behavior in the legacy adapter and do not propagate it into the Domain or a new Response.
