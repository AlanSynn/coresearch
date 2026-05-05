---
name: paper-survey
description: Verified literature survey and related-work synthesis for research topics. Use when the user asks for related work, papers on a topic, citation categories, a literature map, novelty risks, survey writing, or paper recommendations. Requires verification of papers and metadata; never fabricates citations or venues.
---

# Paper Survey

Find, verify, classify, and synthesize real papers. Default output is an in-chat Markdown survey. Generate LaTeX, BibTeX, or PDF only when requested.

## Search policy

Use the OMX `researcher` posture when available: official/proceedings/source-backed references first, version/date awareness, and links in the final answer. When current or exact literature matters and web/search tools are available, search and prefer primary sources:

1. paper PDFs, publisher pages, arXiv/OpenReview/ACM/IEEE/official proceedings;
2. DBLP, Semantic Scholar, OpenReview, Google Scholar snippets when accessible;
3. project pages or blogs only as secondary evidence.

Do not cite a paper unless its existence and key metadata are verified. If metadata is uncertain, mark it `PARTIALLY VERIFIED`.

## Workflow

1. **Scope.** Identify topic, venue community, time window, and desired depth. Ask one question only if scope is impossible to infer.
2. **Search broadly.** Use multiple query formulations and adjacent terms.
3. **Verify each candidate.** Confirm title, authors, venue/year, DOI/arXiv/OpenReview/proceedings link when possible.
4. **Classify.** Group by mechanism, research question, or contribution type, not chronology.
5. **Synthesize.** Explain what each stream enabled, what assumptions it makes, and how the user's project differs or builds on it.
6. **Identify risks.** Closest competitors, missing citations, novelty overlap, weak positioning.
7. **Output sources.** Include links used.

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

## Taxonomy
1. [Stream]: [what this stream studies or enables]
2. [Stream]: [what this stream studies or enables]

## Paper Table
| Paper | Authors | Venue/Year | Link | Category | Why it matters | Verification |
|---|---|---|---|---|---|---|

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
```

## Citation integrity checks

Before final output, check:

- no invented title or venue;
- arXiv year is not confused with publication year;
- author list is not guessed;
- claims about a paper's results are supported by its abstract, paper text, or verified metadata;
- any uncertainty is explicitly marked.
