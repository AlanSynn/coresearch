# Testing and verification

Choose checks by risk: what could this change break, and what evidence would show that it did not?

- A bug fix comes with a regression test that fails on the old code, when that is feasible. A feature gets
  representative examples and edge cases; a risky refactor gets characterization tests first. A new test earns its
  place by catching something the existing suite would miss.
- Test domain rules with fast unit tests, external boundaries with integration or contract tests, and critical user
  journeys end to end. Assert observable contracts rather than implementation details, do not mock away the rule under
  test, and control time, randomness, network and external state.
- Property-based, fuzz, metamorphic or mutation testing pays off for risky parsers, state machines, numerical code and
  invariants. Coverage alone is not evidence of correctness.
- Run the relevant checks before the change when you can, so that failures that were already there stay separate from
  regressions you introduce.
- Missing evidence, malformed verifier output and verifier errors are inconclusive, not passes. A completion signal or
  another model's approval does not replace an acceptance check.
- Record the cause of a flaky check, and say why when an expectation legitimately changes.
