# Changes After Consolidation

Read this in full when a decision that already has a design document changes.

1. Write `최종 정리 뒤 다시 엶(<date>)` in the `현재 상태` block, and handle the changed decision like any changed decision: a `대체됨` line, `impact`, and reopening what rests on it.
2. While the interview is reopened, do not edit the body of the design document. Put one line at its top: `개정 중(<date>): 계획 작성 전에 개정을 기다릴 것`.
3. When every reopened question is answered and the user confirms shared understanding again, rewrite the design document through the final stage, with a list headed `이번 개정에서 바뀐 것` at its top.
4. Treat review or debate results that arrive after consolidation as proposals: list the decisions they would reopen, and ask them one per turn.

Checking a subagent's result before it enters the tree is a separate step; see [Subagents](subagents.md).
