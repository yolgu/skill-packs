# Splitting and Graph View

Read this in full when a split signal appears or the user asks to see the tree as a graph.

## When to split

- Size is not a reason to split. Keep reading cheap with the `현재 상태` block, searches by decision, and partial reads. File boundaries follow independent groups of decisions.
- Start with one document, and split when a group becomes clear. The signals:
  1. Independence: the branch refers mostly to itself and is rarely referred to from outside. An axis boundary is the first candidate.
  2. A separate life cycle: the branch alone is all settled, or the content plays another role, such as facts or the session record.
  3. Different people decide it, or different sessions will work on it.
  4. An outside document needs to point to that branch on its own.
  5. The user asks to see the tree as a graph; then split down to one decision per file.
- Do not split a branch that is still being expanded or decided for adoption, or one that is referred to a lot from outside.
- Apply the same signals to split files. Merge a file back when it loses its independence or most of it is withdrawn.
- When a signal appears, show the signal, the evidence, and one candidate split, and ask once for each split.

## Split file format

- Each fact about a decision lives in one place. The node line holds the ID, status, and title, and the `선행:` line holds prerequisites, whatever the file. A file with a single decision uses the same format.
- The front matter holds three file-level fields only: `root` (the ID of the file's root decision), `description` (one line on what the branch decides), and `parent` (the file holding the parent decision, as a quoted wikilink).
- In the parent file, the moved block is replaced by one link line at the node's position: `- [[<tree name>.<ID>]]`.
- Read the map in two layers: the file map from the front matter only, and the decision map from the node lines and `선행:` lines of every file (`map`).

<example>
```markdown
---
root: B.2
description: 부분 환불을 처리하는 순서를 정한다
parent: "[[payment-flow-decision-tree.B]]"
---

- B.2 [open] 부분 환불 처리 순서
  선행: B.1 환불 승인 주체
  ...
```
</example>

## Promoting a branch

1. Split one branch that shows a signal at a time; do not move everything at once. A tree meant for graph view is split down to one decision per file. Show the signal and the evidence, and ask once for each split.
2. Keep every ID.
3. The original document stays as the trunk and keeps the `현재 상태` block. Move the node block to the new file without leaving a copy, and put the link line where it was.
4. Move facts and the session record out only when they show a life-cycle signal; otherwise they stay in the trunk.
5. Compare `map` before and after the move (IDs, statuses, prerequisites), and run `check`.

## File names

- The trunk keeps its file name and place, so links to it keep working.
- Split files go in a folder beside the trunk that has the trunk's name, as `<tree name>.<ID>.md`. The tree name is the trunk's file name without its extension.
- Keep titles out of file names; titles change.

```text
outputs/
├─ payment-flow-decision-tree.md            trunk: 현재 상태, remaining axes, link lines
└─ payment-flow-decision-tree/
   ├─ payment-flow-decision-tree.B.md       root: B
   └─ payment-flow-decision-tree.B.2.md     root: B.2, parent: "[[payment-flow-decision-tree.B]]"
```

## Graph view

- A graph shows one tree's decision structure: parents, children, and `선행:` relations. Links between trees, design documents, or projects are out of scope.
- Split the tree down to one decision per file. The parent link lives in the `parent` field, and prerequisites are wikilinks on `선행:` lines, such as `선행: [[payment-flow-decision-tree.B.1]] 환불 승인 주체`.
- Keep the tree where it is. To view it, open the tree's folder (the folder beside the trunk, or `outputs/`) in Obsidian as a vault of its own. Do not move it into another vault or link it in with a symbolic link: Obsidian does not watch changes made outside it behind a symbolic link, and the tree is edited from outside.
- What must last goes into the design document; whether the tree goes into git is the project's call.
