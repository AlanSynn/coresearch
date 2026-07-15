---
name: research-loop
description: Autonomous research mission and validator-gated loop design for AI, graphics, HCI, or technical research projects. Use when the user wants to start, steer, or audit an autonomous research loop, define hypotheses and experiments, or create artifact validators, sandbox limits, and stop conditions. Optionally hands off execution to `$autoresearch` when an OMX install is present; does not create ad-hoc `.agents/` state.
---

# Research Loop

Design an artifact-gated research loop: progress is complete only when evidence
artifacts satisfy explicit validators — not when an agent says it is done. Run
cumulatively in chat (default); if OMX is installed, optionally hand off
execution to `$autoresearch`.

## What & When

Start, steer, or audit autonomous research missions; convert hypotheses into
artifacts, validators, sandbox limits, stop conditions, OMX handoff contracts;
default to chat-only execution; if OMX is installed, `$autoresearch`, `$ralplan`, and `$team` are optional OMX executors.
Use when: starting a multi-hypothesis project; turning an idea into experiments
and stop conditions; creating an OMX mission after `$deep-interview
--autoresearch`; auditing an existing loop for weak validators, unsafe
assumptions, or unverifiable claims. Not for: ordinary paper planning →
`research-design`; single experiment implementation → `research-engineer`;
creating legacy `.agents/` state, mailboxes, or ad-hoc multi-agent frameworks.

## Procedure

- **Define mission** — objective, domain, intended contribution, non-goals.
- **State hypotheses** — 2–5 hypotheses or design questions, each tied to evidence.
- **Specify artifacts** — code, logs, tables, figures, datasets, study notes,
  benchmark outputs, manuscript sections.
- **Define validators** — for each artifact, a pass/fail check, threshold,
  reviewer-usefulness test, or human-inspection criterion.
- **Set sandbox boundaries** — allowed files, datasets, external calls, compute
  limits, credentials, privacy/confidentiality, destructive-operation policy.
- **Plan the loop** — inner experiment loop, outer synthesis loop, reflection
  cadence, stop conditions.
- **Score research risk** — novelty, evidence, reproducibility, ethics, venue-fit.
- **Choose handoff** — stay in chat, create requested files, or hand off to
  `$deep-interview --autoresearch` / `$autoresearch` when OMX runtime is active.
  Execute with `$autoresearch` only after validator mode exists.

## Output

Research Mission Contract:
- **Mission** — Objective / Domain & venue mode / Intended contribution / Non-goals.
- **Hypotheses / Research Questions** — table: ID / hypothesis or question /
  evidence needed / artifact / validator / risk.
- **Loop Design** — Inner Loop (experiment/build/analyze iteration) + Outer Loop
  (synthesis, decision, pivot, reflection).
- **Sandbox and Permissions** — allowed files & directories / allowed data,
  models, APIs / compute or time limits / credentials & private-data boundary /
  destructive operations.
- **Stop Conditions** — Success / Blocked / Failure / Human decision required.
- **OMX Handoff** — recommended lane (chat / `$deep-interview --autoresearch` /
  `$autoresearch` / `$ralplan` / `$team`) / files to create only if authorized /
  validation evidence required before completion.
- **Immediate Next Actions** — ordered list, highest-impact first.

## Reject when

- completion claimed by "agent says done" with no validator passed;
- a goal lacks a metric, evidence artifact, or review criterion — "improve
  results" is not a validator;
- a claim needs human/official evidence and has none.

## State & Handoff

Canonical Coresearch state is the orchestrator `ledger.yaml`
(state-ledger.md); skills never write state inside their own directory.
Otherwise state lives in chat, or in `.omx/` only when an OMX workflow is
active or requested. Do not create `.agents/` chats or mailboxes. Write an OMX
`.omx/specs/autoresearch-{slug}/mission.md`, `sandbox.md`, and `result.json`
only when an OMX autoresearch workflow is invoked or the user asks — those are
the OMX runtime's mirror of this mission contract, not the canonical
Coresearch state. Keep validators executable or inspectable. In a multi-skill
run, seed `hypothesis_state.candidates` (each with a falsifier) to the ledger
so research-causal can extend them; standalone, the mission contract above is
enough. Next: `$autoresearch` (OMX runtime, only when installed) /
`research-design` (scope narrows to a paper) / `research-engineer` (single
experiment).

Re-entry: return to `coresearch` to re-route the next stage.
