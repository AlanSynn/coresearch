# Academic Writing Style Guide for AI, Robotics, Graphics, and HCI Papers

**Rhetorical analysis of public paper-writing patterns associated with Sehoon Ha and HyunJoo Oh**
**Primary use:** a long-form Markdown guide and prompt library for paper writing, revision, and section-level style control.

---

## 0. Scope and Use

This guide abstracts **public academic writing patterns** from representative papers and project pages across robotics, AI, graphics, HCI, tangible interaction, fabrication, paper electronics, and design computing. It is not a recipe for impersonating an individual author. Use it as a **rhetorical and structural guide**: how to frame problems, state gaps, organize sections, name contributions, connect evidence to claims, and tune the academic voice for different venues.

MotionSmith-like writing is intentionally low priority here. The emphasis is on paper-level rhetoric for:

- AI and robotics systems.
- Physics-based graphics and computational design.
- HCI, tangible interaction, fabrication, and design computing.
- Hybrid Graphics + HCI / AI + HCI papers.

The guide is organized around two reusable rhetorical modes:

1. **Ha-style technical systems writing**: operational bottleneck → targeted technical intervention → measurable evidence.
2. **Oh-style design-computing writing**: material/practice context → underexplored design opportunity → toolkit/system/artifact → situated findings and design implications.

---

# 1. Executive Summary

## 1.1 Ha-style writing in one sentence

> A difficult embodied or computational problem is made concrete through operational constraints; the paper proposes a mechanism that directly attacks those constraints and proves the claim with measurable evidence.

This style is strongest for **AI, robotics, physical simulation, character control, computational robot design, reinforcement learning, co-optimization, and real-world deployment** papers.

The central rhetorical contract is:

> **Our method enables X under constraint Y, and we demonstrate it using evidence Z.**

Typical constraints include:

- sample efficiency
- simulation-to-real transfer
- hardware safety
- manual reset burden
- contact-rich dynamics
- morphology-control coupling
- controller tuning
- physical plausibility
- robustness across terrains, morphologies, or tasks
- authoring or optimization cost

## 1.2 Oh-style writing in one sentence

> A familiar material, practice, learner context, or creative workflow is reframed as an underexplored computational medium; the paper presents a toolkit or artifact that opens a design space and studies what people can make, understand, modify, or appropriate through it.

This style is strongest for **HCI, tangible interaction, physical computing education, paper electronics, fabrication, material-driven design, creative tools, construction kits, and design research** papers.

The central rhetorical contract is:

> **Our toolkit/material system enables people to explore X through practice Y, revealing design implication Z.**

Typical values include:

- accessibility
- adaptability
- expressiveness
- material affordance
- hands-on learning
- embodied understanding
- playful exploration
- craft compatibility
- learner agency
- situated appropriation
- design-space expansion

## 1.3 The most useful hybrid strategy

For a hybrid **Graphics/HCI** or **AI/HCI** paper, do not simply average the two voices. Use them sequentially.

A strong hybrid introduction often works like this:

1. Start with an Oh-style human/material/design context.
2. Narrow into a Ha-style technical bottleneck.
3. Present the system as both a technical method and an interaction medium.
4. Evaluate with both technical evidence and human/design evidence.
5. Discuss both system limitations and design implications.

A compact hybrid claim looks like this:

> We present a system that preserves the openness of hands-on making while providing algorithmic support for physically constrained design. Technical evaluations show that the system satisfies geometric and motion constraints, while a user study shows how designers appropriate the system for exploratory prototyping.

---

# 2. High-Level Rhetorical DNA

## 2.1 Ha-style: problem pressure, mechanism, proof

Ha-style papers tend to create pressure through the **difficulty of the task**. The introduction usually moves from a concrete challenge to a specific operational bottleneck.

A common shape:

```text
Problem is important and physically/computationally hard.
Existing approaches solve part of it, but require assumptions, manual effort, or controlled conditions.
Recent learning/optimization methods are promising, but direct deployment remains difficult.
We propose a method that changes the learning/design/control loop.
The key mechanism enables the target behavior under realistic constraints.
Experiments demonstrate performance through metrics, baselines, ablations, and/or hardware validation.
```

The style is precise and bounded. It usually avoids overly broad language like “intelligence,” “creativity,” or “naturalness” unless those claims are translated into concrete mechanisms or measurements.

### Default claim shape

```text
Our method enables [capability] by [mechanism], while addressing [constraint].
We validate this claim on [tasks/platforms/settings] using [metrics/baselines].
```

### Default paragraph energy

- Tight.
- Technical.
- Mechanism-first.
- Evidence-driven.
- Less reflective; more operational.
- Gap is stated in terms of what prior methods **require**, **assume**, or **do not directly address**.

## 2.2 Oh-style: material opportunity, toolkit, situated implications

Oh-style papers tend to create interest through a **reframing of a familiar material or practice**. The introduction often begins with paper, craft, tangible interaction, physical computing, or a learning context, then argues that its computational potential has not been fully explored.

A common shape:

```text
A familiar material/practice/context is accessible and meaningful.
Prior systems have explored parts of this space, but often separate material practice from computation.
This leaves an underexplored opportunity.
We present a toolkit/material system/workflow that makes computation visible, tangible, or craft-compatible.
Examples and studies show what people can create, how they reason through the system, and what design tensions emerge.
The paper contributes a system, a design space, findings, and implications.
```

The style is reflective, but still concrete. It often uses materials, workflows, artifacts, workshops, and participant practices as evidence.

### Default claim shape

```text
Our toolkit enables [people/audience] to [make/modify/explore] [interactive artifacts] through [material practice], revealing [design finding or implication].
```

### Default paragraph energy

- Material-aware.
- Human-centered.
- Generative rather than adversarial.
- Gap is framed as an **underexplored opportunity** rather than a failure.
- Evidence includes artifacts, observations, themes, breakdowns, and design implications.

---

# 3. Section-by-Section Comparison

| Paper Section | Ha-style technical systems mode | Oh-style HCI/design-computing mode |
|---|---|---|
| Title | Names the technical operation: learning, control, optimization, computational design, real-world deployment. | Names the artifact, material, or toolkit: paper, craft, tangible, construction kit, material system, interaction technique. |
| Abstract | Challenge → bottleneck → method → measurable result. | Material/context → toolkit/system → examples/study → design implications. |
| Introduction | Starts from a hard technical challenge and narrows to an operational bottleneck. | Starts from a familiar material/practice/context and opens a design opportunity. |
| Gap | Prior work requires manual engineering, simulation fidelity, unsafe exploration, high data cost, or fixed assumptions. | Prior work separates making from computation, underuses material affordances, or leaves a design space unexplored. |
| Contributions | Algorithm/framework/system + technical mechanism + experiments. | Toolkit/material process + design space/examples + study findings + implications. |
| Related Work | Taxonomy and technical contrast. | Research lineage and design positioning. |
| Method/System | Problem formulation, components, algorithm, implementation details. | Design goals, material choices, workflow, construction process, examples, implementation. |
| Evaluation | Metrics, baselines, ablations, hardware validation, robustness tests. | Workshops, participant artifacts, qualitative themes, breakdowns, situated findings. |
| Discussion | Scope, failure modes, deployment limits, future technical work. | Design implications, material tensions, accessibility, appropriation, future design space. |
| Tone | Controlled, precise, operational, performance-oriented. | Reflective, material-centered, generative, human-centered. |

---

# 4. Ha-Style Technical Systems Writing

## 4.1 Core rhetorical identity

Ha-style writing is built around the idea that **physical or embodied intelligence becomes difficult at the boundary between algorithm and deployment**. The paper does not merely say that a task is hard. It specifies exactly where the hardness appears:

- in contact dynamics;
- in real-world data collection;
- in policy learning;
- in reset and safety;
- in sim-to-real transfer;
- in morphology-control coupling;
- in controller tuning;
- in high-dimensional design search;
- in physical plausibility and stability.

The paper then introduces a system or method that directly modifies the relevant loop:

- the learning loop;
- the control loop;
- the simulation loop;
- the design-optimization loop;
- the data-collection loop;
- the user-authoring loop.

The writing is strongest when the claimed contribution is **not generic improvement** but a change in the structure of the problem.

Weak:

```text
We improve robot learning with a more robust algorithm.
```

Stronger:

```text
We reduce the operational burden of real-world locomotion learning by combining autonomous reset with safety-aware policy optimization.
```

Weak:

```text
Our method generates better character motion.
```

Stronger:

```text
Our controller generates physically plausible landing motions by decomposing the task into flight, preparation, impact, and recovery phases, each governed by dynamics-aware objectives.
```

## 4.2 Typical contribution logic

A Ha-style contribution usually answers four questions.

### Question 1: What is the task?

Examples:

- learning a locomotion policy directly on hardware;
- transferring a controller from simulation to a physical robot;
- designing a robot morphology from high-level motion specifications;
- co-optimizing mechanical design and motion;
- producing agile physically simulated character motion.

### Question 2: What makes the task difficult?

Examples:

- large design spaces;
- high-dimensional continuous control;
- expensive or unsafe real-world exploration;
- non-smooth contact dynamics;
- simulator mismatch;
- task-specific manual tuning;
- morphology and controller dependence;
- unstable physical behavior.

### Question 3: What mechanism addresses the difficulty?

Examples:

- safety-constrained reinforcement learning;
- automatic reset and data collection;
- modular search over component libraries;
- sensitivity analysis for design optimization;
- decomposition of motion phases;
- iterative human-guided control refinement.

### Question 4: What evidence closes the claim?

Examples:

- real hardware demonstrations;
- training time;
- number of resets or interventions;
- locomotion success rate;
- terrain transfer;
- ablations;
- baseline comparisons;
- fabricated prototypes;
- quantitative motion metrics;
- qualitative comparison to reference footage.

## 4.3 Ha-style abstract pattern

A strong Ha-style abstract is short, compressed, and claim-driven.

```text
[Task] remains challenging because [operational bottleneck].
Existing approaches [what they do], but they often [require/assume/fail to address constraint].
We present [method/system], which [key mechanism].
The method [technical capability] while [constraint handled].
We evaluate [method] on [tasks/platforms/settings].
Results show [main measurable outcome], demonstrating [bounded implication].
```

### Example abstract skeleton for robotics

```text
Learning legged locomotion directly on hardware remains difficult because exploration is slow, unsafe, and often requires repeated human intervention. Existing deep reinforcement learning methods can synthesize controllers in simulation, but their direct use on physical robots is limited by reset cost, hardware safety, and simulator mismatch. We present [System], a real-world learning framework that combines [component A] with [component B] to support autonomous data collection under safety constraints. We evaluate the framework on [robot/platform] across [terrains/tasks]. The results show that [System] learns stable locomotion within [training budget] while reducing [intervention/reset/failure metric], suggesting that real-world robot learning can be made more practical by explicitly modeling the operational constraints of hardware training.
```

### Example abstract skeleton for graphics/control

```text
Generating physically plausible [motion class] remains challenging because the motion depends on contacts, dynamics, and task-level intent. Existing controllers often rely on motion capture, pre-scripted state machines, or extensive parameter tuning. We present [Method], a control framework that [mechanism]. By decomposing [motion/task] into [phases/components], the method produces [capability] while maintaining [physical constraint]. Experiments show that [result], and comparisons with [baseline/reference] demonstrate [bounded claim].
```

### Example abstract skeleton for computational design

```text
Designing robotic devices requires reasoning about both morphology and motion, making manual iteration time-consuming and difficult to scale. Existing tools often optimize controllers for fixed designs or require designers to specify low-level mechanisms. We present [Method], a computational design framework that converts [high-level specification] into [design/control output] through [search/optimization mechanism]. We demonstrate the approach on [devices/tasks] and fabricate [prototypes]. The results show that the framework can generate physically realizable designs that satisfy [motion/performance constraints], supporting faster exploration of robot design alternatives.
```

## 4.4 Ha-style Introduction

The introduction is the most important section for this mode. It should create a **logical funnel** from broad technical challenge to a precise bottleneck.

### Paragraph 1: Establish the technical challenge

Do not begin with a generic statement like “Robots are becoming increasingly important.” Start with a specific technical phenomenon.

Good opening patterns:

```text
Legged locomotion remains a central challenge in robotics because it requires stable control under complex contacts, changing terrain, and limited sensing.
```

```text
Creating physically simulated characters that can perform agile motions is difficult because motion quality depends jointly on dynamics, contact timing, and task-level control.
```

```text
Designing robotic devices is challenging because morphology and control are tightly coupled: a change in geometry can alter the space of feasible motions.
```

The first paragraph should make the reader understand the technical problem before it mentions the proposed method.

### Paragraph 2: Explain why existing methods are insufficient

The gap should be operational, not vague.

Weak:

```text
Existing methods have many limitations and cannot solve this problem well.
```

Strong:

```text
Traditional controllers can produce robust behaviors, but they often require hand-designed state machines, task-specific reward shaping, or extensive domain expertise. Learning-based methods reduce some of this manual design, yet they introduce new bottlenecks in sample efficiency, safety, and transfer to real hardware.
```

The key is to use verbs such as:

- require
- assume
- rely on
- depend on
- constrain
- focus on
- do not directly address
- are difficult to deploy because

### Paragraph 3: Introduce recent progress but identify the remaining bottleneck

Ha-style writing often acknowledges the promise of a recent method before narrowing to the unsolved issue.

```text
Recent advances in deep reinforcement learning provide a path toward automatic controller synthesis. However, applying these methods directly to physical robots remains difficult: unsafe exploration can damage hardware, data collection is slow, and resetting the robot often requires human intervention.
```

This creates a fair, technically credible gap. The prior work is not dismissed; it is bounded.

### Paragraph 4: Present the method as a targeted intervention

The “we propose” sentence should state both the object and the mechanism.

Weak:

```text
We propose a new framework for robot learning.
```

Strong:

```text
We propose a real-world learning framework that couples sample-efficient policy optimization with autonomous reset and safety-aware exploration.
```

Even stronger:

```text
The key idea is to treat reset and safety not as external engineering procedures, but as components of the learning loop itself.
```

A good Ha-style introduction always makes the method feel like the natural response to the bottleneck established earlier.

### Paragraph 5: Preview evidence

The evidence paragraph should be specific.

```text
We evaluate the system on a physical quadruped across flat and uneven terrains, comparing against [baseline] and ablating [component]. The results show that the system learns stable locomotion within [training budget] and reduces manual interventions compared with prior real-world learning setups.
```

Do not write:

```text
Extensive experiments demonstrate the effectiveness of our approach.
```

That sentence is too generic unless it is immediately followed by concrete tasks, metrics, and comparisons.

### Paragraph 6: Contributions

Ha-style contributions should be written as claims, not table-of-contents items.

Weak:

```text
Our contributions are:
1. A method.
2. Experiments.
3. Discussion.
```

Strong:

```text
This paper makes three contributions:
1. A real-world locomotion learning framework that integrates policy optimization, autonomous reset, and safety constraints into a single training loop.
2. An empirical analysis showing that each component reduces a distinct operational bottleneck in hardware learning.
3. Real-world experiments demonstrating stable locomotion across [settings] with reduced human intervention.
```

## 4.5 Ha-style Related Work

Ha-style Related Work should be a **taxonomy of technical approaches**. Each subsection should explain what a class of methods enables and what it assumes.

### Recommended structure for robotics / AI

```text
1. Model-based control and trajectory optimization
2. Learning-based control and deep reinforcement learning
3. Sim-to-real transfer and real-world learning
4. Safety, reset, and autonomous data collection
5. Closest work and positioning
```

### Recommended structure for computational design

```text
1. Manual and modular robot design
2. Evolutionary and search-based design methods
3. Co-optimization of morphology and control
4. Fabrication-aware design tools
5. Closest work and positioning
```

### Recommended structure for graphics / animation

```text
1. Motion-capture-based animation
2. Physics-based character control
3. Optimization and reinforcement learning for motion synthesis
4. Interactive authoring and parameter exploration
5. Closest work and positioning
```

### Useful contrast sentences

```text
While these methods demonstrate robust behavior in controlled settings, they often require task-specific engineering that limits deployment to new robots or environments.
```

```text
In contrast to methods that assume a fixed morphology, our formulation jointly considers design and control.
```

```text
Our work is complementary to sim-to-real transfer methods: rather than improving simulation fidelity, we focus on reducing the cost and risk of learning on hardware.
```

```text
Closest to our work are approaches that learn directly on physical robots. Our method differs in that it explicitly incorporates reset and safety constraints into the training process.
```

### What to avoid

Avoid hostile language:

```text
Prior work fails to solve the problem.
```

Prefer boundary-setting language:

```text
Prior work primarily focuses on [X], whereas our work addresses [Y].
```

```text
These methods assume [condition], which is difficult to guarantee in [target setting].
```

## 4.6 Ha-style Method / System Section

The Method section should convert the introduction’s bottleneck into a technical structure.

### Recommended order

```text
1. Problem formulation
2. System overview
3. Core technical components
4. Learning / optimization / control loop
5. Implementation details
6. Practical considerations
```

### Problem formulation language

```text
Our goal is to learn a policy that maps observations to actions while satisfying [task/safety/physical] constraints.
```

```text
We formulate the design problem as a search over [discrete components] and [continuous parameters], subject to [motion/performance/fabrication] constraints.
```

```text
Given [input specification], the system outputs [controller/design/trajectory] that satisfies [objective].
```

### System overview language

```text
The system consists of three components: [A], [B], and [C]. [A] estimates/constructs [X], [B] optimizes [Y], and [C] enforces/evaluates [Z].
```

```text
The training loop alternates between data collection, policy update, safety evaluation, and reset. This structure allows the robot to continue learning without treating hardware recovery as an external manual step.
```

```text
The design loop alternates between candidate generation, simulation-based evaluation, sensitivity analysis, and designer-guided refinement.
```

### Implementation language

The implementation section should be specific but not overloaded. Include details that affect reproducibility or interpretation:

- hardware platform;
- simulator;
- sensors and observations;
- action representation;
- policy architecture;
- reward terms;
- optimization algorithm;
- training duration;
- reset protocol;
- safety conditions;
- baseline settings;
- fabrication parameters;
- evaluation environment.

### Key principle

Every component should answer: **Which bottleneck does this component remove or reduce?**

Do not list features in isolation.

Weak:

```text
The system has a simulator, a controller, and a user interface.
```

Strong:

```text
The simulator evaluates candidate designs before fabrication, the controller tests whether the resulting morphology can realize the target trajectory, and the user interface exposes sensitivity information so designers can identify which parameters most affect performance.
```

## 4.7 Ha-style Evaluation

The evaluation should begin with explicit questions. This creates a direct bridge between claims and evidence.

### Evaluation question template

```text
We evaluate the method with four questions:
Q1. Can the system achieve [target behavior] in [setting]?
Q2. Does it reduce [operational bottleneck] compared with [baseline/prior setting]?
Q3. How robust is the result across [terrain/task/morphology/initial condition] variation?
Q4. Which components are responsible for the improvement?
```

### Metrics for robotics

- success rate
- distance traveled
- velocity
- stability
- falls
- number of resets
- number of human interventions
- training time
- environment interactions
- terrain categories
- energy or torque usage
- policy transfer performance
- recovery after perturbation

### Metrics for AI systems

- performance on primary task
- sample efficiency
- generalization under distribution shift
- inference cost
- robustness to perturbation
- calibration or uncertainty
- failure rate
- ablation delta
- compute/data budget

### Metrics for graphics/control

- physical plausibility
- contact stability
- trajectory error
- motion diversity
- authoring time
- parameter sensitivity
- failure cases
- comparison to reference motions
- qualitative expert/user ratings if appropriate

### Evidence language

```text
The results show that [method] reaches [performance] after [training budget], whereas [baseline] requires [more data/time/interventions].
```

```text
The ablation study indicates that [component] is responsible for [specific improvement], while [other component] primarily affects [secondary metric].
```

```text
These results support our claim that [bottleneck] can be reduced by [mechanism], rather than by additional manual tuning.
```

### What to avoid

Avoid evaluation prose that is detached from the main claim.

Weak:

```text
We ran several experiments. The results are shown in Figure 5.
```

Strong:

```text
We first test whether the learned controller can maintain stable locomotion on the physical robot without manual reset. Figure 5 shows that the policy reaches stable forward motion after [X] interactions, with [Y] falls and [Z] interventions.
```

## 4.8 Ha-style Discussion and Limitations

The discussion should be concise and technical. It should not introduce a new grand vision unless the results justify it.

### Recommended structure

```text
1. Restate what the evidence supports.
2. Clarify the scope of the claim.
3. Explain failure modes or assumptions.
4. Name future work that follows directly from those limitations.
```

### Good limitation language

```text
The current system assumes [condition], which limits its use in [setting].
```

```text
Although the method reduces [bottleneck], it does not eliminate [remaining cost].
```

```text
The controller was evaluated on [range of conditions]; more dynamic environments may require [extension].
```

```text
The optimization currently treats [factor] as fixed. Extending the formulation to jointly model [factor] is an important direction for future work.
```

### Key principle

A Ha-style limitation is not a confession of weakness. It is a **scope condition**.

---

# 5. Oh-Style HCI and Design-Computing Writing

## 5.1 Core rhetorical identity

Oh-style writing is built around the idea that **materials and making practices can be computational media**. The paper often begins with something familiar—paper, craft, folding, physical kits, classrooms, fabrication workflows—and argues that its computational potential is not fully captured by conventional tools.

The core move is not “prior work performs poorly.” The core move is:

> There is a design space here that becomes visible when we treat material practice as part of computation.

This style is especially strong for papers about:

- tangible interaction;
- paper electronics;
- physical computing education;
- craft-based fabrication;
- construction kits;
- toolkits for children, teachers, or novice makers;
- computational materials;
- interfaces that expose rather than hide mechanism;
- workshops and situated design studies.

## 5.2 Typical contribution logic

An Oh-style contribution usually answers four questions.

### Question 1: What material, practice, or context is being reframed?

Examples:

- paper as a computational material;
- folding/cutting/bending as interaction operations;
- mechanical papercraft as a way to learn motion;
- tangible blocks or paper components as programming interfaces;
- transient materials as functional electronics;
- physical craft kits as learning media.

### Question 2: What design opportunity is underexplored?

Examples:

- computation is separated from material construction;
- programming is hidden behind screens;
- sensors and circuits are treated as external modules rather than craft materials;
- toolkits support assembly but not expressive adaptation;
- learners can build artifacts but do not see why they work;
- physical computing tools lack material flexibility.

### Question 3: What artifact or system opens the design space?

Examples:

- a CAD/CAM toolkit;
- a paper-based electronics workflow;
- a tangible programming system;
- a sensing material exploration;
- a craft kit;
- a set of interaction techniques;
- a design probe.

### Question 4: What evidence shows the design value?

Examples:

- participant artifacts;
- workshop observations;
- teacher feedback;
- design examples;
- qualitative themes;
- breakdowns and repair practices;
- appropriation patterns;
- design implications;
- material explorations.

## 5.3 Oh-style abstract pattern

An Oh-style abstract often gives equal weight to system description and design inquiry.

```text
[Material/practice/context] offers [human/design value], yet its role in [computational activity] remains limited by [gap].
We present [System], a [toolkit/material process/platform] that enables [audience] to [make/explore/modify] [interactive artifacts] through [material operations].
The system combines [technical component] with [material/workflow component].
We demonstrate [System] through [examples/workshop/study].
Our findings show [how people used it / what design space emerged / what tension appeared].
We discuss implications for [broader HCI/design/fabrication area].
```

### Example abstract skeleton for paper-based HCI

```text
Paper is an accessible and expressive material for making, yet its computational role is often limited to a surface for circuits, sketches, or assembly. We present [System], a paper-based toolkit that enables makers to construct interactive artifacts through cutting, folding, layering, and sensing. The toolkit combines [material process] with [software/electronics mechanism] so that computational behavior remains visible and modifiable during construction. Through [examples/workshop/study], we show how participants used the system to explore [interaction/design space]. We discuss design implications for material-centered physical computing toolkits.
```

### Example abstract skeleton for learning/toolkit papers

```text
Physical computing can help learners connect code, circuits, and embodied interaction, but existing tools often separate programming from material construction. We present [Toolkit], a tangible computing system designed to make computational behavior inspectable through hands-on assembly. The toolkit supports [workflow] and allows learners to [activities]. We evaluated the system through [workshop/classroom/pilot study] with [participants]. Findings show that [learning/design outcome], while also revealing tensions around [feedback/debugging/open-endedness]. We conclude with design considerations for future educational computing toolkits.
```

## 5.4 Oh-style Introduction

The introduction should make readers see a familiar material or practice differently.

### Paragraph 1: Begin with material, practice, or context

Good opening patterns:

```text
Paper is one of the most accessible materials for making, yet its computational potential is often reduced to a passive surface for drawing, printing, or attaching circuits.
```

```text
Physical computing education asks learners to coordinate code, circuits, and material construction, but many toolkits still present these activities as separate steps.
```

```text
Craft practices such as cutting, folding, and layering offer rich ways to reason through form and motion, yet they are rarely treated as computational actions in interactive systems.
```

The opening should not be sentimental. It should immediately connect the material or practice to a computational/design opportunity.

### Paragraph 2: Position prior work as foundation, not enemy

Oh-style gap writing is generous. It usually says prior work has opened the area, but something remains underexplored.

```text
Prior work in paper electronics, tangible interaction, and construction kits has shown how low-cost materials can support interactive making. However, many systems still separate the electronic function of an artifact from the material operations through which people shape it.
```

```text
Existing toolkits have lowered barriers to physical computing, but they often constrain learners to predefined modules or hide the mechanisms that connect material change to computational behavior.
```

### Paragraph 3: State the design opportunity or research question

This paragraph can use “we ask,” especially for HCI and design research.

```text
We ask: How can paper-based material transformations become first-class resources for computational interaction?
```

```text
How might a toolkit preserve the flexibility of craft while making computational behavior visible enough for learners to inspect, debug, and modify?
```

```text
What kinds of artifacts and interpretations emerge when learners design motion through familiar material operations rather than abstract mechanical notation?
```

The question should include both the material/workflow and the human outcome.

### Paragraph 4: Present the artifact/toolkit

Oh-style “we present” should define the artifact as a medium for action.

Weak:

```text
We present a new toolkit for paper computing.
```

Strong:

```text
We present [System], a paper-based physical computing toolkit that enables learners to construct interactive artifacts by cutting, folding, assembling, and programming computationally functional paper components.
```

Even stronger:

```text
Rather than treating electronics as components added after construction, the toolkit integrates sensing and computation into the material operations of paper craft.
```

### Paragraph 5: Preview examples and study

```text
We demonstrate the toolkit through a set of design examples that illustrate [range of interactions]. We then report findings from [study/workshop] with [participants], focusing on how participants interpreted the material-computational relationship, how they debugged their artifacts, and how they adapted the toolkit for their own designs.
```

### Paragraph 6: Contributions

Oh-style contributions should include artifact, design space, and findings.

```text
This paper contributes:
1. A material-centered toolkit for [activity], designed around [design goals].
2. A set of interaction techniques and examples that demonstrate how [material operations] can support [computational interaction].
3. Findings from [study/workshop] showing how participants [used/understood/adapted] the system.
4. Design considerations for future [toolkits/material systems/educational computing environments].
```

## 5.5 Oh-style Related Work

Oh-style Related Work is usually a **lineage**, not a battle of baselines. Each subsection should explain how a prior research area contributes to the framing.

### Recommended structure for HCI / tangible interaction

```text
1. Materiality and craft in HCI
2. Tangible and embodied interaction
3. Physical computing and educational toolkits
4. Paper electronics / computational materials / fabrication workflows
5. Positioning of the present work
```

### Recommended structure for fabrication / creative tools

```text
1. Digital fabrication and personal fabrication
2. CAD/CAM tools for craft and making
3. Construction kits and learning-by-making
4. Material-centered design systems
5. Positioning of the present work
```

### Recommended structure for HCI + AI / intelligent tools

```text
1. Human-AI co-creation or mixed-initiative tools
2. Creative authoring systems
3. Tangible/material interaction or situated making
4. Explainability, inspectability, or agency in toolkits
5. Positioning of the present work
```

### Useful positioning language

```text
We draw on prior work in [A], [B], and [C] to frame [material/practice] not only as a substrate, but as an active medium for computational expression.
```

```text
Prior toolkits have lowered the barrier to [activity], yet many still separate [human material action] from [computational process].
```

```text
Our work extends this line by foregrounding [material transformation / learner interpretation / situated appropriation] as a design resource.
```

```text
Rather than optimizing for full automation, our system supports exploratory construction in which users can inspect, modify, and repurpose intermediate artifacts.
```

### What to avoid

Avoid a pure “prior work list.” Each subsection needs a framing role.

Weak:

```text
Many systems have used paper. System A did X. System B did Y. System C did Z.
```

Strong:

```text
Prior paper-based systems show that paper can serve as a low-cost substrate for circuits and interaction. However, when paper is treated primarily as a surface for electronics, its material transformations—folding, cutting, bending, layering, and tearing—remain secondary to the computational design. Our work instead treats these transformations as central interaction resources.
```

## 5.6 Oh-style System / Design Section

The System section should not merely document implementation. It should explain the **design rationale** behind the artifact.

### Recommended order

```text
1. Design goals
2. System overview
3. Material choices
4. Workflow / authoring process
5. Interaction techniques or components
6. Example artifacts
7. Technical implementation
```

### Design goal language

```text
We designed the toolkit around three goals: preserving the flexibility of paper craft, making computational behavior visible, and supporting iterative construction by novice makers.
```

```text
The system is intended to support open-ended exploration rather than fully automate the design process.
```

```text
We prioritize accessibility and adaptability over mechanical precision, because the target use case is early-stage exploratory making.
```

### Material choice language

```text
We chose paper because it is inexpensive, familiar, easy to modify, and compatible with both manual and digital fabrication processes.
```

```text
The material is not a neutral substrate: its ability to bend, crease, layer, and deform shapes both the interaction and the learner’s understanding of the system.
```

### Workflow language

```text
The workflow begins with a familiar material action: users cut, fold, or assemble paper components before adding computational behavior.
```

```text
Users move between digital design, physical construction, and testing. This back-and-forth process is central to the toolkit because it allows users to compare simulated behavior with material behavior.
```

```text
Rather than hiding the mechanism inside a black-box device, the system exposes its structure so that learners can inspect and modify how motion is produced.
```

### Example language

Examples should be framed as evidence for a design space, not as decorative demos.

```text
These examples are not intended to exhaust the application space. Instead, they illustrate how the same material mechanism can support different forms of interaction, expression, and interpretation.
```

```text
The examples demonstrate three recurring design patterns: [pattern A], [pattern B], and [pattern C].
```

## 5.7 Oh-style Study / Evaluation

The evaluation should explain what the study is trying to understand. For HCI/design papers, the question is rarely only “does it work?”

### Study question template

```text
We conducted a [workshop/study/deployment] to understand:
Q1. How do participants interpret the relationship between material action and computational behavior?
Q2. How do participants use the toolkit to create, modify, and debug artifacts?
Q3. What design opportunities and breakdowns emerge during open-ended making?
```

### Study description checklist

Include:

- participants and recruitment context;
- workshop duration;
- tasks or prompts;
- materials provided;
- training or scaffolding;
- data collection method;
- analysis method;
- artifact documentation;
- limitations of the setting.

### Findings language

```text
Participants treated the components not only as functional parts, but also as expressive materials that could be decorated, repaired, and reconfigured.
```

```text
The workshop revealed a tension between open-ended exploration and the need for visible computational feedback.
```

```text
Several participants used physical breakdowns as debugging cues, suggesting that material failure can sometimes become a resource for learning rather than only an error state.
```

```text
Participants’ artifacts show that the toolkit supported both direct replication of examples and creative adaptation beyond the initial tutorial.
```

### Converting findings into implications

A finding is what happened. An implication is what the field should learn from it.

Finding:

```text
Participants repeatedly folded and unfolded the sensor regions to test how the circuit responded.
```

Implication:

```text
Future paper-based computing toolkits should make material state changes inspectable during construction, so that learners can connect physical manipulation to computational response.
```

Finding:

```text
Participants struggled when the output changed but the cause was not visible.
```

Implication:

```text
Open-ended toolkits should provide feedback that preserves creative ambiguity while making causal relationships debuggable.
```

## 5.8 Oh-style Discussion and Limitations

The discussion should not simply repeat findings. It should convert them into design knowledge.

### Recommended structure

```text
1. Reframe the main findings as design principles.
2. Discuss tensions: flexibility vs. precision, openness vs. scaffolding, craft ambiguity vs. computational feedback.
3. Explain situated limitations.
4. Suggest future design directions grounded in the findings.
```

### Good discussion language

```text
Our findings highlight the value of preserving material ambiguity in computational toolkits: the same flexibility that makes paper imprecise can also make it approachable and expressive.
```

```text
Rather than treating noise as a purely technical failure, designers can sometimes use noisy material response as feedback about deformation, contact, or user manipulation.
```

```text
The study was limited to a short workshop setting, so we do not claim long-term learning outcomes. However, participants’ artifacts and debugging strategies suggest design opportunities for future material-centered computing tools.
```

### Key principle

An Oh-style limitation is not merely a threat to validity. It is also a way to clarify the situated context in which the design knowledge was produced.

---

# 6. Field-Specific Adaptation

## 6.1 AI papers

For AI papers, use mostly Ha-style rhetoric. The writing should make the bottleneck measurable.

### Strong AI bottlenecks

- data efficiency;
- distribution shift;
- deployment constraints;
- compute budget;
- supervision cost;
- inference-time control;
- robustness;
- uncertainty;
- safety;
- human-in-the-loop correction;
- interpretability tied to use.

### AI introduction template

```text
Recent advances in [model family] have enabled [capability], but deploying these models in [setting] remains difficult because [operational bottleneck]. Existing approaches typically address [subproblem], yet they assume [condition] or require [resource]. We propose [method], which [mechanism]. The key idea is to [one-sentence technical insight]. Experiments on [benchmarks/settings] show that [method] improves [metric] under [constraint], suggesting that [broader but bounded implication].
```

### AI vocabulary

Use:

- policy
- model
- objective
- supervision
- inference
- distribution shift
- robustness
- calibration
- constraint
- adaptation
- generalization
- sample efficiency
- ablation
- baseline
- deployment setting

Avoid unsupported:

- intelligent
- human-like
- general
- autonomous
- intuitive
- powerful

unless immediately operationalized.

## 6.2 Robotics papers

Robotics is the most natural fit for Ha-style rhetoric.

### What must appear early

- physical robot or embodied system;
- task environment;
- sensing/action constraints;
- contact or dynamics difficulty;
- deployment cost;
- safety or reset issue if relevant;
- how evidence will be measured on hardware or realistic simulation.

### Robotics introduction template

```text
[Task] remains challenging for physical robots because it requires [control capability] under [physical constraints]. Traditional approaches can produce reliable behavior, but often require [manual engineering / modeling assumptions / tuning]. Learning-based methods reduce some of this manual effort, yet their real-world use is limited by [sample efficiency / safety / reset / transfer]. We present [System], which [mechanism]. The system treats [bottleneck] as part of the learning/control loop rather than as an external engineering step. We evaluate [System] on [robot] across [settings], showing [measurable result].
```

### Robotics contribution examples

```text
A real-world learning system that integrates autonomous reset, safety monitoring, and policy optimization for legged locomotion.
```

```text
A morphology-control co-optimization method that identifies design parameters most responsible for task performance.
```

```text
Hardware experiments demonstrating that the proposed method reduces manual intervention while preserving locomotion stability across terrain variation.
```

## 6.3 Graphics papers

Graphics papers can use Ha-style rhetoric when the contribution is technical, but should often include a user/authoring dimension.

### Translate robotics terms into graphics terms

| Robotics term | Graphics equivalent |
|---|---|
| physical robot | physically simulated character or animated artifact |
| terrain | scene, contact condition, environment, task variation |
| safety | stability, plausibility, constraint satisfaction |
| reset | recovery, failure handling, reinitialization |
| policy | controller, motion generator, authoring model |
| deployment | interactive use, production workflow, downstream editing |
| sample efficiency | authoring efficiency, optimization cost, simulation budget |

### Graphics introduction template

```text
Generating [motion/geometry/interaction] remains challenging because the result must satisfy both [physical/geometric constraints] and [authoring/design intent]. Existing methods often trade off realism, controllability, and generality: data-driven approaches can produce high-quality examples but require representative data, while physics-based methods provide structure but often require tuning. We present [Method], which [mechanism]. The method enables [capability] while preserving [constraint]. We evaluate it through [technical comparisons/examples/user study if applicable], showing [main result].
```

### Graphics evaluation should include

- visual quality;
- physical plausibility;
- constraint satisfaction;
- authoring cost;
- diversity/control;
- comparison to baselines or reference footage;
- failure cases;
- user study only if the claim is about usability or creative control.

## 6.4 HCI papers

HCI is the most natural fit for Oh-style rhetoric. The writing must connect artifact, practice, and evidence.

### What must appear early

- who the system is for;
- what practice or context it enters;
- what current tools separate, hide, constrain, or make difficult;
- what design opportunity the system opens;
- how the paper will study or demonstrate that opportunity.

### HCI introduction template

```text
[Practice/material/context] plays an important role in [activity], yet its relationship to computation remains limited by [gap]. Prior systems have supported [related capability], but they often separate [human action] from [computational process]. We present [System], a [toolkit/platform/material process] that enables [audience] to [activity] through [interaction/material workflow]. Through [examples/study/workshop], we examine how people [use/understand/adapt] the system. Our findings show [main situated result] and suggest design implications for [broader area].
```

### HCI contribution examples

```text
A material-centered toolkit that integrates sensing with paper craft operations such as cutting, folding, and layering.
```

```text
A workflow that allows novice makers to move between digital design, physical assembly, and interactive testing.
```

```text
A workshop study showing how learners use visible material mechanisms to debug, reinterpret, and adapt computational artifacts.
```

## 6.5 Graphics + HCI hybrid papers

For creative tools, fabrication systems, and authoring interfaces, combine Oh-style setup with Ha-style technical grounding.

### Hybrid introduction template

```text
[Creative practice] relies on iterative movement between intention, material, and form. However, adding [technical capability] often forces designers to leave this open-ended workflow and use tools that require [technical expertise / rigid specification / separated pipeline]. We present [System], an authoring environment that preserves [human/material practice] while providing [technical mechanism]. The key technical idea is [mechanism], which enables [capability] under [constraint]. We evaluate the system through [technical evaluation] and [user/design study], showing that it both [technical result] and [human-facing result].
```

### Hybrid claim contract

```text
Technical claim: The system can compute/generate/optimize [output] under [constraints].
Design claim: The system changes what users can make, inspect, modify, or understand.
```

A hybrid paper fails when it proves only one of these claims while promising both.

## 6.6 AI + HCI hybrid papers

Use Ha-style precision for the model contribution and Oh-style care for the human context.

### AI + HCI introduction template

```text
[Human practice] increasingly involves [AI capability], but current systems often provide outputs without supporting [inspection/control/appropriation/learning]. Existing AI methods improve [metric], yet they do not directly address how users [understand/steer/repair] the model in [context]. We present [System], which combines [model mechanism] with [interaction mechanism]. The system enables users to [human action] while maintaining [technical constraint]. We evaluate [model performance] and [human interaction outcome], showing [bounded claim].
```

### Common AI + HCI mistake

Do not write an HCI paper that treats the user study as a decoration around a model paper. Do not write a model paper that hides the human interaction claim. State both claim types explicitly.

---

# 7. Rhetorical Move Library

## 7.1 Opening moves

### Ha-style opening moves

```text
[Task] remains challenging because [specific physical/computational difficulty].
```

```text
Despite progress in [area], deploying [capability] in [setting] remains difficult due to [operational bottleneck].
```

```text
Designing [system] requires reasoning jointly about [coupled factors], making manual iteration slow and error-prone.
```

```text
Generating [behavior] requires satisfying [constraints] while maintaining [desired property].
```

### Oh-style opening moves

```text
[Material] is familiar and accessible, yet its computational role is often limited to [narrow use].
```

```text
[Practice] offers rich opportunities for [learning/expression/design], but current tools often separate it from [computation/programming/electronics].
```

```text
For [audience], [activity] requires coordinating [material action] with [computational concept], a relationship that is often hidden in existing toolkits.
```

```text
We revisit [material/practice] as a computational medium rather than a passive substrate.
```

## 7.2 Gap moves

### Ha-style gap language

Use when prior work is technically strong but incomplete for your target setting.

```text
These methods often require [assumption], which is difficult to satisfy in [setting].
```

```text
However, direct deployment remains limited by [bottleneck].
```

```text
While [class of methods] can [strength], they do not directly address [constraint].
```

```text
The remaining challenge is not only to [capability], but to do so under [realistic condition].
```

### Oh-style gap language

Use when prior work inspires your system but leaves a design opportunity.

```text
Prior work has shown the value of [area], but less is known about how [material/practice] can support [new interaction or learning outcome].
```

```text
Many systems treat [material] as [passive role], leaving its [affordance] underexplored.
```

```text
Existing toolkits lower the barrier to [activity], yet they often separate [practice] from [computation].
```

```text
This opens an opportunity to design tools that preserve [material/human value] while supporting [computational capability].
```

## 7.3 Key insight moves

### Ha-style key insight

```text
Our key insight is that [bottleneck] can be treated as part of [learning/control/design loop], rather than as an external procedure.
```

```text
The central idea is to decompose [hard task] into [subproblems] that can be optimized under [constraints].
```

```text
Instead of optimizing [component] after fixing [other component], we jointly reason about [coupled variables].
```

### Oh-style key insight

```text
Our key insight is that [material operation] can serve as both a construction action and a computational interaction.
```

```text
Rather than hiding [mechanism], we expose it as a resource for inspection, debugging, and creative adaptation.
```

```text
We treat [material property] not as a limitation to eliminate, but as a design feature that shapes how users understand and appropriate the system.
```

## 7.4 Contribution moves

### Ha-style contribution verbs

- formulate
- introduce
- propose
- demonstrate
- validate
- evaluate
- quantify
- analyze
- optimize
- learn
- control
- synthesize
- transfer

### Oh-style contribution verbs

- present
- design
- explore
- foreground
- characterize
- investigate
- support
- enable
- scaffold
- reveal
- discuss
- derive
- articulate

### Ha-style contribution templates

```text
We formulate [problem] as [technical formulation], enabling [capability] under [constraint].
```

```text
We introduce [method/system], which [mechanism] to reduce [bottleneck].
```

```text
We demonstrate [result] on [platform/task], showing [metric] compared with [baseline].
```

```text
We analyze [component/factor] through [ablation/sensitivity study], showing its effect on [metric].
```

### Oh-style contribution templates

```text
We present [toolkit/system], designed to support [audience] in [practice] through [material/workflow].
```

```text
We characterize a design space of [interactions/artifacts] enabled by [material mechanism].
```

```text
We report findings from [study/workshop] showing how participants [use/interpret/adapt] the system.
```

```text
We derive design considerations for future [toolkits/material systems/learning environments].
```

## 7.5 Evaluation moves

### Ha-style evaluation moves

```text
We first evaluate whether [method] can achieve [capability] in [target setting].
```

```text
We compare against [baseline] to isolate the effect of [mechanism].
```

```text
We conduct an ablation study to determine whether [component] is necessary for [result].
```

```text
We test robustness by varying [terrain/task/initial condition/object/morphology].
```

```text
These results support our claim that [mechanism] reduces [bottleneck].
```

### Oh-style evaluation moves

```text
We conducted a workshop to understand how participants used the toolkit during open-ended making.
```

```text
Our analysis focuses on participants’ artifacts, debugging strategies, and interpretations of the material-computational relationship.
```

```text
The study revealed three themes: [theme A], [theme B], and [theme C].
```

```text
These findings suggest that future toolkits should [design implication].
```

```text
We do not claim long-term learning outcomes; instead, we use the study to identify situated opportunities and tensions.
```

## 7.6 Limitation moves

### Ha-style limitation templates

```text
The current system assumes [condition], which may not hold in [setting].
```

```text
Although [method] reduces [bottleneck], it still requires [remaining resource].
```

```text
The evaluation covers [scope], but does not yet address [broader case].
```

```text
Future work should extend the framework to [specific technical direction] by [specific mechanism].
```

### Oh-style limitation templates

```text
The study was conducted in [setting], so the findings should be interpreted as situated design insights rather than general learning outcomes.
```

```text
The toolkit currently supports [scope], leaving [material/workflow/context] for future exploration.
```

```text
Participants’ difficulties with [issue] suggest a design tension between [value A] and [value B].
```

```text
Future systems should explore how to preserve [openness/material flexibility] while providing stronger support for [debugging/feedback/scaffolding].
```

---

# 8. Vocabulary and Tone Control

## 8.1 Ha-style vocabulary

### Nouns

- policy
- controller
- dynamics
- contact
- trajectory
- morphology
- design parameter
- objective
- reward
- constraint
- optimization
- simulation
- transfer
- hardware
- deployment
- reset
- safety
- terrain
- stability
- robustness
- sample efficiency
- ablation
- baseline
- prototype
- performance
- generalization

### Verbs

- formulate
- optimize
- learn
- control
- synthesize
- transfer
- constrain
- evaluate
- validate
- demonstrate
- compare
- ablate
- reduce
- estimate
- search
- execute
- deploy

### Adjectives

- stable
- robust
- sample-efficient
- physically plausible
- real-world
- hardware-aware
- contact-rich
- modular
- high-dimensional
- deployment-oriented
- computational
- automatic
- adaptive

### Connective rhetoric

- However,
- In contrast,
- While prior work...
- Unlike methods that...
- Our key insight is...
- This allows...
- We evaluate whether...
- These results suggest...

## 8.2 Oh-style vocabulary

### Nouns

- material
- materiality
- affordance
- craft
- paper
- folding
- cutting
- bending
- layering
- assembly
- toolkit
- workflow
- tangible interaction
- physical computing
- construction kit
- making
- learners
- teachers
- workshop
- prototype
- artifact
- design space
- design probe
- appropriation
- scaffolding
- feedback
- expressiveness
- accessibility
- adaptability
- situated practice
- design implication
- design consideration

### Verbs

- present
- design
- explore
- foreground
- support
- enable
- scaffold
- reveal
- investigate
- characterize
- appropriate
- adapt
- modify
- assemble
- construct
- inspect
- debug
- reflect
- discuss
- derive

### Adjectives

- tangible
- material-centered
- accessible
- adaptable
- expressive
- playful
- hands-on
- open-ended
- situated
- craft-compatible
- low-cost
- visible
- inspectable
- modular
- exploratory
- embodied

### Connective rhetoric

- We draw on...
- We foreground...
- Rather than treating X as Y...
- This opens a design space...
- Our findings suggest...
- The workshop revealed...
- These examples illustrate...
- We discuss implications for...

## 8.3 Words to use carefully

The following words are common in papers but often become empty unless supported.

| Word | When it is acceptable | Better replacement if unsupported |
|---|---|---|
| novel | When the novelty is explicitly defined. | “We introduce...” followed by mechanism. |
| robust | When tested across perturbations or conditions. | “stable across [conditions].” |
| intuitive | When user evidence supports it. | “participants were able to...” |
| seamless | Rarely useful. | “without switching tools,” “within the same workflow.” |
| flexible | When degrees of freedom or use cases are shown. | “supports [specific variations].” |
| efficient | When time/data/compute is measured. | “requires [X] fewer steps/interactions.” |
| general | When evaluated across task families. | “applies to [specific range].” |
| expressive | When examples or participant artifacts show range. | “supports [forms of variation].” |

---

# 9. Section-Level Prompt Pack

Use these prompts directly when drafting or revising a paper.

## 9.1 Full-paper style prompt

```text
You are an expert academic writing assistant for AI, Robotics, Graphics, and HCI papers.

Write or revise my paper using two rhetorical modes:

Ha-style technical systems mode:
- Start from a concrete technical challenge.
- Narrow the problem into operational bottlenecks such as sample efficiency, safety, transfer, robustness, manual engineering, physical constraints, optimization difficulty, or deployment cost.
- Present the method as a targeted intervention, not a generic improvement.
- Use precise technical nouns: policy, controller, dynamics, contact, constraint, optimization, simulation, deployment, robustness, generalization, reset, data collection, morphology, trajectory, reward, benchmark, ablation.
- Make every claim measurable or operational.
- Use contrastive rhetoric only when it creates a real turn: “however,” “in contrast,” “while prior work,” “unlike,” “our key insight.”
- In evaluation, state explicit research questions, compare to baselines, report task conditions, and connect metrics back to the central claim.

Oh-style HCI/design-computing mode:
- Start from a familiar material, practice, learner context, or creative workflow.
- Treat materials and tools as active design media, not passive substrates.
- Frame the gap as an underexplored design opportunity, not only a failure of prior work.
- Use concrete material and practice-oriented nouns: paper, craft, folding, cutting, bending, layering, toolkit, tangible interaction, physical computing, affordance, accessibility, adaptability, expressiveness, workshop, learners, teachers, co-design, design space, design implications.
- Present the system as a toolkit, platform, material process, or design probe that enables people to make, understand, modify, and appropriate computational artifacts.
- In evaluation, discuss not only performance but also how participants used the system, what artifacts they created, what breakdowns occurred, and what design implications emerged.
- Use reflective but precise language: “we draw on,” “we foreground,” “this opens a design space,” “our findings suggest,” “rather than treating X as Y, we treat it as Z.”
- Avoid universal claims from small workshops. State situated findings and design implications.

Choose the correct mode by section:
- Introduction: use Ha-style for AI/Robotics-heavy papers; use Oh-style for HCI/Design/Fabrication-heavy papers; use a hybrid when both technical and human-facing claims are central.
- Related Work: use technical taxonomy for AI/Robotics; use research lineage and design positioning for HCI/Design.
- Method/System: define inputs, outputs, assumptions, components, and mechanism for technical papers; define design goals, workflow, material operations, user actions, and implementation for design papers.
- Evaluation/Study: use benchmarks, baselines, ablations, and metrics for technical claims; use workshops, artifacts, themes, and implications for HCI/design claims.
- Discussion: discuss scope, failure modes, and future technical directions for technical papers; discuss design implications, material tensions, and situated limitations for HCI/design papers.

Inputs:
- Paper field:
- Target venue:
- Paper title:
- One-sentence contribution:
- Technical method:
- Human/user/material context:
- Main evidence:
- Baselines or related systems:
- Key results:
- Intended rhetorical mode: Ha-style / Oh-style / hybrid:

Output:
Produce polished academic prose. Prioritize clarity, structure, correctness, and claim-evidence alignment. Avoid marketing language. Do not overclaim.
```

## 9.2 Introduction-only prompt

```text
Write the Introduction of my paper in a precise academic style suitable for AI, Robotics, Graphics, or HCI.

Use this rhetorical plan:

Paragraph 1: Establish the central phenomenon or challenge.
- For AI/Robotics: begin with the hard technical problem and why it matters in deployed or embodied systems.
- For Graphics: begin with the difficulty of satisfying visual, physical, geometric, or authoring constraints.
- For HCI/Design: begin with the human practice, creative workflow, material, learner context, or interaction setting.
- Avoid broad motivational clichés. Make the first paragraph concrete.

Paragraph 2: Define the limitation of existing approaches.
- Do not say “existing methods have limitations.”
- Specify what they require, assume, separate, hide, constrain, or fail to support.
- AI/Robotics language: sample efficiency, safety, transfer, reset, manual engineering, robustness, deployment, physical constraints.
- Graphics language: physical plausibility, controllability, authoring cost, data dependence, parameter tuning, simulation budget.
- HCI/Design language: accessibility, adaptability, expressiveness, material affordance, learning, appropriation, workflow separation, toolkit complexity.

Paragraph 3: Introduce the opportunity.
- Explain why recent work makes the problem newly tractable or worth revisiting.
- For technical papers, state the key bottleneck that remains.
- For design papers, state the underexplored design space.

Paragraph 4: Present the system or method.
- Use “We present” or “We propose.”
- First sentence: define what the system/method is.
- Second sentence: explain the key mechanism.
- Third sentence: explain what this enables that was previously difficult.

Paragraph 5: State evaluation and results.
- For technical papers, include baselines, metrics, tasks, and deployment settings.
- For HCI/design papers, include study/workshop/examples, participants if available, and the nature of findings.
- For hybrid papers, include both technical and human-facing evidence.

Final paragraph: Contributions.
Write 3–4 contributions as strong, specific claims:
1. The artifact/method/framework.
2. The key technical or material mechanism.
3. The empirical result or study finding.
4. The broader implication for the field.

Style constraints:
- Use precise, grounded, confident academic language.
- Do not overclaim.
- Do not use marketing language.
- Do not use vague words like “novel,” “seamless,” “intuitive,” or “powerful” unless the sentence immediately explains what that means.
- Every paragraph should create a rhetorical dependency: the next paragraph should feel necessary.
```

## 9.3 Related Work prompt

```text
Write the Related Work section.

First, identify whether the paper is primarily:
- AI/Robotics/technical systems,
- Graphics/computational design,
- HCI/design computing,
- or hybrid.

For AI/Robotics:
- Organize prior work into technical categories.
- For each category, explain what it enables, what it assumes, and what bottleneck remains.
- Use contrastive but fair language: “focuses on,” “assumes,” “requires,” “does not directly address,” “is complementary to.”
- End with a closest-work paragraph that precisely states how this paper differs.

For HCI/Design:
- Organize prior work as research lineages.
- Explain how each lineage informs the design framing.
- Frame the gap as an underexplored design opportunity.
- Use generative language: “draws on,” “extends,” “foregrounds,” “opens a design space.”
- End with a positioning paragraph that states what the present work foregrounds differently.

For Graphics/HCI hybrid:
- Include both technical prior work and design/toolkit prior work.
- Do not let one side dominate if the paper claims both technical and human-facing contributions.
- End by stating the exact intersection the paper occupies.
```

## 9.4 Method/System prompt

```text
Write the Method/System section.

For a technical paper:
1. Start with the problem formulation.
2. Define inputs, outputs, assumptions, objectives, and constraints.
3. Give a system overview with components.
4. Explain the core mechanism.
5. Provide implementation details needed for reproducibility.
6. For each component, explain which bottleneck it addresses.

For an HCI/design paper:
1. Start with design goals.
2. Explain the material/system overview.
3. Describe the user workflow.
4. Explain material choices and design rationale.
5. Describe interaction techniques or components.
6. Use examples to show the design space.
7. Provide implementation details, but keep them connected to user action and design goals.

For a hybrid paper:
- Start with design goals and problem formulation.
- Explain the technical mechanism in relation to the user workflow.
- Make clear which parts are algorithmic contributions and which parts are interaction/design contributions.
```

## 9.5 Evaluation/Study prompt

```text
Write the Evaluation or Study section.

Begin with explicit questions.

For technical evaluation:
- Q1 should test whether the method achieves the target capability.
- Q2 should compare against baselines.
- Q3 should test robustness or generalization.
- Q4 should isolate components through ablation or sensitivity analysis.
- Include metrics, tasks, platforms, settings, and implementation details.
- Connect every result back to the paper’s central bottleneck.

For HCI/design study:
- Q1 should ask how participants use or understand the system.
- Q2 should ask how participants create, modify, debug, or appropriate artifacts.
- Q3 should ask what design opportunities, tensions, or breakdowns emerge.
- Include participants, tasks, procedure, data collection, analysis, artifacts, and limitations.
- Convert findings into design implications.

For hybrid evaluation:
- Separate technical evaluation and user/design study unless they are tightly integrated.
- Make clear which claim each evaluation supports.
- Do not use user enthusiasm as evidence for technical performance.
- Do not use technical performance as evidence for usability.
```

## 9.6 Discussion prompt

```text
Write the Discussion section.

For technical papers:
- Start by restating what the evidence supports.
- Clarify scope conditions.
- Discuss failure modes and assumptions.
- Propose future work that follows directly from limitations.
- Keep the claims bounded and operational.

For HCI/design papers:
- Convert findings into design implications.
- Discuss tensions such as openness vs. scaffolding, flexibility vs. precision, material ambiguity vs. computational feedback.
- State situated limitations without overclaiming.
- Propose future design directions grounded in the study.

For hybrid papers:
- Discuss how the technical mechanism and human-facing workflow shaped each other.
- Identify which limitations are algorithmic, which are material, and which are study-related.
- End with a field-level implication that is supported by both kinds of evidence.
```

---

# 10. Practical Revision Checklist

## 10.1 Introduction checklist

Before submitting, check whether the introduction answers:

1. What is the concrete problem?
2. Why is it hard?
3. What do existing approaches require, assume, or leave underexplored?
4. What is the specific bottleneck or design opportunity?
5. What is the proposed method/system/toolkit?
6. What is the key mechanism?
7. What does it enable?
8. What evidence supports the claim?
9. What are the exact contributions?
10. Does each paragraph make the next paragraph necessary?

## 10.2 Related Work checklist

1. Are prior works grouped into meaningful categories?
2. Does each category have a role in the argument?
3. Is the contrast fair and specific?
4. Is the closest work clearly identified?
5. Does the final paragraph position this paper precisely?

## 10.3 Method/System checklist

1. Are inputs, outputs, assumptions, and constraints clear?
2. Is the system overview understandable before details?
3. Does each component have a purpose?
4. Are implementation details sufficient for interpretation?
5. For HCI/design papers, are user actions and material operations described clearly?
6. For technical papers, is the algorithmic mechanism clear?
7. For hybrid papers, is the connection between workflow and mechanism explicit?

## 10.4 Evaluation checklist

1. Are evaluation questions stated before results?
2. Does each experiment/study part answer a question?
3. Are metrics or qualitative themes connected to claims?
4. Are baselines and ablations justified?
5. Are study participants and procedures clear?
6. Are limitations acknowledged in the right place?
7. Are results interpreted without overclaiming?

## 10.5 Discussion checklist

1. Does the discussion synthesize rather than repeat?
2. Are limitations stated as scope conditions?
3. Are design implications grounded in findings?
4. Are future directions specific?
5. Does the conclusion return to the paper’s main contribution without inflating it?

---

# 11. Common Failure Modes and Fixes

## 11.1 Failure mode: vague novelty

Weak:

```text
We propose a novel and flexible system for robot learning.
```

Fix:

```text
We propose a real-world robot learning system that reduces manual reset by integrating recovery behavior into the training loop.
```

## 11.2 Failure mode: unsupported HCI claim

Weak:

```text
The toolkit is intuitive and easy to use.
```

Fix:

```text
Participants were able to complete the first interactive artifact after the tutorial, but debugging sensor behavior required additional scaffolding.
```

## 11.3 Failure mode: disconnected related work

Weak:

```text
Previous systems include A, B, C, and D.
```

Fix:

```text
Previous systems show three strategies for supporting paper-based interaction: embedding circuits into paper, augmenting paper with sensing, and using paper as a construction material. Our work builds on these strategies but foregrounds material transformation as the computational interface.
```

## 11.4 Failure mode: evaluation without claim alignment

Weak:

```text
We tested our system in several scenarios.
```

Fix:

```text
We designed the evaluation to test whether the system reduces the two bottlenecks identified in the introduction: manual parameter tuning and failure recovery.
```

## 11.5 Failure mode: hybrid paper with two unrelated halves

Weak:

```text
We present an algorithm. We also conducted a user study.
```

Fix:

```text
The algorithm supports the user-facing workflow by computing physically feasible suggestions during iterative design. We therefore evaluate both constraint satisfaction and how designers use these suggestions during prototyping.
```

---

# 12. Final Writing Rules

1. **Write claims as contracts.** A claim is not complete until the paper shows what evidence will support it.
2. **Use concrete nouns.** “Controller,” “reset,” “fold,” “sensor,” and “artifact” are stronger than “capability,” “experience,” or “functionality.”
3. **Do not overuse “novel.”** Novelty should emerge from the mechanism and positioning.
4. **Make gaps operational.** Say what prior work requires, assumes, separates, or does not directly address.
5. **Make design opportunities generative.** In HCI, the gap often opens a space rather than defeats prior work.
6. **Match evaluation to claim type.** Technical claims need metrics; design claims need situated evidence.
7. **Preserve section roles.** Introduction motivates; Related Work positions; Method explains; Evaluation proves; Discussion interprets.
8. **Use limitations to define scope.** Do not hide them, but do not let them erase the contribution.
9. **For hybrid papers, state both claim types.** Technical validity and human/design value require different evidence.
10. **Stop when the paper’s central claim is clear.** Additional detail should serve the argument, not bury it.

---

# 13. Compact Style Cards

## 13.1 Ha-style card

```text
Voice: precise, technical, operational.
Opening: concrete embodied/computational challenge.
Gap: prior work requires assumptions, manual effort, safe conditions, simulation fidelity, or high data cost.
Method: targeted intervention in the learning/control/design loop.
Evidence: metrics, baselines, ablations, hardware/simulation validation.
Best for: AI, robotics, physics-based graphics, computational design.
Claim form: “We enable X under Y constraint using Z mechanism.”
Avoid: vague intelligence, broad novelty, unsupported robustness.
```

## 13.2 Oh-style card

```text
Voice: material-aware, human-centered, reflective, concrete.
Opening: familiar material, practice, learner context, or creative workflow.
Gap: underexplored design space; computation separated from material practice.
System: toolkit, platform, material process, design probe.
Evidence: examples, workshops, artifacts, themes, breakdowns, design implications.
Best for: HCI, tangible interaction, fabrication, physical computing education, design computing.
Claim form: “We enable people to explore X through material practice Y, revealing design implication Z.”
Avoid: universal claims from small studies, vague ease-of-use claims, decorative examples.
```

## 13.3 Hybrid card

```text
Voice: human/material context plus technical precision.
Opening: design practice or user context.
Narrowing: technical bottleneck that blocks the practice.
System: authoring environment, toolkit, or model that connects workflow and mechanism.
Evidence: technical evaluation plus user/design study.
Best for: Graphics/HCI, AI/HCI, fabrication tools, creative AI systems.
Claim form: “We preserve human/material practice while providing technical capability under constraint.”
Avoid: proving only the technical claim while promising a design contribution, or proving only user interest while promising technical novelty.
```

---

# 14. Representative Source Base

This guide abstracts rhetorical patterns from representative public materials, including:

## Sehoon Ha-oriented source base

- Public research profile describing work across character animation, robotics, and AI.
- Real-world robot learning papers on legged locomotion, safety-aware learning, autonomous reset, and minimal human intervention.
- Deep reinforcement learning papers for learning walking policies on physical robots.
- Computational robot design papers involving modular components, high-level motion specifications, morphology-control coupling, and co-optimization.
- Graphics and animation papers on physics-based controllers, falling/landing motion, parameter exploration, and interactive control refinement.

## HyunJoo Oh-oriented source base

- Public publication/project pages in HCI, design computing, tangible interaction, and paper-based making.
- FoldMecha and related paper-mechatronics work on mechanical papercraft, construction kits, workshops, and learning by making.
- PEP and paper-based electronic papercraft work connecting digital fabrication with paper electronics.
- Sensing Kirigami and related material-driven explorations of carbon-coated paper, folding, bending, and tangible interaction.
- Physical computing education and toolkit papers involving children, teachers, tangible programming, visible computing, and situated design studies.

---

# 15. One Strong Default Prompt

Use this when you want one general-purpose prompt for future paper writing.

```text
Revise the following paper section using a hybrid academic style suitable for AI, Robotics, Graphics, and HCI.

Use Ha-style precision when discussing technical contributions:
- define the concrete challenge;
- state the operational bottleneck;
- present the method as a targeted mechanism;
- make claims measurable;
- connect evaluation to baselines, metrics, ablations, and deployment constraints.

Use Oh-style design-computing rhetoric when discussing human, material, or interaction contributions:
- begin from the material/practice/context;
- frame the gap as an underexplored design opportunity;
- describe the system as a toolkit, workflow, artifact, or design probe;
- connect examples and studies to design implications;
- avoid overclaiming beyond the study setting.

For every paragraph:
1. Identify its rhetorical role.
2. Remove vague novelty language.
3. Replace abstract adjectives with concrete mechanisms or evidence.
4. Make the transition to the next paragraph necessary.
5. Ensure the section’s claims match the paper’s evidence.

Return a polished version first. Then provide a short note listing the major structural edits.

Section type:
Paper field:
Target venue:
Main contribution:
Evidence available:
Draft text:
```

---

# 16. Source-to-Style Mapping Appendix

This appendix maps representative papers and project families to the rhetorical patterns extracted above. It is intended to make the style guide easier to audit and reuse.

## 16.1 Ha-oriented papers and observed rhetorical patterns

### Real-world locomotion learning with minimal human effort

**Observed rhetorical structure:**

```text
Stable locomotion is a hard robotics problem.
Hand-engineered controllers require expertise.
Deep reinforcement learning is promising but simulation-trained policies remain limited by transfer.
Real-world learning is desirable but difficult because automation, reset, and safety become operational bottlenecks.
The paper proposes a system-level learning framework that explicitly addresses these bottlenecks.
Evaluation questions test learning success, human intervention, terrain variation, and component contribution.
```

**Reusable writing lesson:**

This is the clearest Ha-style pattern for robotics writing. The introduction does not frame the problem as “we need better RL.” It frames the problem as **making RL practical under the physical constraints of hardware training**.

**Best reusable phrases:**

```text
remains challenging because...
requires substantial manual engineering...
real-world deployment remains difficult...
unsafe exploration can damage hardware...
resetting the robot requires human intervention...
we address these challenges by...
we evaluate with the following questions...
```

### Learning to Walk via Deep Reinforcement Learning

**Observed rhetorical structure:**

```text
Learning locomotion policies directly on real robots is difficult.
The paper positions deep RL as a way to reduce manual controller design.
The contribution is stated as an end-to-end framework rather than a single isolated algorithm.
The method is justified through data efficiency, asynchronous learning, and direct hardware results.
Related Work is organized around technical categories: control, reinforcement learning, sim-to-real, and real-world policy learning.
```

**Reusable writing lesson:**

When the method is algorithmic, the paper still keeps the writing grounded in the physical robot. This prevents the introduction from becoming a generic RL paper.

**Best reusable sentence pattern:**

```text
Rather than relying on hand-designed controllers or a carefully tuned simulator, our framework learns [behavior] directly from [interaction source] using [algorithmic mechanism].
```

### Automated DRL environment for modular legged robot hardware

**Observed rhetorical structure:**

```text
Manual design and tuning become especially difficult for modular robots because morphology changes the control problem.
Simulation is insufficient when real hardware has unmodeled deformation, joint slackness, contacts, and stochastic dynamics.
The system contribution is not only the learning algorithm but also the automated hardware environment.
The writing treats infrastructure as a research contribution because it changes what kinds of experiments become possible.
```

**Reusable writing lesson:**

A tool or infrastructure paper can still be written in a strong technical voice if the paper clearly states the operational bottleneck it removes.

**Best reusable sentence pattern:**

```text
The main obstacle is not only policy optimization, but the cost of repeatedly collecting reliable data on physical hardware.
```

### Computational design from high-level motion specifications

**Observed rhetorical structure:**

```text
Robot design is important but manual design requires expertise.
Modular components make design more accessible, but the design space becomes combinatorial.
The paper frames the problem as converting high-level motion intent into physical design.
Related Work is organized around manual design, task-based design, evolutionary search, and physical character design.
The method is justified by the coupling between structure, parameters, and motion behavior.
```

**Reusable writing lesson:**

For computational design papers, the introduction should highlight **coupling**: morphology, controller, material, fabrication, and desired behavior cannot be optimized independently.

**Best reusable sentence pattern:**

```text
Designing [artifact] requires reasoning about both [form] and [function], because changes in [design parameter] alter the feasible space of [behavior].
```

### Computational co-optimization of design parameters and motion trajectories

**Observed rhetorical structure:**

```text
The paper frames robotic design as a form-function coupling problem.
Manual iteration is time-consuming because designers must repeatedly revise hardware and test behavior.
The method supports design exploration by identifying which parameters affect performance.
The writing emphasizes iterative design rather than one-shot automatic optimization.
Hardware validation closes the loop between computation and physical realization.
```

**Reusable writing lesson:**

A strong computational design paper should not overclaim full automation. It can be more persuasive to say the system **supports designer decision-making** by exposing sensitivities, tradeoffs, and feasible directions.

**Best reusable sentence pattern:**

```text
Rather than replacing the designer with a fully automatic optimizer, the framework exposes how design parameters influence motion performance, enabling more informed iteration.
```

### Physics-based falling and landing motion control

**Observed rhetorical structure:**

```text
Agile motion is difficult because it requires contact timing, dynamic balance, and physically plausible recovery.
Prior approaches often depend on motion capture, scripted controllers, or task-specific state machines.
The paper decomposes a complex motion into phases that can be controlled and evaluated.
Evaluation uses both physical performance and comparison to plausible reference behavior.
Limitations are stated as task and scope constraints.
```

**Reusable writing lesson:**

For graphics/control papers, write the problem as a **physical control problem with visual consequences**, not as a purely visual generation problem.

**Best reusable sentence pattern:**

```text
The challenge is to produce motion that is both physically plausible and controllable under varying initial conditions.
```

### Physics Storyboards and iterative training papers

**Observed rhetorical structure:**

```text
Simulation and procedural systems often require repeated parameter tuning.
The paper reframes the problem as an authoring and exploration bottleneck.
The system summarizes parameter effects or uses iterative feedback to support control refinement.
The technical method is connected to designer workflow rather than presented as standalone automation.
```

**Reusable writing lesson:**

For Graphics/HCI-adjacent systems, a Ha-style technical mechanism can be introduced through a user-facing workflow bottleneck: repeated simulation, parameter tuning, or failed trial interpretation.

**Best reusable sentence pattern:**

```text
The difficulty is not only generating a valid simulation, but helping designers understand how parameter changes affect the resulting behavior.
```

## 16.2 Oh-oriented papers and observed rhetorical patterns

### FoldMecha

**Observed rhetorical structure:**

```text
The paper begins with tangible interaction and physical embodiment.
It identifies mechanical behavior as a difficult but valuable form of making.
Paper is framed as lightweight, malleable, inexpensive, and craft-compatible.
The system is a CAD environment and construction workflow, not merely a mechanism generator.
The paper values exploratory construction, familiar motion descriptions, and learning through physical prototyping.
The workshop study examines how teenagers design, build, interpret, and adapt mechanisms.
Findings are converted into design implications around accessibility, adaptability, expressiveness, and gradual skill development.
```

**Reusable writing lesson:**

FoldMecha is a strong example of how to write a toolkit paper that is technical enough for HCI but still centered on learning, making, and design exploration.

**Best reusable sentence pattern:**

```text
We designed the system to support exploratory construction, allowing learners to move between simulated motion, physical assembly, and creative adaptation.
```

### Paper Mechatronics and paper-based making work

**Observed rhetorical structure:**

```text
Paper is positioned as a familiar material with underused computational and mechanical potential.
The writing often connects paper craft to electronics, motion, sensing, and learning.
The paper-based medium is not justified only by low cost; it is justified by its capacity for adaptation, decoration, repair, and hands-on experimentation.
```

**Reusable writing lesson:**

Do not write “paper is cheap” as the entire motivation. The stronger claim is that paper changes the learning and design relationship because it is editable, visible, and culturally familiar.

**Best reusable sentence pattern:**

```text
Paper is valuable not only because it is inexpensive, but because it makes construction visible, modifiable, and approachable during the design process.
```

### PEP: 3D Printed Electronic Papercrafts

**Observed rhetorical structure:**

```text
The paper connects digital fabrication, paper craft, and electronics.
The writing frames the contribution as an integrated workflow rather than a single fabrication trick.
The system supports sculpting and constructing paper-based electronic devices.
The rhetorical emphasis is on bridging physical form-making and electronic function.
```

**Reusable writing lesson:**

For fabrication papers, emphasize the integration of workflow stages that are usually separated: form design, material construction, circuitry, and interaction.

**Best reusable sentence pattern:**

```text
The workflow integrates form-making and electronic function so that interactive behavior can be designed as part of the paper artifact rather than attached after construction.
```

### Sensing Kirigami

**Observed rhetorical structure:**

```text
The paper begins from a material-driven inquiry.
Paper is described as modest but rich in craft and design affordances.
Kirigami is framed through cutting, folding, and bending flat sheets into dynamic three-dimensional forms.
Carbon-coated paper is introduced as a material whose electrical resistance changes through folding and bending.
The paper uses material exploration to develop design propositions for tangible interfaces.
```

**Reusable writing lesson:**

Sensing Kirigami is a strong example of Oh-style material rhetoric: the technical sensor mechanism is inseparable from the material form and interaction affordance.

**Best reusable sentence pattern:**

```text
We treat [material transformation] as both a physical deformation and a computational signal, enabling interaction techniques that emerge from the material itself.
```

### Tangible-MakeCode and Making Computing Visible Toolkit family

**Observed rhetorical structure:**

```text
The papers/projects are positioned around physical computing education.
The writing emphasizes children, teachers, tangible programming, visible computational behavior, and classroom use.
The system contribution is tied to co-design, iterative development, and pilot studies rather than only technical novelty.
The evidence is oriented toward how learners and teachers understand, adapt, and use the toolkit.
```

**Reusable writing lesson:**

Educational HCI papers should write the system as a scaffold for understanding, not merely as a simplified interface.

**Best reusable sentence pattern:**

```text
The toolkit makes computational behavior visible and manipulable, allowing learners to connect physical actions with programming concepts during construction.
```

### Functional Destruction, SwellSense, SPIN, and related material-interface work

**Observed rhetorical structure:**

```text
The papers reframe unusual material properties as interaction resources.
Physical transiency, swelling, creasing, or energy harvesting are not treated only as engineering constraints.
They become design opportunities for new forms of interaction, feedback, sustainability, or self-powered interfaces.
The writing frequently turns material instability into a situated design feature.
```

**Reusable writing lesson:**

When a material is noisy, transient, deformable, or imprecise, avoid treating that only as a limitation. In HCI/design-computing rhetoric, the same property can become a design tension or opportunity.

**Best reusable sentence pattern:**

```text
Rather than treating [material behavior] only as a source of error, we examine how it can become a resource for interaction, feedback, and situated use.
```

---

# 17. Final Recommendation for Your Own Paper Writing

If your paper is primarily **robotics or AI**, use Ha-style rhetoric for the introduction and evaluation. Add Oh-style language only when discussing human-facing workflow, authoring, or deployment implications.

If your paper is primarily **HCI, design computing, fabrication, or tangible interaction**, use Oh-style rhetoric for the introduction, related work, study, and discussion. Use Ha-style rhetoric inside the technical system section to keep the mechanism precise.

If your paper is **Graphics/HCI**, start from the creative or material practice, narrow into a graphics/optimization/control bottleneck, and evaluate both:

```text
Can the system technically produce the intended result?
Can users/designers meaningfully inspect, control, modify, or appropriate that result?
```

If your paper is **AI/HCI**, start from the human practice, narrow into the AI capability gap, and evaluate both:

```text
Does the model perform under the intended constraints?
Does the interaction design help users understand, steer, repair, or appropriate the model output?
```

The strongest paper will not sound like a surface imitation of either writing style. It will use the correct **claim architecture**:

```text
Ha-style architecture:
Problem pressure → operational bottleneck → mechanism → measurable evidence → scoped technical implication.

Oh-style architecture:
Material/practice context → design opportunity → toolkit/workflow → situated evidence → design implication.

Hybrid architecture:
Human/material practice → technical bottleneck → integrated system → dual evaluation → field-level implication.
```
