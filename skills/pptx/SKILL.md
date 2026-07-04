---
name: pptx
description: Coresearch-owned PowerPoint workflow for creating, reading, editing, modernizing, rendering, and QA-checking .pptx decks. Use whenever a .pptx file is input or output, when the user asks for slides/deck/presentation with finished PowerPoint mechanics, when editing templates or existing decks, or when a research deck needs academic argument structure plus release validation.
---

# PPTX

Own finished PowerPoint mechanics and release QA. For research content, preserve the claim-faithful plan from `research-slides`; do not invent claims, evidence, figures, citations, or results to make a deck look complete.

This skill is meta-first: good decks are persuasive academic arguments, not topic mood boards. Visual style must serve the argument spine.

## Good for

- Creating finished `.pptx` decks from a slide plan, notes, paper outline, or existing template.
- Reading, summarizing, editing, merging, splitting, or repairing existing `.pptx` files.
- Turning a research talk plan into a PowerPoint artifact with academic argument flow, clear hierarchy, and render QA.
- Optional Claude `pptx` delegation through the external delegation gate, while Coresearch keeps claim/narrative validation.

## Must do

- Inspect inputs before editing: extract text, inspect template/layouts, and render thumbnails or slide images when possible.
- Preserve academic presentation structure: background → tension/gap → thesis/insight → method → evidence → limits → takeaway.
- Keep one claim per slide; title should usually state the takeaway.
- Prefer concise slide briefs and checklists over verbose prompt blocks.
- Use Claude `pptx` / Claude agent routes only through the external delegation gate below.
- Render or export the deck for visual QA before declaring success.
- Run at least one fix-and-verify cycle when QA finds issues.

## Not for

- Designing the paper contribution or evidence plan; use `research-design`.
- Building the research talk narrative from scratch; use `research-slides` first unless user already gave a complete slide brief.
- LaTeX/PDF/equation-heavy source-faithful academic extraction; prefer `academic-ppt` when installed.
- Fabricating missing data, figures, citations, or paper claims.

## Quick reference

| Task | Default path |
|---|---|
| Read deck content | `python -m markitdown deck.pptx` if available; otherwise inspect with `python-pptx` or unzip OOXML |
| Visual overview | convert to PDF/images with LibreOffice + Poppler, or use platform thumbnail tools |
| Edit existing deck | inspect template → edit copy → render → QA → fix |
| Create from scratch | slide brief → external delegation gate or local `pptxgenjs`/`python-pptx` → render QA |
| Template-based deck | analyze layouts/placeholders first; preserve master styles unless user asks to redesign |
| Academic research deck | preserve argument spine; use visuals as evidence, not decoration |

## External delegation gate

Treat Claude's document/plugin `pptx` skill as an optional mechanics engine, not an automatic route. Send content/files to Claude, `ask-claude`, `ask`, or other external tools only when:

- the user explicitly authorizes external delegation for those files/content; or
- the packet is redacted to mechanics-only with no unpublished, private, or confidential source content.

Otherwise, build locally with the same QA gate.

Default delegation packet:

```markdown
# PPTX Build/Edit Brief

Goal: [new deck / edit deck / QA deck]
Audience:
Talk length / slide budget:
Input files:
Output path:
Academic spine:
1. Background/stakes:
2. Gap/tension:
3. Thesis/key insight:
4. Method/system:
5. Evidence sequence:
6. Limits:
7. Takeaway:

Slide table:
| # | Claim title | Purpose | Visual/evidence | Speaker note |
|---:|---|---|---|---|

Must preserve:
- [claims, numbers, citations, figures]

QA required:
- text extraction
- render thumbnails/images
- overflow/contrast/placeholder check
- fix and re-render affected slides
```

How to invoke:

- In Claude runtime: invoke the local `pptx` skill only after the gate passes.
- In Codex/OMX: use `ask-claude` or `ask` only after the gate passes; request artifact path plus QA notes back.
- If Claude is unavailable or the gate fails, build locally with installed tools and keep the same QA gate.

Do not copy proprietary Claude skill text into Coresearch. Treat Claude `pptx` as an external engine, not a prompt source.

## Academic presentation architecture

Use this spine unless the user provides a better one:

1. **Audience contract.** Who is in the room, why this matters, how much background they need.
2. **Background.** Minimal concepts needed to understand the problem.
3. **Tension/gap.** What current methods/tools/studies cannot explain, compute, support, or scale.
4. **Thesis/key insight.** One memorable sentence: “We show/build/find X by doing Y, enabling Z.”
5. **Approach logic.** The method/system/study pipeline, shown as cause-effect, not implementation dump.
6. **Evidence sequence.** Main result first, then comparisons, ablations, examples, studies, failures as needed.
7. **Boundary.** Limitations, failure modes, assumptions, ethics, or deployment scope.
8. **Takeaway.** What should the audience believe, reuse, or remember.

Field tone changes evidence emphasis, not the spine:

- AI/ML/CV: formulation, baselines, ablations, error analysis, reproducibility.
- Graphics: representation, algorithm/pipeline, visual quality, comparisons, runtime, limitations.
- Robotics: task/platform, sensing/action/contact, safety, resets, failures, sim-to-real.
- HCI: audience/practice, design rationale, interaction, study/findings, implications, accessibility.
- Hybrid: technical claim and human/workflow claim must both be visible.

## Slide roles

Use these roles to avoid generic decks:

- setup slide: defines audience stakes and terms;
- contrast slide: old way vs new tension;
- thesis slide: one central claim;
- mechanism slide: how the system/method works;
- evidence plate: figure/table/example as proof;
- comparison slide: why this is better/different;
- ablation/failure slide: what matters and what breaks;
- implication slide: what changes for field/practice;
- recap slide: compress section into one remembered point.

## Layout rules

- Slide title = claim, not label, unless it is a section divider.
- Use varied layouts: full-figure evidence, side-by-side comparison, process strip, annotated diagram, result plate, table-to-takeaway.
- Avoid text-only slides except title, agenda, and section breaks.
- Left-align body text; use large readable labels and direct annotations.
- Keep margins generous and hierarchy obvious.
- Captions explain why the visual matters, not what it is.
- Speaker notes hold nuance; slides hold claims and evidence.

## Tool choices

Use installed tools; do not add dependencies unless necessary.

- `markitdown[pptx]`: text extraction.
- `python-pptx`: reliable basic creation/editing, text boxes, images, shapes, notes-adjacent inspection.
- `pptxgenjs`: richer from-scratch deck generation when Node tooling is available.
- LibreOffice `soffice`: convert `.pptx` to PDF for render checks.
- Poppler `pdftoppm`: convert PDF pages to slide images.
- Raw OOXML unzip/edit/rezip: only for features libraries cannot represent; keep a backup.

## Workflow

1. **Clarify artifact state.** New deck, existing deck edit, template fill, merge/split, or QA-only.
2. **Inspect.** Extract text; inspect slide count, order, layouts, notes/comments if relevant; render overview when possible.
3. **Check academic spine.** If missing, ask `research-slides` for a compact slide brief or derive one from provided claims.
4. **Choose mechanics engine.** External delegation gate or local `pptxgenjs`/`python-pptx`.
5. **Build or edit a copy.** Never destroy the only input file.
6. **Render.** Export to PDF/images or thumbnails.
7. **QA.** Check content order, placeholders, overflow, collisions, contrast, margins, unreadable figures, broken equations, and claim drift.
8. **Fix and verify.** Re-render affected slides after fixes.
9. **Report release state.** Output path, checks run, defects fixed, unresolved risks.

## Content QA

Before visual QA, check text content:

```bash
python -m markitdown output.pptx > /tmp/deck-text.txt
```

Then scan for:

- missing sections or wrong slide order;
- leftover placeholders such as `lorem`, `xxx`, `TODO`, `subtitle`, `insert`, `placeholder`;
- copied template text;
- unsupported claim wording;
- mismatched figure/table numbers;
- citations or provenance removed by accident.

## Visual QA

Render when tools are available:

```bash
soffice --headless --convert-to pdf --outdir /tmp output.pptx
pdftoppm -jpeg -r 150 /tmp/output.pdf /tmp/slide
```

Inspect images for:

- overlap, cropped text, wrapped titles, or off-slide elements;
- low contrast and tiny labels;
- figures too small to interpret;
- inconsistent alignment, spacing, or margins;
- decorative shapes competing with evidence;
- repeated layouts that make the talk feel generic;
- broken equations, missing glyphs, missing images;
- claim drift between title, visual, and speaker note.

Use a fresh-eye reviewer/subagent for non-trivial decks when available.

## Output schema

```markdown
# PPTX Result

## Artifact
- Input:
- Output:
- Mode: [new / edit / template / merge / QA]
- Mechanics engine: [Claude pptx / local python-pptx / local pptxgenjs / other]

## Academic Spine
- Background:
- Gap/tension:
- Thesis:
- Evidence sequence:
- Takeaway:

## Checks
| Check | Result | Evidence |
|---|---|---|

## Fixed Issues
- [Issue fixed]

## Remaining Risks
- [Unresolved defect, missing asset, or manual check]
```

## Guardrails

- Do not overwrite the input deck without explicit instruction.
- Do not bypass claim/evidence validation to improve aesthetics.
- Do not use generic corporate templates unless the user asks.
- Do not add new dependencies for simple edits that existing tools can handle.
- Do not declare success from code generation alone; inspect the rendered deck.
- Do not send any deck/source content or files to Claude/`ask-claude`/external tools without explicit user authorization; if authorization is absent, use local tools or a redacted mechanics-only brief.
