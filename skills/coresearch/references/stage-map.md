# Coresearch Stage Map

Use this when the user starts or re-scopes research.

| Stage | Question | Default route |
|---|---|---|
| Intake | What artifact, field mode, confidentiality, deadline? | `coresearch` + one question if missing |
| Idea | What is the central contribution? | `research-design` |
| Survey | What work is closest and what novelty risk exists? | `research-survey` |
| Design | What claims need evidence? | `research-design` |
| Prototype | What code supports which claim? | `research-engineer` |
| Evidence | What experiment/study/benchmark validates claims? | `research-loop` or `research-engineer` |
| Figures | What visual evidence answers reviewers? | `research-figures` |
| Manuscript | What section needs argument/clarity repair? | `research-write` |
| Review | What score and blockers are likely? | `research-review` |
| Rebuttal | What response can move scores? | `research-rebuttal` |
| Release | Can others reproduce artifacts? | `research-engineer` |

If several stages apply, start at the earliest blocked stage. Do not jump to prose before claim/evidence is clear.

## Analytical stages (router-owned)

These reasoning stages are owned by the Coresearch router and route via `reasoning-skills.md`; each maps to one skill.

| Stage | Question | Default route |
|---|---|---|
| Gap | What is the unsolved problem? | `research-gap` |
| Dialectic | Where do claims conflict? | `research-dialectic` |
| Causal | What causal mechanism holds? | `research-causal` |
| Audit | Is a load-bearing paper sound? | `research-audit` |
| Adversary | What counter-evidence survives? | `research-adversary` |

## Field-mode prompt

When starting research, classify the work before routing:

- AI/ML/CV: formulation, benchmark, baseline, ablation, reproducibility.
- Robotics: embodied task, hardware/sim2real, sensing/action/contact/safety, deployment limits.
- Graphics: representation, visual/physical correctness, authoring control, runtime, failure cases.
- HCI: practice/material context, design space, study/findings, implications, accessibility.
- Hybrid: paired technical claim plus design/workflow claim.
