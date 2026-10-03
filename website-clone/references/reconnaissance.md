# Source reconnaissance

Capture the source before implementation. Do not estimate a value the browser or supplied source can reveal.

## Baseline captures

Capture representative full-page and focused section images at the agreed desktop, tablet, and mobile sizes. Record URL, timestamp, viewport, device pixel ratio, theme, locale, account state, consent state, and any animation or carousel time position.

## Page topology

List sections from top to bottom and identify:

- global shell, header, navigation, footer, overlays, portals, and fixed layers;
- normal document flow, grid or flex ownership, containers, breakout regions, and scroll owners;
- sticky, pinned, snap, parallax, reveal, canvas, video, and WebGL regions;
- z-index relationships and content that each overlay must not cover;
- responsive reorder, collapse, substitution, or omission behavior.

## Interaction sweep

Scroll slowly before clicking so scroll-driven tabs and sticky transitions are not mistaken for click behavior. Then exercise every visible button, link, tab, pill, card, accordion, modal trigger, carousel control, input, and menu. Record hover, focus, pressed, selected, loading, error, success, disabled, expanded, keyboard-open, and time-driven states that actually exist.

Repeat affected interactions at each target size. Record exact state changes, transition purpose and timing, focus behavior, URL changes, preserved content, and recovery.

## Design values and content

Extract the actual fonts and fallbacks, color roles, text scale, line height, spacing, radii, borders, shadows, icons, image treatment, container widths, breakpoints or content change points, animation timing, and reduced-motion behavior. Preserve real visible copy when the scope authorizes it; otherwise use user-provided content without inventing product claims.

## Asset inventory

Inventory image sources and dimensions, videos and posters, CSS background images, inline SVGs, icons, fonts, favicons, manifests, and layered masks or overlays. A visual may consist of several positioned assets; do not rebuild it as generic HTML before confirming its real composition.

## Complex section dependency map

For every animation-heavy or interaction-heavy section, record the DOM or component roots, selectors or style owners, scripts and listeners, keyframes or timelines, assets, masks, z-index layers, external libraries, data inputs, and responsive conditions. If source internals are unavailable, record observed behavior and the uncertainty instead of inventing an implementation.

