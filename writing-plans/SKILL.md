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

## 3. Plan Item Contract

각 작업 항목은 반드시 아래 계약을 따른다.

## [P{number}] {Task Name} - Status: {Pending|In Progress|Blocked|Done}

Purpose:

- 이 작업이 왜 필요한지 한 문장으로 설명한다.

Goal linkage:

- 어떤 Goal 또는 Success Criteria를 만족하는지 연결한다.

Dependencies:

- depends_on: [P0, P1, ...]
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

---

## 4. Anti-Vagueness Rules

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

## 5. Missing-Work Prevention

긴 작업이나 대용량 문서, 여러 모듈이 있는 작업은 반드시 누락 방지 전략을 포함한다.

포함할 것:

- 전체 범위 인벤토리 방식
- 청크 또는 모듈 분할 기준
- 각 청크/모듈의 순서 번호
- 처리 완료 여부 추적 방식
- 실패한 청크만 재시도하는 방법
- 최종 병합 방식
- 누락 검증 체크리스트

---

## 6. Context Ledger Requirement

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

## 7. Progressive Context / Skill Loading

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

## 8. Output Format

최종 출력은 반드시 아래 구조를 따른다.

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

## 6. Milestone Plan

위의 “Plan Item Contract” 형식으로 P0부터 작성한다.

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
- [ ] 모든 P-item이 dependency, risk, rollback, validation을 가진다.
- [ ] 모든 중요한 제약이 Scope Guard에 반영되었다.
- [ ] 누락 방지 전략이 있다.
- [ ] 회귀 매트릭스가 있다.
- [ ] 검증 명령 또는 체크가 있다.
- [ ] hidden reasoning을 노출하지 않는다.
- [ ] 불확실성은 Assumption/Open Question으로 분리했다.
- [ ] 바로 다음 작업자가 실행 가능한 수준이다.

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
