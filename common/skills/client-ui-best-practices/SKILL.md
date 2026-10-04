---
name: client-ui-best-practices
description: Vite + React + TypeScript 및 Flutter + Dart 클라이언트 코드에서 상태 소유권, 컴포넌트·위젯 경계, 기능 구조, 서버 상태, 폼, 라우팅, 비동기 흐름, 테스트, 접근성, 성능과 보안을 저장소 맥락에 맞게 설계·구현·리팩터링·진단·리뷰한다. UI 아키텍처, 상태관리, 데이터 흐름 또는 기능 경계가 중요한 React·Flutter 작업에 사용한다. 순수 스타일링, 배포, 백엔드 전용 또는 무관한 단순 수정에는 사용하지 않는다.
---

# Client UI Best Practices

저장소의 현재 계약과 상태 소유권을 먼저 확인한 뒤, Vite + React + TypeScript 또는 Flutter + Dart 클라이언트 작업을 최소 범위로 설계하고 수행한다. 라이브러리 취향이나 폴더 템플릿을 강제하지 말고, 올바른 소유권·명시적인 데이터 흐름·검증 가능한 사용자 동작을 만든다.

## 요청 모드 확정

사용자의 동사와 명시적 범위로 모드를 먼저 확정한다.

- **리뷰**: 읽기 전용으로 결함을 찾는다. 파일을 수정하지 않는다. 반드시 [review-rubric.md](references/review-rubric.md)를 추가로 읽는다.
- **진단**: 원인과 근거를 추적한다. 사용자가 수정을 요청하지 않았으면 파일을 수정하지 않는다.
- **설계**: 저장소의 실제 구조와 제약에 맞는 경계와 선택지를 제시한다. 구현 요청이 없으면 파일을 수정하지 않는다.
- **구현·수정·리팩터링**: 요청에 필요한 파일과 테스트를 변경하고 프로젝트의 검증 명령을 실행한다.
- **혼합 요청**: 명시적으로 요청된 변경만 수행하고, 나머지는 별도 제안으로 분리한다.

모드가 애매하면 먼저 읽기 전용 탐색을 수행한다. 읽기 전용 요청을 구현 권한으로 확대하지 않는다.

## 대상 기술 판별과 참조 선택

사용자에게 묻기 전에 manifest, lockfile, 설정, import, 대상 파일을 확인한다.

1. `package.json`, lockfile, Vite 설정, `tsconfig`, React import와 실제 소스가 대상이면 [react-typescript.md](references/react-typescript.md)를 읽는다.
2. `pubspec.yaml`, lockfile, Flutter·Dart SDK 제약, Flutter import와 실제 소스가 대상이면 [flutter-dart.md](references/flutter-dart.md)를 읽는다.
3. 모노레포에 두 기술이 있어도 사용자가 지정한 기능이나 파일의 참조만 읽는다.
4. 한 요청이 두 클라이언트를 실제로 함께 변경할 때만 두 참조를 모두 읽는다.
5. 리뷰 모드에서만 기술 참조와 함께 [review-rubric.md](references/review-rubric.md)를 읽는다.

설정 파일이 존재한다는 이유만으로 대상 기술이나 배포 플랫폼을 단정하지 않는다. 실제 import, build 설정, 사용처를 교차 확인한다.

## 작업 절차

### 1. 범위와 저장소 계약 파악

- 사용자 목표, 완료 조건, 비목표, 변경 가능 범위를 한 문장씩 정리한다.
- 작업 트리의 기존 사용자 변경을 확인하고 관련 없는 변경을 보존한다.
- 아키텍처와 계층 경계, naming, file layout, dependency direction, 테스트 관례를 확인한다.
- 상태관리, 서버 상태, 라우팅, 폼, 직렬화, 테스트 도구와 실제 버전을 manifest·lockfile·import에서 확인한다.
- 실제 build, typecheck, lint, analysis, test 명령을 package script, tool 설정, 프로젝트 문서에서 찾는다.

### 2. 정의와 사용처 추적

- 먼저 기능·데이터 흐름·상태 소유권을 포괄하는 넓은 의미 검색을 수행한다.
- 같은 개념을 다른 표현으로 여러 번 검색한다.
- 대상 symbol의 정의, 생성 지점, 변환, 모든 주요 소비자, 테스트를 추적한다.
- API 계약, schema, type, config, constant, fixture 중 무엇이 단일 진실 공급원인지 확인한다.
- 기존 추상화가 요청을 이미 해결하는지 확인하기 전에는 새 추상화를 만들지 않는다.

### 3. 상태 소유권 분류

각 상태에 대해 의미, 권위 있는 소유자, 소비자, 변경 주체, 생명주기, 복원 요구, 폐기 시점을 확인한다. 다음 순서로 배치한다.

1. 다른 값에서 계산할 수 있으면 저장하지 말고 파생한다.
2. 일시적인 표현 상태는 사용하는 가장 가까운 컴포넌트·위젯이 소유한다.
3. 입력 중인 초안과 표시 오류는 폼 경계가 소유한다.
4. 공유·북마크·새로고침·뒤로 가기 복원이 필요하면 URL·라우터·내비게이션이 소유한다.
5. 원격 데이터와 freshness·loading·error는 query/cache 계층이 소유한다.
6. 기기에 유지되는 값은 storage repository를 권위 있는 경계로 둔다.
7. 여러 화면이 함께 수정하는 클라이언트 도메인 상태는 feature 범위 상태 객체가 소유한다.
8. 인증 세션처럼 앱 전체 생명주기를 가진 상태만 app global로 승격한다.

같은 서버 데이터를 query cache, global store, local state에 복제하지 않는다. 같은 URL 값을 router와 store에 함께 저장하지 않는다. 복제가 불가피하면 목적, 권위자, 동기화 방향, 충돌, 만료와 폐기를 명시한다.

### 4. 책임과 데이터 흐름 설계

다음 흐름이 코드에서 읽히게 한다.

`사용자 입력 → 의도가 드러나는 명령 → 상태 객체·Use Case → Repository·외부 경계 → 명시적 상태 전이 → UI`

- `setLoading`, 범용 setter보다 `submitOrder`, `retryPayment`, `selectDeliveryAddress`처럼 사용자 의도를 드러낸다.
- UI는 렌더링·조합·입력 전달에 집중한다.
- Domain은 프레임워크, HTTP, 저장소, 라우터에 의존하지 않는다.
- Application·Use Case는 도메인 행위와 외부 경계를 조정한다.
- Infrastructure는 API, storage, analytics, platform API를 구현한다.
- 앱 시작 지점이나 명확한 composition root에서 dependency를 조립한다.
- mutable global singleton과 어디서나 접근하는 service locator를 만들지 않는다.

DDD·Clean Architecture·OOP는 실제 도메인 복잡도에 비례해 적용한다. 식별성과 생명주기가 있을 때 Entity, 의미와 검증 규칙이 있을 때 Value Object, 여러 경계를 조정할 때 Use Case, 실제 외부 경계를 보호할 때 Repository나 interface를 도입한다. 단순 CRUD에 비어 있는 계층과 구현 하나뿐인 장식용 abstraction을 만들지 않는다.

### 5. 컴포넌트·위젯 경계 결정

줄 수가 아니라 책임, 상태 소유권, 생명주기, 변경 이유로 나눈다.

- 독립 state·effect·async work·error handling·test contract가 있으면 분리를 검토한다.
- 상위 요소와 다른 이유로 변경되거나 같은 의미와 계약으로 반복 사용되면 분리를 검토한다.
- 긴 JSX·widget tree, 미래의 재사용 추측, 고정 파일 크기만으로 분리하지 않는다.
- 분리 후 많은 구현 세부 props를 그대로 전달한다면 경계를 다시 검토한다.
- boolean flag가 늘어 여러 역할을 맡으면 composition, 명시적 variant, slot·children을 검토한다.
- 두 번 사용됐다는 이유만으로 `shared`에 승격하지 않는다. 안정된 의미, 동일 계약, 동일 변경 방향, 명확한 소유권이 모두 확인될 때만 공용화한다.
- 공용 UI primitive가 특정 feature store, API client, route에 의존하지 않게 한다.

### 6. 비동기·서버·폼·라우팅 계약 확정

- 중요한 비동기 흐름은 `initial`, `loading`, `success(data)`, `empty`, `refreshing(previousData)`, `failure(error, previousData?)` 중 실제 필요한 상태를 배타적으로 모델링한다.
- 겹치는 요청에는 latest-wins, 중복 차단, 순차 실행 중 하나를 의식적으로 정한다.
- mutation 후 권위 있는 cache 갱신 또는 invalidation 정책을 정한다.
- optimistic update는 사용자 가치와 rollback 계약이 있을 때만 사용한다.
- 폼 초안, 클라이언트 안내용 검증, 도메인 규칙, 서버 검증의 소유자를 분리한다.
- URL path·query·deep link를 외부 입력으로 파싱하고 serialize·deserialize 규칙을 한곳에 둔다.
- 복원돼야 할 상태를 메모리 전용 route extra나 임시 store에 숨기지 않는다.

### 7. 규칙 강도와 변경 범위 판단

규칙을 다음 세 단계로 구분한다.

- **필수 계약**: 실제 오동작, 데이터 불일치, 보안·개인정보 위험을 막는 규칙이다. 위반을 그대로 답습하지 않는다.
- **강한 기본값**: feature-first, local state 우선, intent-centered API, server-state 전용 소유자, 접근성 완료 기준 등이다. 저장소 근거가 있으면 예외를 허용한다.
- **상황별 휴리스틱**: 특정 store·form·router 도구, memoization, codegen, file split 등이다. 현재 버전, 팀 표준, 측정 결과로 선택한다.

기존 Redux, Zustand, BLoC, Provider, ChangeNotifier 등을 개인 취향으로 교체하지 않는다. 실제 결함을 해결하는 최소 범위만 변경하고, 광범위한 migration은 별도 제안으로 분리한다. “베스트 프랙티스이므로”를 변경 근거로 사용하지 않는다.

## 필수 계약

- 하나의 사실에는 하나의 권위 있는 소유자를 둔다.
- React render와 Flutter build 중 네트워크, 저장, analytics 같은 부수 효과를 실행하지 않는다.
- API, storage, URL, environment, file, deep link, platform channel 등 외부 입력을 runtime validation 또는 명시적 parser로 내부 타입에 변환한다.
- 정적 type assertion이나 cast만으로 외부 데이터가 유효하다고 가정하지 않는다.
- 오류를 조용히 삼키거나 무관한 기본값으로 바꾸지 않는다. 복구 가능한 오류와 계약·프로그램 오류를 구분한다.
- subscription, controller, stream, animation, request 등 리소스의 owner와 cleanup·cancellation을 명확히 한다.
- client route guard와 UI 숨김을 최종 authorization으로 간주하지 않는다.
- client bundle·binary·log·analytics·error report에 secret, token, password, 불필요한 개인정보를 넣지 않는다.
- raw HTML, WebView content, external URL, redirect, file path의 신뢰 경계와 validation·sanitization을 확인한다.
- logout과 account switch 때 사용자별 cache와 민감 state의 폐기 범위를 정한다.
- accessibility를 선택적 사후 작업이 아니라 기능 완료 조건으로 취급한다.
- 사용자 표시 문자열을 state code나 domain 판단 값으로 사용하지 않는다. Domain·Application은 번역 문장 대신 의미 있는 code와 type을 반환한다.

## 성능·오프라인·관찰 가능성

- 안정적인 domain identifier를 list key로 사용하고 state subscription 범위를 실제 소비 범위로 제한한다.
- derived state와 server state를 중복 저장하지 않고, render·build의 반복적인 무거운 계산을 피한다.
- 광범위한 memoization, caching, normalization, virtualization은 재현 조건과 측정 근거가 있을 때 적용한다.
- 기본은 online-first다. cache를 offline-first의 권위 있는 local model로 오해하지 않는다.
- offline editing이 명시적 요구일 때만 command queue, idempotency, conflict, retention, account isolation, 복구를 별도 동기화 도메인으로 설계한다.
- log, error report, analytics는 공급자 중립적인 Infrastructure boundary 뒤에 둔다.
- 같은 오류를 여러 계층에서 중복 기록하지 않고, event contract를 typed single source로 관리한다.

## 버전·의존성·코드 생성

- 설치된 manifest, lockfile, import와 공식 문서에서 현재 API를 확인한다.
- 최신이라는 이유만으로 dependency를 upgrade하거나 요청받지 않은 major migration을 수행하지 않는다.
- 그린필드 dependency는 작업 시점의 stable 공식 문서와 실제 필요를 확인한 뒤 최소로 추가한다.
- 코드 생성은 OpenAPI·GraphQL schema, serialization declaration, typed route declaration처럼 권위 있는 선언에서 반복 계약을 파생할 때만 사용한다.
- generated file을 직접 수정하지 않는다. declaration을 단일 진실 공급원으로 두고 generate·validate 명령을 재현한다.

## 테스트와 완료 조건

행동 변경에는 가장 가까운 책임 경계의 테스트를 추가하거나 갱신한다.

- Domain rule은 프레임워크 없는 단위 테스트로 검증한다.
- Use Case와 state transition은 제어 가능한 외부 경계 대역으로 검증한다.
- component·widget은 내부 구현보다 사용자가 보는 결과와 상호작용으로 검증한다.
- loading, success, empty, failure, retry, duplicate submission, routing 등 실제 분기를 검증한다.
- 버그 수정에는 실패를 재현하는 regression test를 먼저 확보한다.
- E2E는 실패 비용이 큰 핵심 사용자 여정에 집중한다.

구현 모드에서는 저장소가 정의한 관련 테스트, typecheck, lint, Dart analysis, format check와 필요한 build를 실행한다. 실패를 분류해 원인을 바꾸지 않은 동일 재시도를 반복하지 않는다. 실행하지 못한 검증은 명령, 이유, 남은 위험과 함께 보고한다.

리뷰·진단·설계 모드에서는 파일을 변경하지 않았음을 유지하고, 결론을 근거와 함께 제시한다. 최종 응답은 결과를 먼저 전달하고 변경 파일, 핵심 판단, 통과한 검증, 남은 검증 공백만 간결하게 정리한다.
