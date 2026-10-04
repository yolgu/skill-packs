---
name: grill-with-tree
description: Sharpen a plan or design through a persistent decision tree. Choose necessary questions across the current and next depth, provide concrete recommendations, and update only the affected parts of the tree.
---

# Grill with Tree

Build a shared understanding through an evolving decision tree.
Keep the overall subject and main decision axes visible while examining
individual decisions.

Read `../grilling/SKILL.md` and apply its rules for contextual recommendations,
fact-finding, user decisions, and final consolidation.

This skill controls question count, exploration order, document management,
resuming, and pausing. These rules replace the underlying skill's
one-question-at-a-time and automatic branch-by-branch traversal rules.

Conduct and document the interview. Do not execute the product or plan
being discussed.

## Decision nodes

A node represents one decision that can be answered, settled, or reconsidered
independently.

Its title and content together must make clear what it decides.
Keep that decision boundary stable unless the discussion actually changes it.

A child node refines a decision within its parent's context.
A prerequisite is a decision or fact that must be resolved before another
decision can be answered. Related subject matter alone establishes neither
relationship.

A parent decision may constrain its children without answering them.
Settling a parent does not settle its descendants or prevent further expansion.

Each node may have zero, one, or many children.
Branches may have different widths and depths.

Create another node when there is another independently answerable decision.
Do not turn explanatory paragraphs into nodes merely to shorten the text.
Place new nodes under the decision they actually refine, not automatically
under the most recently answered node.

## Building and maintaining the tree

Derive the main decision axes from the conversation and relevant materials.
Incorporate decisions already made and briefly show the initial map.
Do not ask the user to construct the map or repeat known information.

The initial map may be incomplete. Expand it as meaningful decisions emerge.
Do not let a newly discovered detail silently replace the overall subject.

Maintain one persistent Markdown document.
Use the user's specified location; otherwise use the environment's designated
output directory or `outputs/` in the current workspace.

Identify each node with a stable ID, status, and short human-readable title.
Use nested Markdown lists to represent the hierarchy.

Write the content beneath each node naturally, at the length needed to preserve
its unresolved issue, accepted decision, and relevant context.
Include rationale, alternatives, dependencies, uncertainties, or sources when
they help explain the decision.

Field labels are optional. There is no one-line limit and no mandatory
`Question / Decision / Rationale` template.

For example:

```markdown
- A [settled] Source data
  Use the weather alerts and disaster messages already collected.
  Additional source datasets are outside the current scope.

  - A.1 [open] Evidence for fixed safety information
    Decide whether explicit statements are sufficient, or whether recurring
    notices can also support an inference about persistent risk.

    These approaches rely on different kinds of evidence.
```

Only entries with node IDs represent decision nodes.
Prose and explanatory lists belong to their owning node and do not introduce
another decision depth.

Use these statuses:
- `open`: the decision remains unresolved.
- `blocked`: a necessary prerequisite remains unresolved.
- `settled`: this node's decision has been made.
- `withdrawn`: the decision is no longer relevant; retain a brief reason.

Determine depth from the document's nesting.
Preserve existing IDs when adding, withdrawing, or moving nodes.
Do not renumber nodes to make the tree look tidy.

Keep a brief session record of the working position and the most recently
presented question nodes. Preserve other unresolved decisions in the tree.

## Choosing questions

Choose the working position and question order according to the decisions
that need to be made and their prerequisites.

Honor an explicit user request for a node, segment, or order.
When the user selects an unresolved node, address that decision itself.
Do not bypass it merely to ask about its descendants.

At the beginning, choose the necessary starting decision and ask it directly.
Do not require a separate choice of starting route.

For subsequent turns, select up to two substantive questions:
- At most one necessary decision one level deeper.
- At most one necessary unresolved decision at the same depth.

Use the same reference position when selecting both candidates.
The same-depth candidate may belong to another relevant branch.

Keep unresolved peer decisions in view when choosing where to continue.
A newly available child is not automatically more important than those peers.

Ask only questions that can meaningfully be answered now.
Investigate facts available from the environment or materials yourself.

If one question's answer could change the other question's necessity, meaning,
or scope, ask the prerequisite question first and defer the dependent question.

Omit a direction when it has no useful, eligible question.
Do not invent decisions or add filler questions to reach two.

Choose and present the actual decision questions.
Do not insert a separate turn asking whether to move deeper, sideways,
or to another node.

## Presenting questions

Each question concerns one node and one decision.

Identify its node using this exact marker structure:

[현재노드-<ID>-<short human-readable node title>]

Keep the node marker separate from the actual question.
Immediately below the marker, state the decision as a clear, self-contained
question. Then provide your recommended answer with a brief, contextual reason
and any useful explanation. Use the user's language.

Do not use the node title as a substitute for the question or replace the
question with a generic request to approve your recommendation.

The recommendation must address the decision itself, not recommend a navigation
destination.

Present at most two such question blocks, then wait for the user's response.
Do not hide additional independent decisions inside either block.

Show only the tree context needed to understand the questions.
Do not repeat the full tree or a navigation menu after every answer.

## Interpreting answers and updating nodes

First determine which decisions the user's response actually answers or changes.
Distinguish explicit decisions, verified facts, and your own interpretation.

If the user answers only one of the presented questions, leave the other
unresolved. Do not treat silence, a recommendation, or navigation as agreement.

Update other nodes when the answer actually affects them:
- Record another decision when the user explicitly makes or changes it.
- Update an affected premise, dependency, or status when necessary.
- Reopen a decision whose accepted answer no longer holds.
- Leave a newly required choice unresolved until it is answered.

Before changing another node, identify which premise, decision, or status
is affected. If none is affected, leave the node unchanged.

Shared terminology or related subject matter alone does not justify an edit.
Do not rewrite titles, explanations, or neighboring decisions merely to make
their wording match the latest response.

Reflect necessary changes across the tree without treating one answer as
permission to settle other decisions.

## Editing the document

Create the document once and maintain it through targeted edits.

Before editing, read the relevant nodes and enough surrounding context to
understand their boundaries and dependencies.

Change only the affected text and statuses, or insert new nodes where they
belong. Preserve valid existing content, descendants, and IDs.

Do not regenerate the document or an entire subtree to update one decision.
Do not reconstruct the file from conversational memory.

Save and inspect the affected region before proceeding.
If an edit fails, reread the current content and correct it.

After recording the answer, reconsider the next necessary questions using
the updated tree.

## Resuming, reconsidering, and finishing

When resuming, read the existing document and recover the decisions,
unresolved questions, and working position.

If the user specifies a node or segment, continue there.
If the user simply says "continue," choose the next necessary questions yourself.
Do not require another navigation choice.

Expanding a settled node preserves its accepted decision while examining
necessary details beneath it.

Reconsidering a decision is a separate action.
When its answer changes, retain enough context to explain the change and update
only the descendants or dependent nodes actually affected.

When the user stops, preserve the tree and stop asking questions.

If no eligible question remains, distinguish unresolved blockers from a
completed review. Do not manufacture further questions to keep the session going.

For a partial summary, distinguish settled decisions from open or blocked ones.
For final completion, follow `grilling`'s confirmation and final-consolidation
rules. Preserve the tree for later resumption or expansion.
