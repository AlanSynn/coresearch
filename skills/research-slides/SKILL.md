---
name: research-slides
description: Academic research presentation workflow. Use when the user asks for slides, a talk, a deck, Beamer, PowerPoint, keynote structure, conference presentation, thesis defense, interview talk, group meeting, or to convert a paper, abstract, results, or notes into a clear research presentation.
---

# Research Slides

Create research talks that preserve the paper's evidence and contribution without overloading slides. Default output is a slide plan and slide text in chat. Generate `.tex`, `.pptx`, or files only when requested. In OMX workflows, treat the deck as a derived artifact from verified paper claims, not a new source of claims.

If the user asks for a finished `.pptx` deck, keep this skill responsible for research narrative, claim calibration, and slide structure, then route mechanics:

- Prefer `pptx` when the priority is finished PowerPoint mechanics, Claude-style `.pptx` execution, template editing, visual polish, or robust PowerPoint QA.
- Use `academic-ppt` when the priority is paper-faithful extraction from LaTeX/PDF, equation-heavy academic dossiers, or defense-style source fidelity.
- For the best result, produce a compact claim-faithful slide brief here, then hand it to `pptx` for build/render/QA; Claude delegation follows `pptx`'s external delegation gate.

## Good for

- Research talk outlines, slide titles as claims, speaker notes, Beamer drafts, conference talks, thesis defenses, interviews, and group meetings.
- Converting paper claims, figures, and evidence into a clear audience-specific narrative.
- Preparing a claim-faithful plan before `.pptx` generation.

## Must do

- Preserve paper claims and evidence; slides are derived artifacts, not new claims.
- Use one claim per slide and put the takeaway in the title when possible.
- Identify figures/assets needed and density risks.
- Route finished `.pptx` mechanics to `pptx`; Claude handoff follows `pptx`'s external delegation gate. Use `academic-ppt` for paper-faithful/equation-heavy builds.

## Not for

- Low-level PowerPoint mechanics by default.
- Decorative slide generation without a research narrative.
- Inventing results, visuals, or claims to make slides look complete.

## Inputs

Use the paper, abstract, notes, figures, results, venue, audience, and talk length. If talk length is missing, assume:

- 5 minutes: 5–7 slides;
- 10–15 minutes: 8–14 slides;
- 30 minutes: 18–25 slides;
- defense: 35–55 slides depending on norms.

## Academic presentation spine

1. Audience contract: who is listening and what background they need.
2. Background: minimum concepts needed for the argument.
3. Problem stakes: why the field should care.
4. Tension/gap: what existing approaches cannot explain, compute, support, or scale.
5. Key insight/thesis: one sentence the talk proves.
6. Method/system/study logic: how the work makes the thesis plausible.
7. Evidence sequence: main result, comparisons, ablations, examples, studies, or failures.
8. Limitations and scope.
9. Takeaway and future direction.

## Slide rules

- One claim per slide.
- Put the takeaway in the title when possible.
- Use figures as evidence, not decoration.
- Avoid paragraphs; use keywords and speaker notes for nuance.
- Do not add unsupported claims or results.
- For interdisciplinary audiences, define terms before using them as arguments.

## Argument-first deck rules

Default to academic persuasion, not a visual theme:

- Background slides earn attention; they are not literature dumps.
- Gap slides create tension; they explain why current options fail or remain incomplete.
- Thesis slides state the talk's promise in one memorable sentence.
- Method slides show logic and trust path, not every implementation detail.
- Evidence slides prove claims with figures, examples, studies, comparisons, ablations, or failure cases.
- Limitation slides increase credibility by bounding claims.
- Visual polish is subordinate to argument clarity: hierarchy, contrast, readable figures, and claim-title alignment matter more than motif.
- Field tone changes evidence emphasis, not the spine: AI/Robotics/Graphics/HCI decks still need background → gap → thesis → method → evidence → limits → takeaway.

## Finished `.pptx` QA handoff

When `pptx` or another deck builder generates or edits a `.pptx`, require the checks below. If the builder is Claude/`ask-claude`, apply `pptx`'s external delegation gate first:

1. text extraction check for missing content, wrong order, typos, and placeholder residue;
2. rendered slide images or thumbnails;
3. visual bug hunt for overflow, overlap, contrast, edge margins, cramped spacing, unreadable figures, and claim drift;
4. at least one fix-and-verify cycle for affected slides;
5. final statement of unresolved deck risks.

## Output schema

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

## Optional Beamer guidance

When generating LaTeX Beamer:

- keep a clean academic theme;
- define colors semantically;
- avoid dense equations unless the audience needs them;
- include speaker notes as comments if requested;
- compile and report the command if files are generated.
