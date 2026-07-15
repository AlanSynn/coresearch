---
name: research-proofread
description: Final line-level proofreading workflow for academic manuscripts and LaTeX papers. Use when the user asks to proofread, check grammar, polish wording, inspect LaTeX formatting, notation, citations-as-written, captions, tables, acronym consistency, or find small errors. Phase 1 reports issues only; edits files only after approval.
---

# research-proofread — Final Line-Level Pass

Line-level grammar/LaTeX/notation pass, run only after contribution, evidence,
and structure are settled. Not a venue review, not a contribution critique.

## What & When

Line-level proofreading of manuscripts and LaTeX papers. Use when: "proofread
this", "check grammar", "polish wording", "inspect LaTeX", "notation/acronym/
caption consistency", pre-submission read-only sweep. Scope is grammar/LaTeX/
notation only — content is settled upstream. Not for: acceptance risk →
research-review; reframing contributions or restructuring → research-write /
research-design; adding citations, results, or claims → out of scope.

## Procedure

Phase 1 is read-only: report issues, never edit files. Phase 2 edits only after
user approval; if the user pasted text asking for direct correction, return
corrected text in chat. Preserve technical meaning and author voice; report
severity + proposed fix + confidence per issue. Check:

1. Grammar, spelling, articles, prepositions, agreement.
2. Non-native or awkward academic phrasing.
3. Overclaim words: significant, SOTA, robust, general, novel, intuitive, seamless.
4. Tense: present for established knowledge, past for conducted experiments.
5. Notation and acronym consistency.
6. Figure/table/caption clarity and cross-references.
7. LaTeX: missing refs, undefined commands, bad math punctuation, inconsistent citation commands.
8. Hyphenation and terminology consistency.
9. Abstract/conclusion alignment at the wording level.

## Output

Proofreading Report containing:

- **Critical Fixes** / **Major Fixes** / **Minor-Style Fixes** — each a table:
  `Location | Text snippet | Issue | Proposed fix | Confidence`.
- **Consistency Table** — `Term/acronym/notation | Variants found | Recommended form | Action`.
- **LaTeX / Reference Issues** — issue list, or "Not checked."
- **Edit Readiness** — `Safe to apply automatically: yes/no`; `Requires author decision: [bullets]`.

Severity: **Critical** — title/abstract typo, wrong variable, contradiction,
broken citation/ref, grammar that changes meaning. **Major** — awkward/unclear
sentence, undefined term, inconsistent notation, unsupported strong word.
**Minor/style** — concision, local flow, formatting, repeated words that do not
change meaning.

## Reject when

- a proposed edit would change technical meaning;
- asked to add new citations, results, or claims;
- asked to rewrite whole sections (defer to research-write) unless explicitly requested;
- a fix would require fabricating citations or facts;
- in OMX/team contexts, broadening beyond line-level polishing into argument
  review — stay a verifier pass; route to research-review unless the user asks.

## State & Handoff

State: Phase 1 report delivered; Phase 2 edits blocked on user approval, with
Edit Readiness flagging auto-apply vs author-decision items. Next: research-write
(structural rewrites surfaced as "author decision") / research-review
(acceptance risk) / submission. Artifacts: proofreading report only — no claims,
citations, or results are added by this pass.
