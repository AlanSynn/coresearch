# Design: simplicity, SOLID, DDD and architecture

## 5. Simplicity, scope, and code quality
- Implement only what the request requires. Avoid speculative features, one-use abstractions, generic frameworks, and configuration without a concrete need.
- Follow established conventions. Prefer meaningful names, cohesive modules, explicit dependencies, and readable control flow. Explain non-obvious reasons and constraints in comments, not what the code already says.
- Prefer composition where it reduces coupling. Separate pure computation from I/O and side effects; use types and contracts where they improve correctness without manufacturing object hierarchies.
- Apply DRY to duplicated knowledge, not coincidentally similar syntax or concepts from different domains. Balance reuse with KISS and YAGNI.
- Keep unrelated cleanup, renaming, and bulk formatting out of the change. Remove dead code created by your edits; report unrelated debt instead of expanding scope.

## 6. Apply SOLID as design criteria
- **SRP:** Group code by coherent responsibility and reason to change. Do not split classes or functions mechanically to satisfy a size threshold.
- **OCP:** Isolate demonstrated variation behind stable extension points. Do not forbid ordinary edits or invent abstractions for hypothetical extensions.
- **LSP:** Substitutable implementations must preserve caller-visible preconditions, outcomes, errors, and side-effect contracts. Use shared contract tests where substitution matters.
- **ISP:** Provide focused contracts tailored to consumers. Do not make a caller depend on unrelated capabilities or a universal interface.
- **DIP:** Keep core policy independent of infrastructure details. Introduce ports at meaningful volatility or testing boundaries and compose implementations externally; not every class needs an interface.
- Use the language's natural functions, modules, protocols, or types. SOLID guides change impact and dependency direction; it does not require object-oriented ceremony.

## 7. DDD: domain meaning and strategic boundaries
- Establish the user goal, domain rules, and important examples. Use a consistent Ubiquitous Language in discussions, code, and tests; clarify genuinely ambiguous business terms.
- For complex domains, distinguish core, supporting, and generic subdomains. Make Bounded Context responsibilities, model boundaries, data ownership, and public contracts explicit.
- Maintain a Context Map when integrations matter. Preserve context-specific meanings and use an Anti-Corruption Layer where external models would distort the local domain.
- Do not equate Domain-Driven Design with microservices, CQRS, or event sourcing. For a new system, consider a modular monolith unless actual constraints justify another deployment structure.
- Keep simple CRUD, scripts, and prototypes simple. Introduce rich models and tactical patterns only when business complexity or consistency requirements justify them.

## 8. DDD: invariants and state transitions
- Distinguish Entity identity from Value Object equality. Validate meaningful Value Objects at construction and keep them immutable when appropriate.
- Define Aggregates around invariants and consistency boundaries. Expose intent through the Aggregate Root; do not let callers bypass domain behavior and mutate internal state arbitrarily.
- Put business rules in the domain and use-case coordination, authorization enforcement, and transaction orchestration in the application layer. Use Domain Services for genuine domain behavior that does not belong to one object.
- Enforce strongly consistent rules within an atomic boundary or explicitly design coordination. Across boundaries, specify acceptable delay, duplicate handling, ordering, and compensation rather than merely saying "eventual consistency."
- Use Repositories for meaningful Aggregate access, not mechanically for every table. Do not force read-only queries through unnecessary Aggregate reconstruction.
- Distinguish internal domain events from published integration events. When events are warranted, define publication timing, delivery failure handling, idempotency, and schema evolution.

## 9. Architecture and dependency boundaries
- Understand the existing architecture before changing it. In new domain boundaries, keep business policy independent of UI, transport, persistence, and framework implementation details.
- Cross boundaries through explicit contracts. Avoid leaking ORM entities or external SDK types into core domain interfaces without a justified tradeoff.
- Do not bypass another Context's ownership through internal imports or direct writes to its data. Use its supported API, events, or explicitly approved integration contract.
- Distinguish logical boundaries from deployment units. Add services, layers, and shared kernels only for demonstrated operational, security, performance, or ownership needs.

## 10. Maintain the design continuously
- For meaningful behavior changes, assess effects on terminology, Contexts, invariants, contracts, dependencies, quality attributes, and migration or recovery. No design impact means no extra document is required.
- Record consequential decisions using the existing ADR format. Otherwise, capture context, alternatives, decision, rationale, consequences, risks, verification, and revisit triggers concisely.
- Distinguish proposed, accepted, and superseded decisions. Do not claim approval that was not given; preserve decision history when replacing an earlier choice.
- Update affected glossaries, Context Maps, diagrams, and contract documentation in the same change set. Distinguish current architecture from intended architecture; do not duplicate obvious code facts.
- Make important constraints executable where practical: forbidden dependencies, cycles, ownership boundaries, contract compatibility, and domain invariants. Confirm that new checks actually select and exercise their intended targets.
- Baseline existing violations without adding new ones. Document exceptions with a reason, known owner, and removal or review condition; do not invent owners or deadlines.
- Revisit affected decisions when requirements, scale, incidents, trust boundaries, or major dependencies change. Do not use documentation maintenance as a pretext for an unrelated redesign.
