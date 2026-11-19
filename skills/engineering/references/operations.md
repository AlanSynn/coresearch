# Reliability, performance and delivery

## 13. Reliability, performance, and user experience
- Give external calls and long-running work appropriate deadlines, cancellation, and resource limits. Retry only transient failures with safe replay, bounded attempts, backoff, and jitter.
- Do not disguise failures as empty data or successful responses. Propagate actionable context without exposing secrets or unnecessary personal information.
- Optimize from representative measurements. Compare the relevant latency, throughput, memory, queries, or cost; design cache freshness, invalidation, and consistency explicitly.
- Include necessary logs, metrics, traces, health checks, alerts, and recovery procedures for operational changes. Derive SLOs and limits from real requirements rather than invented targets.
- For UI changes, inspect the running interface and exercise the affected interactions. Check relevant keyboard access, accessibility, responsive behavior, loading, empty, error, and retry states.

## 18. Delivery and operational readiness
- Review the final diff for scope creep, debug leftovers, secrets, unnecessary dependencies, and generated files. Maintain generated artifacts through their source and documented regeneration path.
- Before adding or upgrading dependencies, check necessity, alternatives, compatibility, security, licensing, and lockfile impact. Novelty and recency alone are not reasons to adopt a tool.
- Split large changes into units that can be validated and deployed safely. Give temporary feature flags removal conditions; keep deployment and rollback within approved procedures.
- Commit, push, or create a pull request only when requested or explicitly authorized. Include only your intended changes, not unrelated user or agent work.
