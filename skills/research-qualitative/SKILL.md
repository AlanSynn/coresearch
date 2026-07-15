---
name: research-qualitative
description: Qualitative Evidence Synthesizer. Transform raw qualitative evidence into defensible themes preserving provenance and negative cases. Two phases - structure (unitize, code, memo, coverage) then synthesize (consolidate, categorize, theme, negative-case, relate, saturation). Frequency is reportable, never a vote or importance.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/qualitative/codebook.yaml
  - docs/research/qualitative/themes.md
---

# research-qualitative — Qualitative Evidence Synthesizer

Turn raw excerpts into themes that make an analytical claim. Provenance and
negative cases survive the whole way. Frequency is reportable — never importance.

## What & When

Phase 1 structures evidence with analytical codes; phase 2 synthesizes into
themes grounded in excerpts. Use for interview/observation/open-response coding,
themes that survive a skeptic with the raw excerpts, a design claim resting on
qualitative evidence. Not for: mapping published literature → research-survey;
quantitative/empirical synthesis → research-dialectic.

## Procedure

**Phase 1 — Structure.** Unitize (excerpt_id, participant_or_source, session,
timestamp/location, raw_text, context, research_question). Initial coding:
short analytical labels NOT summaries ("assembly ambiguity", not "participant
had difficulty"). Code memo: code, definition, include_when, exclude_when,
example_excerpts, counterexamples. Coverage: participants/sessions/excerpts/
diversity/intensity/negative cases — frequency reportable, NOT a vote, NOT importance.

**Phase 2 — Synthesize.** Consolidate (merge synonyms, split over-broad).
Categorize by mechanism/phenomenon, not topic similarity. Theme = analytical
claim. Negative-case: who did not express it; revise scope. Relate:
causal/sequential/hierarchical/reinforcing/contradictory/conditional. Saturation:
code saturation, meaning saturation, groups covered, where new evidence kept
changing interpretation — never claim universal saturation.

## Output

- Research Question
- Data Coverage (participants, sessions, excerpts, diversity, negative cases)
- Codebook (codes + memos)
- Theme N, each with mandatory `analytical_claim:` (a claim, NOT a topic label —
  e.g. "Teachers treated assembly ambiguity as classroom-management risk", not
  "Assembly") + supporting codes + representative evidence + participants/contexts
  + negative cases + boundary conditions + implication
- Relationships Among Themes
- Alternative Interpretations
- Saturation and Coverage
- Design/Research Implications

Confidence three-dim per theme; coverage usually the binding dimension.

## Reject when (gates 2,6,9)

- theme is only a topic label (no `analytical_claim`);
- one isolated excerpt;
- overgeneralized wording;
- contradictory cases omitted;
- frequency used as importance;
- analyst interpretation written as participant speech;
- quotes detached from context;
- groups merged without justification;
- too few excerpts/participants → keep at code/category level, do not promote to theme.

## State & Handoff

State: artifacts (codebook.yaml, themes.md) written; unsupported design claims to
`quality_state.unresolved_methodology_issues`; saturation limits logged. Next:
research-adversary (challenge themes) / research-dialectic (conflict with
literature). Artifacts: codebook.yaml +
themes.md.

Re-entry: return to `coresearch` to re-route the next stage.
