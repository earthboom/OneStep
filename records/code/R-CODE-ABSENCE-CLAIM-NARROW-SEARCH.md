---
id: R-CODE-ABSENCE-CLAIM-NARROW-SEARCH
title: A design said a class of objects had no kind identifier after searching only for dedicated type tags
summary: A design claimed that runtime objects of one category carried no kind identifier and chose a broader selection rule because of it. The identifier existed as the data row's identity tag, published on the object by a shared data component; the search had covered only the tag names the author expected.
kind: error
scope: Design evidence for a data-driven Unreal Engine game; any claim that an identifier, field or hook does not exist
keywords: [absence claim, negative claim, search scope, design evidence, data row schema, identity tag, gameplay tag, FGameplayTagContainer, data component, allowlist, selection rule, unverified assumption]
status: resolved
checked_at: '2026-11-24'
trigger: Writing a design claim that something does not exist, based on a search for the names the author expected it to have
symptom: The claim was false, and the design built a wider, costlier selection rule on it until a reader asked whether the selection could be set up in data
cause_status: confirmed
prevention: Before an absence claim, list the fields of the object's data row schema and each place the runtime object publishes row data, and write the search terms and scope beside the claim
prevention_status: proposed
relations:
  prevention: [K-CODE-UE-TAGQUERY-EMPTY-MATCH]
---

## Expected and observed

A design document states what exists and what does not, each with its basis, so that the chosen structure follows from the codebase as it is.

A design for "this hazard breaks objects of one kind" stated that such objects carry no kind identifier at runtime. From that it selected targets by a generic rule (collision object types plus a remaining-durability check), which would also have selected other kinds and needed extra exclusions. A reader asked whether the set of breakable objects could be configured in data. Rereading the data row schema showed that every row has an identity tag, and that a shared data component adds that tag to the object's gameplay tag container when the object is initialized. The identifier the design said was missing had been there all along.

## Cause and resolution

Cause is confirmed. The search behind the claim looked for dedicated type and state tag families by their expected names. It did not enumerate the fields of the data row that describes the object, and it did not look for the code that copies row data onto the runtime object. An identifier stored under a general name (the row's identity) was therefore invisible to the search, and "not found by this search" was written as "does not exist".

The design was revised: targets are selected by a designer-authored tag condition held in a data asset, matched against the object's tag container, and the absence claim was replaced by the location of the publishing code and the count of matching data rows. The revision is a document change checked by reading code and data; nothing was built or run.

## Recheck and prevention

Correction check, 2026-11-24: the publishing line and the data rows were reread, and the rows the new condition is meant to match were counted from the exported data.

Proposed safeguard, not demonstrated: an absence claim in a design is written only after (1) listing the schema fields of the data that defines the object, (2) finding where the runtime object receives or publishes that data, and (3) recording the search terms and scope next to the claim, so a reader can see what the search could not have found. A claim that cannot meet this is marked as an unverified hypothesis. Selecting by an identifier that was found this way usually leads to a tag condition used as an allowlist, whose unset case needs its own check; see the linked knowledge entry.

The safeguard was not applied to a second case, so its detection ability is untested.

## Evidence

- The originating project's defect log entry for this design revision and the two design revisions, kept in that project; they are not published artifacts.
- [Empty tag condition semantics](../../knowledge/code/K-CODE-UE-TAGQUERY-EMPTY-MATCH.md) for the allowlist follow-up.
