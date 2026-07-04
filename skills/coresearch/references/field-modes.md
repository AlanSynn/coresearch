# Field Modes and Narrative Spines

Use this when routing `research-design`, `research-write`, `research-review`, `research-figures`, or `research-engineer`. Pick one primary mode and, when needed, one secondary mode.

## AI / ML / CV — technical systems mode

Good for learning, optimization, perception, generation, representation, or benchmark-driven work.

Narrative spine:

```text
technical task → operational bottleneck → method/mechanism → metrics/baselines/ablations → limits/reproducibility
```

Must foreground formulation, assumptions, datasets/splits, baselines, compute, seeds, ablations, error analysis, limitations, and responsible-use boundaries.

## Robotics — embodied deployment mode

Good for physical systems, control, manipulation, locomotion, sim-to-real, fabrication-to-actuation, or robot design.

Narrative spine:

```text
embodied task → contact/sensing/action/safety bottleneck → control/design mechanism → hardware or realistic-sim evidence → deployment limits
```

Must foreground robot/platform, task environment, resets, safety, calibration, sensor/actuator constraints, morphology-control coupling, sim2real assumptions, hardware trials, failures, and reproducibility.

## Graphics / Visual Computing — representation and artifact mode

Good for geometry, simulation, rendering, animation, character motion, physical fabrication, visual authoring, or computational design.

Narrative spine:

```text
visual/physical/authoring challenge → representation bottleneck → computational method → visual/physical evidence → failure cases and runtime
```

Must foreground representation, geometric/physical correctness, visual quality, controllability, comparisons, ablations, galleries, runtime/memory, implementation detail, and failure cases.

## HCI / Technical HCI — design-computing mode

Good for creative tools, workflows, studies, tangible interaction, fabrication, education, end-user programming, or human-centered systems.

Narrative spine:

```text
practice/material/context → underexplored design opportunity → toolkit/system/artifact → examples/study/findings → implications
```

Must foreground audience, practice, material constraints, design rationale, user agency, artifacts made, study protocol or design process evidence, qualitative themes, accessibility, ethics, and scoped implications.

## Hybrid mode — dual-claim contract

Use for Graphics+HCI, AI+HCI, Robotics+HCI, or design-computing systems with technical mechanisms.

Do not average tones. Sequence them:

1. Start with human/material/creative practice.
2. Narrow to a concrete technical bottleneck.
3. State two linked claims:
   - technical claim: what the system computes, generates, optimizes, controls, or fabricates under constraints;
   - design claim: what people can inspect, steer, revise, reject, appropriate, or understand.
4. Evaluate both claims with matching evidence.

Every paragraph should connect workflow and mechanism, not alternate between disconnected “tool” and “algorithm” stories.

## Style guardrails

- Ha-style technical systems writing: precise, operational, measurable. “Our method enables X under constraint Y using mechanism Z; evidence W supports the claim.”
- Oh-style design-computing writing: material/practice-centered, situated, generative. “Our toolkit enables audience A to explore/make/understand X through practice Y, revealing implication Z.”
- Avoid unsupported words: novel, robust, intuitive, general, efficient, expressive, seamless, significant, SOTA.
