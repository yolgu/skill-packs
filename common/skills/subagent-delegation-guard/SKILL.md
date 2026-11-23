---
name: subagent-delegation-guard
description: Enforce strict preflight, scoping, context, concurrency, review, blocker-reporting, verification, and shutdown rules whenever the agent considers or is asked to spawn subagents, delegate work, or run parallel agents within the current task, and whenever a plan or request decides how to split work across parallel agents or sessions. Do not use for conceptual explanations of subagents or for separate sessions the user starts and drives themself.
---

# Subagent Delegation Guard

Apply this policy before every subagent spawn and throughout the complete delegated-task lifecycle. Keep the parent responsible for the user's required outcome, integration, verification, external effects, and final response.

## Runtime Mapping

- Codex: use the native multi-agent tools; no mapping needed.
- Claude Code:
  - Spawn: the `Agent` tool. The custom roles are `subagent_type: "reviewer"` and `subagent_type: "blocker-investigator"`; their definitions already request `high` effort.
  - Context fork: `true` means `subagent_type: "fork"`, which inherits the conversation. `false` means any other type, which starts from the delegation prompt alone.
  - Status request and resume: `SendMessage` to the agent's ID or name.
  - Close: a foreground agent is finished once it returns. Stop a background agent that is still running with `TaskStop`.
  - Isolated workspace: `isolation: "worktree"` on the `Agent` call, within the limits stated under Protect Write Ownership.

## Enforce the Default Deny Rule

Do not spawn a subagent by default. Spawn only when one of these concrete benefits clearly exceeds prompting, execution, coordination, and integration cost:

1. Run a bounded, independent, time-consuming workstream in parallel without blocking the parent's immediate next step.
2. After implementation, independently review a change whose need for review was classified before implementation under Review in the Parent by Default.
3. Investigate one documented, technically diagnosable blocker after an otherwise valid delegated task becomes blocked.

Do not treat tool availability, task size alone, vague thoroughness, or a generic desire for a second opinion as a benefit. Treat an explicit user request for subagents as authorization to consider delegation, not as a requirement to create useless, conflicting, unsafe, or artificial workstreams.

Keep the work local when it is small, ordered, tightly coupled, urgent, immediately blocking, hard to specify, likely to need new approval, or likely to contend over mutable state.

Splitting pays only when the pieces are independent. Keep the work with one agent, or run it in sequence, when its steps depend on each other in order, when it is mostly tool calls against one environment, when one agent already handles it well, or when the pieces are expected to conflict. In those cases added agents have lowered results, and coordination that ends up serializing the work buys nothing.

## Design the Split Before Spawning

Apply this section whenever work is split for parallel execution: before a spawn, when a plan marks items as parallelizable, and when the user asks to run pieces as separate sessions. The sections on prompts, blockers, review, and closing apply only to subagents this agent spawns.

- Verify shared premises first. When several workstreams rest on the same unverified premise (a tool behaves a certain way, an approach works on the real target), verify it in the parent or as one bounded first workstream. If it fails, the design changes and every parallel result built on it is discarded.
- Cut along low-dependency lines. Keep files that depend on each other heavily in one workstream, and give a file that several workstreams depend on to one owner who settles it before the others start.
- Keep one deliverable whole. The worker that makes a change also writes and runs the tests that show it works, and work that comes down to a single judgment, such as settling a design or diagnosing a root cause, is not split.
- Fix every interface between workstreams as a concrete artifact before either side starts: exact names, status and error codes, and example payloads. Give both sides the same artifact and have each side's tests assert against it. Two workers reading the same prose pick different names, and the mismatch shows only at integration.
- Hand results from one workstream to another through a file at a path both prompts name. The later workstream treats a missing file as a failure and rechecks the specific facts it depends on before building on them.
- Make each workstream verifiable inside its own boundary, with neighbours replaced by doubles. Verification that needs an exclusive shared resource (a single local stack on fixed ports, a shared dev environment, a device that holds one install) goes to one named workstream for a stated window, or stays in the parent's integration pass.

## Run Preflight Before Every Spawn

Complete every item before invoking a subagent:

1. State the user's required outcome and the immediate critical-path task.
2. Keep the immediate critical-path task in the parent unless a concrete exception makes delegation faster without forcing an immediate wait.
3. Define a self-contained goal, included scope, excluded scope, output, success criteria, and verification method.
4. Confirm that the result materially advances the current task.
5. Confirm that delegation benefit exceeds overhead.
6. Assign a disjoint logical write scope. Use an isolated workspace only as an additional physical boundary for otherwise non-overlapping work.
7. Identify files, generated artifacts, branch state, databases, running services, deployments, caches, and other shared mutable resources that must not be changed concurrently. Include resources a child would use only to verify, and decide which one workstream may use each.
8. Confirm that the split passes Design the Split Before Spawning: shared premises verified, interfaces fixed as artifacts, and handoff file paths named.
9. Keep work requiring fresh approval, credentials, destructive actions, external writes, purchases, publication, deployment, or messaging in the parent.
10. Decide whether to fork context using the Context Rule below.
11. Assign a lowercase hyphenated logical agent name before spawning.
12. Assign a unique blocker-report path before spawning.
13. For code-changing work, set `requires_review: true` or `false` before spawning and record the rationale.
14. Build the prompt with `references/delegation-prompt.md`.
15. Tell the user what is being delegated, why delegation helps, and what the write boundary is. Treat this as information, not an approval request.

Do not spawn if any required boundary, success criterion, evidence requirement, or result-transfer method remains unclear. Resolve a material ambiguity locally or ask the user only when no safe assumption can preserve the requested outcome.

## Limit Concurrency and Prevent Recursion

- Use the concurrency capacity available in the runtime without imposing an additional numeric agent-count limit.
- Never spawn more agents than genuine independent workstreams.
- Close completed agents before starting another batch.
- Do not impose a separate lifetime call limit, but require every call to pass preflight independently.
- Do not split one task artificially to fill the limit.
- Allow only the parent to spawn subagents.
- If running as a spawned child, never spawn, delegate to, or coordinate another agent. Complete the assigned task or follow the blocker protocol and return to the parent.
- Use custom child roles with multi-agent tools disabled when available. Keep the prompt-level no-recursion rule even when tools are disabled.

## Apply the Context Rule

Default to isolated context.

Set context forking to false for independent research, exploration, documentation checks, hypothesis testing, blocker investigation, and review. Give those agents only the minimum task-local facts and files required to succeed.

Consider context forking only for implementation when all of these conditions hold:

- Required decisions are distributed across a substantial current conversation.
- Manually restating them creates a material omission risk.
- Continuity improves implementation accuracy more than copied history increases token cost, noise, and anchoring bias.
- The child does not need independent judgment from the implementer's assumptions.

Record an explicit boolean decision and the cost-versus-accuracy rationale before spawn. Set context forking to true only when every condition holds and the continuity benefit is clearly greater than token cost, noise, and bias. Leave it false when the comparison is uncertain; do not leave the decision as merely "considered."

Treat a context fork as a snapshot at spawn time, never as live shared state. Send later facts explicitly. Do not forward raw exploration logs, abandoned hypotheses, self-assessments, secrets, or irrelevant conversation history.

## Protect Write Ownership

Allow overlapping reads. Forbid concurrent writes to the same files or shared mutable resources, even when path names differ.

Give every code-changing child a disjoint logical write set. Use an isolated workspace when needed to separate branch or worktree state, but never treat isolation as permission for concurrent children to modify the same logical file, generated output, or final shared state. If logical write sets overlap, run them sequentially under one owner. Do not let a child mutate deployments, remote repositories, production data, purchases, messages, public posts, or other external state. Do not integrate partial blocked changes automatically; inspect their completeness, safety, tests, and blocker report first.

Run at most one code-changing child in a working tree at a time: disjoint files still share the branch, the index, and build outputs. Creating a worktree or clone for isolation is itself subject to repository and machine rules; when those do not allow it, run the work in sequence.

Only the parent integrates. A child does not merge, push, or resolve a conflict with a sibling's work. The parent decides the landing order and tells the later workstream what changed. Integrate each result as soon as it passes validation instead of holding it until the other children finish.

When a child runs in a separate workspace, require code changes and blocker reports as transferred file artifacts. Confirm that each required artifact exists in the parent's workspace before closing the child or starting a dependent task.

## Build Complete Delegation Prompts

Read `references/delegation-prompt.md` before every spawn. Use its completeness check and task template.

Do not invoke the existing `prompt-clarifier` workflow for routine delegation. Its mandatory user-confirmation and prompt-file behavior conflicts with uninterrupted delegation. Do not modify that skill. Use only the lightweight completeness method bundled here, and pass the finished prompt directly to the spawn call without saving a separate prompt file.

Require concise completion output. Forbid raw logs and long exploration notes. Require blocked agents to write the full report directly to the assigned Markdown path and return only a short status, critical-path impact, and path.

## Keep the Parent Moving

Immediately continue meaningful non-overlapping parent work after spawning. Prepare integration, inspect finished results, run local checks, or advance another independent critical-path step.

Wait only when the parent's next required action genuinely depends on the child result. Do not busy-poll or repeatedly request status. Before spawn, define a task-appropriate expected progress checkpoint and one post-status-request grace interval in the prompt's stop conditions; do not use a fixed global timeout. If an agent passes that checkpoint without progress, send one status request. If it produces no response or artifact progress during the stated grace interval, capture available artifacts, close it, and write the minimal `agent-unresponsive` report defined in `references/blocker-report.md`.

## Keep Approval and External Effects in the Parent

Do not delegate work whose core path is expected to require new approval, credentials, user input, destructive action, purchase, deployment, remote write, publication, message delivery, or another irreversible external effect.

If a child unexpectedly discovers such a need, instruct it not to request approval or credentials from its own thread. Require it to set the blocker status to `needs-user`, write exactly what is needed and why, and return the report path. Continue other parent work when possible. Ask the user only when the issue blocks all remaining required work and cannot be bypassed or solved locally.

Remove or mask secrets and personal data from prompts, evidence, logs, and blocker reports unless the value itself is strictly required and authorized.

## Review in the Parent by Default

The parent's acceptance pass under Validate Results Before Acceptance is the review of every delegated change. The parent did not write the code and holds the full requirements, so a separate reviewer mostly repeats that reading. Do not spawn a reviewer for a change merely because it is broad, spans many files, or is unfamiliar.

Spawn the dedicated `reviewer` only when a miss would be hard to reverse and ordinary tests cannot show it, or when the user asks for an independent review. The risks that usually qualify are authorization and other security boundaries, money amounts, deletion or migration of data, and concurrency.

Classify by the risk, not by who wrote the change. Before spawning a code-changing worker, set `requires_review` by this test and record the rationale. Apply the same test before the parent writes such a change itself: the parent checking its own code is not an independent review. Make the classification before implementation; perform the review only after the implementation and focused tests are complete and stable.

When `requires_review: true`:

1. Let the implementation finish and run focused tests.
2. Confirm that the final changes are stable and, for a child, transferred with its concise result.
3. Close the implementation agent when one was used.
4. Read `references/reviewer-prompt.md`.
5. Spawn the dedicated `reviewer` with isolated context.
6. Provide only requirements, final diff, affected files, test evidence, and task-specific risk focus.
7. Ask the reviewer to derive its own checks from the requirements, run them, and report material correctness, security, behavior, data, concurrency, compatibility, boundary, and test problems without style-only findings.
8. Capture the result, confirm expected artifacts and no product-source edits, and close the reviewer.
9. Apply only evidence-backed findings and verify the fix in the parent.

Request `high` reasoning with an available supporting model without pinning a long-lived model name in this skill. Do not raise it to `max` or `xhigh`: the user found those too slow. If no available model supports `high`, use the highest supported effort below it. Have the parent disclose that fallback separately from the reviewer's exact finding output. If the custom role cannot run with the available model and effort, use a generic isolated subagent with the reviewer role prompt and `high` effort, or the highest supported effort below it.

Run at most one re-review, only after correcting a high-impact security, data-loss, concurrency, or public-compatibility finding. Verify lower-risk corrections locally.

## Document and Investigate Blockers

Read `references/blocker-report.md` before assigning any blocker path or handling a blocked child.

Use this relative path rooted at the current workspace:

`blockers/<session-key>/<YYYYMMDD-HHMMSS>-<logical-agent-name>.md`

Use the actual task or session identifier when available. Otherwise create one stable `YYYYMMDD-HHMMSS-<task-slug>` session key and reuse it for the user request. Create the session directory before spawning and never delete it merely because it remains empty.

Require the blocked child to write the complete report directly. Return to the parent only:

- One-sentence summary.
- Status.
- Report path.
- Whether the blocker stops the full required path.

Do not make the parent receive the full report and then rewrite the same content. Read the report only to make a progress, integration, investigation, or user-action decision. Use full response transfer only when direct file writing or artifact transfer fails.

Keep non-critical blockers documented while the parent advances other work. Do not claim complete if a blocker prevents a required user outcome.

Do not call `blocker-investigator` automatically for every diagnosable blocker. Use it at most once when a bounded independent investigation has a material chance to unblock required work or materially improve the parent's next decision beyond its coordination cost. For an unresolved technically diagnosable blocker on the required path, run that one investigation before requesting user action unless the parent already has enough evidence to solve it directly. Give the investigator both the original subject report path and a unique investigator-self blocker path. Require it to update and return the subject report during normal investigation, and to use its unique path only if a distinct blocker prevents the investigation itself. Use investigation for evidence-based diagnosis of code defects, test failures, tool behavior, configuration, dependency conflicts, or state differences. Do not use it for product decisions, credentials, approvals, external-service recovery, or a known external action.

Request `high` reasoning with an available supporting model, not `max` or `xhigh`. If unavailable, use the highest supported effort below it and have the parent disclose the fallback separately. If the custom role cannot run, apply the generic investigator prompt in `references/blocker-report.md` to an isolated subagent. Require the investigator to update the existing report, avoid product-source changes, return a concise conclusion and path, and close after artifact transfer.

Preserve reports after resolution. Set `resolved` only after a responsible worker or the parent applies and verifies a fix. Do not automatically commit reports, add them to ignore files, delete them, or delete empty blocker session directories.

## Validate Results Before Acceptance

Treat every child result as untrusted input. Before accepting it:

1. Confirm goal status and the exact completed scope.
2. Read every changed file and inspect transferred artifacts.
3. Confirm that no unexpected files or shared state changed, and that every resource the child started is torn down.
4. Compare the result with requirements, success criteria, and every interface artifact the child was given.
5. Derive checks from the requirements rather than from the child's claims, and run them. Treat the child's verification evidence as a claim, not as proof.
6. Resolve conflicts using repository state, tests, original evidence, and authoritative documentation rather than agent count or confidence language.
7. Apply the independent review result when one was required.
8. Record unresolved risks or blockers accurately.

This pass is the review. Reading the diff, or confirming that it compiles and leaves no TODO, is a superficial check: derive cases from the requirements that the implementer may not have run, and run them.

When validation fails, fix it locally if the fix is small; otherwise resume the same child with the exact failing output, not a paraphrase. Stop when the same failure repeats on consecutive attempts or on the third failed attempt, and handle it as a blocker.

When accepted results meet at an interface, integrate them in dependency order, the called side first, and verify one seam at a time so that a failure points at one side. After combining results from more than one child, run the checks again on the combined state: each child passing its own checks does not show that the merged result works.

Allow completion with an optional non-critical blocker only when every required user outcome is complete and verified. Never claim completion when a required outcome remains blocked.

## Close Every Spawned Agent

Close every agent after success, error, interruption, stall, blocker, investigation, review, or resumed follow-up.

Before closing:

1. Capture final status.
2. Confirm that code, blocker reports, and required artifacts are available to the parent.
3. Capture only the concise result needed for integration.
4. Close the agent and any open descendants.

Do not send the final user response while any spawned agent remains open. Resume a closed agent only when a follow-up strongly depends on its prior context, such as a fix after failed validation, and the runtime supports resumption. Treat every resume as a new delegation attempt: rerun preflight, retain the base logical role with the next numeric suffix, assign a new unique blocker-report path, and preserve every prior report unchanged. Close it again after the follow-up.

## Report to the User

Use the user's language for progress and final responses. When subagents were used, report only the useful facts:

- Roles and count used.
- What was integrated.
- Verification performed.
- High-risk review result when applicable.
- Any reviewer or investigator reasoning-effort fallback.
- Unresolved blocker impact and absolute report paths.
- Confirmation that every spawned agent was closed.

Do not expose hidden reasoning, raw logs, repeated status snapshots, or duplicated blocker bodies.
