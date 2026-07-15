---
name: research-figures
description: Research figure planning and caption architecture. Use when the user asks what figures a paper needs, how to improve figures, how to design a pipeline diagram, result gallery, ablation table, study figure, teaser, or captions. Connects every figure to a claim and reviewer question.
---

# research-figures — Figure Plan & Caption Architecture

Design figures as evidence, not decoration: each supports a claim and answers a
reviewer question. Plans only — rendering hands off once the plan is approved.

## What & When

Teasers, pipelines, representations, comparison figures, ablation plots, result
galleries, failure cases, study figures, tables, and captions. Use when: "what
figures does this paper need", "improve these figures", "design the pipeline
diagram / result gallery / ablation table / teaser", "write captions". Not for:
slide-deck structure (user-owned via external tools).

## Procedure

1. State the central claim and venue (field) mode before choosing figures.
2. List claims that need visual or tabular support.
3. Give each figure one caption thesis and one reviewer question it answers.
4. Choose figure type; define panels and assets.
5. Write captions that lead with a one-sentence takeaway, then panel explanations.
6. Identify risks: cherry-picking, unreadability, missing baseline, unsupported generality.

Figure types by field mode:

- **Graphics:** teaser, method pipeline, representation, visual comparisons, ablations, galleries, failure cases, runtime/scalability plots.
- **AI/ML/CV:** method diagram, benchmark table, ablation plot, scaling plot, error analysis, qualitative examples, dataset split/coverage figure.
- **Robotics:** system photo, task setup, sensing/action loop, hardware trial summary, sim-to-real comparison, reset/safety diagram, failure/tolerance plot.
- **HCI/UIST/CHI:** workflow figure, design space, system architecture, study procedure, artifact examples, findings diagram, participant/task overview.

## Output

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

Mandatory: every row binds the figure to `Claim supported`, `Caption thesis`,
and `Reviewer question answered` — none bound means decoration; cut or rebind.

## Reject when

- a figure supports no claim and answers no reviewer question (decoration);
- a caption asserts a result not supplied or implied only by the visual;
- planned, hypothetical, or missing-asset figures are not marked clearly;
- a caption thesis is missing or buries the takeaway below panel detail.

## State & Handoff

State: plan marked `planned`; Missing Assets are build blockers. Next: plotting
or repo-native implementation once approved;
research-audit (claim↔figure alignment). Artifacts: Figure Plan md above.
Carry forward Missing Assets and Risks as warnings.

Re-entry: return to `coresearch` to re-route the next stage.
