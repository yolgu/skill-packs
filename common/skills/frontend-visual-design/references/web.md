# Browser Web contract

Use this reference for DOM-based browser pages, interactive landing experiences, and browser-hosted WebView content.

## Existing stack

Inspect the framework, style system, build scripts, component primitives, route owner, server-rendering boundary, public asset path, supported browsers, and existing test tools. Preserve them. Use semantic HTML before recreating native controls with generic elements.

## Responsive behavior

Derive change points from content and container constraints. Test just below and above each affected change point, plus the supported minimum and representative wide size. Account for zoom, text scaling, browser chrome, safe areas where applicable, on-screen keyboards, overflow, and localization.

Horizontal scrolling is valid for task-owned tables, timelines, maps, and canvases when headers, navigation, focus, and context remain usable. Root-page horizontal overflow caused by layout mistakes is a defect.

## States and input

Verify pointer, touch, keyboard, focus, hover where supported, pressed, selected, loading, empty, error, and success states. Do not make hover the only way to discover necessary content or actions. Preserve input and focus during asynchronous updates and responsive reflow.

## Performance and assets

Give images explicit dimensions or aspect ratios, use appropriate responsive sources, and avoid loading visual media before it can contribute to the current screen. Add animation or image packages only with approval. Measure performance only when performance is part of the claim or a changed asset creates material risk.

## Browser proof

Build or serve the production-like target with the project's command. Record the browser, viewport, route, state, content, theme, and input used for every retained capture. Console output, network errors, and source inspection may explain failures but do not replace the rendered journey.

