---
name: engineering
description: Engineering policy for changes to architecture, domain models, public contracts, persistence, migrations or test strategy.
---

# Engineering policy

Alan's engineering policy (English v2, 2026-09-29), an independent synthesis rather than an official vendor policy. It
scales with the risk of the change: a small local fix needs none of it. Read only the reference that matches the
change in front of you.

| Change | Reference |
|---|---|
| Planning a multi-file change, executing in short loops, reporting completion | [Process](references/process.md) |
| Simplicity, SOLID, Domain-Driven Design, architecture and design records | [Design](references/design.md) |
| Test strategy and verification evidence | [Testing](references/testing.md) |
| Public APIs, stored data, events, schema migrations | [Data and APIs](references/data-and-apis.md) |
| Reliability, performance, user-facing quality, delivery and dependencies | [Operations](references/operations.md) |
| Trust boundaries, secrets, destructive or consequential actions | [Security](references/security.md) |
| Executable workspaces, persistent state, agent context, parallel work | [Workspaces](references/workspaces.md) |
