---
name: research-survey
description: Verified literature survey and related-work synthesis for research topics. Use when the user asks for related work, papers on a topic, citation categories, a literature map, novelty risks, survey writing, or paper recommendations. Requires real-paper verification, research-pdfs-compatible evidence tables when useful, and explicit metadata/PDF confidence; never fabricates citations, venues, or paper claims.
---

# Research Survey

Find, verify, classify, and synthesize real papers. Default output is an in-chat Markdown survey. Generate LaTeX, BibTeX, or PDF only when requested.

## Good for

- Verified related work, literature maps, paper recommendations, novelty-risk analysis, citation categories, and survey prose.
- Finding closest competitors across AI, Robotics, Graphics, HCI, and hybrid fields.
- Producing `research-pdfs`-compatible roadmaps when full-text verification is needed.

## Must do

- Verify paper existence and metadata before citing.
- Assign evidence level: `PDF VERIFIED`, `FULL TEXT VERIFIED`, `METADATA VERIFIED`, `PARTIALLY VERIFIED`, or `NOT FOUND`.
- Synthesize by mechanism, research question, field object, or contribution type; do not list papers chronologically by default.
- Keep metadata-only papers out of detailed method/result/limitation claims.

## Not for

- Batch PDF downloading itself; use `research-pdfs`.
- Paper contribution planning; use `research-design`.
- Fact-checking a fixed draft/source pair; use `research-verify`.

## Search policy

Use the OMX `researcher` posture when available: official/proceedings/source-backed references first, version/date awareness, and links in the final answer. When current or exact literature matters and web/search tools are available, search and prefer primary sources:

1. paper PDFs, publisher pages, arXiv/OpenReview/ACM/IEEE/official proceedings;
2. DBLP, Semantic Scholar, OpenReview, Google Scholar snippets when accessible;
3. project pages or blogs only as secondary evidence.

Do not cite a paper unless its existence and key metadata are verified. If metadata is uncertain, mark it `PARTIALLY VERIFIED`.

## Real-paper and PDF evidence policy

The default standard is **real papers, not inferred papers**. Do not infer a paper's methods, results, venue, or contribution from a title, citation graph, abstract snippet, or model memory alone.

Use explicit evidence levels:

- `PDF VERIFIED` — full text or PDF was retrieved and inspected, and the survey claim is supported by that text.
- `FULL TEXT VERIFIED` — official HTML/full-text page was inspected when no PDF is needed or available.
- `METADATA VERIFIED` — title, authors, venue/year, and source link were verified, but the paper text was not inspected; only make existence, bibliographic, or high-level positioning claims.
- `PARTIALLY VERIFIED` — some metadata is unresolved or conflicting; do not use as a closest-competitor claim without caveat.
- `NOT FOUND` — keep as a candidate or manual-follow-up item; do not cite as established work.

When exactness matters, when the user says not to assume, or when the task asks for a paper list/roadmap, align with `research-pdfs`:

1. Build or request a Markdown roadmap table in the crawler's supported format:

   ```markdown
   | # | 제목 | 저자 | 저널/학회 | 비고 |
   |---|---|---|---|---|
   | 1 | Paper Title | First Author et al. | Venue/Journal | Year; DOI/arXiv/OpenReview/proceedings link |
   ```

2. If a file path is available and downloading is requested or useful for verification, run a dry run first:

   ```bash
   python3 skills/research-pdfs/crawler.py "<path-to-roadmap.md>" --dry-run
   ```

   If this repository path is not current, resolve the crawler relative to the `research-pdfs` skill folder.

3. For real downloads, follow `research-pdfs` guardrails exactly: open-access sources by default, no paywall bypassing, fuzzy DOI matches are candidates only, and lists over 30 papers require reviewed dry-run output plus `--yes-large`.
4. Use downloaded PDFs in `pdf/` next to the roadmap, official full-text pages, or verified source PDFs as the basis for method/result/limitation claims.
5. If the user only requested an in-chat survey and did not request file writes/downloads, do not create files solely for process; instead include a `PDF Crawl Roadmap` table that can be saved and passed to `research-pdfs`.

## Workflow

1. **Scope.** Identify topic, venue community, time window, and desired depth. Ask one question only if scope is impossible to infer.
2. **Search broadly.** Use multiple query formulations and adjacent terms.
3. **Create the evidence ledger.** Record candidates in a `research-pdfs`-compatible roadmap table or equivalent in-chat table before synthesis.
4. **Verify each candidate.** Confirm title, authors, venue/year, DOI/arXiv/OpenReview/proceedings link when possible; assign an evidence level.
5. **Crawl or inspect paper text when needed.** Use `research-pdfs` for batch open-access PDFs when a roadmap file is available; otherwise inspect official PDFs/full text directly. Do not upgrade beyond `METADATA VERIFIED` without paper text.
6. **Classify.** Group by mechanism, research question, or contribution type, not chronology.
7. **Synthesize from evidence.** Explain what each stream enabled, what assumptions it makes, and how the user's project differs or builds on it. Keep metadata-only papers out of detailed result claims.
8. **Identify risks.** Closest competitors, missing citations, novelty overlap, weak positioning.
9. **Output sources.** Include links used and any `research-pdfs` command/output summary when run.

## Inclusion guidance

Do not impose a rigid citation-count threshold unless the user asks. Include:

- directly competing work even if not highly cited;
- foundational work;
- recent or concurrent work;
- strong surveys with useful taxonomies;
- official benchmarks or datasets when relevant.

## Output schema

```markdown
# Literature Map — [Topic]

## Scope
- Topic:
- Venue/community lens:
- Search status: [verified / partial]
- Inclusion rule:
- Evidence standard: [PDF/full-text inspected / metadata-only allowed with caveats]
- research-pdfs status: [not needed / roadmap provided / dry run / downloaded / partial]

## Taxonomy
1. [Stream]: [what this stream studies or enables]
2. [Stream]: [what this stream studies or enables]

## Paper Table
| Paper | Authors | Venue/Year | Link | Category | Why it matters | Evidence level | PDF status |
|---|---|---|---|---|---|---|---|

## PDF Crawl Roadmap
Use this when PDFs should be fetched with `research-pdfs`; omit if no crawl/download workflow is needed.

| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|

## Synthesis by Stream
### [Stream]
[What it enabled, common assumptions, representative papers, and relation to the user's work.]

## Closest Competitors
| Paper | Overlap | Difference | Risk level |
|---|---|---|---|

## Missing Citation Categories
- [Category and why it matters]

## Positioning Recommendation
[How to phrase the contribution without overclaiming.]

## Open Questions
- [Research gap or uncertainty]

## Sources Used
- [Links]

## Verification Notes
- research-pdfs command/output summary if run:
- Metadata-only papers and why:
- Not-found/manual-access papers:
```

## Citation integrity checks

Before final output, check:

- no invented title or venue;
- arXiv year is not confused with publication year;
- author list is not guessed;
- claims about a paper's results are supported by its abstract, paper text, or verified metadata;
- method/result/limitation claims are not made from metadata-only papers;
- fuzzy `research-pdfs` or DOI matches are not treated as verified papers;
- papers that `research-pdfs` reports as not found are not cited as established evidence unless independently verified elsewhere;
- local PDFs or official full text were actually inspected before marking `PDF VERIFIED` or `FULL TEXT VERIFIED`;
- any uncertainty is explicitly marked.
