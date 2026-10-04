---
name: frontend-visual-design
description: Design, restyle, or visually review browser Web and Flutter mobile interfaces with a deliberate visual direction, project-owned design values, responsive and accessible states, and verification against the real rendered surface. Use for visual design, layout, styling, motion, design-system, screenshot-reference, or visual QA work. Do not use for state management, routing, API flow, backend work, or nonvisual client changes.
license: MIT
---

# Frontend Visual Design

Improve the interface users actually see without replacing the product's existing architecture or design authority.

## Responsibility boundary

- Own visual direction, hierarchy, typography, color roles, spacing, component appearance, responsive composition, motion character, and rendered visual QA.
- Leave state ownership, server state, routing, forms, async orchestration, and feature boundaries to the project's client architecture guidance.
- Preserve the current stack and component system. Do not introduce a UI framework, icon pack, font, animation package, or image dependency without approval.
- Treat the repository's existing tokens, themes, styles, components, and representative screens as authoritative. Create `DESIGN.md` only when the repository already uses it or the user explicitly requests a new design contract.

## Select only the needed references

Read [references/ux-and-scope.md](references/ux-and-scope.md) for every task, then add only what the changed visual claim needs:

- Browser Web: [references/web.md](references/web.md)
- Flutter mobile or tablet, including a Flutter-owned renderer or WebView shell: [references/mobile-flutter.md](references/mobile-flutter.md)
- New or changed visual values: [references/design-system.md](references/design-system.md)
- Layout, scrolling, reflow, or motion: [references/layout-and-motion.md](references/layout-and-motion.md)
- Marketing, editorial, campaign, or an explicitly new visual direction: [references/visual-direction.md](references/visual-direction.md)
- Supplied screenshot, mockup, generated concept, or authorized reference: [references/image-reference.md](references/image-reference.md)
- Any changed visual claim: [references/visual-qa.md](references/visual-qa.md)

The optional files under `references/styles/` are scoped observations, not token authority. Read one only when the user names that brand or its direction clearly fits an approved brief. Never copy logos, protected artwork, brand copy, or a complete trade dress.

## Workflow

1. Inspect the product purpose, affected users, current screen, existing visual source, target platform, supported screen bounds, inputs, states, and validation commands.
2. State the visual delta and its non-goals. For an existing surface, preserve identity and behavior unless redesign is explicitly authorized.
3. Define one coherent direction from product content and existing authority. Avoid stacking unrelated visual ideas.
4. Implement the smallest complete slice, including applicable loading, empty, error, disabled, selected, focus, text-scaling, localization, and reduced-motion states.
5. Build or run the real target. Inspect the affected surface at target-derived sizes and states rather than judging source code alone.
6. Record visual findings and limitations in `VISUAL_QA.md` only when a visual claim changed. Run the relevant functional, accessibility, type, test, and build checks separately.

## Local visual QA workspace

Resolve `SKILL_DIR` as the absolute directory containing this file. Create a collision-safe ignored run directory with:

```bash
node "$SKILL_DIR/scripts/run-root.mjs" create <lowercase-slug>
```

The command prints a path under `.local-state/visual-qa/frontend-visual-design/`. Store only task-relevant captures, comparison JSON, and `VISUAL_QA.md` there. Do not treat a non-empty file as proof by itself.

For PNG references, use:

```bash
node "$SKILL_DIR/scripts/visual-diff.mjs" <reference.png> <actual.png> --json
```

The score locates visual drift; it cannot prove behavior, semantics, accessibility, platform integration, or usability.

For Web CSS only, `scripts/design-token-check.mjs` can flag undeclared hex colors and off-scale pixel spacing. It is a partial lint, not a design-system or accessibility verdict. Do not run it against Flutter source.

## Completion

Finish only when the requested surface is functionally truthful, the changed visual states were inspected on the real target, applicable accessibility and responsive checks ran, and remaining unverified states are named. A narrow nonvisual change may state that visual impact is unchanged and omit visual artifacts.

