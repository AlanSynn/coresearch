---
name: research-slides
description: Academic research presentation workflow. Use when the user asks for slides, a talk, a deck, Beamer, PowerPoint, keynote structure, conference presentation, thesis defense, interview talk, group meeting, or to convert a paper, abstract, results, or notes into a clear research presentation.
---

# Research Slides

Create research talks that preserve the paper's evidence and contribution without overloading slides. Default output is a slide plan and slide text in chat. Generate `.tex`, `.pptx`, or files only when requested.

## Inputs

Use the paper, abstract, notes, figures, results, venue, audience, and talk length. If talk length is missing, assume:

- 5 minutes: 5–7 slides;
- 10–15 minutes: 8–14 slides;
- 30 minutes: 18–25 slides;
- defense: 35–55 slides depending on norms.

## Narrative spine

1. Problem and audience stakes.
2. Core difficulty.
3. Key idea or system workflow.
4. Method details needed to trust the work.
5. Evidence: results, study findings, examples, ablations, or case studies.
6. Limitations and scope.
7. Takeaway and future direction.

## Slide rules

- One claim per slide.
- Put the takeaway in the title when possible.
- Use figures as evidence, not decoration.
- Avoid paragraphs; use keywords and speaker notes for nuance.
- Do not add unsupported claims or results.
- For interdisciplinary audiences, define terms before using them as arguments.

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
