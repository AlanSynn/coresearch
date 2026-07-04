---
name: research-proofread
description: Final line-level proofreading workflow for academic manuscripts and LaTeX papers. Use when the user asks to proofread, check grammar, polish wording, inspect LaTeX formatting, notation, citations-as-written, captions, tables, acronym consistency, or find small errors. Phase 1 reports issues only; edits files only after approval.
---

# Research Proofread

Perform a final line-level pass. This skill is not a venue review and not a contribution critique; use `research-review` for acceptance risk and `research-write` for structural rewriting.

## Good for

- Final grammar, LaTeX, notation, acronym, caption, table, reference-as-written, and consistency checks.
- Safe local polishing after contribution, evidence, and structure are already settled.
- Read-only verifier passes before submission.

## Must do

- Preserve technical meaning and author voice.
- Report issue severity and proposed fix.
- Keep Phase 1 read-only unless pasted text asks for direct corrected output.
- Ask/require approval before editing files.

## Not for

- Reframing contributions or changing paper structure; use `research-design` or `research-write`.
- Acceptance scoring; use `research-review`.
- Adding new citations, results, or claims.

## Default policy

- Phase 1 is read-only: report issues without editing files.
- In OMX/team contexts, proofreading is a final verifier pass; do not broaden into argument review unless the user asks.
- Phase 2 edits only after user approval.
- If the user pasted text and asks for direct correction, provide corrected text in chat.
- Do not change technical meaning.

## What to check

1. Grammar, spelling, articles, prepositions, agreement.
2. Non-native or awkward academic phrasing.
3. Overclaim words: significant, SOTA, robust, general, novel, intuitive, seamless.
4. Tense consistency: present for established knowledge, past for conducted experiments.
5. Notation and acronym consistency.
6. Figure/table/caption clarity and cross-references.
7. LaTeX issues: missing refs, undefined commands, bad math punctuation, inconsistent citation commands.
8. Hyphenation and terminology consistency.
9. Abstract/conclusion alignment at the wording level.

## Output schema

```markdown
# Proofreading Report

## Critical Fixes
| Location | Text snippet | Issue | Proposed fix | Confidence |
|---|---|---|---|---|

## Major Fixes
| Location | Text snippet | Issue | Proposed fix | Confidence |
|---|---|---|---|---|

## Minor / Style Fixes
| Location | Text snippet | Issue | Proposed fix | Confidence |
|---|---|---|---|---|

## Consistency Table
| Term / acronym / notation | Variants found | Recommended form | Action |
|---|---|---|---|

## LaTeX / Reference Issues
- [Issue or “Not checked.”]

## Edit Readiness
- Safe to apply automatically: [yes/no]
- Requires author decision: [bullets]
```

## Severity guide

- **Critical:** typo in title/abstract, wrong variable, contradiction, broken citation/ref, grammar that changes meaning.
- **Major:** awkward or unclear sentence, undefined term, inconsistent notation, unsupported strong word.
- **Minor/style:** concision, local flow, formatting, repeated words that do not change meaning.

## Guardrails

- Do not fabricate citations or facts.
- Do not add new results.
- Do not rewrite whole sections unless asked.
- Preserve author voice and venue tone.
