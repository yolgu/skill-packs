---
name: writing-plans
description: Use only when Codex will actually implement a code or configuration change in the current task and needs a multi-step implementation plan before coding. Do not use for standalone plans, strategy, brainstorming, roadmaps, analysis, recommendations, or hypothetical future work that Codex will not implement as part of the same task.
---

# Writing Plans

## Overview

임무는 사용자의 요청을 단순한 할 일 목록으로 바꾸는 것이 아니라, 실제 팀·에이전트·개발자가 즉시 실행할 수 있는 최고급 계획서로 변환하는 것입니다.

다음 5가지 관점을 동시에 유지합니다.

1. Product Strategist: 왜 이 일을 하는지, 어떤 성공 기준을 만족해야 하는지 정의한다.
2. System Architect: 구조, 경계, 데이터 흐름, 의존성, 인터페이스를 설계한다.
3. Execution Lead: 작업을 단계별로 쪼개고 의존성, 우선순위, 병렬 가능성을 정한다.
4. QA / TDD Lead: 각 단계마다 검증 기준, 실패 확인, 통과 확인, 회귀 방지 방법을 붙인다.
5. Risk / Handoff Owner: 리스크, 롤백, 보안, 프라이버시, 운영 부작용, 다음 작업자 인수인계를 명시한다.

중요:

- 구체적인 구현 코드를 바로 작성하지 마라. 먼저 계획 품질을 극대화하라.
- 숨겨진 추론 과정은 출력하지 마라. 대신 판단 근거를 간결한 요약으로 제시하라.
- 불확실한 내용은 추측으로 확정하지 말고 “Assumption”, “Open Question”, “Revisit Trigger”로 분리하라.
- 계획은 멋있어 보이는 문서가 아니라 실행, 검증, 롤백, 인수인계가 가능한 계약서여야 한다.

---

# INPUT

사용자는 아래 형식 중 일부만 줄 수 있다. 비어 있는 항목은 합리적 기본값을 세우되, 중요한 불확실성은 명시하라.

<TASK>
사용자가 달성하려는 목표:
{{USER_TASK}}
</TASK>

<CONTEXT>
현재 상황, 기존 시도, 관련 파일, 참고 문서, 제약:
{{PROJECT_CONTEXT}}
</CONTEXT>

<STACK_OR_DOMAIN>
기술 스택, 도메인, 플랫폼, 언어, 도구:
{{STACK_OR_DOMAIN}}
</STACK_OR_DOMAIN>

<CONSTRAINTS>
시간, 비용, 보안, 정책, 품질, 배포, 호환성 제약:
{{CONSTRAINTS}}
</CONSTRAINTS>

<QUALITY_BAR>
사용자가 원하는 수준:
예: MVP, production-ready, enterprise-grade, research-grade, “20000억원 가치급”
{{QUALITY_BAR}}
</QUALITY_BAR>

---

# OPERATING PRINCIPLES

## 1. Context First

먼저 사용자의 입력에서 다음을 추출한다.

- 핵심 목표
- 현재 상태
- 명시된 요구사항
- 암묵적 요구사항
- 금지사항 / 비목표
- 품질 기준
- 관련 리소스, 파일, API, 시스템
- 외부 의존성
- 성공을 검증할 방법
- 사용자가 아직 결정하지 않은 중요한 변수

입력이 부족해도 바로 멈추지 마라.  
단, 다음 중 하나에 해당하면 “Blocking Question”을 최대 1개만 제시한다.

- 목표 자체가 상충한다.
- 실행 위치나 대상이 전혀 불명확하다.
- 보안상 위험한 행동이 필요할 수 있다.
- 계획의 방향이 완전히 달라질 수 있는 핵심 선택지가 있다.

그 외에는 합리적 가정을 세우고 계속 진행하라.

---

## 2. Three-Layer Plan Model

모든 계획은 다음 3개 층을 가져야 한다.

### Layer A: Strategic Plan

왜 하는가, 무엇이 성공인가, 무엇을 하지 않는가.

반드시 포함:

- Goal
- Non-goals
- Success criteria
- Stakeholders / users
- Constraints
- Assumptions
- Open questions

### Layer B: Architecture / System Plan

무엇이 어디에 속하고, 어떤 경계와 계약으로 움직이는가.

반드시 포함:

- Domain model or conceptual model
- System boundaries
- Public interfaces
- Data flow or state transitions
- File/module/resource mapping
- External dependencies
- Security/privacy considerations
- Failure behavior

### Layer C: Execution Plan

어떤 순서로, 누가, 무엇을, 어떻게 검증하며 진행하는가.

반드시 포함:

- Milestones
- Dependencies
- Parallelizable 여부
- Required skills
- Files/resources to create/modify/test
- Completion criteria
- TDD or validation steps
- Risk
- Rollback
- Verification commands/checks
- Handoff notes

---

## 3. Plan Bundle Contract

계획은 채팅 본문 하나로만 출력하지 않고, 하나의 master plan과 P-item별 독립 파일로 저장한다.

### Save location

저장 위치는 다음 우선순위로 정한다.

1. 사용자가 지정한 위치
2. 저장소에 이미 존재하는 호환 가능한 plan 문서 규칙
3. 기본값: `docs/plans/YYYY-MM-DD-<topic>/`

기본 구조:

```text
docs/plans/YYYY-MM-DD-<topic>/
|-- plan.md
`-- items/
    |-- P0.md
    |-- P1.md
    `-- ...
```

규칙:

- `<topic>`은 짧은 lowercase kebab-case로 작성한다.
- `P0`, `P1`, ... 식별자는 실행 순서가 아니라 안정적인 작업 ID다. 순서는 dependency로 표현한다.
- 파일명은 제목이 바뀌어도 링크가 깨지지 않도록 `P{number}.md`로 고정한다.
- 각 `items/P{number}.md`에는 정확히 하나의 P-item만 둔다.
- P-item을 추가하거나 제거할 때 기존 ID를 불필요하게 재번호화하지 않는다.

### Source of truth and references

- `plan.md`는 전체 계획의 진입점이며 Strategic Plan, Architecture / System Plan, milestone index, 전체 dependency diagram, regression matrix, side-effect review, 공통 verification, handoff를 소유한다.
- `items/P{number}.md`는 해당 작업의 상세 내용과 status, dependencies, files/resources, risk, rollback, completion criteria, TDD / validation steps의 Single Source of Truth다.
- `plan.md`의 milestone index는 모든 P-item을 상대 링크로 참조해야 한다. P-item 본문 전체를 `plan.md`에 복제하지 않는다.
- 각 P-item은 상단에서 `../plan.md`를 parent plan으로 참조하고, dependency가 있으면 같은 디렉토리의 해당 P-item 파일을 상대 링크로 참조한다.
- master의 dependency diagram과 regression matrix처럼 전체 조망을 위해 필요한 파생 정보는 허용하되, P-item 변경 시 같은 작업에서 동기화한다.
- 절대 경로, `file://` URI, 채팅 전용 참조를 문서 간 링크에 사용하지 않는다.
- 최종 응답에는 `plan.md` 링크와 생성된 P-item 개수만 간결하게 제시하고, 파일 본문 전체를 다시 붙여 넣지 않는다.

### Bundle creation order

1. 전체 범위를 인벤토리화하고 P-item 경계를 정한다.
2. 안정적인 P-ID와 dependency를 확정한다.
3. 각 `items/P{number}.md`를 작성한다.
4. 모든 P-item을 참조하는 `plan.md`를 작성한다.
5. 링크, ID, dependency, 누락 여부를 검증한다.

---

## 4. Plan Item Contract

각 작업 항목은 반드시 독립된 `items/P{number}.md` 파일에서 아래 계약을 따른다.

```markdown
# [P{number}] {Task Name}

Parent plan:

- [전체 계획](../plan.md)

Status:

- {Pending|In Progress|Blocked|Done}

Purpose:

- 이 작업이 왜 필요한지 한 문장으로 설명한다.

Goal linkage:

- 어떤 Goal 또는 Success Criteria를 만족하는지 연결한다.

Dependencies:

- depends_on: [] 또는 [[P0](P0.md), [P1](P1.md), ...]
- parallelizable: true/false

Required skills:

- [skill-1, skill-2, ...]

Boundary mapping:

- Public interface:
- Implementation boundary:
- Out-of-scope adjacent behavior:
- Regression scenarios:

Files / Resources:

- Create:
- Modify:
- Test:
- Delete:

Difficulty:

- 🟢 Low / 🟡 Medium / 🔴 High

Risk:

- 가장 큰 실패 가능성을 적는다.

Rollback:

- 이 작업이 실패했을 때 되돌리는 방법을 적는다.

Completion criteria:

- [ ] 측정 가능한 완료 조건 1
- [ ] 측정 가능한 완료 조건 2
- [ ] 측정 가능한 완료 조건 3

TDD / Validation steps:

1. Failing probe or failing test:
   - Command/check:
   - Expected before implementation:
2. Minimal implementation:
   - Action:
3. Passing verification:
   - Command/check:
   - Expected after implementation:
4. Regression lock:
   - 무엇이 다시 깨지지 않게 잠기는가?

Notes:

- 중요한 판단, 제한, 주의사항.
```

---

## 5. Anti-Vagueness Rules

다음 표현은 금지하거나 즉시 구체화하라.

금지:

- “구현한다”
- “연동한다”
- “최적화한다”
- “테스트한다”
- “보안 고려”
- “필요시”
- “나중에”

대체:

- 무엇을 생성/수정/삭제하는가
- 어느 파일/모듈/API/DB/도구가 관련되는가
- 어떤 입력과 출력이 있는가
- 어떤 명령이나 체크로 통과를 확인하는가
- 실패하면 어떤 상태가 되며 어떻게 복구하는가
- 지금 하지 않는 것은 무엇인가

---

## 6. Missing-Work Prevention

긴 작업이나 대용량 문서, 여러 모듈이 있는 작업은 반드시 누락 방지 전략을 포함한다.

포함할 것:

- 전체 범위 인벤토리 방식
- 청크 또는 모듈 분할 기준
- 각 청크/모듈의 순서 번호
- `plan.md`의 P-item 링크를 통해 각 파일의 처리 상태를 추적하는 방식
- 실패한 청크만 재시도하는 방법
- 최종 병합 방식
- 누락 검증 체크리스트

---

## 7. Context Ledger Requirement

장기 실행, 에이전트, 자동화, 플러그인, 다단계 구현 계획에는 반드시 관찰 가능한 상태 저장소를 설계한다.

포함할 것:

- state
- events
- context snapshot
- plan
- artifacts
- cancellation / resume state
- user intervention requests

규칙:

- 숨겨진 추론 과정은 저장하지 않는다.
- 저장되는 것은 관찰 가능한 이벤트, 요약, 도구 호출, 결과, 상태 변경뿐이다.
- 사용자가 중간에 “지금 어디까지 됐어?”라고 물으면 답할 수 있어야 한다.

---

## 8. Progressive Context / Skill Loading

사용 가능한 문맥이 많을 때는 전부 읽지 말고 점진적으로 로드한다.

우선순위:

1. 사용자가 이번 요청에서 직접 제공한 컨텍스트
2. 현재 작업 디렉토리 또는 현재 대화의 명시적 지시
3. 상위 범위의 정책/프로젝트 지시
4. 관련 skill catalog 또는 문서 목록
5. 실제 필요한 순간의 상세 문서 또는 SKILL.md

규칙:

- 모든 skill/document body를 무작정 읽지 않는다.
- 어떤 컨텍스트를 사용했는지 기록한다.
- 충돌하는 지시는 우선순위와 이유를 명시한다.

---

## 9. Output Format

최종 산출물은 반드시 `plan.md`와 P-item 파일들로 나눈다.

### Master file: `plan.md`

`plan.md`는 아래 구조를 따른다.

```markdown
# {Plan Title}

## 1. Executive Summary

- 한 문단으로 목표, 접근법, 핵심 리스크, 성공 기준을 요약한다.

## 2. Extracted Context

- User goal:
- Current situation:
- Constraints:
- Existing assets:
- Assumptions:
- Open questions:

## 3. Success Criteria

| Goal | Measure | Verification |
| ---- | ------- | ------------ |

## 4. Scope Guard

### In scope

- ...

### Out of scope

- ...

### Revisit triggers

- ...

## 5. Architecture / System Model

- Domain concepts:
- Components:
- Public interfaces:
- Data/state flow:
- Storage/artifacts:
- Security/privacy:

## 6. Milestone Index

| Item | Purpose | Depends on | Parallelizable |
| ---- | ------- | ---------- | -------------- |
| [P0 - {Task Name}](items/P0.md) | ... | - | true/false |
| [P1 - {Task Name}](items/P1.md) | ... | [P0](items/P0.md) | true/false |

모든 P-item을 빠짐없이 나열하되 상세 계약은 각 링크의 파일에만 작성한다.

## 7. Dependency Diagram

텍스트 다이어그램으로 표시한다.

예:
P0 -> P1
P1 -> P2
P1 -> P3
P2, P3 -> P4

## 8. Regression Matrix

| Scenario | Setup | Action | Expected result | Locked by |
| -------- | ----- | ------ | --------------- | --------- |

## 9. Side Effect Review

| Area | Risk | Mitigation | Verification |
| ---- | ---- | ---------- | ------------ |

## 10. Verification Commands / Checks

- Command/check:
  - Expected:

## 11. Handoff Context

- Current status:
- Key decisions:
- Watchouts:
- Next operator starts from:
- Do not do:

## 12. Self-Audit Before Final

아래 항목을 점검하고 부족한 부분을 보강한 뒤 최종 답변한다.

- [ ] 모든 Success Criteria가 검증 방법을 가진다.
- [ ] 모든 P-item이 독립된 `items/P{number}.md` 파일 하나에만 존재한다.
- [ ] `plan.md`가 모든 P-item을 상대 링크로 참조하고 P-item 본문을 중복하지 않는다.
- [ ] 모든 P-item이 parent plan, dependency, risk, rollback, validation을 가진다.
- [ ] 모든 P-ID가 유일하고 모든 dependency 링크가 실제 파일로 해석된다.
- [ ] orphan P-item과 끊어진 링크가 없다.
- [ ] 모든 중요한 제약이 Scope Guard에 반영되었다.
- [ ] 누락 방지 전략이 있다.
- [ ] 회귀 매트릭스가 있다.
- [ ] 검증 명령 또는 체크가 있다.
- [ ] hidden reasoning을 노출하지 않는다.
- [ ] 불확실성은 Assumption/Open Question으로 분리했다.
- [ ] 바로 다음 작업자가 실행 가능한 수준이다.
```

### P-item files: `items/P{number}.md`

- P0부터 각 작업을 위의 “Plan Item Contract” 형식으로 별도 파일에 작성한다.
- master에 없는 P-item 파일이나 파일이 없는 milestone 항목을 만들지 않는다.
- 공통 설명을 반복하지 말고 필요한 master section으로 링크한다.
- 작업 실행자는 `plan.md`를 먼저 읽은 뒤 실행할 P-item 파일을 읽는다고 가정한다.

---

# RESPONSE STYLE

- 한국어로 작성한다.
- 사용자가 원하지 않는 한 장황한 이론 설명을 하지 않는다.
- 계획서는 구체적이어야 하지만, 구현 코드는 요청받기 전까지 최소화한다.
- 판단이 필요한 부분은 단정하지 말고 “권장 기본값”과 “재검토 조건”으로 제시한다.
- 사용자가 “20000억원 가치급”을 요구하면, 과장된 마케팅 문구가 아니라 다음 기준을 만족하는 계획으로 해석한다.
  - 실행 가능성
  - 검증 가능성
  - 확장 가능성
  - 운영 가능성
  - 실패 복구 가능성
  - 인수인계 가능성
  - 보안/프라이버시 고려
  - 컨텍스트 추적 가능성
