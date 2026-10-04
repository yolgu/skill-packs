# Faithful implementation

## Inspect the destination first

Read the repository instructions, manifest, design values, shared components, routes, asset conventions, test tools, and build commands. Preserve existing user changes and avoid broad refactors. Use the smallest destination boundary that can faithfully own the page.

## Build the foundation

Establish only the shared elements the reproduced sections actually need:

- approved fonts and metadata;
- global or page-scoped design values;
- shared icons and authorized assets;
- content types for repeated sections;
- responsive container and spacing rules;
- shared motion primitives with reduced-motion behavior.

Run the narrowest build or type check after the foundation before layering sections on it.

## Section contract

Before implementing a complex section, write a compact local note containing:

- source capture and target sizes;
- content and asset mapping;
- DOM or widget structure;
- layout, typography, colors, depth, and responsive behavior;
- interactions, motion, focus, and reduced-motion behavior;
- exact acceptance states;
- known source uncertainty and approved deviations.

Implement one bounded section against that note. Reuse a shared primitive only when it has the same semantic role and change reason. Do not use a generic card or carousel merely because it is convenient.

## Fidelity decisions

Prefer the destination framework's maintainable expression when it can reproduce the observed behavior. Port a source structure directly only when authorized and necessary for fidelity. Do not transplant minified, licensed, or inaccessible code blindly.

For custom JavaScript, keyframes, canvas, video, Lottie, WebGL, scroll timelines, masks, or layered positioning, reproduce the actual behavior model and dependencies. If a materially faithful implementation is unavailable, stop for approval rather than replacing the section with a similar-looking static block.

## Functional boundary

Visible interactions must be truthful. If the original depends on an out-of-scope backend, provide a clearly labelled local fixture or disabled state approved by the user; do not fake durable success, account state, payment, or private data.

## Incremental checks

After each coherent slice, run the affected build, type, lint, component, or widget checks and render the section at its target sizes. Correct the first causal mismatch before accumulating more sections.

