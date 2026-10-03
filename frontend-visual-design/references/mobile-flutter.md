# Flutter mobile and tablet contract

Use this reference for Flutter-owned phone or tablet UI and for journeys that cross a Flutter shell and embedded WebView.

## Platform and renderer ownership

Resolve supported OS versions, form factors, current window bounds, orientation, safe areas, system bars, package channel, supported inputs, locale, restoration model, and available emulator or device validation. Flutter owns pixels and much of the semantic bridge; native services still own permissions, pickers, system handoffs, and platform lifecycle.

Do not infer native behavior from visual resemblance. Verify semantics, focus, editable text, IME composition, selection, clipboard, keyboard avoidance, platform back behavior, interruptions, process recreation, and permissions where the changed journey depends on them.

## Adaptive composition

Respond to current window and content constraints rather than device model names. Exercise text scaling, long Korean content, rotation or resizing when supported, safe areas, on-screen keyboard, locale changes, reduced motion, and high-contrast or theme changes when applicable.

Do not force text scale to a fixed value to protect a layout. Fix the composition so required text remains readable and actions remain reachable.

## Flutter design authority

Inspect `ThemeData`, `ColorScheme`, text themes, app-owned color and spacing constants, shared widgets, and representative screens before adding values. Prefer the actual project owner over a parallel Markdown token file. Add a semantic design value only when a component needs a role the existing owner does not express.

## WebView boundary

For embedded Web, name whether Flutter, the Web document, the bridge, or the remote service owns each state and action. A JavaScript message or spinner does not prove that a native or durable operation succeeded. Verify navigation policy, input, focus, accessibility, permission, cancellation, reload, and return-path behavior separately on the owners involved.

## Mobile proof

Keep a minimum regression floor that builds and launches the real target, executes the changed journey, and exercises the nearest adjacent path. Emulator evidence is suitable for deterministic states; physical-device evidence is required only for sensor, permission, performance, input, accessibility-service, or rendering claims simulation cannot establish.

