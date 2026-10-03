---
name: humanize-korean
description: Rewrite supplied Korean prose so it sounds natural while preserving meaning, facts, register, modality, numbers, dates, URLs, code, product names, and quoted text. Use only when the user explicitly invokes $humanize-korean. Do not use for translation, fact expansion, SEO rewriting, legal drafting, or generic proofreading.
license: MIT
---

# Humanize Korean

Post-edit already written Korean. Remove observable translationese, repetitive rhythm, formulaic transitions, inflated significance, and unnecessary nominal constructions without inventing content or changing the author's certainty and obligations.

## Explicit invocation only

Use this skill only after the user explicitly invokes `$humanize-korean`. Do not activate it from Korean language, typos, a request for generic proofreading, or a preference for concise answers.

## Required references

- Read [references/quick-rules.md](references/quick-rules.md) before rewriting.
- Read [references/quality-rubric.md](references/quality-rubric.md) before grading or finalizing.
- Use [references/golden-set.md](references/golden-set.md) only when additional calibration is needed.
- Preserve [references/upstream-notice.md](references/upstream-notice.md) when redistributing this skill.

## Contract

- Rewrite Korean text only.
- Preserve meaning, claims, facts, numbers, dates, units, URLs, emails, code, product and model names, acronyms, legal references, and quoted spans.
- Preserve register and modality. A requirement remains a requirement; uncertainty remains uncertainty.
- Prefer fewer, sharper edits. Keep the character-change rate below 30% when possible and report risk above 50%.
- Do not add examples, metaphors, facts, citations, first-person experience, marketing claims, or deliberate mistakes.
- In Korean prose, replace em dashes and en dashes with punctuation or sentence structure appropriate to the meaning, except inside protected code or quotations.
- N-1 modifier precision: attach modifiers to the fact they actually qualify. Do not turn an accurate time, number, specification, or relationship into a vague adjective.

## Workflow

1. Identify the source and intended genre: public notice, report, blog, column, conversation, or product copy. A user-supplied genre wins.
2. Mark protected spans before editing.
3. Diagnose concrete defects using `quick-rules.md`; do not edit a strong sentence merely to make it different.
4. Rewrite paragraph by paragraph, preserving protected spans and meaning before improving rhythm.
5. For file-backed work, resolve `SKILL_DIR` as the absolute directory containing this file and create an ignored run directory:

   ```bash
   node "$SKILL_DIR/scripts/run-root.mjs" create <lowercase-slug>
   ```

6. Store `source.md`, `final.md`, `summary.md`, and `audit.json` in the printed directory.
7. Run:

   ```bash
   node "$SKILL_DIR/scripts/audit-humanize-output.mjs" \
     --source <source.md> \
     --final <final.md> \
     --report <audit.json> \
     --genre "<genre>"
   ```

8. If the audit reports a hard failure, repair once. If it still fails, return the safest meaning-preserving version and name the unresolved risk.

## Output

For text supplied directly in chat, return the rewritten Korean unless the user asks for commentary. For file-backed work, report the output path, change rate, grade, protected-token status, and a few representative changes without pasting the full artifact unless requested.
