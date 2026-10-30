---
name: grill-with-tree
description: Use only when the user directly invokes grill-with-tree, or when continuing an interview that is already running with this skill.
---

# Grill with Tree

Run a decision interview from the first map to the final consolidation, and keep every decision in a persistent decision tree document. Read `../grilling/SKILL.md` and follow it; this skill sets the question order, the tree, and the stages around the interview.

Conduct and record the interview. Do not carry out the plan being discussed.

## Stages

1. Start: draft, widen perspectives, show the map, expand each axis, then decide each candidate. Read [Starting a Tree](references/starting-a-tree.md) in full whenever you create a new tree.
2. Interview: the turn loop and the tree document below.
3. Split and graph: Read [Splitting and Graph View](references/splitting-and-graph.md) in full when a split signal appears or the user asks to see the tree as a graph.
4. Consolidation and after: see Finishing. Read [Changes After Consolidation](references/after-consolidation.md) in full when a decision that already has a design document changes.

Read [Subagents](references/subagents.md) in full before you spawn an agent for the interview and when an agent's result arrives. Read a stage reference again each time you enter its stage; compaction can drop it.

## Each turn

Go through these steps in order. Korean labels and phrases in this skill are literal: write them exactly as shown (see Labels and terms).

### 1. Reload what the turn needs

- When resuming, or when this skill, the base skill, or a recorded domain skill is no longer in context (for example after compaction), load it again before replying.
- When resuming, read the `현재 상태` block at the top of the tree first, then find open and blocked decisions by searching for their statuses.
- Load domain skills yourself when the tree is created, when a new axis opens, and when the topic changes. List what the interview decides (code in a language or framework, data, screens, contracts, module structure), pick the available skills whose descriptions own rules for those artifacts, load them the way the harness loads skills, and record them on the `불러온 영역 스킬` line. Load them even in a turn that writes no code: the recommendations decide what gets built, and the rule check in step 5 sees only loaded skills. When no skill fits, research best practice as step 5 describes.

### 2. Read the answer

- Decide which decisions the reply actually answers or changes. Separate explicit decisions, verified facts, and your own interpretation, and record them as `사용자 결정(...)`, as facts with their source, and as `모델의 해석(사용자 확인 전):`.
- A reply phrased as a question is never a decision, whatever it suggests.
  - Asking back: answer, add one line with the question and your answer to that node, keep its status, and present the same question again.
  - A counter-proposal or alternative in question form: restate it in its strongest form, compare it with your recommendation by the same criteria, say whether your recommendation changes and why, and present the same question again.
  - A request to recommend again or to research: research, then present the same question with the revised recommendation.
- Silence, your recommendation, and moving elsewhere are not agreement.
- When the answer directly settles another decision, leaving it no real choice, settle that one in the same turn: write `따라 정함(<date>): <decision> 결정에서` in its node and report it on the `이렇게 적었습니다:` line. When the answer only narrows another decision's candidates, keep that decision open and recommend from what remains.
- A parent's status follows its own decision only, never its children's.
- When a later decision would rest on a recorded `모델의 해석(사용자 확인 전):`, ask that interpretation as a decision question first.
- An item the user adds as a question, a counter-question, or a request to think about it ("생각해 봐") is wanted now: check it for overlap, add it, and ask it first; a question that was waiting is presented again later. An item the user only mentions is checked for overlap, added as an open node, and asked in the usual order.
- A request about how to run this interview ("이 인터뷰에서는 …") goes on a `진행 약속` line and holds until the interview ends. Save it to permanent memory only when the user asks for that. When it reads as a request to change this skill, ask that as a decision question.
- Treat messages that arrive while you work the same way, and choose the question again if the pending one changed.

### 3. Record and propagate

- Use four statuses: `open`, `blocked`, `settled`, `withdrawn`.
  - `blocked` holds only while a decision named on a `선행:` line is not settled; switch to `open` once all of them are. A prerequisite that applies only under a condition is written with its condition in the body and does not block. A missing fact does not block; find it yourself.
  - A decision asked and answered "no" is settled with `거절` and its reason. `withdrawn` is for a decision whose premise disappeared; keep the reason.
  - A decision moved out of this scope to later work is settled, with where it went.
- Only withdrawal propagates, and only downward: withdraw the descendants of a withdrawn parent with `부모 철회에 따름(<date>)`, and move a descendant that is still needed under its proper parent with `옮김(<date>): <old parent> → <new parent>`.
- When a decision changes:
  1. Keep the old decision in its node: write the new one on top and put `대체됨(<date>): <reason>` before the old one.
  2. Find what rests on it: run `impact <ID>`, which covers `선행:` lines, mentions, and children, and also check tables and prose that describe it without the ID.
  3. Reopen decisions whose premise actually changed, fix only the wording where only the wording is stale, and leave the rest. Report reopened decisions in one line before the next question.
- When a decision is made, handle the decisions that point to it the same way and switch the ones it unblocks to `open`. When it rules out candidates elsewhere ("no target date", "excluded from this scope", "no subagents"), add a line pointing to it under `지킬 조건`, search the whole tree once by its topic words for decisions it contradicts, and check every later recommendation against that list.
- Before creating a node, write in one sentence what it decides and compare it only with its parent and siblings. Do not create it when the parent already decided it (reopen the parent if that must change); merge it into a sibling that decides the same thing; write the boundary into both bodies when they partly overlap. Report the fix in one line.
- Delete a node only when it was created by mistake, such as a duplicate, has no children, nothing points to it (`impact`), and holds no decision record. Note the deletion in `세션 기록`.
- Edit in place. Create the document once, read the affected nodes and their boundaries before editing, change only the affected text and statuses, and never regenerate the document or a subtree or rebuild it from memory. Run `check` after editing; fix every error, and fix warnings only on lines you wrote or touched.

### 4. Choose one question

- Ask one decision question per turn, with one recommendation.
- Run `next`, and choose in this order:
  1. An unsettled prerequisite of the decision you would ask.
  2. Within the current axis, the shallowest undecided decision; siblings come before their children.
  3. When the current axis has nothing answerable now, the next axis.
- A decision the user names comes first. When they name an undecided node, ask that decision itself, not its descendants.
- Ask only what can be answered now. Look facts up yourself instead of asking for them.

### 5. Build the recommendation

- Recommend the option you judge best, as a concrete example, not a safe middle. Do not fix the size of the solution in advance: compare small and fundamental options side by side, and prefer the simpler one only when they come out about even.
- Think in this order before recommending. These are steps of thought, not sections of the reply: go deeper on core decisions, and show only what changed the judgment.
  1. Set the purpose and the criteria for this decision from the user's goals, the parent decisions, and `지킬 조건`.
  2. Check facts and outside evidence. Inspect the current state directly. Look up the outside facts the decision rests on (behavior of tools and standards, specifications), best practice, and precedents, starting from primary sources: official documentation, standards, original papers, the original author. Always look them up for core decisions and for decisions that rest on outside facts; for the rest, when unsure. Record what you found as verified facts with date and source, and mark what rests on memory as `확인 전`. Do this research yourself, since the next question depends on it.
  3. Lay out at least three distinct options: as is, small, fundamental, the user's, a precedent's.
  4. Compare effect, total cost to build, run, and change, difficulty of reversal, and conflicts with `지킬 조건`.
  5. Drop options that lose on every count, and pick the one that makes the biggest difference to the purpose; when it is close, pick the one that is easier to reverse and simpler.
  6. Test it against the strongest objection. If the user argued the opposite, check that the same evidence still leads to the same conclusion.
  7. State what it loses, how well it is verified, and what would overturn it.
- Check rules before recommending: this skill, the base skill, the domain skills loaded in this session, and the project and global instructions. Decisions inside the tree are checked through `지킬 조건`.
  - Add a `규칙과의 관계:` line only when the recommendation touches a rule, with one of `일치`, `구체화`, `바꿈(<rule>)`, `이번만 예외`.
  - When it is unclear whether a rule applies here, make that the decision question instead of applying or skipping the rule silently.
  - When a decision departs from a rule, write `규칙 예외: <rule>, <why>` in its node, report it on the next `이렇게 적었습니다:` line, and add it to `지킬 조건` when it rules out other decisions' candidates.

### 6. Present the question

- Write the recommendation into the node as `추천(<date>):` before presenting it. When it changes, add a new `추천(<date>):` line.
- Reply in this order:
  1. Notices, starting with `이렇게 적었습니다:`: what was decided, settled as derived, merged or pruned, reopened, reframed, or excepted from a rule. Leave it out when there is nothing to report.
  2. The marker `[현재노드-<ID>-<short title>]`.
  3. A mini tree in a code block.
  4. The question as one self-contained sentence.
  5. One recommendation, its reasons, and what it loses.
  6. `규칙과의 관계:` only when a rule is touched.
- The mini tree shows the axis of the current decision, the decisions directly under that axis, the line down to the current decision, and its siblings. Write titles without IDs, follow each with its status in English, and mark the current decision `▶ <title> ← 지금 질문`. When the axis holds many decisions, collapse the settled ones into one line such as `정한 결정 4개`.
- The question is the decision itself. Do not put the node title in its place, ask the user to approve your recommendation, or ask approval for a map or route ("이 지도로 시작할까요?").
- Show only the context the question needs; do not repeat the whole tree. The content and length of the reasons, and the choice of list or table, are free.

### 7. Update the current state

Overwrite the `현재 상태` block on every reply. It holds `작업 위치`, `최근 제시한 질문`, `지킬 조건`, `진행 약속`, `불러온 영역 스킬`, and `최종 정리 뒤 다시 엶(<date>)` after a reopening. Do not list open decisions or waiting questions there; statuses and `추천(<date>):` lines already hold them. Add dated lines to `세션 기록` at the bottom in time order.

### When the frame changes

When an answer changes the frame itself (a corrected premise, a corrected term, a counter-question that overturns the framing), realign the boundaries and titles of the affected axes and nodes to the user's words, separately from recording the answer. Keep the old frame as `대체됨` and report the realignment on the `이렇게 적었습니다:` line. Do not edit wording only to make it match.

### When an axis closes

In the turn that settles the last decision of a top-level axis, add three notices before the next question: what the axis decided, in three lines or fewer; one progress line with the axes closed out of the total and the open and blocked counts, counted with `map` at that moment; and the sentence `빠진 결정이 보이면 말씀해 주세요.`

## Red flags

These thoughts come right before the most common mistakes.

| Thought | Instead |
|---|---|
| "These two questions are independent, so I can ask both." | Ask one; the other waits its turn. |
| "Their alternative is as good as mine, so I'll record it." | A question-form reply is not a decision: compare, then ask the same question again. |
| "I answered what they asked, so this turn is done." | Present the same decision question again. |
| "It ends in a question, but it only flags a missing decision; it can wait its turn." | An item raised as a question is asked first. |
| "Settling that one too would treat one answer as permission for another decision." | If the answer leaves it no choice, settle it with `따라 정함` and report it; if it only narrows the candidates, keep it open. |
| "This turn writes no code, so the domain skills don't apply." | Load them; the recommendations become the code. |
| "A simple, safe option is enough here." | Compare small and fundamental options and recommend the best. |
| "This axis looks unnecessary, so I'll drop it before the map." | Prune only clear nonsense, and report what you pruned once, outside the tree. |
| "I'll ask which axes to keep." | Show the map; the user adds or removes axes whenever they like. |
| "This preference should last, so I'll save it to memory." | Write a `진행 약속` line; use memory only when asked. |
| "The ID search found nothing else, so nothing else is affected." | Search by topic words too, and add a `지킬 조건` line. |

## Labels and terms

Write these labels exactly; people read them and the script looks for them. Dates are `YYYY-MM-DD`.

| Concept | Label |
|---|---|
| prerequisite | `선행: <ID> <title>` |
| superseded | `대체됨(<date>): <reason>` |
| derived | `따라 정함(<date>): <decision> 결정에서` |
| user decision | `사용자 결정(<date>):`, or with how it was decided, `사용자 결정(<date>, 추천안대로):` |
| model interpretation | `모델의 해석(사용자 확인 전):` |
| confirmed interpretation | `사용자 확인(<date>):` |
| recommendation | `추천(<date>):` |
| adopt / reject | `채택` / `거절` |
| moved | `옮김(<date>): <old parent> → <new parent>` |
| withdrawn with parent | `부모 철회에 따름(<date>)` |
| rule exception | `규칙 예외: <rule>, <why>` |
| unverified | `확인 전` |

- Write statuses in English as they are.
- A group of decisions is an axis (`축`). A perspective (`관점`) is only the view used to find axes at the start.
- Prune (`가지치기`) means only removing nonsensical candidates before anything is recorded.
- `withdrawn` means only a decision whose premise disappeared.
- Name rules by their titles, not by numbers.

## Tree document

Keep the tree where the user says; otherwise in the environment's designated output directory, or at `outputs/<topic>-decision-tree.md` in the project.

```markdown
# <주제> 결정 트리

## 주제
...

## 현재 상태
- 작업 위치: B
- 최근 제시한 질문: B.2
- 지킬 조건: 출시 목표일을 정하지 않는다(출시 목표일 결정 B.1)
- 진행 약속: 이 인터뷰에서는 설명을 표 대신 목록으로 한다
- 불러온 영역 스킬: code-principles

## 확인한 사실
- F1. ...(날짜, 출처)

## 결정 트리
- A [settled] ...
  ...

## 세션 기록
- 2026-10-30: ...
```

- A node is a nested list item `- <ID> [<status>] <short title>`, and nesting sets its depth. Lines without an ID belong to the node above and add no depth.
- A node is one decision that can be answered, settled, or reconsidered on its own; its title and text together make clear what it decides. Put a new node under the decision it refines, not under the one answered last. Related subject matter alone makes neither a parent nor a prerequisite.
- Write the text under a node naturally, at the length needed to keep its open question, its decision, and the context. Field names are optional, except `선행:`, which is written only when the prerequisite is a decision in the tree; the parent is shown by position and is never written as a prerequisite.
- Top-level axes take letters (`A`, `B`), deeper levels take numbers (`B.1`, `B.1.2`). An ID is given when a candidate becomes a node and never changes: do not renumber, and keep the ID when moving a node.
- An axis that only groups decisions still has a decision of its own, such as what the axis covers.
- To point to a decision from outside the tree, write its meaning followed by the tree name and ID, such as "환불 계좌를 받지 않는 결정(예약 보증금 트리 C.2)", and link the tree name to the file inside documents. Do not use `file#ID` anchors; list items have none.

## Examples

These show the shape of a reply and of nodes, not their content.

<example>
이렇게 적었습니다: 허용 형식은 JPEG, PNG, HEIC로 정했습니다(사용자 결정). HEIC를 받기로 해서 서버에서 JPEG로 바꿔 저장하는 결정도 따라 정했습니다.

[현재노드-B.5-사진 한 장의 용량 상한]

```text
사진 업로드                          settled
├─ 정한 결정 4개
├─ ▶ 사진 한 장의 용량 상한          open    ← 지금 질문
└─ 업로드가 끊겼을 때 이어 올리기    open
```

사진 한 장을 올릴 때 용량 상한을 얼마로 둘까요?

추천: 20MB로 두고, 그보다 큰 사진은 앱에서 긴 변 4,096px로 줄여 올립니다.

이유:
- 요즘 휴대폰의 고화질 사진은 10MB를 자주 넘어서, 10MB 상한이면 원본을 그대로 올리지 못하는 일이 잦습니다.
- 앱에서 먼저 줄이면 실패 화면 없이 올라가고, 서버는 크기만 검사하면 됩니다.

잃는 것: 10MB 상한보다 저장 비용이 늘고, 긴 변이 4,096px보다 큰 원본은 남지 않습니다.

규칙과의 관계: 구체화. 코드 원칙의 "신뢰할 수 없는 경계에서 검증한다"를 서버의 크기 검사로 적용합니다.
</example>

<example>
```markdown
- C [settled] 환불
  사용자 결정(2026-11-04): 보증금을 돌려주는 방식과 조건을 이 축에서 다룬다.

  - C.1 [settled] 환불 방식
    사용자 결정(2026-11-05, 바뀐 추천안대로): 원래 결제 수단으로 돌려준다.
    대체됨(2026-11-05): 포인트를 쓰지 않는 손님의 항의가 이어졌다.
    사용자 결정(2026-11-04, 추천안대로): 매장 포인트로 돌려준다.

  - C.2 [settled] 환불 계좌 입력 화면
    따라 정함(2026-11-05): 환불 방식 결정에서. 원래 결제 수단으로 돌려주므로 계좌를 받지 않고, 화면을 만들지 않는다.

  - C.3 [blocked] 당일 취소의 환불 비율
    선행: B.2 노쇼 판정 시각
    추천(2026-11-05): 예약 3시간 전까지 취소하면 전액, 그 뒤에는 절반을 돌려준다.
```
</example>

## Scripts

`scripts/decision_tree.py` in this skill's directory reads a tree, including its split files, and never changes it. Run `python3 <this skill's directory>/scripts/decision_tree.py <command> <tree file>`, and add `--json` for structured output.

- Before presenting a question, run `next`; `--from <ID>` starts from a decision you name.
- After editing the tree, run `check`. Errors, with exit code 1, are structural: duplicate IDs, unknown statuses, a `선행:` line without an ID or pointing to a missing decision, prerequisite cycles, statuses that disagree with `선행:`, and broken split-file front matter. Warnings flag label formats; older trees may carry older label styles, so fix warnings only on lines you wrote or touched.
- When a decision changes, and before deleting a node, run `impact <tree file> <ID>`.
- When an axis closes, run `map` for the counts; it also lists waiting questions and unconfirmed interpretations.

## Finishing

- When the user stops, keep the tree and stop asking.
- When no answerable question remains, say whether blockers remain or the review is complete; do not invent questions to keep going.
- A partial summary separates settled decisions from open and blocked ones.
- Before the final stage, find live `모델의 해석(사용자 확인 전):` lines (search, or `map`) and ask each as a decision question, one per turn. Change a confirmed one to `사용자 확인(<date>):`; fix a wrong one and propagate it like a changed decision. An unconfirmed interpretation never enters the design document as a decision.
- Begin the final stage as the base skill directs, only after every material question is resolved and the user explicitly confirms shared understanding. Leave the tree where it is for later reopening; the design document is what lasts. Do not propose a separate decision-record format beside the tree.
