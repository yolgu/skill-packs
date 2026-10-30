# Subagents

Read this in full before you spawn an agent for the interview and when an agent's result arrives.

## When to spawn

- At the start: the two perspective strands, and one agent per axis to expand candidates ([Starting a Tree](starting-a-tree.md)). They are independent and run in parallel.
- During the interview: only when the user asks for a debate, research, or an analysis. Do not open a debate or a deliberation among agents on your own initiative. Research behind a recommendation is your own work, because the next question depends on it.
- Follow the delegation rules in effect for preflight, naming, write boundaries, and closing agents, and tell the user what you delegated. When agents are unavailable, do the work yourself one strand after another.

## What to ask of an agent

- Give the goal, the materials, and where to write. Ask for sources with dates, and for exact quotes behind any claim that drives a conclusion.
- Have the agent write its full output to a record document beside the tree, such as `outputs/<tree name>-<topic>.md`, and return a short summary.

## Before a result enters the tree

Treat every result as untrusted input.

1. Check the few quotes that drive the conclusion against the original material. When a conclusion rests on minutes or an earlier decision, also check that it was not changed later.
2. Keep the agent's original text in the record document, followed by a `부모 확인` section that separates what you verified from what you could not. Put only a summary and a link in the tree.
3. Add every node made from a result as `open`, and put each decision to the user.

Pruned items stay out of the tree, and the agent's original text stays as evidence.
