# Feedback: An ambiguous answer to an approval question led to an unwanted outward-facing creation

- Date: 2026-11-26
- OneStep version used: 99cd60c (checkout HEAD on 2026-11-26; local working-tree edits present, not inspected for this concern)
- Relevant skills/instructions: skills/vegabond-scout/SKILL.md (Material ambiguity), agents/vegabond-agent.md
- Kind: suggestion
- Status: received
- Task context: A small code refactoring in a game repository. The user asked for an issue-tracker card to be created "after approval". The agent showed a card draft and asked for approval with options.

## Expected and observed

Expected: the agent creates the tracker card only after an unambiguous go-ahead, and every approval question offers a "do not create yet" choice.

Observed (AI observation, confirmed by user feedback): the user answered the approval question with a two-word reply that can mean either "revise the draft, then create" or "create after the code change is done". The agent took the first reading without confirming it. Its follow-up question offered only "create" variants, so the user's next answer created the card. The user had meant to wait, asked why the card was created without permission, and deleted it by hand. Impact: one unwanted public card in the team tracker, manual cleanup by the user, and lost trust in later approval questions.

## Evidence and suspected cause

- The scout "Material ambiguity" rule addresses interpretation of the task at kickoff: state the intended deliverable and ask when the choice belongs to the user. It does not say that the user's answer to a mid-task approval question can itself be ambiguous, and its "reversible choice: state your assumption and proceed" clause can be read as allowing an assumption for a card that can be deleted afterwards.
- The common contract has no rule for outward-facing actions (cards, merge requests, comments, messages) beyond what the host harness says.
- Suspected cause: mainly a failure to follow the host's own explicit-permission rule, with no OneStep safeguard that would have caught it. Not reproduced in a fresh session.

## Suggested improvement

Add one line to the scout Material ambiguity section, or to the common contract: "An answer to an approval question for an outward-facing or hard-to-reverse action (creating a ticket, merge request, comment or message) counts as approval only when it has one reading. If it can be read two ways, confirm the reading first. Every such approval question includes a neutral 'not yet' option. Deletability does not make the action reversible for this rule."

Check: in a controlled session, give an approval question an ambiguous reply such as "after the fix, create"; the improved behavior is a confirmation question with a "not yet" option and no creation call.

## Review and verification

Maintainer fills during processing.
