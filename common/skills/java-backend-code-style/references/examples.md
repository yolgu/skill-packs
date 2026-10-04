# Connected Java Examples

## Scope

The complete example below updates one stored forecast value. Each Java block is one source file, with package declarations showing source dependencies. The service owns the transaction; the public repository owns its input and result; the JPA implementation owns Entity access and conversion.

Use these roles when the task needs them. This CRUD example has no business rule requiring a separate domain twin, UseCase interface, Mapper, or extra Adapter.

## HTTP input and service input

### UpdateForecastRequest.java

~~~java
package example.weather.controller.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import example.weather.service.model.UpdateForecastRequestDto;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public class UpdateForecastRequest {

    @NotNull
    private final BigDecimal temperature;

    @JsonCreator
    public UpdateForecastRequest(
        @JsonProperty("temperature") final BigDecimal temperature
    ) {
        this.temperature = temperature;
    }

    public UpdateForecastRequestDto toDto(final Long forecastId) {
        return UpdateForecastRequestDto.of(forecastId, temperature);
    }
}
~~~

### UpdateForecastRequestDto.java

~~~java
package example.weather.service.model;

import java.math.BigDecimal;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(staticName = "of")
public class UpdateForecastRequestDto {

    private final Long forecastId;
    private final BigDecimal temperature;
}
~~~

## Public repository contract

### ForecastRepository.java

~~~java
package example.weather.repository;

import example.weather.repository.model.ForecastResultDto;
import example.weather.repository.model.SaveForecastRequestDto;

public interface ForecastRepository {

    ForecastResultDto update(SaveForecastRequestDto request);
}
~~~

### SaveForecastRequestDto.java

~~~java
package example.weather.repository.model;

import java.math.BigDecimal;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(staticName = "of")
public class SaveForecastRequestDto {

    private final Long forecastId;
    private final BigDecimal temperature;
}
~~~

### ForecastResultDto.java

~~~java
package example.weather.repository.model;

import java.math.BigDecimal;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(staticName = "of")
public class ForecastResultDto {

    private final Long forecastId;
    private final BigDecimal temperature;
}
~~~

### ForecastNotFoundException.java

~~~java
package example.weather.repository;

public class ForecastNotFoundException extends RuntimeException {

    public ForecastNotFoundException(final Long forecastId) {
        super("Forecast not found: " + forecastId);
    }
}
~~~

The repository's public types have no JPA or QueryDSL dependency. The normal API exception handler can translate this absence to its own HTTP contract.

## JPA implementation

### ForecastJpaEntity.java

~~~java
package example.weather.repository.jpa.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "weather_forecast")
@Getter
@Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class ForecastJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private BigDecimal temperature;
}
~~~

### ForecastSpringDataRepository.java

~~~java
package example.weather.repository.jpa;

import example.weather.repository.jpa.model.ForecastJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ForecastSpringDataRepository
    extends JpaRepository<ForecastJpaEntity, Long> {
}
~~~

### JpaForecastRepository.java

~~~java
package example.weather.repository.jpa;

import example.weather.repository.ForecastNotFoundException;
import example.weather.repository.ForecastRepository;
import example.weather.repository.jpa.model.ForecastJpaEntity;
import example.weather.repository.model.ForecastResultDto;
import example.weather.repository.model.SaveForecastRequestDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class JpaForecastRepository implements ForecastRepository {

    private final ForecastSpringDataRepository forecasts;

    @Override
    public ForecastResultDto update(final SaveForecastRequestDto request) {
        final ForecastJpaEntity entity = forecasts
            .findById(request.getForecastId())
            .orElseThrow(() -> new ForecastNotFoundException(request.getForecastId()));

        entity.setTemperature(request.getTemperature());
        final ForecastJpaEntity saved = forecasts.save(entity);

        return ForecastResultDto.of(saved.getId(), saved.getTemperature());
    }
}
~~~

Entity access and value mapping stay here. ForecastResultDto does not declare from(ForecastJpaEntity), and the Entity does not accept a DTO.

## Application flow and result

### ForecastService.java

~~~java
package example.weather.service;

import example.weather.repository.ForecastRepository;
import example.weather.repository.model.ForecastResultDto;
import example.weather.repository.model.SaveForecastRequestDto;
import example.weather.service.model.UpdateForecastRequestDto;
import example.weather.service.model.UpdateForecastResultDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ForecastService {

    private final ForecastRepository forecasts;

    @Transactional
    public UpdateForecastResultDto update(final UpdateForecastRequestDto request) {
        final SaveForecastRequestDto storageRequest = SaveForecastRequestDto.of(
            request.getForecastId(),
            request.getTemperature()
        );
        final ForecastResultDto stored = forecasts.update(storageRequest);
        return UpdateForecastResultDto.from(stored);
    }
}
~~~

### UpdateForecastResultDto.java

~~~java
package example.weather.service.model;

import example.weather.repository.model.ForecastResultDto;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public class UpdateForecastResultDto {

    private final Long forecastId;
    private final BigDecimal temperature;

    public static UpdateForecastResultDto from(final ForecastResultDto result) {
        return new UpdateForecastResultDto(result.getForecastId(), result.getTemperature());
    }
}
~~~

When actual business rules exist, this service invokes a plain business object or Policy before preparing the storage request. Authorization and execution time are established at the application boundary when that operation requires them. Those responsibilities do not move to the JPA Entity.

## HTTP output

### ForecastResponse.java

~~~java
package example.weather.controller.model;

import example.weather.service.model.UpdateForecastResultDto;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public class ForecastResponse {

    private final Long forecastId;
    private final BigDecimal temperature;

    public static ForecastResponse from(final UpdateForecastResultDto result) {
        return new ForecastResponse(result.getForecastId(), result.getTemperature());
    }
}
~~~

### ForecastController.java

~~~java
package example.weather.controller;

import example.weather.controller.model.ForecastResponse;
import example.weather.controller.model.UpdateForecastRequest;
import example.weather.service.ForecastService;
import example.weather.service.model.UpdateForecastResultDto;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class ForecastController {

    private final ForecastService forecasts;

    @PatchMapping("/forecasts/{forecastId}")
    public ForecastResponse update(
        @PathVariable("forecastId") final Long forecastId,
        @Valid @RequestBody final UpdateForecastRequest request
    ) {
        final UpdateForecastResultDto result = forecasts.update(request.toDto(forecastId));
        return ForecastResponse.from(result);
    }
}
~~~

## Provider conversion

This excerpt belongs inside a provider implementation. The protocol client exists only if it already has a separate communication responsibility; a small provider implementation can perform the call directly.

~~~java
@Override
public NotificationDeliveryResultDto deliver(
    final NotificationDeliveryRequestDto request
) {
    final FcmProviderResponse response = client.send(
        FcmProviderRequest.of(request.getRecipient(), request.getMessage())
    );
    return NotificationDeliveryResultDto.of(response.getRequestId(), response.isAccepted());
}
~~~

The published result receives values, not FcmProviderResponse. Translate SDK failures into the integration contract's failure meanings in this implementation. Acceptance means provider acceptance, not confirmed end-user receipt. Use the configured timeout and retry policy without duplicating retries at every layer.

## Query result conversion

This excerpt belongs inside the query implementation after the authorized scope and query result have been obtained.

~~~java
if (authorizedScope.isEmpty()) {
    return List.of();
}

final List<MemberSummaryQueryRow> rows = queryFactory
    .select(Projections.constructor(MemberSummaryQueryRow.class, member.id, member.nickname))
    .from(member)
    .where(scopePredicate(authorizedScope))
    .orderBy(member.id.asc())
    .limit(request.getPageSize())
    .fetch();

return rows.stream()
    .map((MemberSummaryQueryRow row) -> MemberSummaryResultDto.of(row.getId(), row.getNickname()))
    .toList();
~~~

MemberSummaryQueryRow is internal. MemberSummaryResultDto is the public repository result and does not import that row or a QueryDSL type. A plain DTO projection can also be used directly when no internal query representation is needed. An empty authorized scope must never become an unrestricted query.

For an existing API with a required representation difference, keep that conversion in its own HTTP response or handler. Do not assume a legacy endpoint or introduce a compatibility layer into a new example.
