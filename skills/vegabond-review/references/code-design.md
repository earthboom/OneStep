# Software design review

Assess requirements, interfaces, ownership, state transitions and failure mechanisms in a proposed design. Use the relevant sections of the existing [design review](../../vegabond-code-design/references/review.md); this review does not start implementation.

- Trace each important requirement to an enforcing mechanism, assumptions and an observable acceptance check. Distinguish a promised guarantee from its mechanism.
- Challenge important boundaries with a concrete event sequence: partial completion, unknown outcome, retry, cancellation, ownership changes or mixed-version callers as relevant. A local lock or unique database key does not automatically constrain external effects.
- Compare viable alternatives under the same constraints when the choice matters. Explain cost, complexity, operational burden and the condition that would change the recommendation. Avoid inventing alternatives to a settled local choice.
- Identify prerequisites needed before dependent work separately from checks possible only after implementation. A future test plan cannot resolve a missing design premise.

Report the specific invariant or decision affected, counterexample or source evidence, tradeoff, and bounded next step. Preserve the required guarantee when proposing a repair; label any alternative that weakens it. Design consistency is not proof of working code, measured capacity or production readiness.
