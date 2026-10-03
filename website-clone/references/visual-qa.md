# Clone visual QA

## Controlled comparison

Use the same viewport, device pixel ratio, theme, locale, content, assets, fonts, account state, consent state, scroll position, and animation time for source and result captures. Normalize only conditions the approved scope allows.

Compare at least the affected desktop and mobile states; add tablet and intermediate change points when layout behavior differs. Capture interaction states separately when one static full-page image cannot show them.

## Review order

1. Missing or extra sections, layers, assets, and content
2. Major container geometry, section height, alignment, and responsive order
3. Typography family, weight, size, line height, wrapping, and density
4. Image crop, video, mask, overlay, depth, and color roles
5. Sticky, fixed, scroll, hover, focus, click, carousel, and modal behavior
6. Fine spacing, borders, radii, shadows, and motion timing

Use `scripts/visual-diff.mjs` on equal-size PNGs to locate drift. A high similarity score may still hide a wrong interaction, inaccessible state, replaced asset, or important local mismatch; inspect ranked hotspots and the actual page.

## Keep or reject

Keep a change only when it improves the targeted mismatch without breaking a previously matching state, destination test, accessibility path, or adjacent screen. If an intentional deviation is required by platform behavior, accessibility, real content, or authorization, record the owner and reason.

## Completion record

Write `VISUAL_QA.md` in the run directory with:

- target and authorized scope;
- source and result capture matrix;
- build and interaction checks;
- measured comparisons and reviewed hotspots;
- retained assets and behaviors;
- intentional deviations;
- unresolved mismatches and untested states;
- final faithful, accepted-with-deviations, blocked, or incomplete result.

Never call a result pixel-perfect without controlled criteria and a passing review of every in-scope state.

