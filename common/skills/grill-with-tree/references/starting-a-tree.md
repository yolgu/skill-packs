# Starting a Tree

Read this in full whenever you create a new decision tree. Widening first costs time and tokens; do it by default anyway, because axes found late reopen decisions already made.

## Five steps

1. **Draft.** Derive first axes from the request and the materials. Put in the decisions the user already made, and look up facts yourself.
2. **Widen perspectives.** Run three strands together:
   - Yourself: derive concerns from the stakeholders, and perspectives from the concerns.
   - One agent: perspectives used in comparable prior cases on the web.
   - Another agent: perspectives from the project's materials and from this user's past sessions (how they answer, how they revised trees).

   Merge the three, group overlaps, and stop when a new strand yields no new perspective. Spawn and check the agents as [Subagents](subagents.md) describes; when agents are unavailable, run the strands yourself one after another.
3. **Organize and show the map.**
   - Group the perspectives into axes and prune only clear nonsense. Report what you pruned once in the reply, each with a one-line reason, and report merged items with where they went. Pruned items never enter the tree; if the user revives one, it becomes an open node.
   - Mark each axis as core or general on the map without asking.
   - Do not ask whether to keep axes: they hold decisions and are not decisions themselves. The user adds, removes, or reshapes axes whenever they like.
4. **Expand each axis.** Spawn one agent per axis to lay out candidate decisions, and check the results before they enter the tree.
5. **Decide each candidate.** Each remaining candidate becomes an open decision node, and its answer adopts it (`채택`, settled, then expanded beneath) or rejects it (`거절`, settled, with the reason). Ask them through the turn loop, inside axes first. Withdraw an axis when every candidate under it is rejected.

Write an axis that only groups decisions as `settled`, with one line on what it covers; the map shows it and the user can change it at any time. An axis whose own decision is a real choice stays `open` and is asked like any decision. IDs are given when candidates become nodes.

## Widening and descending

- Horizontal expansion widens perspectives and sibling decisions on one layer. Vertical expansion lays out sub-decisions beneath a decision.
- Widen and cut one layer at a time, and descend only through the branches that remain.
- Stop descending a branch once its decision is a single question that can be answered now. Expand beneath it after it is settled, the same way.

## Core and general axes

- A core axis carries the user's purpose; a general axis is resolved by common practice.
- Give core axes deep expansion, comparison, and research. Ask general axes briefly, recommending the best common practice.

## The first reply

1. Create the document in the shape under Tree document in SKILL.md, with the `현재 상태` block filled in, including `불러온 영역 스킬` for the domain skills loaded at creation.
2. Reply with what you delegated, the map, the pruned and merged notice, and then the first question block, chosen by the usual order. Do not ask for approval of the map.

<example>
선행 사례와 지난 세션 자료에서 관점을 찾는 일을 에이전트 둘에게, 축마다 후보 결정을 펼치는 일을 에이전트 다섯에게 맡겼습니다.

```text
사내 장비 대여 결정 트리
├─ A 대여 대상과 기간        핵심
├─ B 신청과 승인 흐름        핵심
├─ C 반납과 연체 처리        일반
├─ D 알림                    일반
└─ E 관리자 화면             일반
```

가지친 것: 대여료 경매(사내 무료 서비스라 맞지 않습니다).
합친 것: 연체 알림은 알림(D)에 합쳤습니다.
</example>
