# Artifact Companion Routing

Use this when the research output involves `.docx`, `.pdf`, `.pptx`, `.xlsx`, frontend design, or shareable web artifacts. Coresearch owns research content and claim integrity. `pptx` is owned by Coresearch; other companion skills/tools own their format mechanics when installed.

## Common artifact skeleton

For file artifacts, follow:

```text
inspect → transform/build → render/export → validate → fix once if needed
```

Never treat a file as done until the format-specific validation step has run or an explicit blocker is reported.

## Quick route table

| User need | Coresearch role | Companion route |
|---|---|---|
| Word manuscript, reviewer response, DOCX edits | Preserve claims, comments, and research meaning | `docx` when `.docx` IO/editing is explicit |
| Generic PDF extraction/edit/merge/OCR | Verify content and citation/source faithfulness | `pdf`; use `research-pdfs` only for open-access literature crawl |
| Talk plan or slide narrative | `research-slides` creates claim-faithful plan | owned `pptx` for finished PowerPoint mechanics and authorized/redacted Claude `pptx` delegation; `academic-ppt` only for paper-faithful/equation-heavy builds |
| Results workbook, benchmark sheet, study coding table | `research-engineer` / `research-verify` defines data/contracts | `xlsx` for spreadsheet formulas/formatting/recalc |
| Research demo UI or website | `research-engineer` owns architecture, `research-figures` owns evidence visuals | `frontend-design` / `frontend-skill` for UI quality |
| Shareable interactive artifact | Define research claim, data provenance, reproducibility | `web-artifacts-builder` for bundle/export pipeline |

## Critical validation by artifact type

- **DOCX:** preserve page setup, lists, tables, tracked changes/comments if relevant; validate by opening/unpacking or using the companion’s validator.
- **PDF:** distinguish text extraction from visual layout; check pages, glyphs, equations, and source fidelity; do not bypass paywalls.
- **PPTX:** use owned `pptx` for PowerPoint creation/editing, academic argument spine checks, Claude `pptx` delegation, and visual QA; Claude/external delegation requires explicit user authorization or a redacted mechanics-only brief. Use `academic-ppt` for LaTeX/PDF extraction, equations, and source-faithful defense decks. Render slides to images or thumbnails, inspect for placeholder text, overflow, broken fonts, unreadable figures, and claim drift.
- **XLSX:** preserve formulas rather than hardcoding outputs; recalc when possible; check for formula errors, broken references, hidden-sheet assumptions, and template damage.
- **Frontend/web artifacts:** build and smoke-test; make design subject-grounded, not generic; verify accessibility basics and exportability.

## Design anti-slop rules

Visual and interactive artifacts must encode the research subject:

- hero/teaser = thesis, not decoration;
- motif, typography, palette, and motion come from domain content;
- one visual claim per slide/screen;
- no generic purple gradients, default cards, empty dashboard chrome, or decorative charts without evidence.

For research decks, use an argument-first academic structure: audience/background → gap/tension → thesis → method logic → evidence sequence → limits → takeaway. Visual polish must serve this spine. When Claude's `pptx` skill is stronger for file mechanics, route through `pptx`/`ask-claude` only after explicit authorization, or pass a redacted mechanics-only brief; otherwise use local tools.
