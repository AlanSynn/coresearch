# Design

Give the problem the design it warrants: simple where the domain is simple, explicit boundaries where change,
ownership or consistency demand them.

## Simplicity and code quality

- Build what the problem needs now. A speculative feature, a one-use abstraction, a generic framework or configuration
  without a concrete need costs more to read than it saves, and so does indirection that adds no branch or boundary.
- Follow the repository's conventions. Readable code has meaningful names, cohesive modules, explicit dependencies and
  plain control flow; fewer lines, short names and dense one-liners are not simplicity. Comments give non-obvious
  reasons and constraints, not what the code already says.
- Reuse existing logic where it stays correct. Before you consolidate or remove code, keep the behavior its callers
  rely on unless the task is to change it.
- Apply DRY to duplicated knowledge, not to code that looks alike but changes for different reasons.
- Separate pure computation from I/O and side effects, and use types and contracts where they make correctness easier
  to see.
- Remove dead code your change creates. Whether to also fix nearby debt depends on who owns the design, which the
  working agreement and the repository's instructions settle; otherwise report it.

## SOLID as criteria

Use SOLID to judge change impact and dependency direction, not as ceremony: group code by its reason to change, isolate
variation you have actually seen, keep substitutable implementations true to their callers' contracts (preconditions,
outcomes, errors and side effects), give consumers focused interfaces, and keep core policy independent of
infrastructure. Use the language's natural functions, modules, protocols or types; not every class needs an interface.

## Domain-driven design, when the domain is complex

- Keep CRUD, scripts, prototypes and research code simple. Introduce domain models and tactical patterns when business
  rules or consistency requirements justify them.
- Domain-driven design does not mean microservices, CQRS or event sourcing. A new system starts as a modular monolith
  unless actual constraints justify another deployment structure.
- In a complex domain, use one vocabulary in discussion, code and tests; make each Bounded Context's responsibilities,
  data ownership and public contracts explicit; and put an anti-corruption layer where an external model would distort
  the local one.
- Draw Aggregates around invariants and consistency boundaries, and let callers change state only through the
  Aggregate's behavior. Business rules belong in the domain; coordination, authorization and transactions in the
  application layer. Repositories serve Aggregate access, not every table or read-only query.
- Across boundaries, say what "eventually consistent" means: acceptable delay, duplicates, ordering and compensation.
  Keep internal domain events distinct from published integration events.

## Boundaries

- Understand the existing architecture before you change it. Before changing architecture, public contracts,
  authorization or persistence, weigh the alternatives, compatibility, migration and recovery.
- Cross boundaries through explicit contracts, not through another context's internals or data. Keep ORM entities and
  external SDK types out of core interfaces unless you state the trade-off.
- Add services, layers and shared kernels for a demonstrated operational, security, performance or ownership need.

## Design records

- Record a consequential decision with its context, alternatives, decision, rationale, consequences and the trigger to
  revisit it, in the repository's ADR format when it has one. A change with no design impact needs no document.
- Mark decisions as proposed, accepted or superseded, and claim approval only where it was given. Update the affected
  glossaries, context maps and contract documents in the same change, and keep current and intended architecture
  apart.
- Make important constraints executable where practical (forbidden dependencies, cycles, contract compatibility,
  invariants), and confirm that a new check exercises its target. Baseline existing violations instead of adding new
  ones, and record an exception with its reason and the condition for revisiting it.
