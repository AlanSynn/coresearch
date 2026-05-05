---
name: paper-figures
description: Research figure planning and caption architecture. Use when the user asks what figures a paper needs, how to improve figures, how to design a pipeline diagram, result gallery, ablation table, study figure, teaser, or captions. Connects every figure to a claim and reviewer question.
---

# Paper Figures

Design figures as evidence, not decoration. Every figure should support at least one claim and answer a likely reviewer question.

## Workflow

1. Identify the paper's central claim and venue mode.
2. List claims that need visual or tabular support.
3. Choose figure types: teaser, pipeline, representation, comparison, ablation, result gallery, failure case, study protocol, qualitative findings, benchmark table.
4. Define panels and assets.
5. Write caption theses that state the takeaway.
6. Identify figure risks: cherry-picking, unreadability, missing baseline, unsupported generality.

## Figure types by venue

- **Graphics:** teaser, method pipeline, representation, visual comparisons, ablations, galleries, failure cases, runtime/scalability plots.
- **AI/ML/CV:** method diagram, benchmark table, ablation plot, scaling plot, error analysis, qualitative examples, dataset split/coverage figure.
- **HCI/UIST/CHI:** workflow figure, design space, system architecture, study procedure, artifact examples, findings diagram, participant/task overview.

## Output schema

```markdown
# Figure Plan

## Figure Strategy
- Venue mode:
- Central claim:
- Main visual evidence gap:

## Figure Table
| # | Figure | Claim supported | Type | Panels / assets | Caption thesis | Reviewer question answered | Risk |
|---:|---|---|---|---|---|---|---|

## Caption Drafts
### Figure [#]
[Caption with one-sentence takeaway first, then panel explanations.]

## Missing Assets
- [Asset, source, or experiment needed]

## Risks to Avoid
- [Cherry-picking / too dense / missing baseline / unsupported caption claim]
```

## Guardrails

- Do not imply a result exists unless supplied.
- Mark planned or hypothetical figures clearly.
- Keep captions claim-calibrated.
