# UX and scope contract

## Establish the delta

Before changing appearance, reproduce the current journey and identify the affected screen, user job, current design authority, implementation owner, target platform, representative content, and adjacent state that could regress. Separate observed facts, approved direction, assumptions, and unknowns.

For a narrow visual correction, keep the scope narrow. A new or redesigned surface should define the entry, action, system response, recovery, and exit; relevant loading, empty, partial, error, retry, disabled, selected, and completed states; and the accessibility and localization constraints that affect composition.

## Functional truth

- An enabled control must perform its advertised outcome. A handler call, toast, spinner, or mock response is not success.
- A failed operation must preserve recoverable input, state what happened without leaking internals, and provide a useful recovery path when one exists.
- Editable-looking controls must support the actual edit, validation, commit, and cancellation behavior expected by the platform.
- Decorative elements must not gain a false interactive role, focus stop, hover treatment, or pressed state.
- Simulated capabilities must be labelled and must not be presented as production behavior.

## Content and information hierarchy

Name the primary task, essential state, blocker or error, recovery action, and next decision. Give each task-bearing region a user-recognizable purpose. Remove or merge regions that repeat the same job merely to make the screen look complete.

Dense interfaces are valid when comparison or monitoring requires concurrent visibility. Sparse interfaces are valid when one decision deserves focus. Choose density from the task rather than a generic aesthetic.

## Accessibility and localization

Verify applicable names, roles, states, actions, reading and focus order, visible focus, status announcements, contrast, text scaling, touch targets, keyboard or assistive-technology paths, and alternatives to gesture-only actions. Reduced motion must preserve the semantic outcome and essential feedback.

Exercise representative long Korean text, unbroken values, mixed scripts, translated content, taller text, and right-to-left content when supported. Do not build layout around one ideal string.

## Evidence boundaries

A screenshot proves one rendered state. It does not prove behavior, accessibility, performance, semantics, or usability. A static checker proves only the rule it evaluates. Match each completion claim to the narrowest real evidence that can establish it.

