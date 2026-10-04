---
name: website-clone
description: Reproduce an authorized website or page from a URL, screenshot, or existing implementation by inspecting its real structure, assets, responsive behavior, and interactions, then comparing the local rendered result with the source. Use for clone, rebuild, migration, pixel-focused recovery, or faithful page reproduction. Do not use for phishing, deceptive impersonation, credential capture, access-control evasion, or ordinary inspiration-based redesign.
license: MIT
---

# Website Clone

Reverse-engineer an authorized target into a working implementation in the current repository. Fidelity comes from inspecting the real source and comparing the real result, not from approximating a screenshot from memory.

## Load the workflow

Read these references in order:

1. [references/authorization-and-scope.md](references/authorization-and-scope.md)
2. [references/reconnaissance.md](references/reconnaissance.md)
3. [references/implementation.md](references/implementation.md)
4. [references/visual-qa.md](references/visual-qa.md)

## Core contract

- Confirm the target, authorization, pages, states, screen sizes, interactions, and explicit exclusions before editing.
- Use a real browser or another tool that exposes the rendered page, DOM or accessibility structure, computed styles, assets, network behavior, and interaction states.
- Inspect the current repository stack, components, commands, and user changes before choosing the implementation boundary.
- Capture source truth before building: page topology, behavior, design values, content, assets, responsive transitions, and complex section dependencies.
- Build one coherent section at a time while preserving shared foundations such as fonts, design values, icons, content shapes, and assets.
- Do not silently improve, rewrite, simplify, restyle, or replace assets during a faithful reproduction.
- Do not add dependencies without approval. Do not copy server behavior, authentication, payment, analytics, or protected data unless the user explicitly scopes and authorizes it.
- Verify the completed page in the real local runtime at controlled desktop, tablet, and mobile sizes and compare it with the source.

## Local run workspace

Resolve `SKILL_DIR` as the absolute directory containing this file. Create an ignored run directory with:

```bash
node "$SKILL_DIR/scripts/run-root.mjs" create <hostname-or-project-slug>
```

The command prints a path under `.local-state/visual-qa/website-clone/`. Keep source and result captures, notes, asset inventories, comparison JSON, and `VISUAL_QA.md` there unless the user requests permanent documentation.

Compare controlled PNG captures with:

```bash
node "$SKILL_DIR/scripts/visual-diff.mjs" <source.png> <result.png> --json
```

The comparison identifies drift; it does not authorize copying, prove interaction, or replace accessibility and functional checks.

## Stopping conditions

Stop and report the smallest concrete blocker when:

- authorization is absent or the request enables phishing, impersonation, credential capture, or access-control evasion;
- the source is behind a login, bot wall, or technical block that the available authorized access cannot cross;
- a protected asset, dependency, backend, or third-party service requires new permission;
- a high-visibility, animated, sticky, fixed, or interaction-heavy section can only be approximated with materially lower fidelity and the user has not approved that trade-off;
- the local runtime cannot be built or rendered reliably enough to compare.

## Completion

Finish with the implemented scope, source and result sizes and states, retained assets and interactions, build and test results, visual comparison findings, intentional deviations, untested states, and the stopping reason. Never call an approximation pixel-perfect.

