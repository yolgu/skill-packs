# Layout and motion contract

## Layout ownership

Use this section when a region is added, removed, reordered, resized, collapsed, overlaid, virtualized, or moved across responsive states.

Record the primary task and content, supporting regions, exposure mode, semantic order, visual placement, focus order, layout owner, scroll owners, size constraints, overlay responsibilities, and the state that must survive adaptation. Multiple scroll areas are acceptable only when each has a clear task and users can enter, exit, and understand which region moved.

Derive the test matrix from supported bounds, content change points, system insets, text scaling, zoom, locale, and input. Exercise affected empty, long, unbroken, error, bidirectional, and dynamically changing content.

## Motion ownership

Use this section only when motion, transition, gesture progress, animated continuity, or haptic behavior changes.

State the purpose, trigger, frequency, before/intermediate/after states, durable owner, interruption and cancellation behavior, and reduced-motion treatment. Repeated input must not duplicate commands or completion feedback. An animation callback is not durable success.

Prefer platform-native or compositor-friendly mechanisms appropriate to the actual target. Do not force identical timing or physics across platforms. A resting screenshot cannot prove motion; exercise the real interaction and record what remains unverified.

