# Reliability, performance and delivery

- Give external calls and long-running work deadlines, cancellation and resource limits. Retry only transient failures
  that are safe to replay, with bounded attempts, backoff and jitter. Before a retry, check for partial execution and
  external side effects: a timeout or an exception does not mean the work rolled back.
- Let failures surface. An empty result or a success response must not hide one; carry actionable context without
  exposing secrets or personal information.
- Optimize from representative measurements of latency, throughput, memory, queries or cost, and design cache
  freshness and invalidation explicitly.
- An operational change comes with the logs, metrics, health checks, alerts and recovery steps it needs; derive limits
  and service levels from real requirements.
- For a change to a user interface, run it and use the affected interactions, including keyboard access, responsive
  layout and the loading, empty, error and retry states.
- Before adding or upgrading a dependency, weigh necessity, alternatives, compatibility, security, license and lockfile
  impact; recency alone is not a reason.
- Review the final diff for debug leftovers, secrets, unneeded dependencies and generated files, and regenerate
  generated artifacts from their source. Split a large change into units that can be validated and released safely,
  and give a temporary feature flag its removal condition.
