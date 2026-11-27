# Code review

Inspect implemented behavior against its contract. Establish the changed revision or diff and relevant callers, data ownership and environment; expand beyond changed lines only for real dependencies. For a diff review, distinguish newly introduced defects from relevant pre-existing ones.

- Trace inputs, state transitions, outputs, errors and cleanup. Challenge boundary values, repeated operations, partial failures and concurrency only where reachable in this code.
- Check compatibility, security boundaries, resource lifetime and performance against actual use. Describe a concrete trigger and consequence; a disliked pattern or imagined workload alone is not a defect.
- Inspect tests for observable behavior and meaningful failure cases. A passing test is limited to what it exercises; an absent test does not by itself establish broken behavior.
- Use a focused reproduction or test when needed and authorized. Label static reasoning separately from executed evidence. Do not run unfamiliar code with external side effects merely to complete a review.

Use [software verification](../../vegabond-code/references/verification.md) when selecting runtime checks; apply only the relevant scope. If the issue concerns an unimplemented mechanism or architectural guarantee, add [code-design](code-design.md).

Findings should name the affected path/lines or symbol, trigger, expected versus actual behavior, and impact. Suggest a correction at the cause without silently implementing it. A static review cannot claim a successful build, runtime behavior, or performance measurement.
