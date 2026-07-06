# Manual accessibility checklist

Automated axe checks catch the mechanical issues (missing labels, contrast, broken ARIA),
but only about a third of real problems. The rest need a human. Run this before a release,
on the main flows.

## Keyboard only (put the mouse away)

- [ ] Tab through the whole page. Can you reach every control?
- [ ] Is the focused element always visibly highlighted?
- [ ] Can you operate the text dropdowns on /select with Enter or Space? They're currently
      `<a onclick=...>` with no href, which is a known problem: anchors like that aren't
      keyboard-operable or announced as buttons.
- [ ] Can you complete the multi-step vocab form (select-vocab-step-form.js) from start to
      finish without a mouse?
- [ ] Can you close any menu or dropdown with the keyboard?

## Screen reader (NVDA on Windows is free; VoiceOver on Mac)

- [ ] Turn the screen off and try to build a vocab list.
- [ ] Are the dropdown items announced as something you can activate?
- [ ] When the form adds a vocab row dynamically, is that change announced?
- [ ] Do form fields read out a meaningful label, not just "edit text"?
- [ ] Are images and icons given meaningful alt text, or hidden if they're decorative?

## Zoom and reflow

- [ ] Zoom the browser to 200% and 400%. Does content reflow without overlapping or getting
      cut off?

## Color

- [ ] Is any information conveyed by color alone (for example a red/green status with no
      text label)?
- [ ] Do text and background meet contrast? (axe covers most of this.)

## FastBridge hotspots to watch

- The text-selection dropdowns (the onclick anchors).
- The multi-step vocab builder.
- The vocab result tables (they need real table headers).
- The lemmatizer file upload and the result sheet.
