---
name: research-figures
description: Research figure planning and caption architecture. Use when the user asks what figures a paper needs, how to improve figures, how to design a pipeline diagram, result gallery, ablation table, study figure, teaser, or captions. Connects every figure to a claim and reviewer question.
---

# Research Figures

Design figures as evidence, not decoration. Every figure should support at least one claim and answer a likely reviewer question. If actual figure generation is requested, hand off to an appropriate plotting/image skill or repository-native implementation after the figure plan is approved.

## Good for

- Teasers, pipelines, representations, comparison figures, ablation plots, result galleries, failure cases, study figures, tables, and captions.
- Connecting every visual to a claim, evidence artifact, and reviewer question.
- Planning Graphics, AI, Robotics, HCI, or hybrid figure narratives before plotting.

## Must do

- State the central claim and field mode before choosing figures.
- Give each figure one caption thesis and one reviewer question it answers.
- Mark missing assets, planned experiments, or hypothetical visuals clearly.
- Validate that figures are evidence, not decoration.

## Not for

- Actual plotting/rendering/image generation unless the user asked and repo tools are clear.
- Inventing results, screenshots, studies, or qualitative findings.
- Slide-deck structure; use `research-slides`.

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
- **Robotics:** system photo, task setup, sensing/action loop, hardware trial summary, sim-to-real comparison, reset/safety diagram, failure/tolerance plot.
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
