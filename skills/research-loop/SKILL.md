---
name: research-loop
description: OMX-compatible autonomous research mission design for AI, graphics, HCI, or technical research projects. Use when the user wants to start, steer, or audit an autonomous research loop, define hypotheses and experiments, create validator-gated success criteria, or hand off to OMX autoresearch without creating ad-hoc .agents state.
---

# Research Loop

Design a research loop that can run cumulatively in chat or hand off to OMX `$autoresearch`. The loop is artifact-gated: progress is complete only when evidence artifacts satisfy explicit validators, not when an agent says it is done.

## When to use

Use this skill for:

- starting a multi-hypothesis research project;
- turning an idea into experiments and stop conditions;
- creating an OMX autoresearch mission after `$deep-interview --autoresearch`;
- auditing an existing autonomous loop for weak validators, unsafe assumptions, or unverifiable claims.

For ordinary paper planning, use `paper-design`. For implementation of a specific experiment, use `research-engineer`.

## Inputs

Use available project notes, repo state, papers, datasets, constraints, target venue, compute budget, and desired artifacts. Ask one concise question only if the research objective or success metric is impossible to infer.

## Workflow

1. **Define mission.** State the research objective, domain, intended contribution, and non-goals.
2. **State hypotheses.** List 2–5 hypotheses or design questions, each tied to evidence.
3. **Specify artifacts.** Code, logs, tables, figures, datasets, study notes, benchmark outputs, or manuscript sections.
4. **Define validators.** For each artifact, define a pass/fail check, threshold, reviewer-usefulness test, or human-inspection criterion.
5. **Set sandbox boundaries.** Allowed files, datasets, external calls, compute limits, credentials, privacy/confidentiality limits, and destructive-operation policy.
6. **Plan the loop.** Inner experiment loop, outer synthesis loop, reflection cadence, and stop conditions.
7. **Score the research risk.** Novelty, evidence, reproducibility, ethics, and venue-fit risks.
8. **Choose handoff.** Stay in chat, create requested files, or hand off to `$deep-interview --autoresearch` / `$autoresearch` when OMX runtime is active.

## OMX handoff rules

- Do not create `.agents/` chats or mailboxes.
- Do not create `.omx/specs/...` unless the user explicitly asks for files or an OMX autoresearch workflow is being invoked.
- If creating OMX mission files, prefer `.omx/specs/autoresearch-{slug}/mission.md`, `sandbox.md`, and `result.json` as the durable contract.
- Keep validators executable or inspectable. Avoid vague goals such as “improve results” without a metric, evidence artifact, or review criterion.

## Output schema

```markdown
# Research Mission Contract

## Mission
- Objective:
- Domain / venue mode:
- Intended contribution:
- Non-goals:

## Hypotheses / Research Questions
| ID | Hypothesis or question | Evidence needed | Artifact | Validator | Risk |
|---|---|---|---|---|---|

## Loop Design
### Inner Loop
[Experiment/build/analyze iteration steps.]

### Outer Loop
[Synthesis, decision, pivot, and reflection steps.]

## Sandbox and Permissions
- Allowed files / directories:
- Allowed data / models / APIs:
- Compute or time limits:
- Credentials / private data boundary:
- Destructive operations:

## Stop Conditions
- Success:
- Blocked:
- Failure:
- Human decision required:

## OMX Handoff
- Recommended lane: [chat / $deep-interview --autoresearch / $autoresearch / $ralplan / $team]
- Files to create only if authorized:
- Validation evidence required before completion:

## Immediate Next Actions
1. [Highest-impact next action]
2. [Next action]
3. [Next action]
```
