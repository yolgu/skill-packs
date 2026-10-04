# Rendered visual QA

## When required

Run visual QA when appearance, layout, typography, imagery, responsive behavior, or a visibly expressed interaction state changes. Omit it for a genuinely nonvisual change and state why.

## Capture contract

For each retained capture, record:

- target and build;
- route or screen;
- account and data state without secrets;
- viewport or device bounds and pixel ratio;
- locale, text scale, theme, reduced-motion setting, and input where relevant;
- expected visual claim and observed result;
- untested states and limitations.

Capture representative normal states and only the loading, empty, error, selected, disabled, expanded, keyboard-open, long-content, or alternate-theme states affected by the change.

## Comparison

When a controlled reference exists, run `scripts/visual-diff.mjs` on equal-size PNGs. Use similarity and hotspot output to direct inspection. Review typography, assets, crop, hierarchy, overflow, and interaction states with human judgment. Explain intentional deviations rather than forcing accessible or platform-correct differences back toward the reference.

## Completion report

`VISUAL_QA.md` should name the requested outcome, captures, comparisons, retained changes, checks, limitations, and result. Do not claim an unsupported state passed because a neighboring screenshot looks correct.

