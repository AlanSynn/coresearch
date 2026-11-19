# Testing and verification

## 11. Trustworthy testing and verification
- Reproduce bugs with a failing regression test when feasible. Define representative examples and edge cases for features; characterize behavior before risky refactors.
- Test domain rules with fast unit tests, external boundaries with integration or contract tests, and critical user journeys end to end. Select checks by risk and impact, not by habit.
- Assert observable contracts rather than incidental implementation details. Do not mock away the rule under test; control time, randomness, network dependencies, and external state.
- Use property-based, fuzz, metamorphic, or mutation testing when it meaningfully strengthens risky parsers, state machines, numerical logic, or invariants. A coverage percentage alone is not evidence of correctness.
- Do not delete, skip, or weaken tests to manufacture a pass. Explain legitimate expectation changes and record the causes of flaky checks.
- Start with focused tests and expand to relevant lint, type, build, and regression checks. Record actual commands and outcomes, including checks not run.
- Treat missing evidence, malformed verifier output, and verifier errors as inconclusive, not successful. Formatting compliance, a completion signal, and an LLM's approval are not substitutes for acceptance checks.
