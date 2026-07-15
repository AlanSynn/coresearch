---
name: research-slides
description: Academic research presentation workflow. Use when the user asks for slides, a talk, a deck, Beamer, PowerPoint, keynote structure, conference presentation, thesis defense, interview talk, group meeting, or to convert a paper, abstract, results, or notes into a clear research presentation.
---

# research-slides — Academic Research Presentation

Build research talks that preserve a paper's evidence and contribution without overloading slides — a derived artifact from verified claims, not a new source of claims. Default: slide plan + slide text in chat; `.tex`/`.pptx`/files only when requested.

## What & When

Outlines, claim-titled slides, speaker notes, Beamer drafts, conference talks,
thesis defenses, interviews, group meetings; paper claims/figures/evidence into an audience-specific narrative; a claim-faithful plan before `.pptx`. Not for: low-level PowerPoint mechanics by default; decorative slides without a narrative. Inputs: paper, abstract, notes, figures, results, venue, audience, length — if missing assume 5 min → 5–7 slides, 10–15 min → 8–14, 30 min → 18–25, defense → 35–55.

## Procedure

1. **Audience contract** — who is listening and what background they need.
2. **Background** — minimum concepts needed for the argument.
3. **Problem stakes** — why the field should care.
4. **Tension/gap** — what existing approaches cannot explain, compute, support, or scale.
5. **Key insight/thesis** — one sentence the talk proves.
6. **Method/system/study logic** — how the work makes the thesis plausible.
7. **Evidence sequence** — main result, comparisons, ablations, examples, studies, or failures.
8. **Limitations and scope.**
9. **Takeaway and future direction.**

**Slide rules** — one claim per slide; takeaway in the title when possible; figures as evidence, not decoration; no paragraphs (keywords + speaker notes carry nuance); no unsupported claims or results; define terms before wielding them as arguments for interdisciplinary audiences.

**Argument-first deck rules** — default to academic persuasion, not a visual theme:

- Background slides earn attention; they are not literature dumps.
- Gap slides create tension; they explain why current options fail or remain incomplete.
- Thesis slides state the talk's promise in one memorable sentence.
- Method slides show logic and trust path, not every implementation detail.
- Evidence slides prove claims with figures, examples, studies, comparisons, ablations, or failure cases.
- Limitation slides increase credibility by bounding claims.
- Visual polish is subordinate to argument clarity: hierarchy, contrast, readable figures, and claim-title alignment matter more than motif.
- Field tone changes evidence emphasis, not the spine: AI/Robotics/Graphics/HCI decks still need background → gap → thesis → method → evidence → limits → takeaway.

**Finished `.pptx` mechanics** — this skill owns research narrative, claim calibration, and slide structure; route build/render/QA to the Claude `pptx` companion (`academic-ppt` for paper-faithful LaTeX/PDF/equation-heavy builds). Produce a compact claim-faithful brief here first. When a companion or builder generates/edits a `.pptx`, require the QA handoff:

1. text extraction check for missing content, wrong order, typos, and placeholder residue;
2. rendered slide images or thumbnails;
3. visual bug hunt for overflow, overlap, contrast, edge margins, cramped spacing, unreadable figures, and claim drift;
4. at least one fix-and-verify cycle for affected slides;
5. final statement of unresolved deck risks.

## Output

```markdown
# Research Talk Plan

## Talk Assumptions
- Audience:
- Length:
- Venue/context:
- Core takeaway:

## Slide Outline
| # | Title as claim | Purpose | Visual/evidence | Speaker note |
|---:|---|---|---|---|

## Full Slide Draft
### Slide 1 — [Title]
- [On-slide bullets]
Speaker note: [What to say]
Visual: [Figure/table/diagram]

[Repeat]

## Figure and Asset Needs
- [Needed figure, table, diagram, or animation]

## Risks
- [Claim that needs evidence]
- [Slide likely too dense]
```

## Reject when

- decorative slides with no research narrative, or inventing results/visuals/claims to look complete;
- a slide carries an unsupported claim or result;
- a finished `.pptx` is emitted without the QA handoff checks above.

## State & Handoff

No ledger by default; the Research Talk Plan is the handoff artifact. Next: Claude `pptx` companion for `.pptx` build/render/QA; `academic-ppt` for paper-faithful LaTeX/PDF; Beamer — clean academic theme, semantic colors, dense equations only if the audience needs them, speaker notes as comments if requested, compile and report the command when files are generated.
