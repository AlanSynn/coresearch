---
name: engineering
description: Engineering judgment for changing architecture, domain models, public APIs, stored data and migrations, or test strategy. A local fix does not need it.
---

# Engineering

The user's engineering stances for consequential changes: criteria for judging a design, not a procedure to follow.
Scope, approvals, evidence and reports are in the working agreement, and the repository's own instructions come
first. Read only the reference that matches the change in front of you.

| Change | Reference |
|---|---|
| Structure, modules and boundaries; domain models; design records | [Design](references/design.md) |
| What to test and what counts as verification | [Testing](references/testing.md) |
| Public APIs, stored data, events, schema migrations | [Data and APIs](references/data-and-apis.md) |
| Reliability, performance, interfaces, dependencies, release | [Operations](references/operations.md) |
| Trust boundaries, secrets, untrusted input, destructive operations | [Security](references/security.md) |
| Notebooks and other persistent state, visual output, parallel agents, long tasks | [Workspaces](references/workspaces.md) |
