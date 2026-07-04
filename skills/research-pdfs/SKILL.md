---
name: research-pdfs
description: Batch-download open-access PDFs for papers listed in a markdown research roadmap or paper list. Use when the user asks to fetch PDFs, crawl PDFs from a markdown file, or download open-access papers from a verified list. Runs the bundled crawler script when appropriate and avoids paywall-circumvention fallbacks by default.
---

# Research PDFs

Download open-access PDFs for papers listed in a Markdown table. This is an optional utility skill, not a core paper-writing workflow.

`research-survey` may emit a compatible roadmap table when a literature survey needs PDF-backed evidence. Preserve the crawler's output categories so `research-survey` can distinguish `PDF VERIFIED`, metadata-only, fuzzy, and not-found papers instead of assuming paper content.

## Good for

- Batch downloading open-access PDFs from a verified Markdown paper list.
- Producing local PDFs for later `research-survey` or `research-verify` inspection.
- Keeping fuzzy/not-found/open-access status explicit.

## Must do

- Dry-run before large or uncertain crawls.
- Avoid paywall bypass and treat publisher PDF extraction as opt-in.
- Preserve downloaded, skipped, fuzzy, and not-found categories.
- State that downloaded PDFs prove access only, not claim correctness.

## Not for

- Generic PDF editing/OCR/merge/split; route to a `pdf` companion if installed.
- Literature synthesis; use `research-survey`.
- Treating fuzzy DOI or metadata matches as verified evidence.

## Supported input

A Markdown file with paper rows. The bundled crawler works best with tables containing Korean headers:

```markdown
| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|
```

It extracts title, authors, venue/journal, and year from `비고`.

## Workflow

1. Confirm the Markdown path if ambiguous.
2. For lists larger than 30 papers, the script refuses real downloads until a dry run has been reviewed and `--yes-large` is supplied.
3. Use verified open-access sources by default: arXiv, eLife, bioRxiv, and Semantic Scholar `openAccessPdf`.
4. Treat fuzzy DOI matches as not downloadable by default.
5. Save PDFs into `pdf/` next to the Markdown file.
6. Report downloaded, skipped, fuzzy, and not-found papers.

## Invocation

```bash
python3 skills/research-pdfs/crawler.py "<path-to-roadmap.md>" --dry-run
python3 skills/research-pdfs/crawler.py "<path-to-roadmap.md>"
python3 skills/research-pdfs/crawler.py "<path-to-roadmap.md>" --yes-large
```

Publisher landing-page `citation_pdf_url` lookup is opt-in only:

```bash
python3 skills/research-pdfs/crawler.py "<path-to-roadmap.md>" --allow-publisher-pdf
```

If this repository path is not current, resolve the script relative to this skill folder.

## Output summary

```markdown
# PDF Crawl Result
- Input:
- Output folder:
- Downloaded:
- Already existed:
- Fuzzy matches requiring verification:
- Not found / manual access needed:
- Command run:
```

## Guardrails

- Do not bypass paywalls.
- Prefer arXiv, bioRxiv, eLife, Semantic Scholar `openAccessPdf`, or institutional/manual access notes.
- Use `--allow-publisher-pdf` only when publisher landing-page PDF extraction is appropriate for the user's access context.
- Treat fuzzy DOI matches as candidates, not verified papers; the script does not download DOI-derived PDFs from fuzzy matches by default.
- A downloaded or already-existing PDF only proves local access; paper claims still require reading the PDF or official full text.
- Not-found papers remain manual-follow-up items unless independently verified from primary metadata or official sources.
