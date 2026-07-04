# Core Research Rules

Use this when a project is being framed, scored, or converted from “interesting demo” into paper-grade research.

## Importance doctrine

Important research changes at least one community habit:

- what the field treats as a problem;
- what it can define, measure, design, fabricate, or compare;
- what artifact, method, dataset, benchmark, taxonomy, protocol, or failure theory others can reuse.

A strong topic usually has this form:

```text
The field wants A, but bottleneck B prevents C.
We change the problem with D, enabling E.
```

If that sentence is weak, do not compensate with prose. Rework the problem.

## Field-object test

Before writing or reviewing, answer:

> After this paper, what can the community define, measure, build, compare, or reuse differently?

Valid field objects include:

- formulation or representation;
- algorithm or solver;
- design space or grammar;
- benchmark, dataset, metric, or evaluation protocol;
- toolkit or fabrication pipeline;
- taxonomy or failure-mode theory;
- reproducible implementation or artifact package.

A demo alone is not enough. The system must produce reusable knowledge.

## Contribution taxonomy

Pick one primary contribution and at most two supporting ones:

| Type | Core question |
|---|---|
| Method | Does it enable a computation, optimization, representation, or control capability that was blocked before? |
| System / artifact | Does it expose a new workflow, design space, or reusable technical substrate? |
| Empirical | Does it reveal a reliable fact about how people, models, robots, or systems behave? |
| Theory / framework | Does it change the vocabulary or assumptions the field uses? |
| Dataset / benchmark | Does it let future work compare or measure something better? |
| Design knowledge | Does it make domain design principles reusable beyond examples? |

## Claim-evidence fit

| Claim | Evidence required |
|---|---|
| More accurate / performant | benchmark, baseline, ablation, statistical or seed-aware comparison |
| More fabricatable / deployable | trials, tolerances, failures, hardware logs, safety/reset details |
| More controllable / expressive | task coverage, user choices, authoring cost, qualitative examples, process analysis |
| More general | multiple domains, boundary cases, stress tests, failure modes |
| New problem definition | taxonomy, counterexamples, design-space map, case analysis |
| System contribution | end-to-end examples, expert/user feedback, reproducibility package, implementation detail |

## Research impact screen

Use this compact screen:

```text
Impact = Problem Centrality × New Insight × Evidence Quality × Reusability × Timing × Framing
```

One zero weakens the paper. Diagnose the zero before polishing language.
