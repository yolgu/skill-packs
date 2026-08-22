# 클라이언트 UI 코드 리뷰 기준

이 문서는 사용자가 명시적으로 리뷰를 요청했을 때만 읽는다. 리뷰는 읽기 전용이다. 사용자가 수정·적용까지 요청하지 않은 한 source, test, configuration, generated file을 변경하지 않는다.

## 목차

- [리뷰 목표와 범위](#리뷰-목표와-범위)
- [리뷰 절차](#리뷰-절차)
- [증거 기준](#증거-기준)
- [심각도](#심각도)
- [Finding 작성 계약](#finding-작성-계약)
- [결함과 취향 구분](#결함과-취향-구분)
- [상태 소유권 점검](#상태-소유권-점검)
- [경계와 데이터 흐름 점검](#경계와-데이터-흐름-점검)
- [비동기와 오류 점검](#비동기와-오류-점검)
- [컴포넌트·위젯 점검](#컴포넌트위젯-점검)
- [외부 데이터와 타입 점검](#외부-데이터와-타입-점검)
- [폼과 라우팅 점검](#폼과-라우팅-점검)
- [접근성 점검](#접근성-점검)
- [보안과 개인정보 점검](#보안과-개인정보-점검)
- [성능과 생명주기 점검](#성능과-생명주기-점검)
- [테스트와 검증 점검](#테스트와-검증-점검)
- [Finding이 없을 때](#finding이-없을-때)
- [최종 응답 형식](#최종-응답-형식)

## 리뷰 목표와 범위

- 사용자가 지정한 diff, feature, file, module을 우선 범위로 삼는다.
- 변경 코드 자체뿐 아니라 호출자, 권위 있는 type·schema·config, 주요 consumer, 관련 test를 추적한다.
- 현재 변경 때문에 새로 발생했거나 악화된 실제 결함을 우선한다.
- 기존 결함은 변경과 직접 연결되거나 심각한 위험을 명확히 드러낼 때만 별도 표시한다.
- 저장소 전체를 이상적인 architecture와 비교해 전면 재설계를 요구하지 않는다.
- 순수 style preference와 팀마다 합리적으로 다를 수 있는 선택은 finding으로 만들지 않는다.
- 리뷰 범위에서 확인할 수 없는 사항은 단정하지 않고 검증 공백으로 분리한다.

## 리뷰 절차

1. 사용자 요청, diff 또는 대상 파일과 완료 조건을 확인한다.
2. 대상 기술의 참조 문서를 읽고 현재 프로젝트의 manifest, lockfile, 설정을 확인한다.
3. 기능과 데이터 흐름을 설명하는 넓은 검색으로 시작한다.
4. 관련 symbol의 정의, 생성 지점, mutation, 모든 주요 consumer와 test를 추적한다.
5. 현재 상태의 권위 있는 owner와 외부 contract의 단일 진실 공급원을 식별한다.
6. 정상 경로뿐 아니라 loading, empty, failure, retry, duplicate action, navigation, cleanup을 추적한다.
7. 실제 사용자·데이터·보안 영향이 있는 후보만 남긴다.
8. 후보마다 재현 가능한 조건과 코드 근거를 독립적으로 확인한다.
9. severity를 영향과 발생 가능성으로 정한다.
10. finding을 심각도 순으로 작성하고, finding이 없으면 그 사실과 검증 공백을 보고한다.

첫 발견에서 멈추지 않는다. 같은 상태나 symbol을 다른 표현으로 검색하고 sibling implementation과 test convention을 확인해 누락과 오탐을 줄인다.

## 증거 기준

Finding에는 다음 증거가 있어야 한다.

- 실제 file과 가능한 한 좁은 line 또는 symbol
- 문제가 발생하는 입력, state, lifecycle, navigation 또는 concurrency 조건
- 현재 코드가 그 조건에서 실행되는 경로
- observable impact: 잘못된 UI, stale data, duplicate request, crash, leak, inaccessible action, privacy exposure 등
- 최소한의 수정 방향

다음만으로 finding을 만들지 않는다.

- “보통 이렇게 한다”는 일반론
- 저장소에서 사용하지 않는 library의 권장 방식
- 실제 호출되지 않는 dead code에 대한 추측성 production impact
- 재현 조건이 없는 성능 미세 최적화
- line count, folder name, pattern 이름만을 근거로 한 구조 비판
- 미래 요구를 가정한 abstraction 제안

코드를 실행하거나 test를 돌리지 못해도 정적 경로로 확실히 증명할 수 있으면 finding이 될 수 있다. 반대로 실행 결과만 있고 원인 경로를 설명할 수 없다면 진단 공백을 명시한다.

## 심각도

| 등급 | 기준 | 예시 |
| --- | --- | --- |
| P0 · 치명적 | 광범위한 사용자 피해, 민감 정보 노출, 데이터 손상, 핵심 기능 전면 중단이 즉시 발생 | secret 노출, 모든 사용자의 잘못된 계정 데이터 표시 |
| P1 · 높음 | 일반적인 조건에서 핵심 흐름 실패, 잘못된 mutation, authorization 착각, 반복 crash | 결제 중복 제출, stale response가 최신 선택을 덮음 |
| P2 · 중간 | 특정하지만 현실적인 조건에서 기능 오동작, 접근성 차단, resource leak, 복구 불가 상태 | deep link 복원 실패, controller 미해제로 반복 화면 진입 시 leak |
| P3 · 낮음 | 영향이 제한된 실제 결함 또는 유지보수 위험이 가까운 변경에서 오류를 유발 | 일부 error branch 누락, 의미 있는 test gap |

severity는 수정 난이도나 코드가 보기 싫은 정도가 아니라 사용자 영향, 데이터·보안 위험, 발생 가능성으로 정한다. 확신이 낮으면 등급을 올리지 말고 근거와 검증 공백을 명시한다.

## Finding 작성 계약

각 finding을 다음 구조로 작성한다.

```text
[P1] 짧고 명령형이 아닌 문제 제목
위치: path/to/file:line

어떤 조건에서 어떤 코드 경로가 실행되고, 무엇이 실제로 잘못되는지 한 문단으로 설명한다.
권위 있는 owner 또는 깨진 contract를 지목하고 사용자·데이터·운영 영향을 연결한다.
최소 수정 방향을 제시하되 전체 patch를 작성하지 않는다.
```

제목은 결과를 드러낸다. “상태관리 개선”, “리팩터링 필요”처럼 추상적으로 쓰지 않는다.

좋은 제목 예:

- `[P1] 오래된 검색 응답이 최신 필터 결과를 덮습니다`
- `[P2] 로그아웃 후 이전 계정의 query cache가 유지됩니다`
- `[P2] 키보드로 결제 수단을 선택할 수 없습니다`

본문은 한 finding에 한 원인과 한 수정 경계를 유지한다. 같은 root cause가 여러 line에 나타나면 대표 위치 하나에 묶는다. 서로 독립적으로 수정 가능한 문제는 분리한다.

## 결함과 취향 구분

다음 질문 중 하나에 구체적으로 답할 수 있어야 결함으로 취급한다.

- 잘못된 observable behavior는 무엇인가?
- 어떤 state combination이나 race가 실제로 가능한가?
- 어떤 source of truth가 충돌하는가?
- 어떤 external input이 검증 없이 내부 invariant를 깨는가?
- 어떤 사용자가 접근할 수 없는가?
- 어떤 secret·PII·authorization 경계가 노출되는가?
- 어떤 resource가 해제되지 않는가?
- 어떤 기존 public contract나 test expectation을 깨는가?

다음은 대개 취향 또는 제안이다.

- Redux와 Zustand 중 개인 선호
- BLoC와 Riverpod 중 개인 선호
- feature file을 몇 개로 나눌지에 대한 고정 숫자
- 무해한 naming 차이
- 실제 반복 contract가 없는 작은 duplication
- 측정되지 않은 memoization 제안
- 모든 기능에 Use Case·Repository interface를 추가하자는 요구

취향 차이를 finding처럼 severity와 함께 제시하지 않는다. 사용자에게 도움이 되면 finding 뒤의 “선택적 개선” 한두 문장으로 분리한다.

## 상태 소유권 점검

- 계산 가능한 값이 별도 mutable state로 저장되어 충돌하지 않는가?
- transient UI state가 app-global owner로 불필요하게 승격되지 않았는가?
- form draft가 form library, local state, global store에 중복되지 않았는가?
- share·refresh·back 복원 값이 URL과 store에 동시에 존재하지 않는가?
- server response가 query cache와 general global store에 복제되지 않았는가?
- persistence의 권위자가 storage repository인지, memory copy인지 불명확하지 않은가?
- account·session state의 생명주기와 logout cleanup이 정의되어 있는가?
- 여러 consumer가 state를 수정하면서 public mutable setter나 내부 collection을 직접 사용하지 않는가?
- owner, mutation API, lifecycle이 코드와 test에서 추적 가능한가?
- 복제가 있다면 authority, sync direction, conflict, expiration이 명확한가?

## 경계와 데이터 흐름 점검

- render·build가 network, storage, analytics side effect를 실행하지 않는가?
- user action이 intent-centered command로 연결되는가?
- business invariant가 component·widget·serializer·controller에 흩어지지 않았는가?
- Domain이 React, Flutter, HTTP, router, storage package에 의존하지 않는가?
- Use Case가 단순 forwarding layer가 아니라 실제 orchestration을 담당하는가?
- Repository가 persistence와 network boundary를 담당하고 business decision을 숨기지 않는가?
- API client, storage, analytics가 composition root에서 조립되는가?
- mutable singleton·service locator가 dependency와 test boundary를 숨기지 않는가?
- `shared` abstraction이 안정된 의미 없이 여러 feature를 결합하지 않는가?
- 기존 project pattern을 무시한 넓은 migration이 diff에 섞이지 않았는가?

## 비동기와 오류 점검

- initial, loading, success, empty, refreshing, failure가 필요한 수준으로 구분되는가?
- 독립 boolean이 impossible state combination을 허용하지 않는가?
- 겹친 request의 latest-wins, block, queue 정책이 있는가?
- stale response가 최신 state를 덮을 수 있는가?
- non-idempotent command가 자동 재시도로 중복 실행될 수 있는가?
- optimistic update에 rollback과 server rejection 처리가 있는가?
- unmount·dispose 뒤 callback이 state나 context를 사용하는가?
- network, validation, auth, domain, unexpected error가 하나의 문자열로 뭉개지지 않는가?
- 오류가 조용히 삼켜지거나 무관한 default로 바뀌지 않는가?
- 동일 오류가 여러 계층에서 중복 기록되지 않는가?
- 사용자에게 internal exception과 stack trace가 노출되지 않는가?

## 컴포넌트·위젯 점검

- 한 요소가 독립 state·lifecycle·async work를 과도하게 함께 소유하지 않는가?
- 분리된 child가 부모 구현 세부사항을 많은 props·callbacks로 그대로 전달받지 않는가?
- boolean flag 누적으로 여러 역할과 불가능한 조합이 생기지 않는가?
- shared primitive가 feature store, API client, route에 직접 의존하지 않는가?
- 도메인 의미가 다른 요소를 외형이 비슷하다는 이유로 공용화하지 않았는가?
- custom Hook·ViewModel·Notifier가 실제 orchestration 없이 pass-through wrapper가 되지 않았는가?
- UI component가 business rule이나 raw network parsing을 소유하지 않는가?
- 접근성 semantics와 interaction contract가 component boundary에 포함되는가?

파일 길이만으로 giant component finding을 만들지 않는다. 서로 다른 변경 이유, state owner, side effect, test contract를 근거로 든다.

## 외부 데이터와 타입 점검

- API success·error response가 runtime parsing되는가?
- URL, deep link, local storage, environment, remote config, file, notification, platform channel이 검증되는가?
- TypeScript assertion, Dart cast, `any`, `dynamic`, raw map이 내부로 퍼지지 않는가?
- missing field, unknown enum, malformed date·amount·identifier가 명시적으로 처리되는가?
- schema, type, validator가 서로 중복돼 drift하지 않는가?
- generated file을 직접 수정하지 않았는가?
- validation failure가 빈 값이나 generic error로 조용히 변환되지 않는가?
- trusted internal flow에 불필요한 중복 null check가 business logic을 흐리지 않는가?

## 폼과 라우팅 점검

- 편집 draft, client guidance, domain rule, server validation의 owner가 분리되는가?
- submit 중 duplicate action과 retry가 안전한가?
- server field error와 form-level error가 구분되는가?
- multi-step draft의 persistence, expiration, restoration이 정의되는가?
- URL·route parameter parsing과 canonical serialization이 한곳에 있는가?
- 복원 필수 state가 memory-only route extra에 숨겨지지 않는가?
- direct entry, refresh, back, deep link, not found, unauthorized가 동작하는가?
- 인증 후 원래 목적지 복귀와 account switch reset이 올바른가?
- path 문자열이 여러 호출부에서 불일치하게 조립되지 않는가?

## 접근성 점검

- semantic HTML 또는 Flutter 기본 semantics를 사용할 수 있는데 custom control을 만들지 않았는가?
- interactive control의 이름, 역할, 현재 state, error relation이 보조 기술에 제공되는가?
- keyboard 또는 적절한 대체 입력으로 핵심 action을 수행할 수 있는가?
- focus order, modal open·close, route transition의 focus가 예측 가능한가?
- loading, save failure, form error 같은 중요한 비시각 상태가 필요한 경우 전달되는가?
- 색상만으로 selection·success·error를 구분하지 않는가?
- touch target과 spacing이 사용을 방해하지 않는가?
- text scaling, rotation, dynamic size에서 핵심 정보와 action이 사라지지 않는가?
- 자동 검사만 통과하고 실제 interaction flow가 막히지 않는가?

접근성 finding은 “ARIA 추가” 같은 처방보다 어떤 사용자가 어떤 행동을 완료할 수 없는지 설명한다.

## 보안과 개인정보 점검

- Vite client env, web bundle, mobile binary에 secret·admin credential이 포함되지 않는가?
- client route guard와 UI 숨김을 최종 authorization으로 사용하지 않는가?
- local storage·database의 민감 정보 저장 필요성과 보호 방식이 타당한가?
- logout·account switch에서 사용자별 cache와 민감 state가 폐기되는가?
- log, analytics, error report, notification에 token, password, 전체 request body, PII가 노출되지 않는가?
- raw HTML·WebView content의 source와 sanitization contract가 명확한가?
- external URL, redirect, deep link, file path의 scheme·host·origin이 검증되는가?
- mobile permission을 필요한 최소 범위와 시점에 요청하는가?
- obfuscation을 secret 보호로 오해하지 않는가?
- frontend-only finding을 backend security 전체 해결로 과장하지 않는가?

## 성능과 생명주기 점검

- list key가 stable domain identifier인가?
- state subscription이 실제 소비 범위보다 넓지 않은가?
- global update가 불필요하게 전체 화면을 render·rebuild하는가?
- render·build에서 반복되는 무거운 계산·객체 생성·side effect가 있는가?
- controller, listener, stream, timer, animation, request가 owner 종료 때 정리되는가?
- 대형 list·image·route resource가 실제 사용 시점과 memory cost를 고려하는가?
- 성능 finding에 재현 조건, 규모, profiler·metric 또는 명백한 complexity 근거가 있는가?
- memoization·caching 제안의 복잡성 비용보다 실제 효과가 큰가?

측정 근거 없는 미세 최적화는 finding으로 만들지 않는다. 다만 render·build side effect나 무한 loop처럼 구조상 확실한 문제는 측정 없이도 결함이다.

## 테스트와 검증 점검

- 변경된 domain rule이 domain test로 잠겼는가?
- state transition과 concurrency branch가 observable behavior로 검증되는가?
- component·widget test가 사용자 interaction과 결과를 검증하는가?
- loading, empty, failure, retry, duplicate submission 같은 실제 branch가 빠지지 않았는가?
- bug fix에 regression test가 있는가?
- routing과 dependency wiring 변경에 integration coverage가 있는가?
- test가 private state, method call count, giant snapshot에 과도하게 결합하지 않는가?
- repository가 정의한 typecheck, lint, analysis, test가 실제로 실행 가능한가?
- flaky timing, real network, global state leakage가 test 신뢰도를 해치지 않는가?

단순히 test가 없다는 이유만으로 항상 finding을 만들지 않는다. 현재 변경의 실패 가능성과 비용이 높고 기존 test convention으로 잠글 수 있을 때 구체적인 누락 branch를 지목한다.

## Finding이 없을 때

확인된 actionable finding이 없으면 명확히 그렇게 말한다. 억지로 사소한 취향을 finding으로 만들지 않는다.

다음은 함께 보고할 수 있다.

- 검토한 범위
- 실행한 test·typecheck·lint·analysis
- 실행하지 못한 검증과 이유
- 확인하지 못한 platform, runtime, backend contract
- 낮은 확신의 비차단적 관찰 한두 개

“문제 없음”을 모든 behavior의 완전한 보증처럼 표현하지 않는다. 검토 범위와 검증 공백을 연결한다.

## 최종 응답 형식

1. Finding을 심각도 순으로 먼저 제시한다.
2. 각 finding에 정확한 file·line, 조건, impact, 최소 수정 방향을 포함한다.
3. 질문이나 전제가 있으면 finding 뒤에 짧게 둔다.
4. 마지막에 검토 범위와 검증 상태를 간결하게 요약한다.
5. finding이 없으면 “확인된 결함 없음”을 먼저 말하고 남은 검증 공백을 설명한다.
6. 사용자가 patch를 요청하지 않았다면 코드나 파일을 수정하지 않는다.

리뷰 결과가 길어져도 같은 root cause를 반복하지 않는다. 사용자가 우선순위를 바로 판단할 수 있도록 실제 영향과 증거를 중심으로 작성한다.
