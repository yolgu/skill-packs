# Flutter + Dart 실행 기준

이 문서는 Flutter + Dart가 실제 작업 대상일 때만 읽는다. 공통 상태 소유권, 필수 계약, 요청 모드와 최소 변경 원칙은 상위 `SKILL.md`를 단일 진실 공급원으로 사용하고, 여기서는 Flutter 생태계에 필요한 판단만 구체화한다.

## 목차

- [프로젝트와 플랫폼 분석](#프로젝트와-플랫폼-분석)
- [기능 구조와 의존 방향](#기능-구조와-의존-방향)
- [그린필드 아키텍처](#그린필드-아키텍처)
- [기존 상태관리 체계 존중](#기존-상태관리-체계-존중)
- [상태 도구 선택](#상태-도구-선택)
- [View와 ViewModel·Notifier](#view와-viewmodelnotifier)
- [비동기와 서버 상태](#비동기와-서버-상태)
- [라우팅과 내비게이션](#라우팅과-내비게이션)
- [폼과 편집 초안](#폼과-편집-초안)
- [외부 데이터와 코드 생성](#외부-데이터와-코드-생성)
- [리소스 생명주기](#리소스-생명주기)
- [의존성 조립](#의존성-조립)
- [테스트](#테스트)
- [접근성](#접근성)
- [성능](#성능)
- [보안과 개인정보](#보안과-개인정보)
- [국제화·관찰 가능성·오프라인](#국제화관찰-가능성오프라인)
- [안티패턴과 교정 기준](#안티패턴과-교정-기준)
- [검증](#검증)
- [공식 기준 자료](#공식-기준-자료)

## 프로젝트와 플랫폼 분석

다음 순서로 현재 계약을 확인한다.

1. `pubspec.yaml`, `pubspec.lock`, Dart·Flutter SDK 제약, dependency와 dev_dependency를 읽는다.
2. `analysis_options.yaml`, formatter·linter, build runner, test 설정과 실제 명령을 확인한다.
3. state management, router, HTTP, serialization, local storage, analytics package의 선언과 실제 import·사용처를 찾는다.
4. `lib`의 feature 경계, app composition root, shared module, import direction을 확인한다.
5. 대상 Provider·Notifier·BLoC·ChangeNotifier·Controller의 선언, override, listener, consumer, dispose, test를 추적한다.
6. API schema, DTO declaration, generated file, domain type, fixture 중 권위 있는 선언을 식별한다.
7. Android·iOS가 기본 대상인지 build 설정과 실제 코드를 확인한다. web·desktop은 프로젝트가 실제 지원할 때만 해당 제약을 적용한다.

platform directory가 존재한다는 사실만으로 지원 대상을 단정하지 않는다. build configuration, plugin support, conditional import, 실제 배포 script를 교차 확인한다.

## 기능 구조와 의존 방향

기본은 기능 중심 수직 분할이다.

```text
lib/
  app/
  features/
    checkout/
      domain/
      application/
      infrastructure/
      presentation/
  shared/
```

이 예시의 네 내부 계층을 모든 기능에 강제하지 않는다.

- 작은 기능은 View, state owner, Repository 구현 등 필요한 파일만으로 시작한다.
- business invariant, UI orchestration, external I/O가 서로 다른 이유로 변경될 때만 계층을 분리한다.
- widget은 presentation edge에, 순수 entity·value object·rule은 framework-free domain module에 둔다.
- HTTP, storage, platform channel, notification, analytics SDK는 infrastructure edge에 둔다.
- 여러 repository를 조정하는 실제 business flow가 있을 때만 application use case를 둔다.
- ProviderScope override와 app startup에서 dependency를 조립한다.
- `shared`에는 안정된 의미와 계약을 가진 domain-neutral widget·utility만 승격한다.
- 전역 `widgets`, `services`, `models`, `providers`가 기능 소유권 없는 잡동사니 폴더가 되지 않게 한다.

## 그린필드 아키텍처

그린필드의 기본 후보는 기능 중심 MVVM에 현재 stable Riverpod의 Notifier API 모델을 필요한 범위만 결합하는 구조다. 설계 명세의 Riverpod 3 기준은 API 모델을 뜻하며, 실제 도입 시 현재 공식 문서와 stable package를 확인한다.

| 책임 | 기본 위치 |
| --- | --- |
| rendering, layout, animation, input 전달 | View·Widget |
| 화면·기능의 UI state와 사용자 command | ViewModel 역할의 Notifier·AsyncNotifier |
| authoritative data 접근 | Repository |
| HTTP, file, storage, platform API | Service·Infrastructure adapter |
| 여러 repository를 조정하는 복잡한 business flow | 필요한 경우에만 Use Case |
| dependency assembly와 test replacement | app composition·Provider override |

다음을 기계적으로 만들지 않는다.

- 모든 작은 widget의 ViewModel
- 모든 feature의 비어 있는 Domain·Application·Infrastructure 폴더
- 단순 local toggle을 위한 immutable state class와 Notifier
- 구현 하나뿐이고 외부 경계 역할도 없는 interface
- 모든 async work를 모은 거대한 global Provider
- 별도 근거 없는 Riverpod과 BLoC의 혼용

## 기존 상태관리 체계 존중

기존 프로젝트가 BLoC, Cubit, Provider, ChangeNotifier, Riverpod 또는 자체 controller 체계를 사용하면 개인 선호로 전면 교체하지 않는다.

- event, state, dependency injection, test convention을 먼저 확인한다.
- 요청 기능의 owner와 현재 architecture가 일치하면 기존 체계 안에서 구현한다.
- giant state object, stale duplication, widget-level I/O, lifecycle leak 같은 실제 결함만 최소 범위로 고친다.
- BLoC의 명시적 event log, 엄격한 transition, 조직 표준이 가치가 있으면 그대로 사용한다.
- ChangeNotifier가 작고 응집된 기능을 올바르게 소유한다면 Riverpod migration을 만들지 않는다.
- migration이 필요해도 대상 feature와 compatibility bridge, rollback, test를 별도 계획으로 분리한다.

## 상태 도구 선택

가장 좁은 소유권부터 선택한다.

| 요구 | 기본 선택 | 승격 조건 |
| --- | --- | --- |
| 한 widget 안의 일시적 표현 상태 | `StatefulWidget` | 소비자나 생명주기가 실제로 넓어질 때 |
| immutable dependency·read-only computation | `Provider` | 명확한 dependency graph나 공유 계산이 있을 때 |
| user interaction으로 변하는 screen·feature state | `Notifier` | 여러 widget이나 화면이 같은 transition을 공유할 때 |
| async initialization·query·command state | `AsyncNotifier` 또는 read-only async Provider | retry, refresh, command orchestration 계약이 있을 때 |
| 장수명 app state | 제한된 app-scope owner | session처럼 앱 전체 생명주기가 실제로 필요할 때 |
| persisted state | Repository·storage boundary | 복원, schema, migration, account isolation이 필요할 때 |

- 계산 가능한 값을 state에 중복 저장하지 않는다.
- Provider 범위를 편의상 app 전체로 넓히지 않는다.
- widget이 state 객체를 직접 변경하지 않고 notifier의 의미 있는 method를 호출하게 한다.
- `setLoading`보다 `submitPayment`, `retryLoadingMethods`, `selectPaymentMethod`처럼 의도를 드러낸다.
- read-only Provider와 user-mutated state owner를 구분한다.
- provider family parameter, auto-dispose·keep-alive, override 범위를 feature 생명주기와 맞춘다.
- code generation은 기존 project consistency와 실제 반복 비용이 있을 때만 사용한다.

## View와 ViewModel·Notifier

- View는 rendering, layout, animation, 단순한 표시 분기, 사용자 event 전달에 집중시킨다.
- ViewModel·Notifier는 Repository 결과를 UI state로 변환하고 의미 있는 command를 제공하게 한다.
- 하나의 작은 widget마다 ViewModel을 만들지 말고 사용자 중심 screen 또는 feature 흐름 단위로 둔다.
- business invariant는 ViewModel이 아니라 Entity, Value Object 또는 Domain Service에 둔다.
- Repository implementation과 raw HTTP call을 Notifier에 섞지 않는다.
- public API는 최소한의 state와 command만 노출하고 mutable collection이나 internal controller를 노출하지 않는다.
- state는 가능한 한 immutable하게 유지하고 서로 배타적인 상태를 명시적으로 표현한다.
- ViewModel이 navigation 자체를 직접 수행할지, typed result를 View에 돌려줄지 기존 프로젝트의 boundary를 따르되 domain이 router를 알지 못하게 한다.
- context-dependent UI concern은 Widget에, testable feature decision은 state owner에 둔다.

## 비동기와 서버 상태

- 초기 loading, success, empty, previous data가 있는 refreshing, failure를 실제 UX에 맞게 구분한다.
- 독립 불리언으로 불가능한 상태 조합을 만들지 않는다. `AsyncValue` 또는 명시적 sealed state를 일관되게 사용한다.
- latest-wins search, duplicate-blocked submit, sequential write 중 concurrency policy를 정한다.
- 오래된 response가 최신 selection이나 query를 덮지 않게 request identity, cancellation, provider lifecycle을 사용한다.
- widget `build`나 `initState`에서 Repository 구현을 직접 호출해 UI state와 network lifecycle을 섞지 않는다.
- pull-to-refresh와 background refresh에서 previous data 보존 여부를 명시한다.
- mutation 후 authoritative repository/cache의 refresh·invalidation·local update 정책을 정한다.
- optimistic update는 rollback state, server rejection, concurrent edit 정책이 있을 때만 사용한다.
- non-idempotent command를 근거 없이 자동 재시도하지 않는다.
- network, validation, authentication·authorization, recoverable domain, unexpected error를 typed result로 구분한다.
- 사용자에게 raw exception이나 stack trace를 표시하지 않고 같은 오류를 여러 계층에서 중복 기록하지 않는다.

Flutter 생태계에는 하나의 cache library를 보편적 기본값으로 강제하지 않는다. 현재 Repository, HTTP client, Riverpod owner와 freshness 요구를 분석해 server state의 권위자를 하나로 정한다.

## 라우팅과 내비게이션

- 그린필드에서 routing이 실제 필요하면 `go_router`를 기본 후보로 사용한다.
- single-screen app에는 router를 미리 추가하지 않는다.
- 복잡한 route parameter와 tree에서 type safety의 가치가 확인되면 `go_router_builder`를 평가한다.
- path, query, deep link를 외부 입력으로 parsing·validation한다.
- route name·path 문자열을 화면 곳곳에서 조합하지 말고 typed parameter를 받는 경계를 둔다.
- not found, invalid parameter, redirect loop, unauthorized, error route를 명시한다.
- 인증 후 원래 목적지 복귀와 account switch 시 navigation reset을 정한다.
- bottom navigation과 nested branch의 state preservation, back behavior를 명시한다.
- 복원돼야 할 핵심 값을 route `extra` 같은 메모리 객체에만 두지 않는다.
- 공유·복원해야 하는 filter, selection, identifier는 path·query 또는 authoritative repository에서 복구하게 한다.
- navigation side effect의 owner를 정하고 build 중 실행하지 않는다.

## 폼과 편집 초안

- 일반 form은 기본 `Form`과 `TextFormField`로 시작한다.
- `TextEditingController`, `FocusNode`, form key는 가장 가까운 owner가 생성하고 dispose한다.
- 편집 draft와 표시 error는 form boundary가 소유하게 한다.
- field 수, cross-field dependency, lifecycle이 단순하면 별도 form package를 추가하지 않는다.
- multi-step, restorable draft, cross-screen edit flow는 명시적 Draft model과 feature-level state owner로 승격한다.
- domain invariant를 validator와 submit callback에 중복 복사하지 않는다.
- server가 판정하는 uniqueness, inventory, authorization을 client validator가 확정하지 않는다.
- field error, form-level error, network·authentication error를 구분한다.
- validation을 모든 key stroke마다 공격적으로 표시하지 않고 submit, blur, touched 상태를 고려한다.
- duplicate submit, cancel, retry, 성공 후 reset·유지·navigation 정책을 명시한다.
- 기존 프로젝트 표준이나 확인된 복잡성이 있을 때만 추가 form package를 도입한다.

## 외부 데이터와 코드 생성

- API response, local database·preferences, deep link, remote config, file, notification, platform channel을 외부 입력으로 취급한다.
- raw `Map<String, dynamic>`과 `dynamic`이 presentation·domain으로 퍼지지 않게 DTO parser에서 변환한다.
- Dart cast만으로 required field, enum, date, amount, identifier가 유효하다고 가정하지 않는다.
- unknown enum, missing field, malformed value의 failure behavior를 boundary에서 정한다.
- JSON serialization generator가 기존 프로젝트의 권위 있는 declaration을 파생하면 그 체계를 따른다.
- generated file을 직접 수정하지 않고 annotation·declaration·schema를 변경한다.
- `build_runner`나 Riverpod code generation은 중복 계약과 유지 비용을 실제로 줄일 때만 추가한다.
- typed route generation도 충분히 복잡한 route tree와 parameter contract가 있을 때만 사용한다.
- generate command와 generated diff를 source change와 함께 검증한다.

## 리소스 생명주기

- `TextEditingController`, `FocusNode`, `AnimationController`, `ScrollController`, stream subscription, timer의 owner를 명확히 한다.
- owner가 종료될 때 dispose·cancel한다.
- Provider auto-dispose·keep-alive 선택을 screen navigation과 background work의 실제 생명주기에 맞춘다.
- listener를 build마다 중복 등록하지 않는다.
- app lifecycle change에서 중단·재개해야 하는 camera, location, media, connection을 adapter contract로 다룬다.
- async callback이 widget disposal 뒤 context나 state를 사용하지 않게 한다.
- resource cleanup을 단순히 framework가 알아서 할 것이라고 가정하지 않는다.

## 의존성 조립

- HTTP client, Repository implementation, storage, analytics, notification, platform adapter를 app startup과 Provider override에서 조립한다.
- feature에는 필요한 작은 capability만 전달한다.
- Domain과 Application이 Flutter, Riverpod, HTTP package, shared preferences, analytics SDK를 import하지 않게 한다.
- 실제 external boundary나 test replacement가 필요할 때만 abstract interface를 만든다.
- 거대한 `ApiService`보다 `PaymentMethodRepository.loadAvailableMethods`처럼 feature가 요구하는 계약을 선호한다.
- mutable global singleton과 service locator를 편의상 도입하지 않는다.
- environment·platform 차이는 adapter와 composition root에서 해소한다.
- `Platform.isX` 조건을 공통 business flow에 흩뿌리지 않는다.
- conditional import나 platform implementation은 실제 지원 target이 있을 때만 만든다.

## 테스트

저장소의 기존 test structure와 package를 우선한다.

- domain rule은 Flutter binding 없이 가능한 빠른 Dart unit test로 검증한다.
- use case, Notifier, BLoC, ViewModel state transition은 제어 가능한 Repository 대역으로 검증한다.
- widget test는 보이는 text·semantics·control과 사용자 interaction을 검증한다.
- private field, internal method call count, framework implementation detail에 결합하지 않는다.
- loading, success, empty, failure, retry, duplicate submit, dispose 이후 callback을 검증한다.
- routing은 direct deep link, invalid parameter, back navigation, redirect를 검증한다.
- Provider override로 외부 응답과 clock·identifier 같은 nondeterministic dependency를 제어한다.
- bug fix에는 기존 실패를 재현하는 regression test를 추가한다.
- giant golden·snapshot으로 state behavior test를 대체하지 않는다. visual contract가 실제 요구일 때만 golden test를 사용한다.
- integration test는 payment, login, critical creation flow처럼 실패 비용이 큰 여정에 집중한다.

## 접근성

- platform-native 의미를 제공하는 기본 widget을 우선한다.
- custom control에 `Semantics`, accessible label, role, selected·enabled·error state를 제공한다.
- keyboard·switch·screen reader 등 적절한 대체 입력으로 핵심 흐름을 사용할 수 있게 한다.
- focus traversal과 dialog·route 전환의 focus 이동을 예측 가능하게 한다.
- loading 완료, save failure, form error처럼 시각적으로만 바뀌는 중요한 상태를 필요한 경우 알린다.
- 색상만으로 selection·success·error를 구분하지 않는다.
- touch target과 간격을 고려한다.
- text scaling, screen rotation, dynamic size에서 핵심 정보와 action이 사라지지 않게 한다.
- automated semantics test만으로 완료하지 말고 핵심 interaction을 검증한다.

## 성능

- `const` constructor, stable key, 좁은 Provider subscription처럼 저비용 구조 개선을 사용한다.
- state owner 전체가 아니라 실제 필요한 field만 관찰해 rebuild 범위를 제한한다.
- build 안에서 반복되는 큰 object 생성과 계산을 피한다.
- server state와 derived state를 복제해 rebuild를 늘리지 않는다.
- 긴 list는 실제 item 수와 frame·memory 지표를 확인하고 lazy builder, pagination을 선택한다.
- widget을 작게 쪼개면 무조건 빠르다고 가정하지 않는다.
- caching, selector tuning, keep-alive, image prefetch는 DevTools나 재현 가능한 지표가 있을 때 적용한다.
- controller와 image·stream resource의 memory cost와 release를 확인한다.

## 보안과 개인정보

- mobile binary에 포함한 secret, admin credential, 신뢰할 encryption key는 보호되지 않는다고 가정한다.
- obfuscation을 secret protection이나 reverse-engineering 방지 보장으로 취급하지 않는다.
- client-side route·button guard를 최종 authorization으로 간주하지 않는다. server가 최종 인가하게 한다.
- token과 민감 정보는 저장 필요성을 먼저 줄이고, 필요하면 platform에 맞는 protected storage를 사용한다.
- local storage·database 값은 외부 입력처럼 validate하고 account별 isolation, logout cleanup, retention을 정한다.
- token, password, 전체 request body, 불필요한 PII를 `debugPrint`, analytics, crash report, notification에 넣지 않는다.
- WebView content, external URL, deep link, file path의 scheme·host·origin·content trust boundary를 검증한다.
- permission은 기능에 필요한 최소 범위와 시점에 요청하고 거부·영구 거부 상태를 처리한다.
- platform channel과 plugin response도 신뢰되지 않은 boundary로 parsing한다.

## 국제화·관찰 가능성·오프라인

- 사용자 문구를 domain state나 error 판정 값으로 사용하지 않는다.
- date, number, currency는 locale-aware formatter로 표현한다.
- 실제 다국어 요구가 있을 때 Flutter localization 체계나 기존 프로젝트 도구를 사용하고 plural, missing translation, locale change를 검증한다.
- analytics event는 widget build나 lifecycle 횟수가 아니라 의미 있는 user action 또는 use case result에서 한 번 발생시킨다.
- event name과 property를 typed contract 한곳에서 관리하고 provider SDK를 infrastructure adapter 뒤에 둔다.
- 기본은 online-first다. cache가 있다는 이유로 local database를 authoritative model로 만들지 않는다.
- offline editing 요구가 있으면 command queue, resend order, idempotency, conflict, delete·restore, account isolation, encryption, app restart recovery를 별도 동기화 도메인으로 설계한다.

## 안티패턴과 교정 기준

| 신호 | 실제 위험 | 최소 교정 |
| --- | --- | --- |
| widget `build`에서 network·storage 호출 | 반복 side effect, race, test 난이도 | state owner의 command와 Repository boundary로 이동 |
| 하나의 app-global Notifier에 모든 feature state | owner·lifecycle 상실, 넓은 rebuild | feature별 owner와 app-scope state를 분류 |
| server data를 Notifier와 Repository cache에 복제 | stale data, 양방향 sync | 권위자를 하나로 정하고 표시 값은 파생 |
| 여러 loading·error boolean | impossible state combination | `AsyncValue` 또는 sealed state로 전환 |
| controller·subscription 미해제 | memory leak, disposal 이후 callback | owner와 dispose·cancel을 명시 |
| 단순 toggle도 Riverpod으로 승격 | ceremony, 생명주기 확대 | `StatefulWidget` local state로 축소 |
| 모든 feature에 ViewModel·UseCase·Repository interface | empty layer와 indirection | 실제 rule·orchestration·boundary가 있는 계층만 유지 |
| route `extra`에 복원 필수 값 저장 | deep link·process restore 실패 | path·query·Repository에서 복구 |
| raw `dynamic`·cast가 UI까지 전파 | runtime contract failure | DTO parser에서 typed model로 변환 |
| BLoC·Provider를 취향으로 Riverpod 전면 교체 | 큰 migration과 회귀 | 대상 feature의 실제 결함만 수정 |

교정이 현재 요청보다 광범위하면 즉시 전면 개편하지 말고 영향, migration boundary, compatibility와 별도 검증을 제안한다.

## 검증

프로젝트가 정의한 명령을 우선 사용하고 SDK channel이나 package manager를 임의로 바꾸지 않는다.

1. 변경한 Dart 파일에 format check를 수행한다.
2. `flutter analyze` 또는 저장소의 정적 분석 명령을 실행한다.
3. 변경된 behavior를 직접 검증하는 관련 unit·widget test를 실행한다.
4. routing, dependency wiring, generated code를 바꿨다면 관련 generation·integration 검증을 수행한다.
5. platform plugin이나 build 설정을 바꿨다면 실제 대상 Android·iOS build 또는 프로젝트가 정의한 smoke check를 실행한다.
6. 사용자 핵심 flow가 영향을 받으면 관련 integration test를 실행한다.
7. 실패 명령, 실패 원인, 실행하지 못한 플랫폼 검증과 남은 위험을 분리해 보고한다.

## 공식 기준 자료

버전별 API는 실행 시점에 다음 공식 자료와 설치된 package를 함께 확인한다.

- [Flutter: Guide to App Architecture](https://docs.flutter.dev/app-architecture/guide)
- [Flutter: Command Pattern](https://docs.flutter.dev/app-architecture/design-patterns/command)
- [Riverpod: Providers](https://riverpod.dev/docs/concepts2/providers)
- [go_router package](https://pub.dev/packages/go_router)
- [go_router_builder package](https://pub.dev/packages/go_router_builder)
- [Flutter: Build a Form with Validation](https://docs.flutter.dev/cookbook/forms/validation)
- [Flutter: Retrieve Text Input and Dispose Controllers](https://docs.flutter.dev/cookbook/forms/retrieve-input)
- [Flutter: Obfuscate Dart Code and Security Limitations](https://docs.flutter.dev/deployment/obfuscate)
- [OWASP Mobile Application Security Verification Standard](https://mas.owasp.org/MASVS/)
- [OWASP MASVS Storage](https://mas.owasp.org/MASVS/05-MASVS-STORAGE/)
