# APIs, data, events and migrations

## 12. APIs, data, events, and migrations
- Validate untrusted input at boundaries and preserve core invariants internally. Distinguish null, absence, empty results, and errors; provide stable error contracts.
- Assess compatibility for public APIs, events, and stored representations. Breaking changes require consumer impact analysis, transition steps, and an explicit deprecation or versioning strategy.
- Review transactions, constraints, concurrent updates, and duplicate requests. Represent money, time, units, and identifiers according to their domain semantics.
- Plan schema changes around operational constraints, using staged expansion, migration, and contraction where suitable. Test locks, backfills, partial failure, and recovery; identify irreversible steps and forward-fix options.
- When database updates and message publication must be coordinated, evaluate a transactional outbox or another justified mechanism. Do not assume exactly-once transport; handle replay, duplication, and reordering.
