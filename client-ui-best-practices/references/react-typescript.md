# React + TypeScript 실행 기준

이 문서는 Vite + React + TypeScript가 실제 작업 대상일 때만 읽는다. 공통 상태 소유권, 필수 계약, 요청 모드와 최소 변경 원칙은 상위 `SKILL.md`를 단일 진실 공급원으로 사용하고, 여기서는 React 생태계에 필요한 판단만 구체화한다.

## 목차

- [프로젝트 분석](#프로젝트-분석)
- [기능 구조와 의존 방향](#기능-구조와-의존-방향)
- [상태 도구 선택](#상태-도구-선택)
- [컴포넌트와 Hook](#컴포넌트와-hook)
- [Effect와 외부 동기화](#effect와-외부-동기화)
- [서버 상태](#서버-상태)
- [라우팅과 URL 상태](#라우팅과-url-상태)
- [폼과 런타임 검증](#폼과-런타임-검증)
- [비동기와 오류](#비동기와-오류)
- [의존성 조립](#의존성-조립)
- [테스트](#테스트)
- [접근성](#접근성)
- [성능](#성능)
- [보안과 개인정보](#보안과-개인정보)
- [국제화·관찰 가능성·오프라인](#국제화관찰-가능성오프라인)
- [코드 생성과 버전](#코드-생성과-버전)
- [안티패턴과 교정 기준](#안티패턴과-교정-기준)
- [검증](#검증)
- [공식 기준 자료](#공식-기준-자료)

## 프로젝트 분석

다음 순서로 현재 계약을 확인한다.

1. `package.json`의 scripts, dependencies, devDependencies와 package manager lockfile을 읽는다.
2. Vite 설정, `tsconfig`, lint·format 설정, test 설정, environment 접근 지점을 확인한다.
3. router, query/cache, state store, form, validation, API client, serialization 도구의 선언뿐 아니라 실제 import와 사용처를 찾는다.
4. `src`의 feature 경계, app composition root, shared module, import direction과 alias를 확인한다.
5. 대상 상태가 생성·변경·파생·직렬화·폐기되는 모든 주요 위치와 관련 테스트를 추적한다.
6. API schema, generated type, runtime schema, DTO, domain type 중 권위 있는 선언을 식별한다.
7. 기존 package script로 관련 test, typecheck, lint, build를 어떻게 실행하는지 확인한다.

dependency가 설치되어 있다는 사실만으로 현재 기능의 표준이라고 단정하지 않는다. 사용되지 않는 package, migration 중인 이중 체계, test 전용 dependency를 구분한다.

## 기능 구조와 의존 방향

기본은 기능 중심 수직 분할이다.

```text
src/
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

- 작은 기능은 응집된 파일 몇 개로 시작한다.
- 실제 비즈니스 규칙, 외부 I/O, 화면 orchestration이 서로 다른 이유로 변경될 때만 계층을 분리한다.
- React component와 Hook은 `presentation`에, 순수 domain rule은 framework-free module에 둔다.
- fetch implementation, browser storage, analytics SDK는 infrastructure edge에 둔다.
- 여러 repository를 조정하는 실제 흐름이 있을 때만 application use case를 둔다.
- 전체 provider·router·adapter는 `app` composition boundary에서 조립한다.
- `shared`에는 안정된 의미와 계약을 가진 domain-neutral primitive만 승격한다.
- 전역 `components`, `hooks`, `services`, `models`가 기능 소유권 없는 잡동사니 폴더가 되지 않게 한다.

## 상태 도구 선택

그린필드에서 가장 좁은 소유권부터 선택한다.

| 요구 | 기본 선택 | 승격 조건 |
| --- | --- | --- |
| 한 component의 일시적 UI 상태 | `useState` | 소비자나 생명주기가 실제로 넓어질 때 |
| 여러 값이 함께 전이하는 local·feature 상태 | `useReducer` | 전이가 복잡하고 명시적 event가 이해를 돕는 경우 |
| 가까운 component 간 공유 | closest common owner로 lifting | prop 전달이 아니라 소유권 자체가 더 넓을 때 |
| 변경 빈도가 낮은 app dependency·setting | 제한된 `Context` | 소비 범위와 update frequency가 app 수명과 맞을 때 |
| 원격 데이터와 freshness | 기존 query/cache 도구, 그린필드의 비단순 앱은 TanStack Query | 서버 상태 계약이 실제로 있을 때 |
| 여러 feature가 수정하는 장수명 client state | 기존 store, 필요하면 Zustand·Redux Toolkit 평가 | 독립 소비자, 추적할 event sequence, undo·audit·offline queue 등이 있을 때 |

- 계산 가능한 값은 render 중 파생하고 별도 state에 저장하지 않는다.
- `Context`, Zustand, Redux Toolkit, TanStack Query를 그린필드라는 이유만으로 모두 설치하지 않는다.
- 기존 Redux Toolkit 또는 Zustand가 있으면 현재 slice·store·middleware·selector 관례를 확인하고 필요한 범위에서 사용한다.
- server response를 global client store에 복제하지 않는다.
- form library state를 `useState`나 global store에 다시 복제하지 않는다.
- 전역 state를 도입할 때 owner, mutation API, persistence, cleanup, account isolation을 명시한다.

## 컴포넌트와 Hook

- component는 rendering, composition, 접근성 구조, 사용자 intent 전달에 집중시킨다.
- 상태와 effect의 owner가 component 경계와 일치하게 한다.
- independent lifecycle, async work, error handling, behavior test가 있으면 분리를 검토한다.
- 한 번 쓰이는 짧은 markup을 숨기거나 파일 길이를 맞추기 위해 분리하지 않는다.
- boolean prop가 역할을 계속 추가하면 명시적 variant나 composition으로 책임을 분리한다.
- domain-neutral primitive와 domain-specific component의 소유권을 구분한다.
- custom Hook은 반복되는 stateful behavior 또는 복잡한 UI orchestration을 캡슐화할 때만 만든다.
- Hook 이름과 반환 API가 `useCheckoutSubmission`, `retryPayment`처럼 기능 의도를 드러내게 한다.
- public mutable setter와 내부 state 객체 전체를 반환하지 말고 최소한의 값과 의미 있는 action을 제공한다.
- Hook을 domain service처럼 사용하지 않는다. framework-free business invariant는 domain module에 둔다.
- React의 함수 component 관례를 OOP 요구 때문에 class component로 바꾸지 않는다.

## Effect와 외부 동기화

Effect는 React 바깥의 시스템과 동기화할 때 사용한다.

적합한 대상:

- DOM 또는 third-party widget lifecycle
- browser event·subscription
- timer, connection, media, imperative API
- 현재 router·query 도구로 표현되지 않는 외부 resource synchronization

부적합한 대상:

- props와 state에서 파생 가능한 값을 다시 state로 설정
- click·submit 같은 사용자 action의 우회 실행
- API response를 다른 store에 복사해 맞추기
- mount마다 query library와 중복 fetch
- 서로의 state를 감시하며 양방향 동기화하는 Effect 체인

Effect가 필요하면 setup과 cleanup을 같은 외부 contract로 다루고 dependency를 실제로 사용하는 값과 일치시킨다. async response가 순서를 바꿀 수 있으면 abort, request identity 또는 query 도구의 cancellation을 사용해 stale result가 최신 상태를 덮지 않게 한다.

## 서버 상태

기존 query/cache 도구가 있으면 그 도구의 owner model을 따른다. 비단순 server-backed 그린필드에서는 TanStack Query를 기본 후보로 평가한다.

- query key를 feature의 식별자, filter, pagination contract와 일치시킨다.
- query function은 typed API boundary를 호출하고 외부 response를 runtime parsing한 결과만 반환하게 한다.
- freshness, stale time, garbage collection, retry를 데이터 특성과 사용자 비용에 맞춘다.
- 초기 loading, empty, failure, previous data가 있는 refreshing을 UI에서 구분한다.
- mutation 후 관련 query invalidation 또는 권위 있는 cache update 중 하나를 의식적으로 선택한다.
- optimistic update는 rollback snapshot, server rejection, concurrent mutation policy가 있을 때만 사용한다.
- non-idempotent mutation을 근거 없이 자동 재시도하지 않는다.
- route loader를 parameter validation과 prefetch에 사용할 수 있지만 loader와 query cache가 독립된 server-state owner가 되지 않게 한다.
- component lifecycle callback과 Effect에서 같은 endpoint를 중복 호출하지 않는다.
- server state를 Zustand, Redux slice, Context, local state로 옮겨 “전역화”하지 않는다.

단순 일회성 request에서 query dependency의 비용이 더 크면 기존 API abstraction과 명시적 async state를 사용할 수 있다. 선택 이유를 실제 invalidation, sharing, caching 요구로 설명한다.

## 라우팅과 URL 상태

- 그린필드 Vite SPA에 routing이 실제 필요하면 React Router Data Mode와 `createBrowserRouter`를 기본 후보로 사용한다.
- single-screen app에는 router를 미리 추가하지 않는다.
- 검색어, filter, sort, page, 의미 있는 tab처럼 공유·복원할 값은 path 또는 query parameter가 소유하게 한다.
- path·query를 외부 입력으로 파싱하고 default, invalid value, canonical serialization을 한 module에서 관리한다.
- 동일한 값을 URL과 store에 함께 저장하지 않는다.
- 연속 입력 같은 변경은 history `replace`, 의미 있는 navigation은 `push`가 적합한지 구분한다.
- 전체 route tree는 app boundary에서 조립하고 feature route definition은 feature 가까이에 둘 수 있다.
- not found, invalid parameter, unauthorized, error route와 인증 후 원래 목적지 복귀를 명시한다.
- 직접 링크와 뒤로 가기의 대상인 modal·detail panel은 route 모델을 검토한다.
- 문자열 path를 여러 component에서 직접 조합하지 말고 typed parameter를 받는 route 생성 경계를 둔다.

## 폼과 런타임 검증

- field가 적고 dependency가 단순한 form은 native `<form>`과 React 기본 state로 시작한다.
- field array, conditional field, multi-step, 복잡한 error·performance 요구가 있으면 기존 도구를 따르며 그린필드 후보로 React Hook Form을 평가한다.
- 외부 구조의 runtime validation이 필요하면 기존 schema 도구를 따르며 그린필드 후보로 Zod를 평가한다.
- installed version과 공식 문서에서 현재 API를 확인하고 특정 major version을 기계적으로 강제하지 않는다.
- OpenAPI·GraphQL 등 권위 있는 schema에서 validator와 type을 생성할 수 있으면 수동 Zod schema와 TypeScript type의 중복을 피한다.
- 편집 draft와 표시 error는 form이 소유하게 한다.
- domain invariant는 domain object 또는 use case가 소유하게 하고 form schema에 복사하지 않는다.
- uniqueness, inventory처럼 server가 판정할 rule을 client가 확정하지 않는다.
- field error, form-level error, authentication·authorization error를 구분한다.
- submit 중 duplicate request, cancel, retry, 성공 후 reset·유지·navigation 정책을 명시한다.
- API, local storage, URL, environment variable은 `as SomeType`만으로 신뢰하지 않고 parser에서 internal DTO나 domain type으로 변환한다.
- validation failure를 조용히 빈 값으로 바꾸지 말고 사용자 입력 오류와 계약 오류를 구분한다.

## 비동기와 오류

- 중요한 흐름은 discriminated union이나 query 도구의 배타적인 상태 모델로 표현한다.
- `isLoading`, `isSuccess`, `hasError` 불리언을 독립적으로 관리해 불가능한 조합을 만들지 않는다.
- recoverable domain error, authentication·authorization, network, validation, unexpected programming error를 typed boundary에서 구분한다.
- 사용자 메시지에 raw exception, stack trace, backend 내부 문구를 노출하지 않는다.
- feature가 복구 가능한 오류는 feature boundary에서 처리하고, 예상하지 못한 render 오류는 적절한 route·screen error boundary로 전달한다.
- 같은 오류를 API client, Hook, component에서 반복 기록하지 않는다.
- duplicate submit, latest-wins search, sequential write처럼 concurrency policy를 이름과 테스트로 드러낸다.

## 의존성 조립

- API client, storage, analytics, error reporting, browser API adapter는 app composition root에서 조립한다.
- feature에는 사용하는 작은 capability만 전달한다.
- `Context`는 dependency 전달에 사용할 수 있지만 변경이 잦은 모든 state의 기본 store로 사용하지 않는다.
- domain과 application code가 React, fetch library, local storage, analytics SDK를 import하지 않게 한다.
- 실제 외부 boundary나 test replacement가 필요할 때만 interface를 만든다.
- 거대한 `ApiService`보다 `OrderRepository.cancel`, `ProductSearchRepository.search`처럼 feature가 요구하는 계약을 선호한다.
- environment 차이는 composition root에서 해소하고 component 안의 조건문으로 퍼뜨리지 않는다.

## 테스트

저장소의 기존 test runner와 library를 우선한다.

- domain rule은 React 없이 빠르게 테스트한다.
- reducer, use case, state transition은 input과 observable output으로 검증한다.
- component test는 role, accessible name, visible content, user interaction을 사용한다.
- internal Hook call count, private state, component implementation detail에 결합하지 않는다.
- API는 controllable boundary로 success, empty, validation failure, network failure, retry를 검증한다.
- routing은 invalid parameter, direct entry, back navigation, authorization result를 검증한다.
- bug fix에는 기존 실패를 재현하는 regression test를 추가한다.
- giant snapshot으로 behavior test를 대체하지 않는다.
- E2E는 login, payment, critical creation flow처럼 실패 비용이 큰 여정에 한정한다.

## 접근성

- `button`, `a`, `input`, `select`, heading, landmark 같은 semantic HTML을 우선한다.
- native semantics로 해결할 수 없는 경우에만 ARIA를 사용한다.
- control에 accessible name, 현재 state, validation error와 설명 관계를 제공한다.
- keyboard로 핵심 action, menu, dialog, form을 사용할 수 있게 한다.
- modal·menu가 열릴 때 focus를 이동하고 닫힐 때 합리적인 trigger로 복원한다.
- loading 완료, save failure, form error처럼 시각적으로만 변하는 중요한 상태를 필요한 경우 알린다.
- 색상만으로 selection·success·error를 구분하지 않는다.
- custom interactive element를 만들기 전에 native control로 해결 가능한지 확인한다.
- automated accessibility 검사만으로 완료하지 말고 핵심 keyboard·focus flow를 검증한다.

## 성능

- list key에는 index나 임의 생성 값 대신 stable domain identifier를 사용한다.
- Context와 external store의 subscription 범위를 실제 소비 component로 제한한다.
- server state와 derived state를 복제해 render를 늘리지 않는다.
- render 중 반복되는 명백히 큰 계산은 먼저 data flow를 단순화한다.
- `memo`, `useMemo`, `useCallback`을 기본 의식처럼 전역 적용하지 않는다.
- profiler 또는 재현 가능한 render count·latency 근거가 있을 때 가장 큰 병목 하나를 수정하고 다시 측정한다.
- 대형 list의 virtualization, pagination, lazy loading, prefetch는 실제 데이터 크기와 interaction을 근거로 선택한다.
- memoization이 stale closure, dependency confusion, API complexity를 만드는 비용을 함께 평가한다.

## 보안과 개인정보

- `VITE_`로 노출한 environment variable은 client bundle에 포함되는 공개 값으로 취급한다.
- secret key, admin credential, 신뢰할 encryption key를 source, bundle, sourcemap, client storage에 넣지 않는다.
- route guard와 숨긴 button을 최종 authorization으로 간주하지 않는다. server가 최종 인가하게 한다.
- local storage, session storage, IndexedDB의 값은 외부 입력처럼 validate하고 사용자별 data isolation과 logout cleanup을 정한다.
- raw HTML은 content source와 sanitization contract가 명확할 때만 사용한다.
- external link, redirect destination, deep link, pasted structured content를 검증한다.
- token, password, 전체 request body, 불필요한 PII를 console, analytics, error report에 기록하지 않는다.
- third-party script와 SDK를 추가할 때 데이터 수집 범위와 사용자 동의 요구를 확인한다.

## 국제화·관찰 가능성·오프라인

- 사용자 문구를 domain state나 error 판정 값으로 사용하지 않는다.
- date, number, currency는 locale-aware formatter로 표현한다.
- 실제 다국어 요구가 있을 때 기존 i18n 체계를 사용하고 message semantics, plural, missing translation을 검증한다.
- analytics event는 render나 Effect 횟수가 아니라 의미 있는 user action 또는 use case result에서 한 번 발생시킨다.
- event name과 property를 typed contract 한곳에서 관리하고 provider SDK를 infrastructure adapter 뒤에 둔다.
- 기본은 online-first다. query cache를 offline write model로 취급하지 않는다.
- offline editing 요구가 있으면 queue, idempotency, conflict, rollback, account switch를 별도 설계한다.

## 코드 생성과 버전

- API schema가 권위자이면 generated client, DTO, runtime validator를 검토한다.
- generated output을 직접 수정하지 않고 schema·generator config를 변경한다.
- generate command와 generated diff 검증을 프로젝트 script에 맞춰 수행한다.
- 현재 manifest와 lockfile을 우선하고 dependency 추가나 API 선택 시 공식 문서를 확인한다.
- 최신이라는 이유만으로 package를 upgrade하거나 Redux·router·query major migration을 함께 수행하지 않는다.

## 안티패턴과 교정 기준

| 신호 | 실제 위험 | 최소 교정 |
| --- | --- | --- |
| API response를 Zustand·Context·local state에 복사 | owner 불명확, stale data, sync Effect | query/cache를 owner로 복원하고 표시 값은 파생 |
| Effect가 state를 계산해 다시 set | extra render, impossible intermediate state | render 또는 selector에서 파생 |
| 여러 Effect가 서로의 state를 감시 | 순서 의존, loop, race | 사용자 intent 하나와 명시적 transition으로 통합 |
| 모든 state를 Context에 저장 | 넓은 subscription, owner 상실 | local·URL·form·server state로 재분류 |
| 파일이 길다는 이유로 component 분리 | 무의미한 indirection | 독립 책임·state·lifecycle이 있을 때만 분리 |
| 공용 component에 boolean prop 누적 | 여러 역할과 조합 폭발 | explicit variant 또는 composition으로 분리 |
| `as` assertion으로 API 신뢰 | runtime contract failure | boundary parser와 typed error 추가 |
| route filter를 store에도 저장 | back·refresh 불일치 | URL을 owner로 정하고 parser를 중앙화 |
| 모든 component에 `memo` | 복잡성, stale dependency, 미미한 효과 | 측정된 병목만 최적화 |
| Redux가 있다는 이유로 전면 제거 | 넓은 migration과 회귀 | 대상 feature의 실제 ownership 결함만 수정 |

교정이 현재 요청보다 광범위하면 즉시 전면 개편하지 말고 영향, migration 경계, 별도 검증을 제안한다.

## 검증

프로젝트가 정의한 명령을 우선 사용하고 임의 package manager를 가정하지 않는다.

1. 변경된 behavior를 직접 검증하는 관련 test를 실행한다.
2. TypeScript typecheck를 실행한다.
3. lint와 format check를 실행한다.
4. route, dependency wiring, environment 또는 build contract를 바꿨다면 Vite build를 실행한다.
5. 사용자 핵심 flow가 영향을 받으면 관련 integration 또는 E2E를 실행한다.
6. 실패 명령, 실패 원인, 실행하지 못한 검증과 남은 위험을 분리해 보고한다.

## 공식 기준 자료

버전별 API는 실행 시점에 다음 공식 자료와 설치된 package를 함께 확인한다.

- [React: Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- [React: Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure)
- [React: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [React: Common Components and raw HTML safety](https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html)
- [Vite: Environment Variables and Modes](https://vite.dev/guide/env-and-mode)
- [TanStack Query: React Overview](https://tanstack.com/query/latest/docs/framework/react/overview)
- [React Router: Picking a Mode](https://reactrouter.com/start/modes)
- [React Router: Data Mode Routing](https://reactrouter.com/start/data/routing)
- [React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [Zod documentation](https://zod.dev/)
