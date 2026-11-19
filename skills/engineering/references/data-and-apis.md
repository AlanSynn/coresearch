# APIs, data, events and migrations

- Validate untrusted input at boundaries and keep core invariants inside. Keep null, absence, empty results and errors
  distinct, and give errors a stable contract.
- Public APIs, events and stored representations are contracts with consumers you may not see. A breaking change needs
  an analysis of its consumers, transition steps and a deprecation or versioning plan.
- Review transactions, constraints, concurrent updates and duplicate requests. Represent money, time, units and
  identifiers by their domain meaning.
- Plan schema changes around operational constraints, with staged expand, migrate and contract steps where they fit.
  Exercise locks, backfills, partial failure and recovery, and name the irreversible steps and the forward fix.
- When a database update and a message must happen together, consider a transactional outbox or another justified
  mechanism. Transport is not exactly-once: handle replay, duplication and reordering.
- Check version-sensitive APIs and configuration against the installed version and its primary documentation. When you
  rely on an external implementation, read the relevant code and record its revision, not only its README.
