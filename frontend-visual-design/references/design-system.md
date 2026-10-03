# Design-system contract

## Choose the authority first

Inspect the repository's existing themes, CSS variables, style layer, component library, platform conventions, and representative screens before writing design documentation.

- If the project already uses `DESIGN.md`, update it when the changed visual role belongs there.
- If code or another document owns the system, update that source instead of creating a competing file.
- If no formal document exists, preserve working conventions and introduce only the minimum coherent semantic roles required by the change.

## Roles

For a new or approved redesigned direction, define only the roles the product needs:

- atmosphere and one recognizable visual thesis;
- color roles with light, dark, state, and contrast behavior where supported;
- typography roles with weight, size, line height, fallback, scaling, and locale behavior;
- spacing and size roles in the platform's native units;
- component structure and applicable states;
- motion purpose, interruption, and reduced-motion behavior;
- depth strategy such as tonal separation, borders, shadows, or native elevation.

Do not mix unrelated token systems. App-defined values must be added to the authoritative source before use. Platform-owned runtime values remain platform-owned.

## Partial Web check

For CSS targets only, `scripts/design-token-check.mjs` can find raw hex colors absent from a Markdown design contract and pixel spacing outside its declared base scale. The script does not understand CSS variables, typography, components, native code, or accessibility completely; use its output as a focused finding list.

